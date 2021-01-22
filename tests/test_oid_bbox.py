import pytest

from src.oidconv.oid_constants import *
from src.oidconv.oidconv_config import OidConvConfig
from src.oidconv.oid_bbox import OidBbox


class TestOidBbox(object):

    @pytest.fixture()
    def get_config(self):
        def _config(config_path):
            config = OidConvConfig()
            config.read(config_path)
            return config
        return _config

    def test_oid_bbox_constructor(self, global_variables, get_config):
        config = get_config(global_variables.test_config_path)
        for ds_type in DATASET_TYPE_ALL:
            bbox_path = config.get_bbox_path(ds_type)
            bbox = OidBbox(ds_type, bbox_path)
            assert bbox
            assert bbox.ds_type == ds_type
            assert bbox.bbox_path == bbox_path

    @pytest.fixture
    def create_bbox(self):
        def _bbox(config, ds_type):
            bbox_path = config.get_bbox_path(ds_type)
            bbox = OidBbox(ds_type, bbox_path)
            return bbox
        return _bbox

    def test_oid_bbox_all(self, global_variables, get_config, create_bbox):
        config = get_config(global_variables.test_config_path)
        for ds_type in DATASET_TYPE_ALL:
            if ds_type != DATASET_TYPE_VAL:
                continue
            bbox = create_bbox(config, ds_type)

            label_filter = config.get_label_filter(ds_type)
            required_labels = config.get_required_labels(ds_type)
            bbox.filter_with_label(label_filter, required_labels)

            columns = bbox.needed_columns
            for column in columns:
                assert column in bbox.df.columns
            assert len(bbox.df) > 0
            print(bbox.df.head(5))
