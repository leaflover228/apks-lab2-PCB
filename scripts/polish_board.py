"""PCB cosmetic pass: hide Value fields, keep refs clear of pads."""
import os
import pcbnew

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PCB = os.path.join(ROOT, "lab2.kicad_pcb")
MM = pcbnew.FromMM

# reference field positions (absolute, mm) for footprints whose default collides
REF_POS = {
    "J1": (4.0, 17.6),
}

b = pcbnew.LoadBoard(PCB)
for fp in b.GetFootprints():
    ref = fp.GetReference()
    value = fp.GetField(2)
    value.SetVisible(False)
    if ref in REF_POS:
        x, y = REF_POS[ref]
        f = fp.GetField(1)
        f.SetPosition(pcbnew.VECTOR2I(MM(x), MM(y)))
        f.SetTextAngle(pcbnew.EDA_ANGLE(0, pcbnew.DEGREES_T))
        f.SetKeepUpright(False)
pcbnew.SaveBoard(PCB, b)
print("board polished")
