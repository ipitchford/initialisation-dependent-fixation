"""Build the consensus manuscript with Pandoc and XeLaTeX.

Run from anywhere. Pandoc, XeLaTeX and the listed fonts/TeX packages must be
installed. Build intermediates live in a temporary directory, outside the bundle.
"""
from pathlib import Path
import argparse
import json
import re
import shutil
import subprocess
import tempfile

ROOT = Path(__file__).resolve().parents[1]
JOBS = {
    "consensus": ("consensus/manuscript.md", "consensus/initialisation_dependent_fixation.pdf"),
}


def build(key):
    source_name, output_name = JOBS[key]
    source, output = ROOT / source_name, ROOT / output_name
    if not source.exists():
        return {"document": key, "status": "source not yet present"}
    source_text = source.read_text()
    if not source_text.startswith("---\n"):
        match = re.match(r"# ([^\n]+)\n", source_text)
        title = match.group(1) if match else key.replace("_", " ").title()
        if match:
            source_text = source_text[match.end():]
        source_text = "---\ntitle: " + json.dumps(title) + "\ndate: \"27 October 2026\"\nlang: en-GB\n---\n" + source_text
        # Reviews use a title at level one and eleven numbered sections at level two.
        source_text = re.sub(r"(?m)^(#{2,6}) ", lambda m: m.group(1)[1:] + " ", source_text)
    with tempfile.TemporaryDirectory(prefix="applied_math_pdf_") as tmp:
        tmp = Path(tmp)
        staged = tmp / "input.md"
        staged.write_text(source_text)
        latex = tmp / "document.tex"
        command = [
            "pandoc", str(staged), "--from=markdown+tex_math_dollars+raw_tex+autolink_bare_uris",
            "--standalone", "--top-level-division=section", "--output", str(latex),
            "--resource-path=" + str(source.parent),
            "--include-in-header=" + str(ROOT / "evidence/pdf_header.tex"),
            "--variable=documentclass:article", "--variable=papersize:a4",
            "--variable=fontsize:11pt", "--variable=geometry:margin=24mm",
            "--variable=linestretch:1.08",
            # Latin Modern OpenType files ship with every TeX Live; loading them by
            # file name avoids depending on system font registration.
            "--variable=mainfont:lmroman10-regular.otf",
            "--variable=mainfontoptions:BoldFont=lmroman10-bold.otf,ItalicFont=lmroman10-italic.otf,BoldItalicFont=lmroman10-bolditalic.otf",
            "--variable=sansfont:lmsans10-regular.otf",
            "--variable=sansfontoptions:BoldFont=lmsans10-bold.otf,ItalicFont=lmsans10-oblique.otf",
            "--variable=monofont:lmmono10-regular.otf",
            "--variable=colorlinks:true", "--variable=linkcolor:Maroon",
            "--variable=urlcolor:Maroon",
        ]
        p = subprocess.run(command, cwd=source.parent, text=True, capture_output=True)
        if p.returncode:
            raise RuntimeError(p.stderr)
        for _ in range(2):
            p = subprocess.run(["xelatex", "-interaction=nonstopmode", "-halt-on-error",
                                "-output-directory=" + str(tmp), str(latex)],
                               cwd=source.parent, text=True, capture_output=True)
            if p.returncode:
                error_file = ROOT / "evidence" / (key + "_build_error.txt")
                error_file.write_text(p.stdout + "\n" + p.stderr)
                raise RuntimeError("XeLaTeX failed; see " + str(error_file))
        shutil.copy2(latex, source.with_suffix(".tex"))
        log = (tmp / "document.log").read_text(errors="replace")
        warnings = [line for line in log.splitlines()
                    if any(word in line for word in ("Overfull", "Missing character", "LaTeX Warning"))]
        shutil.copy2(tmp / "document.pdf", output)
        return {"document": key, "status": "built", "pdf": output_name,
                "bytes": output.stat().st_size, "layout_warnings": warnings}


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("documents", nargs="*", help="Optional document keys: " + ", ".join(JOBS))
    args = parser.parse_args()
    keys = args.documents or list(JOBS)
    for key in keys:
        if key not in JOBS:
            parser.error("Unknown document: " + key)
    result = [build(key) for key in keys]
    print(json.dumps(result, indent=2))
