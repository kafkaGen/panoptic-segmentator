from typing import Union

import cv2
import numpy as np
from mmdet.apis import DetInferencer

from settings import Config  # type: ignore[attr-defined]


class PanopticSegmentator:
    def __init__(
        self, model_config: str = Config.model_config, model_checkpoint: str = Config.model_checkpoint, device: str = Config.device
    ) -> None:
        self.model_config = model_config
        self.model_checkpoint = model_checkpoint
        self.device = device

    def __call__(self, imgs: Union[np.array, list[np.array]]) -> list[np.array]:
        if not isinstance(imgs, list):
            imgs = [np.array(imgs)]
        imgs = [cv2.cvtColor(img, cv2.COLOR_RGB2BGR) for img in imgs]
        inferencer = DetInferencer(model=self.model_config, weights=self.model_checkpoint, device=self.device)
        segmented_imgs = inferencer(imgs, return_vis=True)["visualization"]
        return segmented_imgs  # type: ignore[no-any-return]
