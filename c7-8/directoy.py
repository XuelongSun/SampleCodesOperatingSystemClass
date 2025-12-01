import os
import shutil

os.mkdir("newdir")
# 或创建多级目录
os.makedirs("path/to/newdir")

# 删除目录
os.rmdir("emptydir")

# 删除非空目录 - 递归删除
shutil.rmtree("nonemptydir") 

