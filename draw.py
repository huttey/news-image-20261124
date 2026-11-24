#!/usr/bin/env python3
"""Draw the news-image-20261124 front page (1024x1024) with PIL.

Build tooling only -- this file lives OUTSIDE the entry repository.
The repository holds the rendered entry.png plus a one-line program
that copies it to /output/entry.png.
"""
import os
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
OUT = os.path.expanduser(
    "~/workspace/makefun-setup/entries/news-image-20261124/entry.png")

SERIF_B = "/usr/share/fonts/truetype/liberation/LiberationSerif-Bold.ttf"
SANS_B = "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf"
SANS = "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf"

PAPER = (248, 245, 238)
INK = (17, 17, 17)
RED = (179, 32, 44)
BLUE = (26, 77, 143)
GREY = (90, 86, 78)
RULE = (180, 172, 156)
CARD_BG = (255, 255, 255)
CARD_LINE = (210, 203, 188)


def font(path, size):
    return ImageFont.truetype(path, size)


def fit(draw, text, f, max_w):
    """Truncate text with an ellipsis so it fits max_w pixels."""
    if draw.textlength(text, font=f) <= max_w:
        return text
    ell = "..."
    lo, hi = 0, len(text)
    while lo < hi:
        mid = (lo + hi + 1) // 2
        if draw.textlength(text[:mid] + ell, font=f) <= max_w:
            lo = mid
        else:
            hi = mid - 1
    return text[:lo] + ell


def wrap(draw, text, f, max_w, max_lines):
    """Greedy word wrap, at most max_lines lines; last line gets an ellipsis."""
    words = text.split()
    lines, cur = [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if draw.textlength(trial, font=f) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
            if len(lines) == max_lines:
                break
    if len(lines) < max_lines and cur:
        lines.append(cur)
    lines = lines[:max_lines]
    if lines and draw.textlength(lines[-1], font=f) > max_w:
        lines[-1] = fit(draw, lines[-1], f, max_w)
    return lines


img = Image.new("RGB", (W, H), PAPER)
d = ImageDraw.Draw(img)

# ---------- Header ----------
d.text((24, 8), "THE WORLD", font=font(SERIF_B, 56), fill=INK)
d.text((24, 66), "One day's news — in one picture",
       font=font(SANS, 15), fill=GREY)
d.text((W - 24, 14), "TUESDAY", font=font(SANS_B, 22), fill=RED,
       anchor="ra")
d.text((W - 24, 42), "24 NOVEMBER 2026", font=font(SANS_B, 22),
       fill=RED, anchor="ra")
d.text((W - 24, 70), "41 stories, all reported today",
       font=font(SANS, 13), fill=GREY, anchor="ra")
d.line([(24, 92), (W - 24, 92)], fill=INK, width=3)
d.line([(24, 96), (W - 24, 96)], fill=RULE, width=1)

# ---------- Lead story ----------
y = 104
d.text((24, y), "MARKETS  ·  THE COMEBACK", font=font(SANS_B, 13),
       fill=RED)
lead_head = ["Huang is back — Nvidia adds", "$952bn in one day"]
f_lead = font(SANS_B, 32)
for i, line in enumerate(lead_head):
    d.text((24, y + 20 + i * 36), line, font=f_lead, fill=INK)
lead_sum = ("Board reinstates Jensen Huang as chief executive 11 days "
            "after his resignation; shares jump 31.5%, their best day "
            "since 2003, and the Nasdaq surges 6.5%.")
for i, line in enumerate(wrap(d, lead_sum, font(SANS, 14), 700, 2)):
    d.text((24, y + 96 + i * 18), line, font=font(SANS, 14), fill=INK)
# lead stat box, right side
d.rectangle([760, y + 16, 1000, y + 142], outline=CARD_LINE, width=1,
            fill=CARD_BG)
d.text((880, y + 26), "+31.5%", font=font(SANS_B, 34), fill=RED,
       anchor="ma")
d.text((880, y + 68), "Nvidia shares", font=font(SANS_B, 14), fill=INK,
       anchor="ma")
d.text((880, y + 90), "best day since May 2003", font=font(SANS, 12),
       fill=GREY, anchor="ma")
d.text((880, y + 110), "Nasdaq +6.5%  ·  S&P +4.7%",
       font=font(SANS, 12), fill=GREY, anchor="ma")
d.line([(24, 242), (W - 24, 242)], fill=RULE, width=1)

# ---------- Cards: 2 cols x 5 rows ----------
CARDS = [
    ("UKRAINE", "Kyiv strikes kill at least 14",
     "Russian drones and missiles hit the Kyiv region; a home in Dymer was damaged.", "AP"),
    ("AI", "States sue Musk firms over Grok images",
     "US states say the chatbot made sexualised images of real people.", "AP"),
    ("USA", "Congressman Gomez resigns",
     "Ethics panel found evidence of sexual misconduct; the Democrat quits.", "AP"),
    ("TRAVEL", "Storms threaten Thanksgiving travel",
     "Storms and airline glitches set up a messy holiday getaway.", "AP"),
    ("INDONESIA", "Factory fire kills 24",
     "More bodies are pulled from a burned candy factory in Banten.", "AP"),
    ("BALTIC", "Russian ship burns after drone hit",
     "Cargo ship Sparta II catches fire in the Gulf of Finland.", "TOI"),
    ("SUDAN", "Drones hit homes and UN building",
     "Strikes hit houses and a UN building in the capital, Khartoum.", "AP"),
    ("INDIA–NEPAL", "New train links Ayodhya and Janakpur",
     "Modi and Nepal's PM flag off the Saryu-Kamala Express.", "Jagran Josh"),
    ("CLIMATE", "COP31 split over fossil fuels",
     "Talks in Antalya, Türkiye, stall on curbing oil and gas.", "Jagran Josh"),
    ("TENNIS", "Alcaraz wins first ATP Finals title",
     "The Spaniard beats Zverev in the final in Turin, Italy.", "TOI"),
]
cx0, cy0 = 24, 252
cw, ch, cg = 488, 60, 8
for i, (tag, head, summ, src) in enumerate(CARDS):
    col, row = i % 2, i // 2
    x = cx0 + col * (cw + cg)
    yy = cy0 + row * (ch + 5)
    d.rectangle([x, yy, x + cw, yy + ch], outline=CARD_LINE, width=1,
                fill=CARD_BG)
    d.text((x + 10, yy + 5), tag, font=font(SANS_B, 11), fill=RED)
    d.text((x + 10, yy + 19), fit(d, head, font(SANS_B, 15), cw - 20),
           font=font(SANS_B, 15), fill=INK)
    d.text((x + 10, yy + 39),
           fit(d, summ, font(SANS, 12), cw - 20),
           font=font(SANS, 12), fill=GREY)
d.line([(24, 580), (W - 24, 580)], fill=RULE, width=1)

# ---------- Ticker: the day in brief, 2 cols x 15 rows ----------
TICKER = [
    "Lisbon: thousands march over living costs",
    "Turkey: thousands protest media closures",
    "Macron eyes constitution change to curb spending",
    "UN chief: AI risk rules needed within a year",
    "Nepal PM in India for economy and energy talks",
    "Thai court upholds verdict on opposition MP",
    "Myanmar junta faults ASEAN decision",
    "North Korea 'ready to expand ties'",
    "Denmark court backs hardline 'ghetto law'",
    "US court gives Trump path to erase hush-money case",
    "Allies: Russia may launch nuclear space weapon",
    "Oxfam: Gaza left toxic by explosives",
    "Taliban erase women's names in Balkh papers",
    "Lego picks Portugal for its 8th factory",
    "England trials AI breast-cancer screening",
    "WHO chief pleads for peace in Ebola-hit Congo",
    "Verstappen wins the Las Vegas Grand Prix",
    "Pant hits 128 as India–NZ Test is drawn",
    "Gukesh begins chess title defence in Geneva",
    "Ferrari unveils two new 296 Challenge cars",
    "India oil import bill up 60% to $16bn",
    "SpiceJet crisis: pilots seek state help",
    "India–China army talks in Arunachal",
    "Modi opens AI centre at IIT Patna",
    "FIFA picks 2031, 2035 Women's World Cup hosts",
    "Supermoon meets the Seven Sisters tonight",
    "Japan GDP slump 'more than a blip'",
    "Warming pushes Nagano celery uphill",
    "India court frees Godhra convict on bail",
    "Allegheny County certifies midterm results",
]
d.text((24, 590), "THE DAY IN BRIEF", font=font(SANS_B, 14), fill=INK)
d.line([(24, 612), (W - 24, 612)], fill=INK, width=2)
tx0, ty0 = 24, 622
tw, th = 488, 22
for i, item in enumerate(TICKER):
    col, row = i % 2, i // 2
    x = tx0 + col * (tw + 8)
    yy = ty0 + row * th
    d.text((x, yy), "•", font=font(SANS_B, 13), fill=RED)
    d.text((x + 14, yy),
           fit(d, item, font(SANS, 13), tw - 16),
           font=font(SANS, 13), fill=INK)
d.line([(24, 960), (W - 24, 960)], fill=RULE, width=1)

# ---------- Numbers strip ----------
NUMBERS = [
    ("$952bn", "Nvidia's one-day gain"),
    ("+31.5%", "Nvidia shares"),
    ("+6.5%", "Nasdaq"),
    ("+1,448", "Dow points"),
    ("14", "killed in Kyiv strikes"),
    ("24", "killed in Indonesia fire"),
]
nx = 24
for num, lab in NUMBERS:
    d.text((nx, 970), num, font=font(SANS_B, 15), fill=INK)
    nw = d.textlength(num, font=font(SANS_B, 15))
    d.text((nx + nw + 5, 972), lab, font=font(SANS, 12), fill=GREY)
    nx += nw + 5 + d.textlength(lab, font=font(SANS, 12)) + 22

# ---------- Footer ----------
d.text((24, 994),
       "Sources: AP, CNN, Reuters, WSJ, Japan Times, The Manila Times, "
       "Times of India, Jagran Josh",
       font=font(SANS, 10), fill=GREY)

img.save(OUT, format="PNG", optimize=True)
size = os.path.getsize(OUT)
print("saved", OUT, size, "bytes")
if size > 1048576:
    img.save(OUT, format="JPEG", quality=88)
    print("PNG over gate; saved JPEG", os.path.getsize(OUT), "bytes")
