from typing import Union

import torch


class Config:
    model_config: str = "models/panoptic_fpn_r50_fpn_mstrain_3x_coco.py"
    model_checkpoint: str = "models/panoptic_fpn_r50_fpn_mstrain_3x_coco_20210824_171155-5650f98b.pth"
    # model_config: str = 'models/mask2former_r50_8xb2-lsj-50e_coco-panoptic.py'
    # model_checkpoint: str = 'models/mask2former_r50_8xb2-lsj-50e_coco-panoptic_20230118_125535-54df384a.pth'
    device: Union[torch.device, str] = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")

    segmented_video_output: str = "generated/segmented_video.mp4"
