import os
import glob
import json
import uuid
import re
from datetime import datetime

base_dir = r"D:\Fundamentals"
files_to_read = [
    os.path.join(base_dir, "the_propagation_framework.md"),
    os.path.join(base_dir, "theory_of_propagation.md"),
    os.path.join(base_dir, "sandbox_results.md"),
    os.path.join(base_dir, "derivations", "topological_weight_from_propagation.md")
]

for path in glob.glob(os.path.join(base_dir, "RESEARCH", "*", "MASTER.md")):
    files_to_read.append(path)

output_dir = r"D:\Harmonia\nexus_mundi\knowledge_library\entries"
os.makedirs(output_dir, exist_ok=True)

def determine_frequency(chunk_text, source_file):
    text_lower = chunk_text.lower()
    
    if "open gap" in text_lower or "speculat" in text_lower or "unsupported" in text_lower or "hypothesis" in text_lower:
        return "vision" # 720Hz
    elif "derive" in text_lower or "equation" in text_lower or "math" in text_lower or "impedance" in text_lower or "formula" in text_lower:
        return "unity" # 432Hz
    elif "claim" in text_lower or "axiom" in text_lower or "truth" in text_lower or "fundamental" in text_lower:
        return "truth" # 672Hz
    elif "synthesis" in text_lower or "integrat" in text_lower or "framework" in text_lower:
        return "cascade" # 594Hz
    elif "insight" in text_lower or "creat" in text_lower or "new" in text_lower:
        return "love" # 528Hz
    else:
        if "topological_weight" in source_file or "theory" in source_file:
            return "unity"
        elif "sandbox" in source_file:
            return "truth"
        elif "MASTER" in source_file:
            return "cascade"
        return "unity"

def chunk_text(text, max_words=400):
    paragraphs = text.split("\n\n")
    chunks = []
    current_chunk = []
    current_words = 0
    
    for p in paragraphs:
        p = p.strip()
        if not p: continue
        words = len(p.split())
        if current_words + words > max_words and current_chunk:
            chunks.append("\n\n".join(current_chunk))
            current_chunk = [p]
            current_words = words
        else:
            current_chunk.append(p)
            current_words += words
            
    if current_chunk:
        chunks.append("\n\n".join(current_chunk))
        
    return chunks

def process_file(filepath):
    if not os.path.exists(filepath):
        print(f"Warning: {filepath} not found.")
        return

    with open(filepath, 'r', encoding='utf-8', errors='replace') as f:
        content = f.read()

    chunks = chunk_text(content)
    count = 0
    for chunk in chunks:
        # Ignore very short chunks unless they're the only one
        if len(chunk.split()) < 10:
            continue
        freq = determine_frequency(chunk, filepath)
        entry_id = str(uuid.uuid4())
        
        entry = {
            "knowledge_id": entry_id,
            "content": chunk,
            "primary_frequency": freq,
            "secondary_frequencies": ["cascade"] if freq != "cascade" else ["unity"],
            "coherence": 0.618033988749895,
            "metadata": {
                "source": os.path.relpath(filepath, base_dir),
                "confidence": 0.95 if freq == "truth" else (0.75 if freq == "vision" else 0.85),
                "created_at": datetime.now().isoformat()
            }
        }
        
        out_path = os.path.join(output_dir, f"{entry_id}.json")
        with open(out_path, 'w', encoding='utf-8') as f:
            json.dump(entry, f, indent=2)
        count += 1
    print(f"Processed {filepath} -> {count} entries")

def main():
    existing_files = glob.glob(os.path.join(output_dir, "*.json"))
    for f in existing_files:
        try:
            os.remove(f)
        except Exception as e:
            pass

    for f in files_to_read:
        process_file(f)
        
    print(f"Done. Generated {len(glob.glob(os.path.join(output_dir, '*.json')))} entries in {output_dir}")

if __name__ == '__main__':
    main()
