"""Index de lecture d'un export Legends. Seule la bibliothèque standard est requise."""
import codecs
import hashlib
import os
import re
import sqlite3
import tempfile
from collections import Counter, defaultdict
from contextlib import closing
from pathlib import Path
from xml.parsers import expat


SCHEMA = """
CREATE TABLE sources(name TEXT PRIMARY KEY, sha256 TEXT, encoding TEXT);
CREATE TABLE sections(source TEXT, section TEXT, entries INTEGER, value TEXT);
CREATE TABLE records(category TEXT, id INTEGER, type TEXT, name TEXT, year INTEGER,
    seconds72 INTEGER, source TEXT NOT NULL, line INTEGER, PRIMARY KEY(category,id));
CREATE TABLE fields(source TEXT, category TEXT, owner_id INTEGER, path TEXT,
    ordinal INTEGER, value TEXT, line INTEGER, scope TEXT);
CREATE TABLE refs(source TEXT, category TEXT, owner_id INTEGER, path TEXT,
    ordinal INTEGER, target_category TEXT, target_id INTEGER, line INTEGER, scope TEXT);
CREATE TABLE structures(source TEXT, site_id INTEGER, local_id INTEGER, name TEXT, type TEXT, line INTEGER);
CREATE TABLE structure_refs(source TEXT, category TEXT, owner_id INTEGER, path TEXT,
    ordinal INTEGER, site_id INTEGER, local_id INTEGER, line INTEGER);
CREATE TABLE issues(source TEXT, category TEXT, owner_id INTEGER, path TEXT, value TEXT, reason TEXT);
"""
INDEXES = """
CREATE INDEX fields_owner ON fields(category,owner_id,path);
CREATE INDEX refs_owner ON refs(category,owner_id,path);
CREATE INDEX refs_target ON refs(target_category,target_id,category);
CREATE INDEX records_type ON records(category,type);
INSERT INTO issues
    SELECT r.source,r.category,r.owner_id,r.path,CAST(r.target_id AS TEXT),'cible absente : ' || r.target_category
    FROM refs r LEFT JOIN records t ON t.category=r.target_category AND t.id=r.target_id
    WHERE t.id IS NULL;
CREATE INDEX structures_target ON structures(site_id,local_id);
CREATE INDEX structure_refs_target ON structure_refs(site_id,local_id);
INSERT INTO issues
    SELECT r.source,r.category,r.owner_id,r.path,CAST(r.local_id AS TEXT),'structure absente du site ' || r.site_id
    FROM structure_refs r WHERE NOT EXISTS (SELECT 1 FROM structures s
    WHERE s.site_id=r.site_id AND s.local_id=r.local_id);
CREATE INDEX issues_owner ON issues(category,owner_id);
"""
# Identifiers never cross categories. The spelling is significant (wc_id != wcid).
ALIASES = {
    "historical_figure": ("hfid", "hf_id", "hfid1", "hfid2", "hfid_target", "hist_figure_id",
        "hist_fig_id"),
    "entity": ("enid", "entity_id", "entity_1", "entity_2", "entity_id_1", "entity_id_2", "civ_id",
        "religion_id", "aggressor_ent_id", "defender_ent_id"),
    "site": ("site_id", "site_id1", "site_id2", "site_id_1", "site_id_2",
        "attacking_squad_site", "defending_squad_site"),
    "artifact": ("artifact_id", "holds_artifact"),
    "region": ("region_id", "subregion_id", "pop_srid"),
    "written_content": ("wc_id", "written_content_id"),
    "world_construction": ("wcid", "master_wcid", "world_construction_id"),
    "entity_population": ("ent_pop_id", "expelled_pop_id", "attacking_squad_entity_pop",
        "defending_squad_entity_pop"),
}
EXACT = {name: category for category, names in ALIASES.items() for name in names}
SUFFIXES = {"_hfid": "historical_figure", "_hist_figure_id": "historical_figure",
            "_enid": "entity", "_entity_id": "entity", "_civ_id": "entity", "_site_id": "site",
            "_artifact_id": "artifact", "_written_content_id": "written_content"}
STRUCTURE_SITE = {"structure_id": "site_id", "structure_local_id": "site_id",
                  "source_structure_id": "source_site_id", "dest_structure_id": "dest_site_id"}
COLLECTION = {"event": "historical_event", "eventcol": "historical_event_collection",
              "parent_eventcol": "historical_event_collection", "war_eventcol": "historical_event_collection"}
FORM = {"poem": "poetic_form", "poetic form created": "poetic_form", "musical form created": "musical_form",
        "dance form created": "dance_form", "musical composition": "musical_form", "choreography": "dance_form"}
ID_LIKE = re.compile(r"(?:^id$|_id(?:_?\d+)?$|hfid$|enid$|_eppid$)")
XML_ENCODING = re.compile(br"""<\?xml\s+[^?]*?encoding\s*=\s*["']([^"']+)["']""", re.I)


def target_category(category, path, event_type, form):
    key = path.rsplit("/", 1)[-1]
    if category == "historical_event_collection" and key in COLLECTION:
        return COLLECTION[key]
    if key == "form_id":
        return FORM.get(event_type) or FORM.get(form)
    if key == "site_hfid":  # Ambiguous exported role; retain the exact field.
        return None
    if category == "historical_figure" and path == "honor_entity/entity":
        return "entity"
    if key in EXACT:
        return EXACT[key]
    for suffix, target in SUFFIXES.items():
        if key.endswith(suffix):
            return target
    return None


def number(value):
    try:
        return int(value)
    except (TypeError, ValueError):
        return None


def encoding_of(prefix):
    if prefix.startswith((codecs.BOM_UTF32_BE, codecs.BOM_UTF32_LE)):
        return "utf-32"
    if prefix.startswith((codecs.BOM_UTF16_BE, codecs.BOM_UTF16_LE)):
        return "utf-16"
    if prefix.startswith(codecs.BOM_UTF8):
        return "utf-8-sig"
    if prefix.startswith(b'\x00<\x00?'):
        return "utf-16-be"
    if prefix.startswith(b'<\x00?\x00'):
        return "utf-16-le"
    declared = XML_ENCODING.match(prefix)
    return codecs.lookup(declared[1].decode("ascii") if declared else "utf-8").name


class Node:
    __slots__ = ("tag", "line", "parts", "children", "attrs")

    def __init__(self, tag, line, attrs):
        self.tag = tag
        self.line = line
        self.parts = []
        self.children = []
        self.attrs = attrs

    def value(self):
        return "".join(self.parts).strip()


def leaves(node, prefix="", scope=""):
    """Include occurrence indices in scope so an optional sibling cannot shift a relationship."""
    counts = Counter()
    for ch in node.children:
        path = prefix + ch.tag
        occurrence = counts[ch.tag]
        counts[ch.tag] += 1
        address = f"{scope}/{ch.tag}[{occurrence}]" if scope else f"{ch.tag}[{occurrence}]"
        for key, val in ch.attrs.items():
            yield path + "/@" + key, val, ch.line, address
        if ch.children:
            yield from leaves(ch, path + "/", address)
        if not ch.children or ch.value():
            yield path, ch.value(), ch.line, scope


def site_structures(conn, filename, node, site_id):
    for group in node.children:
        if group.tag != "structures":
            continue
        for entry in group.children:
            values = {ch.tag: ch.value() for ch in entry.children}
            local_id = number(values.get("local_id"))
            if entry.tag == "structure" and local_id is not None and local_id >= 0:
                conn.execute("INSERT INTO structures VALUES (?,?,?,?,?,?)",
                             (filename, site_id, local_id, values.get("name"), values.get("type"), entry.line))


def write_record(conn, filename, node, synthetic):
    category = node.tag
    direct = {ch.tag: ch.value() for ch in node.children if not ch.children}
    record_id = number(direct.get("id"))
    if record_id is None:
        if direct.get("id") is not None:
            raise ValueError(f"{filename}:{node.line} identifiant invalide : {direct['id']!r}")
        # Some records (eras, for example) are anonymous. Their ids are local to this build.
        synthetic[category] -= 1
        record_id = synthetic[category] - 1
    event_type = direct.get("type")
    name = direct.get("name") or direct.get("title")
    when = number(direct.get("year", direct.get("start_year")))
    seconds = number(direct.get("seconds72", direct.get("start_seconds72")))
    if seconds == -1:
        seconds = None
    if category == "site":
        site_structures(conn, filename, node, record_id)
    prefix = (filename, category, record_id)
    raw, refs, issues, structure_refs = [], [], [], []
    ordinals = Counter()
    form = direct.get("form")
    for path, value, line, scope in leaves(node):
        ordinal = ordinals[path]
        ordinals[path] += 1
        raw.append((*prefix, path, ordinal, value, line, scope))
        if not name and path == "item/name_string":
            name = value or None
        if path == "id":
            continue
        if category == "site" and path == "structures/structure/local_id":
            continue
        site_field = STRUCTURE_SITE.get(path)
        if site_field and category in ("artifact", "historical_event"):
            site = number(direct.get(site_field))
            local_id = number(value)
            if local_id == -1:
                continue
            if site is not None and site >= 0 and local_id is not None and local_id >= 0:
                structure_refs.append((*prefix, path, ordinal, site, local_id, line))
                continue
        target = target_category(category, path, event_type, form)
        key = path.rsplit("/", 1)[-1]
        if target is None:
            if ID_LIKE.search(key) and value not in ("", "-1"):
                issues.append((*prefix, path, value, "identifiant local ou champ non interprété"))
            continue
        target_id = number(value)
        if target_id is None:
            issues.append((*prefix, path, value, "référence non numérique"))
        elif target_id >= 0:
            refs.append((*prefix, path, ordinal, target, target_id, line, scope))

    conn.execute("""INSERT INTO records VALUES (?,?,?,?,?,?,?,?) ON CONFLICT(category,id)
        DO UPDATE SET type=coalesce(records.type,excluded.type),name=coalesce(records.name,excluded.name),
        year=coalesce(records.year,excluded.year),seconds72=coalesce(records.seconds72,excluded.seconds72)""",
        (category, record_id, event_type or None, name, when, seconds, filename, node.line))
    conn.executemany("INSERT INTO fields VALUES (?,?,?,?,?,?,?,?)", raw)
    conn.executemany("INSERT INTO structure_refs VALUES (?,?,?,?,?,?,?,?)", structure_refs)
    conn.executemany("INSERT INTO refs VALUES (?,?,?,?,?,?,?,?,?)", refs)
    conn.executemany("INSERT INTO issues VALUES (?,?,?,?,?,?)", issues)
    return record_id


def read_source(conn, path, synthetic):
    parser = expat.ParserCreate("UTF-8")
    parser.buffer_text = True
    stack = []
    entries = 0
    seen_records = set()

    def start(tag, attrs):
        nonlocal entries
        if not stack and tag not in ("df_world", "df_world_plus"):
            raise ValueError(f"{path.name}: racine Legends inconnue : {tag}")
        if len(stack) == 1:
            entries = 0
        node = Node(tag, parser.CurrentLineNumber, attrs)
        if len(stack) >= 3:
            stack[-1].children.append(node)
        stack.append(node)

    def data(value):
        if stack and (len(stack) >= 3 or value.strip()):
            stack[-1].parts.append(value)

    def end(_tag):
        nonlocal entries
        node = stack.pop()
        if len(stack) == 2:
            record_id = write_record(conn, path.name, node, synthetic)
            record = (node.tag, record_id)
            if record in seen_records:
                raise ValueError(f"{path.name}:{node.line} identifiant dupliqué : {record}")
            seen_records.add(record)
            entries += 1
        elif len(stack) == 1:
            conn.execute("INSERT INTO sections VALUES (?,?,?,?)", (path.name, node.tag, entries, node.value()))

    def reject_doctype(*_args):
        raise ValueError(f"{path.name}: déclaration DTD non prise en charge")

    parser.StartElementHandler = start
    parser.EndElementHandler = end
    parser.CharacterDataHandler = data
    parser.StartDoctypeDeclHandler = reject_doctype
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        chunk = stream.read(64 * 1024)
        encoding = encoding_of(chunk[:1024])
        decoder = codecs.getincrementaldecoder(encoding)()
        while chunk:
            digest.update(chunk)
            decoded = decoder.decode(chunk)
            if encoding == "cp437":
                decoded = decoded.replace("\x10", "►").replace("\x11", "◄")
            parser.Parse(decoded, False)
            chunk = stream.read(64 * 1024)
        parser.Parse(decoder.decode(b"", final=True), True)
    conn.execute("INSERT INTO sources VALUES (?,?,?)", (path.name, digest.hexdigest(), encoding))


def build_index(sources: list[Path], database: Path):
    """Build one world's index atomically; keep the original XML and any previous successful index intact."""
    if not sources:
        raise ValueError("Aucun export XML fourni")
    database = Path(database)
    sources = [Path(p) for p in sources]
    if database.resolve() in (p.resolve() for p in sources):
        raise ValueError("La destination correspond à une source XML")
    if len({p.name for p in sources}) != len(sources):
        raise ValueError("Deux sources ont le même nom")
    database.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile(dir=database.parent, prefix=".legends-", suffix=".sqlite", delete=False) as tmp:
        temp = Path(tmp.name)
    try:
        with closing(sqlite3.connect(temp)) as conn:
            conn.execute("PRAGMA journal_mode=OFF")
            conn.executescript(SCHEMA)
            synthetic = defaultdict(int)
            for path in sorted(sources, key=lambda p: p.stem.lower().endswith("legends_plus")):
                try:
                    read_source(conn, path, synthetic)
                except (expat.ExpatError, UnicodeError, LookupError) as exc:
                    raise ValueError(f"{path.name}: {exc}") from exc
            conn.executescript(INDEXES)
            conn.commit()
        os.replace(temp, database)
    finally:
        temp.unlink(missing_ok=True)
