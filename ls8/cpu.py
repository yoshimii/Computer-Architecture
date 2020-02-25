"""CPU functionality."""

import sys

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.ram = [None] * 256  
        self.reg = [None] * 8
        self.pc = 0

    def ram_read(self, MAR):
        return self.ram[MAR]
    
    def ram_write(self, MDR, MAR):
        self.ram[MAR] = MDR

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
        PC = self.pc
        # print('STARTER', int(self.ram_read(PC), 2), PC)
        IR = int(self.ram_read(PC), 2)

        operand_a = self.ram_read(PC + 1)
        operand_b = self.ram_read(PC + 2)
                     
        while IR != 1:                       
            if IR == 130: # LDI
                self.ram_write(int(operand_b, 2), len(self.load()))
            elif IR == 71: # PRINT
                print(self.ram_read(len(self.load())))
            elif IR == 1: # HALT
                sys.exit(0)
            PC += 1
            IR = int(self.ram_read(PC), 2)

        

        
