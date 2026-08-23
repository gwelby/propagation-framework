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

def extract_section(content, selector):
    """Extract a specific section from markdown content by selector.
    
    Supports:
    - §N or §N.M — extract section "## N" or "### N.M" up to next same/higher heading
    - §N intro — extract section N, only up to first ### subsection
    - TEST N — extract "### TEST N — ..." up to next ### or ## heading
    - Appendix A — extract "## Appendix A" up to next ## heading
    - Appendix A+B — extract both Appendix A and Appendix B
    - Sections N-M — extract sections N through M inclusive
    - §N expanded — extract section N (allow expansion, still just that section)
    
    Returns None if selector is None/empty. Returns "[SECTION NOT FOUND]" if
    the requested section cannot be located (fail-loud, not silent whole-file).
    """
    if not selector:
        return None
    
    lines = content.split("\n")
    
    # Parse the selector
    # Pattern: §N.M, §N, §N intro, §N expanded, TEST N, Appendix X, Appendix X+Y, Sections N-M
    sec_match = re.match(r"§(\d+)(?:\.(\d+))?(?:\s+(intro|expanded))?", selector)
    test_match = re.match(r"TEST\s+(\d+)", selector)
    appendix_match = re.match(r"Appendix\s+([A-Z])(?:\s*\+\s*([A-Z]))?", selector)
    sections_range_match = re.match(r"Sections\s+(\d+)[–-](\d+)", selector)
    
    if sec_match:
        major = sec_match.group(1)
        minor = sec_match.group(2)
        modifier = sec_match.group(3)
        
        if minor:
            # §N.M — find ### N.M
            target_pattern = re.compile(rf"^###\s+{re.escape(major)}\.{re.escape(minor)}\b")
            end_pattern = re.compile(r"^##\s+")  # ends at next ## or ###
        else:
            # §N — find ## N
            target_pattern = re.compile(rf"^##\s+{re.escape(major)}\b")
            if modifier == "intro":
                # §N intro — only up to first ### subsection
                end_pattern = re.compile(r"^###\s+")
            else:
                end_pattern = re.compile(r"^##\s+")  # ends at next ##
        
    elif test_match:
        test_num = test_match.group(1)
        target_pattern = re.compile(rf"^###\s+TEST\s+{re.escape(test_num)}\b")
        end_pattern = re.compile(r"^###\s+")  # ends at next ### or ##
        
    elif appendix_match:
        letters = [appendix_match.group(1)]
        if appendix_match.group(2):
            letters.append(appendix_match.group(2))
        
        result_parts = []
        for letter in letters:
            target = re.compile(rf"^##\s+Appendix\s+{re.escape(letter)}\b")
            end = re.compile(r"^##\s+")
            section_lines = _extract_heading_block(lines, target, end)
            if section_lines is None:
                return "[SECTION NOT FOUND: Appendix " + letter + "]"
            result_parts.append("\n".join(section_lines))
        return "\n\n".join(result_parts)
        
    elif sections_range_match:
        start_n = int(sections_range_match.group(1))
        end_n = int(sections_range_match.group(2))
        result_parts = []
        for n in range(start_n, end_n + 1):
            target = re.compile(rf"^##\s+{n}\b")
            end = re.compile(r"^##\s+")
            section_lines = _extract_heading_block(lines, target, end)
            if section_lines is None:
                return f"[SECTION NOT FOUND: Section {n}]"
            result_parts.append("\n".join(section_lines))
        return "\n\n".join(result_parts)
    else:
        # Unknown selector format — fail loud, do NOT silently return whole file
        return f"[UNKNOWN SELECTOR FORMAT: {selector}]"
    
    section_lines = _extract_heading_block(lines, target_pattern, end_pattern)
    if section_lines is None:
        return f"[SECTION NOT FOUND: {selector}]"
    return "\n".join(section_lines)


def _extract_heading_block(lines, target_pattern, end_pattern):
    """Extract lines from the first target heading match to the first end heading.
    
    Returns None if target heading not found. Returns list of lines (including
    the target heading line itself) if found.
    """
    in_section = False
    result = []
    for line in lines:
        if not in_section:
            if target_pattern.match(line):
                in_section = True
                result.append(line)
                continue
        else:
            if end_pattern.match(line):
                break
            result.append(line)
    
    if not in_section:
        return None
    return result


def parse_selector(source_str):
    """Extract a section selector from a source string like 'file.md §6' or 'file.md TEST 1'.
    
    Returns the selector string (e.g. '§6', 'TEST 1', 'Appendix A+B') or None.
    """
    # §N.M with optional modifier
    m = re.search(r"§(\d+(?:\.\d+)?)(?:\s+(intro|expanded))?", source_str)
    if m:
        return m.group(0).strip()
    # TEST N
    m = re.search(r"TEST\s+\d+", source_str)
    if m:
        return m.group(0).strip()
    # Appendix X(+Y)?
    m = re.search(r"Appendix\s+[A-Z](?:\s*\+\s*[A-Z])?", source_str)
    if m:
        return m.group(0).strip()
    # Sections N-M
    m = re.search(r"Sections\s+\d+[–-]\d+", source_str)
    if m:
        return m.group(0).strip()
    return None


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
            # Parse and remove section selector (§N, TEST N, Appendix X, Sections N-M)
            selector = parse_selector(search_p)
            if selector:
                clean_p = re.sub(r"\s+" + re.escape(selector) + ".*", "", clean_p).strip()
            else:
                # Also strip trailing modifiers like "expanded", "intro" if no § prefix
                clean_p = re.sub(r"\s+(expanded|intro).*$", "", clean_p, flags=re.IGNORECASE).strip()
            
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
                    elif selector:
                        # Section selector — extract only the requested section
                        extracted = extract_section(content, selector)
                        if extracted is None:
                            combined_content += f"\n\n[SELECTOR PARSE ERROR: {selector} on {clean_p}]\n\n"
                            continue
                        elif extracted.startswith("[SECTION NOT FOUND") or extracted.startswith("[UNKNOWN SELECTOR"):
                            combined_content += f"\n\n### From: {clean_p} ({selector})\n\n{extracted}\n\n"
                            continue
                        else:
                            content = extracted
                    
                    combined_content += f"\n\n### From: {clean_p}"
                    if selector:
                        combined_content += f" ({selector})"
                    combined_content += "\n\n"
                    combined_content += content + "\n"
                else:
                    combined_content += f"\n\n[MISSING SOURCE: {clean_p}]\n\n"
            
    return combined_content

def assemble():
    entries = parse_source_map()
    full_content = "# THE PROPAGATION FRAMEWORK\n\n"
    
    # Duplicate-content control: track content fingerprints to detect
    # repeated insertion of identical blocks across source-map entries.
    # This catches assembler bugs where the same file/section is inserted
    # multiple times without deduplication.
    content_hashes = {}
    duplicate_warnings = []
    
    for entry in entries:
        print(f"Processing: {entry['title']}")
        content = resolve_source(entry)
        
        # Track content fingerprints for duplicate detection
        if content and len(content.strip()) > 100:
            import hashlib
            # Hash the stripped content (ignore whitespace differences)
            content_hash = hashlib.sha256(content.strip().encode("utf-8")).hexdigest()[:16]
            section_label = entry['title']
            if content_hash in content_hashes:
                duplicate_warnings.append(
                    f"  DUPLICATE: '{section_label}' has identical content to '{content_hashes[content_hash]}'"
                )
            else:
                content_hashes[content_hash] = section_label
        
        full_content += f"\n<!-- SECTION: {entry['title']} -->\n"
        full_content += content
        full_content += "\n\n<hr />\n"
    
    if duplicate_warnings:
        print("\n" + "=" * 60)
        print("DUPLICATE CONTENT WARNINGS:")
        for w in duplicate_warnings:
            print(w)
        print("=" * 60)
    
    # Standardize horizontal rules to avoid Pandoc YAML confusion
    # Use <hr /> instead of --- or *** to close lists and prevent header leakage
    full_content = re.sub(r'^\s*(?:---|\*\*\*)\s*$', '\n<hr />\n', full_content, flags=re.MULTILINE)
    
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write(full_content)
    
    return len(duplicate_warnings)

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
    dup_count = assemble()
    print(f"Manuscript assembled at {OUTPUT_FILE}")
    if dup_count > 0:
        print(f"WARNING: {dup_count} duplicate content blocks detected — review source map selectors")
    validate_and_write_manifest()
