from src.oidconv.coco import Coco
from src.oidconv.coco_category import CocoCategories
from src.oidconv.coco_image import CocoImages
from src.oidconv.oid import Oid
from src.oidconv.oid_class import OidClass
from src.oidconv.oid_conv import OidConv
from src.oidconv.oid_image import OidImages
from src.oidconv.oid_constants import *


class TestCoco(object):

    def test_coco_constructor(self):
        assert Coco()

    def test_coco_read_info(self, global_variables):
        coco = Coco()
        coco.read_info(global_variables.coco_info_path)
        assert coco.info

    def test_coco_read_licenses(self, global_variables):
        coco = Coco()
        coco.read_licenses(global_variables.coco_licenses_path)
        assert type(coco.licenses) == list
        assert len(coco.licenses) > 0
        # print(coco.licenses)

    def test_coco_create_categories(self, global_variables):
        coco = Coco()
        coco.build_categories(global_variables.required_class)
        assert type(coco.categories) == CocoCategories
        assert coco.categories.objs
        # print(coco.categories)

    def test_coco_create_images(self, global_variables):
        coco = Coco()
        assert coco
        oid = Oid()
        oid.build_config(global_variables.test_config_path)
        conv = OidConv()
        for ds_type in DATASET_TYPE_ALL:
            if ds_type != DATASET_TYPE_VAL:
                continue
            oid.build_bbox(ds_type)
            oid.build_image(ds_type)
            assert oid.images[ds_type]
            assert type(oid.images[ds_type]) == OidImages
            coco_images = conv.conv_images(oid_images=oid.images[ds_type])
            coco.create_images(coco_images)
            assert coco.images[ds_type]
            assert type(coco.images[ds_type]) == CocoImages
            assert conv.oid_images
            assert conv.coco_images

    def test_coco_conv_id(self, global_variables):
        oid = Oid()
        oid.build_config(global_variables.test_config_path)
        ds_type = DATASET_TYPE_VAL
        oid.build_bbox(ds_type)
        oid.build_image(ds_type)

        conv = OidConv()
        assert conv
        coco_images = conv.conv_images(oid_images=oid.images[ds_type])
        assert coco_images
        assert conv.oid_images
        assert coco_images == conv.coco_images
        assert coco_images.images
        assert coco_images.images_fileid
        file_id = "0ba4e129511b237b"
        image_id = coco_images.conv_id(file_id)
        print(f"file_id: {file_id}, image_id: {image_id}")
        assert image_id > 0

        oid_class = OidClass()
        assert oid_class
        oid_class.read(global_variables.class_desc_path)

        label_name = global_variables.required_labels[0]
        class_name = global_variables.required_class[0]
        assert oid_class.conv2label([class_name]) == [label_name]
        assert oid_class.label2class(label_name) == class_name

        print(f"required_class: {global_variables.required_class}")
        coco_category = CocoCategories()
        coco_category.build(global_variables.required_class)
        conv.set(oid_class, coco_category)
        assert conv.oid_class
        assert conv.coco_categories

        for label_name in global_variables.required_labels:
            category_id = conv.conv_label2category_id(label_name)
            print(f"label_name: {label_name}, category_id: {category_id}")

    def test_coco_conv_bbox(self, global_variables):
        coco = Coco()
        assert coco
        oid = Oid()
        assert oid
        oid.build_config(global_variables.test_config_path)
        conv = OidConv()
        assert conv

        ds_type = DATASET_TYPE_VAL
        oid.build_bbox(ds_type)
        assert oid.bbox[ds_type]
        oid.build_image(ds_type)
        assert oid.images[ds_type]
        assert type(oid.images[ds_type]) == OidImages

        coco_images = conv.conv_images(oid_images=oid.images[ds_type])
        assert coco_images
        assert conv.oid_images
        assert conv.coco_images

        oid_class = OidClass()
        assert oid_class
        oid_class.read(global_variables.class_desc_path)
        lable_name = "/m/01jfm_"
        class_name = "Vehicle registration plate"
        assert oid_class.conv2label([class_name]) == [lable_name]
        assert oid_class.label2class(lable_name) == class_name

        coco_category = CocoCategories()
        coco_category.build(global_variables.required_class)
        conv.set(oid_class, coco_category)
        assert conv.oid_class
        assert conv.coco_categories

        print(f"oid.bbox[ds_type].df lengh: {len(oid.bbox[ds_type].df)}")
        conv.conv_bbox(oid_bbox=oid.bbox[ds_type])
        print(f"conv.coco_bbox lengh: {len(conv.coco_bbox)}")
        assert len(conv.coco_bbox) == len(oid.bbox[ds_type].df)
        print(conv.coco_bbox.head(5))
        print(conv.coco_bbox.tail(5))

        annotions_json = conv.anntations_json()
        assert annotions_json
        assert len(annotions_json["annotations"]) == len(conv.coco_bbox)
