from typing import List, Dict, Optional
import logging
import json

from src.oidconv.coco_image import CocoImages
from src.oidconv.coco_category import CocoCategory, CocoCategories

logger = logging.getLogger(__name__)


class Coco(object):
    def __init__(self):
        self.info: Optional[dict] = None
        self.licenses: Optional[List] = None
        self.categories: CocoCategories = CocoCategories()
        self.images: Optional[Dict] = dict()
        self.annotations: Optional[Dict] = dict()

    def read_info(self, info_path: str) -> None:
        """read the info in json file and covert it into json object"""
        try:
            with open(info_path) as f:
                info_obj = json.load(f)
                self.info = info_obj
        except Exception as e:
            logger.error(f'action=read_info error={e}')
            raise

    def read_licenses(self, licenses_path: str) -> None:
        """read the licenses in json file and covert it into json object"""

        def _check_licenses(licenses_obj: dict) -> None:
            if 'licenses' not in licenses_obj.keys():
                raise TypeError(f'licenses is not included')
            license_list = licenses_obj['licenses']
            if len(license_list) <= 0:
                raise TypeError(f'licenses is not included')
            necessary_keys = ['url', 'id', 'name']
            for license_obj in license_list:
                for necessary_key in necessary_keys:
                    if necessary_key not in license_obj:
                        raise TypeError(f'{necessary_key} does not exist in license')
                    if necessary_key == 'id':
                        id_value = license_obj.get(necessary_key)
                        if not isinstance(id_value, int) or id_value <= 0:
                            raise TypeError(f'id:{id_value} is invalid')

        try:
            with open(licenses_path) as f:
                licenses = json.load(f)
                _check_licenses(licenses)
                self.licenses = licenses['licenses']
        except Exception as e:
            logger.error(f'action=read_licenses error={e}')
            raise

    def build_categories(self, category_names: List[str]) -> None:
        self.categories.build(category_names)

    def get_category(self, name: str) -> CocoCategory:
        return self.categories.get_category(name)

    def create_images(self, coco_images: CocoImages):
        self.images[coco_images.ds_type] = coco_images

    def build_annotations(self, ds_type: int) -> None:
        self.annotations[ds_type] = None
        # XXX annotations を作成する オブジェクトではなく DataFrame でデータを保持しているが、どのように扱うか？
