from src.oidconv.oid_class import *
import pytest

class_desc_path = "/loft/open_images_dataset_v6/files/class-descriptions-boxable.csv"


class TestOidClass(object):
    def test_oid_class_constructor_without_path(self):
        oid_class = OidClass()
        assert oid_class is not None

    def test_oid_class_constructor(self):
        oid_class = OidClass(class_desc_path)
        assert oid_class is not None

    def test_oid_class_read(self):
        oid_class = OidClass()
        oid_class.read(class_desc_path)
        assert oid_class.class_desc_path == class_desc_path

    def test_oid_class_read_path_not_set(self):
        oid_class = OidClass()
        with pytest.raises(ValueError):
            oid_class.read()

    def test_oid_class_read_path_is_invalid(self):
        oid_class = OidClass()
        with pytest.raises(ValueError):
            oid_class.read()

    def test_oid_class_conv2label_single(self):
        oid_class = OidClass()
        oid_class.read(class_desc_path)
        class_names_01 = ["Vehicle registration plate"]
        label_names_01 = oid_class.conv2label(class_names_01)
        assert len(label_names_01) == 1
        assert type(label_names_01) == list
        assert label_names_01[0] == "/m/01jfm_"

    def test_oid_class_conv2label_multiple(self):
        oid_class = OidClass()
        oid_class.read(class_desc_path)
        class_names_02 = ["Human face", "Person", "Car"]
        label_names_02 = oid_class.conv2label(class_names_02)
        assert len(label_names_02) == 3
        assert type(label_names_02) == list
        assert label_names_02[0] == "/m/01g317"
        assert label_names_02[1] == "/m/0dzct"
        assert label_names_02[2] == "/m/0k4j"

    def test_oid_class_conv2label_error(self):
        oid_class = OidClass()
        with pytest.raises(ValueError):
            class_names = ["Vehicle registration plate"]
            label_names = oid_class.conv2label(class_names)
            print(label_names)
