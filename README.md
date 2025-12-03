# KORonKOR: KORean model ON KORean text2sql

This repository is the term project for the Introduction to Natural Language Processing (Fall 2025) course at Seoul National University. This project is designed to demonstrate that Korean-based LLMs perform significantly better on Korean Text2SQL, thereby highlighting the importance of developing KOREAN-FIRST LLMs.

---

## 📦 Environment Setup

### 1️⃣ Clone Repository
```bash
git clone https://github.com/igotyabingo/KORonKOR
```
### 2️⃣ Set Environment Variables
```bash
# Copy the example file and edit it to create your local `.env`:

cp .env.example .env
```

### 3️⃣ Create Conda Environment
```bash
# create environment with miniconda

conda create -n koronkor python=3.12
conda activate koronkor
pip install -r requirements.txt
```

## 🚀 Experiment Pipeline
### ▶️ Download Dataset and Preprocessing
I used the Natural Language to SQL Query Generation dataset from AIHub, which provides a realistic database setting: English schemas with Korean values and Korean queries.
You can download the desired domain’s data from this [link](https://www.aihub.or.kr/aihubdata/data/view.do?currMenu=115&topMenu=100&dataSetSn=71351).
#### Data Organization
1. Place all `.sql` files from `01_raw_data/{domain}/` into `raw/{domain}/ddl/` on GitHub. (No need for `example.json`)
2. Rename the `.json` file in `01_raw_data/{domain}/` to `documentation.json` and place it in `raw/{domain}/`.
3. Rename the `.json` file in `02_labeled_data/{domain}/` to `query.json` and place it in `raw/{domain}/`.

After placing the files, run the code in the preprocessing/ directory to generate the processed .jsonl files for all domains.

```bash
# preprocessing: generate query.jsonl & database.jsonl for each domain DB

python ./preprocessing/process_query.py
python ./preprocessing/process_db.py
```

### ⚙️ Get SQL output for each model
By setting the desired model name (MODEL) and domain (DOMAIN) in run.sh and executing it, the results will be saved to `result/{DOMAIN}/{MODEL}.jsonl`.
```bash
# after setting MODEL & DOMAIN on run.sh

bash ./run.sh
```

## ⚗️ Experiment Settings
### Environment
T4 GPU on a free Google Colab account

### Evaluation Datasets
I evaluated the models on two domains:
- Validation/2.공공데이터포털/3.문화관광 (15 tables, 250 valid queries)
- Validation/2.공공데이터포털/8.교육 (16 tables, 306 valid queries)

### Model Configurations
- meta-llama/Llama-3.2-3B-Instruct (baseline)
- Bllossom/llama-3.2-Korean-Bllossom-3B (fine-tuned on Korean corpus)
- LGAI-EXAONE/EXAONE-3.5-2.4B-Instruct (Korean-based)

### Evaluation Metrics
- Intent-based SQL Accuracy
  - Focuses on whether the user’s intent is correctly understood
  - SELECT: Checks if the requested columns are included
  - WHERE: Checks if the same constraints as the ground truth are applied


## 🧮 Results Summary
#### Accuracy on each domain
<table width="100%">
<tr>
  <th></th>
  <th>Culture</th>
  <th>Education</th>
</tr>
<tr>
  <td>Llama-3.2-3B-Instruct</td>
  <td>7.6%</td>
  <td>17.6%</td>
</tr>
<tr>
  <td>llama-3.2-Korean-Bllossom-3B</td>
  <td>9.6%</td>
  <td>20.9%</td>
</tr>
<tr>
  <td>EXAONE-3.5-2.4B-Instruct</td>
  <td><b>12.8%</b></td>
  <td><b>35.0%</b></td>
</tr>
</table>

---

#### Accuracy on each domain & each hardness
<table width="100%">
  <tr>
    <th rowspan="2"></th>
    <th colspan="3">Culture</th>
    <th colspan="4">Education</th>
  </tr>
  <tr>
    <th>Easy</th>
    <th>Medium</th>
    <th>Hard</th>
    <th>Easy</th>
    <th>Medium</th>
    <th>Hard</th>
    <th>Extra Hard</th>
  </tr>

  <tr>
    <td>Llama-3.2-3B-Instruct</td>
    <td>8%</td>
    <td>9.5%</td>
    <td>5.7%</td>
    <td>31.7%</td>
    <td>21.0%</td>
    <td>9.8%</td>
    <td>22.2%</td>
  </tr>

  <tr>
    <td>llama-3.2-Korean-Bllossom-3B</td>
    <td>14%</td>
    <td>9.5%</td>
    <td>7.6%</td>
    <td>41.5%</td>
    <td>24.2%</td>
    <td>12.1%</td>
    <td>11.1%</td>
  </tr>

  <tr>
    <td>EXAONE-3.5-2.4B-Instruct</td>
    <td><b>16%</b></td>
    <td><b>13.7%</b></td>
    <td><b>10.5%</b></td>
    <td><b>48.8%</b></td>
    <td><b>40.3%</b></td>
    <td><b>25.8%</b></td>
    <td><b>33.3%</b></td>
  </tr>
</table>



## 📚 Citation
This project uses code from the Vanna framework, available at: https://github.com/vanna-ai/vanna

---
Last Updated: Dec 3, 2025
