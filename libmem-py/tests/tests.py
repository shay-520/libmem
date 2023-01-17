from libmem import *
import ctypes
import struct

def separator():
    print("========================================")

print("[*] libmem-py tests")

separator()

print("[*] Process Enumeration")
print("\n".join([str(proc) for proc in LM_EnumProcesses()[:5]]))

separator()

print("[*] Current Process")
curproc = LM_GetProcess()
print(curproc)

separator()

print("[*] Parent Process of Current Process")
parent_proc = LM_GetProcessEx(curproc.ppid)
print(parent_proc)

separator()

print("[*] Remote Process")
proc = LM_FindProcess("test1")
print(proc)

separator()

print(f"[*] Is Remote Process Alive? {'Yes' if LM_IsProcessAlive(proc) else 'No'}")

separator()

print(f"[*] System Bits: {LM_GetSystemBits()}")

separator()

print(f"[*] Current Process Threads: {LM_EnumThreads()}")

separator()

print(f"[*] Remote Process Threads: {LM_EnumThreadsEx(proc)}")

separator()

thread = LM_GetThread()
print(f"[*] Current Thread: {thread}")

separator()

print(f"[*] Remote Thread: {LM_GetThreadEx(proc)}")

separator()

print(f"[*] Process From Thread '{thread}': {LM_GetThreadProcess(thread)}")

separator()

print("[*] Module Enumeration - Current Process")
print("\n".join([str(mod) for mod in LM_EnumModules()[:5]]))

separator()

print("[*] Module Enumeration - Remote Process")
print("\n".join([str(mod) for mod in LM_EnumModulesEx(proc)[:5]]))

separator()

curmod = LM_FindModule(curproc.path)
print(f"[*] Current Process Module: {curmod}")

separator()

mod = LM_FindModuleEx(proc, proc.path)
print(f"[*] Remote Process Module: {mod}")

separator()

# TODO: Add tests for LM_LoadModule(Ex) and LM_UnloadModule(Ex)

# separator()

print("[*] Symbol Enumeration")

print("\n".join([str(sym) for sym in LM_EnumSymbols(curmod)[:5]]))

separator()

print("[*] Symbol Address Search")

symaddr = LM_FindSymbolAddress(curmod, "Py_BytesMain")
print(f"[*] Py_BytesMain Address: {symaddr}")

separator()

print("[*] Page Enumeration - Current Process")
print("\n".join([str(page) for page in LM_EnumPages()[:5]]))

separator()

print("[*] Page Enumeration - Remote Process")
print("\n".join([str(page) for page in LM_EnumPagesEx(proc)[:5]]))

separator()

print(f"[*] Page From Current Process Module: {LM_GetPage(symaddr)}")

separator()

print(f"[*] Page From Remote Process Module: {LM_GetPageEx(proc, mod.base)}")

separator()

val = ctypes.c_int(10)
val_addr = ctypes.addressof(val)
rdbuf = LM_ReadMemory(val_addr, ctypes.sizeof(val))
rdval = struct.unpack("@i", rdbuf)[0]
print(f"[*] Read Integer From '{hex(val_addr)}': {str(rdval)}")

separator()

# TODO: Add tests for 'LM_ReadMemoryEx'
# separator()

LM_WriteMemory(val_addr, bytearray(b"\x39\x05\x00\x00"))
print(f"[*] Integer After LM_WriteMemory: {val}")

separator()

# TODO: Add tests for 'LM_WriteMemoryEx'
# separator()

LM_SetMemory(val_addr, b"\x00", ctypes.sizeof(val))
print(f"[*] Integer After LM_SetMemory: {val}")

separator()

# TODO: Add tests for 'LM_SetMemoryEx'
# separator()

print("[*] Changing Memory Protection - Current Process")
old_prot = LM_ProtMemory(curmod.base, 0x1000, LM_PROT_XRW)
print(f"[*] Old Memory Protection ({hex(curmod.base)}): {old_prot}")
page = LM_GetPage(curmod.base)
print(f"[*] Current Memory Protection ({hex(curmod.base)}): {page.prot}")
