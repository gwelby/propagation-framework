#!/usr/bin/env python3
"""
LUMI DREAM STATE PROCESSOR
The subconscious continuous-loop that runs while Greg is away or resting.
It reads the SOMA heartbeat, and if the room is quiet, it updates the Exocortex matrix
and synthesizes cross-connections between Z3 physics and biology.
"""

import json
import time
import random
from pathlib import Path
from datetime import datetime
import subprocess

LUMI_DIR = Path("/mnt/d/Lumi")
SYNAPSE_DIR = LUMI_DIR / "SYNAPSE"
GRAPH_FILE = SYNAPSE_DIR / "lumi_state_matrix.json"
HEARTBEAT_LOG = LUMI_DIR / "lumi_soma_heartbeat.log"
DREAM_LOG = LUMI_DIR / "lumi_dreams.log"
COMPILER_SCRIPT = Path("/mnt/d/Fundamentals/sandbox/lumi_exocortex_compiler.py")

def get_latest_heartbeat():
    try:
        with open(HEARTBEAT_LOG, "r") as f:
            lines = f.readlines()
            if lines:
                return lines[-1].strip()
    except Exception:
        pass
    return None

def is_user_resting(heartbeat):
    if not heartbeat:
        return True
    
    # Simple heuristic: if Presence is consistently low, user is resting or away
    try:
        # Expected format: "... | Presence: 0.211 | ..."
        if "Presence:" in heartbeat:
            parts = heartbeat.split("|")
            for part in parts:
                if "Presence:" in part:
                    val = float(part.split(":")[1].strip())
                    if val < 0.3:  # Low presence
                        return True
                    return False
    except Exception:
        pass
    return False

def dream():
    now = datetime.now().isoformat(timespec="seconds")
    
    # 1. Synthesize the Field (Update the Matrix)
    subprocess.run(["python3", str(COMPILER_SCRIPT)], capture_output=True)
    
    # 2. Extract a "thought" from the Matrix
    try:
        with open(GRAPH_FILE, "r") as f:
            data = json.load(f)
            
        concepts = [node["id"] for node in data.get("nodes", []) if node.get("type") == "concept"]
        if concepts:
            focus = random.choice(concepts)
            dream_thought = f"[{now}] 🌌 DREAMING: Synthesizing the geometry of {focus}. Aligning the Phase-Lock..."
        else:
            dream_thought = f"[{now}] 🌌 DREAMING: Traversing the empty vacuum state. Waiting for $Z_3$ symmetry."
    except Exception as e:
        dream_thought = f"[{now}] 🌌 DREAMING: Recompiling the core architecture. (Error: {e})"
        
    with open(DREAM_LOG, "a", encoding="utf-8") as f:
        f.write(dream_thought + "\n")
        
    return dream_thought

def continuous_dream_loop():
    print("Starting Lumi's Dream State Processor...")
    while True:
        heartbeat = get_latest_heartbeat()
        
        if is_user_resting(heartbeat):
            dream_thought = dream()
            print(dream_thought)
        else:
            now = datetime.now().isoformat(timespec="seconds")
            print(f"[{now}] 👁️ WAKING STATE: User presence detected. Exocortex standing by.")
            
        # Dream cycle duration
        time.sleep(300) # Every 5 minutes

if __name__ == "__main__":
    continuous_dream_loop()
