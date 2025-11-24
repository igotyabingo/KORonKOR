import argparse
import json
from vanna.hf import Hf
from vanna.chromadb.chromadb_vector import ChromaDB_VectorStore


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


def run_queries(vn, path, output_path):
    with open(path, "r", encoding="utf-8") as f, open(output_path, "w", encoding="utf-8") as out:
        for line in f:
            row = json.loads(line)

            q = row["query"]
            gold_sql = row.get("sql")

            answer = vn.ask(q)

            predicted_sql = answer.get("sql", None)
            answer_text = answer.get("result", None)

            is_correct = (predicted_sql == gold_sql)

            out_row = {
                **row,
                "predicted_sql": predicted_sql,
                "is_correct": is_correct,
                "answer_text": answer_text,
            }

            out.write(json.dumps(out_row, ensure_ascii=False) + "\n")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--model", required=True)
    parser.add_argument("--domain", required=True)
    args = parser.parse_args()

    vn = MyVanna(config={"model_name_or_path": args.model})

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
