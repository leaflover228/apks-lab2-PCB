"""Prepare the project footprint library: renumber the 4-pad tactile switch
so every pad has its own number (1..4) and set library descriptions."""
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LIB = os.path.join(ROOT, "lib", "lab2.pretty")

DESCR = {
    "J1_1x5_P2.54.kicad_mod": "Lab2 1x5 pin header, 2.54 mm",
    "U1_SOIC-8_P1.27.kicad_mod": "Lab2 SOIC-8 IC, 1.27 mm pitch",
    "SW_PUSH_6mm.kicad_mod": "Lab2 6 mm push button",
    "U5_2x06_P2.54.kicad_mod": "Lab2 2x6 test header, 2.54 mm",
}


def set_descr(path, text):
    s = open(path, encoding="utf-8").read()
    s = re.sub(r'\(descr "[^"]*"\)', '(descr "%s")' % text, s, count=1)
    open(path, "w", encoding="utf-8", newline="\n").write(s)


def renumber_pads(path, numbers):
    s = open(path, encoding="utf-8").read()
    it = iter(numbers)

    def repl(m):
        return '(pad "%s" ' % next(it)

    s2, n = re.subn(r'\(pad "\d+" ', repl, s)
    open(path, "w", encoding="utf-8", newline="\n").write(s2)
    print(path, "pads renumbered:", n)


for name, text in DESCR.items():
    set_descr(os.path.join(LIB, name), text)

renumber_pads(os.path.join(LIB, "SW_PUSH_6mm.kicad_mod"), ["1", "2", "3", "4"])
print("done")
