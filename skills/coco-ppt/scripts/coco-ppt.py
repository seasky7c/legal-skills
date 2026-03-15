#!/usr/bin/env python3
"""
COCA-PPT 主命令行工具

智能 PPT 生成技能 - 自动识别模板版式并匹配内容
"""

import sys
import click
from pathlib import Path
from rich.console import Console

# 添加项目路径
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.loader.template_loader import TemplateLoader
from src.loader.content_loader import ContentLoader
from src.analyzer.layout_analyzer import LayoutAnalyzer
from src.analyzer.content_analyzer import ContentAnalyzer
from src.analyzer.matcher import LayoutMatcher
from src.generator.assembler import SlideAssembler
from src.generator.content_applier import ContentApplier
from src.generator.validator import SlideValidator
from src.utils.logger import get_logger
from src.utils.thumbnail import generate_thumbnails

console = Console()
logger = get_logger("coco-ppt")


@click.command()
@click.option('--template', required=True, help='PPTX 模板文件路径')
@click.option('--outline', help='Markdown 大纲文件路径')
@click.option('--content', help='JSON 内容文件路径')
@click.option('--output', required=True, help='输出 PPTX 文件路径')
@click.option('--report', is_flag=True, help='生成详细匹配报告')
@click.option('--thumbnails', is_flag=True, help='生成缩略图预览')
@click.option('--analyze-only', is_flag=True, help='仅分析不生成')
@click.option('--interactive', is_flag=True, help='交互式选择版式')
@click.option('--debug', is_flag=True, help='调试模式')
@click.option('--log-level', default='INFO', 
              type=click.Choice(['DEBUG', 'INFO', 'WARNING', 'ERROR']),
              help='日志级别')
def main(template, outline, content, output, report, thumbnails, 
         analyze_only, interactive, debug, log_level):
    """
    COCO-PPT - 智能 PPT 生成工具
    
    自动识别 PPT 模板版式并匹配内容生成演示文稿
    """
    # 设置日志级别
    if debug:
        log_level = 'DEBUG'
    
    global logger
    logger = get_logger("coco-ppt", log_level)
    
    # 验证输入
    if not outline and not content:
        console.print("[red]错误：必须提供 --outline 或 --content[/red]")
        sys.exit(1)
    
    if outline and content:
        console.print("[yellow]警告：同时提供了 --outline 和 --content，将使用 --outline[/yellow]")
    
    try:
        # Step 1: 加载模板
        logger.step("加载模板")
        template_loader = TemplateLoader(template)
        prs = template_loader.load()
        
        # 验证模板
        validation = template_loader.validate()
        if not validation.is_valid:
            console.print("[red]模板验证失败:[/red]")
            for error in validation.errors:
                console.print(f"  - {error}")
            sys.exit(1)
        
        console.print(f"[green]✓[/green] 模板加载成功：{validation.slide_count}张幻灯片，{validation.layout_count}个版式")
        
        for warning in validation.warnings:
            console.print(f"[yellow]⚠ {warning}[/yellow]")
        
        # Step 2: 加载内容
        logger.step("加载内容")
        content_loader = ContentLoader()
        
        if outline:
            if not Path(outline).exists():
                console.print(f"[red]错误：大纲文件不存在：{outline}[/red]")
                sys.exit(1)
            pres_content = content_loader.load_outline(outline)
        else:
            if not Path(content).exists():
                console.print(f"[red]错误：内容文件不存在：{content}[/red]")
                sys.exit(1)
            pres_content = content_loader.load_content(content)
        
        console.print(f"[green]✓[/green] 内容加载成功：{len(pres_content.slides)}张幻灯片")
        
        # Step 3: 分析版式
        logger.step("分析版式")
        layout_analyzer = LayoutAnalyzer()
        layouts = layout_analyzer.analyze(prs)
        
        # 统计版式类型
        layout_types = {}
        for layout in layouts:
            lt = layout.layout_type
            layout_types[lt] = layout_types.get(lt, 0) + 1
        
        console.print(f"[green]✓[/green] 版式分析完成")
        for lt, count in sorted(layout_types.items()):
            console.print(f"  - {lt}: {count}个")
        
        if analyze_only:
            # 仅分析模式
            if report:
                console.print("\n[bold]版式档案:[/bold]")
                for profile in layout_analyzer.export_profiles():
                    console.print(f"  幻灯片 {profile['slide_index']}: {profile['layout_type']} "
                                f"(置信度：{profile['confidence']:.2f})")
            return
        
        # Step 4: 分析内容
        logger.step("分析内容")
        content_analyzer = ContentAnalyzer()
        requirements = content_analyzer.analyze(pres_content)
        
        console.print(f"[green]✓[/green] 内容分析完成")
        
        # Step 5: 智能匹配
        logger.step("智能匹配")
        matcher = LayoutMatcher()
        matches = matcher.match_all(requirements, layout_analyzer.layout_profiles)
        
        console.print(f"[green]✓[/green] 匹配完成，平均分数：{sum(m.score for m in matches) / len(matches):.2f}")
        
        # 显示低分匹配警告
        low_conf = matcher.get_low_confidence_matches(threshold=0.7)
        if low_conf:
            console.print(f"[yellow]⚠ {len(low_conf)}个低置信度匹配，可能需要手动调整[/yellow]")
        
        if report:
            console.print("\n" + matcher.generate_report())
        
        if analyze_only:
            return
        
        # Step 6: 组装幻灯片
        logger.step("组装幻灯片")
        assembler = SlideAssembler(prs)
        output_prs = assembler.assemble(matches)
        
        console.print(f"[green]✓[/green] 组装完成：{assembler.get_slide_count()}张幻灯片")
        
        # Step 7: 应用内容
        logger.step("应用内容")
        applier = ContentApplier(output_prs)
        issues = applier.apply_all(matches)
        
        if issues:
            console.print(f"[yellow]⚠ 内容应用发现{len(issues)}个问题[/yellow]")
        else:
            console.print(f"[green]✓[/green] 内容应用完成")
        
        # Step 8: 质量验证
        logger.step("质量验证")
        validator = SlideValidator(output_prs)
        validation_result = validator.validate()
        
        if report:
            console.print("\n" + validator.generate_report(validation_result))
        
        if not validation_result.is_valid:
            console.print("[red]⚠ 验证发现错误，但仍会保存文件[/red]")
        
        # Step 9: 保存结果
        logger.step("保存结果")
        
        # 确保输出目录存在
        output_path = Path(output)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        assembler.save(str(output_path))
        console.print(f"[green]✓[/green] 已保存：{output}")
        
        # Step 10: 生成缩略图
        if thumbnails:
            logger.step("生成缩略图")
            thumb_path = generate_thumbnails(str(output_path), str(output_path.parent))
            if thumb_path:
                console.print(f"[green]✓[/green] 缩略图：{thumb_path}")
            else:
                console.print("[yellow]⚠ 缩略图生成失败（需要安装 LibreOffice）[/yellow]")
        
        # 完成
        console.print("\n[bold green]🎉 生成完成！[/bold green]")
        
    except FileNotFoundError as e:
        console.print(f"[red]错误：{e}[/red]")
        sys.exit(1)
    except Exception as e:
        console.print(f"[red]错误：{e}[/red]")
        if debug:
            import traceback
            traceback.print_exc()
        sys.exit(1)


if __name__ == '__main__':
    main()
