# -*- coding: UTF-8 -*-

import json
import os
import yaml

import subprocess
import re

def config_thrift(tls):
    if tls:
        f = open('config/service-config.json')
        content = f.read()
        j = json.loads(content)

        j['ssl']['enabled'] = True

        f.close()
        f = open('config/service-config.json', 'w')
        f.write(json.dumps(j, indent=2))
        f.close()
    else:
        f = open('config/service-config.json')
        content = f.read()
        j = json.loads(content)

        j['ssl']['enabled'] = False

        f.close()
        f = open('config/service-config.json', 'w')
        f.write(json.dumps(j, indent=2))
        f.close()

def config_mongod(tls, config_filename, port):
    f = open('config/'+config_filename)
    content = f.read()
    y = yaml.load(content)

    y['net']['port'] = port
    # XXX: Maybe we'll have to change the TLS port but we don't deal with TLS yet
    if tls:
        y['net']['tls']['mode'] = 'requireTLS'
        y['net']['tls']['certificateKeyFile'] = '/keys/server.pem'
    else:
        y['net']['tls']['mode'] = 'disabled'
        try:
            del y['net']['tls']['certificateKeyFile']
        except:
            pass

    f.close()
    f = open('config/'+config_filename, 'w')
    f.write(yaml.dump(y, default_flow_style=False))
    f.close()

def config_redis(tls, config_filename, port):
    f = open('config/'+config_filename)
    content = f.read()

    if tls:
        content = re.sub(r'port [0-9]+', "port 0", content)
        content = re.sub(r'tls-port [0-9]+', ("port %d" % port), content)
        #content = content.replace('port 6379', 'port 0')
        #content = content.replace('tls-port 0', ('tls-port %d' % port))
    else:
        content = re.sub(r'port [0-9]+', ("port %d" % port), content)
        content = re.sub(r'tls-port [0-9]+', "port 0", content)
        #content = content.replace('port 0', ('port %d' % port))
        #content = content.replace('tls-port 6379', 'tls-port 0')

    f.close()
    f = open('config/'+config_filename, 'w')
    f.write(content)
    f.close()

def config_services():
    f = open('config/service-config.json')
    content = f.read()
    j = json.loads(content)

    j['user-service']['port'] = 2000
    j['user-mongodb']['port'] = 2001
    j['social-graph-service']['port'] = 3000
    j['social-graph-mongodb']['port'] = 3001
    j['social-graph-redis']['port'] = 3002

    for k in j:
        if k.endswith("-service") or k.endswith("-mongodb") or k.endswith("-redis"):
            if 'addr' in j[k]:
                j[k]['addr'] = 'localhost'


    f.close()
    f = open('config/service-config.json', 'w')
    f.write(json.dumps(j, indent=2))
    f.close()

def config_disable_jaeger_tracing():
    f = open('config/jaeger-config.yml')
    content = f.read()
    y = yaml.load(content)

    y['disabled'] = True

    f.close()
    f = open('config/jaeger-config.yml', 'w')
    f.write(yaml.dump(y, default_flow_style=False))
    f.close()


tls = False # the original default was True
tls_str = os.environ.get('TLS', '0').lower()
if tls_str == '1' or tls_str == 'true':
    tls = True

subprocess.run(["rm", "-rf", "config"])
subprocess.run(["cp", "-R", "../../socialNetwork/config/", "."])
subprocess.run(["cp", "config/mongod.conf", "config/mongod_user-service.conf"])
subprocess.run(["mv", "config/mongod.conf", "config/mongod_social-graph-service.conf"])
subprocess.run(["mv", "config/redis.conf", "config/redis_social-graph-service.conf"])

config_thrift(tls)
config_mongod(tls, "mongod_user-service.conf", 2001)
config_mongod(tls, "mongod_social-graph-service.conf", 3001)
config_redis(tls, "redis_social-graph-service.conf", 3002)

config_services()
config_disable_jaeger_tracing()
