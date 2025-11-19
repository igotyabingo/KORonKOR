import json
import re
from pathlib import Path

RAW_DIR = Path("data/raw")
PROCESSED_DIR = Path("data/processed")

def extract_create_table(ddl_text: str):
    match = re.search(r"(CREATE TABLE[\s\S]*?\);)", ddl_text, re.IGNORECASE)
    return match.group(1).strip() if match else ""

def extract_insert_values(ddl_text: str):
    inserts = re.findall(
        r"INSERT INTO\s+\S+\s*\((.*?)\)\s*values\s*\((.*?)\);", ddl_text, re.IGNORECASE
    )
    data_dict = {}
    for i, (cols_str, values_str) in enumerate(inserts):
        if i >= 3:
            break
        cols = [c.strip() for c in cols_str.split(",")]
        values = [v.strip().strip("'") for v in re.split(r",(?![^()]*\))", values_str)]
        for col, val in zip(cols, values):
            data_dict.setdefault(col, []).append(val)
    return data_dict

def match_table_info(doc_item, table_eng):
    table_map = {orig: kor for orig, kor in zip(doc_item["table_names_original"], doc_item["table_names"])}
    col_map = {orig: kor for (_, orig), (_, kor) in zip(doc_item["column_names_original"][1:], doc_item["column_names"][1:])}
    col_types = {col: t for col, t in zip([c[1] for c in doc_item["column_names_original"][1:]], doc_item["column_types"][1:])}
    return table_map.get(table_eng, ""), col_map, col_types, doc_item["db_id"]

def process_domain(domain_dir: Path):
    ddl_dir = domain_dir / "ddl"
    doc_path = domain_dir / "documentation.json"

    if not ddl_dir.exists() or not doc_path.exists():
        return

    processed_dir = PROCESSED_DIR / domain_dir.name
    processed_dir.mkdir(parents=True, exist_ok=True)
    out_path = processed_dir / "database.jsonl"

    with open(doc_path, "r", encoding="utf-8") as f:
        doc = json.load(f)
    doc_items = doc.get("data", [])

    with open(out_path, "w", encoding="utf-8") as out:
        for sql_file in ddl_dir.glob("*.sql"):
            ddl_text = sql_file.read_text(encoding="utf-8")
            ddl_only = extract_create_table(ddl_text)
            sample_data = extract_insert_values(ddl_text)

            table_match = re.search(r"CREATE TABLE\s+\"?(\w+)\"?", ddl_only, re.IGNORECASE)
            if not table_match:
                continue
            table_eng = table_match.group(1)

            doc_item = next((d for d in doc_items if table_eng in d["table_names_original"]), None)
            if not doc_item:
                continue

            table_kor, col_map, col_types, db_id = match_table_info(doc_item, table_eng)

            columns = []
            for col_eng in col_map:
                columns.append({
                    "eng": col_eng,
                    "kor": col_map[col_eng],
                    "type": col_types.get(col_eng, ""),
                    "data": sample_data.get(col_eng, [])
                })

            line = {
                "ddl": ddl_only,
                "table": {"eng": table_eng, "kor": table_kor},
                "columns": columns,
                "db_id": db_id
            }
            out.write(json.dumps(line, ensure_ascii=False) + "\n")

def run():
    for domain in RAW_DIR.iterdir():
        if domain.is_dir():
            print(f"Processing domain: {domain.name}")
            process_domain(domain)

if __name__ == "__main__":
    run()
