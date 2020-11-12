DATASET_TYPE_INVALID = -1
DATASET_TYPE_TRAIN = 0
DATASET_TYPE_VAL = 1
DATASET_TYPE_TEST = 2

DATASET_STR_TRAIN = 'train'
DATASET_STR_VAL = 'val'
DATASET_STR_TEST = 'test'


def dataset_type2str(ds_type: int) -> str:
    """convert dataset type to string"""
    if ds_type == DATASET_TYPE_TRAIN:
        return DATASET_STR_TRAIN
    elif ds_type == DATASET_TYPE_VAL:
        return DATASET_STR_VAL
    elif ds_type == DATASET_TYPE_TEST:
        return DATASET_STR_TEST
    else:
        raise TypeError(f'ds_type:{ds_type} is invalid')
