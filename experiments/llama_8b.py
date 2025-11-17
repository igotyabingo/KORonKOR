# The import statement will vary depending on your LLM and vector database. This is an example for OpenAI + ChromaDB

from vanna.openai.openai_chat import OpenAI_Chat
from vanna.hf import Hf
from vanna.chromadb.chromadb_vector import ChromaDB_VectorStore

class MyVanna(ChromaDB_VectorStore, Hf):
    def __init__(self, config=None):
        ChromaDB_VectorStore.__init__(self, config=config)
        Hf.__init__(self, config=config)

vn = MyVanna(config={'api_key': 'sk-...', 'model': 'gpt-4-...'})

# See the documentation for other options

# 1. training VN
vn.train(ddl=""" 
    CREATE TABLE IF NOT EXISTS my-table (
        id INT PRIMARY KEY,
        name VARCHAR(100),
        age INT
    )
""") # train with DDL statements (about my database)

vn.train(documentation="Our business defines XYZ as ...")

# also can train with some sql 
vn.train(sql="SELECT name, age FROM my-table WHERE name = 'John Doe'")

# 2. query
vn.ask("What are the top 10 customers by sales?")

# models:
# 1. Llama-3.1-8B-Instruct (baseline model) {meta-llama/Llama-3.1-8B-Instruct}
# 2. Llama-VARCO-8B-Instruct (fine-tuned on Korean data) {NCSOFT/Llama-VARCO-8B-Instruct}
# 3. EXAONE-3.5-7.8B-Instruct (Korean-targeted model) {LGAI-EXAONE/EXAONE-3.5-7.8B-Instruct}