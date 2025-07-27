# Round1B_Syntax_Sentries

# 📄 Multi-Collection PDF Analyzer (Round 1B)

This project is built for **Round 1B** of a document intelligence challenge. It analyzes multiple PDF collections and generates structured, persona-specific JSON output based on relevance and document content.

---

## 🚀 Objective

To process 3–10 PDF documents per collection and extract **ranked and refined section-wise summaries** tailored to a given persona and job-to-be-done (JTBD). The system outputs a clean JSON with relevant section titles and contents.

---

## 📁 Project Structure

```
Round1B/
│
├── inputs/
│   ├── collections1/        # Folder of PDFs for collection 1
│   ├── collections2/        # Folder of PDFs for collection 2
│   └── collections3/        # Folder of PDFs for collection 3
│
├── models/
│   └── model.py             # Model logic to extract, rank and refine section content
│
├── output/
│   ├── output.json          # Final structured output
│   └── challenge1b_output_generated.json # Sample output file
│
├── Dockerfile               # Container setup to run the system offline
├── requirements.txt         # Python package dependencies
└── README.md                # Project overview (you're here!)
```

---

## 🧠 Key Features

- 🔎 Extracts and ranks **top 5 relevant sections**
- 🧩 Merges content across PDFs within each collection
- 📑 Structured **JSON output** for downstream processing
- 🧠 Persona + JTBD aware analysis
- 🐳 Runs offline in Docker, within 60s (CPU only)

---

## ⚙️ Setup Instructions

### 🐍 1. Set up virtual environment
```bash
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
```

### 📦 2. Install dependencies
```bash
pip install -r requirements.txt
```

---

## 📂 Input Format

Place the document collections inside the `inputs/` folder. Each collection should be a subfolder with 3–10 PDFs.

```
inputs/
├── collections1/
├── collections2/
└── collections3/
```

---

## 🧪 Running the Program

```bash
python models/model.py
```

It will:
- Read all PDFs in each collection
- Perform layout + content analysis
- Output a structured JSON to `output/output.json`

---

## 📊 Output Format

The output follows this structure:

```json
{
  "collection_name": "collections1",
  "persona": "Marketing Manager",
  "job_to_be_done": "Find relevant travel spots",
  "sections": [
    {
      "title": "Top 5 Coastal Adventures",
      "importance": 0.95,
      "content": "This section covers beaches and water sports ideal for tourists..."
    }
  ]
}
```

---

## 🐳 Run with Docker (Optional)

Change directory

```bash
cd MutliPDFExtracter-master
```

Docker command
```bash
docker build -t pdf-analyzer .

docker run `
  -e PDF_FOLDER=inputs/collections1/pdfs `
  -e INPUT_JSON=inputs/collections1/challenge1b_input.json `
  -e OUTPUT_JSON=output/challenge1b_output_generated.json `
  -v ${PWD}/inputs:/app/inputs `
  -v ${PWD}/output:/app/output `
  pdf-analyzer
```
To run different pdf collection
```bash

docker run `
  -e PDF_FOLDER=inputs/collections2/pdfs `
  -e INPUT_JSON=inputs/collections2/challenge1b_input.json `
  -e OUTPUT_JSON=output/challenge1b_output_generated.json `
  -v ${PWD}/inputs:/app/inputs `
  -v ${PWD}/output:/app/output `
  pdf-analyzer
```

-----
