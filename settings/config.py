import torch


class Config:
    device: torch.device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
    segmented_video_output: str = "generated/segmented_video.mp4"
    models_dir: str = "models"
    model_checkpoints = {
        "fpn_r50": "1g-WDCOwKyNg7KeQIkzPm9UrBHm-jF_6k",  # default
        "mask2former_r50": "1NN5LCozvQtiGRAUrkMf7VgVEiLXwUV7m",
        "mask2former_swin-b": "1hg1bnemgPoX3GF5hsO08lOa4C1uTz_yJ",
    }
