"""Consigner uniquement les compteurs de consommation d'une demande sur la branche concernée."""

import argparse
import hashlib
import json
import os
import re
import subprocess
import tempfile
from datetime import datetime, timezone
from pathlib import Path

from ci_legendes import git, git_text

WORLD_JOURNAL = Path("reperes/usage-llm")
MAIN_JOURNAL = Path("suivi/usage-llm")
KEY = re.compile(r"[A-Za-z0-9][A-Za-z0-9._-]{0,119}\Z")


def journal_for(branch):
    if branch == "main-story-writer":
        return MAIN_JOURNAL
    if branch.startswith("legendes/"):
        return WORLD_JOURNAL
    raise ValueError("Le journal appartient à main-story-writer ou à une branche legendes/.")


def safe(value, label):
    if not isinstance(value, str) or not KEY.fullmatch(value):
        raise ValueError(f"{label} doit être un identifiant alphanumérique court.")
    return value


def meter(value, label):
    if type(value) is not int or value < 0:
        raise ValueError(f"Compteur absent ou invalide : {label}.")
    return value


def receipt(raw):
    usage = raw.get("usage")
    if not isinstance(usage, dict):
        raise ValueError("Reçu sans compteurs usage. Utiliser le mode indisponible.")
    rid = safe(raw.get("id"), "id de réponse")
    model = raw.get("model")
    if model is not None and (not isinstance(model, str) or not re.fullmatch(r"[a-zA-Z0-9._:/-]{1,160}", model)):
        raise ValueError("Identifiant du modèle invalide.")
    responses = "input_tokens" in usage
    i, o = ("input_tokens", "output_tokens") if responses else ("prompt_tokens", "completion_tokens")
    inp, out, total = (meter(usage.get(k), k) for k in (i, o, "total_tokens"))
    if inp + out != total:
        raise ValueError("Le total du reçu diffère de la somme entrée + sortie.")
    result = {"id": rid, "modele": model, "entree": inp, "sortie": out, "total": total}
    for source_key, name, limit in (
        (i + "_details", "cached_tokens", inp),
        (o + "_details", "reasoning_tokens", out),
    ):
        detail = usage.get(source_key) or {}
        if not isinstance(detail, dict):
            raise ValueError("Détail de compteur invalide : " + source_key)
        if name in detail and detail[name] is not None:
            value = meter(detail[name], name)
            if value > limit:
                raise ValueError(f"{name} dépasse le compteur dont il fait partie.")
            result[name] = value
    return result


def merge(previous, branch, key, track, receipts, complete):
    stamp = datetime.now(timezone.utc).date().isoformat()
    result = (
        previous.copy()
        if previous
        else {"branche": branch, "demande": key, "date_utc": stamp, "piste": track, "appels": []}
    )
    if result["branche"] != branch or result["demande"] != key or (track and result["piste"] not in (None, track)):
        raise ValueError("Le reçu existant désigne une autre demande, piste ou branche.")
    if track:
        result["piste"] = track
    calls = {r["id"]: r for r in result["appels"]}
    old = set(calls)
    for r in receipts:
        if r["id"] in calls and calls[r["id"]] != r:
            raise ValueError("Deux mesures différentes pour la même réponse : " + r["id"])
        calls[r["id"]] = r
    if complete and not calls:
        raise ValueError("Un total complet demande au moins un reçu.")
    confirmed = complete or (result.get("statut") == "mesuré" and set(calls) == old)
    result["statut"] = "mesuré" if confirmed else ("partiel" if calls else "indisponible")
    result["appels"] = [calls[k] for k in sorted(calls)]
    result["sous_total_appels_mesurés"] = sum(r["total"] for r in calls.values()) if calls else None
    result["total_demande"] = result["sous_total_appels_mesurés"] if confirmed else None
    return result


def compter_texte(path, encoding):
    try:
        import tiktoken
    except ImportError as exc:
        raise ValueError("Pour mesurer un texte visible, installer le module optionnel tiktoken.") from exc
    raw = path.read_bytes()
    codec = tiktoken.get_encoding(encoding)
    return {
        "sha256": hashlib.sha256(raw).hexdigest(),
        "encodage": codec.name,
        "tokens_texte_visible": len(codec.encode_ordinary(raw.decode("utf-8-sig"))),
    }


def visible_measure(values):
    if not isinstance(values, dict) or set(values) != {"encodage", "message_utilisateur", "reponse_finale"}:
        raise ValueError("L’indication visible attend encodage, message_utilisateur et reponse_finale.")
    encoding = safe(values["encodage"], "encodage")
    user = meter(values["message_utilisateur"], "message_utilisateur")
    answer = meter(values["reponse_finale"], "reponse_finale")
    return {
        "encodage": encoding,
        "message_utilisateur": user,
        "reponse_finale": answer,
        "total_visible": user + answer,
    }


def encode(value):
    return json.dumps(value, indent=2, ensure_ascii=False) + "\n"


def from_env():
    payload = json.loads(os.environ.get("RECUS") or "[]")
    return payload if isinstance(payload, list) else [payload]


def remote_tip(ref):
    # FETCH_HEAD est partagé entre les processus du même clone. Lire le SHA de la branche demandée.
    tip = git_text("ls-remote", "--refs", "--exit-code", "origin", ref).split()[0]
    if subprocess.run(["git", "cat-file", "-e", tip + "^{commit}"], stderr=subprocess.DEVNULL).returncode:
        depth = ["--depth=1"] if git_text("rev-parse", "--is-shallow-repository") == "true" else []
        git("fetch", "--quiet", "--no-tags", "--no-write-fetch-head", *depth, "origin", tip)
    return tip


def write_ci(ref, path, update):
    # Mise à jour d'un seul blob depuis la branche de méthode, sans exécuter de code du monde.
    for _ in range(3):
        tip = remote_tip(ref)
        for parent in (path.parent.parent, path.parent):
            ancestor = git_text("ls-tree", tip, "--", parent)
            if ancestor and not ancestor.startswith("040000 tree "):
                raise ValueError(f"Emplacement du journal non ordinaire : {parent}.")
        prior = git_text("ls-tree", tip, "--", path)
        if prior and not prior.startswith("100644 blob "):
            raise ValueError("Entrée du journal non régulière.")
        old = git_text("show", f"{tip}:{path}") if prior else ""
        new = encode(update(json.loads(old) if old else None))
        if new.strip() == old:
            return
        blob = git_text("hash-object", "-w", "--stdin", input=new)
        with tempfile.TemporaryDirectory() as tmp:
            env = dict(os.environ, GIT_INDEX_FILE=str(Path(tmp) / "index"))
            git("read-tree", tip, env=env)
            git("update-index", "--add", "--cacheinfo", f"100644,{blob},{path}", env=env)
            tree = git_text("write-tree", env=env)
        commit = git_text(
            "-c",
            "user.name=github-actions[bot]",
            "-c",
            "user.email=41898282+github-actions[bot]@users.noreply.github.com",
            "commit-tree",
            tree,
            "-p",
            tip,
            "-m",
            "Consigner les compteurs de la demande " + path.stem,
        )
        run = subprocess.run(["git", "push", f"--force-with-lease={ref}:{tip}", "origin", f"{commit}:{ref}"])
        if run.returncode == 0:
            head = remote_tip(ref)
            saved = json.loads(git_text("show", f"{head}:{path}"))
            if saved == json.loads(new):
                return
            # Une autre publication a pu enrichir la fiche avant la relecture.
            continue
        if remote_tip(ref) == tip:
            raise ValueError("Publication du journal refusée sur la branche demandée.")
    raise ValueError("La branche a changé pendant la publication. La demande peut être rejouée.")


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument(
        "--demande", required=True, help="identifiant stable de la demande, réutilisé pour tous ses appels"
    )
    p.add_argument("--piste")
    p.add_argument("--publier", action="store_true", help="publier et vérifier uniquement la fiche sur origin")
    p.add_argument("--branche", help="branche cible avec --publier (par défaut, la branche courante)")
    p.add_argument("--message-utilisateur", type=Path, help="texte UTF-8 du seul message courant")
    p.add_argument("--reponse-finale", type=Path, help="texte UTF-8 de la réponse finale préparée")
    p.add_argument(
        "--recu", action="append", default=[], type=Path, help="réponse API JSON ou objet minimal id/model/usage"
    )
    p.add_argument(
        "--texte", type=Path, action="append", default=[], help="fichier UTF-8 visible à mesurer séparément"
    )
    p.add_argument("--encodage", help="encodage tiktoken explicite des textes, par exemple o200k_base")
    p.add_argument("--complet", action="store_true", help="tous les appels de cette demande sont comptabilisés")
    p.add_argument("--ci", action="store_true", help=argparse.SUPPRESS)
    args = p.parse_args()
    try:
        key = safe(args.demande, "demande")
        if args.piste and not re.fullmatch(r"P\d+", args.piste):
            raise ValueError("Identifiant de piste invalide.")
        if args.branche and not args.publier:
            raise ValueError("--branche s’utilise avec --publier.")
        branch = os.environ["BRANCHE"] if args.ci else (args.branche or git_text("branch", "--show-current"))
        journal = journal_for(branch)
        if journal == MAIN_JOURNAL and args.piste:
            raise ValueError("Une piste appartient au journal de sa branche XML.")
        ref = "refs/heads/" + branch
        git("check-ref-format", ref)
        if args.ci:
            payload = from_env()
        else:
            payload = [json.loads(f.read_text(encoding="utf-8")) for f in args.recu]
        if not all(isinstance(r, dict) for r in payload):
            raise ValueError("Un reçu JSON par appel est attendu.")
        measured = [receipt(r) for r in payload]
        complete = args.complet or (args.ci and os.environ.get("COMPLET") == "true")
        if bool(args.message_utilisateur) != bool(args.reponse_finale):
            raise ValueError("Fournir le message courant et la réponse finale ensemble.")
        if bool(args.texte or args.message_utilisateur) != bool(args.encodage):
            raise ValueError("Associer les textes à leur --encodage de référence.")
        visible = None
        if args.message_utilisateur:
            visible = visible_measure(
                {
                    "encodage": args.encodage,
                    "message_utilisateur": compter_texte(args.message_utilisateur, args.encodage)[
                        "tokens_texte_visible"
                    ],
                    "reponse_finale": compter_texte(args.reponse_finale, args.encodage)["tokens_texte_visible"],
                }
            )
        elif args.ci and os.environ.get("INDICATION"):
            visible = visible_measure(json.loads(os.environ["INDICATION"]))
        texts = [compter_texte(path, args.encodage) for path in args.texte]

        def update(old):
            result = merge(old, branch, key, args.piste or None, measured, complete)
            counts = {(t["sha256"], t["encodage"]): t for t in result.get("textes_visibles", []) + texts}
            if visible is not None:
                result["indication_visible"] = visible
            if counts:
                result["textes_visibles"] = [counts[k] for k in sorted(counts)]
            return result

        path = journal / (key + ".json")
        if args.ci or args.publier:
            write_ci(ref, path, update)
        else:
            root = Path(git_text("rev-parse", "--show-toplevel"))
            dest = root / path
            if dest.resolve() != dest:
                raise ValueError("Le journal doit être un fichier ordinaire de la branche.")
            dest.parent.mkdir(parents=True, exist_ok=True)
            # Une demande unique par fichier. Refuser des écritures locales simultanées sur la même demande.
            with tempfile.TemporaryDirectory(dir=dest.parent) as tmp:
                lock = dest.with_suffix(".lock")
                with lock.open("x"):
                    pass
                try:
                    old = json.loads(dest.read_text(encoding="utf-8")) if dest.exists() else None
                    staged = Path(tmp) / "recu.json"
                    staged.write_text(encode(update(old)), encoding="utf-8")
                    os.replace(staged, dest)
                finally:
                    lock.unlink(missing_ok=True)
        print(path)
    except (OSError, ValueError, KeyError, subprocess.CalledProcessError) as exc:
        p.exit(1, f"Journal : {exc}\n")


if __name__ == "__main__":
    main()
