import os
from typing import List, Optional
from pathlib import Path
import pandas as pd
import concurrent.futures
from concurrent.futures import ProcessPoolExecutor


class OidBbox(object):
    def __init__(self, bbox_path: str):
        self.df = None
        self.bbox_path: str = bbox_path

    def _check(self, bbox_path: Optional[str] = None):
        if bbox_path:
            if not Path.is_file(Path(bbox_path)):
                raise ValueError(f'bbox_path is invalid')
            else:
                self.bbox_path = bbox_path
        if self.bbox_path is None:
            raise ValueError(f'bbox_path must be set')

    @staticmethod
    def _split_last_df_image(df):
        df_image = df.groupby("ImageID")
        last_image_id = df.tail(1)["ImageID"]
        last_group = df_image.get_group(*last_image_id)
        last_group_len = len(last_group)
        if last_group_len < len(df):
            df.drop(df.tail(last_group_len).index, inplace=True)
        df_all = df
        df_rest = last_group
        return df_all, df_rest

    @staticmethod
    def _apply_filter(df: pd.DataFrame, label_filter: List, required_labels: List[str]) -> Optional[pd.DataFrame]:

        def _filter_func(df_tgt: pd.DataFrame, labels_list: List, required: List[str]) -> Optional[pd.DataFrame]:
            for labels in labels_list:
                if set(labels).issubset(list(df["LabelName"])):
                    return df_tgt[df_tgt['LabelName'].isin(required)]
            return None

        return df.groupby("ImageID", as_index=False).apply(_filter_func,
                                                           labels_list=label_filter, required=required_labels)

    def filter_with_label(self, label_filter: List, required_labels: List[str]) -> None:
        self._check()
        chunk_size = 10000
        futures = []
        with ProcessPoolExecutor(max_workers=os.cpu_count()) as executor:
            df_rest = None
            needed_columns = ["ImageID", "LabelName", "XMin", "XMax", "YMin", "YMax"]
            for index, df_bbox in enumerate(pd.read_csv(self.bbox_path, header=0, usecols=needed_columns,
                                                        chunksize=chunk_size)):
                df, df_last = self._split_last_df_image(df_bbox)
                if df_rest is not None:
                    df = pd.concat([df_rest, df])
                df_rest = df_last
                if index == 0:
                    df = self._apply_filter(df, label_filter, required_labels)
                    self.df = df
                else:
                    future = executor.submit(self._apply_filter, df, label_filter, required_labels)
                    futures.append(future)

        concurrent.futures.wait(futures, timeout=None)
        df_list = [future.result() for future in concurrent.futures.as_completed(futures)]
        for df in df_list:
            self.df = pd.concat([self.df, df])

    def backup_bbox_temp(self, backup_filename: str) -> None:
        self.df.to_csv(backup_filename, header=True, index=False, mode='w')
