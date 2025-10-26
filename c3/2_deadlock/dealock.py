import threading
import time

printer_lock = threading.Lock()
disk_lock = threading.Lock()

class Resource:
    def __init__(self, name):
        self.name = name
        self.lock = threading.Lock()
        self.owner = None
    
    def acquire(self, owner):
        print(f"{owner} ==> {self.name}")
        self.lock.acquire()
        self.owner = owner
        print(f"{owner} 🔒 {self.name}")
        return True
    
    def acquire_with_timeout(self, owner, timeout=4):
        print(f"{owner} ==> {self.name} ({timeout}s)")
        acquired = self.lock.acquire(timeout=timeout)
        if acquired:
            self.owner = owner
            print(f"{owner} 🔒 {self.name}")
        else:
            print(f"{owner} ❌ {self.name} (timeout)")
        return acquired
    
    def release(self):
        if self.lock.locked():
            print(f"{self.owner} 🔓 {self.name}")
            self.owner = None
            self.lock.release()
            

class NumberResource(Resource):
    def __init__(self, name, num):
        super().__init__(name)
        self.N = num

resources = {
    "printer": Resource("🖨️"),
    "disk": Resource("💾"),
}

num_resources = {
    "printer": NumberResource("🖨️", 2),
    "disk": NumberResource("💾", 1),
}

def programmer_a():
    resources["printer"].acquire("A")
    time.sleep(2) 
    resources["disk"].acquire("A")  
    time.sleep(1)
    print("A: ✅")
    resources["printer"].release()
    resources["disk"].release()

def programmer_b():
    resources["disk"].acquire("B")
    time.sleep(2) 
    resources["printer"].acquire("A")  
    time.sleep(1)
    print("B:✅")
    resources["printer"].release()
    resources["disk"].release()


def safe_worker_bhw(name, needed_resources):
    acquired = []
    try:
        for res in needed_resources:
            resources[res].acquire(name)
            acquired.append(res)
        time.sleep(1)
        print(f"{name}: ✅")
    finally:
        for res in reversed(acquired):
            resources[res].release()

def safe_worker_bp(name, needed_resources):
    while(1):
        acquired = []
        for res in needed_resources:
            if resources[res].acquire_with_timeout(name):
                acquired.append(res)
                time.sleep(1)
            else:
                for r in reversed(acquired):
                    resources[r].release()
                    acquired.remove(r)
        if len(acquired) == len(needed_resources):
            time.sleep(1)
            print(f"{name}: ✅")
            for res in reversed(needed_resources):
                resources[res].release()
            break

def safe_worker_bcw(name, needed_resources):
    # Enforce a global order: printer < disk
    sorted_resources = sorted(needed_resources,
                              key=lambda r: num_resources[r].N)
    acquired = []
    try:
        for res in sorted_resources:
            resources[res].acquire(name)
            acquired.append(res)
        time.sleep(1)
        print(f"{name}: ✅")
    finally:
        for res in reversed(acquired):
            resources[res].release()


if __name__ == "__main__":
    demo = "deadlock"
    if demo == "deadlock":
        thread1 = threading.Thread(target=programmer_a)
        thread2 = threading.Thread(target=programmer_b)
    elif demo == "Break Hold and Wait":
        thread1 = threading.Thread(target=safe_worker_bhw, args=("A", ["printer", "disk"]))
        thread2 = threading.Thread(target=safe_worker_bhw, args=("B", ["disk", "printer"]))
    elif demo == "Break preemption":
        thread1 = threading.Thread(target=safe_worker_bp, args=("A", ["printer", "disk"]))
        thread2 = threading.Thread(target=safe_worker_bp, args=("B", ["disk", "printer"]))
    elif demo == "Break circular wait":
        thread1 = threading.Thread(target=safe_worker_bcw, args=("A", ["printer", "disk"]))
        thread2 = threading.Thread(target=safe_worker_bcw, args=("B", ["disk", "printer"]))
    else:
        pass

    thread1.start()
    thread2.start()
    thread1.join() 
    thread2.join()
    