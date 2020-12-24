from typing import List, Dict, Optional
import logging

logger = logging.getLogger(__name__)


class CocoCategory(object):
    def __init__(self, category_id: int, category_name: str, supercategory_name: str):
        self.id: int = category_id
        self.name: str = category_name
        self.supercategory: str = supercategory_name


class CocoCategories(object):
    def __init__(self):
        self.objs: Dict = dict()

    def build(self, category_names: List[str]) -> None:

        def has_duplicated(cats: List[str]) -> bool:
            return len(cats) != len(set(cats))

        try:
            if has_duplicated(category_names):
                raise ValueError(f'category_names has duplicated entries')
            for category_id, category_name in enumerate(category_names, start=1):
                self.objs[category_name] = CocoCategory(category_id, category_name, category_name)

        except Exception as e:
            logger.error(f'action=build error={e}')
            raise

    def get_category(self, category_name: str) -> Optional[CocoCategory]:
        if category_name not in self.objs:
            return None
        else:
            return self.objs[category_name]
