# DLL Injection Tool

This is a Python-based tool for injecting and unloading DLLs into a specified process. It utilizes the `pymem` library to interact with processes and perform the necessary operations.

This tool is useful for injecting/unloading the Dumper-7 SDK.

## Features

- Find process ID by name
- Get base address of a module in a process
- Inject DLL into a process
- Unload DLL from a process
- Configuration via `setting.ini` file

## Requirements

- Python 3.x
- `pymem` library
- `configparser` library

## Installation

1. Clone the repository:

    ```sh
    git clone https://github.com/your-username/your-repo-name.git
    cd your-repo-name
    ```

2. Install the required Python packages:

    ```sh
    pip install -r requirements.txt
    ```

## Configuration

Create a `setting.ini` file in the root directory of the project with the following structure:

    ```ini
    [Settings]
    process_name = YourProcessName.exe
    dll_path = C:\\path\\to\\your\\dll.dll
    ```

Replace `YourProcessName.exe` with the name of the process you want to inject the DLL into, and `C:\\path\\to\\your\\dll.dll` with the full path to your DLL.

## Usage

Run the script:

    ```sh
    python injection.py
    ```

The script will read the process name and DLL path from the `setting.ini` file, find the process, and inject or unload the DLL as necessary.

## Example

1. Ensure the process you want to inject the DLL into is running.
2. Create and configure the `setting.ini` file.
3. Run the script:

    ```sh
    python injection.py
    ```

The script will output messages indicating whether the DLL was successfully injected or unloaded.

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.
