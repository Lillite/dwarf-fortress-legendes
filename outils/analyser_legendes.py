"""Construit l'index et les relevés d'une branche d'export Legends."""

import argparse
import codecs
import json
import sqlite3
import tempfile
from contextlib import closing
from pathlib import Path
from xml.parsers import expat

from legends_index import build_index, encoding_of
from legends_rapports import write_reports


MANIFEST = "manifest.json"
FORMAT = "dwarf-fortress-legendes/index-v1"


def export_kind(path: Path) -> str | None:
    name = path.stem.lower()
    if name.endswith("legends_plus"):
        return "plus"
    if name.endswith("legends"):
        return "standard"
    # Arrêter la lecture au premier élément, même si un marqueur CP437 le suit.
    def root_found(tag, _attrs):
        raise StopIteration(tag)

    parser = expat.ParserCreate("UTF-8")
    parser.StartElementHandler = root_found
    with path.open("rb") as stream:
        chunk = stream.read(4096)
        decoder = codecs.getincrementaldecoder(encoding_of(chunk))()
        try:
            while chunk:
                parser.Parse(decoder.decode(chunk), False)
                chunk = stream.read(4096)
            parser.Parse(decoder.decode(b"", final=True), True)
        except StopIteration as first:
            return {"df_world": "standard", "df_world_plus": "plus"}.get(first.value)
    return None


def find_sources(directory: Path) -> list[Path]:
    if not directory.is_dir():
        raise ValueError(f"Répertoire de sources introuvable : {directory}")
    standard = []
    plus = []
    for path in sorted(directory.rglob("*")):
        if not path.is_file() or path.suffix.lower() != ".xml":
            continue
        kind = export_kind(path)
        if kind == "standard":
            standard.append(path)
        elif kind == "plus":
            plus.append(path)
    if len(standard) > 1 or len(plus) > 1:
        raise ValueError("Plusieurs exports détectés. Fournir un seul export par branche et son éventuel legends_plus.xml.")
    if not standard and not plus:
        raise ValueError("Aucun XML Legends trouvé dans le répertoire des sources.")
    if standard and plus:
        primary, extra = standard[0].stem.lower(), plus[0].stem.lower()
        if primary.endswith("legends") and extra.endswith("legends_plus") and extra.removesuffix("_plus") != primary:
            raise ValueError("Les noms de l'export standard et du complément désignent des exports différents.")
    return standard + plus


def check_paths(sources: Path, database: Path, reports: Path) -> None:
    if (database == sources or database.is_relative_to(sources)
            or reports.is_relative_to(sources) or sources.is_relative_to(reports)
            or database.is_relative_to(reports) or reports.is_relative_to(database)):
        raise ValueError("Les sources, la base et le dossier des rapports doivent avoir des destinations distinctes.")
    if reports.exists() and any(reports.iterdir()):
        marker = reports / MANIFEST
        if not marker.is_file() or json.loads(marker.read_text(encoding="utf-8")).get("format") != FORMAT:
            raise ValueError(f"Le dossier {reports} contient déjà des fichiers. Choisir un dossier dédié aux rapports.")


def analyse(sources: Path, database: Path, reports: Path) -> None:
    sources, database, reports = (path.resolve() for path in (sources, database, reports))
    check_paths(sources, database, reports)
    xml = find_sources(sources)
    database.parent.mkdir(parents=True, exist_ok=True)
    reports.parent.mkdir(parents=True, exist_ok=True)
    # Garder la dernière analyse lisible si le nouvel export est incomplet ou illisible.
    with (tempfile.TemporaryDirectory(dir=database.parent) as db_tmp,
          tempfile.TemporaryDirectory(dir=reports.parent) as report_tmp):
        staged_db = Path(db_tmp) / "legendes.sqlite"
        staged_reports = Path(report_tmp) / "rapports"
        staged_reports.mkdir()
        build_index(xml, staged_db)
        write_reports(staged_db, staged_reports)
        with closing(sqlite3.connect(staged_db)) as conn:
            digests = dict(conn.execute("SELECT name, sha256 FROM sources"))
        manifest = {"format": FORMAT, "sources": [
            {"chemin": p.relative_to(sources).as_posix(), "sha256": digests[p.name]} for p in xml
        ]}
        (staged_reports / MANIFEST).write_text(
            json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        old_reports = Path(report_tmp) / "precedent"
        if reports.exists():
            reports.rename(old_reports)
        try:
            staged_reports.rename(reports)
            staged_db.replace(database)
        except OSError:
            if reports.exists():
                reports.rename(staged_reports)
            if old_reports.exists():
                old_reports.rename(reports)
            raise
    print(f"Index construit à partir de {len(xml)} fichier(s). Sommaire : {reports / 'README.md'}")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--sources", required=True, type=Path, help="dossier sources de la branche")
    parser.add_argument("--base", required=True, type=Path, help="base SQLite de sortie")
    parser.add_argument("--rapports", required=True, type=Path, help="dossier dédié aux rapports générés")
    args = parser.parse_args()
    try:
        analyse(args.sources, args.base, args.rapports)
    except (OSError, ValueError, expat.ExpatError, LookupError, sqlite3.Error) as exc:
        parser.exit(1, f"Analyse interrompue : {exc}\n")


if __name__ == "__main__":
    main()
