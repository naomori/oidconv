from src.oidconv.oidconv_config import *
import pytest


class TestOidConfig(object):

    def test_oid_config_read(self, global_variables):
        oid_config = OidConvConfig()
        oid_config.read(global_variables.test_config_path)
        assert len(oid_config.class_desc_path) > 0

        for ds_type in DATASET_TYPE_ALL:
            assert oid_config.get_bbox_path(ds_type) == global_variables.get_bbox_path(ds_type)
            assert oid_config.get_label_filter(ds_type).sort() == global_variables.get_label_filter(ds_type).sort()
            assert oid_config.get_required_labels(ds_type) == global_variables.get_required_labels()
            assert oid_config.get_image_dir(ds_type) == global_variables.get_images_dir(ds_type)
            assert oid_config.get_output_images_dir(ds_type) == global_variables.get_output_images_dir(ds_type)
            assert oid_config.get_output_bbox_path(ds_type) == global_variables.get_output_bbox_path(ds_type)
            assert oid_config.get_proportion(ds_type) == global_variables.get_mixed_dataset_proportion(ds_type)

        image_all_dirs = oid_config.get_image_all_dirs()
        assert type(image_all_dirs) == dict
        for k, v in image_all_dirs.items():
            assert k == DATASET_TYPE_TRAIN or k == DATASET_TYPE_VAL or k == DATASET_TYPE_TEST
            assert v == global_variables.get_images_dir(k)

    def test_oid_config_read_error(self, global_variables):
        oid_config = OidConvConfig()
        with pytest.raises(TypeError):
            oid_config.read(global_variables.test_config_error_path)
