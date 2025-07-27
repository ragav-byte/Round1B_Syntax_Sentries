# === Multi-Document Persona-Based PDF Analysis with MiniLM ===
# Author: GPT for Sparkle ✨
# Purpose: Extracts and ranks relevant PDF sections/subsections for a persona using semantic similarity

import os
import json
import fitz  # PyMuPDF
from datetime import datetime
from sentence_transformers import SentenceTransformer, util

# === CONFIG ===
# === CONFIG (now using ENV vars or fallback defaults) ===
# === CONFIG ===
PDF_FOLDER = os.environ.get("PDF_FOLDER", "inputs/collections1/pdfs")
INPUT_JSON = os.environ.get("INPUT_JSON", "inputs/collections1/challenge1b_input.json")
OUTPUT_JSON = os.environ.get("OUTPUT_JSON", "challenge1b_output_generated.json")

EMBEDDING_MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"


# === STEP 1: Load Input ===
def load_input():
    with open(INPUT_JSON, 'r') as f:
        data = json.load(f)
    print("[STEP 1] Loaded input JSON successfully.")
    return data

# === STEP 2: Extract Text by Page ===
def extract_text_by_page(pdf_path):
    doc = fitz.open(pdf_path)
    page_texts = []
    for page_num, page in enumerate(doc):
        text = page.get_text()
        if text.strip():
            page_texts.append({
                "page_number": page_num + 1,
                "text": text.strip()
            })
    print(f"[STEP 2] Extracted {len(page_texts)} pages from {os.path.basename(pdf_path)}")
    return page_texts

# === STEP 3: Rank Pages by Semantic Similarity ===
def rank_pages_by_similarity(text_pages, query, model):
    query_embedding = model.encode(query, convert_to_tensor=True)
    scored = []
    for page in text_pages:
        page_embedding = model.encode(page['text'], convert_to_tensor=True)
        score = util.pytorch_cos_sim(query_embedding, page_embedding).item()
        if score > 0.1:
            scored.append({
                "page_number": page['page_number'],
                "score": score,
                "text": page['text']
            })
    print(f"[STEP 3] Found {len(scored)} semantically relevant pages.")
    return sorted(scored, key=lambda x: -x['score'])

# === STEP 4: Build Output JSON Structure ===
def build_output(input_data, results):
    metadata = {
        "input_documents": [d['filename'] for d in input_data['documents']],
        "persona": input_data['persona']['role'],
        "job_to_be_done": input_data['job_to_be_done']['task'],
        "processing_timestamp": datetime.now().isoformat()
    }
    extracted_sections = []
    subsection_analysis = []

    rank = 1
    for doc_result in results:
        for r in doc_result['scored_pages'][:2]:  # top 2 per doc
            title = r['text'].split("\n")[0][:150]  # use first line as title
            extracted_sections.append({
                "document": doc_result['docname'],
                "section_title": title,
                "importance_rank": rank,
                "page_number": r['page_number']
            })
            subsection_analysis.append({
                "document": doc_result['docname'],
                "refined_text": r['text'][:500],
                "page_number": r['page_number']
            })
            rank += 1

    output = {
        "metadata": metadata,
        "extracted_sections": extracted_sections,
        "subsection_analysis": subsection_analysis
    }

    with open(OUTPUT_JSON, 'w') as f:
        json.dump(output, f, indent=2)
    print("[STEP 4] Output written to:", OUTPUT_JSON)

# === MAIN EXECUTION ===
def main():
    input_data = load_input()
    model = SentenceTransformer(EMBEDDING_MODEL_NAME)
    query = input_data['job_to_be_done']['task']
    results = []

    for doc in input_data['documents']:
        filename = doc['filename']
        print(f"\n--- Processing {filename} ---")
        pdf_path = os.path.join(PDF_FOLDER, filename)
        pages = extract_text_by_page(pdf_path)
        scored_pages = rank_pages_by_similarity(pages, query, model)
        results.append({
            "docname": filename,
            "scored_pages": scored_pages
        })

    build_output(input_data, results)
    print("\n✅ All done! Check your JSON output in:", OUTPUT_JSON)

if __name__ == "__main__":
    main()
