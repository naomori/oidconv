from src.oidconv.oid_constants import *
from src.oidconv.oid_obj import *
from typing import List, Optional
import logging
import json

logger = logging.getLogger(__name__)


class OidConfig(object):
    """read an oid config file and check"""

    def __init__(self):
        """initialize"""
        self.objs = {
            DATASET_TYPE_TRAIN: OidObject(DATASET_TYPE_TRAIN),
            DATASET_TYPE_VAL: OidObject(DATASET_TYPE_VAL),
            DATASET_TYPE_TEST: OidObject(DATASET_TYPE_TEST)
        }
        self.class_desc_path: str = ""

    @staticmethod
    def _check(config_obj: dict) -> None:
        """check the config file"""
        l1_keys_mandatory = ['images', 'bounding_boxes', 'class_descriptions']
        l1_keys_has_l2 = ['images', 'bounding_boxes']
        l2_keys = ['train', 'val', 'test']
        l2_keys_class_filter = ['train', 'val', 'train_and_val', 'test']

        for l1_key in l1_keys_mandatory:
            if l1_key not in config_obj.keys():
                raise TypeError(f'{l1_key} not found')

        for l1_key in l1_keys_has_l2:
            for l2_key in l2_keys:
                if l2_key not in config_obj[l1_key].keys():
                    raise TypeError(f'{l1_key}.{l2_key} not found')

        l1_key = 'class_filter'
        for l2_key in config_obj[l1_key].keys():
            if l2_key not in l2_keys_class_filter:
                raise TypeError(f'{l1_key}.{l2_key} is invalid')

    @staticmethod
    def _get_class_filter(config_obj: dict, ds_type: int) -> Optional[List]:
        ds_str = dataset_type2str(ds_type)
        for l2_keys in config_obj['class_filter'].keys():
            if ds_str in l2_keys:
                return config_obj['class_filter'][l2_keys]
        return None

    @staticmethod
    def _get_required_class(config_obj: dict) -> Optional[List]:
        return config_obj['required_class']

    def read(self, config_path: str) -> None:
        """read an oid config file"""
        try:
            with open(config_path) as f:
                config_obj = json.load(f)
                self._check(config_obj)

            self.class_desc_path = config_obj['class_descriptions']
            oid_class = OidClass(self.class_desc_path)
            oid_class.read()
            self.objs[DATASET_TYPE_TRAIN].set(DATASET_TYPE_TRAIN,
                                              config_obj['images'][DATASET_STR_TRAIN],
                                              config_obj['bounding_boxes'][DATASET_STR_TRAIN],
                                              oid_class, self._get_class_filter(config_obj, DATASET_TYPE_TRAIN),
                                              self._get_required_class(config_obj))
            self.objs[DATASET_TYPE_VAL].set(DATASET_TYPE_VAL,
                                            config_obj['images'][DATASET_STR_VAL],
                                            config_obj['bounding_boxes'][DATASET_STR_VAL],
                                            oid_class, self._get_class_filter(config_obj, DATASET_TYPE_VAL),
                                            self._get_required_class(config_obj))
            self.objs[DATASET_TYPE_TEST].set(DATASET_TYPE_TEST,
                                             config_obj['images'][DATASET_STR_TEST],
                                             config_obj['bounding_boxes'][DATASET_STR_TEST],
                                             oid_class, self._get_class_filter(config_obj, DATASET_TYPE_TEST),
                                             self._get_required_class(config_obj))

        except Exception as e:
            logger.error(f'action=read error={e}')
            raise
