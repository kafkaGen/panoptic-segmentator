import base64
import hashlib
import os
import unittest
from io import BytesIO

import cv2
import numpy as np
import requests
from PIL import Image


def images_batch_processing(
    model_name: str,
    url: str = "http://127.0.0.1:8000",
    input_images_path: str = "test/test_images_raw",
    test_images_path: str = "test/test_images_processed",
) -> bool:
    url = f"{url}/images/?model_name={model_name}"

    file_list, open_files = [], []
    for path in os.listdir(input_images_path):
        file_path = os.path.join(input_images_path, path)
        open_file = open(file_path, "rb")
        if ".jpg" in file_path:
            file_list.append(("images", (path, open_file, "image/jpeg")))
        else:
            file_list.append(("images", (path, open_file, "image/png")))
        open_files.append(open_file)

    response = requests.post(url, files=file_list)
    for fl in open_files:
        fl.close()
    if response.status_code != 200:
        return False

    for test_path, segmented_image_encoded in zip(os.listdir(input_images_path), response.json()["segmented_images_bytes"]):
        test_path = test_path.split(".")[0] + f"_{model_name}.png"
        file_path = os.path.join(test_images_path, test_path)
        test_image = cv2.imread(file_path)
        segmented_image_decoded = base64.b64decode(segmented_image_encoded)
        segmented_image = np.array(Image.open(BytesIO(segmented_image_decoded)))

        if not np.array_equal(test_image, segmented_image):
            return False

    return True


def videos_batch_processing(
    model_name: str,
    url: str = "http://127.0.0.1:8000",
    input_videos_path: str = "test/test_videos_raw",
    test_videos_path: str = "test/test_videos_processed",
) -> bool:
    url = f"{url}/videos/?model_name={model_name}"

    file_list, open_files = [], []
    for path in os.listdir(input_videos_path):
        file_path = os.path.join(input_videos_path, path)
        open_file = open(file_path, "rb")
        if ".mp4" in file_path:
            file_list.append(("videos", (path, open_file, "video/mp4")))
        open_files.append(open_file)

    response = requests.post(url, files=file_list)
    for fl in open_files:
        fl.close()
    if response.status_code != 200:
        return False

    for test_path, segmented_video_encoded in zip(os.listdir(input_videos_path), response.json()["segmented_videos_bytes"]):
        test_path = test_path.split(".")[0] + f"_{model_name}.mp4"
        file_path = os.path.join(test_videos_path, test_path)
        with open(file_path, "rb") as fl:
            test_video = fl.read()
        segmented_video = base64.b64decode(segmented_video_encoded)

        if hashlib.sha512(test_video).hexdigest() != hashlib.sha512(segmented_video).hexdigest():
            return False

    return True


class APITest(unittest.TestCase):
    def test_images_segmentation(self) -> None:
        self.assertEqual(images_batch_processing(model_name="fpn_r50"), True)
        self.assertEqual(images_batch_processing(model_name="mask2former_r50"), True)
        self.assertEqual(images_batch_processing(model_name="mask2former_swin-b"), True)

    def test_videos_segmentation(self) -> None:
        self.assertEqual(videos_batch_processing(model_name="fpn_r50"), True)
        self.assertEqual(videos_batch_processing(model_name="mask2former_r50"), True)
        self.assertEqual(videos_batch_processing(model_name="mask2former_swin-b"), True)


if __name__ == "__main__":
    unittest.main()
