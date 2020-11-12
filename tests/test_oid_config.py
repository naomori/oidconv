from src.oidconv.oid_config import *
from src.oidconv.oid_constants import *


def test_oid_images_constructor():
    oid_images = OidImages(DATASET_TYPE_TRAIN)
    assert oid_images
    assert oid_images.ds_type == DATASET_TYPE_TRAIN
    assert not oid_images.ds_path
    assert oid_images.is_path_dir is True
    assert not oid_images.ds_filter


def test_oid_images_set():
    oid_images = OidImages(DATASET_TYPE_TRAIN)
    ds_path = "/loft/open_images_dataset_v6/images/validation"
    ds_filter = [["hoge", "fuga"], ["fuga", "moga"]]
    oid_images.set(DATASET_TYPE_VAL, ds_path, ds_filter)
    assert oid_images.ds_type == DATASET_TYPE_VAL
    assert oid_images.ds_path == ds_path
    assert oid_images.is_path_dir is True
    assert oid_images.ds_filter == ds_filter


def test_oid_config_constructor():
    dataset_type_list = [DATASET_TYPE_TRAIN, DATASET_TYPE_VAL, DATASET_TYPE_TEST]
    oid_config = OidConfig()
    assert oid_config
    for ds_type in dataset_type_list:
        # images
        assert oid_config.images[ds_type]
        assert oid_config.images[ds_type].ds_type == ds_type
        assert not oid_config.images[ds_type].ds_path
        assert oid_config.images[ds_type].is_path_dir is True
        assert not oid_config.images[ds_type].ds_filter
        assert isinstance(oid_config.images[ds_type], OidImages)
        # bboxes
        assert not oid_config.bboxes[ds_type]
    assert not oid_config.class_desc_path


def test_oid_config_read():
    oid_config = OidConfig()
    config_path = "tests/config/test_oid.json"
    oid_config.read(config_path)
