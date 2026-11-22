"""Retrouve les notices liées à un identifiant dans une base Legends existante."""

import argparse
import sqlite3
from pathlib import Path

from legends_rapports import write_dossier


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("base", type=Path)
    parser.add_argument("categorie", help="catégorie XML, par exemple historical_figure")
    parser.add_argument("identifiant", type=int)
    parser.add_argument("--sortie", required=True, type=Path, help="fichier Markdown dédié au dossier")
    args = parser.parse_args()
    if not args.base.is_file():
        parser.error(f"Base SQLite introuvable : {args.base}")
    if args.base.resolve() == args.sortie.resolve():
        parser.error("Le fichier de sortie doit être distinct de la base.")
    try:
        args.sortie.parent.mkdir(parents=True, exist_ok=True)
        write_dossier(args.base, args.categorie, args.identifiant, args.sortie)
    except (ValueError, OSError, sqlite3.Error, KeyError) as exc:
        parser.exit(1, f"Dossier indisponible : {exc}\n")


if __name__ == "__main__":
    main()
