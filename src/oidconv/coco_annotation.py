from typing import List, Dict, Optional
import logging

logger = logging.getLogger(__name__)


class CocoAnnotation(object):
    def __init__(self):
        self.id: int = 0
        self.image_id: int = 0
        self.category_id: int = 0
        self.bbox: Optional[List[float]] = None

    def set(self, image_id: int, category_id: int, bbox: List[float], annotation_id: int = 0):
        if annotation_id > 0:
            self.id = annotation_id
        self.image_id = image_id
        self.category_id = category_id
        self.bbox = bbox

    def json(self) -> Dict:
        annotation_json = dict()
        annotation_json["id"] = self.id
        annotation_json["image_id"] = self.image_id
        annotation_json["category_id"] = self.category_id
        annotation_json["bbox"] = self.bbox
        return annotation_json


class CocoAnnotations(object):

    def __init__(self, ds_type: int):
        self.ds_type: int = ds_type
        self.annotations: Dict = dict()

    def add(self, annotation_id: int, annotation: CocoAnnotation) -> None:
        annotation.id = annotation_id
        self.annotations[annotation_id] = annotation

    def get(self, annotation_id: int) -> Optional[CocoAnnotation]:
        if annotation_id not in self.annotations:
            return None
        return self.annotations[annotation_id]

    def json(self, annotation_id: int) -> Optional[Dict]:
        annotation = self.get(annotation_id)
        if not annotation:
            logger.error(f"annotation_id:{annotation_id} not found")
            return None
        return annotation.json()
