import os
from typing import Final
import hydra
from omegaconf import DictConfig
from sites import VirginMediaPage
from dotenv import load_dotenv

IMPLICITY_WAIT: Final[int] = 30

@hydra.main(config_path=f'{os.path.dirname(os.path.dirname(os.path.realpath(__file__)))}/conf', config_name='main')
def main(cfg: DictConfig):
    if cfg.site.class_name == 'VirginMediaPage':
        site = VirginMediaPage(cfg.captcha_api_key, cfg.site.login, cfg.site.password)
    site.run()

if __name__ == "__main__":
    load_dotenv()
    main()