import os
import hydra
import time
import shutil
from omegaconf import DictConfig
from sites import VirginMediaPage
from dotenv import load_dotenv
from flask import Flask, current_app, jsonify


IMPLICITY_WAIT: int = 15
app = Flask(__name__)

def current_timestamp() -> str:
    return time.strftime('%Y-%m-%d---%H-%M-%S')

def repo_path():
    return os.path.dirname(os.path.dirname(os.path.realpath(__file__)))

def list_files_in_dir(dir):
    files = [f'{dir}/{file}' for file in os.listdir(dir)]
    files.sort(key=lambda x: os.path.getmtime(x))
    return files

@app.route('/virginmedia', methods=['POST'])
def run_script():
    cfg = current_app.config["config"]
    old_list_files = list_files_in_dir(f'{repo_path()}/downloads')

    try:
        site = VirginMediaPage(cfg.captcha_api_key, cfg.virginmedia.login, cfg.virginmedia.password)
        site.run()
        new_list_files = list_files_in_dir(f'{repo_path()}/downloads')

        if old_list_files == new_list_files:
            return 'file wasnt downloaded', 401

        filename = f'{repo_path()}/downloads/virgin_media_invoice_{current_timestamp()}{os.path.splitext(new_list_files[-1])[1]}'
        shutil.move(new_list_files[-1], filename)

        return os.path.basename(filename), 200
    except Exception as e:
        return str(e), 403

@hydra.main(config_path=f'{repo_path()}/conf', config_name='main')
def main(cfg: DictConfig):
    app.config["config"] = cfg
    app.run(host=cfg.server.host, port=cfg.server.port, debug=True)

if __name__ == "__main__":
    load_dotenv()
    main()