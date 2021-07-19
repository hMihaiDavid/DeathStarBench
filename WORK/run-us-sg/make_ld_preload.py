import sys
import os
import subprocess

if __name__ == "__main__":
    us_name = sys.argv[1]
    us_binary = "../../socialNetwork/build/src/%s/%s" % (us_name, us_name)
    command = "ldd %s | grep \"not found\"" % us_binary
    lines = subprocess.run([command], shell=True, stdout=subprocess.PIPE).stdout.decode('utf-8').splitlines()

    libs = []

    for line in lines:
        line = line.strip()
        if not line:
            continue
        [libname, _] = line.split(' => ')
        libname = libname.strip()
#        print(libname)
        command = "find lib/ -name \"%s\" -type \"f,l\"" % libname
        [libpath] = subprocess.run([command], shell=True, stdout=subprocess.PIPE).stdout.decode('utf-8').splitlines()
        libpath = libpath.strip()
        libs.append(libpath)
#        print(libpath)

    s = "LD_PRELOAD=\"%s\"" % (':'.join(libs))
    print(s)
