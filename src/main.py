import os
from typing import Final
import hydra
from omegaconf import DictConfig
from sites import VirginMediaPage
from dotenv import load_dotenv
from flask import Flask, current_app, jsonify


IMPLICITY_WAIT: Final[int] = 15
app = Flask(__name__)

@app.route('/virginmedia', methods=['POST'])
def run_script():
    cfg = current_app.config["config"]
    try:
        site = VirginMediaPage(cfg.captcha_api_key, cfg.virginmedia.login, cfg.virginmedia.password)
        site.run()
        return { "status": 200, "message": "invoice was downloaded" }
    except Exception as e:
        return { "status": 403, "message": str(e) }

@hydra.main(config_path=f'{os.path.dirname(os.path.dirname(os.path.realpath(__file__)))}/conf', config_name='main')
def main(cfg: DictConfig):
    app.config["config"] = cfg
    app.run(host=cfg.server.host, port=cfg.server.port, debug=True)

if __name__ == "__main__":
    load_dotenv()
    main()