from typing import Optional, Tuple, List
import os
import glob
from pathlib import Path
import logging
from PIL import Image
import pandas as pd
import numpy as np
import concurrent.futures
from concurrent.futures import ProcessPoolExecutor


logger = logging.getLogger(__name__)


class OidImage(object):
    needed_columns = ["ImageID", "ImagePath", "Width", "Height"]

    def __init__(self, ds_type: int, images_dir: str):
        self.ds_type: int = ds_type
        self.images_dir: str = images_dir
        self.df = pd.DataFrame(index=[], columns=OidImage.needed_columns)

    @classmethod
    def get_resolution(cls, image_path: str) -> Tuple[int, int]:
        try:
            if not Path.is_file(Path(image_path)):
                raise ValueError(f'image_path is invalid')
            with Image.open(image_path) as image:
                width = image.size[0]
                height = image.size[1]
                return width, height

        except Exception as e:
            logger.error(f'action=get_resolution error={e}')
            raise

    @staticmethod
    def get_oid_image_list(dir_path: str, image_id_list: List) -> Optional[pd.DataFrame]:
        """create OidImage from the images directory path and the image ID"""
        df = pd.DataFrame(index=[], columns=OidImage.needed_columns)
        for image_id in image_id_list:
            image_path_list = glob.glob(f'{dir_path}/{image_id}.*')
            if not image_path_list:
                logger.warning(f'{dir_path}/{image_id}.* not found')
                continue
            image_path = image_path_list[0]
            width, height = OidImage.get_resolution(image_path)
            row = {"ImageID": image_id, "ImagePath": image_path, "Width": width, "Height": height}
            df = df.append(row, ignore_index=True)
        return df

    def build_images(self, image_id_list: np.ndarray) -> None:
        try:
            futures = []
            with ProcessPoolExecutor(max_workers=os.cpu_count()) as executor:
                for image_id_chunk in np.array_split(image_id_list, os.cpu_count()):
                    future = executor.submit(self.get_oid_image_list, self.images_dir, image_id_chunk)
                    futures.append(future)

            concurrent.futures.wait(futures, timeout=None)
            for future in concurrent.futures.as_completed(futures):
                self.df = pd.concat([self.df, future.result()])
            self.df.reset_index(drop=True, inplace=True)

        except Exception as e:
            logger.error(f'action=build_images error={e}')
            raise

    def resolution(self, image_id: str) -> Tuple[int, int]:
        try:
            if len(self.df) == 0:
                raise ValueError(f'not be called build_images() yet')
            row = self.df[self.df["ImageID"] == image_id]
            width_list = row["Width"].values.tolist()
            height_list = row["Height"].values.tolist()
            return width_list[0], height_list[0]
        except Exception as e:
            logger.error(f'action=resolution error={e}')
            raise
