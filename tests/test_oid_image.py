import pytest

from src.oidconv.oid_constants import *
from src.oidconv.oidconv_config import OidConvConfig
from src.oidconv.oid_bbox import OidBbox
from src.oidconv.oid_image import OidImage


class TestOidImage(object):
    def test_oid_image_constructor(self, global_variables):
        for ds_type in DATASET_TYPE_ALL:
            images_dir = global_variables.get_output_images_dir(ds_type)
            oid_image = OidImage(ds_type, images_dir)
            assert oid_image
            assert oid_image.ds_type == ds_type
            assert oid_image.images_dir == images_dir

    @pytest.fixture()
    def get_config(self):
        def _config(config_path):
            config = OidConvConfig()
            config.read(config_path)
            return config
        return _config

    @pytest.fixture
    def build_bbox(self):
        def _bbox(config, ds_type):
            bbox_path = config.get_bbox_path(ds_type)
            label_filter = config.get_label_filter(ds_type)
            required_labels = config.get_required_labels(ds_type)
            bbox = OidBbox(ds_type, bbox_path)
            bbox.filter_with_label(label_filter, required_labels)
            return bbox
        return _bbox

    def test_oid_image_build(self, global_variables, get_config, build_bbox):
        config = get_config(global_variables.test_config_path)

        for ds_type in DATASET_TYPE_ALL:
            if ds_type != DATASET_TYPE_VAL:
                continue
            bbox = build_bbox(config, ds_type)

            images_dir = config.get_image_dir(ds_type)
            oid_image = OidImage(ds_type, images_dir)
            assert oid_image
            assert oid_image.ds_type == ds_type
            assert oid_image.images_dir == images_dir

            image_id_list = bbox.get_image_id()
            oid_image.build_images(image_id_list)
            columns = oid_image.needed_columns
            for column in columns:
                assert column in oid_image.df.columns
            assert len(oid_image.df) > 0
            print(oid_image.df.head(5))

    def test_get_resolution(self, global_variables, get_config, build_bbox):
        config = get_config(global_variables.test_config_path)
        ds_type = DATASET_TYPE_VAL

        images_dir = config.get_image_dir(ds_type)
        oid_image = OidImage(ds_type, images_dir)
        image_id_list = ["ffff21932da3ed01"]
        oid_image.build_images(image_id_list)

        image_path = f"{global_variables.images_val_path}/ffff21932da3ed01.jpg"
        actual_resolution = OidImage.get_resolution(image_path)
        resolution = oid_image.resolution(image_id_list[0])
        assert resolution == actual_resolution
