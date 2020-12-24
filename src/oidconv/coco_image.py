from typing import Optional, Dict
import os
import datetime
import logging

logger = logging.getLogger(__name__)


class CocoImage(object):

    def __init__(self):
        self.id: int = 0
        self.file_id: Optional[str] = None
        self.file_name: Optional[str] = None
        self.license_id: int = 0
        self.width: int = 0     # the number of piexels
        self.height: int = 0    # the number of piexels
        self.date_captured: Optional[str] = None

    def set(self, file_name: str, license_id: int, height: int, width: int) -> None:
        self.file_name = file_name
        self.file_id = os.path.splitext(os.path.basename(file_name))[0]
        self.license_id = license_id
        self.height = height
        self.width = width
        now = datetime.datetime.now()
        self.date_captured = now.strftime('%Y-%m-%d %H:%M:%S')

    def json(self) -> Dict:
        image_json = dict()
        image_json["id"] = self.id
        image_json["file_name"] = self.file_name
        image_json["license"] = self.license_id
        image_json["width"] = self.width
        image_json["heigh"] = self.height
        image_json["date_captured"] = self.date_captured
        return image_json


class CocoImages(object):

    def __init__(self, ds_type: int, images_dir: str):
        self.ds_type: int = ds_type
        self.images_dir: str = images_dir
        self.images: Dict[int, CocoImage] = dict()          # key is an image_id
        self.images_fileid: Dict[str, CocoImage] = dict()   # key is a file_id

    def add(self, image_id: int, image: CocoImage) -> None:
        image.id = image_id
        self.images[image_id] = image
        self.images_fileid[image.file_id] = image

    def get(self, image_id: int) -> Optional[CocoImage]:
        if image_id not in self.images:
            return None
        return self.images[image_id]

    def conv_id(self, file_id: str) -> Optional[int]:
        if file_id not in self.images_fileid:
            return None
        return self.images_fileid[file_id].id

    def json(self, image_id: int) -> Optional[Dict]:
        image = self.get(image_id)
        if not image:
            logger.error(f"image_id:{image_id} not found")
            return None
        return image.json()
