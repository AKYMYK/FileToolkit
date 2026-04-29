# FileToolkit

一个简单、轻量级的多功能文件工具箱，提供 **文件加密/解密**、**文件编码转换**、**批量文件重命名** 三个独立功能。  
既能作为命令行工具直接使用，也能当作 Python 包被其他项目引用。

## 功能概览

| 功能 | 说明 |
|------|------|
| 🔐 文件加密/解密 | 使用 AES-256 对称加密，支持任意文件类型，密码自定义 |
| 🔄 文件编码转换 | 自动检测源编码，转换为 UTF-8、GBK 等目标编码 |
| 📝 批量文件重命名 | 支持前缀、后缀、序号、字符串替换、正则替换，带预览模式 |

## 系统要求

- Python 3.8 或更高版本
- pip（Python 包管理工具）
- 需要安装的外部库（会自动安装）：
  - `pycryptodome`（加密）
  - `chardet`（编码检测）

## 安装方法

### 方法一：从源码安装（推荐给开发者）

```bash
git clone https://github.com/你的用户名/FileToolkit.git
cd FileToolkit
pip install .
```

安装完成后，命令行会多出 `filetoolkit` 这个命令。

### 方法二：直接用 pip 安装（需要先发布到 PyPI，可选）

```bash
pip install filetoolkit
```

### 方法三：不安装，直接从源码运行

```bash
git clone https://github.com/你的用户名/FileToolkit.git
cd FileToolkit
python -m filetoolkit.cli --help
```

### 方法四：打包成独立 exe（无需 Python 环境）

```bash
pip install pyinstaller
cd FileToolkit
pyinstaller --onefile filetoolkit/cli.py -n filetoolkit
```
生成的 `filetoolkit.exe` 在 `dist/` 目录，可以直接发给别人运行。

## 使用方法

### 1. 命令行方式

安装后，直接在终端使用 `filetoolkit` 命令。

#### 加密文件

```bash
filetoolkit encrypt --input test.txt --output test.enc --password mysecret
```

#### 解密文件

```bash
filetoolkit decrypt --input test.enc --output test_dec.txt --password mysecret
```

#### 文件编码转换（自动检测源编码）

```bash
filetoolkit convert --input gbk_file.txt --output utf8_file.txt --to utf-8
```

也可以手动指定源编码：
```bash
filetoolkit convert --input shift_jis.txt --output utf8.txt --from shift_jis --to utf-8
```

#### 批量重命名（预览模式）

先看看重命名效果（不会真改）：
```bash
filetoolkit rename --folder ./myfolder --prefix holiday_ --start-index 1 --preview
```

实际执行重命名（去掉 `--preview`）：
```bash
filetoolkit rename --folder ./myfolder --prefix holiday_ --start-index 1
```

其他重命名选项：
- `--replace-old "旧文字" --replace-new "新文字"` 替换文件名中的文字
- `--regex-pattern "正则" --regex-repl "替换串"` 支持正则替换
- `--suffix "_final"` 添加后缀

可以使用 `filetoolkit --help` 查看所有参数。

### 2. 作为 Python 库引用

```python
from filetoolkit.encryptor import encrypt_file, decrypt_file
from filetoolkit.converter import convert_encoding
from filetoolkit.renamer import batch_rename

# 加密
encrypt_file("doc.pdf", "doc.enc", "password123")

# 编码转换
convert_encoding("old.txt", "new.txt", from_enc="gbk", to_enc="utf-8")

# 重命名（预览）
batch_rename("./myfolder", prefix="img_", start_index=1, preview=True)
```

## 运行测试

```bash
cd FileToolkit
python -m unittest discover -s tests -p "test_*.py"
```

所有测试应该全部通过。

## 安全说明

本项目 **没有故意植入任何恶意代码**：
- 所有操作仅限于用户指定的文件，不会访问网络、注册表或其他敏感信息。
- 代码中不使用 `eval`、`exec` 等动态执行函数。
- 无后门、无数据收集、无联网行为。
- 安全测试方法：使用 `bandit` 静态扫描 `filetoolkit/` 目录，结果无安全问题。

```bash
pip install bandit
bandit -r filetoolkit/
```

你也可以用全文搜索（如 `grep`）查找 `socket`、`http`、`subprocess` 等关键词，确认无恶意调用。

## 开源许可

本项目使用 [MIT License](LICENSE)，你可以自由使用、修改、分发，甚至用于商业用途。

## 贡献

欢迎提 Issue 或 Pull Request，但请先阅读 CONTRIBUTING.md（如果有的话）。  
也可以直接 Fork 本仓库，自行扩展。


