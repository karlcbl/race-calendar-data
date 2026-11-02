# race-calendar-data

Data file for the RaceCalendar iPhone app: the 2027 UCI road, cyclocross and mountain bike calendar, race locations, where to watch (Spain / US) and top riders' race programmes.

The app downloads `races.json` from this repository on launch and every few hours in the background. When `dataVersion` changes, it compares the new file with the old one and sends alerts for new races, date changes, published routes and rider programme changes.

- `races.json` – the live data file the app reads
- `tools/build_data.py` – script that generated the initial calendar

Bump `dataVersion` (ISO date/time, e.g. `2026-11-02T13:10`) on every change so the app picks it up.
