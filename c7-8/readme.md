### File System

#### Logical
+ inode - 索引节点
    check the inode usage for the filesystem
    ```bash
    df -i
    # for a specific device
    tune2fs -l /dev/sda1 | grep -i inode
    ```
    show inode:
    ```bash
    # 显示文件的 inode 号
    ls -i filename.txt

    # 显示目录下所有文件的 inode 号
    ls -i /path/to/directory/

    # 详细显示（包含 inode 号）
    ls -li
    ```
    show inode info:
    ```bash
    # 显示文件的完整 inode 信息
    stat filename.txt

    # 显示多个文件的信息
    stat file1.txt file2.txt

    # 简洁格式（只显示 inode 号）
    stat -c %i filename.txt
    ```
+ operations
  + CLI:
   （1）file
    ```bash
    # 1. create a file/directory
    touch filename.txt
    
    # 2. delete a file
    rm filename.txt

    # 3. open, read and then close
    cat filename.txt
    head -n 5 file.txt
    tail -n 3 file.txt

    # 4. write
    echo "new content" > file.txt    # overwrite
    echo "append" >> file.txt        # append
    
    # 5. move/renmae
    mv oldname.txt newname.txt          
    mv file.txt /another/directory/

    # 6. hard link
    ln target.txt symlink.txt

    # 7. soft (symbolic) link
    ln -s target.txt symlink.txt
    ```
    

    (2) directory
    ```bash
    # 1. create a directory
    mkdir newdir
    mkdir -p test/c/newdir
    # 2. delete
    rmdir emptydir          # 只能删除空目录
    rm -r nonemptydir       # 递归删除非空目录
    ```
  + Python:`file.py` and `directory.py`
    
  + C:`file.c` and `directory.c`
#### Physical

##### 文件在外存上的组织形式
+ 连续组织
+ 链接组织
  + 隐式链接
  + 显示链接： FAT12 - FAT16 - FAT32 - NTFS
+ 索引组织

##### 空闲块管理
+ 空闲表
+ 空闲链表
+ Linux-EXT: 位示图Bitmap
  `bitmap.py`:
  ```shell
  Allocate 0, Bitmap: 0000000000000001
  Allocate 1, Bitmap: 0000000000000011
  Free 0, Bitmap: 0000000000000010
  Allocate 0, Bitmap: 0000000000000011
  ```
+ UNIX-SystemV: 成组链接