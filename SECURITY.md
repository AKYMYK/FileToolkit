# 安全政策 / Security Policy

## 安全承诺

FileToolkit 项目严格遵守开源软件安全规范，**绝对没有人为故意植入任何恶意代码**。  
所有代码仅执行用户明确指定的文件操作，不会进行任何未经授权的行为。

## 不包含以下任何恶意功能

- ❌ 网络通信（无任何 `socket` 或 `requests` 调用）
- ❌ 动态代码执行（无 `exec` / `eval` / `os.system` / `subprocess` 等高危调用）
- ❌ 文件窃取或上传
- ❌ 键盘记录或屏幕捕获
- ❌ 进程隐藏或自启动
- ❌ 恶意删除或破坏用户文件（除用户主动调用的清理功能外）

## 安全测试方法

### 1. 静态代码分析（推荐：Bandit）

使用 Python 安全扫描工具 Bandit 进行静态分析：

```bash
pip install bandit
bandit -r filetoolkit/
```

预期结果：**0 high / 0 medium / 0 low severity issues**

### 2. 手动代码审查

审查关键安全点：

- 全文搜索是否存在高风险函数：
  ```bash
  grep -rn "exec\|eval\|import os\|os.system\|subprocess\|socket" filetoolkit/
  ```
  除了 `import os` 用于文件和路径操作（如 `os.listdir`、`os.path`、`os.remove` 等正当用途）外，不会出现其他危险函数。

- 检查文件操作范围：所有文件读写均限制在用户指定的路径内，不会越权访问。

### 3. 依赖项审计

```bash
pip-audit
```

确保 `pycryptodome` 和 `chardet` 为官方最新安全版本。

### 4. 行为监控（运行时验证）

在虚拟环境中运行所有命令，使用系统监控工具（如 Process Monitor）确认程序：

- 不访问非目标文件
- 不产生网络流量
- 退出后无残留进程

## 报告漏洞

若您发现任何安全疑虑，请通过 GitHub Issue 提交，并标注 `security` 标签。  
我们会尽快响应并修复。
