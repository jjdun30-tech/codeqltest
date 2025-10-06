# vulnerable_format_exec.py
import os

def ping_host():
    host = input("Enter host to ping: ")
    # BAD: concatenated string fed to os.system
    cmd = "ping -c 1 " + host
    print(f"[DEBUG] running: {cmd}")
    os.system(cmd)

if __name__ == "__main__":
    ping_host()
