"""Align PCB footprint Value/Description fields with the schematic symbols
so that kicad-cli PCB DRC --schematic-parity has nothing to report."""
import os
import pcbnew

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PCB = os.path.join(ROOT, "lab2.kicad_pcb")

FIELDS = {
    "J1": ("1x5", "Lab2 module J1_lab2"),
    "U1": ("8x8", "Lab2 module U1_lab2"),
    "U2": ("4x4", "Lab2 module U2_lab2"),
    "U3": ("4x4", "Lab2 module U3_lab2"),
    "U4": ("4x4", "Lab2 module U4_lab2"),
    "U5": ("12x12", "Lab2 module U5_lab2"),
}

board = pcbnew.LoadBoard(PCB)
for fp in board.GetFootprints():
    ref = fp.GetReference()
    if ref not in FIELDS:
        print("skip", ref)
        continue
    value, desc = FIELDS[ref]
    fp.SetValue(value)
    fp.SetLibDescription(desc)
    for field in fp.GetFields():
        if field.GetName() == "Description":
            field.SetText(desc)
    print(ref, "->", fp.GetValue(), "|", fp.GetLibDescription())
pcbnew.SaveBoard(PCB, board)
print("done")
