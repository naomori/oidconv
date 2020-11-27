from src.oidconv.oid_obj import *
from src.oidconv.oid_bbox import *
from src.oidconv.oid_constants import *


class TestOidBbox(object):

    def test_oid_bbox_val(self, global_variables, oid_class_default):
        val_obj = OidObject(DATASET_TYPE_VAL)
        val_obj.set(DATASET_TYPE_VAL, global_variables.images_val_path, global_variables.bbox_val_path,
                    oid_class_default,
                    global_variables.class_filter_train_and_val, global_variables.required_class)

        val_bbox = OidBbox(global_variables.bbox_val_path)
        val_label_filter = val_obj.create_label_filter()
        val_bbox.filter_with_label(val_label_filter, global_variables.required_labels)
        # val_bbox.backup_bbox_temp("/tmp/hoge_val.csv")

    def test_oid_bbox_train(self, global_variables, oid_class_default):
        train_obj = OidObject(DATASET_TYPE_TRAIN)
        train_obj.set(DATASET_TYPE_TRAIN, global_variables.images_train_path, global_variables.bbox_train_path,
                      oid_class_default,
                      global_variables.class_filter_train_and_val, global_variables.required_class)

        train_bbox = OidBbox(global_variables.bbox_train_path)
        train_label_filter = train_obj.create_label_filter()
        train_bbox.filter_with_label(train_label_filter, global_variables.required_labels)
        # train_bbox.backup_bbox_temp("/tmp/hoge_train.csv")

    def test_oid_bbox_test(self, global_variables, oid_class_default):
        test_obj = OidObject(DATASET_TYPE_TEST)
        test_obj.set(DATASET_TYPE_TEST, global_variables.images_test_path, global_variables.bbox_test_path,
                     oid_class_default,
                     global_variables.class_filter_test, global_variables.required_class)

        test_bbox = OidBbox(global_variables.bbox_test_path)
        test_label_filter = test_obj.create_label_filter()
        test_bbox.filter_with_label(test_label_filter, global_variables.required_labels)
        # test_bbox.backup_bbox_temp("/tmp/hoge_test.csv")
