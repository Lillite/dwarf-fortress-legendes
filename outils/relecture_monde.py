"""Contrôles structurels des sources éditoriales. Les décisions de lecture restent dans le plan."""

import csv
import hashlib
import re
from collections import defaultdict
from pathlib import Path

from legends_rapports import _md

SECTIONS = {
    "historical_figures": "historical_figure",
    "historical_events": "historical_event",
    "historical_event_collections": "historical_event_collection",
    "entities": "entity",
    "sites": "site",
    "artifacts": "artifact",
    "written_contents": "written_content",
    "poetic_forms": "poetic_form",
    "musical_forms": "musical_form",
    "dance_forms": "dance_form",
    "regions": "region",
    "world_constructions": "world_construction",
}
CHAPTER_WORD = {
    "fr": "Chapitre",
    "en": "Chapter",
    "es": "Capítulo",
    "de": "Kapitel",
    "it": "Capitolo",
    "pt": "Capítulo",
}


def verifier_glossaire(db, world, diagnostics):
    gloss = defaultdict(list)
    path = world / "reperes/glossaire.csv"
    if not path.is_file():
        return gloss
    with path.open(encoding="utf-8-sig", newline="") as f:
        for row in csv.DictReader(f):
            ref = row["reference_source"]
            parts = ref.split("/")
            source = Path(row["fichier_source"]).name
            if len(parts) == 4 and parts[0] == "sites" and parts[2] == "structures":
                found = db.execute(
                    "SELECT 1 FROM structures WHERE site_id=? AND local_id=? AND source=?",
                    (parts[1], parts[3], source),
                ).fetchone()
            elif len(parts) == 2 and parts[0] in SECTIONS and parts[1].isdigit():
                cat, ident = SECTIONS[parts[0]], int(parts[1])
                found = db.execute(
                    "SELECT 1 FROM fields WHERE category=? AND owner_id=? AND source=? LIMIT 1",
                    (cat, ident, source),
                ).fetchone()
                label = row["langue_cible"] + " · " + row["forme_retenue"]
                if label not in gloss[cat, ident]:
                    gloss[cat, ident].append(label)
                declared = row["categorie"]
                if declared in SECTIONS and SECTIONS[declared] != cat:
                    diagnostics.append(f"Glossaire : catégorie {declared} incompatible avec {ref}.")
            else:
                found = None
            if not found:
                diagnostics.append(f"Glossaire : référence à vérifier dans {source}, {ref}.")
    return gloss


def controles_manuscrits(world, output, version, diagnostics):
    snapshot = world / ".fichiers-git"
    tracked = (
        set(snapshot.read_bytes().decode("utf-8", errors="surrogateescape").split("\0"))
        if snapshot.is_file()
        else set()
    )
    books = defaultdict(list)
    openings = ["# Passages à relire", "", "## Ouvertures", ""]
    repeated = defaultdict(list)
    for book in sorted((world / "manuscrits").glob("*/*")):
        if not book.is_dir() or not re.fullmatch(r"P\d+", book.name):
            continue
        books[book.name].append(book)
        rel = book.relative_to(world)
        language = book.parent.name.split("-")[0]
        presentation = book / "0.md"
        if not presentation.is_file():
            diagnostics.append(f"{rel} : présentation 0.md absente ({version}).")
        elif not re.match(r"^#\s+[^\n]+\n\s*\n\S", presentation.read_text(encoding="utf-8").strip()):
            diagnostics.append(f"{rel}/0.md : vérifier le titre et le texte de présentation.")
        chapters = sorted(
            (f for f in book.glob("*.md") if f.stem.isdecimal() and int(f.stem) > 0), key=lambda f: int(f.stem)
        )
        short = book / "nouvelle.md"
        if short.is_file() and chapters:
            diagnostics.append(f"{rel} : nouvelle et chapitres séparés présents, vérifier la forme retenue.")
        if not chapters and not short.is_file():
            diagnostics.append(f"{rel} : aucun chapitre ni nouvelle rédigé.")
        for n, chapter in enumerate(chapters, 1):
            first = next(
                (line.strip() for line in chapter.read_text(encoding="utf-8").splitlines() if line.strip()), ""
            )
            word = CHAPTER_WORD.get(language)
            correct = first == f"# {word} {n}" if word else re.fullmatch(r"#\s+.+\s+" + str(n), first)
            if n != int(chapter.stem) or not correct:
                diagnostics.append(
                    f"{chapter.relative_to(world)} : vérifier le numéro et l’en-tête du chapitre {n}."
                )
        if short.is_file():
            text = short.read_text(encoding="utf-8")
            headings = re.findall(r"^#{1,2}\s+(.+)$", text, re.M)
            word = CHAPTER_WORD.get(language)
            parts = [
                h
                for h in headings
                if re.match(
                    r"(?:[IVXLCDM]+\.|\d+\.|" + (re.escape(word) + r"\b" if word else r"(?!)") + ")", h, re.I
                )
            ]
            if word and any(h != f"{word} {n}" for n, h in enumerate(parts, 1)):
                diagnostics.append(
                    f"{rel}/nouvelle.md : vérifier les divisions numérotées au regard de la forme choisie."
                )
        for i, chapter in enumerate(chapters + ([short] if short.is_file() else [])):
            blocks = [
                b.strip()
                for b in re.split(r"\n\s*\n", chapter.read_text(encoding="utf-8"))
                if b.strip() and not b.lstrip().startswith(("#", "<!--"))
            ]
            if i == 0 and blocks:
                openings.extend([f"### {rel}", "", "> " + blocks[0].replace("\n", " ")[:550], ""])
            for k, block in enumerate(blocks, 1):
                if len(block) >= 60:
                    repeated[hashlib.sha256(block.encode()).hexdigest()].append(
                        f"{chapter.relative_to(world)} §{k}"
                    )
        for path in book.glob("*.md"):
            for dest in re.findall(r"\]\(([^\s)]+)\)", path.read_text(encoding="utf-8")):
                local = dest.partition("#")[0]
                if not local or ":" in local or local.startswith("/"):
                    continue
                target = (path.parent / local).resolve()
                if (
                    target.is_relative_to(world)
                    and not target.exists()
                    and target.relative_to(world).as_posix() not in tracked
                ):
                    diagnostics.append(f"{path.relative_to(world)} : cible de lien absente {local}.")
    openings += ["## Paragraphes identiques de 60 caractères ou plus", ""]
    openings += [
        "- " + " · ".join(_md(loc) for loc in locations) for locations in repeated.values() if len(locations) > 1
    ] or ["Aucun relevé."]
    (output / "relecture.md").write_text("\n".join(openings) + "\n", encoding="utf-8")
    return books
