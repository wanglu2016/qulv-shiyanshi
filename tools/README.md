# 工具

## subset_fonts.py：按页面用字裁剪字体

页面不依赖 Google Fonts（国内常打不开），而是把字体裁剪成只含 `index.html` 实际用到的字符，放在 `assets/fonts/`。修改页面文字、出现新汉字后，需要重新运行一次。

### 1. 准备源字体

把下面这些文件放进 `tools/fonts-src/`（该目录已被 .gitignore 忽略）：

| 文件 | 来源仓库中的路径 |
| --- | --- |
| NotoSansSC-Regular.otf、NotoSansSC-Medium.otf、NotoSansSC-Bold.otf | notofonts/noto-cjk：`Sans/SubsetOTF/SC/` |
| NotoSerifSC-SemiBold.otf、NotoSerifSC-Black.otf | notofonts/noto-cjk：`Serif/SubsetOTF/SC/` |
| JetBrainsMono-Regular.ttf、JetBrainsMono-SemiBold.ttf | JetBrains/JetBrainsMono：`fonts/ttf/` |
| STIXTwoText-Regular.input.ttf、STIXTwoText-Italic.input.ttf、STIXTwoMath.input.ttf | stipub/stixfonts：`source/` |

只取需要的文件，避免下载整个仓库（noto-cjk 有好几 GB）：

```bash
mkdir -p tools/fonts-src && cd tools/fonts-src
git clone --depth 1 --filter=blob:none --sparse https://github.com/notofonts/noto-cjk.git
(cd noto-cjk && git sparse-checkout set --no-cone \
  /Sans/SubsetOTF/SC/NotoSansSC-Regular.otf /Sans/SubsetOTF/SC/NotoSansSC-Medium.otf /Sans/SubsetOTF/SC/NotoSansSC-Bold.otf \
  /Serif/SubsetOTF/SC/NotoSerifSC-SemiBold.otf /Serif/SubsetOTF/SC/NotoSerifSC-Black.otf)
git clone --depth 1 --filter=blob:none --sparse https://github.com/JetBrains/JetBrainsMono.git
(cd JetBrainsMono && git sparse-checkout set --no-cone /fonts/ttf/JetBrainsMono-Regular.ttf /fonts/ttf/JetBrainsMono-SemiBold.ttf)
git clone --depth 1 --filter=blob:none --sparse https://github.com/stipub/stixfonts.git
(cd stixfonts && git sparse-checkout set --no-cone /source/STIXTwoText-Regular.input.ttf /source/STIXTwoText-Italic.input.ttf /source/STIXTwoMath.input.ttf)
cp noto-cjk/*/SubsetOTF/SC/*.otf JetBrainsMono/fonts/ttf/*.ttf stixfonts/source/*.input.ttf .
cd ../..
```

### 2. 运行

```bash
pip install fonttools brotli
python3 tools/subset_fonts.py
```

脚本会读取 `index.html` 中出现的全部字符（另外始终保留全部 ASCII 和常用数学符号），生成 `assets/fonts/*.woff2` 并重写 `assets/fonts/fonts.css`。

### 3. 重新打包离线版

```bash
rm -rf /tmp/qulv && mkdir -p /tmp/qulv/qulv-shiyanshi
cp -r index.html assets README.md /tmp/qulv/qulv-shiyanshi/
cp tools/使用说明.txt /tmp/qulv/qulv-shiyanshi/
(cd /tmp/qulv && zip -qr - qulv-shiyanshi) > download/qulv-shiyanshi-site.zip
```
