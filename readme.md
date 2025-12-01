### Codes used in my Operating System class

The source files are organized into folders `c[x]` by chapters and `lab[x]` by Labs.

#### c1
*Introduction to OS*
+ `1_hello.c`: show how computer could read binary while we coding in C
  ```bash
  gcc 1_hello.c -o 1_hello.o
  ```
  then use `xdd` to check the binary file:
  ```bash
  xdd 1_hello.o | less
  ```

#### c2
*Process Description and Control*
+ `1_cpu.c`: shows how OS makes concurrency possible.
    compile and then run multiples and check/kill the process:
    ```bash
    gcc 1_cpu.c -o cpu.o
    ./cpu A & ./cpu.o B &
    ps aux | grep cpu
    kill [pid]
    ```
+ `2_mthreads.c`: show that without OS, process concurrency will bring mistakes.
+ `3_zombie_process.py`: use `os.fork()` to create a child process to see the `X` state.
+ `4_process_state_demo/`: bash commands to observe different kind of process state in Linux.
+ `5_mutual_exclusion/`: demos for *locks*, *mutex*, *peterson algorithms*, etc.
+ `6_sync/`: demos for *conditional variable*, *semaphores* solving *producer-consumer* problems.
+ `7_communication/`: demos for process communication.
+ `8_threads/`: demos for threads.

#### c3
*Scheduling and Deadlock*
+ `1_schedule`: implementation of the job/process/realtime scheduling algorithms and their analysis
+ `2_deadlock`: deadlock demos and algorithms for prevent, avoid (banker's algorithm) and detecting deadlock.

#### c7-8
*File System*


#### lab1 
*OS interface of Linux*
+ `templates.md`: template for writing the report of the Lab1 assignment. 
+ `students_v1.csv` and `students_v2.csv` for file comparison.
+ `c_project`: for file processing jobs.
+ `linux.png`: for image processing jobs.
+ `sys_call_copy.py`: python implementation of file copy using system calls.

#### lab2
*Mutual exclusion and synchronization*
+ `templates.md`: template for writing the report of the Lab2 assignment. 
+ `framework.py`: basic codes for the experiment

#### lab3
*CPU simulating and program running*
+ `templates.md`: template for writing the report of the Lab3 assignment. 
+ `framework/`: basic codes for the experiment

#### lab4
*Schedule algorithms on lab3' CPU*
+ `templates.md`: template for writing the report of the Lab4 assignment. 

#### lab5
*Memory Allocation*
+ `run.py`: testing demo scripts for memory allocation
+ `memory.py`: start-file of implementing fixed and dynamic memory allocation methods.
+ `templates.md`: template for writing the report of the Lab5 assignment. 

#### lab6
*Memory Management and Virtual Memory*
+ `memory.py`: start-file of implementing page-based memory management and virtual memory.
+ `templates.md`: template for writing the report of the Lab6 assignment. 