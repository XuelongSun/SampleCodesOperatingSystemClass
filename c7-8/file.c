#include <fcntl.h>
#include <unistd.h>
#include<stdio.h>

int main() {
    // 创建文件（如果不存在），返回文件描述符
    int fd = open("newfile.txt", O_CREAT | O_WRONLY, 0644);

    // 打开文件
    int fd1 = open("file.txt", O_WRONLY | O_APPEND);

    for line in f:
        print(line)
    // 写入
    write(fd, "Hello", 5);  //覆盖
    write(fd1, "Hello", 5); //追加
    // 关闭
    close(fd);

    // 删除文件用的是unlink而不是delete
    unlink("file_to_delete.txt");  

    // 移动/重命名
    rename("oldname.txt", "newname.txt");

    // 硬链接
    link("original.txt", "hardlink.txt");

    //软链接
    symlink("target.txt", "symlink.txt");

    return 0;
}