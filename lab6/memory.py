from typing import Dict
import random
import prettytable
import colorama
from colorama import Fore, Back, Style
colorama.init(autoreset=True)

class PageEntry:
    def __init__(self):
        self.present = False
        self.frame = None
        self.disk_location = None 
        self.accessed = False
        self.modified = False

class PageTable:
    def __init__(self):
        self.entries:Dict[int, PageEntry] = {}

class MemoryFrame:
    def __init__(self, frame_number):
        self.frame_number = frame_number
        self.free = True
        self.pid = None

class PageMemory:
    def __init__(self, physical_size=1024, page_size=1):
        # 按顺序i给物理块编号
        self.frames = [MemoryFrame(i) for i in range(physical_size // page_size)] 
        self.page_size = page_size
        # page tables - 各进程的页表用字典存储(现实中是放在内存中)
        self.page_tables:Dict[str, PageTable] = {}
    
    def create_page_table(self, pid, num_pages):
        # 为进程创建页表
        pt = PageTable()
        for i in range(num_pages):
            ...
        # 创建后填入page_tables
        self.page_tables[pid] = pt

    def allocate_frame(self, pid):
        # 为页分配物理块
        ...
        # 返回物理块号
        return frame_index

    def show_memory(self):
        # print frame number
        for i in range(len(self.frames)):
            print(f" {Fore.GREEN}{i:^4} ", end='' if i < len(self.frames) -1 else f'\n{Style.RESET_ALL}')
        print("┌" + "─────┬" * (len(self.frames) - 1) + "─────┐")
        frame_display = "│"
        for frame in self.frames:
            if frame.free:
                # frame_display += f" {Back.GREEN}{Fore.WHITE}{" ".center(3)}{Style.RESET_ALL} │"
                frame_display += f"{" ".center(5)}│"
            else:
                frame_display += f" {Back.RED}{Fore.WHITE}{frame.pid:^3}{Style.RESET_ALL} │"
        print(frame_display)
        print("└" + "─────┴" * (len(self.frames) - 1) + "─────┘")
    
    def show_page_table(self, pid):
        if pid not in self.page_tables:
            print(f"No page table for process {pid}")
            return
        pt = self.page_tables[pid]
        # table header
        table = prettytable.PrettyTable()
        table.field_names = ["Page", "Frame", "Present", "Disk Location", "Accessed", "Modified"]
        for vpage, entry in pt.entries.items():
            table.add_row([
                vpage,
                entry.frame if entry.frame is not None else "-",
                entry.present,
                entry.disk_location if entry.disk_location is not None else "-",
                entry.accessed,
                entry.modified
            ])
        print(table)


class RequestPageMemory:
    def __init__(self, physical_size=1024, page_size=1,
                 allocate_num_frame=3, page_replacement_algorithm="FIFO"):
        #frames
        self.frames = [MemoryFrame(i) for i in range(physical_size // page_size)]
        self.page_size = page_size
        # pre-load number of pages/frames per process
        self.allocate_num_frame = allocate_num_frame
        
        # page tables
        self.page_tables:Dict[str, PageTable] = {}
        
        # simulate disk storage
        self.disk = []
        
        # data structure for page replacement
        # 1. algorithm
        self.page_replacement_algorithm = page_replacement_algorithm
        # 2. for FIFO 
        self.fifo_
        # 3. for LRU
        self.lru_

        # efficiency metrics
        self.page_faults = 0
        self.page_hits = 0
    
    def create_page_table(self, pid, num_pages):
        pass

    def allocate_frame(self, pid):
        pass
        return frame_index
    
    def handle_page_fault(self, pid, vpage):
        pass

    def page_replacement(self, pid, page):
        pass
    
    def access_page(self, pid, page):
        pass

    def get_page_fault_rate(self):
        pass
    
    def show_page_table(self, pid):
        if pid not in self.page_tables:
            print(f"No page table for process {pid}")
            return
        pt = self.page_tables[pid]
        # table header
        table = prettytable.PrettyTable()
        table.field_names = ["Page", "Frame", "Present", "Disk Location", "Accessed", "Modified"]
        for vpage, entry in pt.entries.items():
            table.add_row([
                vpage,
                entry.frame if entry.frame is not None else "-",
                entry.present,
                entry.disk_location if entry.disk_location is not None else "-",
                entry.accessed,
                entry.modified
            ])
        print(table)


if __name__ == "__main__":
    # 1kb frame size (page size) and 16 frames (16kb physical memory)
    mm = PageMemory(physical_size=16, page_size=1)
    vmm = RequestPageMemory(physical_size=6, page_size=1,
                            allocate_num_frame=3,
                            page_replacement_algorithm="LRU")
    processes = {
        'P1': {'pages': 4, 'page_access': [0, 3, 2, 1, 3, 1, 0, 1, 3, 2, 1, 2, 3, 2, 1, 3]},
        'P2': {'pages': 6, 'page_access': [0, 3, 0, 4, 2, 3, 0, 3, 2, 1, 2, 0, 1, 5, 0, 1]},
    }
    for pid, info in processes.items():
        pt = mm.create_page_table(pid, info['pages'])
        vpt = vmm.create_page_table(pid, info['pages'])
    
    # 1.分页存储
    print("Page-based Memory Management:")
    mm.show_memory()
    for pid, pt in mm.page_tables.items():
        print(f"Process {pid}:")
        mm.show_page_table(pid)
    print("*"*100)
    
    # 2.请求分页存储
    print("Virtual Memory Management:")
    vmm.show_page_table('P1')
    vmm.show_page_table('P2')
    # 遍历进程
    for pid, info in processes.items():
        print(f"Process {pid} accessing pages: {info['page_access']}")
        # 遍历页面访问序列
        for page in info['page_access']:
            vmm.access_page(pid, page)
        print(f"Page Faults Rate for Process {pid}: {vmm.page_faults}/{vmm.page_faults + vmm.page_hits} = {vmm.get_page_fault_rate():.2f}")
        vmm.page_faults = 0  # reset for next process
        vmm.page_hits = 0
    vmm.show_page_table('P1')
    vmm.show_page_table('P2')

