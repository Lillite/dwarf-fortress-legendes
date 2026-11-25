import csv
import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

TOOLS = Path(__file__).resolve().parents[1] / "outils"
sys.path.insert(0, str(TOOLS))
from dossiers_pistes import generate
from journal_tokens import merge, receipt, visible_measure
from legends_index import build_index
from legends_rapports import _open
from test_legendes import STANDARD


def write_csv(path, columns, rows):
    with path.open("w", encoding="utf-8", newline="") as stream:
        w = csv.writer(stream)
        w.writerow(columns.split())
        w.writerows(rows)


class EditorialTests(unittest.TestCase):
    def test_sources_deduplicated_distinct_roles_and_chapter(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            world = root / "monde"
            (world / "sources").mkdir(parents=True)
            study = world / "reperes"
            study.mkdir()
            book = world / "manuscrits/fr/P001"
            book.mkdir(parents=True)
            (book / "01.md").write_text("# Chapitre 1\n\nLe récit commence au gué.\n", encoding="utf-8")
            (book / "plan.md").write_text("Décision du chapitre, événement 70.\n", encoding="utf-8")
            (study / "pistes.md").write_text("## P001\n\n## P007\n", encoding="utf-8")
            xml = world / "sources" / "a-legends.xml"
            xml.write_bytes(STANDARD.encode("cp437"))
            db_path = root / "a.sqlite"
            build_index([xml], db_path)
            write_csv(
                study / "occurrences.csv",
                "piste evenement_id champs_qui_relient_la_notice",
                [
                    ("P001", 70, "motif commun"),
                    ("P001", 90, "motif commun"),
                    ("P007", 70, "autre motif"),
                    ("P007", 99999, "à vérifier"),
                ],
            )
            write_csv(
                study / "chronologie.csv",
                "reference_evenement chapitres_associes date_dans_le_monde",
                [
                    ("historical_events/70", "manuscrits/fr/P001/01.md", "an 4"),
                    ("historical_event_collections/16", "manuscrits/fr/P001/01.md", ""),
                ],
            )
            dest = root / "rapport"
            db = _open(db_path)
            try:
                generate(db, world, dest, "SPEC test")
            finally:
                db.close()
            summary = (dest / "P001.md").read_text()
            self.assertEqual(summary.count("motif commun"), 1)
            self.assertIn("[70](notices/70.md)", summary)
            self.assertIn("[90](notices/90.md)", summary)
            self.assertIn("[P007](P007.md)", summary)
            self.assertTrue((dest / "notices/collection-16.md").is_file())
            self.assertIn("Décision du chapitre", (dest / "scenes/fr/P001/01.md").read_text())
            self.assertIn("99999", (dest / "controles.md").read_text())
            self.assertIn("0.md absente", (dest / "controles.md").read_text())
            deps = json.loads((dest / "dependances.json").read_text())
            self.assertEqual(deps["70"]["pistes"], ["P001", "P007"])
            self.assertEqual(deps["70"]["chapitres"], ["manuscrits/fr/P001/01.md"])


class TokenTests(unittest.TestCase):
    def test_incomplete_retry_complete_and_partial_counters(self):
        b = "legendes/test"
        raw = {
            "id": "resp_A",
            "model": "modele",
            "output": "texte à exclure",
            "usage": {
                "input_tokens": 90,
                "output_tokens": 10,
                "total_tokens": 100,
                "input_tokens_details": {"cached_tokens": 50},
                "output_tokens_details": {"reasoning_tokens": 2},
            },
        }
        r = receipt(raw)
        self.assertNotIn("output", r)
        empty = merge(None, b, "edition", None, [], False)
        self.assertIsNone(empty["total_demande"])
        partial = merge(empty, b, "edition", "P001", [r, r], False)
        self.assertEqual(partial["sous_total_appels_mesurés"], 100)
        self.assertIsNone(partial["total_demande"])
        measured = merge(partial, b, "edition", "P001", [r], True)
        self.assertEqual(measured["total_demande"], 100)
        self.assertEqual(merge(measured, b, "edition", None, [r], False), measured)
        r2 = receipt(
            {"id": "chatcmpl_B", "usage": {"prompt_tokens": 2, "completion_tokens": 3, "total_tokens": 5}}
        )
        self.assertEqual(merge(measured, b, "edition", None, [r2], True)["total_demande"], 105)
        with self.assertRaises(ValueError):
            merge(measured, b, "edition", None, [dict(r, total=999)], True)
        with self.assertRaises(ValueError):
            receipt({"id": "resp", "usage": {"input_tokens": 2, "output_tokens": 1, "total_tokens": 5}})
        with self.assertRaises(ValueError):
            merge(None, b, "edition", None, [], True)

    def test_visible_indication_accepts_only_token_counts(self):
        counts = {"encodage": "o200k_base", "message_utilisateur": 20, "reponse_finale": 30}
        self.assertEqual(visible_measure(counts), dict(counts, total_visible=50))
        for bad in (
            {"texte": "privé"},
            dict(counts, reponse_finale=-1),
            dict(counts, message_utilisateur=True),
            dict(counts, texte="privé"),
            [],
        ):
            with self.subTest(bad=bad), self.assertRaises(ValueError):
                visible_measure(bad)

    def test_manual_ci_only_writes_the_requested_branch_and_file(self):
        with tempfile.TemporaryDirectory() as temp:
            repo = Path(temp) / "repo"
            repo.mkdir()

            def run(*args, env=None, check=True):
                return subprocess.run(args, cwd=repo, capture_output=True, text=True, check=check, env=env)

            remote = Path(temp) / "remote.git"
            run("git", "init", "--bare", str(remote))
            run("git", "init", "-b", "main")
            run(
                "git",
                "-c",
                "user.name=Test",
                "-c",
                "user.email=test@example.org",
                "commit",
                "--allow-empty",
                "-m",
                "Méthode",
            )
            start = run("git", "rev-parse", "HEAD").stdout.strip()
            run("git", "remote", "add", "origin", str(remote))
            run("git", "push", "origin", "main", "HEAD:refs/heads/legendes/test")
            cli = [sys.executable, str(TOOLS / "journal_tokens.py"), "--ci", "--demande", "reprise-2"]
            env = dict(os.environ, BRANCHE="legendes/test", COMPLET="false", RECUS="")
            run(*cli, env=env)

            def tip(name):
                return run("git", "ls-remote", "origin", "refs/heads/" + name).stdout.split()[0]

            first = tip("legendes/test")
            run(*cli, env=env)
            self.assertEqual(tip("legendes/test"), first)
            run("git", "fetch", "origin", "legendes/test")
            p = "reperes/usage-llm/reprise-2.json"
            data = json.loads(run("git", "show", "FETCH_HEAD:" + p).stdout)
            self.assertEqual(data["statut"], "indisponible")
            self.assertIsNone(data["total_demande"])
            self.assertEqual(run("git", "diff", "--name-only", start, "FETCH_HEAD").stdout.strip(), p)
            self.assertEqual(tip("main"), start)
            second_env = dict(
                env,
                BRANCHE="main",
                INDICATION=json.dumps(
                    {
                        "encodage": "o200k_base",
                        "message_utilisateur": 3,
                        "reponse_finale": 4,
                    }
                ),
            )
            run(*cli, env=second_env)
            main_first = tip("main")
            entry = "suivi/usage-llm/reprise-2.json"
            self.assertEqual(run("git", "diff", "--name-only", start, main_first).stdout.strip(), entry)
            data = json.loads(run("git", "show", main_first + ":" + entry).stdout)
            self.assertEqual(data["branche"], "main")
            self.assertEqual(data["indication_visible"]["total_visible"], 7)
            self.assertIsNone(data["total_demande"])
            run(*cli, env=second_env)
            self.assertEqual(tip("main"), main_first)

            # Une nouvelle demande a ses propres compteurs. Les changements locaux ne partent pas avec elle.
            pending = repo / "travail-en-cours.md"
            pending.write_text("brouillon")
            run("git", "add", pending.name)
            recu = Path(temp) / "appel.json"
            recu.write_text(
                json.dumps(
                    {
                        "id": "nouvel_appel",
                        "usage": {
                            "input_tokens": 9,
                            "output_tokens": 2,
                            "total_tokens": 11,
                        },
                    }
                )
            )
            run(
                sys.executable,
                str(TOOLS / "journal_tokens.py"),
                "--publier",
                "--branche",
                "main",
                "--demande",
                "autre",
                "--recu",
                str(recu),
                "--complet",
            )
            second = "suivi/usage-llm/autre.json"
            main_second = tip("main")
            self.assertEqual(run("git", "diff", "--name-only", main_first, main_second).stdout.strip(), second)
            new = json.loads(run("git", "show", main_second + ":" + second).stdout)
            self.assertEqual(new["total_demande"], 11)
            self.assertNotIn("indication_visible", new)
            self.assertEqual(run("git", "diff", "--cached", "--name-only").stdout.strip(), pending.name)
            self.assertEqual(tip("legendes/test"), first)
            self.assertNotEqual(run(*cli, "--piste", "P014", env=second_env, check=False).returncode, 0)
            self.assertNotEqual(run(*cli, env=dict(env, BRANCHE="autre"), check=False).returncode, 0)
            self.assertEqual(tip("main"), main_second)
