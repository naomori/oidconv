from typing import List, Dict, Optional
import logging
import json

from src.oidconv.oid_constants import *
from src.oidconv.oidconv_configobj import OidConvConfigObj
from src.oidconv.oid_class import OidClass

logger = logging.getLogger(__name__)


class OidConvConfig(object):
    """read an oid config file and check"""

    def __init__(self):
        """ Initializer """
        self.objs = {
            DATASET_TYPE_TRAIN: OidConvConfigObj(DATASET_TYPE_TRAIN),
            DATASET_TYPE_VAL: OidConvConfigObj(DATASET_TYPE_VAL),
            DATASET_TYPE_TEST: OidConvConfigObj(DATASET_TYPE_TEST)
        }
        self.class_desc_path: str = ""
        self.oid_class: Optional[OidClass] = None
        self.mixed_dataset: Optional[Dict] = None
        self.output: Dict = dict()
        self.output['images']: Dict = dict()
        self.output['bounding_boxes']: Dict = dict()

    @staticmethod
    def _check(config_obj: dict) -> None:
        """check the syntax of the config file"""
        mandatory_keys = ['images', 'bounding_boxes', 'class_descriptions', 'output']
        mandatory_keys_with_dataset = ['images', 'bounding_boxes']
        dataset_keys = ['train', 'val', 'test']
        class_filter_keys = ['train', 'val', 'train_and_val', 'test']

        for m_key in mandatory_keys:
            if m_key not in config_obj.keys():
                raise TypeError(f'{m_key} not found')

        for m_key in mandatory_keys_with_dataset:
            for ds_key in dataset_keys:
                if ds_key not in config_obj[m_key].keys():
                    raise TypeError(f'{m_key}.{ds_key} not found')

        for m_key in mandatory_keys_with_dataset:
            output_key = 'output'
            if not config_obj[output_key][m_key]:
                raise TypeError(f'{output_key}.{m_key} not found')
            for ds_key in dataset_keys:
                if ds_key not in config_obj[output_key][m_key].keys():
                    raise TypeError(f'{output_key}.{m_key}.{ds_key} not found')

        class_filter_key = 'class_filter'
        for cf_key in config_obj[class_filter_key].keys():
            if cf_key not in class_filter_keys:
                raise TypeError(f'{class_filter_key}.{cf_key} is invalid')

        if 'mixed_dataset' in config_obj:
            sum_proportion = 0
            for k, v in config_obj['mixed_dataset'].items():
                if k == 'train' or k == 'val' or k == 'test':
                    sum_proportion += v
                else:
                    raise ValueError(f'{k} must be train, val or test.')
            if sum_proportion != 1.0:
                raise ValueError(f'{sum_proportion} must be 1.0.')

    @staticmethod
    def _class_filter(config_obj: dict, ds_type: int) -> Optional[List]:
        """ fetch the class filter from the config object """
        ds_str = dataset_type2str(ds_type)
        for l2_keys in config_obj['class_filter'].keys():
            if ds_str in l2_keys:
                return config_obj['class_filter'][l2_keys]
        return None

    @staticmethod
    def _required_class(config_obj: dict) -> Optional[List]:
        """ return the required class """
        return config_obj['required_class']

    def read(self, config_path: str) -> None:
        """read an oid config file"""
        try:
            with open(config_path) as f:
                config_obj = json.load(f)
                self._check(config_obj)

            self.class_desc_path = config_obj['class_descriptions']
            self.oid_class = OidClass(self.class_desc_path)
            self.oid_class.read()
            for ds_type in DATASET_TYPE_ALL:
                ds_str = dataset_type2str(ds_type)
                self.objs[ds_type].set(ds_type, config_obj['images'][ds_str], config_obj['bounding_boxes'][ds_str],
                                       self.oid_class, self._class_filter(config_obj, ds_type),
                                       self._required_class(config_obj))
                self.output['images'][ds_type] = config_obj['output']['images'][ds_str]
                self.output['bounding_boxes'][ds_type] = config_obj['output']['bounding_boxes'][ds_str]
            if 'mixed_dataset' in config_obj:
                self.mixed_dataset = config_obj['mixed_dataset']

        except Exception as e:
            logger.error(f'action=read error={e}')
            raise

    def get_bbox_path(self, ds_type: int) -> str:
        """ return the path for bounding box csv file """
        return self.objs[ds_type].bbox_path

    def get_label_filter(self, ds_type: int) -> List[str]:
        """ return the filter constructed of label names """
        return self.objs[ds_type].create_label_filter()

    def get_required_labels(self, ds_type: int) -> List[str]:
        """ return the requid labels """
        return self.objs[ds_type].create_required_labels()

    def get_image_dir(self, ds_type: int) -> str:
        """ return the path for images of specified the dataset type """
        return self.objs[ds_type].images_path

    def get_image_all_dirs(self) -> Dict:
        """ return pathes for all images """
        image_dirs = dict()
        for ds_type in DATASET_TYPE_ALL:
            image_dirs[ds_type] = self.objs[ds_type].images_path
        return image_dirs

    def get_output_images_dir(self, dst_type: int) -> str:
        """ return the output directory for images """
        return self.output['images'][dst_type]

    def get_output_bbox_path(self, ds_type: int) -> str:
        """ return the output path for the bounding box """
        return self.output['bounding_boxes'][ds_type]

    def get_proportion(self, ds_type: int) -> Optional[float]:
        return self.mixed_dataset.get(dataset_type2str(ds_type), None)
