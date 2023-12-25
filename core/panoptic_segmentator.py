import random
from typing import Union

import cv2
import numpy as np
import torch
from mmdet.apis import DetInferencer

from settings import Config  # type: ignore[attr-defined]


class PanopticSegmentator:
    def __init__(self, model_name: str, device: str = Config.device) -> None:
        self.set_random_seed()
        model_config = f"{Config.models_dir}/{model_name}.py"
        model_checkpoint = f"{Config.models_dir}/{model_name}.pth"
        self.inferencer = DetInferencer(model=model_config, weights=model_checkpoint, device=device)

    def __call__(self, imgs: Union[np.array, list[np.array]]) -> list[np.array]:
        if not isinstance(imgs, list):
            imgs = [np.array(imgs)]
        imgs = [cv2.cvtColor(img, cv2.COLOR_RGB2BGR) for img in imgs]
        segmented_imgs = self.inferencer(imgs, return_vis=True)["visualization"]
        return segmented_imgs  # type: ignore[no-any-return]

    @staticmethod
    def set_random_seed(seed: int = Config.random_seed, deterministic: bool = True) -> None:
        random.seed(seed)
        np.random.seed(seed)
        torch.manual_seed(seed)
        torch.cuda.manual_seed_all(seed)
        if deterministic:
            torch.backends.cudnn.deterministic = True
            torch.backends.cudnn.benchmark = False
