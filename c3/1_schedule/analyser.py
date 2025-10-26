from dataclasses import dataclass
from typing import List, Tuple, Dict, Optional
import math
import matplotlib.pyplot as plt

bar_colors = ["#1f77b4", "#ff7f0e", "#2ca02c", "#d62728", "#9467bd", "#8c564b", "#e377c2", "#7f7f7f", "#bcbd22", "#17becf"]
def metrics_gantt(gantt: List[Tuple[str,int,int]], arrivals: Dict[str,int], total_work: Optional[int]=None):
    """ Calculate scheduling metrics from a Gantt chart.
    gantt: List of (job_name, start_time, end_time)
    arrivals: Dict of job_name to arrival_time
    total_work: total CPU work done (optional, for CPU utilization)
    """
    first_start = {}; finish = {}; burst = {};
    for n,s,e in gantt:
        if n not in first_start: first_start[n]=s
        finish[n]=e
        burst[n] = burst.get(n, 0) + (e - s)
    per={}
    for n in finish:
        a=arrivals[n]; r=first_start[n]-a; t=finish[n]-a; w=t-burst[n]
        per[n]={"arrival":a,"first_run":first_start[n],"finish":finish[n],
                "response":r,"turnaround":t,"waiting":w}
    avg_wait = sum(v["waiting"] for v in per.values())/len(per) if per else 0.0
    avg_turn = sum(v["turnaround"] for v in per.values())/len(per) if per else 0.0
    avg_resp = sum(v["response"] for v in per.values())/len(per) if per else 0.0
    if total_work is None:
        total_work = sum(e-s for _,s,e in gantt)
    makespan = (max(finish.values()) - min(arrivals.values())) if per else 0
    throughput = (len(per)/makespan) if makespan>0 else 0.0
    cpu_util = (total_work/makespan) if makespan>0 else 0.0
    return {"avg_wait":avg_wait,"avg_turnaround":avg_turn,"avg_response":avg_resp,
            "throughput":throughput,"cpu_util":cpu_util}, per

def plot_gantt(gantt: List[Tuple[str,int,int]], title: str, RT=None):
    order=[]; pos={}; 
    for n,s,e in gantt:
        if n not in pos: pos[n]=len(order); order.append(n)
    plt.figure(figsize=(8,2+0.4*len(order)))
    names = set([n for n,_,_ in gantt])
    colors = {}
    for i, (n,s,e) in enumerate(gantt):
        color = bar_colors[list(names).index(n) % len(bar_colors)]
        colors[n] = color
        y=pos[n]; plt.barh(y=y, width=(e-s), left=s, color=color); plt.text(s+(e-s)/2,y,n,ha="center",va="center")
    plt.yticks(range(len(order)), order); plt.xlabel("Time"); plt.title(title); 
    # also plot deadline as vertical lines and label the job's name if it is a RT job
    if RT:
        for j in RT:
            color = colors[j.name] if j.name in colors else 'r'
            plt.axvline(x=j.deadline, color=color, linestyle='--')
            plt.text(j.deadline, len(colors), f"{j.name}", rotation=45, verticalalignment='bottom',
                     color=color)
        plt.ylim(-1, len(order)+1)
        
    plt.tight_layout(); plt.show()

if __name__ == "__main__":
    # Example usage
    # example_gantt = [("P0",0,5),("P1",5,8),("P2",8,12)]
    example_gantt = [("P0",0,2),("P2",2,4),("P0",4,7),("P1",7,9)]
    arrivals = {"P0":0,"P1":1,"P2":2}
    metrics, per_job = metrics_gantt(example_gantt, arrivals)
    print("Metrics:", metrics)
    print("Per-job details:", per_job)
    plot_gantt(example_gantt, "Example Gantt Chart")