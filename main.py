#!/usr/bin/env python3
"""The World Today -- one-page newspaper front page summing up the world's
news of Friday 20 November 2026.

Deterministic Pillow renderer (no network, no clock, no randomness):
reads only the embedded DejaVu fonts in ./fonts and writes a 1024x1024
PNG to $MAKEFUN_OUTPUT_DIR/entry.png (default /output/entry.png).
"""
import os
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
BASE = Path(__file__).resolve().parent

PAPER = (247, 242, 232)
INK = (20, 20, 20)
GREY = (105, 100, 92)
RULE = (60, 55, 48)
RED = (178, 32, 44)
DARKRED = (140, 20, 30)
BLUE = (28, 62, 110)
TEAL = (14, 92, 86)
GOLD = (176, 124, 20)
GREEN = (34, 96, 52)
PURPLE = (84, 52, 110)

SERIF_B = str(BASE / "fonts" / "DejaVuSerif-Bold.ttf")
SANS = str(BASE / "fonts" / "DejaVuSans.ttf")
SANS_B = str(BASE / "fonts" / "DejaVuSans-Bold.ttf")


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, width):
    """Greedy word wrap; returns list of lines that fit within width."""
    lines, cur = [], ""
    for word in text.split():
        trial = (cur + " " + word).strip()
        if draw.textlength(trial, font=fnt) <= width:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def text_w(draw, text, fnt):
    return draw.textlength(text, font=fnt)


# ---------------------------------------------------------------- stories
LEAD = {
    "kicker": "WAR IN EUROPE  •  KYIV, UKRAINE",
    "headline": "KYIV'S BRIDGES HIT IN RUSSIA'S BIGGEST AIR ASSAULT",
    "deck": ("More than 400 drones and 110 missiles rained down overnight. "
             "Three bridges over the Dnipro were struck, at least nine people "
             "were killed, and power, heating and water were cut across the "
             "capital of three million."),
    "numbers": "400+ DRONES  •  110+ MISSILES  •  9 KILLED  •  3 BRIDGES HIT",
    "source": "REUTERS",
}

SECTIONS = [
    ("EUROPE & THE WAR", BLUE, "eu", [
        ("RUSSIAN MISSILES LAND IN POLAND",
         "Two cruise missiles and a drone come down in the east; NATO calls it a grave violation.",
         "REUTERS"),
        ("ESTONIA TO CLOSE BORDERS WITH RUSSIA",
         "Tallinn cites 'sustained aggression' against Europe as it moves to close crossings.",
         "KYIV IND."),
        ("KYIV DEPLOYS LASER AIR DEFENCE",
         "An experimental laser system joins the capital's shield against the nightly drone waves.",
         "KYIV IND."),
        ("UNICEF: 1,144 CHILDREN KILLED OR HURT",
         "This year's child toll in Ukraine's war, the agency reports.",
         "UNICEF"),
        ("UKRAINE HITS DRUZHBA OIL STATION",
         "A key pipeline station is struck in Russia's Tatarstan, Kyiv's General Staff says.",
         "GEN. STAFF"),
    ]),
    ("DIPLOMACY", PURPLE, "globe", [
        ("TRUMP, XI AND PUTIN: PEACE DECLARATION",
         "First three-way summit in Shenzhen ends with four points - and no mention of Ukraine.",
         "REUTERS"),
        ("COURT: MYANMAR COMMITTED GENOCIDE",
         "The ICJ finds the state guilty over the Rohingya; reparations are ordered.",
         "HRW"),
        ("UK AND EU SEAL BREXIT RESET DEAL",
         "Food trade eased, carbon markets linked, 100,000 youth visas a year.",
         "REUTERS"),
        ("DENMARK OKAYS GREENLAND PACT",
         "A security pact for the Arctic island is approved in Copenhagen.",
         "ONE TURN"),
        ("US AND VENEZUELA SIGN MILITARY PACT",
         "Hegseth in Caracas: joint training and intelligence sharing agreed.",
         "FRONTIER MARKETS"),
    ]),
    ("MARKETS", DARKRED, "chart", [
        ("ASIA'S AI SELL-OFF DEEPENS",
         "Nikkei -4.8%, Kospi -5.7%; Taiwan heads for its worst week since 1990.",
         "REUTERS"),
        ("DOW AND S&P SLIDE INTO CORRECTION",
         "Both indexes now sit 10% below recent highs as the tech rout reaches Wall Street.",
         "NY TIMES"),
        ("ANTHROPIC SINKS ON DAY TWO",
         "The record IPO star falls 11% as doubts about AI spending swamp the market.",
         "AUGERTON"),
        ("GOLD AND SILVER TUMBLE",
         "Metals hit one-year lows as investors sell to cover losses elsewhere.",
         "MORNINGSTAR"),
        ("EUROPE FOLLOWS ASIA DOWN",
         "Stoxx 600 off 1.5%, now 5% below its record high of 12 November.",
         "REUTERS"),
    ]),
    ("CLIMATE & WEATHER", TEAL, "cyclone", [
        ("COP31 SLIPS INTO OVERTIME WITH NO DEAL",
         "Nearly 200 nations deadlocked in Antalya as the talks run past Friday.",
         "ASIA TODAY"),
        ("DRAFT DROPS ALL FOSSIL-FUEL WORDING",
         "The $120bn adaptation fund is cut too; small islands warn of a 'ghost COP'.",
         "BBC / REUTERS"),
        ("CYCLONE AKVAN MAKES LANDFALL",
         "The storm crosses India's Odisha coast at 80 km/h; heavy rain floods the east.",
         "IMD / HINDU"),
        ("STORMS FLOOD FLORIDA'S COAST",
         "Soaking rains shift north; water rescues for people and horses.",
         "AP"),
        ("MAGNITUDE 6.7 QUAKE HITS PERU",
         "A strong tremor shakes central Peru; no early casualty reports.",
         "ONE TURN"),
    ]),
    ("MIDDLE EAST & AFRICA", GOLD, "flame", [
        ("HOUTHI MISSILE HITS RIYADH'S PIF TOWER",
         "Saudi Arabia's wealth-fund HQ is damaged across several floors; no injuries.",
         "REUTERS"),
        ("ISRAELI TROOPS CROSS GAZA TRUCE LINE",
         "First ground push past the Yellow Line since the truce; Hamas protests.",
         "ONE TURN"),
        ("IRAN WAR ENTERS NINTH MONTH",
         "Hormuz tanker attacks intensify; a tanker burns after hitting a mine.",
         "ONE TURN"),
        ("BOAT CAPSIZES OFF SENEGAL",
         "A migrant boat goes down near Yenne; dozens missing, search under way.",
         "ONE TURN"),
        ("DRONE STRIKE KILLS 10 AT SUDAN MINE",
         "An attack on the Bajoun mining site in South Kordofan.",
         "ONE TURN"),
    ]),
    ("AMERICAS", GREEN, "dome", [
        ("CONGRESS FIGHTS OVER IRAN WAR FUNDS",
         "A bid to cut off money for the war before the 11 December funding deadline.",
         "AUGERTON"),
        ("MAMDANI: CLOSE RIKERS BY 2032",
         "New York's mayor unveils a plan to shut the notorious jail complex.",
         "AP"),
        ("GUPTA GETS 19 1/2 YEARS IN MURDER PLOT",
         "An Indian man is sentenced in New York over the Pannun assassination plan.",
         "AP"),
        ("TEXAS EXECUTES REINALDO DENNES",
         "The lethal injection takes over an hour as staff struggle to find a vein.",
         "AP"),
        ("CISA NOMINEE DOUBTS JAN. 6 ATTACK",
         "Trump pick LoSapio is pressed at his Senate confirmation hearing.",
         "AUGERTON"),
    ]),
]

ALSO = [
    ("CLAIM: AI CRACKED RIEMANN PUZZLE",
     "Alp\u00f6ge: Claude helped prove the riddle."),
    ("VOYAGER 1: ONE LIGHT-DAY AWAY",
     "NASA: the probe is 26bn km out."),
    ("GTA VI REVEALS ITS VOICE CAST",
     "Rockstar names the Vice City cast. (AP)"),
    ("FANS MOURN FIONA THE HIPPO",
     "Cincinnati's beloved hippo dies at 9. (AP)"),
    ("BUKELE REGISTERS FOR A THIRD TERM",
     "El Salvador's president seeks a third term."),
    ("BOLSONARO TAKEN TO HOSPITAL",
     "Brazil's ex-president hospitalised. (Rio Times)"),
    ("BRAZIL RECOGNISES RAONI'S LAND",
     "Raoni's ancestral land recognised. (One Turn)"),
    ("BANGLADESH BRACES FOR HASINA RETURN",
     "Troops out as the ousted PM returns. (Frontier)"),
]

TICKER = ("KYIV BRIDGES HIT  •  RUSSIAN MISSILES LAND IN POLAND  •  COP31: NO DEAL AS TALKS RUN INTO OVERTIME  •  "
          "ASIA'S AI ROUT: NIKKEI -4.8%  •  UK-EU RESET DEAL SEALED")


# ---------------------------------------------------------------- drawing
def draw_glyph(d, kind, cx, cy, color):
    """Small flat glyph drawn in the section header."""
    if kind == "eu":  # circle of dots
        d.ellipse([cx - 9, cy - 9, cx + 9, cy + 9], outline=color, width=2)
        for i in range(8):
            import math
            a = i * math.pi / 4
            d.ellipse([cx + 6 * math.cos(a) - 1.5, cy + 6 * math.sin(a) - 1.5,
                       cx + 6 * math.cos(a) + 1.5, cy + 6 * math.sin(a) + 1.5],
                      fill=color)
    elif kind == "globe":
        d.ellipse([cx - 9, cy - 9, cx + 9, cy + 9], outline=color, width=2)
        d.ellipse([cx - 4, cy - 9, cx + 4, cy + 9], outline=color, width=1)
        d.line([cx - 9, cy, cx + 9, cy], fill=color, width=1)
    elif kind == "chart":
        d.line([(cx - 10, cy + 7), (cx - 3, cy + 1), (cx + 2, cy + 4), (cx + 10, cy - 8)],
               fill=color, width=2)
        d.polygon([(cx + 10, cy - 8), (cx + 4, cy - 8), (cx + 10, cy - 2)], fill=color)
    elif kind == "cyclone":
        for r in (9, 6, 3):
            d.arc([cx - r, cy - r, cx + r, cy + r], 20, 300, fill=color, width=2)
    elif kind == "flame":
        d.polygon([(cx, cy - 10), (cx + 7, cy + 2), (cx + 3, cy + 8),
                   (cx - 3, cy + 8), (cx - 7, cy + 2)], fill=color)
    elif kind == "dome":
        d.pieslice([cx - 8, cy - 8, cx + 8, cy + 4], 180, 360, fill=color)
        d.rectangle([cx - 9, cy + 4, cx + 9, cy + 9], fill=color)
        d.line([cx - 10, cy + 9, cx + 10, cy + 9], fill=color, width=2)


def draw_bridge_scene(d, x, y, w, h):
    """Flat vector scene: river, three bridges, explosions, smoke."""
    d.rectangle([x, y, x + w, y + h], fill=(214, 226, 235))
    # sky band
    d.rectangle([x, y, x + w, y + 58], fill=(232, 222, 200))
    # sun
    d.ellipse([x + w - 52, y + 12, x + w - 22, y + 42], fill=(226, 178, 60))
    # distant skyline
    for bx, bw, bh in [(8, 34, 42), (48, 26, 58), (80, 40, 34), (300, 30, 50), (336, 24, 40)]:
        d.rectangle([x + bx, y + 58 - bh, x + bx + bw, y + 58], fill=(150, 148, 138))
    # river
    d.rectangle([x, y + 58, x + w, y + h], fill=(96, 138, 168))
    d.rectangle([x, y + 58, x + w, y + 66], fill=(70, 112, 142))
    # bridge decks (three spans)
    for by in (86, 122, 158):
        d.rectangle([x, y + by, x + w, y + by + 7], fill=(52, 52, 56))
        for px in range(12, w, 46):
            d.line([x + px, y + by, x + px + 18, y + by - 16], fill=(52, 52, 56), width=2)
            d.line([x + px + 18, y + by - 16, x + px + 36, y + by], fill=(52, 52, 56), width=2)
        # piers
        for px in (60, 190, 320):
            d.rectangle([x + px, y + by + 7, x + px + 10, y + h - 4], fill=(70, 70, 76))
    # explosions on two bridges
    for ex, ey, r in [(120, 92, 26), (300, 128, 30)]:
        pts = []
        import math
        for i in range(12):
            ang = i * math.pi / 6
            rr = r if i % 2 == 0 else r * 0.45
            pts.append((x + ex + rr * math.cos(ang), y + ey + rr * math.sin(ang)))
        d.polygon(pts, fill=(232, 120, 30))
        d.ellipse([x + ex - 9, y + ey - 9, x + ex + 9, y + ey + 9], fill=(250, 210, 60))
    # smoke puffs
    for sx, sy, sr in [(150, 62, 12), (168, 52, 9), (330, 98, 13), (348, 88, 9)]:
        d.ellipse([x + sx - sr, y + sy - sr, x + sx + sr, y + sy + sr], fill=(120, 118, 112))
    d.rectangle([x, y, x + w, y + h], outline=RULE, width=2)


def draw_story(d, x, y, width, headline, summary, source, max_bottom):
    """One story block; returns y after the block. Warns on overflow."""
    hf = font(SANS_B, 12)
    sf = font(SANS, 10)
    srcf = font(SANS_B, 8)
    lines = wrap(d, headline, hf, width)
    for ln in lines[:2]:
        d.text((x, y), ln, font=hf, fill=INK)
        y += 15
    slines = wrap(d, summary, sf, width - 62)
    for i, ln in enumerate(slines[:2]):
        d.text((x, y), ln, font=sf, fill=(52, 50, 46))
        if i == min(len(slines[:2]), 2) - 1:
            sx = x + text_w(d, ln, sf) + 5
            d.text((sx, y + 1), "\u00b7 " + source, font=srcf, fill=GREY)
        y += 13
    if y > max_bottom:
        print(f"OVERFLOW in story: {headline[:40]}", file=sys.stderr)
    return y + 1


def render():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # ---- masthead
    d.text((W // 2, 16), "ONE DAY  •  ONE PAGE  •  THE WHOLE WORLD",
           font=font(SANS_B, 11), fill=GREY, anchor="ma")
    d.text((W // 2, 34), "THE WORLD TODAY", font=font(SERIF_B, 56),
           fill=INK, anchor="ma")
    d.line([16, 100, 1008, 100], fill=RULE, width=2)
    d.line([16, 104, 1008, 104], fill=RULE, width=1)
    d.text((16, 110), "FRIDAY 20 NOVEMBER 2026", font=font(SANS_B, 16), fill=RED)
    d.text((1008, 110), "39 STORIES  •  7 REGIONS", font=font(SANS_B, 13),
           fill=INK, anchor="ra")

    # ---- ticker
    d.rectangle([16, 134, 1008, 160], fill=DARKRED)
    tf = font(SANS_B, 12)
    while text_w(d, TICKER, tf) > 976 and tf.size > 9:
        tf = font(SANS_B, tf.size - 1)
    d.text((W // 2, 140), TICKER, font=tf, fill=(255, 255, 255), anchor="ma")

    # ---- lead story
    lx, ly, lw = 16, 170, 592
    d.text((lx, ly), LEAD["kicker"], font=font(SANS_B, 11), fill=RED)
    hl = wrap(d, LEAD["headline"], font(SERIF_B, 29), lw)
    y = ly + 20
    for ln in hl:
        d.text((lx, y), ln, font=font(SERIF_B, 29), fill=INK)
        y += 34
    dl = wrap(d, LEAD["deck"], font(SANS, 13), lw)
    y += 4
    for ln in dl:
        d.text((lx, y), ln, font=font(SANS, 13), fill=(52, 50, 46))
        y += 17
    y += 6
    d.text((lx, y), LEAD["numbers"], font=font(SANS_B, 12), fill=BLUE)
    y += 20
    d.text((lx, y), "SOURCE: " + LEAD["source"], font=font(SANS_B, 9), fill=GREY)
    draw_bridge_scene(d, 624, 170, 384, 196)

    # ---- section grid: 3 cols x 2 rows
    gx, gy = 16, 374
    pw, ph, gap = 325, 272, 8
    for idx, (title, color, glyph, stories) in enumerate(SECTIONS):
        col, row = idx % 3, idx // 3
        px = gx + col * (pw + gap)
        py = gy + row * (ph + gap)
        d.rectangle([px, py, px + pw, py + ph], fill=(255, 253, 247),
                    outline=RULE, width=1)
        d.rectangle([px, py, px + pw, py + 28], fill=color)
        draw_glyph(d, glyph, px + 16, py + 14, (255, 255, 255))
        d.text((px + 30, py + 7), title, font=font(SANS_B, 13),
               fill=(255, 255, 255))
        y = py + 36
        for i, (h, s, src) in enumerate(stories):
            y = draw_story(d, px + 10, y, pw - 20, h, s, src, py + ph - 6)
            if i < len(stories) - 1:
                d.line([px + 10, y + 1, px + pw - 10, y + 1], fill=(214, 208, 196), width=1)
                y += 2

    # ---- also today band
    ay = 934
    d.rectangle([16, ay, 1008, ay + 66], fill=(255, 253, 247), outline=RULE, width=1)
    d.rectangle([16, ay, 1008, ay + 20], fill=INK)
    d.text((26, ay + 4), "ALSO TODAY", font=font(SANS_B, 11), fill=(255, 255, 255))
    d.text((1008 - 10, ay + 4), "SCIENCE  •  CULTURE  •  THE AMERICAS",
           font=font(SANS_B, 10), fill=(200, 200, 200), anchor="ra")
    colw = 992 / 4
    for i, (h, s) in enumerate(ALSO):
        col, row = i % 4, i // 4
        ax = 26 + col * colw
        ayy = ay + 22 + row * 20
        hf = font(SANS_B, 9)
        sf = font(SANS, 9)
        avail = colw - 14
        h2 = h
        while text_w(d, h2, hf) > avail and len(h2) > 4:
            h2 = h2[:-2]
        if h2 != h:
            h2 = h2.rstrip() + "…"
        d.text((ax, ayy), h2, font=hf, fill=INK)
        s2 = s
        while text_w(d, s2, sf) > avail and len(s2) > 4:
            s2 = s2[:-2]
        if s2 != s:
            s2 = s2.rstrip() + "…"
        d.text((ax, ayy + 10), s2, font=sf, fill=(52, 50, 46))

    # ---- footer
    d.line([16, 1006, 1008, 1006], fill=RULE, width=1)
    d.text((W // 2, 1011),
           "SOURCES: REUTERS  •  AP  •  BBC  •  NY TIMES  •  IMD  •  NASA  •  ICJ  •  HRW  •  MORNINGSTAR  —  ALL STORIES HAPPENED OR WERE FIRST REPORTED ON FRIDAY 20 NOVEMBER 2026",
           font=font(SANS, 9), fill=GREY, anchor="ma")
    return img


def main():
    outdir = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))
    outdir.mkdir(parents=True, exist_ok=True)
    img = render()
    out = outdir / "entry.png"
    img.save(out, format="PNG", optimize=True)
    print(f"wrote {out} ({out.stat().st_size} bytes)")


if __name__ == "__main__":
    main()
