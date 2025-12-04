### 实验7：基于索引节点的文件系统
#### 实验目的
1. 理解文件系统的逻辑功能以及需要提供给用户的接口
2. 通过模拟inode(索引节点)，理解文件系统的文件与目录管理
3. 通过shell模拟体会接口函数API的测试方法

#### inode
索引节点是比文件控制块（FCB-File Control Block）更轻量的文件系统管理方式，它完成了由用户关心的文件名到系统关系的inode数据结构的对应关系。
基于Python实现索引节点类：
```py
class INode:
    next_inode_id = 1 # inode 自增
    def __init__(self, name, is_directory=False, size=0, permissions=0o755):
        self.inode_id = INode.next_inode_id
        INode.next_inode_id += 1
        self.name = name
        self.is_directory = is_directory
        self.size = size
        self.permissions = permissions
        # 简化实现：用字典实现目录的内容，用字符串表示文件内容
        self.content = {} if is_directory else b''
        self.owner = "root"
        self.group = "root"
        # 时间记录
        self.created = self.modified = self.accessed = 0
        self.parent = None
```
#### Filesystem
文件系统的实现，主要是对inode的管理，以及为用户提供逻辑文件系统的功能接口。

对于路径的解析是个难点，需要用到递归，指直到文件名。比如绝对路径`/home/os/project/test.c`,相对路径`../home/os/c.c`和`home/os/c.c`等。因此需要考虑当前目录和父级目录。如：`/home/os/project/test.c` $\to$ `path_resolution()` $\to$ test.c的INode
```py
class FileSystem:
    def __init__(self) -> None:
        self.inodes = {}
        # 更目录
        self.root = INode("/", is_directory=True)
        self.inodes = {self.root.inode_id: self.root}
        # 当前目录
        self.current_directory = self.root
    
    def path_resolution(self,path):
        # 对文件路径进行解析
        pass

    def create_file(self, self, path, size=0, permissions=0o644):
        # 创建新文件
        pass

    def create_directory(self, path, permissions=0o755):
        # 创建新目录
        pass

    def change_directory(self, path):
        # 切换目录
        pass

    def list_directory(self, path="."):
        # 打印目录内容
        pass
```

#### Shell 模拟
Python模拟命令行交互：
```py
class Shell:
    def __init__(self) -> None:
        self.fs = FileSystem()
    
    def run(self):
        while True:
            command = input("yourname-fs> ").strip()
            if command == "exit":
                break
            elif command.startswith("ls"):
                pass
            elif command.startswith("cd"):
                pass
            elif command.startswith("mkdir"):
                pass
            elif command.startswith("touch"):
                pass
            else:
                print("Unknown command")
    
    def ls(self, path, options=[]):
        # 实现 ls 命令
        pass
    
    def cd(self, path):
        # 实现 cd 命令
        pass
    
    def mkdir(self, path):
        # 实现 mkdir 命令
        pass
    
    def touch(self, path):
        # 实现 touch 命令
        pass
```
功能：用户在输入命令，完成对命令的解析，并调用相应的函数，实现对应的功能，其功能本质上对应文件系统inode的变化

**请将命令行提示符改成你的名字拼音的缩写，如：zs-fs>**

#### Assignment
+ 以`fs.py`中的代码为基础进行开发并测试，至少需要实现`ls`,`touch`,`mkdir`,`cd`的基础功能。学有余力的同学可以考虑带参数的命令，比如`ls -i`在文件和目录前显示inode编号，`ls -l`显示文件更详细的信息，`mkdir -p` 若不存在目录，则自动创建等进阶功能。
+ 提交`fs.py`,`OS_Lab7_name.md`(基于`Lab7/templates.md`完成) 和 `OS_Lab7_name.pdf`(由`OS_Lab7_name.md`生成)；
+ **deadline: By the Friday of Week 16 (2025/12/19).**
+ submit to: xsun@gzhu.edu.cn, subject(邮件主题): Assignment-OS-Lab7