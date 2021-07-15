import subprocess
import os
import re

if __name__ == '__main__':
    deps = {}
    os.chdir("../../socialNetwork/src")
    for line in subprocess.run(["grep", "-r", "-I", "ThriftClient<.*ServiceClient>"], stdout=subprocess.PIPE).stdout.decode('utf-8').splitlines():
        line = line.replace("::", "?")
        [f, t] = line.split(':')
        f = f.strip()
        t = t.strip()

        [f, _] = f.split('/')
        if not f.endswith("Service"):
            raise Exception()

        [t] = re.findall("ThriftClient<(.*)Client>", t)
        if not t.endswith("Service"):
            raise Exception()

        if f not in deps:
            deps[f] = set()

        deps[f].add(t)

    #print(deps)

    print("digraph us_socialNetwork {")
    print("label=\"\\lDependencies between microservices in socialNetwork application\\lAn edge means source calls at leas one function in destination\"\n")
    printed_nodes = set()
    for f, ts in deps.items():
        for t in ts:
            if not f in printed_nodes:
                print(("\t%s [label=\"%s\"];" % (f, f)))
                printed_nodes.add(f)
            if not t in printed_nodes:
                print(("\t%s [label=\"%s\"];" % (t, t)))
                printed_nodes.add(t)

            print(("\t%s -> %s;" % (f, t)))

    for line in subprocess.run(["find", ".", "-type", "d"], stdout=subprocess.PIPE).stdout.decode('utf-8').splitlines():
        us = line.replace(".", "").replace("/","").strip()
        if not us:
            continue
        if not us in printed_nodes:
            print(("\t%s [label=\"%s\"];" % (us, us)))
    print("}")
