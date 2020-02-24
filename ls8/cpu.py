"""CPU functionality."""

import sys

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.ram = [None] * 256  
        self.reg = [None] * 8
        self.pc = 0

    def ram_read(self, pc):
        return self.ram[pc]
    
    def ram_write(self, pc):
        print(self.ram[pc])

    def load(self,):
        """Load a program into memory."""

        address = 0
        program = []

        
        with open("examples/print8.ls8") as f:
                for line in f:
                    text = line.split('#')
                    num = text[0].strip()
                    if num != '':
                        program.append(num)

        for instruction in program:
            self.ram[address] = instruction
            address += 1
        return program
        
        


    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        elif op == "SUB":
            self.reg[reg_a] -= self.reg[reg_b]
        elif op == "MUL":
            self.reg[reg_a] *= self.reg[reg_b]
        elif op == "DIV":
            self.reg[reg_a] /= self.reg[reg_b]
        elif op =="MOD":
            self.reg[reg_a] %= self.reg[reg_b]
        elif op =="LDI":
            self.reg[reg_a] = int(self.reg[reg_a])
        elif op =="HLT":
            sys.exit(0)
        else:
            raise Exception("Unsupported ALU operation")

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.pc,
            #self.fl,
            #self.ie,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.reg[i], end='')

        print()

    def run(self):
        """Run the CPU."""

        
