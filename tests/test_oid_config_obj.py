import pytest
from src.oidconv.oid_config_obj import *
from src.oidconv.oid_constants import *


class TestOidObj(object):
    def test_oid_object_constructor(self):
        ds_type = DATASET_TYPE_VAL
        oid_obj = OidConfigObject(ds_type)
        assert oid_obj.ds_type == ds_type
        assert oid_obj.is_images_path is False
        assert oid_obj.oid_class is None

    def test_oid_object_set(self, global_variables, oid_class_default):
        ds_type_list = [DATASET_TYPE_TRAIN, DATASET_TYPE_VAL, DATASET_TYPE_TEST]
        for ds_type in ds_type_list:
            oid_obj = OidConfigObject(ds_type)
            assert oid_obj
            oid_obj.set(ds_type, global_variables.images_val_path, global_variables.bbox_val_path,
                        oid_class_default, global_variables.class_filter_train_and_val, global_variables.required_class)
            assert oid_obj

    def test_oid_object_set_error(self, global_variables, oid_class_default):
        ds_type = DATASET_TYPE_TRAIN
        oid_obj = OidConfigObject(ds_type)
        with pytest.raises(ValueError):
            oid_obj.set(ds_type, "hoge.csv", global_variables.bbox_val_path,
                        oid_class_default, global_variables.class_filter_train_and_val, global_variables.required_class)
