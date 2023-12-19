import os

<<<<<<< HEAD:utils/help.py

def prepare_enviroment(yaml_file: str = "requirements.yaml", txt_file: str = "requirements.txt") -> None:
    os.system(f"micromamba env export --from-history > {yaml_file}")
    os.system(f"pipreqs . --force --savepath {txt_file}")
=======
import gdown
import yaml

from settings.config import Config


def prepare_enviroment_configuration(yaml_file: str = "requirements.yaml", txt_file: str = "requirements.txt") -> None:
    os.system(f"micromamba env export > {yaml_file}")
    os.system(f"micromamba env export --from-history > temp_{yaml_file}")
    with open(yaml_file) as yf:
        config = yaml.load(yf, Loader=yaml.FullLoader)
    with open(f"temp_{yaml_file}") as yf:
        hist_config = yaml.load(yf, Loader=yaml.FullLoader)
    config["dependencies"] = [dep for dep in config["dependencies"] if dep.split("=")[0] in hist_config["dependencies"]]
    with open(yaml_file, "w") as yf:
        yaml.dump(config, yf)
    os.remove(f"temp_{yaml_file}")

    os.system(f"pipreqs . --force --savepath {txt_file}")


def download_model_checkpoints() -> None:
    for model_filepath, model_url in Config.model_checkpoints.items():
        model_filepath = os.path.join(Config.models_dir, f"{model_filepath}.pth")
        gdown.download(id=model_url, output=model_filepath, quiet=False)
>>>>>>> 10013a2 (added model selection, update ci/cd pipeline, autodownload models from gdrive):utils/setups.py
