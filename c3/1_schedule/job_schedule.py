from typing import List, Tuple, Dict, Optional
from dataclasses import dataclass
from analyser import metrics_gantt, plot_gantt

@dataclass
class Job:
    name: str
    arrive: int
    svc: int
    prio: int = 0


def simulate(tasks: List[Job], policy: str):
    t = 0; 
    # sorted by arrival time
    pending = sorted(tasks, key=lambda x:x.arrive)
    ready=[]
    gantt=[]
    def admit():
        nonlocal pending,ready,t
        while pending and pending[0].arrive <= t:
            ready.append(pending.pop(0))
    admit()
    while ready or pending:
        if not ready:
            t = pending[0].arrive
            admit()
        if policy=="FCFS": ready.sort(key=lambda x:x.arrive)
        elif policy=="SJF": ready.sort(key=lambda x:x.svc)
        elif policy=="PRIO": ready.sort(key=lambda x:x.prio)
        elif policy=="HRRN": ready.sort(key=lambda x: -((t-x.arrive+x.svc)/x.svc))
        cur = ready.pop(0)
        start = t
        end = t + cur.svc
        gantt.append((cur.name,start,end))
        t = end
        admit()

    return gantt

if __name__ == "__main__":
    # Example usage
    tasks = [Job('A',0,2), Job('B',2,4), Job('C',4,2),Job('D',6,3)]
    # tasks = [Job("P0",0,5,2), Job("P1",0,3,0), Job("P2",2,4,1)]
    gantt = simulate(tasks, "FCFS")
    
    arrivals = {j.name:j.arrive for j in tasks}
    total = sum(j.svc for j in tasks)
    
    m, per = metrics_gantt(gantt, arrivals, total)
    
    plot_gantt(gantt, "FCFS Scheduling")
    print("Analysis:", m, per)