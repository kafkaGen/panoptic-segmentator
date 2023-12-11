import os


def prepare_enviroment(yaml_file: str = "requirements.yaml", txt_file: str = "requirements.txt") -> None:
    os.system(f"micromamba env export --from-history > {yaml_file}")
    os.system(f"pipreqs . --force --savepath {txt_file}")
