from fastapi import UploadFile
import pandas as pd
from typing import List

class CSVReader:
    @staticmethod
    async def get_columns(file: UploadFile) -> List[str]:
        """
        Pandas ile CSV’yi DataFrame’e çevirir,
        sütun isimlerini liste olarak döner.
        """
        df = pd.read_csv(file.file)
        return df.columns.tolist()
