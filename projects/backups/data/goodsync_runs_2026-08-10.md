# GoodSync — poslední běhy jobů (stav 2026-08-10)

Ručně opsáno z GUI GoodSyncu. **Automaticky se to zjistit nedá** — `jobs.tic` časy
neobsahuje, logy je nevedou po jobech a stavové složky v `_mirrors_` jsou pojmenované
podle cesty, ne podle jobu, takže je několik jobů sdílí. Seznam jobů samotný generuje
`scripts/goodsync_jobs.py`.

| Job | Poslední běh |
|---|---|
| Projects - Ntb | 2026-08-09 20:04 |
| Electronics - Ntb | 2026-08-09 19:18 |
| Others - Ntb | 2026-08-09 19:18 |
| SVN - Ntb | 2026-08-09 19:15 |
| Work - Ntb | 2026-08-09 19:14 |
| Stock - DB | 2026-08-09 19:16 |
| Projects - Cloud | 2026-07-26 21:39 |
| AppData - Disk WD | 2026-07-26 21:24 |
| Projects - Disk WD | 2026-07-26 19:52 |
| Others - Cloud | 2026-07-26 19:45 |
| Work - Cloud | 2026-07-26 19:40 |
| Others - Disk WD | 2026-07-26 19:40 |
| OneDrive - Projects | 2026-07-26 19:40 |
| Electronics - Cloud | 2026-07-26 19:35 |
| Photos - Cloud | 2026-07-26 19:34 |
| Photos XXX - Cloud | 2026-07-26 19:34 |
| Work - Disk WD | 2026-07-26 19:34 |
| Electronics - Disk WD | 2026-07-26 19:32 |
| Photos - Disk WD | 2026-07-26 19:32 |
| Photos XXX - Disk WD | 2026-07-26 19:32 |
| SVN - Cloud | 2026-07-26 19:31 |
| OneDrive - Electronics | 2026-07-26 19:31 |
| OneDrive - Others | 2026-07-26 19:31 |
| SVN - Disk WD | 2026-07-26 19:29 |
| OneDrive - Work | 2026-07-26 19:29 |
| OneDrive - Photos | 2026-07-26 19:28 |
| OneDrive - SVN | 2026-07-26 19:28 |
| OneDrive - Ledneony | 2026-02-01 20:17 |
| OneDrive - School | 2026-02-01 20:18 |
| Monika - Ntb | 2025-07-27 20:21 |

## Co z toho plyne

- **Notebookové joby běží denně** (2026-08-09), zbytek naposled **2026-07-26** —
  15 dní. Cíle `M:` (MyCloud) a USB disk se tedy neaktualizují průběžně, ale dávkami.
- `OneDrive - Ledneony` a `OneDrive - School` naposled **2026-02-01**, přes 6 měsíců.
  Navíc `D:\Led neons` a `D:\School` **nemají job na MyCloud ani na USB** — existují
  jen na `D:` a v OneDrive.
- `Monika - Ntb` neběžel rok (`L:` je odpojený notebook).
