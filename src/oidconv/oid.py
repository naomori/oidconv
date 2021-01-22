from typing import Dict
import logging

from src.oidconv.oidconv_config import OidConvConfig
from src.oidconv.oid_bbox import OidBbox
from src.oidconv.oid_image import OidImage

logger = logging.getLogger(__name__)


class Oid(object):
    def __init__(self):
        self.bbox: Dict[int, OidBbox] = dict()
        self.image: Dict[int, OidImage] = dict()

    def build_bbox(self, ds_type: int, config: OidConvConfig) -> None:
        try:
            bbox_path = config.get_bbox_path(ds_type)
            bbox = OidBbox(ds_type, bbox_path)

            label_filter = config.get_label_filter(ds_type)
            required_labels = config.get_required_labels(ds_type)
            bbox.filter_with_label(label_filter, required_labels)

            self.bbox[ds_type] = bbox

        except Exception as e:
            logger.error(f'action=build_bbox error={e}')
            raise

    def build_image(self, ds_type: int, config: OidConvConfig) -> None:
        try:
            if ds_type not in self.bbox:
                raise ValueError(f'not yet call build_bbox({ds_type})')

            images_dir = config.get_image_dir(ds_type)
            oid_image = OidImage(ds_type, images_dir)

            image_id_list = self.bbox[ds_type].get_image_id()
            oid_image.build_images(image_id_list)

            self.image[ds_type] = oid_image

        except Exception as e:
            logger.error(f'action=build_image error={e}')
            raise
