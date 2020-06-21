from dataclasses import dataclass, field
from typing import Dict

from app.db.models import Model


@dataclass
class Pagination:
    per_page: int
    page: int
    count: int
    list: Dict[id, Model] = field(default_factory=list)
