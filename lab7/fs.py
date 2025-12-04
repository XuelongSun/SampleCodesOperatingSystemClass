import os as OS

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


class FileSystem:
    def __init__(self) -> None:
        self.inodes = {}
        # 根目录
        self.root = INode("/", is_directory=True)
        self.inodes = {self.root.inode_id: self.root}
        # 当前目录
        self.current_directory = self.root
    
    def path_resolution(self,path):
        # 对文件路径进行解析，返回文件/目录的inode
        pass

    def create_file(self, path, size=0, permissions=0o644):
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

if __name__ == "__main__":
    shell = Shell()
    shell.run()