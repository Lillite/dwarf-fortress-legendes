"""Préparer des fiches de reprise à partir des références explicites d'une branche."""

import argparse
import csv
import hashlib
import json
import os
import re
from collections import defaultdict
from contextlib import closing
from pathlib import Path
from urllib.parse import quote

from legends_rapports import EVENT, _csv, _md, _open
from relecture_monde import controles_manuscrits, verifier_glossaire

TRACK = re.compile(r"P[0-9]+\Z")
CHAPTER = re.compile(r"manuscrits/[^/;,|]+/(P[0-9]+)/[^/;,|]+?\.md")
PUBLISHED = Path("reperes/index-legends/dossiers")


def rows(world, name, required):
    path = world / "reperes" / name
    if not path.exists():
        return []
    with path.open(encoding="utf-8-sig", newline="") as stream:
        reader = csv.DictReader(stream, strict=True)
        if not set(required.split()) <= set(reader.fieldnames or ()):
            raise ValueError(f"{name} : colonnes attendues {required}")
        return list(reader)


def link(target, page):
    return quote(os.path.relpath(target, page.parent).replace(os.sep, "/"), safe="/.-_")


def digest(value):
    return hashlib.sha256(json.dumps(value, ensure_ascii=False, sort_keys=True).encode()).hexdigest()


def register_entries(text):
    """Localiser les pistes inscrites dans le tableau du modèle ou sous leur propre titre."""
    entries = {}
    in_inventory = False
    for number, line in enumerate(text.splitlines(), 1):
        row = line.strip()
        if row.startswith("|"):
            first = row.split("|", 2)[1].strip()
            if first == "ID":
                in_inventory = True
            elif in_inventory and TRACK.fullmatch(first):
                entries.setdefault(first, number)
        else:
            in_inventory = False
            heading = re.match(r"^##\s+(P[0-9]+)\b", line)
            if heading:
                entries[heading[1]] = number
    return entries


def prep_events(db, world, diagnostics):
    tracks = defaultdict(set)
    reasons = defaultdict(set)
    chapters = defaultdict(set)
    asserted = defaultdict(list)
    collections = defaultdict(set)
    editorial_inputs = defaultdict(set)
    for row in rows(world, "occurrences.csv", "piste evenement_id"):
        track, value = row["piste"].strip(), row["evenement_id"].strip()
        if not TRACK.fullmatch(track) or not value.isascii() or not value.isdigit():
            diagnostics.append(f"occurrences.csv : piste ou événement invalide ({track}, {value}).")
            continue
        event = int(value)
        tracks[event].add(track)
        editorial_inputs[str(event)].add(digest(row))
        why = row.get("champs_qui_relient_la_notice", "").strip()
        if why:
            reasons[track, why].add(event)
        asserted[event].append(
            (
                row.get("annee"),
                row.get("seconds72"),
                row.get("type_xml"),
                row.get("ligne_original"),
                "occurrences.csv",
            )
        )
    for row in rows(world, "chronologie.csv", "reference_evenement chapitres_associes"):
        ref = row["reference_evenement"].strip()
        coll = re.fullmatch(r"historical_event_collections?/(\d+)", ref)
        match = re.fullmatch(r"historical_events?/(\d+)", ref)
        if not (match or coll):
            diagnostics.append("chronologie.csv : référence à vérifier " + ref)
            continue
        event = int((match or coll)[1])
        editorial_inputs[f"collection-{event}" if coll else str(event)].add(digest(row))
        paths = [m[0] for m in CHAPTER.finditer(row["chapitres_associes"])]
        for path in paths:
            if coll:
                collections[event].add(path)
            else:
                tracks[event].add(Path(path).parent.name)
                chapters[event].add(path)
            if not (world / path).is_file():
                diagnostics.append(f"Événement {event} : chapitre introuvable {path}.")
        if row["chapitres_associes"].strip() and not paths:
            diagnostics.append(f"Événement {event} : destination à vérifier {row['chapitres_associes']}.")
        date = re.fullmatch(
            r"an\s+(-?\d+)(?:\s*/\s*seconds72\s+(-?\d+))?", row.get("date_dans_le_monde", "").strip(), re.I
        )
        location = row.get("fichier_source", "")
        if location and not (world / location).is_file():
            diagnostics.append(f"Événement {event} : source non trouvée {location}.")
        if coll:
            item = db.execute(
                "SELECT year,seconds72 FROM records WHERE category='historical_event_collection' AND id=?",
                (event,),
            ).fetchone()
            if item is None:
                diagnostics.append(f"Collection {event} absente de la base.")
            elif date and (
                int(date[1]) != item[0] or (date[2] and int(date[2]) != (item[1] if item[1] is not None else -1))
            ):
                diagnostics.append(f"Collection {event} : date indiquée à vérifier.")
            continue
        asserted[event].append(
            (date[1] if date else None, date[2] if date else None, None, None, "chronologie.csv")
        )
    return tracks, reasons, chapters, asserted, collections, editorial_inputs


def write_scene(world, out, chapter, evs):
    path = Path(chapter)
    scene = Path("scenes") / path.relative_to("manuscrits")
    scene_dest = out / scene
    scene_dest.parent.mkdir(parents=True, exist_ok=True)

    scene_page = PUBLISHED / scene
    scene_lines = [
        f"# Sources de {_md(chapter)}",
        "",
        f"[Manuscrit]({link(chapter, scene_page)})",
        "",
        "## Notices associées par la chronologie",
        "",
    ]
    for ev in sorted(evs, key=str):
        scene_lines.append(f"- [{ev}]({link(PUBLISHED / 'notices' / f'{ev}.md', scene_page)})")
    for name in ("plan.md", "note.md"):
        doc = path.with_name(name)
        if not (world / doc).is_file():
            continue
        scene_lines += ["", f"## [Décisions et contexte dans {name}]({link(doc, scene_page)})", ""]
        # Les notes sont citées telles quelles. Une mention numérique sert de renvoi à vérifier.
        for n, line_text in enumerate((world / doc).read_text(encoding="utf-8").splitlines(), 1):
            numbers = set(re.findall(r"(?<!\w)\d+(?!\w)", line_text))
            if any(str(ev).removeprefix("collection-") in numbers for ev in evs):
                scene_lines.append(f"- [Ligne {n}]({link(doc, scene_page)}#L{n}) · {_md(line_text)}")
    scene_dest.write_text("\n".join(scene_lines) + "\n", encoding="utf-8")
    return f"- [{_md(chapter)}]({quote(scene.as_posix())}) · {len(evs)} références."


def related_events(db, labels, events):
    candidates = defaultdict(set)
    for category, ident in labels:
        if category not in {"historical_figure", "entity", "artifact", "written_content", "site"}:
            continue
        for (other_id,) in db.execute(
            "SELECT DISTINCT owner_id FROM refs WHERE target_category=? AND target_id=? AND category=?",
            (category, ident, EVENT),
        ):
            candidates[other_id].add((category, ident))
    selected = set(events)
    return [
        (ev, " | ".join(f"{cat}/{n}" for cat, n in sorted(keys)))
        for ev, keys in sorted(candidates.items())
        if ev not in selected
        and len(keys) >= 2
        and any(cat in {"historical_figure", "artifact", "written_content"} for cat, _ in keys)
    ]


def generate(db, world, out, version):
    out.mkdir(parents=True, exist_ok=True)
    (out / "notices").mkdir(exist_ok=True)
    diagnostics = []
    branch_spec = world / "SPEC_Roman_Dwarf_Fortress.md"
    if branch_spec.is_file():
        match = re.search(r"\*\*Version ([\d.]+)", branch_spec.read_text(encoding="utf-8"))
        if match and "SPEC " + match[1] != version:
            diagnostics.append(f"Copie de la branche : SPEC {match[1]}. Contrôles réalisés selon {version}.")
    tracks, reasons, chapters, asserted, collections, editorial_inputs = prep_events(db, world, diagnostics)
    gloss = verifier_glossaire(db, world, diagnostics)
    books = controles_manuscrits(world, out, version, diagnostics)
    register = world / "reperes/pistes.md"
    register_text = register.read_text(encoding="utf-8") if register.is_file() else ""
    registered = register_entries(register_text)
    ids = set(registered) | set(books)
    by_track = defaultdict(list)
    details = {}
    by_entity = defaultdict(set)
    noted = defaultdict(list)
    dependencies = []
    state = {}
    for event in sorted(set(asserted) | set(tracks)):
        ids.update(tracks[event])
        record = db.execute("SELECT * FROM records WHERE category=? AND id=?", (EVENT, event)).fetchone()
        if record is None:
            diagnostics.append(
                f"Événement {event} absent de l’index, cité par {', '.join(sorted(tracks[event]))}."
            )
            for track in tracks[event]:
                noted[track].append(f"Événement {event} introuvable.")
            continue
        fields = list(
            db.execute(
                "SELECT path,value,source,line,ordinal FROM fields WHERE category=? AND owner_id=? ORDER BY source,line,ordinal,path",
                (EVENT, event),
            )
        )
        locations = {r["source"] for r in fields}
        for year, timer, kind, line, origin in asserted[event]:
            for label, value, expected in (
                ("année", year, record["year"]),
                ("seconds72", timer, record["seconds72"]),
                ("type", kind, record["type"]),
                ("ligne", line, record["line"]),
            ):
                if value not in (None, "") and str(value) != str(
                    -1 if expected is None and label == "seconds72" else expected
                ):
                    # Un relevé à deux sources peut citer la ligne du complément.
                    if label == "ligne" and len(locations) > 1:
                        continue
                    diagnostics.append(
                        f"{origin} · événement {event} · {label} indiqué {value}, index {expected}."
                    )
        refs = list(
            db.execute(
                """SELECT DISTINCT x.path,x.target_category,x.target_id,r.name
            FROM refs x LEFT JOIN records r ON (r.category,r.id)=(x.target_category,x.target_id)
            WHERE x.category=? AND x.owner_id=? ORDER BY 1,2,3""",
                (EVENT, event),
            )
        )
        parents = list(
            db.execute(
                """SELECT DISTINCT owner_id FROM refs WHERE category='historical_event_collection'
            AND path='event' AND target_category=? AND target_id=? ORDER BY owner_id""",
                (EVENT, event),
            )
        )
        details[event] = record, refs, parents
        page = [
            f"# Événement {event} · {_md(record['type'])}",
            "",
            f"{_md(record['source'])}, ligne {record['line']}.",
            "",
            "| Champ XML | Valeur | Source et ligne |",
            "| --- | --- | --- |",
        ]
        for f in fields:
            page.append(
                f"| {_md(f['path'])} | {_md(f['value']) if f['value'] else 'balise présente, vide'} | {_md(f['source'])} L{f['line']} |"
            )
        page += [
            "",
            "Collections directes : " + (", ".join(str(p[0]) for p in parents) or "aucune recensée") + ".",
        ]
        (out / "notices" / f"{event}.md").write_text("\n".join(page) + "\n", encoding="utf-8")
        for track in tracks[event]:
            by_track[track].append(event)
        for _, cat, ident, _ in refs:
            by_entity[cat, ident].add(event)
        related_files = sorted(chapters[event])
        relevant_names = [(r[1], r[2], r[3], gloss.get((r[1], r[2]), [])) for r in refs]
        state[str(event)] = {
            "empreinte": digest(
                [
                    list(record),
                    [list(f) for f in fields],
                    relevant_names,
                    [p[0] for p in parents],
                    sorted(tracks[event]),
                    related_files,
                    sorted(editorial_inputs[str(event)]),
                ]
            ),
            "pistes": sorted(tracks[event]),
            "chapitres": related_files,
        }
        dependencies.append([event, " ".join(sorted(tracks[event])), " | ".join(related_files)])
    for cid, destinations in collections.items():
        item = db.execute(
            "SELECT * FROM records WHERE category='historical_event_collection' AND id=?", (cid,)
        ).fetchone()
        if item is None:
            continue
        paths = sorted(destinations)
        affected = sorted({Path(path).parent.name for path in paths})
        ids.update(affected)
        key = f"collection-{cid}"
        content = list(
            db.execute(
                "SELECT path,value,source,line FROM fields WHERE category='historical_event_collection' AND owner_id=? ORDER BY source,line,path,ordinal",
                (cid,),
            )
        )
        state[key] = {
            "empreinte": digest([list(item), [list(f) for f in content], paths, sorted(editorial_inputs[key])]),
            "pistes": affected,
            "chapitres": paths,
        }
        dependencies.append([key, " ".join(affected), " | ".join(paths)])
        (out / "notices" / f"{key}.md").write_text(
            f"# Collection {cid} · {_md(item['name'])}\n\n"
            + "\n".join(f"- {_md(field)} = {_md(val)} · {_md(src)} L{line}" for field, val, src, line in content)
            + "\n",
            encoding="utf-8",
        )
    index = [
        "# Dossiers de travail",
        "",
        f"Référentiel commun {version}. Ouvrir la piste, puis les seules notices utiles.",
        "",
        "[Structure et références](controles.md) · [Extraits et répétitions exactes](relecture.md) · [Dépendances](dependances.csv)",
        "",
    ]
    for track in sorted(ids):
        events = sorted(
            by_track[track],
            key=lambda e: (
                details[e][0]["year"] is None,
                details[e][0]["year"],
                details[e][0]["seconds72"] is not None,
                details[e][0]["seconds72"] or 0,
                e,
            ),
        )
        page = PUBLISHED / f"{track}.md"
        lines = [f"# {track}"]
        if register.is_file():
            target = link("reperes/pistes.md", page)
            if track in registered:
                target += f"?plain=1#L{registered[track]}"
            lines += ["", f"[Registre]({target})"]
        for book in books.get(track, []):
            for source_file in sorted(book.glob("*.md")):
                if source_file.name in {"plan.md", "note.md", "0.md"}:
                    dest = source_file.relative_to(world)
                    lines.append(f"- [{_md(str(dest))}]({link(dest, page)})")
        lines += [
            "",
            "## Chronologie documentée",
            "",
            "Une même date peut correspondre à plusieurs notices. « ? » indique une précision absente.",
            "",
        ]
        labels = {}
        evidence = defaultdict(set)
        for event in events:
            record, refs, parents = details[event]
            roles = []
            for path, cat, ident, name in refs:
                key = (cat, ident)
                if key not in labels:
                    labels[key] = len(labels) + 1, name
                roles.append(f"{_md(path)} → {labels[key][0]}")
            # Garder les faits discriminants même si le type, la date et les acteurs sont identiques.
            extras = [
                f"{_md(r[0])}={_md(r[1]) or 'présent'}"
                for r in db.execute(
                    """SELECT DISTINCT path,value FROM fields WHERE category=? AND owner_id=?
                AND path IN ('state','reason','method','action','interaction','secret_goal','outcome','cause',
                'failed_judgment_test','successful','wrongful_conviction','death_penalty') ORDER BY path,value""",
                    (EVENT, event),
                )
            ]
            lines.append(
                f"- {record['year'] if record['year'] is not None else '?'} / {record['seconds72'] if record['seconds72'] is not None else '?'} · "
                f"[{event}](notices/{event}.md) · {_md(record['type'])} · " + ", ".join(roles + extras)
            )
            for chapter in sorted(chapters[event]):
                evidence[chapter].add(event)
        lines += ["", "## Personnes, lieux et autres références", ""]
        for (cat, ident), (n, name) in labels.items():
            other = sorted({t for ev in by_entity[cat, ident] for t in tracks[ev]} - {track})
            aliases = ", ".join(gloss.get((cat, ident), []))
            lines.append(
                f"- {n}. {_md(name) or 'Nom non renseigné'} · {_md(cat)} {ident}"
                + (f" · {_md(aliases)}" if aliases else "")
                + (" · également cité dans " + ", ".join(other) if other else "")
            )
        lines += ["", "## Sources de scène et motifs du registre", ""]
        for cid, destinations in collections.items():
            for path in destinations:
                if Path(path).parent.name == track:
                    evidence[path].add(f"collection-{cid}")
        for chapter, evs in sorted(evidence.items()):
            lines.append(write_scene(world, out, chapter, evs))
        for (t, note), evs in sorted(reasons.items()):
            if t == track:
                lines.append(f"- {_md(note)} ({', '.join(map(str, sorted(evs)))}).")
        for ev in events:
            other = sorted(tracks[ev] - {track})
            if other:
                lines.append(f"- Notice {ev} également retenue pour " + ", ".join(f"[{t}]({t}.md)" for t in other))
        extra = related_events(db, labels, events)
        if extra:
            _csv(out / f"{track}-renvois.csv", ("evenement_a_examiner", "references_communes"), extra)
            lines += [
                "",
                f"[{len(extra)} autres événements à examiner]({track}-renvois.csv) : au moins deux références communes, dont une personne, une œuvre ou un artefact. Le registre décide de leur pertinence.",
            ]
        lines.extend(noted[track])
        (out / page.name).write_text("\n".join(lines) + "\n", encoding="utf-8")
        index.append(f"- [{track}]({track}.md) · {len(events)} événements résolus.")
    (out / "README.md").write_text("\n".join(index) + "\n", encoding="utf-8")
    (out / "controles.md").write_text(
        f"# Contrôles selon {version}\n\n"
        + (
            "\n".join("- " + _md(s) for s in sorted(set(diagnostics)))
            or "Aucun écart détecté dans les données contrôlées."
        )
        + "\n",
        encoding="utf-8",
    )
    _csv(out / "dependances.csv", ("evenement", "pistes", "chapitres"), dependencies)
    (out / "dependances.json").write_text(
        json.dumps(state, ensure_ascii=False, sort_keys=True) + "\n", encoding="utf-8"
    )


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("base", type=Path)
    p.add_argument("--monde", type=Path, required=True)
    p.add_argument("--sortie", type=Path, required=True, help="nouveau dossier de génération")
    args = p.parse_args()
    if args.sortie.exists() and any(args.sortie.iterdir()):
        p.error("Utiliser un dossier de sortie vide pour cette génération.")
    spec = (Path(__file__).resolve().parents[1] / "SPEC_Roman_Dwarf_Fortress.md").read_text(encoding="utf-8")
    version = "SPEC " + re.search(r"\*\*Version ([\d.]+)", spec)[1]
    with closing(_open(args.base)) as db:
        generate(db, args.monde.resolve(), args.sortie, version)


if __name__ == "__main__":
    main()
