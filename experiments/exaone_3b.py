from vanna.hf import Hf
from vanna.chromadb.chromadb_vector import ChromaDB_VectorStore
from sqlalchemy import create_engine
import pandas as pd

class MyVanna(ChromaDB_VectorStore, Hf):
    def __init__(self, config=None):
        ChromaDB_VectorStore.__init__(self, config=config)
        Hf.__init__(self, config=config)

vn = MyVanna(config={'model_name_or_path': 'LGAI-EXAONE/EXAONE-3.5-2.4B-Instruct'})

# 1. training VN with DDL statements
vn.train(ddl=""" 
    CREATE TABLE IF NOT EXISTS my-table (
        id INT PRIMARY KEY,
        name VARCHAR(100),
        age INT
    )
""") 

# 2. training VN with documentations about DB
vn.train(documentation="Our business defines XYZ as ...")

# 3. query LLM to output SQL
vn.ask("What are the top 10 customers by sales?")