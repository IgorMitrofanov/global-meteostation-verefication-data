# /main.py

import threading
from scraper.run_daemon import run_upload_daemon, run_uploader
from dashboard.app import run_dashboard_app


if __name__ == '__main__':

    

    upload_daemon_thread = threading.Thread(target=run_upload_daemon, daemon=True)
    dashboard_app_thread = threading.Thread(target=run_dashboard_app, daemon=True)

    upload_daemon_thread.start()
    dashboard_app_thread.start()
    upload_daemon_thread.join()
    dashboard_app_thread.join()
