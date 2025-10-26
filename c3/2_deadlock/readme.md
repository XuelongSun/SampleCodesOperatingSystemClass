#### deadlock

+ `deadlock.py`: a simple demo showing how deadlock could happen, and how to prevent deadlocks by breaking the 4 conditions caused deadlock (use demo name in the program as follows):
  + Mutual Exclusion
  + Hold and Wait
  + Preemptive
  + Circular Wait
  ```py
   demo = "deadlock"
   demo == "Break Hold and Wait"
   demo == "Break preemption"
   demo == "Break circular wait"
  ```

+ `banker_algorithm`: a simple implementation of banker's algorithm for avoiding deadlock