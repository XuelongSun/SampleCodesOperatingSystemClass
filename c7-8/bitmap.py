class BitmapDisk:
    def __init__(self, total_blocks=16):
        self.total_blocks = total_blocks
        self.bitmap = 0
        
    def allocate(self):
        for i in range(self.total_blocks):
            if (self.bitmap & (1 << i)) == 0:  # check if free
                self.bitmap |= (1 << i)  # set to 1
                print(f"Allocate {i}, Bitmap: {bin(self.bitmap)[2:].zfill(self.total_blocks)}")
                return i
        return -1  # No free block
        
    def free(self, block_num):
        self.bitmap &= ~(1 << block_num)  # set 0
        print(f"Free {block_num}, Bitmap: {bin(self.bitmap)[2:].zfill(self.total_blocks)}")

# 演示
disk = BitmapDisk(16)
disk.allocate()
disk.allocate()
disk.free(0)
disk.allocate()