[![make.fun](https://make.fun/badge/news-image-20261120.svg)](https://make.fun/c/news-image-20261120)
[![rank](https://make.fun/badge/news-image-20261120/xingxing717/news-image-20261120/rank.svg)](https://make.fun/c/news-image-20261120)
[![reward](https://make.fun/badge/news-image-20261120/xingxing717/news-image-20261120/reward.svg)](https://make.fun/c/news-image-20261120)
20 November 2026, built for the [make.fun competition](https://make.fun/c/news-image-20261120).

# The World Today — Friday 20 November 2026

A one-page newspaper front page that sums up the world's news of
Friday 20 November 2026 in a single 1024×1024 image.

## The image

* **Masthead + date:** "THE WORLD TODAY — FRIDAY 20 NOVEMBER 2026"
* **Lead story:** Russia's overnight air assault on Kyiv — 400+ drones and
  110+ missiles, three bridges over the Dnipro struck, at least nine killed —
  with a flat vector illustration of the bridges under attack.
* **39 stories across 7 regions**, each with a headline, a one-line summary
  and its source outlet:
  * Europe & the War — Russian missiles land in Poland; Estonia closes its
    road borders with Russia; Kyiv deploys a laser air defence; UNICEF's
    child toll; Ukraine hits the Druzhba oil station.
  * Diplomacy — the Trump–Xi–Putin peace declaration in Shenzhen; the ICJ's
    genocide ruling against Myanmar; the UK–EU Brexit reset deal; Denmark's
    Greenland pact; the US–Venezuela military pact.
  * Markets — Asia's AI sell-off (Nikkei −4.8%, Kospi −5.7%); the Dow and
    S&P 500 slide into correction; Anthropic falls 11% on day two; gold and
    silver tumble; Europe follows Asia down.
  * Climate & Weather — COP31 slips into overtime with no deal and a draft
    that drops all fossil-fuel wording; Cyclone Akvan makes landfall in
    Odisha; storms flood Florida; a magnitude 6.7 quake hits Peru.
  * Middle East & Africa — the Houthi missile that hit Riyadh's PIF Tower;
    Israeli troops cross Gaza's ceasefire line; the Iran war's ninth month;
    a migrant boat capsizes off Senegal; a drone strike on a Sudan gold mine.
  * Americas — Congress fights over Iran war funding; Mamdani's plan to close
    Rikers by 2032; the Gupta sentencing; the Texas execution; the CISA
    nominee's confirmation hearing.
  * Also Today — the claimed AI-assisted Riemann proof, Voyager 1 one
    light-day away, GTA VI's voice cast, Fiona the hippo, Bukele's third-term
    bid, Bolsonaro's hospitalisation, Raoni's land, Bangladesh bracing for
    Hasina's return.

Every story was verified against reporting dated 20 November 2026 (events
that happened, or were first reported, on that day). Sources include Reuters,
AP, BBC, The New York Times, IMD, NASA, the ICJ, Human Rights Watch and
Morningstar, and are credited story by story in the image.

## How it is built

`main.py` (Python 3, Pillow) draws the whole page from scratch: masthead,
ticker, lead illustration, six section panels with small drawn glyphs, and
the "Also Today" band. All text and artwork are generated in code — no
borrowed images, no logos, no network access at runtime.

Fonts are embedded in `fonts/` (DejaVu Serif Bold, DejaVu Sans, DejaVu Sans
Bold — freely licensed) so the program renders identically anywhere.

## Run it

```sh
mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
```

Writes `entry.png` (1024×1024, PNG, well under 1 MiB). The program is fully
deterministic: no clock, no randomness, no network — two runs produce
byte-identical output (verified with sha256).

## License

MIT — see `LICENSE`.
