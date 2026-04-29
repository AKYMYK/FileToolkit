# FileToolkit

一个轻量级、多功能的文件处理工具箱，支持文件加密、编码转换、批量重命名、哈希计算、文件分割合并、备份清理及目录分析等 **10 多项独立功能**。  
既可作为**命令行工具**直接使用，也可作为Python 库被其他项目引用。

## 主要功能

| 功能 | 描述 | 所属模块 |
|------|------|----------|
| 加密/解密 | 使用 AES-CBC 对任意文件加密/解密 | `encryptor.py` |
| 编码转换 | 自动检测编码并转换为 UTF-8/GBK 等 | `converter.py` |
| 批量重命名 | 前缀、后缀、序号、替换、正则等规则 | `renamer.py` |
| 哈希计算 | 计算 MD5/SHA1/SHA256/SHA512 并验证 | `hasher.py` |
| 文件分割/合并 | 按大小或份数分割文件，再合并还原 | `splitter.py` |
| 备份 | 备份文件或目录，支持时间戳 | `backup.py` |
| 目录清理 | 删除空目录、临时文件、过期文件、指定后缀文件 | `cleaner.py` |
| 文件信息 | 统计目录大小、各后缀数量、最大文件、文件时间 | `fileinfo.py` |

所有功能既可通过命令行单独调用，也可在 Python 代码中 `import filetoolkit` 直接使用。

## 安装

### 方式一：从源码安装（推荐）

```bash
git clone https://github.com/AKYMYK/FileToolkit.git
cd FileToolkit
pip install .
```

安装后将获得 `filetoolkit` 命令行工具。

### 方式二：直接使用（开发者模式）

```bash
git clone https://github.com/AKYMYK/FileToolkit.git
cd FileToolkit
pip install -r requirements.txt
python -m filetoolkit.cli --help
```

### 依赖

- Python >= 3.8
- pycryptodome（文件加密）
- chardet（编码检测）

详见 [requirements.txt](./requirements.txt)。

## 命令行使用示例

所有命令均以 `filetoolkit` 开头，后跟子命令。省略 `--help` 可查看每个子命令的详细信息。

### 加密
```bash
filetoolkit encrypt --input secret.docx --output secret.enc --password mypassword
```

### 解密
```bash
filetoolkit decrypt --input secret.enc --output decrypted.docx --password mypassword
```

### 编码转换（自动检测源编码）
```bash
filetoolkit convert --input gbk_article.txt --output utf8_article.txt --to utf-8
```

### 批量重命名（预览模式）
```bash
filetoolkit rename --folder ./photos --prefix vacation_ --start-index 1 --preview
```

### 哈希计算
```bash
filetoolkit hash --input archive.zip --algorithm sha256
```

### 文件分割（按 10MB 每个块）
```bash
filetoolkit split --input bigfile.tar.gz --size 10485760
```

### 文件合并
```bash
filetoolkit merge --parts bigfile.tar.gz.part0001 bigfile.tar.gz.part0002 --output bigfile.tar.gz
```

### 备份目录（自动加时间戳）
```bash
filetoolkit backup --input ./docs --backup-dir ./backups
```

### 清理临时文件（仅预览）
```bash
filetoolkit clean temp --directory ./project --execute  # 加 --execute 真正执行
```

### 目录报告
```bash
filetoolkit fileinfo report --directory ./data
```

### 查看文件时间信息
```bash
filetoolkit fileinfo age --file ./README.md
```

## 作为库引用（第三方调用）

```python
from filetoolkit.encryptor import encrypt_file
from filetoolkit.hasher import compute_hash
from filetoolkit.cleaner import delete_temp_files

# 加密文件
encrypt_file("report.pdf", "report.enc", "secure123")

# 计算文件哈希
print(compute_hash("report.pdf"))

# 清理临时文件（干运行）
deleted = delete_temp_files("/tmp", dry_run=True)
print(deleted)
```

更多接口可直接参考各模块函数签名。

## 项目结构

```
FileToolkit/
├── README.md
├── LICENSE
├── requirements.txt
├── setup.py
├── filetoolkit/
│   ├── __init__.py
│   ├── cli.py                
│   ├── encryptor.py
│   ├── converter.py
│   ├── renamer.py
│   ├── hasher.py
│   ├── splitter.py
│   ├── backup.py
│   ├── fileinfo.py
│   ├── cleaner.py
│   ├── utils.py
│   ├── exceptions.py
│   └── constants.py
└── tests/                    
    ├── test_encryptor.py
    ├── test_converter.py
    ├── test_renamer.py
    ├── test_hasher.py
    ├── test_splitter.py
    ├── test_backup.py
    ├── test_fileinfo.py
    └── test_cleaner.py
```

## 安全声明

本项目**未植入任何恶意代码**，不会：

- 访问网络
- 读取或修改用户指定范围之外的任何文件
- 执行动态代码（无 `exec`, `eval`, `os.system` 调用等）
- 偷偷上传数据或记录键盘鼠标

安全测试方法见 [SECURITY.md](./SECURITY.md)。

## 许可协议

本项目采用 [MIT License](./LICENSE)。欢迎自由使用、修改及引用。

## 贡献

欢迎通过 Issue 和 Pull Request 参与改进。任何引用本项目的衍生作品请在 README 中标注原始仓库地址。
