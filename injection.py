import pymem
import pymem.process
import os
import ctypes
import configparser
import pymem.ressources.kernel32
import pymem.ressources.psapi
import pymem.ressources.structure

def find_process_id_by_name(process_name):
    try:
        process = pymem.process.process_from_name(process_name)
        if process is None:
            return None
        return process.th32ProcessID
    except pymem.exception.ProcessNotFound:
        return None

def get_module_base_address(process_id, module_name):
    pm = pymem.Pymem()
    pm.open_process_from_id(process_id)

    module = pymem.process.module_from_name(pm.process_handle, module_name)
    pm.close_process()

    if not module:
        return None

    return module.lpBaseOfDll

def dll_injection(process_name, dll_path):
    pm = pymem.Pymem(process_name)
    handle = pm.process_handle
    filepath = dll_path.encode('utf-8')
    pymem.process.inject_dll(handle, filepath)
    print(f"[+] {dll_path} injection successful")

def unload_dll(handle, filepath):
    dll_name = os.path.basename(filepath).encode('utf-8')

    module_name_wide = ctypes.wstring_at(dll_name)
    module_handle = pymem.ressources.kernel32.GetModuleHandleW(module_name_wide)

    if not module_handle:
        modules = pymem.process.enum_process_module(handle)
        for mod in modules:
            if mod.name.lower() == dll_name.decode('utf-8').lower():
                module_handle = mod.lpBaseOfDll
                break

    if not module_handle:
        raise RuntimeError(f"Module {dll_name} is not loaded in the process")

    print(f"[DEBUG] Module handle: 0x{module_handle:x}")

    free_library_addr = pymem.ressources.kernel32.GetProcAddress(
        pymem.ressources.kernel32.GetModuleHandleW("kernel32"),
        b"FreeLibrary"
    )
    if not free_library_addr:
        raise RuntimeError("Failed to get FreeLibrary address")

    thread_h = pymem.ressources.kernel32.CreateRemoteThread(
        handle, None, 0, free_library_addr, module_handle, 0, None
    )
    pymem.ressources.kernel32.WaitForSingleObject(thread_h, -1)

    pymem.ressources.kernel32.VirtualFreeEx(
        handle, ctypes.c_void_p(module_handle), 0, pymem.ressources.structure.MEMORY_STATE.MEM_RELEASE.value
    )

    return True

def main():
    config = configparser.ConfigParser()
    config.read('setting.ini')
    process_name = config['Settings']['process_name']
    dll_path = os.path.abspath(config['Settings']['dll_path'])

    process_id = find_process_id_by_name(process_name)
    if not process_id:
        print(f"Could not find process {process_name}")
        return

    pm = pymem.Pymem()
    pm.open_process_from_id(process_id)

    try:
        module_base_address = get_module_base_address(process_id, os.path.basename(dll_path))
        if module_base_address:
            print(f"Module {dll_path} is already loaded in the process, attempting to unload")
            unload_dll(pm.process_handle, dll_path)
            print(f"{dll_path} unload successful")
        else:
            print(f"Module {dll_path} is not loaded in the process, attempting to inject")
            dll_injection(process_name, dll_path)
            print(f"{dll_path} injection successful")

    except RuntimeError as e:
        print(f"Operation failed: {e}")

    finally:
        pm.close_process()

if __name__ == "__main__":
    main()
