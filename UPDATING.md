# How races.json is kept up to date

A scheduled task updates `races.json` (daily in December and January, every three days the rest of the year). Each run follows these rules.

## What to look for

1. **Rider programmes** for every rider in `riders`: team announcements and rider interviews about which 2027 races they will ride. Team training-camp season (December–January) is when most are published.
2. **Confirmed start lists** for races starting in the next 10 days: if a listed rider is on the official start list, set their status to `"confirmed"`. If they are announced as out (injury, illness, team decision), remove that race from their programme.
3. **Route presentations** for stage races (Tour, Giro, Vuelta, Paris–Nice, women's races and so on): fill `stages` (number, date, start, finish, type) and update `locations` to the real start/finish towns with coordinates, then remove the "not announced" `locationNote`.
4. **Calendar changes**: date changes, cancellations, new races in the disciplines already in the file (road WorldTour, Worlds, cyclocross World Cup / Euros / Worlds, MTB World Cup XCO and DHI, MTB Worlds).
5. **Broadcast rights** for Spain (`ES`) and the United States (`US`) when 2027 deals are announced.
6. **Rider list**: if a rider moves team for 2027, update `team`. Once the 2026–27 cyclocross World Cup standings exist, re-rank the CX riders from the official standings (keep the existing ids for riders still in the top 10).

## Rules

- Only use credible sources: official team, race organiser or UCI sites, and established cycling media (Cyclingnews, Velo, Escape Collective, Domestique, Sporza, WielerFlits, Marca/AS/MARCA for Spain, etc.). No rumours or forum posts.
- `programme` values are `"planned"` (announced by the team or rider) or `"confirmed"` (on the official start list). Record the source URL in the rider's `sources` map under the race id.
- Never invent coordinates: use the town's real latitude/longitude.
- Allowed `discipline` values: `road`, `cx`, `xco`, `dhi`. Allowed `gender`: `men`, `women`, `all`. Any other value breaks the app, so never add a new discipline.
- Keep race `id`s stable. A new race gets a new id in the same style (`name-gender-2027`).
- Set `dataVersion` to the current time (`YYYY-MM-DDTHH:MM`, Europe/Madrid) whenever anything changes. If nothing changed, do not commit.
- Validate the file with `python3 tools/validate.py` before committing.
- Commit as `Claude <noreply@anthropic.com>` with a message listing the changes.
