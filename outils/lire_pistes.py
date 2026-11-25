"""Croiser la base Legends avec les événements explicitement cités dans occurrences.csv."""

import argparse
import csv
import sqlite3
import sys
from collections import Counter
from contextlib import closing
from pathlib import Path


def referenced_events(path: Path, track: str | None) -> set[int]:
    events = set()
    with path.open(encoding="utf-8-sig", newline="") as stream:
        reader = csv.DictReader(stream, strict=True)
        if not {"piste", "evenement_id"}.issubset(reader.fieldnames or ()):
            raise ValueError("Le CSV doit comporter les colonnes piste et evenement_id.")
        for row in reader:
            track_id = (row["piste"] or "").strip()
            if track is not None and track_id != track:
                continue
            value = (row["evenement_id"] or "").strip()
            if not track_id or not value.isascii() or not value.isdecimal():
                raise ValueError(f"Ligne CSV {reader.line_num} : piste ou identifiant d’événement invalide.")
            events.add(int(value))
    return events


def coverage(db, references, writer):
    totals = Counter()
    cited = Counter()
    examples = {}
    missing = references.copy()
    for event_id, kind in db.execute(
        "SELECT id, type FROM records WHERE category='historical_event' ORDER BY id"
    ):
        kind = kind or ""
        totals[kind] += 1
        if event_id in references:
            cited[kind] += 1
            missing.discard(event_id)
        else:
            examples.setdefault(kind, event_id)
    writer.writerow(("type_xml", "notices_monde", "notices_citees_dans_le_csv", "exemple_non_cite"))
    for kind, count in sorted(totals.items()):
        writer.writerow((kind, count, cited[kind], examples.get(kind)))
    if missing:
        print("Événements cités introuvables dans la base : " + ", ".join(map(str, sorted(missing))),
              file=sys.stderr)


def track_events(db, references, writer):
    dated = []
    missing = []
    for event_id in sorted(references):
        event = db.execute(
            "SELECT year, seconds72, id, type, source, line FROM records WHERE category='historical_event' AND id=?",
            (event_id,),
        ).fetchone()
        if event is None:
            missing.append(event_id)
        else:
            dated.append(event)
    # L’ordre d’affichage au sein d’une année n’établit pas la succession des dates imprécises.
    dated.sort(key=lambda r: (r[0] is None, r[0], r[1] is None, r[1], r[2]))
    writer.writerow(("statut", "annee", "seconds72", "evenement_id", "type_xml", "source", "ligne"))
    for event in dated:
        writer.writerow(("trouvé", *event))
    for event_id in missing:
        writer.writerow(("introuvable", None, None, event_id, None, None, None))
    if not references:
        print("Aucune occurrence pour cette piste dans le CSV fourni.", file=sys.stderr)


def main():
    parser = argparse.ArgumentParser(description=__doc__, epilog=(
        "Sortie TSV, un événement compté une fois même si plusieurs pistes le citent. "
        "La comparaison porte uniquement sur les références du CSV fourni pour le même monde."))
    parser.add_argument("base", type=Path, help="base SQLite de l’export, ouverte en lecture seule")
    parser.add_argument("occurrences", type=Path, help="relevé CSV des occurrences de la branche")
    parser.add_argument("--piste", help="identifiant de la piste à consulter dans le registre de cet export")
    args = parser.parse_args()
    try:
        ids = referenced_events(args.occurrences, args.piste)
        uri = args.base.resolve().as_uri() + "?mode=ro"
        with closing(sqlite3.connect(uri, uri=True)) as db:
            writer = csv.writer(sys.stdout, delimiter="\t", lineterminator="\n")
            if args.piste is None:
                coverage(db, ids, writer)
            else:
                track_events(db, ids, writer)
    except (csv.Error, OSError, ValueError, OverflowError, sqlite3.Error) as error:
        parser.exit(1, f"Lecture interrompue : {error}\n")


if __name__ == "__main__":
    main()
