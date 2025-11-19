import json
import os
from pathlib import Path

RAW_DIR = Path("data/raw")
PROCESSED_DIR = Path("data/processed")

def convert_file(raw_json_path: Path, processed_jsonl_path: Path):
    with open(raw_json_path, "r", encoding="utf-8") as f:
        raw = json.load(f)

    items = raw.get("data", [])

    processed_jsonl_path.parent.mkdir(parents=True, exist_ok=True)

    with open(processed_jsonl_path, "w", encoding="utf-8") as out:
        for idx, item in enumerate(items):
            line = {
                "query_id": idx+1,
                "query": item.get("utterance"),
                "sql": item.get("query"),
                "hardness": item.get("hardness"),
                "db_id": item.get("db_id")
            }
            out.write(json.dumps(line, ensure_ascii=False) + "\n")

def run():
    for domain_dir in RAW_DIR.iterdir():
        if not domain_dir.is_dir():
            continue

        raw_file = domain_dir / f"TEXT_NL2SQL_label_publicdata_{domain_dir.name}.json"
        if not raw_file.exists():
            continue

        processed_dir = PROCESSED_DIR / domain_dir.name
        processed_file = processed_dir / "query.jsonl"

        print(f"Converting: {raw_file} -> {processed_file}")
        convert_file(raw_file, processed_file)

if __name__ == "__main__":
    run()
