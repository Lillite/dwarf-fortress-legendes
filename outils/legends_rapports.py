"""Rapports factuels et dossiers à la demande pour un export Legends indexé."""

import csv
import re
import sqlite3
from collections import defaultdict
from contextlib import closing
from pathlib import Path

EVENT = "historical_event"
COLLECTION = "historical_event_collection"
FIGURE = "historical_figure"
BATTLE_COLUMNS = (
    "annee seconds72 guerre_id guerre bataille_id bataille evenement_id ligne_original "
    "site_id site sous_region_id coordonnees attaquant_civilisation_id attaquant_civilisation "
    "attaquant_chef_id attaquant_chef defenseur_civilisation_id defenseur_civilisation "
    "defenseur_chef_id defenseur_chef issue_xml"
).split()


def _open(database):
    db = sqlite3.connect(database.resolve().as_uri() + "?mode=ro", uri=True)
    db.row_factory = sqlite3.Row
    return db


def _csv(path, header, rows):
    with path.open("w", encoding="utf-8", newline="") as stream:
        writer = csv.writer(stream)
        writer.writerow(header)
        writer.writerows(rows)


def _md(value):
    text = " ".join(str(value if value is not None else "").splitlines())
    text = text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
    return re.sub(r"([\\|`*_[\]#!])", r"\\\1", text)


def _fields(db, category, record_id):
    # Les scalaires de la notice primaire ont priorité. Le complément remplit les lacunes.
    rows = db.execute("""
        SELECT f.path, f.value FROM fields f JOIN records r
          ON r.category=f.category AND r.id=f.owner_id
        WHERE r.category=? AND r.id=? AND f.ordinal=0
        ORDER BY (f.source=r.source) DESC, f.source, f.line
    """, (category, record_id))
    values = {}
    for path, value in rows:
        values.setdefault(path, value)
    return values


def _battles(db):
    names = {(r["category"], str(r["id"])): r["name"] or "" for r in db.execute("""
        SELECT category, id, name FROM records WHERE category IN
        ('historical_figure', 'historical_event_collection', 'entity', 'site')
    """)}
    lines = []
    for battle in db.execute("SELECT * FROM records WHERE category=? AND type='battle' ORDER BY id", (COLLECTION,)):
        batt = _fields(db, COLLECTION, battle["id"])
        events = list(db.execute("""
            SELECT DISTINCT e.* FROM refs x JOIN records e
              ON e.category=x.target_category AND e.id=x.target_id
            WHERE x.category=? AND x.owner_id=? AND x.path='event'
              AND e.category=? AND e.type IN ('attacked site', 'field battle')
            ORDER BY e.id
        """, (COLLECTION, battle["id"], EVENT)))
        wars = {str(row[0]) for row in db.execute("""
            SELECT DISTINCT x.owner_id FROM refs x JOIN records w
              ON w.category=x.category AND w.id=x.owner_id
            WHERE w.category=? AND w.type='war' AND x.path='eventcol'
              AND x.target_category=? AND x.target_id=?
        """, (COLLECTION, COLLECTION, battle["id"]))}
        war = batt.get("war_eventcol", "")
        if war and war != "-1":
            wars.add(war)
        for event in events or [None]:
            ev = _fields(db, EVENT, event["id"]) if event is not None else {}
            site = batt.get("site_id", ev.get("site_id", ""))
            sides = []
            for side in ("attacker", "defender"):
                civ = ev.get(side + "_civ_id", "")
                chief = ev.get(side + "_general_hfid", "")
                sides.extend([civ, names.get(("entity", civ), ""), chief, names.get((FIGURE, chief), "")])
            for parent in sorted(wars) or [war]:
                lines.append([
                    ev.get("year", batt.get("start_year")), ev.get("seconds72", batt.get("start_seconds72")),
                    parent, names.get((COLLECTION, parent), ""), battle["id"], battle["name"],
                    event["id"] if event is not None else None, event["line"] if event is not None else None,
                    site, names.get(("site", site), ""), batt.get("subregion_id", ev.get("subregion_id")),
                    batt.get("coords", ev.get("coords")), *sides, batt.get("outcome"),
                ])
    def date_key(row):
        return tuple(int(row[i]) if row[i] not in (None, "") else -1 for i in (0, 1, 4, 6))
    return sorted(lines, key=date_key)


def _command_changes(battles):
    # Un chef et une bataille comptent une fois par rôle, même en présence de plusieurs notices.
    commands = defaultdict(lambda: {"attaque": {}, "defense": {}})
    names = {}
    for row in battles:
        for role, offset in (("attaque", 14), ("defense", 18)):
            chief = row[offset]
            if chief not in (None, "", "-1"):
                names[chief] = row[offset + 1]
                commands[chief][role].setdefault(row[4], row[6])
    out = []
    for chief, roles in commands.items():
        attack, defense = roles["attaque"], roles["defense"]
        if attack and defense:
            out.append((chief, names[chief], len(attack), len(defense),
                        next(iter(attack.values())), next(iter(defense.values()))))
    return sorted(out, key=lambda r: (-r[2] - r[3], int(r[0])))


def _works(db):
    # Une œuvre abstraite peut être transcrite dans plusieurs objets. Un artefact peut réunir plusieurs textes.
    copies = defaultdict(set)
    for work, item in db.execute("""
        SELECT DISTINCT target_id, owner_id FROM refs
        WHERE category='artifact' AND target_category='written_content'
          AND path='item/page_written_content_id'
    """):
        copies[work].add(item)
    authors = defaultdict(set)
    for work, author in db.execute("""
        SELECT DISTINCT owner_id, target_id FROM refs
        WHERE category='written_content' AND target_category='historical_figure' AND path='author_hfid'
    """):
        authors[work].add(author)
    compositions = defaultdict(set)
    for event, work in db.execute("""
        SELECT DISTINCT x.owner_id, x.target_id FROM refs x JOIN records e
          ON e.category=x.category AND e.id=x.owner_id
        WHERE e.category='historical_event' AND e.type='written content composed'
          AND x.target_category='written_content'
    """):
        compositions[work].add(event)
    def ids(values):
        return " ".join(map(str, sorted(values)))
    return [
        (r["id"], r["name"], ids(authors[r["id"]]), ids(compositions[r["id"]]),
         len(copies[r["id"]]), ids(copies[r["id"]]), r["source"], r["line"])
        for r in db.execute("SELECT * FROM records WHERE category='written_content' ORDER BY id")
    ]


def _sites(db):
    events = list(db.execute("""
        SELECT DISTINCT s.id site_id, s.name site, e.year, e.seconds72, e.id, e.type, e.source, e.line
        FROM records e JOIN refs x ON x.category=e.category AND x.owner_id=e.id
        JOIN records s ON s.category=x.target_category AND s.id=x.target_id
        WHERE e.category='historical_event' AND s.category='site' AND x.path='site_id'
          AND e.type IN ('created site','hf destroyed site','destroyed site','reclaim site',
                         'site taken over','site retired','abandoned site')
        ORDER BY s.id, e.year, e.seconds72, e.id
    """))
    destructions = defaultdict(list)
    for row in events:
        if row["type"] in ("destroyed site", "hf destroyed site") and row["year"] is not None:
            destructions[row["site_id"]].append(row)
    settlements = defaultdict(list)
    for row in db.execute("""
        SELECT DISTINCT x.target_id site_id, p.target_id figure_id, e.year, e.seconds72, e.id
        FROM records e JOIN refs x ON e.category=x.category AND e.id=x.owner_id
        JOIN refs p ON p.category=e.category AND p.owner_id=e.id AND p.source=x.source
        JOIN fields f ON f.category=e.category AND f.owner_id=e.id AND f.source=x.source
        WHERE e.category='historical_event' AND e.type='change hf state' AND e.year IS NOT NULL
          AND x.path='site_id' AND x.target_category='site'
          AND p.path='hfid' AND p.target_category='historical_figure'
          AND f.path='state' AND f.value='settled'
        ORDER BY site_id, figure_id, e.year, e.seconds72, e.id
    """):
        if row["site_id"] in destructions:
            settlements[(row["site_id"], row["figure_id"])].append(row)

    def earlier(first, second):
        if first["year"] != second["year"]:
            return first["year"] < second["year"]
        a, b = first["seconds72"], second["seconds72"]
        return a is not None and b is not None and 0 <= a < b
    returns = []
    for (site, figure), mentions in settlements.items():
        for destruction in destructions[site]:
            before = [r for r in mentions if earlier(r, destruction)]
            after = [r for r in mentions if earlier(destruction, r)]
            if before and after:
                returns.append((site, figure, before[-1]["id"], destruction["id"], after[0]["id"]))
    return events, returns


def write_reports(database: Path, destination: Path):
    """Générer les tables de découverte et le sommaire sans intervention éditoriale."""
    destination.mkdir(parents=True, exist_ok=True)
    with closing(_open(database)) as db:
        battles = _battles(db)
        changes = _command_changes(battles)
        _csv(destination / "commandements.csv", BATTLE_COLUMNS, battles)
        _csv(destination / "chefs-attaque-defense.csv",
             ("figure_id", "nom", "batailles_attaque", "batailles_defense",
              "evenement_exemple_attaque", "evenement_exemple_defense"), changes)
        works = _works(db)
        _csv(destination / "oeuvres.csv",
             ("oeuvre_id", "titre", "auteurs_id", "evenements_composition", "nombre_objets",
              "artefacts_id", "source", "ligne"), works)
        sites, returns = _sites(db)
        _csv(destination / "lieux.csv",
             ("site_id", "site", "annee", "seconds72", "evenement_id", "type", "source", "ligne"), sites)
        _csv(destination / "retours.csv",
             ("site_id", "figure_id", "installation_avant", "destruction", "installation_apres"), returns)
        issues = list(db.execute("""
            SELECT source, category, path, reason, COUNT(*), MIN(owner_id) FROM issues
            GROUP BY source, category, path, reason ORDER BY source, category, path, reason
        """))
        _csv(destination / "references-a-verifier.csv",
             ("source", "categorie", "champ", "raison", "occurrences", "notice_exemple"), issues)
        types = list(db.execute("""
            SELECT type, COUNT(*), MIN(year), MAX(year), MIN(id) FROM records
            WHERE category=? GROUP BY type ORDER BY type
        """, (EVENT,)))
        _csv(destination / "types-evenements.csv",
             ("type", "occurrences", "premiere_annee", "derniere_annee", "evenement_exemple"), types)
        sources = list(db.execute("SELECT name, sha256 FROM sources ORDER BY name"))
        missing = len({r[4] for r in battles if r[6] is None})
    summary = [
        "# Index de l’export Legends", "",
        "Consulter un relevé selon la question posée. Les numéros renvoient aux notices du XML de ce monde.", "",
        "| Relevé | Ce qu’il permet de retrouver |",
        "| --- | --- |",
        f"| [Types d’événements](types-evenements.csv) | {sum(r[1] for r in types)} événements dans {len(types)} types. Un exemple par type pour explorer d’autres domaines. |",
        f"| [Batailles](commandements.csv) | {len({r[4] for r in battles})} batailles. Camp et chef pour chaque notice d’attaque ou de bataille en rase campagne. |",
        f"| [Chefs ayant attaqué et défendu](chefs-attaque-defense.csv) | {len(changes)} figures. Les deux événements donnés en exemple renvoient au relevé des batailles. |",
        f"| [Œuvres et exemplaires](oeuvres.csv) | {len(works)} textes. Chaque ligne relie auteurs, composition et objets porteurs documentés. |",
        f"| [Histoire des lieux](lieux.csv) | {len(sites)} mentions de fondation, destruction, reprise, occupation ou abandon, classées par site. |",
        f"| [Installations encadrant une destruction](retours.csv) | {len(returns)} rapprochements où une même figure s’installe au même site avant et après une destruction datée. |",
        f"| [Références à vérifier](references-a-verifier.csv) | {sum(r[4] for r in issues)} observations groupées par champ et raison. Le détail est dans la table SQLite `issues`. |", "",
        "Une même notice peut documenter plusieurs histoires. Un rôle militaire indique la position dans la bataille. "
        "Une nouvelle installation atteste deux présences, le trajet et ses raisons restent à établir. "
        "Les dates à l’année et les mentions simultanées conservent leur précision d’origine. "
        "Une valeur vide ou `-1` dans un relevé de commandement marque une donnée non renseignée.", "",
    ]
    if missing:
        summary += [f"{missing} bataille(s) ne comportent aucune notice d’attaque reconnue. Leurs lignes gardent les champs d’événement vides.", ""]
    summary += ["## Sources indexées", ""]
    for name, sha in sources:
        summary.append(f"- {_md(name)} · SHA-256 `{sha}`")
    (destination / "README.md").write_text("\n".join(summary) + "\n", encoding="utf-8")


def _structure_links(db, category, record_id):
    # Le site et l'identifiant local forment la clé. Chaque notice garde sa propre ligne XML.
    citations = list(db.execute("""
        SELECT site_id, local_id, path, source, line FROM structure_refs
        WHERE category=? AND owner_id=? ORDER BY site_id, local_id, source, line, ordinal
    """, (category, record_id)))
    keys = {(site, local) for site, local, *_ in citations}
    if category == "site":
        keys.update((site, local) for site, local in db.execute(
            "SELECT DISTINCT site_id, local_id FROM structures WHERE site_id=?", (record_id,)))
    if not keys:
        return []
    out = ["## Structures liées", ""]
    if citations:
        out += ["| Site ID | Structure locale ID | Champ | Source, ligne du renvoi |",
                "| --- | --- | --- | --- |"]
        for site, local, path, source, line in citations:
            out.append(f"| {site} | {local} | `{path}` | {_md(source)}, {line} |")
        out.append("")
    out += ["| Site ID | Structure locale ID | Nom | Type | Source, ligne de la description |",
            "| --- | --- | --- | --- | --- |"]
    for site, local in sorted(keys):
        definitions = db.execute("""
            SELECT name, type, source, line FROM structures WHERE site_id=? AND local_id=?
            ORDER BY source, line
        """, (site, local)).fetchall()
        if not definitions:
            out.append(f"| {site} | {local} | Description introuvable | | |")
        for name, kind, source, line in definitions:
            out.append(f"| {site} | {local} | {_md(name)} | {_md(kind)} | {_md(source)}, {line} |")
    return [*out, ""]


def write_dossier(database: Path, category: str, record_id: int, destination: Path):
    """Présenter une notice avec ses champs et toutes ses références dans les deux sens."""
    with closing(_open(database)) as db:
        record = db.execute("SELECT * FROM records WHERE category=? AND id=?", (category, record_id)).fetchone()
        if record is None:
            raise ValueError(f"Notice introuvable dans cet export : {category} {record_id}")
        refs = """
            SELECT x.path, x.source, x.line, r.name, r.type, r.year, r.seconds72,
                   {kind} other_category, {ident} other_id
            FROM refs x LEFT JOIN records r ON r.category={kind} AND r.id={ident}
            WHERE {my_kind}=? AND {my_id}=?
            ORDER BY r.year IS NULL, r.year, r.seconds72, other_category,
                     other_id, x.source, x.path, x.ordinal
        """
        out = [f"# {_md(record['name'] or record['type'] or category)}", "",
               f"Catégorie `{category}` · identifiant {record_id} · "
               f"{_md(record['source'])}, ligne {record['line']}.", ""]
        for title, expression in [
            ("Notices qui citent cet élément", ("x.category", "x.owner_id", "x.target_category", "x.target_id")),
            ("Renvois de cette notice", ("x.target_category", "x.target_id", "x.category", "x.owner_id")),
        ]:
            rows = db.execute(refs.format(kind=expression[0], ident=expression[1],
                                          my_kind=expression[2], my_id=expression[3]), (category, record_id))
            out += [f"## {title}", "", "| Année | seconds72 | Catégorie et ID | Nom ou type | Champ | Source, ligne du renvoi |",
                    "| --- | --- | --- | --- | --- | --- |"]
            for row in rows:
                year = row['year'] if row['year'] is not None else ""
                seconds = row["seconds72"] if row["seconds72"] is not None else ""
                out.append(f"| {year} | {seconds} | `{row['other_category']}` {row['other_id']} | "
                           f"{_md(row['name'] or row['type'])} | `{row['path']}` | {_md(row['source'])}, {row['line']} |")
            out.append("")
        out.extend(_structure_links(db, category, record_id))
        out += ["## Champs de la notice", "", "| Champ | Valeur | Source, ligne |", "| --- | --- | --- |"]
        for path, value, source, line in db.execute("""
            SELECT path, value, source, line FROM fields WHERE category=? AND owner_id=?
            ORDER BY source, line, path, ordinal
        """, (category, record_id)):
            out.append(f"| `{path}` | {_md(value)} | {_md(source)}, {line} |")
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text("\n".join(out) + "\n", encoding="utf-8")
