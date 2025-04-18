"""
disassembler.py

Author: Gris Iscomeback 
Email: grisiscomeback[at]gmail[dot]com
Date: 14/04/2025
Licencia: GPL v3

Description: This file contain a rudimentary disassembler with no warranty

██╗      █████╗ ███████╗██╗   ██╗ ██████╗ ██╗    ██╗███╗   ██╗
██║     ██╔══██╗╚══███╔╝╚██╗ ██╔╝██╔═══██╗██║    ██║████╗  ██║
██║     ███████║  ███╔╝  ╚████╔╝ ██║   ██║██║ █╗ ██║██╔██╗ ██║
██║     ██╔══██║ ███╔╝    ╚██╔╝  ██║   ██║██║███╗██║██║╚██╗██║
███████╗██║  ██║███████╗   ██║   ╚██████╔╝╚███╔███╔╝██║ ╚████║
╚══════╝╚═╝  ╚═╝╚══════╝   ╚═╝    ╚═════╝  ╚══╝╚══╝ ╚═╝  ╚═══╝

"""

import sys
import struct

class X64Disassembler:
    """
    A disassembler class for x86-64 architecture.

    This class provides methods to disassemble raw binary data into human-readable assembly instructions.
    It supports parsing ELF headers, decoding ModR/M and SIB bytes, and handling various instruction formats.

    License: GPL v3
    """

    def __init__(self):
        """
        Initializes the X64Disassembler instance.

        Sets up registers, syscalls, and other necessary attributes for disassembly.
        """
        
        # Registers of 64 bits
        # Registros de 64 bits
        self.registers = {
            0: "rax", 1: "rcx", 2: "rdx", 3: "rbx",
            4: "rsp", 5: "rbp", 6: "rsi", 7: "rdi",
            8: "r8",  9: "r9",  10: "r10", 11: "r11",
            12: "r12", 13: "r13", 14: "r14", 15: "r15"
        }
        
        # Registers of 8 bits
        # Registros de 8 bits
        self.registers8 = {
            0: "al", 1: "cl", 2: "dl", 3: "bl",
            4: "spl", 5: "bpl", 6: "sil", 7: "dil",
            8: "r8b", 9: "r9b", 10: "r10b", 11: "r11b",
            12: "r12b", 13: "r13b", 14: "r14b", 15: "r15b"
        }
        
        # Registers of 32 bits
        # Registros de 32 bits
        self.registers32 = {
            0: "eax", 1: "ecx", 2: "edx", 3: "ebx",
            4: "esp", 5: "ebp", 6: "esi", 7: "edi",
            8: "r8d", 9: "r9d", 10: "r10d", 11: "r11d",
            12: "r12d", 13: "r13d", 14: "r14d", 15: "r15d"
        }
        
        # Table of syscalls to Linux x86_64
        # Tabla de syscalls en Linux x86_64
        self.syscalls = {
            0: "read",
            1: "write",
            2: "open",
            3: "close",
            59: "execve",
            60: "exit"
        }

    def read_elf_header(self, data):
        """
        Reads the ELF header and finds the code section.

        This function parses the ELF file header to locate the executable segment (TEXT).
        It checks for 64-bit ELF files and extracts the program headers to find the 
        first executable segment. Returns the offset, virtual address, size and entry point 
        of the TEXT segment if found.

        Parameters:
            data (bytes): The raw bytes of the ELF file
        
        Returns:
            tuple: (offset, virtual_address, size, entry_point) or (None, None, None, None) if not found

        Licencia: GPL v3
        """

        # Leer la cabecera ELF y verificar que sea un archivo válido
        # Read the ELF header and check if it's a valid file
        if len(data) < 0x40 or data[:4] != b'\x7fELF':
            return None, None, None, None

        # Verificar que sea un archivo ELF de 64 bits
        # Check for 64-bit ELF file
        ei_class = data[4]
        if ei_class != 0x02:
            return None, None, None, None

        # Obtener el offset a la tabla de encabezados de programa
        # Get the offset to the program headers table
        ph_offset = struct.unpack("<Q", data[0x20:0x28])[0]
        ph_entry_size = struct.unpack("<H", data[0x36:0x38])[0]
        ph_count = struct.unpack("<H", data[0x38:0x3A])[0]
        entry_point = struct.unpack("<Q", data[0x18:0x20])[0]

        # Buscar el segmento ejecutable (TEXT)
        # Search for the executable segment (TEXT)
        for i in range(ph_count):
            ph_entry = data[ph_offset + i * ph_entry_size : ph_offset + (i + 1) * ph_entry_size]
            p_type = struct.unpack("<I", ph_entry[0:4])[0]
            p_flags = struct.unpack("<I", ph_entry[4:8])[0]
            p_offset = struct.unpack("<Q", ph_entry[0x8:0x10])[0]
            p_vaddr = struct.unpack("<Q", ph_entry[0x10:0x18])[0]
            p_filesz = struct.unpack("<Q", ph_entry[0x20:0x28])[0]
            p_memsz = struct.unpack("<Q", ph_entry[0x28:0x30])[0]

            # Verificar si es un segmento ejecutable
            # Check if it's an executable segment
            if p_type == 0x1 and (p_flags & 0x1):
                return p_offset, p_vaddr, p_filesz, entry_point

        # Si no se encuentra ningún segmento ejecutable
        # If no executable segment is found
        return None, None, None, None

    def parse_modrm(self, modrm, rex=0):
        """
        Parses the ModR/M byte and extracts mod, reg, and rm fields.

        This function decodes the ModR/M byte used in x86/x64 instructions to determine 
        how operands are addressed. It also applies REX prefix extensions if present.

        Parameters:
            modrm (int): The ModR/M byte to be parsed.
            rex (int): Optional REX prefix byte (default is 0).

        Returns:
            tuple: A tuple containing the decoded `mod`, `reg`, and `rm` fields.

        License: GPL v3
        """

        # Extraer el campo 'mod' (bits 7-6)
        # Extract the 'mod' field (bits 7-6)
        mod = (modrm >> 6) & 0x03

        # Extraer el campo 'reg' (bits 5-3)
        # Extract the 'reg' field (bits 5-3)
        reg = (modrm >> 3) & 0x07

        # Extraer el campo 'rm' (bits 2-0)
        # Extract the 'rm' field (bits 2-0)
        rm = modrm & 0x07

        # Aplicar las extensiones REX si están presentes
        # Apply REX extensions if they exist
        if rex & 0x04:  # REX.R (extiende el campo 'reg')
            reg |= 0x08  # Extend the 'reg' field
        if rex & 0x01:  # REX.B (extiende el campo 'rm')
            rm |= 0x08   # Extend the 'rm' field

        return mod, reg, rm

    def parse_sib(self, sib, rex=0):
        """
        Parses the SIB byte and extracts scale, index, and base fields.

        This function decodes the Scale/Index/Base (SIB) byte used in x86/x64 addressing modes 
        to determine how memory operands are addressed. It also applies REX prefix extensions 
        if present.

        Parameters:
            sib (int): The SIB byte to be parsed.
            rex (int): Optional REX prefix byte (default is 0).

        Returns:
            tuple: A tuple containing the decoded `scale`, `index`, and `base` fields.

        License: GPL v3
        """

        # Extraer el campo 'scale' (bits 7-6)
        # Extract the 'scale' field (bits 7-6)
        scale = (sib >> 6) & 0x03

        # Extraer el campo 'index' (bits 5-3)
        # Extract the 'index' field (bits 5-3)
        index = (sib >> 3) & 0x07

        # Extraer el campo 'base' (bits 2-0)
        # Extract the 'base' field (bits 2-0)
        base = sib & 0x07

        # Aplicar las extensiones REX si están presentes
        # Apply REX extensions if they exist
        if rex & 0x02:  # REX.X (extiende el campo 'index')
            index |= 0x08  # Extend the 'index' field
        if rex & 0x01:  # REX.B (extiende el campo 'base')
            base |= 0x08   # Extend the 'base' field

        return scale, index, base

    def get_operand_str(self, mod, rm, rex, bytes_data, offset):
        """
        Gets the string representation of the operand based on mod/rm.

        This function decodes the addressing mode specified by the `mod` and `rm` fields 
        in x86/x64 instructions. It handles different cases such as RIP-relative, SIB, 
        and direct register addressing, applying REX prefix extensions if present.

        Parameters:
            mod (int): The 'mod' field from the ModR/M byte.
            rm (int): The 'rm' field from the ModR/M byte.
            rex (int): Optional REX prefix byte.
            bytes_data (bytes): The raw instruction bytes.
            offset (int): Current offset in the instruction bytes.

        Returns:
            tuple: A tuple containing the operand string representation and the number 
                of additional bytes consumed during parsing.

        License: GPL v3
        """

        disp = 0
        additional_bytes = 0

        if mod == 0:
            if rm == 5:  # RIP relative / Relativo a RIP
                # Leer desplazamiento de 32 bits / Read 32-bit displacement
                disp = int.from_bytes(bytes_data[offset:offset+4], byteorder='little', signed=True)
                additional_bytes = 4
                return f"[rip+{disp:#x}]", additional_bytes  # Devolver representación RIP-relative / Return RIP-relative representation

            elif rm == 4:  # Uso del byte SIB / Use SIB byte
                sib = bytes_data[offset]
                scale, index, base = self.parse_sib(sib, rex)  # Decodificar byte SIB / Decode SIB byte
                additional_bytes = 1

                if base == 5:  # Sin registro base, solo desplazamiento de 32 bits / No base register, only 32-bit displacement
                    disp = int.from_bytes(bytes_data[offset+1:offset+5], byteorder='little', signed=True)
                    additional_bytes += 4
                    if index == 4:  # Sin índice / No index
                        return f"[{disp:#x}]", additional_bytes  # Devolver solo desplazamiento / Return only displacement
                    else:
                        return f"[{self.registers[index]}*{1<<scale}+{disp:#x}]", additional_bytes  # Con índice / With index

                if index == 4:  # Sin índice / No index
                    return f"[{self.registers[base]}]", additional_bytes  # Solo base / Only base
                else:
                    return f"[{self.registers[base]}+{self.registers[index]}*{1<<scale}]", additional_bytes  # Base + índice / Base + index

            else:  # Caso simple: direccionamiento directo / Simple case: direct addressing
                return f"[{self.registers[rm]}]", additional_bytes

        elif mod == 1:  # Desplazamiento de 8 bits / 8-bit displacement
            disp = int.from_bytes(bytes_data[offset:offset+1], byteorder='little', signed=True)
            additional_bytes = 1

            if rm == 4:  # Byte SIB con desplazamiento de 8 bits / SIB byte with 8-bit displacement
                sib = bytes_data[offset]
                scale, index, base = self.parse_sib(sib, rex)
                additional_bytes = 2  # Byte SIB + desplazamiento de 8 bits / SIB byte + 8-bit displacement

                if index == 4:  # Sin índice / No index
                    return f"[{self.registers[base]}+{disp}]", additional_bytes
                else:
                    return f"[{self.registers[base]}+{self.registers[index]}*{1<<scale}+{disp}]", additional_bytes

            else:  # Direccionamiento directo con desplazamiento de 8 bits / Direct addressing with 8-bit displacement
                return f"[{self.registers[rm]}+{disp}]", additional_bytes

        elif mod == 2:  # Desplazamiento de 32 bits / 32-bit displacement
            disp = int.from_bytes(bytes_data[offset:offset+4], byteorder='little', signed=True)
            additional_bytes = 4

            if rm == 4:  # Byte SIB con desplazamiento de 32 bits / SIB byte with 32-bit displacement
                sib = bytes_data[offset]
                scale, index, base = self.parse_sib(sib, rex)
                additional_bytes = 5  # Byte SIB + desplazamiento de 32 bits / SIB byte + 32-bit displacement

                if index == 4:  # Sin índice / No index
                    return f"[{self.registers[base]}+{disp:#x}]", additional_bytes
                else:
                    return f"[{self.registers[base]}+{self.registers[index]}*{1<<scale}+{disp:#x}]", additional_bytes

            else:  # Direccionamiento directo con desplazamiento de 32 bits / Direct addressing with 32-bit displacement
                return f"[{self.registers[rm]}+{disp:#x}]", additional_bytes

        elif mod == 3:  # Registro directo / Direct register
            return self.registers[rm], additional_bytes

        # Si no se reconoce el caso / If the case is not recognized
        return f"[unknown-{mod}-{rm}]", additional_bytes

    def disassemble(self, bytes_data, file_offset, vaddr, size, entry_point):
        """
        Main disassembler for x86-64 code.

        This function disassembles raw machine code into human-readable assembly instructions.
        It handles various instruction types, including XOR, PUSH/POP, MOV, immediate loads,
        and system calls. Additionally, it processes REX prefixes and supports RIP-relative addressing.

        Parameters:
            bytes_data (bytes): Raw binary data of the code section.
            file_offset (int): File offset of the code section.
            vaddr (int): Virtual address of the code section.
            size (int): Size of the code section in bytes.
            entry_point (int): Entry point of the program.

        License: GPL v3
        """

        results = []
        offset = 0

        # Imprimir información del punto de entrada
        print(f"; Punto de entrada: {entry_point:#x}  ; Entry point")
        print("; bits 64  ; 64-bit mode")
        print("; default rel  ; Use RIP-relative addressing by default")
        print("section .text  ; Text section")
        print("global _start  ; Define entry point label")
        print("")

        if entry_point == vaddr:
            print("_start:  ; Etiqueta de inicio del programa")

        while offset < size:
            current_addr = vaddr + offset
            instr_offset = file_offset + offset
            rex = 0
            rex_w = False

            if entry_point == current_addr:
                print("_start:  ; Etiqueta de inicio del programa")

            # Procesar prefijos / Process prefixes
            while bytes_data[instr_offset] & 0xF0 == 0x40:  # Prefijos REX / REX prefixes
                rex = bytes_data[instr_offset]
                rex_w = (rex & 0x08) != 0  # Bit REX.W (operandos de 64 bits) / REX.W bit (64-bit operand)
                instr_offset += 1
                offset += 1

            opcode = bytes_data[instr_offset]

            # Instrucciones XOR / XOR instructions
            if opcode == 0x31:  # xor r/m32, r32
                modrm = bytes_data[instr_offset + 1]
                mod, reg, rm = self.parse_modrm(modrm, rex)

                if mod == 3:  # Registro a registro / Register to register
                    reg_name = self.registers[reg] if rex_w else self.registers32[reg]
                    rm_name = self.registers[rm] if rex_w else self.registers32[rm]
                    print(f"    xor {rm_name}, {reg_name}")  # Imprimir instrucción XOR
                else:
                    operand, extra = self.get_operand_str(mod, rm, rex, bytes_data[instr_offset+2:], 0)
                    reg_name = self.registers[reg] if rex_w else self.registers32[reg]
                    print(f"    xor {operand}, {reg_name}")  # Imprimir XOR con operando indirecto
                    offset += extra

                offset += 2  # opcode + modrm

            # PUSH/POP instrucciones / PUSH/POP instructions
            elif 0x50 <= opcode <= 0x5F:
                if opcode <= 0x57:  # PUSH
                    reg_num = opcode - 0x50
                    if rex & 0x01:  # Aplicar REX.B / Apply REX.B
                        reg_num |= 8
                    print(f"    push {self.registers[reg_num]}")  # Imprimir instrucción PUSH
                else:  # POP
                    reg_num = opcode - 0x58
                    if rex & 0x01:  # Aplicar REX.B / Apply REX.B
                        reg_num |= 8
                    print(f"    pop {self.registers[reg_num]}")  # Imprimir instrucción POP
                offset += 1  # solo opcode

            # MOV instrucciones / MOV instructions
            elif opcode == 0x89:  # mov r/m, r
                modrm = bytes_data[instr_offset + 1]
                mod, reg, rm = self.parse_modrm(modrm, rex)

                if mod == 3:  # Registro a registro / Register to register
                    reg_name = self.registers[reg] if rex_w else self.registers32[reg]
                    rm_name = self.registers[rm] if rex_w else self.registers32[rm]
                    print(f"    mov {rm_name}, {reg_name}")  # Imprimir MOV entre registros
                else:
                    operand, extra = self.get_operand_str(mod, rm, rex, bytes_data[instr_offset+2:], 0)
                    reg_name = self.registers[reg] if rex_w else self.registers32[reg]
                    print(f"    mov {operand}, {reg_name}")  # Imprimir MOV con operando indirecto
                    offset += extra

                offset += 2  # opcode + modrm

            elif opcode == 0x8B:  # mov r, r/m
                modrm = bytes_data[instr_offset + 1]
                mod, reg, rm = self.parse_modrm(modrm, rex)

                if mod == 3:  # Registro a registro / Register to register
                    reg_name = self.registers[reg] if rex_w else self.registers32[reg]
                    rm_name = self.registers[rm] if rex_w else self.registers32[rm]
                    print(f"    mov {reg_name}, {rm_name}")  # Imprimir MOV entre registros
                else:
                    operand, extra = self.get_operand_str(mod, rm, rex, bytes_data[instr_offset+2:], 0)
                    reg_name = self.registers[reg] if rex_w else self.registers32[reg]
                    print(f"    mov {reg_name}, {operand}")  # Imprimir MOV con operando indirecto
                    offset += extra

                offset += 2  # opcode + modrm

            # MOV inmediato a registro / Immediate to register MOV
            elif 0xB8 <= opcode <= 0xBF:  # mov r64, imm64 (con REX.W)
                reg_num = opcode - 0xB8
                if rex & 0x01:  # Aplicar REX.B / Apply REX.B
                    reg_num |= 8

                if rex_w:  # Inmediato de 64 bits / 64-bit immediate
                    imm = int.from_bytes(bytes_data[instr_offset+1:instr_offset+9], byteorder='little')
                    print(f"    mov {self.registers[reg_num]}, {imm:#x}")  # Imprimir MOV con inmediato de 64 bits
                    offset += 9  # opcode + imm64
                else:  # Inmediato de 32 bits / 32-bit immediate
                    imm = int.from_bytes(bytes_data[instr_offset+1:instr_offset+5], byteorder='little')
                    print(f"    mov {self.registers32[reg_num]}, {imm:#x}")  # Imprimir MOV con inmediato de 32 bits
                    offset += 5  # opcode + imm32

            # MOV inmediato a AL/AX/EAX/RAX / Immediate to AL/AX/EAX/RAX MOV
            elif 0xB0 <= opcode <= 0xB7:  # mov r8, imm8
                reg_num = opcode - 0xB0
                if rex & 0x01:  # Aplicar REX.B / Apply REX.B
                    reg_num |= 8
                imm = bytes_data[instr_offset + 1]
                print(f"    mov {self.registers8[reg_num]}, {imm:#x}")  # Imprimir MOV con inmediato de 8 bits
                offset += 2  # opcode + imm8

            # SYSCALL / SYSCALL instruction
            elif opcode == 0x0F and bytes_data[instr_offset + 1] == 0x05:
                syscall_num = None
                for i in range(offset - 5, offset):  # Buscar hacia atrás / Search backwards
                    if i >= 0 and bytes_data[file_offset + i] == 0xB8:  # mov eax, imm32
                        syscall_num = int.from_bytes(bytes_data[file_offset + i + 1:file_offset + i + 5], byteorder='little')
                        break
                    elif i >= 0 and bytes_data[file_offset + i] == 0xB0:  # mov al, imm8
                        syscall_num = bytes_data[file_offset + i + 1]
                        break

                if syscall_num in self.syscalls:
                    print(f"    syscall  ; {self.syscalls[syscall_num]}")  # Imprimir SYSCALL con descripción
                else:
                    print("    syscall")  # Imprimir SYSCALL sin descripción
                offset += 2  # 0x0F + 0x05

            # MOV con inmediato a memoria/registro / Immediate to memory/register MOV
            elif opcode == 0xC7:  # mov r/m32, imm32
                modrm = bytes_data[instr_offset + 1]
                mod, reg, rm = self.parse_modrm(modrm, rex)

                if mod == 3:  # Dirección directa / Direct addressing
                    reg_name = self.registers[rm] if rex_w else self.registers32[rm]
                    imm = int.from_bytes(bytes_data[instr_offset+2:instr_offset+6], byteorder='little')
                    print(f"    mov {reg_name}, {imm:#x}")  # Imprimir MOV con inmediato
                    offset += 6  # opcode + modrm + imm32
                else:
                    operand, extra = self.get_operand_str(mod, rm, rex, bytes_data[instr_offset+2:], 0)
                    imm = int.from_bytes(bytes_data[instr_offset+2+extra:instr_offset+6+extra], byteorder='little')
                    print(f"    mov {operand}, {imm:#x}")  # Imprimir MOV con operando indirecto
                    offset += 6 + extra  # opcode + modrm + extra + imm32

            else:
                # Intentar interpretar datos significativos / Try to interpret meaningful data
                if offset + 8 <= size:
                    qword = int.from_bytes(bytes_data[instr_offset:instr_offset+8], byteorder='little')
                    ascii_bytes = bytes_data[instr_offset:instr_offset+8]
                    if all(32 <= b <= 126 or b == 0 for b in ascii_bytes):
                        ascii_repr = ''.join(chr(b) if 32 <= b <= 126 else '.' for b in ascii_bytes)
                        print(f"    dq {qword:#x}  ; '{ascii_repr}'")  # Imprimir QWORD como ASCII
                    else:
                        print(f"    db {opcode:#x}  ; Opcode desconocido")  # Imprimir byte desconocido
                else:
                    print(f"    db {opcode:#x}  ; Opcode desconocido")  # Imprimir byte desconocido
                offset += 1

def main():
    """
    Main function for the disassembler.

    This function handles command-line arguments, reads the binary file,
    and initiates the disassembly process for an ELF file.

    Usage: python3 disassembler.py <binary_file>
    """

    # Verificar el número correcto de argumentos / Check for the correct number of arguments
    if len(sys.argv) != 2:
        print("Uso: python3 disassembler.py <archivo_binario>  ; Usage: python3 disassembler.py <binary_file>")
        sys.exit(1)

    filename = sys.argv[1]

    try:
        # Abrir y leer el archivo binario / Open and read the binary file
        with open(filename, "rb") as f:
            bytes_data = f.read()

            # Crear una instancia del desensamblador y leer la cabecera ELF / Create a disassembler instance and read the ELF header
            disasm = X64Disassembler()
            file_offset, vaddr, size, entry_point = disasm.read_elf_header(bytes_data)

            # Verificar si se encontró la sección de código / Check if the code section was found
            if file_offset is None:
                print("Error: No se encontró la sección de código en el archivo ELF.  ; Error: Code section not found in ELF file.")
                sys.exit(1)

            # Iniciar el proceso de desensamblado / Start the disassembly process
            disasm.disassemble(bytes_data, file_offset, vaddr, size, entry_point)

    except FileNotFoundError:
        # Manejar errores si el archivo no existe / Handle errors if the file does not exist
        print(f"Error: Archivo '{filename}' no encontrado.  ; Error: File '{filename}' not found.")
        sys.exit(1)

if __name__ == "__main__":
    """
    Entry point of the script.

    This block ensures that the main function is executed only when the script is run directly,
    not when imported as a module.
    """

    # Punto de entrada del script / Script entry point
    # Asegurarse de que main() se ejecute solo si el script se ejecuta directamente / Ensure main() runs only if the script is executed directly
    main()