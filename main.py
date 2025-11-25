import os
import argparse
import json
from vanna.hf import Hf
from vanna.chromadb.chromadb_vector import ChromaDB_VectorStore
import sqlparse
from dotenv import load_dotenv

class MyVanna(ChromaDB_VectorStore, Hf):
    def __init__(self, config=None):
        ChromaDB_VectorStore.__init__(self, config=config)
        Hf.__init__(self, config=config)


def build_documentation(table_name_eng, table_name_kor, columns):
    lines = []
    lines.append(f"Table: {table_name_eng} ({table_name_kor})")
    lines.append("Columns:")

    for col in columns:
        eng = col.get("eng")
        kor = col.get("kor")
        col_type = col.get("type")
        data = col.get("data", [])

        example = ""
        if data:
            example = f" (example: {data[0]})"

        lines.append(f"- {eng} ({kor}), type={col_type}{example}")

    return "\n".join(lines)


def load_database_jsonl(path):
    ddls = []
    docs = []

    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            row = json.loads(line)

            if "ddl" in row:
                ddls.append(row["ddl"])

            if "table" in row and "columns" in row:
                doc = build_documentation(
                    row["table"]["eng"],
                    row["table"]["kor"],
                    row["columns"]
                )
                docs.append(doc)

    return ddls, docs

def normalize_sql(sql: str):
    if not sql:
        return ""
    return sqlparse.format(sql, keyword_case="lower", strip_comments=True, reindent=True).replace("\n", " ").replace("  ", " ").strip()

def run_queries(vn, path, output_path):
    with open(path, "r", encoding="utf-8") as f_in, \
         open(output_path, "w", encoding="utf-8") as f_out:

        for idx, line in enumerate(f_in):
            row = json.loads(line)
            q = row["query"]
            gt_sql = row.get("sql", None)

            predicted_sql = vn.generate_sql(q)

            out = {
                "query_id": row["query_id"],
                "query": q,
                "predicted_sql": predicted_sql,
                "gt_sql": gt_sql,
                "match": normalize_sql(predicted_sql) == normalize_sql(gt_sql)
            }

            f_out.write(json.dumps(out, ensure_ascii=False) + "\n")
            print(f"{idx+1} query created")

    print("Done.")



def main():
    load_dotenv()
    token = os.getenv("HF_TOKEN")

    if token is None:
        raise ValueError("HF_TOKEN not found in .env")

    parser = argparse.ArgumentParser()
    parser.add_argument("--model", required=True)
    parser.add_argument("--domain", required=True)
    args = parser.parse_args()

    vn = MyVanna(config={"model_name_or_path": args.model, 'allow_llm_to_see_data': True, 'hf_token': token})

    db_path = f"data/processed/{args.domain}/database.jsonl"
    ddls, docs = load_database_jsonl(db_path)

    for ddl in ddls:
        vn.train(ddl=ddl)

    for doc in docs:
        vn.train(documentation=doc)

    query_path = f"data/processed/{args.domain}/query.jsonl"
    output_path = f"result/{args.domain}.jsonl"
    run_queries(vn, query_path, output_path)


if __name__ == "__main__":
    main()
