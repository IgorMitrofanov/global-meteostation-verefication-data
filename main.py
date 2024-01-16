# /main.py

import threading
from daemon import upload_daemon


def start_upload_daemon():
    scrape_thread = threading.Thread(target=upload_daemon, daemon=True)
    scrape_thread.start()
    scrape_thread.join() # wait for the thread finished


if __name__ == '__main__':
    start_upload_daemon()