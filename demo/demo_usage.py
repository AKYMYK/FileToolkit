# demo_usage.py - 演示第三方程序引用 FileToolkit
from filetoolkit.encryptor import encrypt_file
from filetoolkit.hasher import compute_hash
from filetoolkit.renamer import preview_rename

# 调用加密
encrypt_file("test.txt", "test.enc", "123456")
print("加密成功")

# 调用哈希
print("SHA256:", compute_hash("test.enc"))

# 调用重命名预览
changes = preview_rename("./some_folder", prefix="new_")
print("预览重命名:", changes)
