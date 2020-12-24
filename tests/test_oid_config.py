from src.oidconv.oid_config import *
import pytest


class TestOidConfig(object):

    def test_oid_config_read(self, global_variables):
        oid_config = OidConfig()
        oid_config.read(global_variables.test_config_path)
        assert len(oid_config.class_desc_path) > 0
        for ds_type in DATASET_TYPE_ALL:
            assert oid_config.get_bbox_path(ds_type)
            assert oid_config.get_label_filter(ds_type)
            assert oid_config.get_image_dir(ds_type)
            assert oid_config.get_output_images_dir(ds_type)
            assert oid_config.get_output_bbox_path(ds_type)
        assert type(oid_config.get_image_all_dirs()) == dict

    def test_oid_config_read_error(self, global_variables):
        oid_config = OidConfig()
        with pytest.raises(TypeError):
            oid_config.read(global_variables.test_config_error_path)
