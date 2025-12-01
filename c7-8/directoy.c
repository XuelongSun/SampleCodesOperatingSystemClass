#include <sys/stat.h>

int main() {
    // 创建目录
    mkdir("newdir", 0755);  // 0755是权限标志

    // 只能删除空目录
    rmdir("emptydir");  
}
