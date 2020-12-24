from src.oidconv.coco_image import CocoImage, CocoImages
from src.oidconv.oid_constants import *


class TestCocoImage(object):

    def test_coco_image(self, global_variables):
        coco_image = CocoImage()
        assert coco_image

        coco_image.set(license_id=1, file_name="hoge.jpg", height=1024, width=768)
        assert coco_image
        assert coco_image.license_id > 0
        assert coco_image.file_name
        assert coco_image.height > 0
        assert coco_image.width > 0
        assert coco_image.date_captured

    def test_coco_images(self, global_variables):
        coco_images = CocoImages(ds_type=DATASET_TYPE_VAL, images_dir=global_variables.images_val_path)
        assert coco_images

        license_id = 1
        for image_id in range(1, 100):
            coco_image = CocoImage()
            file_name = f"hoge_{image_id}.jpg"
            coco_image.set(license_id=license_id, file_name=file_name, height=image_id, width=image_id*2)
            coco_images.add(image_id=image_id, image=coco_image)
            assert coco_images.get(image_id)
            json = coco_images.json(image_id)
            assert json["id"] == image_id
