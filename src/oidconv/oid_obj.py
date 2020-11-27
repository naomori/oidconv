from src.oidconv.oid_class import *
from typing import List, Optional


class OidObject(object):
    def __init__(self, ds_type: int):
        self.ds_type: int = ds_type
        self.images_path: str = ""
        self.is_images_path: bool = False
        self.bbox_path: str = ""
        self.oid_class = None
        self.class_filter: list = []
        self.required_class: list = []

    def set(self, ds_type: int, images_path: str, bbox_path: str, oid_class: OidClass,
            class_filter: Optional[list] = None, required_class: Optional[List] = None) -> None:
        try:
            self.ds_type = ds_type
            if not Path.is_dir(Path(images_path)):
                raise ValueError(f'images_path is invalid')
            self.images_path = images_path
            self.is_images_path = Path.is_dir(Path(self.images_path))
            self.bbox_path = bbox_path
            self.oid_class = oid_class
            if class_filter:
                self.class_filter = class_filter
            if required_class:
                self.required_class = required_class
        except Exception as e:
            logger.error(f'action=read error={e}')
            raise

    def create_label_filter(self) -> List[str]:
        label_filter = []
        for class_names in self.class_filter:
            label_names = self.oid_class.conv2label(class_names)
            label_filter.append(label_names)
        return label_filter

    def create_unique_labels(self) -> List[str]:
        unique_class = set()
        for class_names in self.class_filter:
            for class_name in class_names:
                unique_class.add(class_name)
        unique_labels = self.oid_class.conv2label(list(unique_class))
        return unique_labels

    def create_required_labels(self) -> List[str]:
        unique_class = set(self.required_class)
        required_labels = self.oid_class.conv2label(list(unique_class))
        return required_labels
