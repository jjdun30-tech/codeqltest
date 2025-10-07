# cmd_and_path_vulns.py
# Intentional command / path / eval vulnerabilities for testing.

import subprocess
import os
import shutil

def cmd_injection_subprocess():
    # tainted CLI param
    user_arg = input("archive target> ")                          # taint source
    # BAD: passing a constructed command to shell=True
    cmd = "tar -czf /tmp/backup.tgz " + user_arg                  # <-- CMDi #1
    subprocess.run(cmd, shell=True)                               # sink

def os_system_concat():
    path = input("file> ")                                        # taint source
    # BAD: os.system with unsanitized argument
    os.system("cat " + path)                                      # <-- CMDi #2

def path_traversal_delete():
    # path traversal: delete a file under uploads based on untrusted filename
    filename = input("filename> ")                                # taint source
    uploads = "/var/www/uploads/"
    target = os.path.join(uploads, filename)                      # attacker could supply ../../etc/passwd
    # BAD: directly deleting constructed path
    if os.path.exists(target):
        os.remove(target)                                         # sink: destructive file operation (path traversal)

def insecure_eval():
    # insecure eval of user data (code injection)
    payload = input("expr> ")                                      # taint source
    result = eval(payload)                                         # <-- code-injection sink
    return result
