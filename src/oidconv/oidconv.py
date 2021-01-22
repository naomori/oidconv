from typing import Optional, List, Dict
import os
import math
import logging
import itertools
from more_itertools import ichunked
import concurrent.futures
from concurrent.futures import ProcessPoolExecutor
import numpy as np
import pandas as pd

from src.oidconv.oidconv_config import OidConvConfig
from src.oidconv.oid import Oid
from src.oidconv.oid_constants import *

from src.oidconv.oid_class import OidClass
from src.oidconv.oid_image import OidImages
from src.oidconv.coco_image import CocoImage, CocoImages
from src.oidconv.oid_bbox import OidBbox
from src.oidconv.coco_category import CocoCategories

logger = logging.getLogger(__name__)


class OidConv(object):
    image_id: int = 1
    annotation_id: int = 1
    coco_columns = ["AnnotationID", "CategoryID", "ImageID", "XMin", "YMin", "Width", "Height"]

    def __init__(self):
        self.config = OidConvConfig()
        self.oid = Oid()

        self.oid_images: Optional[OidImages] = None
        self.coco_images: Optional[CocoImages] = None
        self.coco_bbox = pd.DataFrame(index=[], columns=OidConv.coco_columns)
        self.oid_class: Optional[OidClass] = None
        self.coco_categories: Optional[CocoCategories] = None

    def read_config(self, config_path: str) -> None:
        self.config.read(config_path)

    def build_oid(self):
        if self.config is None:
            raise ValueError(f'not yet call read_config()')

        for ds_type in DATASET_TYPE_ALL:
            bbox_path = self.config.get_bbox_path(ds_type)
            label_filter = self.config.get_label_filter(ds_type)
            required_labels = self.config.get_required_labels(ds_type)
            self.oid.build_bbox(ds_type, bbox_path, label_filter, required_labels)

            images_dir = self.config.get_image_dir(ds_type)
            self.oid.build_image(ds_type, images_dir)

    def set(self, oid_class: OidClass, coco_categories: CocoCategories) -> None:
        self.oid_class: Optional[OidClass] = oid_class
        self.coco_categories: Optional[CocoCategories] = coco_categories

    @staticmethod
    def _concat_coco_images(coco_images_1: CocoImages, coco_images_2: CocoImages) -> CocoImages:
        coco_images_1.images.update(coco_images_2.images)
        coco_images_1.images_fileid.update(coco_images_2.images_fileid)
        return coco_images_1

    @staticmethod
    def _conv_image(start_image_id: int, oid_image_islice: itertools.islice) -> CocoImages:
        coco_images = CocoImages(0, "")
        image_id = start_image_id
        for oid_image in oid_image_islice:
            coco_image = CocoImage()
            dummy_license_id = 1
            file_name = oid_image.get_filename()
            width, height = oid_image.get_resolution()
            coco_image.set(license_id=dummy_license_id, file_name=file_name, width=width, height=height)
            coco_images.add(image_id, coco_image)
            image_id += 1
        return coco_images

    def conv_images(self, oid_images: OidImages) -> CocoImages:
        try:
            n_iter = math.ceil(len(oid_images.images) / os.cpu_count())
            oid_images_itr = ichunked(oid_images.images.values(), n_iter)

            futures = []
            with ProcessPoolExecutor(max_workers=os.cpu_count()) as executor:
                for oid_images_islice in oid_images_itr:
                    future = executor.submit(self._conv_image, OidConv.image_id, oid_images_islice)
                    futures.append(future)
                    OidConv.image_id += n_iter
                OidConv.image_id -= n_iter - (len(oid_images.images) % n_iter)

            concurrent.futures.wait(futures, timeout=None)
            coco_images = CocoImages(oid_images.ds_type, oid_images.images_dir)
            for future in concurrent.futures.as_completed(futures):
                coco_images = self._concat_coco_images(coco_images, future.result())

            self.oid_images = oid_images
            self.coco_images = coco_images
            return coco_images

        except Exception as e:
            logger.error(f'action=conv_images error={e}')
            raise

    def conv_label2category_id(self, label_name: str) -> Optional[int]:
        class_name = self.oid_class.label2class(label_name)
        category = self.coco_categories.get_category(class_name)
        if category is None:
            print(f"error: label_name: {label_name}, class_name: {class_name}")
            return None
        return category.id

    def _conv_bbox(self, start_annotation_id: int, oid_df: pd.DataFrame) -> pd.DataFrame:
        try:
            df = pd.DataFrame(index=[], columns=OidConv.coco_columns)
            df["CategoryID"] = oid_df["LabelName"].map(self.conv_label2category_id)
            df["ImageID"] = oid_df["ImageID"].map(self.coco_images.conv_id)
            df["XMin"] = oid_df["XMin"] * oid_df["ImageID"].map(self.oid_images.get_resolution_x)
            df["YMin"] = oid_df["YMin"] * oid_df["ImageID"].map(self.oid_images.get_resolution_y)
            df["Width"] = (oid_df["XMax"] - oid_df["XMin"]) * oid_df["ImageID"].map(self.oid_images.get_resolution_x)
            df["Height"] = (oid_df["YMax"] - oid_df["YMin"]) * oid_df["ImageID"].map(self.oid_images.get_resolution_y)
            df["AnnotationID"] = pd.RangeIndex(start=start_annotation_id, stop=start_annotation_id+len(oid_df), step=1)
            return df
        except Exception as e:
            logger.error(f'action=conv_bbox error={e}')
            raise

    def conv_bbox(self, oid_bbox: OidBbox) -> None:
        try:
            df_split = np.array_split(oid_bbox.df, os.cpu_count())
            futures = []
            with ProcessPoolExecutor(max_workers=os.cpu_count()) as executor:
                for df_each in df_split:
                    future = executor.submit(self._conv_bbox, OidConv.annotation_id, df_each)
                    futures.append(future)
                    OidConv.annotation_id += len(df_each)

            concurrent.futures.wait(futures, timeout=None)
            for future in concurrent.futures.as_completed(futures):
                self.coco_bbox = pd.concat([self.coco_bbox, future.result()])
            self.coco_bbox.reset_index(drop=True, inplace=True)

        except Exception as e:
            logger.error(f'action=conv_bbox error={e}')
            raise

    @staticmethod
    def _conv_json(bbox_df: pd.DataFrame) -> List[Dict]:
        try:
            annotation_list = []
            for row in bbox_df.itertuples():
                annotation = dict()
                annotation["id"] = row[0]
                annotation["category_id"] = row[1]
                annotation["image_id"] = row[2]
                annotation["bbox"] = [row[3], row[4], row[5], row[6]]
                annotation_list.append(annotation)
            return annotation_list
        except Exception as e:
            logger.error(f'action=conv_bbox error={e}')
            raise

    def annotations_json(self) -> Dict[str, List]:
        try:
            annos_json = []
            df_split = np.array_split(self.coco_bbox, os.cpu_count())
            futures = []
            with ProcessPoolExecutor(max_workers=os.cpu_count()) as executor:
                for df_each in df_split:
                    future = executor.submit(self._conv_json, df_each)
                    futures.append(future)

            concurrent.futures.wait(futures, timeout=None)
            for future in concurrent.futures.as_completed(futures):
                annos_json += future.result()
            annotations = dict()
            annotations["annotations"] = annos_json
            return annotations

        except Exception as e:
            logger.error(f'action=annotations_json error={e}')
            raise
