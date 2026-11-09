"""PCB cosmetic pass: hide Value fields (kept on F.Fab for documentation)."""
import os
import pcbnew

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PCB = os.path.join(ROOT, "lab2.kicad_pcb")

b = pcbnew.LoadBoard(PCB)
for fp in b.GetFootprints():
    fp.GetField(2).SetVisible(False)
pcbnew.SaveBoard(PCB, b)
print("values hidden:", len(b.GetFootprints()))
