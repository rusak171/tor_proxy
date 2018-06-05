#!/usr/bin/python3
# -*- coding: utf-8 -*-
from stem import Signal
from stem.control import Controller
import asyncio
import os
import subprocess
import json


async def new_identity():
    tor_control = '/var/run/tor/control'
    host = '127.0.0.1'
    port = 9050
    while True:
        try:
            if not os.path.exists(tor_control):
                print('Tor control file does not exists ({}). Try to restart.'.format(tor_control))
                cmd = 'service tor restart'
                subprocess.Popen(cmd, shell=True)
            with Controller.from_socket_file(path=tor_control) as controller:
                # send signal to change tor-identity
                controller.authenticate()
                controller.signal(Signal.NEWNYM)
                # get and print new tor identity
                pipe = subprocess.PIPE
                cmd = 'curl --proxy socks5h://{}:{} https://check.torproject.org/api/ip'\
                    .format(host, port)
                p = subprocess.Popen(cmd, shell=True, stdout=pipe, stderr=pipe)
                res = p.stdout.read().decode('utf-8')
                d = json.loads(res)
                res_ip = d.get('IP')
                print(res_ip)
        except json.decoder.JSONDecodeError as err:
            print(repr(err))
            return
        except Exception as err:
            print(repr(err))
            return
        finally:
            await asyncio.sleep(60)


if __name__ == '__main__':
    print('CHANGE TORIDENTITY STARTED...')
    loop = asyncio.get_event_loop()
    fut = asyncio.gather(new_identity())
    loop.run_until_complete(fut)
    loop.close()
