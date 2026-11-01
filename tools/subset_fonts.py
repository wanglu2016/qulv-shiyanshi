#!/usr/bin/env python3
"""按 index.html 实际用到的字符裁剪字体，生成 assets/fonts/*.woff2 和 fonts.css。

用法（在仓库根目录运行）：
    python3 tools/subset_fonts.py [源字体目录]

源字体目录默认为 tools/fonts-src/，需要放入下面 FONTS 表里列出的文件。
下载方法见 tools/README.md。依赖：pip install fonttools brotli
"""
import os
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = sys.argv[1] if len(sys.argv) > 1 else os.path.join(ROOT, 'tools', 'fonts-src')
OUT = os.path.join(ROOT, 'assets', 'fonts')

# (源文件, 输出文件, CSS family, weight, style)
FONTS = [
    ('NotoSansSC-Regular.otf',        'noto-sans-sc-400.woff2',  'Noto Sans SC',   400, 'normal'),
    ('NotoSansSC-Medium.otf',         'noto-sans-sc-500.woff2',  'Noto Sans SC',   500, 'normal'),
    ('NotoSansSC-Bold.otf',           'noto-sans-sc-700.woff2',  'Noto Sans SC',   700, 'normal'),
    ('NotoSerifSC-SemiBold.otf',      'noto-serif-sc-600.woff2', 'Noto Serif SC',  600, 'normal'),
    ('NotoSerifSC-Black.otf',         'noto-serif-sc-900.woff2', 'Noto Serif SC',  900, 'normal'),
    ('JetBrainsMono-Regular.ttf',     'jetbrains-mono-400.woff2','JetBrains Mono', 400, 'normal'),
    ('JetBrainsMono-SemiBold.ttf',    'jetbrains-mono-600.woff2','JetBrains Mono', 600, 'normal'),
    ('STIXTwoText-Regular.input.ttf', 'stix-two-text-400.woff2', 'STIX Two Text',  400, 'normal'),
    ('STIXTwoText-Italic.input.ttf',  'stix-two-text-400i.woff2','STIX Two Text',  400, 'italic'),
    ('STIXTwoMath.input.ttf',         'stix-two-math.woff2',     'STIX Two Math',  400, 'normal'),
]


def page_chars():
    with open(os.path.join(ROOT, 'index.html'), encoding='utf-8') as f:
        text = f.read()
    chars = set(text)
    chars.update(chr(c) for c in range(0x20, 0x7F))           # 全部 ASCII
    chars.update('０１２３４５６７８９（）：；，。、！？“”‘’《》…—–−·°×÷±≈≤≥∞√∬∮πΣΠΔθαβγψκλ²³″′')
    return ''.join(sorted(c for c in chars if c >= ' '))


def main():
    os.makedirs(OUT, exist_ok=True)
    text_file = os.path.join(OUT, '.chars.txt')
    with open(text_file, 'w', encoding='utf-8') as f:
        f.write(page_chars())
    css = ['/* 由 tools/subset_fonts.py 生成，字体均为 SIL Open Font License 1.1，见本目录 OFL-*.txt */']
    for src, out, family, weight, style in FONTS:
        src_path = os.path.join(SRC, src)
        if not os.path.exists(src_path):
            sys.exit(f'缺少源字体：{src_path}（下载方法见 tools/README.md）')
        subprocess.run([
            'pyftsubset', src_path,
            f'--text-file={text_file}',
            f'--output-file={os.path.join(OUT, out)}',
            '--flavor=woff2', "--layout-features=*", '--no-hinting',
        ], check=True)
        size = os.path.getsize(os.path.join(OUT, out)) // 1024
        print(f'{out:28s} {size:5d} KB')
        css.append(
            '@font-face{font-family:"%s";font-style:%s;font-weight:%d;font-display:swap;src:url("%s") format("woff2")}'
            % (family, style, weight, out))
    with open(os.path.join(OUT, 'fonts.css'), 'w', encoding='utf-8') as f:
        f.write('\n'.join(css) + '\n')
    os.remove(text_file)


if __name__ == '__main__':
    main()
