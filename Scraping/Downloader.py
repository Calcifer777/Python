import requests
from stem import Signal
from stem.control import Controller
import time
import random
from fake_useragent import UserAgent
from datetime import datetime
import urllib3


class Throttle:
    """
    Adds a delay between downloads to the same domain
    """
    def __init__(self, delay_param):
        # amount of delay between downloads for each domain
        self.delay = delay_param
        # timestamp of when a domain was last accessed
        self.domains = {}

    def wait(self, url):
        domain = urllib3.util.parse_url(url).host
        if domain in self.domains.keys():
            last_accessed = self.domains.get(domain)
            if self.delay > 0:
                sleep_secs = self.delay - (datetime.now() - last_accessed).seconds
                if sleep_secs > 0:
                    # domain has been accessed recently
                    # so need to sleep
                    time.sleep(sleep_secs)
        # update the last accessed time
        self.domains[domain] = datetime.now()


class TorDownloader:
    """
    Gestisce la sessione di download ad un sito tramite Tor
    """
    def __init__(self, tor_password, headers=None, delay=5, cookies=None):
        self.tor_password = tor_password
        self.user_agent = UserAgent()
        self.headers = headers
        self.cookies = cookies
        self.throttler = Throttle(delay)
        self.session = None
        self.renew_connection()
        self.num_requests = 0

    def renew_connection(self):
        """ Restart sessione Tor con nuovo ip """
        with Controller.from_port(port=9051) as controller:
            controller.authenticate(password = self.tor_password)
            controller.signal(Signal.NEWNYM)
        self.session = self.create_session()

    def create_session(self):
        random.seed()
        session = requests.session()
        # Tor usa la porta 9050 come porta socks5 di default
        session.proxies = {'http': 'socks5://127.0.0.1:9050',
                           'https': 'socks5://127.0.0.1:9050'}
        session.headers['user-agent'] = self.user_agent.random
        # Aggiorna gli header di default con quelli in input
        session.headers.update(self.headers or {})
        session.cookies.update(self.cookies or {})
        return session

    def __call__(self, url, retries=3, headers={}):
        while (retries > 0):
            if self.num_requests > 250:
                self.renew_connection()
            self.throttler.wait(url)
            self.num_requests += 1
            try:
                request = self.session.get(url)
                html = request.content
                code = request.status_code
            except requests.exceptions.Timeout as e:
                print("Timeout")
            except requests.exceptions.ConnectionError as e:
                print("ConnectionError")

            if (request.status_code == 200):
                break
            elif (500 <= request.status_code <= 600):
                print("Server occupato")
            elif (request.status_code == 429):
                print("Troppe richieste (429)")
                time.sleep(300)
            elif (request.status_code == 403):
                print("Accesso negato (403)")
            else:
                pass
            retries -= 1
        return {'html': html, 'code': code}
