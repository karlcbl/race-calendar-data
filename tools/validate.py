"""Checks races.json matches what the RaceCalendar app can read. Exit code 1 on any problem."""
import json, re, sys

path = sys.argv[1] if len(sys.argv) > 1 else "races.json"
d = json.load(open(path, encoding="utf-8"))
errors = []
DISC, GEN = {"road", "cx", "xco", "dhi"}, {"men", "women", "all"}
DATE = re.compile(r"^\d{4}-\d{2}-\d{2}$")

for key in ("schemaVersion", "dataVersion", "viewingCountries", "riders", "races"):
    if key not in d:
        errors.append(f"missing top-level key {key}")

race_ids = set()
for r in d.get("races", []):
    rid = r.get("id", "?")
    if rid in race_ids:
        errors.append(f"duplicate race id {rid}")
    race_ids.add(rid)
    for k in ("id", "name", "discipline", "gender", "category", "startDate", "endDate",
              "countryCode", "country", "organizer", "locations", "stages", "watch"):
        if k not in r:
            errors.append(f"{rid}: missing {k}")
    if r.get("discipline") not in DISC:
        errors.append(f"{rid}: bad discipline {r.get('discipline')}")
    if r.get("gender") not in GEN:
        errors.append(f"{rid}: bad gender {r.get('gender')}")
    for k in ("startDate", "endDate"):
        if not DATE.match(str(r.get(k, ""))):
            errors.append(f"{rid}: bad {k}")
    if r.get("startDate", "") > r.get("endDate", ""):
        errors.append(f"{rid}: starts after it ends")
    for loc in r.get("locations", []):
        if not all(k in loc for k in ("name", "role", "lat", "lon")):
            errors.append(f"{rid}: location missing fields")
        elif not (-90 <= loc["lat"] <= 90 and -180 <= loc["lon"] <= 180):
            errors.append(f"{rid}: bad coordinates for {loc['name']}")
    for s in r.get("stages", []):
        if not all(k in s for k in ("number", "date", "start", "finish")):
            errors.append(f"{rid}: stage missing fields")

for rider in d.get("riders", []):
    rid = rider.get("id", "?")
    for k in ("id", "name", "team", "gender", "discipline", "programme"):
        if k not in rider:
            errors.append(f"rider {rid}: missing {k}")
    if rider.get("gender") not in {"men", "women"}:
        errors.append(f"rider {rid}: bad gender")
    if rider.get("discipline") not in DISC:
        errors.append(f"rider {rid}: bad discipline")
    for race, status in rider.get("programme", {}).items():
        if race not in race_ids:
            errors.append(f"rider {rid}: unknown race {race}")
        if status not in ("planned", "confirmed"):
            errors.append(f"rider {rid}: bad status {status} for {race}")

if errors:
    print("\n".join(errors))
    sys.exit(1)
print(f"OK: {len(d['races'])} races, {len(d['riders'])} riders, version {d['dataVersion']}")
