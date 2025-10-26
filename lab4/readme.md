### 实验4：进程调度
#### 实验目的
1. 理解作业与进程调度算法的原理
2. 理解进程切换需要做的相关工作
3. 通过在[实验3](../lab3/readme.md)所设计的CPU上完成进程调度，进一步理解进程调度与进程切换开销

#### 进程调度
##### 调度算法
+ 非抢占式((non-preemptive))作业调度
  + 先来先服务 FCFS
  + 短作业优先 SJF
+ 抢占式(preemptive)作业调度算法：
  + RTF(shortest remaining time first)
+ 进程调度
  + 高响应比优先：HRRN-Highest Response Ration Next
  + 基于优先级的调度算法：priority based scheduling algorithm
  + 轮转调度 round robin

##### 程序实现 
进程调度是在OS中完成的，所以需要修改[实验3](../lab3/readme.md)中的`pyos.py`中的`OperatingSystem`类:

+ 增加调度函数：
  ```py
    def schedule(self, policy="RR"):
        if policy == "RR":
            pass
        elif policy == "SRTF":
            pass
        elif policy == ""
  ```
+ 增加保存和恢复现场，以及切换进程的函数：
  ```py
  def save_cpu_context(self):
      pass

  def load_cpu_context(self, context):
      pass

  def switch_process(self, current_process:PCB, next_process:PCB):
      pass
  ```
+ 修改运行函数在每个CPU时钟上重建就绪队列并执行调度算法：
  ```py
  def run(self, max_cycles=100):
    # 初始化与准备
    # ...
    while self.running and cycles < max_cycles:
        # 执行主体
        # ...
        self.clock += 1
  ```

进程的现场数据需要保存在PCB中，所涉及的算法需要知道进程的其他相关信息，比如到达时间，运行时间等，因此还需要修改`pyos.py`中的`PCB`类
```py
class PCB:
    def __init__(self, pid, name, time, program, start_addr=0):
        self.pid = pid
        self.state = State.READY
        self.name = name
        self.program = program

        # 添加新的属性以实现进程正确的切换
        # ...
```

#### Assignment
+ 至少实现两种课上所教的可抢占式进程调度算法并完成思考题，每多实现一个算法，+1分，本实验最多得4分
+ 本实验的框架代码基于[实验3](../lab3/framework),不再提供框架代码
+ 提交一个压缩包`OS_Lab4_name.zip`，内容包括：
  + 修改后的`asm.py`,`cpu.py`,`pyos.py`以及2个以上的汇编文件以模拟两个以上的进程，
  + 实验报告：`OS_Lab4_name.md`(基于`lab4/templates.md`完成) 和 `OS_Lab4_name.pdf`(由`OS_Lab4_name.md`生成)；
+ **deadline: By the Friday of Week 10 (2025/11/07).**
+ submit to: xsun@gzhu.edu.cn, subject(邮件主题): Assignment-OS-Lab4