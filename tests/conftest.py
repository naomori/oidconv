import sys
import os
import pytest
from src.oidconv.oid_class import *

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


@pytest.fixture()
def global_variables():
    gv = TestOidGlobalVariables()
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

    gv.class_filter_test = [
        ["Vehicle registration plate"],
        ["Human face", "Person"]
    ]

    gv.required_class = [
        "Vehicle registration plate", "Human face"
    ]
    gv.required_labels = [
        '/m/01jfm_', '/m/0dzct'
    ]
    return gv


@pytest.fixture()
def oid_class_default():
    class_desc_path = "/loft/open_images_dataset_v6/files/class-descriptions-boxable.csv"
    oid_class = OidClass(class_desc_path)
    oid_class.read()
    return oid_class
