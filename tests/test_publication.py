import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


SCRIPT = Path(__file__).resolve().parents[1] / "outils" / "ci_legendes.py"


class PublicationTests(unittest.TestCase):
    def test_keeps_concurrent_chapter_and_refuses_stale_xml(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            remote = root / "depot.git"
            local = root / "travail"
            local.mkdir()

            def git(*args):
                return subprocess.run(["git", *args], cwd=local, check=True, capture_output=True,
                                      text=True).stdout.strip()

            git("init", "--bare", str(remote))
            git("init", "-b", "main")
            git("config", "user.name", "Tests")
            git("config", "user.email", "tests@example.org")
            git("remote", "add", "origin", str(remote))
            git("commit", "--allow-empty", "-m", "Méthode commune")
            git("push", "origin", "main")
            main = git("rev-parse", "HEAD")
            branch = "legendes/test"
            git("switch", "-c", branch)
            (local / "sources").mkdir()
            xml = local / "sources" / "legends.xml"
            xml.write_text("<df_world/>", encoding="utf-8")
            git("add", "sources")
            git("commit", "-m", "Premier export")
            git("push", "origin", branch)
            source_commit = git("rev-parse", "HEAD")
            env = dict(os.environ, BRANCHE=branch, RUNNER_TEMP=temp, COMMIT_SOURCE=source_commit,
                       COMMIT_POUSSE=source_commit, GITHUB_OUTPUT=str(root / "resultat"))

            def run_ci(action):
                return subprocess.run([sys.executable, str(SCRIPT), action], cwd=local,
                                      env=env, text=True, capture_output=True)

            self.assertEqual(run_ci("preparer").returncode, 0)
            reports = root / "legends-ci" / "publication" / "reperes" / "index-legends"
            reports.mkdir(parents=True)
            (reports / "README.md").write_text("Premier relevé", encoding="utf-8")
            (local / "chapitre.md").write_text("Nouveau chapitre", encoding="utf-8")
            git("add", "chapitre.md")
            git("commit", "-m", "Écriture pendant l’analyse")
            git("push", "origin", branch)

            publication = run_ci("publier")
            self.assertEqual(publication.returncode, 0, publication.stderr)
            git("fetch", "origin", branch)
            self.assertEqual(git("show", "FETCH_HEAD:chapitre.md"), "Nouveau chapitre")
            self.assertEqual(git("show", "FETCH_HEAD:reperes/index-legends/README.md"), "Premier relevé")
            git("merge", "--ff-only", "FETCH_HEAD")
            # En mode éditorial, un nouveau chapitre sous manuscrits invalide les dossiers déjà calculés.
            chapter = local / "manuscrits/fr/P901/01.md"
            chapter.parent.mkdir(parents=True)
            chapter.write_text("# Chapitre 1", encoding="utf-8")
            git("add", "manuscrits")
            git("commit", "-m", "Ouverture")
            git("push", "origin", branch)
            env["DOSSIERS"] = "1"
            self.assertNotEqual(run_ci("publier").returncode, 0)
            del env["DOSSIERS"]

            xml.write_text("<df_world><sites/></df_world>", encoding="utf-8")
            git("commit", "-am", "Nouvel export")
            git("push", "origin", branch)
            next_commit = git("rev-parse", "HEAD")
            self.assertNotEqual(run_ci("publier").returncode, 0)
            self.assertEqual(git("ls-remote", "origin", "refs/heads/" + branch).split()[0], next_commit)
            self.assertEqual(git("ls-remote", "origin", "refs/heads/main").split()[0], main)


if __name__ == "__main__":
    unittest.main()
