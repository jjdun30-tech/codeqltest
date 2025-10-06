# vulnerable_getoutput.py
import subprocess

def who_is_on_line():
    user = input("Enter username to grep in utmp: ")
    # BAD: getoutput runs through shell
    out = subprocess.getoutput(f"who | grep {user}")
    print(out)

if __name__ == "__main__":
    who_is_on_line()
