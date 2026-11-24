#!/usr/bin/env python3
"""news-23 b77 front-page-dense: draw THE WORLD TODAY, Monday 23 November 2026."""
from PIL import Image, ImageDraw, ImageFont
import os

W, H = 1024, 1024
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")

SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SERIF_R = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"

def F(path, size):
    return ImageFont.truetype(path, size)

BLACK = (17, 17, 17)
PAPER = (247, 243, 234)
WHITE = (255, 255, 255)
RED = (166, 25, 46)
GOLD = (201, 162, 39)
GOLD_L = (232, 196, 90)
NAVY = (27, 42, 74)
TEAL = (15, 95, 92)
CREAM = (242, 234, 216)
GRAY = (90, 90, 90)
LGRAY = (210, 210, 210)
MAPGREEN = (207, 227, 192)

img = Image.new("RGB", (W, H), PAPER)
d = ImageDraw.Draw(img)

def text_w(s, font):
    return d.textlength(s, font=font)

def wrap(s, font, max_w):
    words = s.split()
    lines, cur = [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if text_w(t, font) <= max_w:
            cur = t
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines

def trunc(s, font, max_w, ell="..."):
    if text_w(s, font) <= max_w:
        return s
    while s and text_w(s + ell, font) > max_w:
        s = s[:-1]
    return s + ell

def chip(x, y, label, color):
    f = F(SANS_B, 9)
    w = int(text_w(label, f)) + 10
    d.rounded_rectangle([x, y, x + w, y + 14], radius=3, fill=color)
    d.text((x + 5, y + 2), label, font=f, fill=WHITE)
    return w

# ---------------- masthead ----------------
d.rectangle([0, 0, W, 58], fill=BLACK)
d.text((14, 6), "THE WORLD TODAY", font=F(SERIF, 44), fill=WHITE)
dt = "MONDAY 23 NOVEMBER 2026"
d.text((W - 14 - text_w(dt, F(SANS_B, 16)), 20), dt, font=F(SANS_B, 16), fill=GOLD_L)

# ---------------- kicker ----------------
d.rectangle([0, 58, W, 84], fill=RED)
kick = "AI rout hits Asia  \u00b7  UN chief urges AI rules  \u00b7  US lead over China at record low  \u00b7  Anthropic IPO $107.3B"
d.text(((W - text_w(kick, F(SANS_B, 14))) / 2, 64), kick, font=F(SANS_B, 14), fill=WHITE)

# ---------------- number strip (2 rows x 5) ----------------
strip = [
    ("-3.3%", "KOSPI", RED), ("5.3", "US-CHINA POWER GAP", NAVY),
    ("11,762", "EBOLA CASES, DRC", (0, 110, 60)), ("10T won", "SEOUL STABILISATION FUND", (150, 100, 0)),
    ("2%", "BILLIONAIRE TAX IN PARIS", (110, 40, 140)),
    ("$450M", "SKUBAL DEAL", NAVY), ("165", "RUSSIAN MISSILES/WEEK", RED),
    ("12,000", "CLEARED IN MANCHESTER", (0, 110, 60)), ("264 kg", "EXPLOSIVES SEIZED", (150, 100, 0)),
    ("$107.3B", "ANTHROPIC IPO", (110, 40, 140)),
]
cw = (W - 20) / 5
for i, (val, lab, col) in enumerate(strip):
    r, c = divmod(i, 5)
    x = 10 + c * cw
    y = 84 + r * 34
    d.text((x + 4, y + 1), val, font=F(SANS_B, 19), fill=col)
    d.text((x + 4, y + 21), lab, font=F(SANS, 9), fill=GRAY)

# ---------------- region bar ----------------
regions = [("ASIA-PACIFIC 7", 7, (36, 86, 166)), ("AMERICAS 8", 8, (140, 47, 57)),
           ("MIDDLE EAST 6", 6, (183, 121, 31)), ("EUROPE 5", 5, (15, 118, 110)),
           ("AFRICA 3", 3, (109, 40, 168)), ("WORLD 2", 2, (68, 68, 68))]
x = 10
for name, n, col in regions:
    w = 1004 * n / 31
    d.rectangle([x, 154, x + w, 174], fill=col)
    d.text((x + 6, 159), name, font=F(SANS_B, 11), fill=WHITE)
    x += w

# ---------------- UTC strip ----------------
d.rectangle([0, 176, W, 192], fill=(235, 230, 218))
utc = "THE DAY IN UTC   ~00:00 Kospi dives   ~06:30 Guterres opens   ~09:00 Power Index   ~12:00 Paris 2% tax   ~15:00 Kyiv missiles"
d.text((12, 180), utc, font=F(SANS, 10), fill=BLACK)
d.text((W - 12 - text_w("~ APPROX", F(SANS, 10)), 180), "~ APPROX", font=F(SANS, 10), fill=GRAY)

# ---------------- heroes ----------------
HX, HY, HW = 10, 194, 329
GAP = 8

def hero_scene_kospi(x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(22, 35, 63))
    # buildings with lit windows
    import random
    rnd = random.Random(7)
    bx = x + 6
    while bx < x + w - 14:
        bw = rnd.randint(18, 34)
        bh = rnd.randint(34, h - 26)
        by = y + h - bh
        d.rectangle([bx, by, bx + bw, y + h], fill=(12, 20, 40))
        for wy in range(by + 5, y + h - 4, 9):
            for wx in range(bx + 4, bx + bw - 3, 8):
                if rnd.random() < 0.55:
                    d.rectangle([wx, wy, wx + 3, wy + 4], fill=(232, 196, 90))
        bx += bw + 4
    # orange chart line, trending down — kept below the big -3.3% label
    pts = []
    n = 9
    for i in range(n):
        px = x + 14 + i * (w - 28) / (n - 1)
        py = y + 48 + i * (h - 62) / (n - 1) + rnd.uniform(-4, 4)
        pts.append((px, py))
    d.line(pts, fill=(255, 140, 40), width=3)
    for px, py in pts:
        d.ellipse([px - 3, py - 3, px + 3, py + 3], fill=WHITE, outline=(255, 140, 40))
    d.text((x + 10, y + 4), "-3.3%", font=F(SANS_B, 26), fill=(255, 90, 70))

def hero_scene_guterres(x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=TEAL)
    d.text((x + 12, y + 8), "150 DELEGATES", font=F(SANS_B, 24), fill=GOLD_L)
    d.text((x + 12, y + 36), "BACK A RISK", font=F(SANS_B, 24), fill=GOLD_L)
    d.text((x + 12, y + 64), "FRAMEWORK", font=F(SANS_B, 24), fill=GOLD_L)
    # globe
    cx, cy, r = x + w - 62, y + h // 2, 44
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(200, 230, 225), outline=(255, 255, 255), width=2)
    d.ellipse([cx - r // 2, cy - r, cx + r // 2, cy + r], outline=(90, 140, 135), width=1)
    d.line([cx - r, cy, cx + r, cy], fill=(90, 140, 135), width=1)
    d.arc([cx - r, cy - r // 2, cx + r, cy + r // 2], 0, 360, fill=(90, 140, 135), width=1)

def hero_scene_power(x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=CREAM)
    d.text((x + 10, y + 4), "NARROWEST SINCE 2018", font=F(SANS, 10), fill=BLACK)
    d.text((x + w - 10 - text_w("GAP 5.3", F(SANS_B, 11)), y + 3), "GAP 5.3", font=F(SANS_B, 11), fill=RED)
    bars = [("US", 78.9, NAVY), ("CHINA", 73.6, RED), ("INDIA", 40.5, (183, 140, 20))]
    bw = 62
    base = y + h - 8
    total_gap = w - 3 * bw
    for i, (lab, val, col) in enumerate(bars):
        bx = x + total_gap / 2 + i * (bw + total_gap / 4) + i * 0
        bx = x + 18 + i * (bw + 28)
        bh = (h - 52) * val / 78.9
        d.text((bx + bw / 2 - text_w(f"{val}", F(SANS_B, 15)) / 2, base - bh - 20), f"{val}", font=F(SANS_B, 15), fill=BLACK)
        d.rectangle([bx, base - bh, bx + bw, base], fill=col)
        d.text((bx + bw / 2 - text_w(lab, F(SANS_B, 10)) / 2, base - 16), lab, font=F(SANS_B, 10), fill=WHITE)

heroes = [
    (hero_scene_kospi, "KOREA EXCHANGE", "AI ROUT HITS ASIA",
     "Kospi closes -3.3% to 4,708.54, sheds 161 pts; intraday -5.8%. Samsung -3.1%, SK Hynix -2.5%."),
    (hero_scene_guterres, "UNITED NATIONS", "GUTERRES: REGULATE AI BEFORE IT'S TOO LATE",
     "UN chief urges global AI safety rules at the Bridgetown summit; 150 back a risk framework."),
    (hero_scene_power, "LOWY INSTITUTE", "US LEAD OVER CHINA AT RECORD LOW",
     "Asia Power Index 2026: US 78.9, China 73.6 \u2014 gap 5.3, narrowest since 2018. India third at 40.5."),
]
for i, (scene, src, head, body) in enumerate(heroes):
    x = HX + i * (HW + GAP)
    scene(x, HY, HW, 96)
    d.rectangle([x, HY + 96, x + HW, HY + 112], fill=BLACK)
    d.text((x + 8, HY + 100), src, font=F(SANS_B, 10), fill=WHITE)
    hl = wrap(head, F(SERIF, 18), HW - 8)
    yy = HY + 116
    for ln in hl[:2]:
        d.text((x + 2, yy), ln, font=F(SERIF, 18), fill=BLACK)
        yy += 21
    bl = wrap(body, F(SANS, 11), HW - 6)
    yy = HY + 158
    for ln in bl[:2]:
        d.text((x + 2, yy), ln, font=F(SANS, 11), fill=(40, 40, 40))
        yy += 13
    chip(x + HW - 66, HY + 186, "REPORTED", NAVY)

# ---------------- cards ----------------
CY = 422
d.text((10, 400), "MORE OF THE DAY  \u2014  10 STORIES", font=F(SANS_B, 13), fill=BLACK)
d.line([10, 418, W - 10, 418], fill=BLACK, width=2)
cards = [
    ("AMERICAS", 1, (36, 86, 166), "BESSENT: NVIDIA ANSWERS", "Treasury wants answers.", "Reuters", "REPORTED"),
    ("FBI", 2, (36, 86, 166), "FBI PROBES NCIC HACK", "NCIC database hacked.", "AP", "REPORTED"),
    ("WHITE HOUSE", 3, (150, 100, 0), "TRUMP: IRAN STRIKES MAY RESUME", "May resume in New Year.", "Reuters", "REPORTED"),
    ("MARKETS", 4, (15, 118, 110), "US FUTURES JUMP 3%", "Holiday rally lifts futures 3%.", "Bloomberg", "REPORTED"),
    ("SPORT", 5, (140, 47, 57), "SKUBAL'S $450M METS DEAL", "Nine-year deal, largest ever.", "AP", "REPORTED"),
    ("SPORT", 6, (140, 47, 57), "TOM JACKSON DIES AT 75", "Broncos LB, ESPN voice, dies.", "ESPN", "REPORTED"),
    ("LEGAL", 7, (109, 40, 168), "STATES SUE SPACEX", "Ten states sue over AI.", "AP", "REPORTED"),
    ("TECH", 8, (15, 118, 110), "ANTHROPIC IPO: $107.3B", "Raised at $83; closes $97.17.", "WSJ", "REPORTED"),
    ("EUROPE", 9, (15, 118, 110), "POLAND: 3 MISSILES CROSSED AIRSPACE", "Kyiv: three Kh-101s crossed.", "AP", "CLAIM"),
    ("SPACE", 10, (109, 40, 168), "RUSSIAN NUCLEAR SATELLITE", "May carry a nuke.", "Reuters", "CLAIM"),
]
CW2 = 196
for i, (cat, num, col, head, body, src, tag) in enumerate(cards):
    r, c = divmod(i, 5)
    x = 10 + c * (CW2 + 6)
    y = CY + r * 88
    d.rectangle([x, y, x + CW2, y + 16], fill=col)
    d.text((x + 5, y + 2), cat, font=F(SANS_B, 10), fill=WHITE)
    d.text((x + CW2 - 14, y + 2), str(num), font=F(SANS_B, 10), fill=WHITE)
    hl = wrap(head, F(SANS_B, 13), CW2 - 8)
    yy = y + 20
    for ln in hl[:2]:
        d.text((x + 4, yy), ln, font=F(SANS_B, 13), fill=BLACK)
        yy += 16
    d.text((x + 4, y + 54), trunc(body, F(SANS, 11), CW2 - 8), font=F(SANS, 11), fill=(40, 40, 40))
    d.text((x + 4, y + 70), src, font=F(SANS, 9), fill=GRAY)
    chip(x + CW2 - 66, y + 68, tag, NAVY if tag == "REPORTED" else RED)

# ---------------- map + ALSO ----------------
MY = 620
d.text((10, 598), "WHERE IT HAPPENED", font=F(SANS_B, 13), fill=BLACK)
d.line([10, 616, W - 10, 616], fill=BLACK, width=2)
d.text((340, 598), "ALSO ON MONDAY", font=F(SANS_B, 13), fill=BLACK)
# map box
d.rectangle([10, MY, 330, MY + 222], outline=BLACK, width=1, fill=WHITE)
# blobs: Americas, Eurasia, Africa
d.polygon([(24, 656), (60, 644), (96, 648), (122, 668), (128, 708), (112, 748), (96, 788), (70, 808), (44, 788), (28, 738), (20, 698)], fill=MAPGREEN)
d.polygon([(150, 656), (200, 644), (260, 648), (312, 664), (318, 698), (290, 720), (240, 724), (180, 714), (152, 688)], fill=MAPGREEN)
d.polygon([(176, 736), (220, 730), (246, 750), (240, 788), (214, 814), (188, 798), (172, 764)], fill=MAPGREEN)
d.ellipse([286, 794, 318, 820], fill=MAPGREEN)
pins = [(300, 708, "1"), (88, 800, "2"), (278, 698, "3"), (105, 708, "4"),
        (120, 688, "5"), (245, 673, "6"), (90, 728, "7"), (55, 743, "8"),
        (75, 768, "9"), (98, 782, "10"), (220, 663, "11"), (195, 658, "12"),
        (265, 658, "13")]
for px, py, n in pins:
    d.ellipse([px - 9, py - 9, px + 9, py + 9], fill=RED, outline=WHITE, width=1)
    d.text((px - text_w(n, F(SANS_B, 10)) / 2, py - 7), n, font=F(SANS_B, 10), fill=WHITE)
d.text((16, MY + 200), "Pins 1\u201313: 1 Seoul \u00b7 2 Bridgetown \u00b7 3 Beijing \u00b7 4 Washington \u00b7 5 New York \u00b7 6 Kyiv", font=F(SANS, 8), fill=BLACK)
d.text((16, MY + 211), "7 Chicago \u00b7 8 SF \u00b7 9 Denver \u00b7 10 Austin \u00b7 11 Warsaw \u00b7 12 London \u00b7 13 Moscow", font=F(SANS, 8), fill=BLACK)

also = [
    ("14. Paris: 100+ back 2% billionaire tax", False),
    ("15. Manchester: 12,000 cleared", False),
    ("16. Zelenskyy: 165 missiles in a week", False),
    ("17. COP31: the day after pact rejected", False),
    ("18. Benghazi: UN demands port probe [CLAIM]", True),
    ("19. Israel unity talks resume", False),
    ("20. Gaza: two killed in Israeli strike", False),
    ("21. West Bank settler attacks", False),
    ("22. Iran war: no deal in sight", False),
    ("23. Lebanon seizes 264 kg explosives", False),
    ("24. Bahrain: strike hits plant, 2 hurt", False),
    ("25. Sudan: defences down drones [CLAIM]", True),
    ("26. DRC: fighting traps Ebola teams", False),
    ("27. Bangladesh: Hasina jailed if she returns", False),
    ("28. Seoul minister quits in exam row", False),
    ("29. SK Telecom -7.3% as hype cools", False),
    ("30. China eases margin rules", False),
    ("31. Seoul readies 10T-won fund", False),
]
yy = MY + 1
for txt, claim in also:
    d.text((340, yy), txt, font=F(SANS, 12), fill=RED if claim else BLACK)
    yy += 12

# ---------------- DATE CHECK ----------------
DY = 848
d.rectangle([10, DY, W - 10, DY + 62], outline=RED, width=2, fill=WHITE)
d.text((16, DY + 4), "DATE CHECK", font=F(SANS_B, 13), fill=RED)
d.text((W - 16 - text_w("READ 23 NOV 2026, 23:59 UTC \u2014 STORIES DATED 23 NOV ONLY", F(SANS_B, 9)), DY + 6),
       "READ 23 NOV 2026, 23:59 UTC \u2014 STORIES DATED 23 NOV ONLY", font=F(SANS_B, 9), fill=RED)
d.text((16, DY + 24), "LEFT OUT \u2014 NOT 23 NOV: Dems 258 seats (22 Nov) \u00b7 Sparta II fire (22 Nov) \u00b7 El Chapo (22 Nov) \u00b7 EU\u2013Indonesia (21 Nov) \u00b7 Nigeria boat (21 Nov) \u00b7 ICJ Myanmar (19 Nov)", font=F(SANS, 11), fill=BLACK)
d.text((16, DY + 42), "NOT YET \u2014 Dymer search continues (14 missing) \u00b7 4 House races uncalled \u00b7 COP32 venue not set \u00b7 WHO evacuating trapped Ebola staff", font=F(SANS, 11), fill=BLACK)

# ---------------- footer ----------------
d.rectangle([0, 916, W, H], fill=BLACK)
d.text((14, 922), "Sources: Reuters \u00b7 AP \u00b7 Bloomberg \u00b7 AFP \u00b7 Yonhap \u00b7 BBC \u00b7 WSJ \u00b7 NYT \u00b7 ESPN \u00b7 Lowy Institute (Asia Power Index 2026).", font=F(SANS, 10), fill=(200, 200, 200))
d.text((14, 938), "CHIPS: REPORTED = confirmed by wires. CLAIM = one side's claim, not independently confirmed. ONGOING = still developing.", font=F(SANS, 10), fill=(200, 200, 200))
d.text((14, 954), "All times UTC. Figures as reported 23 Nov 2026. Scenes are drawn illustrations, not photographs.", font=F(SANS, 10), fill=(200, 200, 200))
gold = "THE WORLD TODAY  \u2014  Monday 23 November 2026  \u00b7  31 stories  \u00b7  6 regions"
d.text(((W - text_w(gold, F(SANS_B, 12))) / 2, 986), gold, font=F(SANS_B, 12), fill=GOLD_L)

img.save(OUT)
print("saved", OUT, os.path.getsize(OUT), "bytes")
