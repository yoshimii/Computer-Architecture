"""CPU functionality."""

import sys

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.ram = [None] * 256  
        self.reg = [None] * 8
        self.pc = 0
        self.sp = 244
        self.ram[244] = '*' # Mark bottom of stack
        self.fl = 0b00000000 #0b00000LGE (less than, greater than, equal)
        
    def ram_read(self, MAR):
        return self.ram[MAR]
    
    def ram_write(self, MDR, MAR):
        self.ram[MAR] = MDR

    def load(self, filename):
        """Load a program into memory."""

        address = 0
        program = []

        
        with open(filename) as f:
                for line in f:
                    text = line.split('#')
                    num = text[0].strip()
                    if num != '':
                        # program.append(int((num), 2))
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
        elif op =="CMP":
            if self.reg[reg_a] < self.reg[reg_b]: # L
                self.fl = 0b00000100 or self.fl
            if self.reg[reg_a] == self.reg[reg_b]: # E
                self.fl = 0b00000001 or self.fl
            if self.reg[reg_a] > self.reg[reg_b]: # G
                self.fl = 0b00000010 or self.fl
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
        SP = self.sp
        PC = self.pc
        IR = int(self.ram_read(PC), 2)
                     
        while True:

            if IR == 130: # LDI                
                operand_a = int(self.ram_read(PC + 1), 2)
                operand_b = int(self.ram_read(PC + 2), 2)
                self.reg[operand_a] = operand_b
                
            elif IR == 69: # PUSH the register in next IR to stack: SP - 1, increment SP                
                self.ram_write(self.reg[int(self.ram_read(PC + 1), 2)], SP - 1)
                SP -= 1
                
            elif IR == 70: # POP the value from top of stack (SP) and store in register in next IR, decrement SP                
                POP = self.ram[SP]
                self.ram[SP] == None
                self.reg[int(self.ram_read(PC + 1), 2)] = POP
                SP += 1
                
            elif IR == 71: # PRINT                
                print(self.reg[int(self.ram_read(PC + 1), 2)])       
                         
            elif IR == 162: #        
                operand_a = int(self.ram_read(PC + 1), 2)
                operand_b = int(self.ram_read(PC + 2), 2)
                self.alu("MUL", operand_a, operand_b)
            
            elif IR == 160: # ADD
                operand_a = int(self.ram_read(PC + 1), 2)
                operand_b = int(self.ram_read(PC + 2), 2)
                self.alu("ADD", operand_a, operand_b)
                
            elif IR == 80: # CALL a subroutine at the address stored in the register
                self.ram_write(PC + 2, SP - 1)
                SP -= 1
                PC = self.reg[int(self.ram_read(PC + 1), 2)]                
                
            elif IR == 17: # RET
                POP = self.ram[SP]
                self.ram[SP] = None
                PC = POP
                SP += 1
                
            elif IR == 84: # JMP
                PC = self.reg[int(self.ram_read(PC + 1), 2)]
                
            elif IR == 85: # JEQ
                if self.fl & 0b00000001:
                    PC = self.reg[int(self.ram_read(PC + 1), 2)]
                else: PC += 2
                    
            elif IR == 86: # JNE
                if not self.fl & 0b00000001:
                    PC = self.reg[int(self.ram_read(PC + 1), 2)]
                else: PC += 2
                    
            elif IR == 167: # CMP
                operand_a = int(self.ram_read(PC + 1), 2)
                operand_b = int(self.ram_read(PC + 2), 2)
                self.alu("CMP", operand_a, operand_b)                    
                    
                    
                
            elif IR == 1: # HALT                
                sys.exit(0)                
            if not (IR & 0b00010000): # If not a CALL 
                PC += 1 + (IR >> 6)  
            IR = int(self.ram_read(PC), 2)
            # print(PC, IR)
            # print("REG", self.reg)
            # print("RAM", self.ram[-20:])