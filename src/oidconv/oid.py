from typing import Optional, Dict
import logging

from src.oidconv.oid_config import OidConfig
from src.oidconv.oid_bbox import OidBbox
from src.oidconv.oid_image import OidImages

logger = logging.getLogger(__name__)


class Oid(object):
    def __init__(self):
        self.config: Optional[OidConfig] = None
        self.bbox: Dict[int, OidBbox] = dict()
        self.images: Dict[int, OidImages] = dict()

    def build_config(self, config_path: str) -> None:
        try:
            self.config = OidConfig()
            self.config.read(config_path)
        except Exception as e:
            logger.error(f'action=build_config error={e}')
            raise

    def build_bbox(self, ds_type: int) -> None:
        try:
            if self.config is None:
                raise ValueError(f'self.config is not set')
            bbox_path = self.config.get_bbox_path(ds_type=ds_type)
            bbox = OidBbox(ds_type, bbox_path)
            label_filter = self.config.get_label_filter(ds_type=ds_type)
            required_labels = self.config.get_required_labels(ds_type=ds_type)
            bbox.filter_with_label(label_filter=label_filter, required_labels=required_labels)
            self.bbox[ds_type] = bbox
        except Exception as e:
            logger.error(f'action=build_bbox error={e}')
            raise

    def build_image(self, ds_type: int) -> None:
        try:
            if self.config is None or ds_type not in self.bbox:
                raise ValueError(f'not yet call build_config() or build_bbox({ds_type})')
            image_id_list = self.bbox[ds_type].get_image_id()
            oid_images = OidImages(ds_type=ds_type, images_dir=self.config.get_image_dir(ds_type))
            oid_images.build_images(image_id_list=image_id_list)
            self.images[ds_type] = oid_images
        except Exception as e:
            logger.error(f'action=build_image error={e}')
            raise
