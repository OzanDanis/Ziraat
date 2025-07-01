from dataclasses import dataclass
from typing import Optional

@dataclass
class ImportedRecord:
    id: Optional[int]
    name: str
