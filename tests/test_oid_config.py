from src.oidconv.oid_config import *
import pytest

config_path = "tests/config/test_oid.json"
config_error_path = "tests/config/test_oid_error.json"


class TestOidConfig(object):

    def test_oid_config_read(self):
        oid_config = OidConfig()
        oid_config.read(config_path)
        assert oid_config.objs[DATASET_TYPE_TRAIN]
        assert oid_config.objs[DATASET_TYPE_VAL]
        assert oid_config.objs[DATASET_TYPE_TEST]

    def test_oid_config_read_error(self):
        oid_config = OidConfig()
        with pytest.raises(TypeError):
            oid_config.read(config_error_path)