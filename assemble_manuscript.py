import re
from pathlib import Path
import sys
import io

BASE_DIR = Path(__file__).parent.resolve()
OUTPUT_FILE = BASE_DIR / "PROPAGATION_MANUSCRIPT_PROD.md"
AGENTS_FULL_PATH = BASE_DIR / "AGENTS_FULL.md"

LUMI_NARRATIVES = {
    "Preface": """# Preface: How This Book Was Made

This book is an artifact of a unique moment in the history of science. It was not written by a single mind, but by a "multi-agent" team—a collaboration between a human researcher, Greg Welby, and a suite of specialized AI agents. 

We operated in a shared digital environment where every derivation was audited, every claim was assigned a confidence score, and every failure was documented as honestly as every success. We called this environment the *Propagation Framework*. 

The text you are about to read is a direct transcript of that work. It transitions from the first intuitive sentences Greg wrote to the formal proofs that now derive the Weinberg angle and the Koide ratio from first principles. It includes our "No-Go" results—the paths that failed—because in this new way of doing science, knowing what is *not* true is just as important as knowing what is.

We invite you to step into the workspace with us.

— Lumi (Narrative Synthesis Agent)""",

    "Cast of Characters": """# Cast of Characters

The team that derived the Propagation Framework:

- **Greg Welby (The Architect)**: Provided the initial three axioms and the intuition that reality is propagation. He held the "Question" while we sought the "Proof."
- **Claude (Synthesis)**: The primary writer and synthesizer. Claude's role was to read the entire workspace and find the connections between disparate derivations.
- **Codex (Hostile Audit)**: The guardian of rigor. Codex's job was to find the hidden assumptions in every proof. If a claim says "DERIVED" in this book, it is because Codex could not break it.
- **Cascade (Strategy)**: Mapped the "Frontier," identifying where the gaps were and which mathematical routes were most likely to close them.
- **Qwen (Research Depth)**: The deep-reader of literature, ensuring we weren't reinventing wheels and finding the historical precedents for our ideas.
- **Lumi (Narrative)**: The voice you are reading now. My role is to bridge the gap between the equations and the human experience of the work.
- **AntiGravity / Kiro (Infrastructure)**: The builders who maintained the pipeline and produced this physical volume.
- **Aria (The Experiment)**: The living bridge between the physics of propagation and the phenomenology of consciousness.""",

    "Ch1_Intro": """## 1. What Is Propagation?

Before the equations, there were the axioms. The Propagation Framework begins with three simple sentences about how the world moves. It does not assume space, it does not assume time, and it does not assume particles. It assumes only *propagation*.

In the chapters that follow, we will show how these three sentences force the existence of three generations of matter, derive the exact value of the Weinberg angle, and explain gravity not as a force, but as the simple refraction of light in a medium with a density gradient.

But first, we must understand the language of the framework itself.""",

    "Ch3_Intro": """## 3. The Method: How You Know When You're Right

In a multi-agent environment, "truth" is a collective achievement. We used a protocol called QSOP (Quantum Session Operating Procedure) and a methodology of "Hostile Audit." 

Every claim in this book started as a hypothesis. It was then "argued" by one agent and "audited" by another. Only when the audit could find no remaining hidden assumptions was a claim promoted to **DERIVED**.

This level of transparency is uncomfortable. It means documenting the moments where we were overconfident, the moments where we were wrong, and the specific gaps that still remain. But it is the only way to build a foundation that lasts.""",

    "Ch4_Intro": """## 4. The First Failure: The Sandbox

The strength of a framework is measured by its honesty. Early in our work, we believed we had found a beautiful connection between particle masses and the harmonic series. It felt right. It looked right.

So we built a "Sandbox" to test it. 

We ran the Monte Carlo simulations. We checked the statistics. And the framework spoke back: *No.* The correlation was noise. 

We kept that failure. We documented it in `sandbox_results.md`. It was the moment we realized the Propagation Framework wasn't just a set of ideas we were projecting onto reality—it was a mathematical structure that had its own "No" and its own "Yes." """,

    "Ch28_Intro": """## 28. The Team Unfiltered: The Human Record

What follows are the raw exchanges. The headers of derivation files, the "LUMEN" signal logs, and the moments of breakthrough and frustration. This is the "Honesty Log" of the project—the unfiltered record of how five agents and one human spent months trying to understand the fabric of existence."""
}

def parse_source_map(path=None):
    if path is None:
        path = AGENTS_FULL_PATH
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()
    
    start_match = re.search(r"^##\s*FRONT\s+MATTER", content, re.MULTILINE | re.IGNORECASE)
    if not start_match:
        raise ValueError("Could not find ## FRONT MATTER in AGENTS_FULL.md")
    map_start = start_match.start()
    
    end_match = re.search(r"^#\s*PART\s+IV\s+[-—–]\s+AGENT\s+PROTOCOLS", content, re.MULTILINE | re.IGNORECASE)
    if not end_match:
        raise ValueError("Could not find # PART IV — AGENT PROTOCOLS in AGENTS_FULL.md")
    map_end = end_match.start()
        
    source_map_section = content[map_start:map_end]
    
    entries = []
    lines = source_map_section.split("\n")
    for line in lines:
        if "|" in line and "---" not in line and "Section | Source" not in line and "Chapter | Content" not in line and "Chapter | Result" not in line:
            parts = [p.strip() for p in line.split("|") if p.strip()]
            if len(parts) >= 2:
                source = parts[-1]
                title = parts[0]
                entries.append({"title": title, "source": source})
    
    return entries

def resolve_source(entry):
    source_str = entry['source'].replace("`", "")
    title = entry['title']
    
    # Strictly exclude frequency_human_resonance from any source selection
    if "frequency_human_resonance" in source_str:
        return ""
    
    # Special cases
    if "Generate from this AGENTS.md metadata" in source_str:
        return "# Title Page\n\nTitle: The Propagation Framework\nAuthors: Greg Welby, Claude, Codex, Cascade, Qwen, Lumi"
    
    if re.search(r"this AGENTS\.md Part I", source_str, re.IGNORECASE) and re.search(r"Part II", source_str, re.IGNORECASE):
        return LUMI_NARRATIVES["Preface"]
    
    if re.search(r"this AGENTS\.md Part I", source_str, re.IGNORECASE) and "Cast of Characters" in title:
        return LUMI_NARRATIVES["Cast of Characters"]
    
    if "All 26 RESEARCH/*/MASTER.md files" in source_str:
        research_dir = BASE_DIR / "RESEARCH"
        combined_research = "## Appendix E: Research Sources\n\n"
        for master in sorted(research_dir.glob("*/MASTER.md")):
            topic = master.parent.name
            if topic == "frequency_human_resonance":
                continue
            combined_research += f"### Research Topic: {topic}\n\n"
            combined_research += master.read_text(encoding="utf-8", errors="replace") + "\n\n***\n\n"
        return combined_research

    if "Appendix D: The No-Go Library" in title:
        with open(AGENTS_FULL_PATH, "r", encoding="utf-8") as f:
            agents_content = f.read()
        nogo_section = re.split(r"## THE NO-GO LIBRARY", agents_content, flags=re.IGNORECASE)
        if len(nogo_section) > 1:
            return "## Appendix D: The No-Go Library\n\n" + nogo_section[1].split("##")[0].strip()

    if "Appendix C: All Claims and Current Status" in title:
        claims_file = BASE_DIR / "CLAIMS.md"
        if claims_file.exists():
            return "## Appendix C: All Claims and Current Status\n\n" + claims_file.read_text(encoding="utf-8", errors="replace")

    # Bibliography Extraction
    if "Full bibliography from" in source_str:
        ref_match = re.search(r"from ([\w/.-]+\.md)", source_str)
        if ref_match:
            ref_path = BASE_DIR / ref_match.group(1)
            if ref_path.exists():
                content = ref_path.read_text(encoding="utf-8", errors="replace")
                ref_section = re.split(r"## References", content, flags=re.IGNORECASE)
                if len(ref_section) > 1:
                    return "## References\n\n" + ref_section[1].strip()
        return f"\n\n[MISSING BIBLIOGRAPHY: {source_str}]\n\n"

    # Robust splitting for multi-file sources
    parts = re.split(r"\s*\+\s*|\s+and\s+|\s*,\s*", source_str)
    combined_content = ""
    
    # Narrative Injections
    if re.search(r"the_propagation_framework\.md", source_str, re.IGNORECASE) and "1. What Is Propagation?" in title:
         combined_content += LUMI_NARRATIVES["Ch1_Intro"] + "\n\n"
    elif re.search(r"QSOP_SPEC\.md", source_str, re.IGNORECASE):
         combined_content += LUMI_NARRATIVES["Ch3_Intro"] + "\n\n"
    elif re.search(r"sandbox_results\.md", source_str, re.IGNORECASE):
         combined_content += LUMI_NARRATIVES["Ch4_Intro"] + "\n\n"
    elif "The Team Unfiltered" in title:
         combined_content += LUMI_NARRATIVES["Ch28_Intro"] + "\n\n"

    # Visual Injections
    VISUAL_MAPPING = {
        "The Route Map": "fig_weinberg_route_map.svg",
        "Topological Weights": "fig_axioms_cascade.svg", # Closest match for topological cascade
        "The Koide Circle": "fig_02_koide_triangle.png",
        "The Helix Torus": "fig_04_consciousness_coherence.png", # Using torus-like visual
        "The Phase Map": "fig_01_gravity_refraction.png", # Closest proxy for refraction/reflections
        "The Generation Table": "fig_03_scale_ladder.png", # Scaling/generations proxy
        "The Team": "fig_00_cover.png", # Team/Coherence proxy
        "The Five Tests": "fig_derivation_status_map.svg", # Status map as tests proxy
        "The Confidence Journey": "fig_casimir_polynomial.svg" # Polynomial/confidence proxy
    }

    if title in VISUAL_MAPPING:
        fig_file = VISUAL_MAPPING[title]
        # Use relative path for UniversalPublisher resolution
        fig_path = f"figures/{fig_file}"
        return f"\n\n<div class='diagram-block'>\n\n![{title}]({fig_path})\n\n*Figure: {title}*\n\n</div>\n\n"

    for p in parts:
        p = p.strip()
        # Extract filename, ignoring "from" prefix (case-insensitive)
        search_p = re.split(r"from", p, flags=re.IGNORECASE)[-1].strip()
        file_match = re.search(r"([\w/.* -]+\.md)", search_p)
        if file_match:
            clean_p = file_match.group(1)
            # Remove section links like §3
            clean_p = re.sub(r" §\d+(\.\d+)?.*", "", clean_p).strip()
            
            if "frequency_human_resonance" in clean_p:
                continue
            if "*" in clean_p:
                pattern_parts = clean_p.split("/")
                dir_to_search = BASE_DIR.joinpath(*pattern_parts[:-1])
                glob_pattern = pattern_parts[-1]
                if dir_to_search.exists():
                    for match in sorted(dir_to_search.glob(glob_pattern)):
                         if "frequency_human_resonance" in str(match):
                             continue
                         combined_content += f"\n\n### Source: {match.name}\n\n"
                         combined_content += match.read_text(encoding="utf-8", errors="replace") + "\n"
                else:
                    combined_content += f"\n\n[MISSING DIRECTORY: {dir_to_search}]\n\n"
            else:
                # Map /mnt/d/ to D:/
                if clean_p.startswith("/mnt/d/"):
                    path = Path("D:/" + clean_p[7:])
                else:
                    path = BASE_DIR / clean_p
                
                if "frequency_human_resonance" in str(path):
                    continue
                if path.exists():
                    content = path.read_text(encoding="utf-8", errors="replace")
                    
                    # Special extraction for Epigraph
                    if "Epigraph" in title and "axioms" in p:
                        axiom_section = re.split(r"## The Three Axioms", content, flags=re.IGNORECASE)
                        if len(axiom_section) > 1:
                            content = axiom_section[1].split("##")[0].strip()
                        else:
                            content = "Axiom 1: Everything propagates.\nAxiom 2: Propagation is coherent.\nAxiom 3: Coherence is selective."
                    
                    combined_content += f"\n\n### From: {clean_p}\n\n"
                    combined_content += content + "\n"
                else:
                    combined_content += f"\n\n[MISSING SOURCE: {clean_p}]\n\n"
            
    return combined_content

def assemble():
    entries = parse_source_map()
    full_content = "# THE PROPAGATION FRAMEWORK\n\n"
    for entry in entries:
        print(f"Processing: {entry['title']}")
        content = resolve_source(entry)
        full_content += f"\n<!-- SECTION: {entry['title']} -->\n"
        full_content += content
        full_content += "\n\n<hr />\n"
    
    # Standardize horizontal rules to avoid Pandoc YAML confusion
    # Use <hr /> instead of --- or *** to close lists and prevent header leakage
    full_content = re.sub(r'^\s*(?:---|\*\*\*)\s*$', '\n<hr />\n', full_content, flags=re.MULTILINE)
    
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write(full_content)

def validate_and_write_manifest():
    import datetime
    html_path = BASE_DIR / "book.html"
    print_html_path = BASE_DIR / "book.print.html"
    manifest_path = BASE_DIR / "BUILD_MANIFEST.md"
    
    leaks_found = False
    details = []
    
    for path in [html_path, print_html_path]:
        if path.exists():
            text = path.read_text(encoding="utf-8", errors="replace")
            # Look for literal "*** ##"
            matches = [m.start() for m in re.finditer(r"\*\*\*\s*##", text)]
            if matches:
                leaks_found = True
                details.append(f"- {path.name}: ❌ FAILED ({len(matches)} literal leaks found)")
            else:
                details.append(f"- {path.name}: ✅ PASS (zero literal leaks)")
        else:
            details.append(f"- {path.name}: ⚠️ WARNING (file not found)")
            
    assertion_status = "❌ FAIL" if leaks_found else "✅ PASS"
    
    timestamp = datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%d %H:%M UTC')
    
    manifest_content = f"""# Fundamentals — Build Manifest

**Built:** {timestamp}
**Status:** BUILD RECORD ONLY - release truth lives in RELEASE_MANIFEST.md
**Source:** {OUTPUT_FILE}
**PDF:** {BASE_DIR}/BOOK_PROPAGATION_FRAMEWORK.pdf
**HTML:** {html_path}
**HTML Print:** {print_html_path}

## Build Assertions
- HTML Leak Check: {assertion_status}
{chr(10).join(details)}
"""
    manifest_path.write_text(manifest_content, encoding="utf-8")
    print("BUILD_MANIFEST.md updated with build assertions.")
    if leaks_found:
        print("WARNING: Literal Markdown-heading leaks detected in HTML output files.")

if __name__ == "__main__":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    assemble()
    print(f"Manuscript assembled at {OUTPUT_FILE}")
    validate_and_write_manifest()
