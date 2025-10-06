# vulnerable_popen.py
import subprocess

def show_file():
    fname = input("Enter filename to show: ")
    # BAD: shell=True + direct user input -> command injection
    cmd = f"cat {fname}"
    print(f"[DEBUG] running: {cmd}")
    p = subprocess.Popen(cmd, shell=True)
    p.communicate()

if __name__ == "__main__":
    show_file()
