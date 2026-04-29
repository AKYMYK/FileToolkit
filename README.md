# FileToolkit

## 1. 安装方法
- 从源码安装：git clone ... 然后 pip install .
- 从 PyPI 安装：pip install filetoolkit（若发布）
- 打包为exe：pyinstaller cli.py --onefile

## 2. 依赖环境
- Python 3.8+
- 外部库：pycryptodome, chardet （列表）

## 3. 使用方法
### 命令行
- 加密：filetoolkit encrypt --input test.txt --output test.enc --key 1234
- 解密：filetoolkit decrypt ...
- 编码转换：filetoolkit convert --input gbk.txt --output utf8.txt --from gbk --to utf-8
- 重命名：filetoolkit rename --folder ./dir --prefix new_ --start-index 1 --preview

