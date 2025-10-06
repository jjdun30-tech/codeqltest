# vulnerable_cmdi.py
import os

def list_files():
    directory = input("Enter directory to list: ")   # untrusted user input
    # BAD: passing user input directly to a shell command
    cmd = f"ls -la {directory}"
    print(f"[DEBUG] running: {cmd}")
    os.system(cmd)

if __name__ == "__main__":
    list_files()
