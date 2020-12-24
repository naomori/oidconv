from typing import Optional, Tuple, List, Dict
import os
import glob
from pathlib import Path
import logging
from PIL import Image
import numpy as np
import concurrent.futures
from concurrent.futures import ProcessPoolExecutor


logger = logging.getLogger(__name__)


class OidImage(object):
    def __init__(self):
        self.id: str = ""
        self.image_path: str = ""
        self.width: int = 0
        self.height: int = 0

    def set(self, image_id: str, image_path: str):
        try:
            if not Path.is_file(Path(image_path)):
                raise ValueError(f'image_path is invalid')
            self.image_path = image_path
            self.id = image_id

        except Exception as e:
            logger.error(f'action=set error={e}')
            raise

    def get_resolution(self) -> Tuple[int, int]:
        """return (width, height)"""
        with Image.open(self.image_path) as image:
            self.width = image.size[0]
            self.height = image.size[1]
        return self.width, self.height

    def get_filename(self):
        return os.path.basename(self.image_path)

    def display(self):
        print(f"id:{self.id}, path:{self.image_path}, width:{self.width}, height:{self.height}")


class OidImages(object):
    def __init__(self, ds_type: int, images_dir: str):
        self.ds_type: int = ds_type
        self.images_dir: str = images_dir
        self.images: Dict[str, OidImage] = dict()

    @staticmethod
    def _get_oid_image_list(dir_path: str, image_id_list: List) -> Optional[Dict[str, OidImage]]:
        """create OidImage from the images directory path and the image ID"""
        oid_images = dict()
        for image_id in image_id_list:
            image_path_list = glob.glob(f'{dir_path}/{image_id}.*')
            if not image_path_list:
                logger.warning(f'{dir_path}/{image_id}.* not found')
                continue
            oid_image = OidImage()
            image_path = image_path_list[0]
            oid_image.set(image_id, image_path)
            oid_image.get_resolution()
            oid_images[image_id] = oid_image

        return oid_images

    def build_images(self, image_id_list: np.ndarray) -> None:
        try:
            futures = []
            with ProcessPoolExecutor(max_workers=os.cpu_count()) as executor:
                for image_id_chunk in np.array_split(image_id_list, os.cpu_count()):
                    future = executor.submit(self._get_oid_image_list, self.images_dir, image_id_chunk)
                    futures.append(future)

            concurrent.futures.wait(futures, timeout=None)
            for future in concurrent.futures.as_completed(futures):
                self.images.update(future.result())

        except Exception as e:
            logger.error(f'action=build_images error={e}')
            raise

    def get_resolution_x(self, image_id: str) -> Optional[int]:
        if image_id not in self.images:
            return None
        width, height = self.images[image_id].get_resolution()
        return width

    def get_resolution_y(self, image_id: str) -> Optional[int]:
        if image_id not in self.images:
            return None
        width, height = self.images[image_id].get_resolution()
        return height
