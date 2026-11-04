# Gehaeuse fuer RC-Multiswitch-ESP32-C3 (Platine v0.3 NEG/POS, ESP32-C3 SuperMini)
# Abgeleitet vom Gehaeuse RC-Multiswitch-ESP32-S3 (gleiche Breite, Treiber/J1/LEDs/CN2 an gleicher Stelle).
# Parametrisch mit CadQuery. Aufruf: python gehaeuse.py  -> STL/STEP im Ordner "export"
#
# Koordinaten: X = KiCad-x - 123.8, Y = 87.95 - KiCad-y (Platinen-Ecke links vorne = 0/0),
# Z nach oben, Z = 0 = Unterseite Gehaeuseboden.
# Waende: links = CN1/CN2/USB, hinten = J5 (KiCad-Oberkante), J1 wird von oben gesteckt.
# Variante "gewinkelt" (python gehaeuse.py --gewinkelt): J1 = gewinkelte Stiftleiste 2x8, Koerper zur
# rechten Kante, Stecker seitlich durch einen Schlitz in der rechten Wand, Deckel ueber J1 geschlossen.
import os, sys
import cadquery as cq

# ---------------- Parameter (alles in mm) ----------------
PCB_W, PCB_H, PCB_T = 66.52, 50.15, 1.6       # Platine aus Edge.Cuts
WAND      = 2.2      # Wandstaerke
BODEN     = 2.0      # Bodenstaerke
DECKEL    = 2.0      # Deckelstaerke
SPALT     = 0.5      # Luft Platine <-> Innenwand
UNTEN     = 3.0      # Platz unter der Platine (Loetstellen)
INNEN_H   = 11.0     # Platz ueber der Platine (hoechstes Teil: J1 8,5 mm / Treiber U2 im Sockel ca. 8 mm)
ESP_Z     = 2.5      # Unterkante C3 SuperMini ueber Platine (Annahme: direkt auf Stiftleiste geloetet, Kunststoff 2,5 mm)
ESP_T     = 1.0      # Dicke SuperMini-Platine
LEISTE    = 1.2      # Auflagerand unter der Platine (ringsum, keine Pads in diesem Streifen)
DECKEL_SCHR_D = 2.2  # Kernloch Deckelschrauben (2,5 x 8 selbstschneidend)
DECKEL_SCHR_K = 2.8  # Durchgangsloch im Deckel
BOSS_R    = 2.8
LIPPE     = 3.0      # Hoehe der Zentrierlippe am Deckel
TOL       = 0.25     # Spiel Lippe <-> Innenwand
NIEDER    = 0.1      # Niederhalter am Deckel enden so viel ueber der Platine (0 = liegt auf)
J1_GEWINKELT = "--gewinkelt" in sys.argv   # True = gewinkelte Stiftleiste 2x8 fuer die Ausgaenge
J1_SCHLITZ_H = 6.0   # Hoehe Wandschlitz fuer die Stecker ueber Platinen-Oberkante (Leiste 5,1 mm)

Z_PCB = BODEN + UNTEN            # Unterkante Platine
Z_TOP = Z_PCB + PCB_T            # Oberkante Platine
H_BASE = Z_TOP + INNEN_H         # Hoehe Unterteil (Deckel liegt oben drauf)

def kx(x): return x - 123.8
def ky(y): return 87.95 - y

# Innenraum
IX0, IY0 = -SPALT, -SPALT
IX1, IY1 = PCB_W + SPALT, PCB_H + SPALT
# Deckelschrauben: in der vorderen und hinteren Wand (links/rechts bleiben duenn, wegen USB-Stecker)
SY = 0.9 + DECKEL_SCHR_D / 2 + 0.7
SCHR = [(6.0, -SY), (PCB_W - 6.0, -SY), (28.0, PCB_H + SY), (PCB_W - 6.0, PCB_H + SY)]
OX0, OX1 = IX0 - WAND, IX1 + WAND
OY0, OY1 = min(IY0 - WAND, -SY - BOSS_R), max(IY1 + WAND, PCB_H + SY + BOSS_R)
ECKE_R = 3.0

def box(x0, y0, z0, x1, y1, z1):
    return cq.Workplane("XY").box(x1 - x0, y1 - y0, z1 - z0, centered=False).translate((x0, y0, z0))

def rbox(x0, y0, z0, x1, y1, z1, r):
    return (cq.Workplane("XY").workplane(offset=z0).center((x0 + x1) / 2, (y0 + y1) / 2)
            .rect(x1 - x0, y1 - y0).extrude(z1 - z0).edges("|Z").fillet(r))

def cyl(x, y, z0, z1, r):
    return cq.Workplane("XY").workplane(offset=z0).center(x, y).circle(r).extrude(z1 - z0)

# ---------------- Bauteile (aus KiCad) ----------------
# C3 SuperMini (U1, um 90 Grad gedreht): Fab-Rahmen x 127.34-149.86, y 60.07-78.07, USB-C am linken Ende (x 127.34)
ESP = (127.34, 60.07, 149.86, 78.07)
USB_Y = 69.07                       # Mitte USB-C (KiCad-y)
USB_Z = ESP_Z + ESP_T + 1.6         # Mitte USB-C ueber Platinen-Oberkante
LED_KICAD = [(148.66, 42.7), (153.86, 42.7), (159.06, 42.7), (164.23, 42.7),
             (169.36, 42.7), (174.46, 42.7), (179.5, 42.7), (184.5, 42.7)]
LED_OFF = 1.27   # LED_D3.0mm: Mitte liegt 1,27 mm rechts von Pad 1
J1 = (182.05, 60.42, 188.14, 81.74)  # Courtyard Stiftleiste 2x8
J1_PIN = (183.82, 62.19)             # Pad 1; 2. Reihe bei x + 2,54, Pins bis y + 17,78
# Gewinkelte Leiste (KiCad PinHeader_2x08_P2.54mm_Horizontal): Kunststoff 4,04-6,58 mm ab Pad-1-Reihe,
# Pins enden 12,58 mm ab Pad-1-Reihe, Koerper 0-5,08 mm ueber der Platine.

# ---------------- Oeffnungen in den Waenden ----------------
# (Name, Wand, von, bis (entlang der Wand), z_unten, z_oben ueber Platinen-Oberkante)
def kicad_span_y(a, b): return (ky(b), ky(a))
OEFFNUNGEN = [
    ("CN1 UART A",  "L", *kicad_span_y(47.85 - 0.8, 57.75 + 0.8), -0.2, 6.8),
    ("CN2 Last",    "L", *kicad_span_y(81.23 - 0.8, 87.13 + 0.8), -0.2, 6.8),
    ("USB-C ESP",   "L", *kicad_span_y(USB_Y - 6.0, USB_Y + 6.0), USB_Z - 3.8, USB_Z + 3.8),
    ("J5 UART B",   "O", kx(136.15 - 0.8), kx(146.05 + 0.8), -0.2, 6.8),
]
if J1_GEWINKELT:   # 8 Stecker 2-polig nebeneinander (je 2,54 mm), 0,6 mm Luft je Seite
    OEFFNUNGEN.append(("J1 Ausgaenge", "R", *kicad_span_y(J1_PIN[1] - 1.27 - 0.6, J1_PIN[1] + 17.78 + 1.27 + 0.6),
                       -0.2, J1_SCHLITZ_H))

def wand_schnitt(w, a, b, z0, z1, tiefe=1.0):
    za, zb = Z_TOP + z0, Z_TOP + z1
    if w == "L": return box(OX0 - 1, a, za, IX0 + tiefe, b, zb)
    if w == "R": return box(IX1 - tiefe, a, za, OX1 + 1, b, zb)
    if w == "U": return box(a, OY0 - 1, za, b, IY0 + tiefe, zb)
    if w == "O": return box(a, IY1 - tiefe, za, b, OY1 + 1, zb)

# Niederhalter am Deckel: Rippen, die die Platine am Rand (1 mm breit) auf die Auflage druecken.
# Nur an Stellen, wo am Rand kein Bauteil steht.
NIEDERHALTER = [("O", kx(152.0)), ("O", kx(168.0)), ("O", kx(186.0)),
                ("U", kx(140.0)), ("U", kx(165.0)), ("U", kx(185.0)),
                ("R", ky(50.0)), ("R", ky(75.0)),
                ("L", ky(60.5)), ("L", ky(78.3))]
if J1_GEWINKELT:   # Rippe rechts bei y 75 saesse auf dem Leistenkoerper
    NIEDERHALTER.remove(("R", ky(75.0)))

def unterteil():
    b = rbox(OX0, OY0, 0, OX1, OY1, H_BASE, ECKE_R)
    b = b.cut(box(IX0, IY0, BODEN, IX1, IY1, H_BASE + 1))
    # Schraubendome fuer den Deckel (an der Platine freigeschnitten)
    for x, y in SCHR:
        d = cyl(x, y, BODEN, H_BASE, BOSS_R).cut(box(-0.4, -0.4, 0, PCB_W + 0.4, PCB_H + 0.4, H_BASE + 1))
        b = b.union(d).cut(cyl(x, y, BODEN + 2, H_BASE + 1, DECKEL_SCHR_D / 2))
    # Auflage ringsum unter dem Platinenrand
    ring = box(IX0, IY0, BODEN - 0.1, IX1, IY1, Z_PCB).cut(
        box(LEISTE, LEISTE, 0, PCB_W - LEISTE, PCB_H - LEISTE, Z_PCB + 1))
    b = b.union(ring)
    # Mittelstuetze unter der Platine (Stelle ohne Pads, zwischen Treiber U2 und Widerstaenden)
    for x, y in [(167.2, 71.5), (142.0, 52.0)]:
        b = b.union(box(kx(x) - 1.2, ky(y) - 1.2, BODEN - 0.1, kx(x) + 1.2, ky(y) + 1.2, Z_PCB))
    for name, w, a, c, z0, z1 in OEFFNUNGEN:
        b = b.cut(wand_schnitt(w, a, c, z0, z1))
    # USB: aussen eine Tasche, damit auch dicke Stecker weit genug hineinkommen (Restwand 1,2 mm)
    b = b.cut(box(OX0 - 1, ky(USB_Y + 7.0), Z_TOP + USB_Z - 5.0, IX0 - 1.2, ky(USB_Y - 7.0), Z_TOP + USB_Z + 5.0))
    # Befestigungslaschen unten (4x, fuer Schraube oder Kabelbinder ins Modell)
    for x in (OX0 + 11, OX1 - 11):
        for y, s in ((OY0, -1), (OY1, 1)):
            t = rbox(x - 6, y - 7 if s < 0 else y - 1, 0, x + 6, y + 1 if s < 0 else y + 7, 3.0, 2.0)
            b = b.union(t).cut(cyl(x, y + s * 3.8, -1, 5, 1.7))
    return b

# ---------------- Deckel ----------------
def deckel():
    d = rbox(OX0, OY0, 0, OX1, OY1, DECKEL, ECKE_R)
    # Zentrierlippe innen, an den Domen und an hohen Wandoeffnungen ausgespart
    lip = box(IX0 + TOL, IY0 + TOL, -LIPPE, IX1 - TOL, IY1 - TOL, 0.01)
    lip = lip.cut(box(IX0 + TOL + 1.2, IY0 + TOL + 1.2, -LIPPE - 1, IX1 - TOL - 1.2, IY1 - TOL - 1.2, 1))
    for x, y in SCHR:
        lip = lip.cut(cyl(x, y, -LIPPE - 1, 1, BOSS_R + 0.4))
    for name, w, a, c, z0, z1 in OEFFNUNGEN:
        if z1 > INNEN_H - LIPPE:
            lip = lip.cut(wand_schnitt(w, a - 0.3, c + 0.3, z0, INNEN_H + 1, tiefe=3).translate((0, 0, -H_BASE)))
    d = d.union(lip)
    # Niederhalter (Rippen 3 mm breit, 1 mm ueber den Platinenrand)
    zu = -INNEN_H + NIEDER
    for w, p in NIEDERHALTER:
        if w == "O": r = box(p - 1.5, PCB_H - 1.0, zu, p + 1.5, IY1 - TOL, 0.01)
        if w == "U": r = box(p - 1.5, IY0 + TOL, zu, p + 1.5, 1.0, 0.01)
        if w == "R": r = box(PCB_W - 1.0, p - 1.5, zu, IX1 - TOL, p + 1.5, 0.01)
        if w == "L": r = box(IX0 + TOL, p - 1.5, zu, 1.0, p + 1.5, 0.01)
        d = d.union(r)
    # Schraubenloecher mit Senkung
    for x, y in SCHR:
        d = d.cut(cyl(x, y, -LIPPE - 1, DECKEL + 1, DECKEL_SCHR_K / 2))
        d = d.cut(cq.Workplane("XY").workplane(offset=DECKEL - 1.4).center(x, y)
                  .circle(DECKEL_SCHR_K / 2).workplane(offset=1.41).circle(2.6).loft())
    # LED-Fenster (Kontroll-LEDs 1-8)
    for x, y in LED_KICAD:
        d = d.cut(cyl(kx(x + LED_OFF), ky(y), -1, DECKEL + 1, 1.7))
    # Fenster ueber dem SuperMini: BOOT/RESET mit Stift druecken, LED sichtbar
    d = d.cut(rbox(kx(ESP[0] - 0.5), ky(ESP[3] + 0.5), -1, kx(ESP[2] + 0.5), ky(ESP[1] - 0.5), DECKEL + 1, 1.5))
    # Ausschnitt ueber J1 (Ausgaenge, Stiftleiste 2x8, Stecker von oben); gewinkelt: Deckel bleibt zu
    if not J1_GEWINKELT:
        d = d.cut(rbox(kx(J1[0] - 0.4), ky(J1[3] + 0.4), -1, kx(J1[2] + 0.4), ky(J1[1] - 0.4), DECKEL + 1, 1.0))
    # Lueftungsschlitze ueber dem Treiber U2
    for i in range(4):
        x = kx(156.3) + i * 2.6
        d = d.cut(rbox(x, ky(81.0), -1, x + 1.4, ky(62.0), DECKEL + 1, 0.6))
    # Beschriftung (0,6 mm vertieft)
    def txt(s, x, y, size=3.2, rot=0):
        return (cq.Workplane("XY").workplane(offset=DECKEL - 0.6).center(x, y)
                .transformed(rotate=(0, 0, rot)).text(s, size, 1.0, halign="center", valign="center"))
    for s, x, y, sz, r in [("RC Multiswitch C3", kx(161.0), 2.6, 3.4, 0),
                           ("A", 2.2, ky(52.8), 3.2, 0), ("5-12V", 12.5, ky(84.2), 2.6, 0),
                           ("B", kx(131.6), ky(43.5), 3.2, 0),
                           ("ESP", kx(152.6), ky(69.07), 2.6, 90),
                           ("AUSGAENGE", kx(180.3), ky(71.1), 2.6, 90)]:
        d = d.cut(txt(s, x, y, sz, r))
    for i, (x, y) in enumerate(LED_KICAD):
        d = d.cut(txt(str(i + 1), kx(x + LED_OFF), ky(y + 3.6), 2.4))
    return d

def platine_dummy():
    """Platine mit vereinfachten Bauteilen (nur fuer Vorschau / Kollisionskontrolle)."""
    p = box(0, 0, Z_PCB, PCB_W, PCB_H, Z_TOP)
    T = Z_TOP
    def fab(x0, y0, x1, y1, z0, z1):
        return box(kx(x0), ky(y1), T + z0, kx(x1), ky(y0), T + z1)
    teile = {
        "ESP": fab(*ESP, ESP_Z, ESP_Z + ESP_T),
        "USB": fab(126.6, USB_Y - 4.5, 134.0, USB_Y + 4.5, ESP_Z + ESP_T, ESP_Z + ESP_T + 3.2),
        "U2": fab(155.23, 60.0, 165.39, 82.98, 0, 8.0),
        "J1": fab(182.55, 60.92, 187.63, 81.24, 0, 8.5) if not J1_GEWINKELT else
              fab(J1_PIN[0] + 4.04, J1_PIN[1] - 1.27, J1_PIN[0] + 6.58, J1_PIN[1] + 19.05, 0, 5.08)
              .union(fab(J1_PIN[0] + 6.58, J1_PIN[1] - 0.32, J1_PIN[0] + 12.58, J1_PIN[1] + 18.1, 0.95, 4.13)),
        "D1": fab(138.0, 82.67, 147.0, 86.27, 0, 3.6),
        "CN1": fab(124.55, 47.85, 132.15, 57.75, 0, 6.0),
        "CN2": fab(124.05, 81.23, 131.65, 87.13, 0, 6.0),
        "J5": fab(136.15, 38.6, 146.05, 46.2, 0, 6.0),
    }
    for x, y in LED_KICAD:
        teile["LED%.0f" % x] = cyl(kx(x + LED_OFF), ky(y), T, T + 5.3, 1.5)
    for p_ in teile.values():
        p = p.union(p_)
    return p

if __name__ == "__main__":
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    out = args[0] if args else "export"
    os.makedirs(out, exist_ok=True)
    SUFFIX = "_gewinkelt" if J1_GEWINKELT else ""
    u, d = unterteil(), deckel()
    print("Aussenmasse: %.1f x %.1f x %.1f mm (mit Deckel)" % (OX1 - OX0, OY1 - OY0, H_BASE + DECKEL))
    cq.exporters.export(u, f"{out}/Gehaeuse_Unterteil{SUFFIX}.stl", tolerance=0.05, angularTolerance=0.1)
    cq.exporters.export(u, f"{out}/Gehaeuse_Unterteil{SUFFIX}.step")
    # Deckel fuer den Druck umdrehen (Oberseite aufs Bett)
    d_druck = d.rotate((0, 0, 0), (1, 0, 0), 180)
    cq.exporters.export(d_druck, f"{out}/Gehaeuse_Deckel{SUFFIX}.stl", tolerance=0.05, angularTolerance=0.1)
    cq.exporters.export(d, f"{out}/Gehaeuse_Deckel{SUFFIX}.step")
    if "--pruefen" in sys.argv:
        pd = platine_dummy()
        cu = pd.intersect(u).val().Volume()
        cd = pd.intersect(d.translate((0, 0, H_BASE))).val().Volume()
        print("Kollision Platine/Unterteil: %.2f mm3, Platine/Deckel: %.2f mm3" % (cu, cd))
