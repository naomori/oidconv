from src.oidconv.coco_annotation import CocoAnnotation, CocoAnnotations
from src.oidconv.oid_constants import *


class TestCocoAnnotation(object):
    def test_coco_anno(self, global_variables):
        coco_anno = CocoAnnotation()
        assert coco_anno
        assert coco_anno.image_id == 0
        assert coco_anno.category_id == 0

        annotation_id = 1000
        image_id = 1000
        category_id = 1000
        bbox = [0.1, 0.2, 0.3]
        coco_anno.set(annotation_id=annotation_id, image_id=image_id, category_id=category_id, bbox=bbox)

        assume_json = {"id": annotation_id, "image_id": image_id, "category_id": category_id, "bbox": bbox}
        result_json = coco_anno.json()
        assert result_json == assume_json

    def test_coco_annos(self, global_variables):
        ds_type = DATASET_TYPE_VAL
        coco_annos = CocoAnnotations(ds_type)
        assert coco_annos
        assert coco_annos.ds_type == ds_type

        coco_anno = CocoAnnotation()
        annotation_id = 1000
        image_id = 1000
        category_id = 1000
        bbox = [0.1, 0.2, 0.3]
        coco_anno.set(image_id=image_id, category_id=category_id, bbox=bbox)

        coco_annos.add(annotation_id=annotation_id, annotation=coco_anno)
        assert coco_annos.annotations[annotation_id] == coco_anno

        got_coco_anno = coco_annos.get(annotation_id)
        assert coco_anno == got_coco_anno

        got_coco_anno = coco_annos.get(1)
        assert not got_coco_anno

        got_json = coco_annos.json(annotation_id=annotation_id)
        assert got_json == coco_anno.json()

        got_json = coco_annos.json(annotation_id=1)
        assert not got_json




