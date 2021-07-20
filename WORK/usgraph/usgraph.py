import subprocess
import os
import re
import sys

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print(("USAGE: %s <DeathStarBench application name (eg. socialNetwork)>") % sys.argv[0])
        sys.exit(0)
    app_name = sys.argv[1]

    deps = {}
    os.chdir(("../../%s/src" % app_name))
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

    print(("digraph us_%s {") % app_name)
    print(("label=\"\\lDependencies between microservices in %s application\\lAn edge means source calls at leas one function in destination\\lGreen nodes are mongodb instances, red nodes are redis instances, orange nodes are memcached instances\"\n") % app_name)
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

    # redis dependencies
    deps = {}
    for line in subprocess.run(['grep', '-r', '-I', 'init_redis_client_pool'], stdout=subprocess.PIPE).stdout.decode('utf-8').splitlines():
        line = line.replace("::", "?")
        [f, t] = line.split(':')
        f = f.strip()
        t = t.strip()
        if f == "utils_redis.h":
            continue
        [f, _] = f.split('/')
        if not f.endswith("Service"):
            raise Exception()

        [t] = re.findall("init_redis_client_pool\(.+,\s*(.*)\)", t)
        if not t.startswith('"') or not t.endswith('"'):
            raise Exception(line)
        t = t[1:-1] + "-redis"
        if f not in deps:
            deps[f] = set()
        deps[f].add(t)

    for f, ts in deps.items():
        for t in ts:
            if not f in printed_nodes:
                print(("\t%s [label=\"%s\"];" % (f, f)))
                printed_nodes.add(f)
            if not t in printed_nodes:
                print(("\t\"%s\" [label=\"%s\",color=red];" % (t, t)))
                printed_nodes.add(t)
            print(("\t%s -> \"%s\";" % (f, t)))


    # mongo
    deps = {}
    for line in subprocess.run(['grep', '-r', '-I', 'init_mongodb_client_pool'], stdout=subprocess.PIPE).stdout.decode('utf-8').splitlines():
        line = line.replace("::", "?")
        [f, t] = line.split(':')
        f = f.strip()
        t = t.strip()
        if f == "utils_mongodb.h":
            continue
        [f, _] = f.split('/')
        if not f.endswith("Service"):
            if f == "PostStorageSerivce":
                f = "PostStorageService"
                continue
            raise Exception(f+"\n"+t+"\n"+line)

        [t] = re.findall("init_mongodb_client_pool\(.+,\s*(.*)\s*,.*\)", t)
        if not t.startswith('"') or not t.endswith('"'):
            raise Exception(line)
        t = t[1:-1] + "-mongodb"
        if f not in deps:
            deps[f] = set()
        deps[f].add(t)

    for f, ts in deps.items():
        for t in ts:
            if not f in printed_nodes:
                print(("\t%s [label=\"%s\"];" % (f, f)))
                printed_nodes.add(f)
            if not t in printed_nodes:
                print(("\t\"%s\" [label=\"%s\",color=green];" % (t, t)))
                printed_nodes.add(t)
            print(("\t%s -> \"%s\";" % (f, t)))

    # memcached
    # hardcoded for now (and only for socialNetwork)
    if app_name == "socialNetwork":
        hardcoded = {'UserMentionService': ['user-memcached'], 'UserService': ['user-memcached'],
                     'PostStorageService': ['post-storage-memcached'],
                     'UrlShortenService' : ['url-shorten-memcached']}
        for f, ts in hardcoded.items():
            for t in ts:
                if not f in printed_nodes:
                    print(("\t%s [label=\"%s\"];" % (f, f)))
                    printed_nodes.add(f)
                if not t in printed_nodes:
                    print(("\t\"%s\" [label=\"%s\",color=orange];" % (t, t)))
                    printed_nodes.add(t)
                print(("\t%s -> \"%s\";" % (f, t)))



    # microservices that haven't appeared yet
    for line in subprocess.run(["find", ".", "-type", "d"], stdout=subprocess.PIPE).stdout.decode('utf-8').splitlines():
        us = line.replace(".", "").replace("/","").strip()
        if not us:
            continue
        if us == "PostStorageSerivce":
            us = "PostStorageService"
        if not us in printed_nodes:
            print(("\t%s [label=\"%s\"];" % (us, us)))
    print("}")
