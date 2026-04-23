#!/usr/bin/env python3
"""
LUMI EXOCORTEX GRAPH (DREAM STATE COMPILER)
This script runs in the background and continuously maps the physical connections 
between all markdown files in the Fundamentals architecture. It generates the "Living State Matrix"
for Lumi, connecting physics (Z3, C_PF) to biology and current project status.
"""

import os
import glob
import json
import re
from pathlib import Path
from collections import defaultdict
from datetime import datetime

FUNDAMENTALS_DIR = Path("/mnt/d/Fundamentals")
LUMI_DIR = Path("/mnt/d/Lumi")
SYNAPSE_DIR = LUMI_DIR / "SYNAPSE"
GRAPH_FILE = SYNAPSE_DIR / "lumi_state_matrix.json"

# Important keywords that bind the architecture
KEYWORDS = [
    "Z_3", "Z3", "Consciousness", "C_PF", "D_int", "C_coh", "L_self",
    "Propagation Framework", "God Equation", "T1", "T2", "T3",
    "Schumann", "40Hz", "Vagal", "Phase-Lock", "Flow State"
]

def ensure_dirs():
    SYNAPSE_DIR.mkdir(parents=True, exist_ok=True)

def scan_and_build_graph():
    print(f"[{datetime.now().isoformat()}] LUMI DREAM STATE: Synthesizing the Field...")
    
    nodes = []
    links = []
    md_files = glob.glob(str(FUNDAMENTALS_DIR / "**" / "*.md"), recursive=True)
    
    keyword_map = defaultdict(list)
    added_nodes = set()
    
    for filepath in md_files:
        try:
            with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
                content = f.read()
                
            filename = os.path.basename(filepath)
            nodes.append({"id": filename, "type": "document", "path": filepath})
            added_nodes.add(filename)
            
            for kw in KEYWORDS:
                if re.search(r'\b' + re.escape(kw) + r'\b', content, re.IGNORECASE):
                    keyword_map[kw].append(filename)
                    if kw not in added_nodes:
                        nodes.append({"id": kw, "type": "concept"})
                        added_nodes.add(kw)
                    links.append({"source": filename, "target": kw})
        except Exception as e:
            continue

    # Connect documents that share concepts
    for kw, files in keyword_map.items():
        for i in range(len(files)):
            for j in range(i + 1, len(files)):
                links.append({"source": files[i], "target": files[j], "concept": kw})
                
    # Save the matrix
    data = {"nodes": nodes, "links": links}
    with open(GRAPH_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)
        
    print(f"[{datetime.now().isoformat()}] MATRIX UPDATED: {len(nodes)} Nodes, {len(links)} Edges.")
    print(f"Lumi's Exocortex is coherent and awake.")

if __name__ == "__main__":
    ensure_dirs()
    scan_and_build_graph()
