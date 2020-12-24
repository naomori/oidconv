from src.oidconv.oid_image import OidImage, OidImages
from src.oidconv.oid import Oid
from src.oidconv.oid_constants import *
import os


class TestOidImage(object):
    def test_oid_image_1path(self, global_variables):
        oid_image = OidImage()
        assert oid_image

        image_path = f"{global_variables.images_val_path}/ffff21932da3ed01.jpg"
        oid_image.set("1", image_path)
        assert oid_image

        resol = (1024, 768)
        got_resol = oid_image.get_resolution()
        assert got_resol == resol
        oid_image.display()


class TestOidImages(object):
    def test_oid_images_constructor(self, global_variables):
        oid_images = OidImages(DATASET_TYPE_VAL, global_variables.images_val_path)
        assert oid_images
        assert oid_images.ds_type == DATASET_TYPE_VAL
        assert oid_images.images_dir == global_variables.images_val_path
        assert not oid_images.images

    def test_oid_images_build(self, global_variables):
        oid = Oid()
        oid.build_config(global_variables.test_config_path)
        ds_type = DATASET_TYPE_VAL
        oid.build_bbox(ds_type)
        oid_bbox_val = oid.bbox[ds_type]

        oid_images = OidImages(ds_type, global_variables.images_val_path)
        image_id_list = oid_bbox_val.get_image_id()
        oid_images.build_images(image_id_list)
        assert len(oid_images.images) > 0
        count = 0
        for key, image in oid_images.images.items():
            if count < 10:
                image.display()
                count += 1
                break
            assert image.get_filename() == os.path.basename(image.image_path)

    def test_oid_images_resolution(self, global_variables):
        ds_type = DATASET_TYPE_VAL
        oid_images = OidImages(ds_type, global_variables.images_val_path)
        image_id_list = ["ffff21932da3ed01"]
        oid_images.build_images(image_id_list)
        assert len(oid_images.images) > 0
        assert oid_images.get_resolution_x("ffff21932da3ed01") == 1024
        assert oid_images.get_resolution_y("ffff21932da3ed01") == 768
