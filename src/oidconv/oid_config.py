import json
from pathlib import Path
import logging

from src.oidconv.oid_constants import *

logger = logging.getLogger(__name__)


class OidImages(object):
    def __init__(self, ds_type: int):
        self.ds_type: int = ds_type
        self.ds_path: str = ""
        self.is_path_dir: bool = True
        self.ds_filter = []

    def set(self, ds_type: int, ds_path: str, ds_filter):
        self.ds_type = ds_type
        self.ds_path = ds_path
        p = Path(ds_path)
        self.is_path_dir = Path.is_dir(p)
        if ds_filter:
            self.ds_filter = ds_filter


class OidConfig(object):
    """read an oid config file and check"""
    def __init__(self):
        """initialize"""
        self.images = {
            DATASET_TYPE_TRAIN: OidImages(DATASET_TYPE_TRAIN),
            DATASET_TYPE_VAL: OidImages(DATASET_TYPE_VAL),
            DATASET_TYPE_TEST: OidImages(DATASET_TYPE_TEST)
        }
        self.bboxes = {
            DATASET_TYPE_TRAIN: "",
            DATASET_TYPE_VAL: "",
            DATASET_TYPE_TEST: ""
        }
        self.class_desc_path: str = ""

    @staticmethod
    def _check(config_obj):
        """check the config file"""
        l1_keys_mandatory = ['images', 'bboxes', 'class_desc']
        l1_keys_has_l2 = ['images', 'bboxes']
        l2_keys = ['train', 'val', 'test']
        l2_keys_images_filter = ['train', 'val', 'train+val', 'test']

        for l1_key in l1_keys_mandatory:
            if l1_key not in config_obj.keys():
                raise TypeError(f'{l1_key} not found')

        for l1_key in l1_keys_has_l2:
            for l2_key in l2_keys:
                if l2_key not in config_obj[l1_key].keys():
                    raise TypeError(f'{l1_key}.{l2_key} not found')

        l1_key = 'images_filter'
        for l2_key in config_obj[l1_key].keys():
            if l2_key not in l2_keys_images_filter:
                raise TypeError(f'{l1_key}.{l2_key} is invalid')

    @staticmethod
    def _get_images_filter(config_obj, ds_type: int):
        ds_str = dataset_type2str(ds_type)
        for l2_keys in config_obj['images_filter'].keys():
            if ds_str in l2_keys:
                return config_obj['images_filter'][l2_keys]
        return None

    def read(self, config_path: str):
        """read an oid config file"""
        try:
            with open(config_path) as f:
                config_obj = json.load(f)
                self._check(config_obj)

            train_images_filter = self._get_images_filter(config_obj, DATASET_TYPE_TRAIN)
            self.images[DATASET_TYPE_TRAIN].set(DATASET_TYPE_TRAIN,
                                                config_obj['images'][DATASET_STR_TRAIN], train_images_filter)
            val_images_filter = self._get_images_filter(config_obj, DATASET_TYPE_VAL)
            self.images[DATASET_TYPE_VAL].set(DATASET_TYPE_VAL,
                                              config_obj['images'][DATASET_STR_VAL], val_images_filter)
            test_images_filter = self._get_images_filter(config_obj, DATASET_TYPE_TEST)
            self.images[DATASET_TYPE_TEST].set(DATASET_TYPE_TEST,
                                               config_obj['images'][DATASET_STR_TEST], test_images_filter)

            self.bboxes[DATASET_TYPE_TRAIN] = config_obj['bboxes'][DATASET_STR_TRAIN]
            self.bboxes[DATASET_TYPE_VAL] = config_obj['bboxes'][DATASET_STR_VAL]
            self.bboxes[DATASET_TYPE_TEST] = config_obj['bboxes'][DATASET_STR_TEST]

            self.class_desc_path = config_obj['class_desc']

        except Exception as e:
            logger.error(f'action=read error={e}')
            raise
