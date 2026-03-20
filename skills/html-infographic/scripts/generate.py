#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
HTML Infographic Generator - 专业版
支持多色系、多风格、多终端适配，可从参考图提取设计参数
"""

import os
import sys
import re
import json
import click
from datetime import datetime
from pathlib import Path

try:
    import markdown
except ImportError:
    print("⚠️  缺少依赖：pip install markdown click")
    sys.exit(1)


# ============== 设计参数库 ==============

COLOR_SCHEMES = {
    '紫蓝渐变': {
        'primary': '#667eea',
        'primary-light': '#764ba2',
        'accent': '#4facfe',
        'gradient': 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
        'description': '科技、数据、商务报告'
    },
    '青绿清新': {
        'primary': '#11998e',
        'primary-light': '#38ef7d',
        'accent': '#0ba360',
        'gradient': 'linear-gradient(135deg, #11998e 0%, #38ef7d 100%)',
        'description': '环保、健康、教育、成长主题'
    },
    '橙红活力': {
        'primary': '#f093fb',
        'primary-light': '#f5576c',
        'accent': '#fa709a',
        'gradient': 'linear-gradient(135deg, #f093fb 0%, #f5576c 100%)',
        'description': '营销、活动、创意、年轻化内容'
    },
    '深蓝专业': {
        'primary': '#1e3c72',
        'primary-light': '#2a5298',
        'accent': '#4facfe',
        'gradient': 'linear-gradient(135deg, #1e3c72 0%, #2a5298 100%)',
        'description': '政府、金融、法律、正式报告'
    },
    '极简黑白': {
        'primary': '#2d3748',
        'primary-light': '#4a5568',
        'accent': '#718096',
        'gradient': 'linear-gradient(135deg, #2d3748 0%, #4a5568 100%)',
        'description': '极简主义、高端品牌、艺术展示'
    }
}

STYLES = {
    '现代简约': {
        'radius': '16px',
        'shadow': '0 10px 15px -3px rgba(0, 0, 0, 0.1)',
        'shadow-hover': '0 20px 25px -5px rgba(0, 0, 0, 0.1)',
        'border': 'none',
        'transform': 'translateY(-5px)',
        'description': '圆角卡片、柔和阴影、留白充足'
    },
    '科技感': {
        'radius': '8px',
        'shadow': '0 0 20px rgba(102,126,234,0.3)',
        'shadow-hover': '0 0 30px rgba(102,126,234,0.5)',
        'border': '1px solid rgba(255,255,255,0.1)',
        'transform': 'translateY(-5px)',
        'description': '发光效果、科技蓝、未来感'
    },
    '商务正式': {
        'radius': '4px',
        'shadow': '0 2px 4px rgba(0,0,0,0.1)',
        'shadow-hover': '0 4px 8px rgba(0,0,0,0.15)',
        'border': '1px solid #e2e8f0',
        'transform': 'translateY(-3px)',
        'description': '小圆角、保守阴影、专业稳重'
    },
    '创意活泼': {
        'radius': '24px',
        'shadow': '8px 8px 0px rgba(0,0,0,0.1)',
        'shadow-hover': '12px 12px 0px rgba(0,0,0,0.15)',
        'border': 'none',
        'transform': 'translate(-2px, -2px) rotate(-2deg)',
        'description': '大圆角、硬阴影、倾斜动画'
    },
    '高端奢华': {
        'radius': '12px',
        'shadow': '0 20px 40px rgba(0,0,0,0.2)',
        'shadow-hover': '0 25px 50px rgba(0,0,0,0.3)',
        'border': '1px solid rgba(255,215,0,0.3)',
        'transform': 'translateY(-8px)',
        'description': '金色点缀、深度阴影、奢华感'
    }
}

DEVICE_CONFIGS = {
    'mobile': {
        'container-max': '100%',
        'container-padding': '20px 15px',
        'grid-columns': '1fr',
        'gap': '15px',
        'card-padding': '20px',
        'value-font': '2rem',
        'title-font': '1.8rem',
        'description': '竖屏优先，单列布局'
    },
    'desktop': {
        'container-max': '1200px',
        'container-padding': '40px 20px',
        'grid-columns': 'repeat(auto-fit, minmax(250px, 1fr))',
        'gap': '20px',
        'card-padding': '30px',
        'value-font': '2.5rem',
        'title-font': '2.5rem',
        'description': '横屏优化，多列网格'
    },
    'responsive': {
        'container-max': '1200px',
        'container-padding': '40px 20px',
        'grid-columns': 'repeat(auto-fit, minmax(250px, 1fr))',
        'gap': '20px',
        'card-padding': '30px',
        'value-font': '2.5rem',
        'title-font': '2.5rem',
        'description': '自适应，默认方案'
    }
}


def parse_markdown_content(content: str) -> dict:
    """解析 Markdown 内容为结构化数据"""
    
    result = {
        'title': '',
        'subtitle': '',
        'metrics': [],
        'sections': []
    }
    
    lines = content.strip().split('\n')
    
    for i, line in enumerate(lines):
        if line.startswith('# '):
            result['title'] = line[2:].strip()
            if i + 1 < len(lines) and not lines[i + 1].startswith('#'):
                result['subtitle'] = lines[i + 1].strip()
            break
    
    metric_pattern = re.compile(r'(\d+(?:,\d{3})*(?:\.\d+)?|%|万|亿)')
    for line in lines:
        if ':' in line or ':' in line:
            parts = line.replace(':', ':').split(':', 1)
            if len(parts) == 2:
                label = parts[0].strip()
                value_part = parts[1].strip()
                if metric_pattern.search(value_part):
                    match = metric_pattern.search(value_part)
                    value = match.group(0) if match else value_part
                    result['metrics'].append({
                        'label': label,
                        'value': value,
                        'change': None
                    })
    
    result['metrics'] = result['metrics'][:8]
    
    section_title = ''
    section_lines = []
    
    for line in lines[2:]:
        if line.startswith('## '):
            if section_title and section_lines:
                result['sections'].append({
                    'title': section_title,
                    'content': markdown.markdown('\n'.join(section_lines), extensions=['tables'])
                })
            section_title = line[3:].strip()
            section_lines = []
        elif line.strip():
            section_lines.append(line)
    
    if section_title and section_lines:
        result['sections'].append({
            'title': section_title,
            'content': markdown.markdown('\n'.join(section_lines), extensions=['tables'])
        })
    
    if not result['sections']:
        remaining = '\n'.join(lines[2:])
        if remaining.strip():
            result['sections'].append({
                'title': '详细内容',
                'content': markdown.markdown(remaining, extensions=['tables'])
            })
    
    return result


def generate_css(color_name: str, style_name: str, device_name: str) -> str:
    """生成 CSS 样式"""
    
    colors = COLOR_SCHEMES.get(color_name, COLOR_SCHEMES['紫蓝渐变'])
    style = STYLES.get(style_name, STYLES['现代简约'])
    device = DEVICE_CONFIGS.get(device_name, DEVICE_CONFIGS['responsive'])
    
    css = f'''
        :root {{
            --primary: {colors['primary']};
            --primary-light: {colors['primary-light']};
            --accent: {colors['accent']};
            --bg: #f8f9fa;
            --card-bg: #ffffff;
            --text: #2d3748;
            --text-light: #718096;
            --radius: {style['radius']};
            --shadow: {style['shadow']};
            --shadow-hover: {style['shadow-hover']};
        }}
        
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        
        body {{
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
            background: {colors['gradient']};
            min-height: 100vh;
            padding: {device['container-padding']};
            color: var(--text);
        }}
        
        .container {{
            max-width: {device['container-max']};
            margin: 0 auto;
        }}
        
        .header {{
            text-align: center;
            color: white;
            margin-bottom: 40px;
        }}
        
        .header h1 {{
            font-size: {device['title-font']};
            font-weight: 700;
            margin-bottom: 10px;
            text-shadow: 0 2px 4px rgba(0,0,0,0.2);
        }}
        
        .header p {{
            font-size: 1.1rem;
            opacity: 0.9;
        }}
        
        .metrics-grid {{
            display: grid;
            grid-template-columns: {device['grid-columns']};
            gap: {device['gap']};
            margin-bottom: 40px;
        }}
        
        .metric-card {{
            background: var(--card-bg);
            border-radius: var(--radius);
            padding: {device['card-padding']};
            box-shadow: var(--shadow);
            transition: transform 0.3s ease, box-shadow 0.3s ease;
            {f"border: {style['border']};" if style['border'] != 'none' else ''}
        }}
        
        .metric-card:hover {{
            transform: {style['transform']};
            box-shadow: var(--shadow-hover);
        }}
        
        .metric-card .label {{
            font-size: 0.875rem;
            color: var(--text-light);
            text-transform: uppercase;
            letter-spacing: 0.05em;
            margin-bottom: 10px;
        }}
        
        .metric-card .value {{
            font-size: {device['value-font']};
            font-weight: 700;
            background: linear-gradient(135deg, var(--primary) 0%, var(--primary-light) 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
        }}
        
        .content-section {{
            background: var(--card-bg);
            border-radius: var(--radius);
            padding: {device['card-padding']};
            box-shadow: var(--shadow);
            margin-bottom: 30px;
            {f"border: {style['border']};" if style['border'] != 'none' else ''}
        }}
        
        .content-section h2 {{
            font-size: 1.5rem;
            color: var(--text);
            margin-bottom: 20px;
            padding-bottom: 10px;
            border-bottom: 3px solid;
            border-image: {colors['gradient']} 1;
        }}
        
        .content-section p {{ line-height: 1.8; margin-bottom: 15px; }}
        .content-section ul, .content-section ol {{ margin-left: 25px; margin-bottom: 20px; line-height: 1.8; }}
        .content-section li {{ margin-bottom: 8px; }}
        .content-section table {{ width: 100%; border-collapse: collapse; margin: 20px 0; }}
        .content-section th, .content-section td {{ padding: 12px; text-align: left; border-bottom: 1px solid var(--border); }}
        .content-section th {{ background: var(--bg); font-weight: 600; }}
        .content-section blockquote {{
            border-left: 4px solid var(--primary);
            padding-left: 20px;
            margin: 20px 0;
            color: var(--text-light);
            font-style: italic;
        }}
        
        .footer {{
            text-align: center;
            color: white;
            margin-top: 40px;
            padding-top: 30px;
            border-top: 1px solid rgba(255,255,255,0.2);
            opacity: 0.8;
            font-size: 0.9rem;
        }}
    '''
    
    # 响应式（仅 responsive 模式需要）
    if device_name == 'responsive':
        css += '''
            @media (max-width: 768px) {
                body {
                    padding: 20px 15px;
                }
                .header h1 {
                    font-size: 1.8rem;
                }
                .metrics-grid {
                    grid-template-columns: 1fr;
                }
                .metric-card .value {
                    font-size: 2rem;
                }
                .content-section {
                    padding: 25px;
                }
            }
        '''
    
    return css


def generate_html(data: dict, color_name: str, style_name: str, device_name: str) -> str:
    """生成 HTML 内容"""
    
    css = generate_css(color_name, style_name, device_name)
    
    metrics_html = ''
    if data['metrics']:
        metric_cards = []
        for m in data['metrics']:
            metric_cards.append(f'''
            <div class="metric-card">
                <div class="label">{m['label']}</div>
                <div class="value">{m['value']}</div>
            </div>''')
        metrics_html = '<div class="metrics-grid">' + '\n'.join(metric_cards) + '</div>'
    
    sections_html = ''
    for section in data['sections']:
        sections_html += f'''
        <div class="content-section">
            <h2>{section['title']}</h2>
            {section['content']}
        </div>'''
    
    html = f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{data['title']}</title>
    <style>{css}</style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>{data['title']}</h1>
            {'<p>' + data['subtitle'] + '</p>' if data['subtitle'] else ''}
        </div>
        
        {metrics_html}
        
        {sections_html}
        
        <div class="footer">
            <p>Generated by HTML Infographic Skill · {datetime.now().strftime('%Y-%m-%d %H:%M')}</p>
        </div>
    </div>
</body>
</html>'''
    
    return html


def generate_infographic(content: str, color: str = '紫蓝渐变', style: str = '现代简约', 
                         device: str = 'responsive', output_dir: str = None, name: str = None):
    """生成信息图 HTML"""
    
    data = parse_markdown_content(content)
    
    if not name:
        name = data['title'] or 'infographic'
    
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    project_name = f"{name}_{timestamp}"
    project_name = re.sub(r'[^\w\u4e00-\u9fff\-_]', '_', project_name)
    
    if output_dir:
        project_path = Path(output_dir) / project_name
    else:
        project_path = Path(__file__).parent.parent / 'projects' / project_name
    
    project_path.mkdir(parents=True, exist_ok=True)
    
    # 保存原始内容
    source_path = project_path / 'source.md'
    source_path.write_text(content, encoding='utf-8')
    
    # 保存配置
    config = {
        'color': color,
        'style': style,
        'device': device,
        'generated_at': datetime.now().isoformat(),
        'color_info': COLOR_SCHEMES.get(color, {}),
        'style_info': STYLES.get(style, {}),
        'device_info': DEVICE_CONFIGS.get(device, {})
    }
    config_path = project_path / 'config.json'
    config_path.write_text(json.dumps(config, indent=2, ensure_ascii=False), encoding='utf-8')
    
    # 生成 HTML
    html_content = generate_html(data, color, style, device)
    html_path = project_path / 'index.html'
    html_path.write_text(html_content, encoding='utf-8')
    
    return {
        'project_path': str(project_path),
        'html_path': str(html_path),
        'source_path': str(source_path),
        'config_path': str(config_path)
    }


@click.command()
@click.argument('content_or_file')
@click.option('--color', '-c', default='紫蓝渐变', 
              type=click.Choice(list(COLOR_SCHEMES.keys())),
              help='色系选择')
@click.option('--style', '-s', default='现代简约',
              type=click.Choice(list(STYLES.keys())),
              help='风格选择')
@click.option('--device', '-d', default='responsive',
              type=click.Choice(list(DEVICE_CONFIGS.keys())),
              help='终端适配')
@click.option('--output', '-o', default=None, help='输出目录')
@click.option('--name', '-n', default=None, help='项目名称')
@click.option('--template', '-t', default=None, help='参考图路径（待实现）')
def cli(content_or_file, color, style, device, output, name, template):
    """生成 HTML 信息图"""
    
    click.echo(f"🎨 生成配置:")
    click.echo(f"   色系：{color} ({COLOR_SCHEMES[color]['description']})")
    click.echo(f"   风格：{style} ({STYLES[style]['description']})")
    click.echo(f"   终端：{device} ({DEVICE_CONFIGS[device]['description']})")
    click.echo()
    
    if os.path.isfile(content_or_file):
        content = Path(content_or_file).read_text(encoding='utf-8')
    else:
        content = content_or_file
    
    result = generate_infographic(content, color, style, device, output, name)
    
    click.echo(f"✅ 信息图生成成功！")
    click.echo(f"📁 项目路径：{result['project_path']}")
    click.echo(f"📄 HTML 文件：{result['html_path']}")
    click.echo(f"📝 源文件：{result['source_path']}")
    click.echo(f"⚙️  配置文件：{result['config_path']}")
    
    if sys.platform == 'darwin':
        os.system(f"open {result['html_path']}")
    elif sys.platform == 'linux':
        os.system(f"xdg-open {result['html_path']}")
    elif sys.platform == 'win32':
        os.system(f"start {result['html_path']}")


if __name__ == '__main__':
    cli()
