import argparse

from utils.setups import download_model_checkpoints, prepare_enviroment_configuration

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-e", "--set-env", action="store_true", help="rebuild requirements.yaml and requirements.txt")
    parser.add_argument("-d", "--download-models", action="store_true", help="download model checkpoints")
    arguments = parser.parse_args()

    if arguments.set_env:
        prepare_enviroment_configuration()
    if arguments.download_models:
        download_model_checkpoints()
