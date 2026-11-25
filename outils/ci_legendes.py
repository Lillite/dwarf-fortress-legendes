"""Prélever les sources Git d'un monde et y publier les seuls rapports produits."""

import hashlib
import json
import os
import re
import subprocess
import sys
from pathlib import Path


REPORTS = "reperes/index-legends"


def git(*args, **kwargs):
    return subprocess.run(["git", *args], check=True, **kwargs)


def git_text(*args, **kwargs):
    return git(*args, stdout=subprocess.PIPE, text=True, **kwargs).stdout.strip()


def fetch(ref):
    git("fetch", "--no-tags", "--depth=1", "--quiet", "origin", ref)
    return git_text("rev-parse", "FETCH_HEAD^{commit}")


def input_blobs(commit, editorial=False):
    paths = ["sources"]
    if editorial:
        paths.extend(["manuscrits", "reperes/occurrences.csv", "reperes/chronologie.csv",
                      "reperes/glossaire.csv", "reperes/pistes.md", "SPEC_Roman_Dwarf_Fortress.md"])
    entries = git("ls-tree", "-rz", commit, "--", *paths, stdout=subprocess.PIPE)
    blobs = {}
    for entry in entries.stdout.split(b"\0"):
        if not entry:
            continue
        meta, name = entry.split(b"\t", 1)
        relative = Path(os.fsdecode(name))
        if relative.parts[0] == "sources" and relative.suffix.lower() != ".xml":
            continue
        if relative.parts[0] == "manuscrits" and relative.suffix.lower() != ".md":
            continue
        mode, kind, sha = meta.split()
        if kind != b"blob" or mode not in {b"100644", b"100755"}:
            raise SystemExit(f"Entrée non régulière dans Git : {relative!s}")
        blobs[relative] = sha.decode("ascii")
    return blobs


def prepare(ref, work):
    commit = fetch(os.environ.get("COMMIT_POUSSE") or ref)
    editorial = os.environ.get("DOSSIERS") == "1"
    blobs = input_blobs(commit, editorial)
    xml = {p.as_posix():digest for p,digest in blobs.items() if p.parts[0]=="sources"}
    if editorial:
        listing = git("ls-tree","-rz","--name-only",commit,stdout=subprocess.PIPE)
        (work/".fichiers-git").write_bytes(listing.stdout)
    key = hashlib.sha256(json.dumps(xml,sort_keys=True).encode()).hexdigest()
    for relative, sha in blobs.items():
        target = work / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        with target.open("wb") as output:
            git("cat-file", "blob", sha, stdout=output)
    with open(os.environ["GITHUB_OUTPUT"], "a", encoding="utf-8") as output:
        print("commit=" + commit, file=output)
        print("xml=" + str(bool(xml)).lower(), file=output)
        print("cle_xml=" + key, file=output)
    print(f"{len(xml)} fichier(s) XML au commit {commit}.")


def publish(ref, work):
    source = os.environ["COMMIT_SOURCE"]
    editorial = os.environ.get("DOSSIERS") == "1"
    inputs = input_blobs(source, editorial)
    has_xml = any(p.parts[0]=="sources" for p in inputs)
    publish_dir = work / "publication"
    publish_dir.mkdir(parents=True, exist_ok=True)
    if has_xml and not any(path.is_file() for path in (publish_dir / REPORTS).rglob("*")):
        raise SystemExit("L’analyse ne contient aucun rapport à publier.")

    index_env = dict(os.environ, GIT_INDEX_FILE=str(work / "index"),
                     GIT_WORK_TREE=str(publish_dir), GIT_DIR=git_text("rev-parse", "--absolute-git-dir"))
    for _ in range(3):
        tip = fetch(ref)
        if tip != source and input_blobs(tip, editorial) != inputs:
            raise SystemExit("Les données de l’analyse ont changé pendant cette exécution. Relancer sur le nouveau commit.")
        existing = git_text("ls-tree", tip, "--", REPORTS)
        if not has_xml and not existing:
            print("Aucun export ni ancien rapport sur cette branche.")
            return

        # L'index temporaire conserve tous les autres chemins du dernier commit,
        # y compris les modifications de manuscrits intervenues pendant le calcul.
        git("read-tree", tip, env=index_env)
        git("add", "-f", "-A", "--", REPORTS, cwd=publish_dir, env=index_env)
        tree = git_text("write-tree", env=index_env)
        if tree == git_text("rev-parse", tip + "^{tree}"):
            print("Les rapports publiés sont déjà à jour.")
            return
        message = "Actualiser les rapports Legends" if has_xml else "Retirer les rapports de l’export supprimé"
        commit = git_text("-c", "user.name=github-actions[bot]", "-c",
                          "user.email=41898282+github-actions[bot]@users.noreply.github.com",
                          "commit-tree", tree, "-p", tip, "-m", message, "-m", f"Source : {source}")
        # Le parent est exactement tip. Le bail interdit aussi de ressusciter une
        # branche supprimée entre fetch et push.
        result = subprocess.run(["git", "push", "--porcelain", f"--force-with-lease={ref}:{tip}",
                                 "origin", f"{commit}:{ref}"])
        if result.returncode == 0:
            print(f"Rapports publiés au commit {commit}.")
            return
        if fetch(ref) == tip:
            raise SystemExit("Le dépôt a refusé la publication des rapports.")
    raise SystemExit("La branche a changé pendant les trois tentatives de publication. Relancer l’analyse.")


def changes(work):
    """Un rapport de comparaison par exécution, indépendant des fichiers indexés durables."""
    current = os.environ["COMMIT_SOURCE"]
    before = os.environ.get("DEPUIS") or ""
    if before and set(before) != {"0"}:
        if not re.fullmatch(r"[0-9a-fA-F]{40}", before):
            raise ValueError("Le point de comparaison doit être un SHA Git complet.")
        before = fetch(before)
    else:
        before = current
    directory = work / "comparaison"
    directory.mkdir(exist_ok=True)
    dep = "reperes/index-legends/dossiers/dependances.json"
    prior = git_text("ls-tree", before, "--", dep)
    after = json.loads((work / "publication" / dep).read_text(encoding="utf-8"))
    lines = ["# Impact des modifications", "", f"Référence {before}. Source analysée {current}.", ""]
    if prior:
        earlier = json.loads(git_text("show", f"{before}:{dep}"))
        for key in sorted(earlier.keys() | after.keys()):
            prev, new = earlier.get(key, {}), after.get(key, {})
            if prev != new:
                scope = sorted(
                    set(
                        prev.get("pistes", [])
                        + new.get("pistes", [])
                        + prev.get("chapitres", [])
                        + new.get("chapitres", [])
                    )
                )
                lines.append("- " + key + " · " + ", ".join(scope))
        if len(lines) == 4:
            lines.append("Aucune dépendance structurée modifiée.")
    else:
        lines.append(
            "Première référence disponible. Les dépendances courantes serviront à la comparaison suivante."
        )
    (directory / "impact.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    if before != current:
        with (directory / "passages.diff").open("wb") as f:
            git(
                "diff",
                "--no-ext-diff",
                "--no-textconv",
                "--unified=2",
                before,
                current,
                "--",
                "manuscrits",
                stdout=f,
            )


def main():
    branch = os.environ["BRANCHE"]
    ref = "refs/heads/" + branch
    if not branch.startswith("legendes/"):
        raise SystemExit("Le nom de branche doit commencer par legendes/.")
    git("check-ref-format", ref)
    work = Path(os.environ["RUNNER_TEMP"]) / "legends-ci"
    work.mkdir(exist_ok=True)
    if sys.argv[1:] == ["preparer"]:
        prepare(ref, work)
    elif sys.argv[1:] == ["comparer"]:
        changes(work)
    elif sys.argv[1:] == ["publier"]:
        publish(ref, work)
    else:
        raise SystemExit("Usage : ci_legendes.py {preparer|comparer|publier}")


if __name__ == "__main__":
    main()
