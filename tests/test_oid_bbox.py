from typing import Tuple
from src.oidconv.oid_config_obj import *
from src.oidconv.oid_bbox import *
from src.oidconv.oid_constants import *


class TestOidBbox(object):

    def test_oid_bbox_all(self, global_variables, oid_class_default):

        def get_path(dst: int) -> Optional[Tuple[str, str, List[List[str]]]]:
            if dst == DATASET_TYPE_VAL:
                return global_variables.images_val_path,\
                       global_variables.bbox_val_path, \
                       global_variables.class_filter_train_and_val
            elif dst == DATASET_TYPE_TRAIN:
                return global_variables.images_train_path, \
                       global_variables.bbox_train_path, \
                       global_variables.class_filter_train_and_val
            elif dst == DATASET_TYPE_TEST:
                return global_variables.images_test_path, \
                       global_variables.bbox_test_path, \
                       global_variables.class_filter_test
            else:
                return None

        for ds_type in DATASET_TYPE_ALL:
            if ds_type != DATASET_TYPE_VAL:
                continue
            conf_obj = OidConfigObject(ds_type)
            images_path, val_path, class_filter = get_path(ds_type)
            conf_obj.set(ds_type, images_path, val_path, oid_class_default, class_filter,
                         global_variables.required_class)

            oid_bbox = OidBbox(ds_type, val_path)
            label_filter = conf_obj.create_label_filter()
            oid_bbox.filter_with_label(label_filter, global_variables.required_labels)

#    def test_oid_bbox_val(self, global_variables, oid_class_default):
#        val_obj = OidConfigObject(DATASET_TYPE_VAL)
#        val_obj.set(DATASET_TYPE_VAL, global_variables.images_val_path, global_variables.bbox_val_path,
#                    oid_class_default,
#                    global_variables.class_filter_train_and_val, global_variables.required_class)
#
#        val_bbox = OidBbox(DATASET_TYPE_VAL, global_variables.bbox_val_path)
#        val_label_filter = val_obj.create_label_filter()
#        val_bbox.filter_with_label(val_label_filter, global_variables.required_labels)
#        # val_bbox.backup_bbox_temp("/tmp/hoge_val.csv")
#
#    def test_oid_bbox_train(self, global_variables, oid_class_default):
#        train_obj = OidConfigObject(DATASET_TYPE_TRAIN)
#        train_obj.set(DATASET_TYPE_TRAIN, global_variables.images_train_path, global_variables.bbox_train_path,
#                      oid_class_default,
#                      global_variables.class_filter_train_and_val, global_variables.required_class)
#
#        train_bbox = OidBbox(DATASET_TYPE_TRAIN, global_variables.bbox_train_path)
#        train_label_filter = train_obj.create_label_filter()
#        train_bbox.filter_with_label(train_label_filter, global_variables.required_labels)
#        # train_bbox.backup_bbox_temp("/tmp/hoge_train.csv")
#
#    def test_oid_bbox_test(self, global_variables, oid_class_default):
#        test_obj = OidConfigObject(DATASET_TYPE_TEST)
#        test_obj.set(DATASET_TYPE_TEST, global_variables.images_test_path, global_variables.bbox_test_path,
#                     oid_class_default,
#                     global_variables.class_filter_test, global_variables.required_class)
#
#        test_bbox = OidBbox(DATASET_TYPE_TEST, global_variables.bbox_test_path)
#        test_label_filter = test_obj.create_label_filter()
#        test_bbox.filter_with_label(test_label_filter, global_variables.required_labels)
#        # test_bbox.backup_bbox_temp("/tmp/hoge_test.csv")
#