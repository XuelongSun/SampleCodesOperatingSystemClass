import os

# 创建空文件
open("newfile.txt", "w").close()

# 创建读写内容
with open("newfile.txt", "w") as f:
    content = f.read()
    f.write("Hello World")
    for line in f:
        print(line)

# 创建并指定属性
dst_fd = os.open("filename.txt", os.O_WRONLY | os.O_CREAT | os.O_TRUNC, 0o644)

# 删除文件
os.remove("file_to_delete.txt")

# 移动/重命名文件
os.rename("oldname.txt", "newname.txt")

# 链接文件（硬链接）
os.link("original.txt", "hardlink.txt")

# 链接文件（软链接）
os.symlink("original.txt", "softlink.txt")