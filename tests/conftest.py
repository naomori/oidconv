import sys
import os
import pytest

from src.oidconv.oid_class import *
from src.oidconv.oid_constants import *

sys.path.append(os.path.abspath(os.path.dirname(os.path.abspath(__file__)) + "/../src/"))


class TestOidGlobalVariables(object):
    def __init__(self):
        self.class_desc_path = None
        self.images_train_path = None
        self.images_val_path = None
        self.images_test_path = None
        self.bbox_train_path = None
        self.bbox_val_path = None
        self.bbox_test_path = None
        self.class_filter_train_and_val = None
        self.class_filter_test = None
        self.required_class = None
        self.required_labels = None
        self.mixed_dataset = None
        self.label_filter_train_and_val = None
        self.label_filter_test = None
        self.output_images_train = None
        self.output_images_val = None
        self.output_images_test = None
        self.output_bbox_train = None
        self.output_bbox_val = None
        self.output_bbox_test = None

    def get_bbox_path(self, ds_type: int) -> Optional[str]:
        if ds_type == DATASET_TYPE_TRAIN:
            return self.bbox_train_path
        elif ds_type == DATASET_TYPE_VAL:
            return self.bbox_val_path
        elif ds_type == DATASET_TYPE_TEST:
            return self.bbox_test_path
        else:
            return None

    def get_label_filter(self, ds_type: int) -> Optional[List]:
        if (ds_type == DATASET_TYPE_TRAIN) or (ds_type == DATASET_TYPE_VAL):
            return self.label_filter_train_and_val
        elif ds_type == DATASET_TYPE_TEST:
            return self.label_filter_test
        else:
            return None

    def get_required_labels(self) -> List[str]:
        return self.required_labels

    def get_images_dir(self, ds_type: int) -> Optional[str]:
        if ds_type == DATASET_TYPE_TRAIN:
            return self.images_train_path
        elif ds_type == DATASET_TYPE_VAL:
            return self.images_val_path
        elif ds_type == DATASET_TYPE_TEST:
            return self.images_test_path
        else:
            return None

    def get_output_images_dir(self, ds_type: int) -> Optional[str]:
        if ds_type == DATASET_TYPE_TRAIN:
            return self.output_images_train
        elif ds_type == DATASET_TYPE_VAL:
            return self.output_images_val
        elif ds_type == DATASET_TYPE_TEST:
            return self.output_images_test
        else:
            return None

    def get_output_bbox_path(self, ds_type: int) -> Optional[str]:
        if ds_type == DATASET_TYPE_TRAIN:
            return self.output_bbox_train
        elif ds_type == DATASET_TYPE_VAL:
            return self.output_bbox_val
        elif ds_type == DATASET_TYPE_TEST:
            return self.output_bbox_test
        else:
            return None

    def get_mixed_dataset_proportion(self, ds_type: int) -> Optional[int]:
        ds_str = dataset_type2str(ds_type)
        return self.mixed_dataset.get(ds_str, None)


@pytest.fixture()
def global_variables():
    gv = TestOidGlobalVariables()
    gv.test_config_path = "tests/config/test_oidconv.json"
    gv.test_config_error_path = "tests/config/test_oidconv_error.json"
    gv.class_desc_path = "/loft/open_images_dataset_v6/files/class-descriptions-boxable.csv"
    gv.images_train_path = "/loft/open_images_dataset_v6/images/train"
    gv.images_val_path = "/loft/open_images_dataset_v6/images/validation"
    gv.images_test_path = "/loft/open_images_dataset_v6/images/test"
    gv.bbox_train_path = "/loft/open_images_dataset_v6/files/oidv6-train-annotations-bbox.csv"
    gv.bbox_val_path = "/loft/open_images_dataset_v6/files/validation-annotations-bbox.csv"
    gv.bbox_test_path = "/loft/open_images_dataset_v6/files/test-annotations-bbox.csv"
    gv.class_filter_train_and_val = [
        ["Vehicle registration plate"],
        ["Human face", "Person", "Car"],
        ["Human face", "Vehicle"],
        ["Human face", "Land vehicle"],
        ["Human face", "Truck"],
        ["Human face", "Bus"],
        ["Human face", "Van"],
        ["Human face", "Ambulance"],
        ["Human face", "Limousine"],
        ["Human face", "Taxi"],
        ["Human face", "Wheel"],
        ["Human face", "Tire"],
        ["Human face", "Bicycle"],
        ["Human face", "Bicycle wheel"],
        ["Human face", "Motorcycle"],
        ["Human face", "Traffic light"],
        ["Human face", "Traffic sign"],
        ["Human face", "Stop sign"],
        ["Human face", "Parking meter"],
        ["Human face", "Cart"],
        ["Human face", "Street light"],
        ["Human face", "Skateboard"],
        ["Human face", "Wheelchair"],
        ["Human face", "Billboard"],
        ["Human face", "Fire hydrant"],
        ["Human face", "Office building"],
        ["Human face", "Fountain"],
        ["Human face", "Stretcher"],
        ["Human face", "Carnivore"],
        ["Human face", "Roller skates"],
        ["Human face", "Helmet"],
        ["Human face", "Bicycle helmet"],
        ["Human face", "Sunglasses", "Person"],
        ["Human face", "Sun hat", "Person"],
        ["Human face", "Mobile phone", "Person"],
        ["Human face", "Briefcase"],
        ["Human face", "Bench"],
        ["Human face", "Unicycle"],
        ["Human face", "Hiking equipment"],
        ["Human face", "Surfboard"],
        ["Human face", "Golf cart"],
        ["Human face", "Snowmobile"]
    ]

    gv.label_filter_train_and_val = [
        ["/m/01jfm_"],
        ["/m/0dzct", "/m/01g317", "/m/0k4j"],
        ["/m/0dzct", "/m/07yv9"],
        ["/m/0dzct", "/m/01prls"],
        ["/m/0dzct", "/m/07r04"],
        ["/m/0dzct", "/m/01bjv"],
        ["/m/0dzct", "/m/0h2r6"],
        ["/m/0dzct", "/m/012n7d"],
        ["/m/0dzct", "/m/01lcw4"],
        ["/m/0dzct", "/m/0pg52"],
        ["/m/0dzct", "/m/083wq"],
        ["/m/0dzct", "/m/0h9mv"],
        ["/m/0dzct", "/m/0199g"],
        ["/m/0dzct", "/m/01bqk0"],
        ["/m/0dzct", "/m/04_sv"],
        ["/m/0dzct", "/m/015qff"],
        ["/m/0dzct", "/m/01mqdt"],
        ["/m/0dzct", "/m/02pv19"],
        ["/m/0dzct", "/m/015qbp"],
        ["/m/0dzct", "/m/018p4k"],
        ["/m/0dzct", "/m/033rq4"],
        ["/m/0dzct", "/m/06_fw"],
        ["/m/0dzct", "/m/0qmmr"],
        ["/m/0dzct", "/m/01knjb"],
        ["/m/0dzct", "/m/01pns0"],
        ["/m/0dzct", "/m/021sj1"],
        ["/m/0dzct", "/m/0220r2"],
        ["/m/0dzct", "/m/02lbcq"],
        ["/m/0dzct", "/m/01lrl"],
        ["/m/0dzct", "/m/02p3w7d"],
        ["/m/0dzct", "/m/0zvk5"],
        ["/m/0dzct", "/m/03p3bw"],
        ["/m/0dzct", "/m/017ftj", "/m/01g317"],
        ["/m/0dzct", "/m/02wbtzl", "/m/01g317"],
        ["/m/0dzct", "/m/050k8", "/m/01g317"],
        ["/m/0dzct", "/m/0584n8"],
        ["/m/0dzct", "/m/0cvnqh"],
        ["/m/0dzct", "/m/0f6nr"],
        ["/m/0dzct", "/m/0268lbt"],
        ["/m/0dzct", "/m/019w40"],
        ["/m/0dzct", "/m/0323sq"],
        ["/m/0dzct", "/m/01x3jk"]
    ]

    gv.class_filter_test = [
        ["Vehicle registration plate"],
        ["Human face", "Person"]
    ]

    gv.label_filter_test = [
        ["/m/01jfm_"],
        ["/m/0dzct", "/m/01g317"]
    ]

    gv.required_class = [
        "Vehicle registration plate", "Human face"
    ]

    gv.required_labels = [
        '/m/01jfm_', '/m/0dzct'
    ]

    gv.mixed_dataset = {
        "train": 0.8, "val": 0.2
    }

    gv.coco_info_path = "tests/test_coco_files/info.json"
    gv.coco_licenses_path = "tests/test_coco_files/licenses.json"

    gv.output_images_train = "/loft/open_images_dataset_v6/coco/images/train"
    gv.output_images_val = "/loft/open_images_dataset_v6/coco/images/validation"
    gv.output_images_test = "/loft/open_images_dataset_v6/coco/images/test"

    gv.output_bbox_train = "/loft/open_images_dataset_v6/coco/annotations/coco-oid-train-annotations.json"
    gv.output_bbox_val = "/loft/open_images_dataset_v6/coco/annotations/coco-oid-validation-annotations.json"
    gv.output_bbox_test = "/loft/open_images_dataset_v6/coco/annotations/coco-oid-test-annotations.json"

    return gv


@pytest.fixture()
def oid_class_default():
    class_desc_path = "/loft/open_images_dataset_v6/files/class-descriptions-boxable.csv"
    oid_class = OidClass(class_desc_path)
    oid_class.read()
    return oid_class
