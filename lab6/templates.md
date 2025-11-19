### 实验6：内存管理与虚拟内存
*OS2025-2026 信计231 Name[ID]*

#### 分页存储管理
+ 核心代码（以下两个函数）
    ```py
    def create_page_table(self, pid, num_pages):
        pass

    def allocate_frame(self, pid):
        pass
    ```
+ 运行结果（页表与内存可视化）：

#### 虚拟存储（请求分页）
+ 核心代码（以下几个函数）
    ```py
    def handle_page_fault(self, pid, vpage):
        pass

    def page_replacement(self, pid, page):
        pass
    
    def access_page(self, pid, page):
        pass
    ```
+ 运行结果（页面访问前后的页表，FIFO和LRU的缺页率）：


#### 思考和讨论
1. 你认为虚拟存储在实现上的难点有哪些？
2. 比较FIFO和LRU页面置换算法的缺页率，试着更改页面访问序列，你有什么发现？