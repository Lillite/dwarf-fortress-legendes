import csv
import hashlib
import io
import json
import sqlite3
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


CLI = Path(__file__).resolve().parents[1] / "outils" / "analyser_legendes.py"

# IDs repeat across categories. Two distinct figures deliberately share a name.
STANDARD = """<?xml version="1.0" encoding="CP437"?>
<df_world>
  <sites>
    <site><id>7</id><name>gué</name></site>
    <site><id>8</id><name>fort</name></site>
  </sites>
  <entities>
    <entity><id>5</id><name>guilde</name></entity>
    <entity><id>6</id><name>clan</name></entity>
  </entities>
  <historical_figures>
    <historical_figure><id>7</id><name>ada</name></historical_figure>
    <historical_figure><id>8</id><name>ada</name></historical_figure>
  </historical_figures>
  <artifacts>
    <artifact><id>7</id><name>\x11épée\x10</name></artifact>
    <artifact><id>28</id><name>livre</name><item><page_written_content_id>7</page_written_content_id></item></artifact>
  </artifacts>
  <written_contents>
    <written_content><id>7</id><title>Le gué</title><author_hfid>7</author_hfid></written_content>
  </written_contents>
  <historical_events>
    <historical_event>
      <id>70</id><year>4</year><seconds72>101</seconds72><type>attacked site</type>
      <site_id>7</site_id><attacker_civ_id>5</attacker_civ_id><defender_civ_id>6</defender_civ_id>
      <attacker_general_hfid>7</attacker_general_hfid><defender_general_hfid>8</defender_general_hfid>
    </historical_event>
    <historical_event>
      <id>90</id><year>30</year><seconds72>800</seconds72><type>attacked site</type>
      <site_id>8</site_id><attacker_civ_id>6</attacker_civ_id><defender_civ_id>5</defender_civ_id>
      <attacker_general_hfid>-1</attacker_general_hfid><defender_general_hfid>7</defender_general_hfid>
    </historical_event>
    <historical_event>
      <id>120</id><year>31</year><seconds72>-1</seconds72><type>entity persecuted</type>
      <expelled_hfid>7</expelled_hfid><expelled_hfid>8</expelled_hfid>
      <site_id>999</site_id><wrongful_conviction/>
    </historical_event>
    <historical_event><id>150</id><year>40</year><type>written content composed</type>
      <hist_figure_id>7</hist_figure_id><wc_id>7</wc_id><site_id>7</site_id>
    </historical_event>
    <historical_event><id>160</id><year>41</year><type>change hf state</type>
      <hfid>7</hfid><state>settled</state><site_id>7</site_id>
    </historical_event>
    <historical_event><id>161</id><year>42</year><type>destroyed site</type><site_id>7</site_id></historical_event>
    <historical_event><id>162</id><year>45</year><type>change hf state</type>
      <hfid>7</hfid><state>settled</state><site_id>7</site_id>
    </historical_event>
    <historical_event><id>163</id><year>42</year><seconds72>-1</seconds72><type>change hf state</type>
      <hfid>8</hfid><state>settled</state><site_id>7</site_id>
    </historical_event>
    <historical_event><id>164</id><year>45</year><type>change hf state</type>
      <hfid>8</hfid><state>settled</state><site_id>7</site_id>
    </historical_event>
  </historical_events>
  <historical_event_collections>
    <historical_event_collection><id>15</id><type>war</type><name>la guerre</name>
      <eventcol>16</eventcol><eventcol>17</eventcol>
    </historical_event_collection>
    <historical_event_collection><id>16</id><type>battle</type><name>au gué</name>
      <event>70</event><war_eventcol>15</war_eventcol><site_id>7</site_id><outcome>attacker won</outcome>
    </historical_event_collection>
    <historical_event_collection><id>17</id><type>battle</type><name>au fort</name>
      <event>90</event><war_eventcol>15</war_eventcol><site_id>8</site_id><outcome>defender won</outcome>
    </historical_event_collection>
  </historical_event_collections>
</df_world>
"""

PLUS = """<?xml version="1.0" encoding="UTF-8"?>
<df_world>
  <historical_events>
    <historical_event><id>70</id><year>4</year><type>attacked site</type>
      <attacker_general_hfid>7</attacker_general_hfid>
    </historical_event>
  </historical_events>
</df_world>
"""


class IndexLegendsTests(unittest.TestCase):
    def setUp(self):
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        root = Path(tmp.name)
        self.sources = root / "sources"
        self.sources.mkdir()
        self.original = self.sources / "region-test-legends.xml"
        self.raw = STANDARD.replace("\n", "\r\n").encode("cp437")
        self.original.write_bytes(self.raw)
        (self.sources / "region-test-legends_plus.xml").write_text(PLUS, encoding="utf-8")
        self.database = root / "legendes.sqlite"
        self.reports = root / "rapports"

    def run_cli(self, success=True):
        run = subprocess.run(
            [sys.executable, str(CLI), "--sources", str(self.sources),
             "--base", str(self.database), "--rapports", str(self.reports)],
            stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, check=False,
        )
        if success:
            self.assertEqual(run.returncode, 0, run.stdout)
        else:
            self.assertNotEqual(run.returncode, 0, run.stdout)

    def report_rows(self, name):
        with (self.reports / name).open(encoding="utf-8-sig", newline="") as stream:
            return list(csv.DictReader(stream))

    def test_namespaces_source_locations_and_ambiguous_references(self):
        self.run_cli()
        self.assertEqual(self.original.read_bytes(), self.raw)
        manifest = json.loads((self.reports / "manifest.json").read_text(encoding="utf-8"))
        self.assertEqual(
            {item["chemin"]: item["sha256"] for item in manifest["sources"]},
            {p.name: hashlib.sha256(p.read_bytes()).hexdigest() for p in self.sources.iterdir()},
        )
        db = sqlite3.connect(self.database)
        self.addCleanup(db.close)
        self.assertEqual(db.execute("SELECT name FROM records WHERE category='artifact' AND id=7").fetchone(),
                         ("◄épée►",))
        self.assertEqual(db.execute("SELECT name FROM records WHERE category='site' AND id=7").fetchone(),
                         ("gué",))
        self.assertEqual(db.execute("SELECT count(*) FROM records WHERE category='historical_event' AND id=70").fetchone(),
                         (1,))
        locations = db.execute("""SELECT source, line FROM refs
            WHERE category='historical_event' AND owner_id=70 AND path='attacker_general_hfid'
              AND target_category='historical_figure' AND target_id=7""").fetchall()
        self.assertEqual({name for name, _ in locations}, {path.name for path in self.sources.iterdir()})
        for source, line in locations:
            self.assertIn(b"<attacker_general_hfid>7", (self.sources / source).read_bytes().splitlines()[line - 1])
        expelled = db.execute("""SELECT target_id FROM refs WHERE category='historical_event'
            AND owner_id=120 AND path='expelled_hfid' ORDER BY ordinal""").fetchall()
        self.assertEqual(expelled, [(7,), (8,)])
        self.assertTrue(db.execute("""SELECT 1 FROM fields WHERE category='historical_event'
            AND owner_id=120 AND path='wrongful_conviction'""").fetchone())
        self.assertTrue(db.execute("""SELECT 1 FROM issues WHERE category='historical_event'
            AND owner_id=120 AND path='site_id' AND value='999'""").fetchone())
        self.assertFalse(db.execute("SELECT 1 FROM refs WHERE target_id=-1").fetchone())

    def test_battles_use_ids_and_roles_across_sources_and_reruns(self):
        self.run_cli()
        self.assertTrue((self.reports / "README.md").is_file())
        csv_name = "commandements.csv"
        original_csv = (self.reports / csv_name).read_bytes()
        battles = self.report_rows(csv_name)
        self.assertEqual([row["evenement_id"] for row in battles], ["70", "90"])
        self.assertEqual([row["guerre_id"] for row in battles], ["15", "15"])
        self.assertEqual([row["bataille_id"] for row in battles], ["16", "17"])
        self.assertEqual([row["site"] for row in battles], ["gué", "fort"])
        self.assertEqual([row["issue_xml"] for row in battles], ["attacker won", "defender won"])
        figures = self.report_rows("chefs-attaque-defense.csv")
        self.assertEqual([row["figure_id"] for row in figures], ["7"])
        self.assertEqual((figures[0]["batailles_attaque"], figures[0]["batailles_defense"]), ("1", "1"))
        self.run_cli()
        self.assertEqual((self.reports / csv_name).read_bytes(), original_csv)

    def test_incomplete_xml_preserves_previous_analysis(self):
        self.run_cli()
        manifest = (self.reports / "manifest.json").read_bytes()
        database = self.database.read_bytes()
        self.original.write_bytes(b"<df_world><historical_events>")
        self.run_cli(success=False)
        self.assertEqual((self.reports / "manifest.json").read_bytes(), manifest)
        self.assertEqual(self.database.read_bytes(), database)

    def test_works_and_settlements_keep_distinct_evidence(self):
        self.run_cli()
        works = self.report_rows("oeuvres.csv")
        self.assertEqual(len(works), 1)
        work = works[0]
        self.assertEqual((work["titre"], work["auteurs_id"], work["evenements_composition"],
                          work["nombre_objets"], work["artefacts_id"]), ("Le gué", "7", "150", "1", "28"))
        returns = self.report_rows("retours.csv")
        self.assertEqual(returns, [{"site_id": "7", "figure_id": "7", "installation_avant": "160",
                                    "destruction": "161", "installation_apres": "162"}])

    def test_track_reader_counts_only_explicit_distinct_events(self):
        self.run_cli()
        register = self.database.parent / "occurrences.csv"
        register.write_text("piste,evenement_id\nP014,90\nP015,70\nP014,70\nP014,90\nP014,7\n",
                            encoding="utf-8-sig")
        command = [sys.executable, str(CLI.with_name("lire_pistes.py")), str(self.database), str(register)]
        summary = subprocess.run(command, capture_output=True, text=True, check=True)
        rows = {r["type_xml"]: r for r in csv.DictReader(io.StringIO(summary.stdout), delimiter="\t")}
        self.assertEqual(rows["attacked site"], {"type_xml": "attacked site", "notices_monde": "2",
                         "notices_citees_dans_le_csv": "2", "exemple_non_cite": ""})
        self.assertEqual(rows["entity persecuted"]["exemple_non_cite"], "120")
        self.assertIn("7", summary.stderr)  # Figure 7 exists, historical event 7 does not.
        selected = subprocess.run([*command, "--piste", "P014"], capture_output=True, text=True, check=True)
        entries = list(csv.DictReader(io.StringIO(selected.stdout), delimiter="\t"))
        self.assertEqual([r["evenement_id"] for r in entries], ["70", "90", "7"])
        self.assertEqual([r["statut"] for r in entries], ["trouvé", "trouvé", "introuvable"])
        self.assertEqual((entries[0]["annee"], entries[0]["source"]), ("4", self.original.name))
        self.assertGreater(int(entries[0]["ligne"]), 0)
        command[2] = str(self.database.with_name("absente.sqlite"))
        self.assertNotEqual(subprocess.run(command, capture_output=True).returncode, 0)
        self.assertFalse(Path(command[2]).exists())


if __name__ == "__main__":
    unittest.main()
