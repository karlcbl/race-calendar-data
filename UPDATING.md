# How races.json is kept up to date

A scheduled task updates `races.json` (daily in December and January, every three days the rest of the year). Each run follows these rules.

## What to look for

1. **Rider programmes** for every rider in `riders`: team announcements and rider interviews about which 2027 races they will ride. Team training-camp season (December–January) is when most are published.
2. **Confirmed start lists** for races starting in the next 10 days: if a listed rider is on the official start list, set their status to `"confirmed"`. If they are announced as out (injury, illness, team decision), remove that race from their programme.
3. **Route presentations** for stage races (Tour, Giro, Vuelta, Paris–Nice, women's races and so on): fill `stages` (number, date, start, finish, type) and update `locations` to the real start/finish towns with coordinates, then remove the "not announced" `locationNote`.
4. **Calendar changes**: date changes, cancellations, new races in the disciplines already in the file (road WorldTour and elite UCI races held in European countries, Worlds, UEC European Championships, cyclocross World Cup / Euros / Worlds, MTB World Cup XCO and DHI, MTB Worlds and Euros). Elite UCI races only: no junior, U23-only, amateur or regional races. Use the UCI calendar and the UEC calendar (uec.ch) as the reference for which races exist. When a UEC European Championships host is announced (road, cyclocross, MTB), add it.
5. **Broadcast rights** for Spain (`ES`) and the United States (`US`) when 2027 deals are announced.
6. **Official websites**: races may have a `website` (official race site, https) and optional `links` (list of `{"title", "url"}`, e.g. route page, start list). Add the official website for races missing one, verified from a search result, never guessed.
7. **Rider list**: if a rider moves team for 2027, update `team`. Once the 2026–27 cyclocross World Cup standings exist, re-rank the CX riders from the official standings (keep the existing ids for riders still in the top 10).

## Rules

- Only use credible sources: official team, race organiser or UCI sites, and established cycling media (Cyclingnews, Velo, Escape Collective, Domestique, Sporza, WielerFlits, Marca/AS/MARCA for Spain, etc.). No rumours or forum posts.
- `programme` values are `"planned"` (announced by the team or rider) or `"confirmed"` (on the official start list). Record the source URL in the rider's `sources` map under the race id.
- Never invent coordinates: use the town's real latitude/longitude.
- Allowed `discipline` values: `road`, `cx`, `xco`, `dhi`. Allowed `gender`: `men`, `women`, `all`. Any other value breaks the app, so never add a new discipline.
- Keep race `id`s stable. A new race gets a new id in the same style (`name-gender-2027`).
- Set `dataVersion` to the current time (`YYYY-MM-DDTHH:MM`, Europe/Madrid) whenever anything changes. If nothing changed, do not commit.
- Validate the file with `python3 tools/validate.py` before committing.
- Commit as `Claude <noreply@anthropic.com>` with a message listing the changes.

## Open work (do these as sources become available)

- **Women's elite UCI races in Europe (ProSeries and class 1: 1.1, 2.1, 1.Pro, 2.Pro).** Karl wants these alongside the men's races, but no readable 2027 women's ProSeries/class-1 calendar was available when the men's races were added (Nov 2026). Each run, check the UCI calendar and cycling media for the 2027 women's calendar and add every European women's ProSeries and class 1 race (ids `name-w-2027`, gender `women`, category `UCI ProSeries` or `UCI Europe Tour`). Skip class 2 (1.2/2.2), junior and U23 races.
- **Stage races with "end date to be confirmed"** in `locationNote` were added with `endDate` equal to `startDate`. Look up the real end date (velowire.com race pages and organiser sites list them), set `endDate`, and remove that part of the note.
- **Locations shown at a country's centre** ("Venue to be confirmed") need the real host town and coordinates once announced.
- **Check the official websites added on 2 Nov 2026.** They were filled in from memory, not from search results. On the next runs, confirm each `website` opens the race's real official site (fix or remove any that don't), a few per run until all are checked. Checked so far (4 Nov 2026): giroditalia.it, lavuelta.es, paris-roubaix.fr, uec.ch OK; Giro Women changed to giroditaliawomen.it. Checked 7 Nov 2026: strade-bianche.it, tourdownunder.com.au, ucicyclocrossworldcup.com OK.
- **Vuelta a Burgos Féminas 2027** was set to 6–10 May from EsCiclismo and CyclingUpToDate; Cyclingnews calls it a four-day race starting 6 May. Confirm the end date against the UCI calendar or the organiser. (FloBikes lists 21–24 May 2027 as of 7 Nov 2026, likely a stale placeholder; not applied.)
