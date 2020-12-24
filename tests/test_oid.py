from src.oidconv.oid import Oid
from src.oidconv.oid_constants import *


class TestOid(object):
    def test_oid_constructor(self):
        assert Oid()

    def test_oid_build_config(self, global_variables):
        oid = Oid()
        oid.build_config(global_variables.test_config_path)
        assert oid.config

    def test_oid_build_bbox(self, global_variables):
        oid = Oid()
        oid.build_config(global_variables.test_config_path)

        for ds_type in DATASET_TYPE_ALL:
            if ds_type != DATASET_TYPE_VAL:
                continue
            oid.build_bbox(ds_type)
            assert oid.bbox[ds_type]

    def test_oid_build_image(self, global_variables):
        oid = Oid()
        oid.build_config(global_variables.test_config_path)

        for ds_type in DATASET_TYPE_ALL:
            if ds_type != DATASET_TYPE_VAL:
                continue
            oid.build_bbox(ds_type)
            oid.build_image(ds_type)