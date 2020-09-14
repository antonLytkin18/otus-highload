from dataclasses import dataclass, field, asdict
from typing import Dict

from app.db.models import Model


@dataclass
class Pagination:
    per_page: int
    page: int
    count: int
    list: Dict[id, Model] = field(default_factory=list)

    def get_params(self):
        return {k: v for k, v in asdict(self).items() if k not in ['list']}
