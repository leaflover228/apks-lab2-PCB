"""Regenerate lab2.kicad_sch with clean layout: fields inside bodies,
net labels oriented away from the pins, no duplicate items."""
import os
import re
import uuid

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SCH = os.path.join(ROOT, "lab2.kicad_sch")
LIB = os.path.join(ROOT, "lib", "lab2.kicad_sym")

ROOT_UUID = "8dddbafb-b77a-4b3f-b5fc-801d2aad0242"
PROJECT = "lab2"
TITLE = "\u041b\u0420 II \u2014 \u0434\u0440\u0443\u043a\u043e\u0432\u0430\u043d\u0430 \u043f\u043b\u0430\u0442\u0430 (\u0432\u0430\u0440\u0456\u0430\u043d\u0442 30)"
COMPANY = "\u042f\u0449\u0443\u043a \u0413\u0435\u043e\u0440\u0433\u0456\u0439 \u041e\u043b\u0435\u0433\u043e\u0432\u0438\u0447"
GUID = "GUID (md5): 7cc66fd9-e47b-cdd7-b82c-09c580a12247"

STUB = 2.54

# ref, symbol, footprint, value, x, y, ref_dx, ref_dy, val_dx, val_dy, description
COMPONENTS = [
    ("J1", "J1_lab2", "lab2:J1_1x5_P2.54", "1x05", 34.29, 105.41, 0, -4.6, 0, 4.6,
     "Lab2 1x5 pin header, 2.54 mm"),
    ("U1", "U1_lab2", "lab2:U1_SOIC-8_P1.27", "SOIC-8", 85.09, 64.77, 0, -6.6, 0, 6.6,
     "Lab2 SOIC-8 IC, 1.27 mm pitch"),
    ("U2", "U2_lab2", "lab2:SW_PUSH_6mm", "SW_PUSH_6mm", 85.09, 149.86, 0, -5.3, 0, 5.3,
     "Lab2 6 mm push button"),
    ("U3", "U3_lab2", "lab2:SW_PUSH_6mm", "SW_PUSH_6mm", 175.26, 64.77, 0, -5.3, 0, 5.3,
     "Lab2 6 mm push button"),
    ("U4", "U4_lab2", "lab2:SW_PUSH_6mm", "SW_PUSH_6mm", 175.26, 149.86, 0, -5.3, 0, 5.3,
     "Lab2 6 mm push button"),
    ("U5", "U5_lab2", "lab2:U5_2x06_P2.54", "2x06", 245.11, 105.41, 0, -10.4, 0, 10.4,
     "Lab2 2x6 test header, 2.54 mm"),
]

NETS = {
    "N_7": [("U1", "1"), ("U2", "3"), ("U3", "4"), ("U5", "12")],
    "N_C": [("U1", "2"), ("U1", "3"), ("U3", "1"), ("U4", "4"), ("U5", "3")],
    "N_D": [("U1", "7"), ("U3", "2"), ("U3", "3")],
    "N_2": [("U4", "3"), ("U5", "9"), ("U5", "10")],
    "N_9": [("U1", "8"), ("U5", "2")],
    "N_4": [("U2", "2"), ("U5", "11")],
    "N_B": [("U2", "4"), ("U4", "1")],
    "N_8": [("U4", "2"), ("U5", "5")],
    "N_6": [("U1", "4"), ("U1", "5")],
    "N_0": [("U5", "1"), ("U5", "6")],
    "N_F": [("J1", "1"), ("U1", "6")],
    "N_E": [("J1", "2"), ("U2", "1")],
    "N_5": [("J1", "3"), ("U5", "4")],
    "N_A": [("J1", "4"), ("U5", "7")],
    "N_1": [("J1", "5"), ("U5", "8")],
}


def block(txt, start):
    d = 0
    for j in range(start, len(txt)):
        if txt[j] == "(":
            d += 1
        elif txt[j] == ")":
            d -= 1
            if d == 0:
                return txt[start:j + 1]
    raise ValueError("unbalanced")


def top_symbols(path):
    txt = open(path, encoding="utf-8-sig").read()
    out = {}
    k = 0
    while True:
        m = re.search(r"\(symbol \"([^\"]+)\"", txt[k:])
        if not m:
            break
        st = k + m.start()
        blk = block(txt, st)
        out[m.group(1)] = blk
        k = st + len(blk)
    return out


def pins_of(sym_block):
    """-> {number: (x, y, angle)} in symbol coordinates"""
    pins = {}
    parts = sym_block.split("(pin ")[1:]
    for p in parts:
        m_at = re.search(r"\(at ([-\d.]+) ([-\d.]+) ([-\d.]+)\)", p)
        m_num = re.search(r"\(number \"([^\"]+)\"", p)
        if m_at and m_num:
            pins[m_num.group(1)] = (float(m_at.group(1)), float(m_at.group(2)),
                                    float(m_at.group(3)))
    return pins


def prefixed(blk, name):
    return blk.replace('(symbol "%s"' % name, '(symbol "lab2:%s"' % name, 1)


SYMBOLS = top_symbols(LIB)
PINS = {name: pins_of(blk) for name, blk in SYMBOLS.items()}

OUTWARD = {0: (-1, 0), 180: (1, 0), 90: (0, 1), 270: (0, -1)}
LABEL_ANGLE = {0: 0, 180: 0, 90: 90, 270: 90}
LABEL_JUST = {0: "right", 180: "left", 90: "left", 270: "right"}


def esc(s):
    return s.replace('"', '\\"')


def main():
    libs = "\n".join("\t\t" + prefixed(SYMBOLS[n], n) for n in
                     ["J1_lab2", "U1_lab2", "U2_lab2", "U3_lab2", "U4_lab2", "U5_lab2"])

    head = """(kicad_sch
\t(version 20260101)
\t(generator "eeschema")
\t(generator_version "10.0")
\t(uuid "%s")
\t(paper "A4")
\t(title_block
\t\t(title "%s")
\t\t(date "2026-11-08")
\t\t(rev "1.0")
\t\t(company "%s")
\t\t(comment 1 "%s")
\t)
\t(lib_symbols
%s
\t)
""" % (ROOT_UUID, TITLE, COMPANY, GUID, libs)

    body = []
    field_xy = {}

    for ref, sym, fp, value, cx, cy, ref_dx, ref_dy, val_dx, val_dy, desc in COMPONENTS:
        pins = PINS[sym]
        pid = []
        for num in pins:
            pid.append('\t\t(pin "%s"\n\t\t\t(uuid "%s")\n\t\t)' % (num, uuid.uuid4()))
        field_xy[ref] = {}
        props = []
        for name, text, dx, dy, hide in (
                ("Reference", ref, ref_dx, ref_dy, False),
                ("Value", value, val_dx, val_dy, False),
                ("Footprint", fp, None, None, True),
                ("Datasheet", "~", None, None, True),
                ("Description", desc, None, None, True)):
            if dx is None:
                px, py = cx, cy + 25.4  # hidden fields parked far below
            else:
                px, py = cx + dx, cy + dy
                field_xy[ref][name] = (px, py)
            hide_txt = "\n\t\t\t(hide yes)" if hide else ""
            props.append(
                '\t\t(property "%s" "%s"\n\t\t\t(at %.2f %.2f 0)%s\n'
                '\t\t\t(show_name no)\n\t\t\t(do_not_autoplace no)\n'
                '\t\t\t(effects\n\t\t\t\t(font\n\t\t\t\t\t(size 1.27 1.27)\n\t\t\t\t)\n\t\t\t)\n\t\t)'
                % (name, esc(text), px, py, hide_txt))

        body.append(
            '\t(symbol\n\t\t(lib_id "lab2:%s")\n\t\t(at %.2f %.2f 0)\n\t\t(unit 1)\n'
            '\t\t(body_style 1)\n\t\t(exclude_from_sim no)\n\t\t(in_bom yes)\n'
            '\t\t(on_board yes)\n\t\t(in_pos_files yes)\n\t\t(dnp no)\n'
            '\t\t(uuid "%s")\n%s\n%s\n'
            '\t\t(instances\n\t\t\t(project "%s"\n\t\t\t\t(path "/%s"\n'
            '\t\t\t\t\t(reference "%s")\n\t\t\t\t\t(unit 1)\n\t\t\t\t)\n\t\t\t)\n\t\t)\n\t)'
            % (sym, cx, cy, uuid.uuid4(), "\n".join(props), "\n".join(pid), PROJECT, ROOT_UUID, ref))

    # wires + labels
    for net, plist in NETS.items():
        for ref, num in plist:
            cx, cy = [(c[4], c[5]) for c in COMPONENTS if c[0] == ref][0]
            px, py, angle = PINS[[c[1] for c in COMPONENTS if c[0] == ref][0]][num]
            sx, sy = cx + px, cy - py
            ox, oy = OUTWARD[angle]
            ex, ey = sx + ox * STUB, sy + oy * STUB
            body.append(
                '\t(wire\n\t\t(pts\n\t\t\t(xy %.2f %.2f) (xy %.2f %.2f)\n\t\t)\n'
                '\t\t(stroke\n\t\t\t(width 0)\n\t\t\t(type default)\n\t\t)\n'
                '\t\t(uuid "%s")\n\t)' % (sx, sy, ex, ey, uuid.uuid4()))
            body.append(
                '\t(label "%s"\n\t\t(at %.2f %.2f %d)\n\t\t(effects\n'
                '\t\t\t(font\n\t\t\t\t(size 1.27 1.27)\n\t\t\t)\n\t\t\t(justify %s)\n\t\t)\n'
                '\t\t(uuid "%s")\n\t)' % (net, ex, ey, LABEL_ANGLE[angle],
                                        LABEL_JUST[angle], uuid.uuid4()))

    tail = '\t(sheet_instances\n\t\t(path "/"\n\t\t\t(page "1")\n\t\t)\n\t)\n)\n'
    open(SCH, "w", encoding="utf-8", newline="\n").write(head + "\n".join(body) + "\n" + tail)
    print("written", SCH)


if __name__ == "__main__":
    main()

