#!/usr/bin/env python3

import argparse
from termcolor import colored
import subprocess
import sys
import signal
from concurrent.futures import ThreadPoolExecutor

def def_handler(sig, frame):
    print(colored(f"\n[!] Saliendo del programa...\n", 'red'))
    sys.exit(1)

signal.signal(signal.SIGINT, def_handler)


def get_arguments():
    parser = argparse.ArgumentParser(description="Herramienta para descubrir hots activos en una red (ICMP)")
    parser.add_argument("-t","--target",required=True, dest="target", help="Hots o rango de red a escanear")

    args = parser.parse_args()

    return args.target

def parse_target(target_str):

    # 192.168.1.1-100
    target_str_splitted = target_str.split('.') # ["192", "168", "1", "1-100"]
    first_three_octets = '.'.join(target_str_splitted[:3]) # 192.168.1

    if len(target_str_splitted) == 4:
        if "-" in target_str_splitted[3]:
            start, end = target_str_splitted[3].split('-')
            return [f"{first_three_octets}.{i}" for i in range(int(start),int(end)+1)]
        else:
            return [target_str]
    else:
        print(colored(f"\n[!] El formato de IP o rango de IP no es válido.\n", 'red'))

def host_discovery(target):

    try:
        ping = subprocess.run(["ping", "-c", "1", target], timeout=1, stdout=subprocess.DEVNULL)
        if ping.returncode == 0:
            print(colored(f"\t[i] La IP {target} está activa", 'green'))
    except subprocess.TimeoutExpired:
        pass

def main():

    target_str = get_arguments()
    targets = parse_target(target_str)

    print(f"\n[+] Hots activos en la red: \n")

    max_threads = 140
    with ThreadPoolExecutor(max_workers=max_threads) as executor:
        executor.map(host_discovery,targets)
    
if __name__ == '__main__':
    main()
