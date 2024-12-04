from dotenv import dotenv_values
from pathlib import Path
import pandas as pd
import json
import pandas as pd
import tabula 

from src.data_processing.utilities import prepare_and_save_data
# config = dotenv_values(".env")



pdf_file = tabula.read_pdf('0343582793_C01_20241031.pdf', pages = 2)
print(pdf_file)
