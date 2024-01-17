#! /Users/moisha/miniconda3/bin/python3
import os
import sys
import libtmux
import secrets
from tqdm import tqdm


def start(num, path):
    global server
    if server is None:
        server = libtmux.Server().new_session()
    log = ''
    for i in tqdm(range(0, num)):
        if i != 0:
            server.new_window()
        os.makedirs(path + '/dir' + str(i), exist_ok=True)
        token = secrets.token_urlsafe(47)
        server.windows[i].select_pane(target_pane=0).send_keys(f"jupyter notebook "
                                                               f"--ip 127.0.0.1 --port {10000 + i} "
                                                               f"--no-browser "
                                                               f"--NotebookApp.token={token} "
                                                               f"--NotebookApp.notebook_dir={path + '/dir'+ str(i)}")
        log += f'Сессия с id {i} запущена на порту {10000 + i} с токеном {token}\n'
    print(log)


def stop(session_id):
    os.rmdir("dir" + str(session_id))
    if session_id < len(libtmux.Server().windows):
        window = libtmux.Server().windows[session_id]
        window.kill_window()


def stop_all():
    global server
    for directory in os.listdir():
        if directory.startswith("dir"):
            os.rmdir(directory)

    for window in libtmux.Server().windows:
        window.kill_window()


if __name__ == '__main__':
    input_data = sys.argv
    server = None
    if input_data[1] == 'start':
        number = int(input_data[2])
        start(number, os.getcwd())
    elif input_data[1] == 'stop':
        sess_id = int(input_data[2])
        stop(sess_id)
    elif input_data[1] == 'stop_all':
        stop_all()
