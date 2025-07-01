from fastapi import UploadFile
import pandas as pd
from typing import List

class ExcelReader:
    @staticmethod
    async def get_columns(file: UploadFile) -> List[str]:
        df = pd.read_excel(file.file, engine="openpyxl")
        return df.columns.tolist()
