import pytest

from src.oidconv.oid_constants import *
from src.oidconv.oidconv_config import OidConvConfig
from src.oidconv.oid import Oid
from src.oidconv.oid_bbox import OidBbox
from src.oidconv.oid_image import OidImage


class TestOid(object):
    @pytest.fixture()
    def get_config(self):
        def _config(config_path):
            config = OidConvConfig()
            config.read(config_path)
            return config
        return _config

    def test_oid_constructor(self):
        assert Oid()

    def test_oid_build(self, global_variables, get_config):
        config = get_config(global_variables.test_config_path)

        oid = Oid()
        for ds_type in DATASET_TYPE_ALL:
            if ds_type != DATASET_TYPE_VAL:
                continue
            oid.build_bbox(ds_type, config)
            assert type(oid.bbox[ds_type]) == OidBbox
            print(oid.bbox[ds_type].df.head(5))

            oid.build_image(ds_type, config)
            assert type(oid.image[ds_type]) == OidImage
            print(oid.image[ds_type].df.head(5))
