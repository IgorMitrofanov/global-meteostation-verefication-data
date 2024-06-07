# /main.py

import threading
from daemon import run_upload_daemon


if __name__ == '__main__':

    upload_daemon_thread = threading.Thread(target=run_upload_daemon, daemon=True)

    upload_daemon_thread.start()
    upload_daemon_thread.join()
