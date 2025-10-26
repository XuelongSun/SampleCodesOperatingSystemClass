from typing import List, Tuple
from dataclasses import dataclass
import math
from analyser import metrics_gantt, plot_gantt

@dataclass
class RTJob:
    name: str
    arrive: int
    exec: int
    deadline: int

def collapse(g):
    if not g: return g
    out=[[g[0][0], g[0][1], g[0][2]]]
    for n,s,e in g[1:]:
        if out[-1][0]==n and out[-1][2]==s: out[-1][2]=e
        else: out.append([n,s,e])
    return [(n,s,e) for n,s,e in out]

def simulate_rt(jobs, policy="EDF"):
    if policy == "P-EDF":
        return simulate_preemptive_edf(jobs)
    elif policy == "P-LLF":
        return simulate_preemptive_llf(jobs)
    t=0; ready=[];
    pending=sorted(jobs,key=lambda x:x.arrive);
    rem={x.name:x.exec for x in jobs}; gantt=[]; finish={}
    def admit():
        nonlocal pending, ready, t
        while pending and pending[0].arrive<=t: ready.append(pending.pop(0))
    admit()
    while ready or pending:
        if not ready: t=pending[0].arrive; admit()
        if policy=="EDF": ready.sort(key=lambda x:x.deadline)
        elif policy=="LLF": ready.sort(key=lambda x:(x.deadline - (t + rem[x.name])))
        else: raise ValueError(f"Unknown policy: {policy}")
        cur=ready[0]; start=t; rem[cur.name]-=1; t+=1; admit()
        if rem[cur.name]==0: finish[cur.name]=t; ready.pop(0); gantt.append((cur.name,start,t))
        else: gantt.append((cur.name,start,t))
    collapsed=[]
    for n,s,e in gantt:
        if not collapsed: collapsed.append([n,s,e])
        else:
            if collapsed[-1][0]==n and collapsed[-1][2]==s: collapsed[-1][2]=e
            else: collapsed.append([n,s,e])
    gantt=[(n,s,e) for n,s,e in collapsed]
    
    miss = {j.name: (finish.get(j.name, math.inf) > j.deadline) for j in jobs}
    return gantt, miss

def simulate_preemptive_edf(jobs: List[RTJob]):
    t=0; ready=[]; pending=sorted(jobs, key=lambda x:x.arrive)
    rem={j.name:j.exec for j in jobs}; finish={}; gantt=[]; cur=None
    def admit():
        nonlocal ready,pending,t
        while pending and pending[0].arrive<=t: ready.append(pending.pop(0))
    admit()
    while ready or pending or cur:
        if not ready and cur is None: t=pending[0].arrive; admit()
        if cur is None and ready:
            ready.sort(key=lambda x:x.deadline); cur=ready.pop(0); seg_start=t
        else:
            if ready:
                best=min(ready, key=lambda x:x.deadline)
                if best.deadline < cur.deadline:
                    gantt.append((cur.name, seg_start, t)); ready.append(cur)
                    ready.sort(key=lambda x:x.deadline); cur=ready.pop(0); seg_start=t
        rem[cur.name]-=1; t+=1; admit()
        if rem[cur.name]==0:
            finish[cur.name]=t; gantt.append((cur.name, seg_start, t)); cur=None
    gantt=collapse(gantt); missed={j.name:(finish.get(j.name, math.inf) > j.deadline) for j in jobs}
    return gantt, missed

def simulate_preemptive_llf(jobs: List[RTJob]):
    t=0; ready=[]; pending=sorted(jobs, key=lambda x:x.arrive)
    rem={j.name:j.exec for j in jobs}; finish={}; gantt=[]; cur=None
    def admit():
        nonlocal ready,pending,t
        while pending and pending[0].arrive<=t: ready.append(pending.pop(0))
    def slack(job: RTJob): return job.deadline - (t + rem[job.name])
    admit()
    while ready or pending or cur:
        if not ready and cur is None: t=pending[0].arrive; admit()
        def best_job(): return min(ready, key=lambda x:(slack(x), rem[x.name], x.arrive))
        if cur is None and ready:
            cur=best_job(); ready.remove(cur); seg_start=t
        else:
            if ready:
                cand=best_job()
                if slack(cand) < slack(cur):
                    gantt.append((cur.name, seg_start, t)); ready.append(cur); cur=cand; ready.remove(cur); seg_start=t
        rem[cur.name]-=1; t+=1; admit()
        if rem[cur.name]==0:
            finish[cur.name]=t; gantt.append((cur.name, seg_start, t)); cur=None
    gantt=collapse(gantt); missed={j.name:(finish.get(j.name, math.inf) > j.deadline) for j in jobs}
    return gantt, missed

if __name__ == "__main__":
    # jobs=[RTJob("T1",0,3,7), RTJob("T2",1,2,6), RTJob("T3",2,2,5)]
    jobs=[RTJob("T1",0,3,10), RTJob("T2",1,5,6), RTJob("T3",2,2,7)]
    policy = "P-LLF"
    g, miss = simulate_rt(jobs, policy=policy)
    arrivals={j.name:j.arrive for j in jobs}; total=sum(j.exec for j in jobs)
    m, per = metrics_gantt(g, arrivals, total)
    print("Analysis:", m, per)
    plot_gantt(g, f"Real-Time Scheduling: {policy}", RT=jobs)

    
    print("Deadline Misses:", miss)