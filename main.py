# /main.py

import threading
from daemon import run_upload_daemon
from dashboard.app import run_dashboard_app


if __name__ == '__main__':
    dashboard_thread = threading.Thread(target=run_dashboard_app, daemon=True)
    upload_daemon_thread = threading.Thread(target=run_upload_daemon, daemon=True)

    dashboard_thread.start()
    upload_daemon_thread.start()

    dashboard_thread.join()