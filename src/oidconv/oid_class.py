from typing import List, Optional
from pathlib import Path
import logging
import pandas as pd

logger = logging.getLogger(__name__)


class OidClass(object):
    def __init__(self, class_desc_path: Optional[str] = None):
        self.class_desc_path = class_desc_path
        self.df_class: Optional[pd.DataFrame] = None

    def read(self, class_desc_path: Optional[str] = None) -> None:
        try:
            if class_desc_path:
                if not Path.is_file(Path(class_desc_path)):
                    raise ValueError(f'class_desc_path is invalid')
                else:
                    self.class_desc_path = class_desc_path
            if self.class_desc_path is None:
                raise ValueError(f'class_desc_path must be set')
            self.df_class = pd.read_csv(self.class_desc_path, names=['LabelName', 'ClassName'])
        except Exception as e:
            logger.error(f'action=read error={e}')
            raise

    def conv2label(self, class_names: List[str]) -> List[str]:
        try:
            if self.df_class is None:
                raise ValueError(f'read() must be call first')
            df_class_names = self.df_class[self.df_class['ClassName'].isin(class_names)]
            label_names = df_class_names['LabelName'].values.tolist()
            return label_names
        except Exception as e:
            logger.error(f'action=conv2label error={e}')
            raise

    def label2class(self, label_name: str) -> str:
        try:
            if not any(self.df_class['LabelName'].isin([label_name])):
                raise ValueError(f'{label_name} not found')
            df_label_names = self.df_class[self.df_class['LabelName'].isin([label_name])]
            class_names = df_label_names['ClassName'].values.tolist()
            return class_names[0]
        except Exception as e:
            logger.error(f'action=conv2class error={e}')
            raise
