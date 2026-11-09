"""Normalise all copper tracks on lab2 board to the project width (0.25 mm)."""
import os
import pcbnew

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PCB = os.path.join(ROOT, "lab2.kicad_pcb")
WIDTH = 0.25

b = pcbnew.LoadBoard(PCB)
changed = 0
for t in b.GetTracks():
    if t.Type() == pcbnew.PCB_VIA_T:
        continue
    if abs(pcbnew.ToMM(t.GetWidth()) - WIDTH) > 1e-6:
        t.SetWidth(pcbnew.FromMM(WIDTH))
        changed += 1
pcbnew.SaveBoard(PCB, b)
print("tracks widened:", changed)
