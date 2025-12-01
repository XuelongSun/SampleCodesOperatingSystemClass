from typing import List, Tuple, Dict, Optional
from dataclasses import dataclass
from analyser import metrics_gantt, plot_gantt

@dataclass
class Job:
    name: str
    arrive: int
    svc: int
    prio: int = 0


def simulate_preemptive_jobs(
    jobs: List[Job],
    policy: str = "SRTF",
    aging_per_tick: float = 0.1
) -> Tuple[List[Tuple[str,int,int]], Dict]:
    """
    policies: "SRTF", "PRIO_P", "HRRN_P"
    aging_per_tick: for PRIO_P (effective_prio = base_prio - aging*waiting)
    """
    # State
    t = 0
    pending = sorted(jobs, key=lambda x: x.arrive)
    ready: List[Job] = []
    rem = {j.name: j.svc for j in jobs}
    wait = {j.name: 0 for j in jobs}  # waiting time since arrival or last run
    last_owner = None
    seg_start = None
    gantt: List[Tuple[str,int,int]] = []

    def admit():
        nonlocal pending, ready, t
        changed = False
        while pending and pending[0].arrive <= t:
            ready.append(pending.pop(0))
            changed = True
        return changed

    admit()
    while ready or pending:
        # If nothing is ready, jump to next arrival
        if not ready:
            t = pending[0].arrive
            admit()

        # Update waiting counters for policy decisions
        for j in ready:
            if j.name != last_owner:
                wait[j.name] += 1  # 1 tick per loop if not running

        # Choose next by policy (recompute every tick)
        if policy == "SRTF":
            # smallest remaining time
            ready.sort(key=lambda x: rem[x.name])
        elif policy == "PRIO_P":
            # effective priority with linear aging (smaller is better)
            ready.sort(key=lambda x: (x.prio - aging_per_tick * wait[x.name], rem[x.name]))
        elif policy == "HRRN_P":
            # Highest Response Ratio using remaining time:
            # RR = (waiting + remaining) / remaining = 1 + waiting/remaining
            # choose the MAX ratio
            ready.sort(key=lambda x: -((wait[x.name] + rem[x.name]) / max(1, rem[x.name])))
        else:
            raise ValueError("Unknown policy")

        cur = ready[0]

        # Handle preemption boundaries for Gantt
        if last_owner is None:
            last_owner = cur.name
            seg_start = t
        elif cur.name != last_owner:
            gantt.append((last_owner, seg_start, t))
            seg_start = t
            last_owner = cur.name

        # Run the chosen job for 1 tick (preemptive granularity)
        rem[cur.name] -= 1
        t += 1
        admit()

        # If current finished, close segment and remove from ready
        if rem[cur.name] == 0:
            gantt.append((cur.name, seg_start, t))
            ready.pop(0)  # remove cur
            last_owner = None
            seg_start = None

    # Normalize: collapse adjacent identical segments
    # ['A',0,2], ['A',2,5]  =>  ['A',0,5]
    collapsed = []
    for n, s, e in gantt:
        if not collapsed:
            collapsed.append([n, s, e])
        else:
            if collapsed[-1][0] == n and collapsed[-1][2] == s:
                collapsed[-1][2] = e
            else:
                collapsed.append([n, s, e])
    gantt = [(n, s, e) for n, s, e in collapsed]

    arrivals = {j.name: j.arrive for j in jobs}
    total = sum(j.svc for j in jobs)
    m, per = metrics_gantt(gantt, arrivals, total)
    return gantt, {"metrics": m, "per_job": per}


if __name__ == "__main__":
    # workload = [Job("P0",0,5,2), Job("P1",1,2,1), Job("P2",2,2,3)]
    workload = [Job('A',0,2), Job('B',2,4), Job('C',4,2),Job('D',6,3)]
    pol = "SRTF"
    g, info = simulate_preemptive_jobs(workload, policy=pol, aging_per_tick=0.2)
    plot_gantt(g, f"Preemptive job scheduling: {pol}")
    print(pol, info["metrics"])
