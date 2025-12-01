from typing import List, Tuple
from dataclasses import dataclass
from analyser import metrics_gantt, plot_gantt

@dataclass
class Process:
    name: str
    arrive: int
    svc: int
    prio: int = 0

def simulate_rr(tasks: List[Process], quantum: int):
    from collections import deque
    t = 0
    q = deque()
    pending = sorted(tasks,key=lambda x:x.arrive)
    rem = {x.name:x.svc for x in tasks} # remaining times
    gantt=[]
    def admit():
        nonlocal pending,q,t
        while pending and pending[0].arrive<=t:
            q.append(pending.pop(0))
    admit()
    while q or pending:
        if not q:
            t = pending[0].arrive
            admit()
        cur = q.popleft()
        run = min(quantum, rem[cur.name]) # if less than quantum, just run to finish
        start = t
        t += run
        end = t
        gantt.append((cur.name, start, end))
        admit()
        rem[cur.name] -= run
        if rem[cur.name] > 0:
            q.append(cur)
    
    return gantt

def simulate_mlfq(tasks: List[Process], quanta: Tuple[int,...]=(2,4)):
    from collections import deque
    t = 0
    Q = [deque() for _ in quanta] # multiple queues
    pending = sorted(tasks, key=lambda x:x.arrive)
    rem = {x.name:x.svc for x in tasks}
    gantt = []
    def admit():
        nonlocal pending
        while pending and pending[0].arrive <= t:
            Q[0].append(pending.pop(0))
    admit()
    while any(Q) or pending:
        if not any(Q):
            t = pending[0].arrive
            admit() 
        for level, quantum in enumerate(quanta):
            if Q[level]:
                cur = Q[level].popleft()
                run = min(quantum, rem[cur.name])
                start = t
                t += run
                end = t
                gantt.append((cur.name, start, end))
                admit()
                rem[cur.name] -= run
                if rem[cur.name] > 0:
                    next_level = min(level + 1, len(quanta) - 1)
                    Q[next_level].append(cur)
                break
    
    return gantt

if __name__ == "__main__":
    # Example usage
    process = [Process('A',0,2), Process('B',2,4), Process('C',4,2), Process('D',6,3)]
    # process = [Process("P0",0,3), Process("P1",1,6), Process("P2",2,4), Process("P3",4,2)]
    gantt = simulate_rr(process, quantum=1)
    
    # gantt = simulate_mlfq(process,(1,2))
    arrivals = {j.name:j.arrive for j in process}
    total = sum(j.svc for j in process)
    m, per = metrics_gantt(gantt, arrivals, total)
    plot_gantt(gantt, "Round Robin Scheduling (quantum=1)")
    # plot_gantt(gantt, "Multi-level feedback queue (quantum=1,2)")
    print("Analysis:", m, per)