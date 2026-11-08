"""Print a verification summary of the lab2 PCB (geometry, nets, routing)."""
import collections
import math
import os

import pcbnew

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PCB = os.path.join(ROOT, "lab2.kicad_pcb")

b = pcbnew.LoadBoard(PCB)

bb = b.GetBoardEdgesBoundingBox()
print("board outline: %.2f x %.2f mm  (origin %.2f, %.2f)" % (
    pcbnew.ToMM(bb.GetWidth()), pcbnew.ToMM(bb.GetHeight()),
    pcbnew.ToMM(bb.GetX()), pcbnew.ToMM(bb.GetY())))

print("copper layers: %d" % b.GetCopperLayerCount())
print("footprints: %d, nets: %d" % (len(b.GetFootprints()), b.GetNetCount() - 1))

widths = collections.Counter()
angles = collections.Counter()
layers = collections.Counter()
vias = 0
length = 0.0
for t in b.GetTracks():
    if t.Type() == pcbnew.PCB_VIA_T:
        vias += 1
        continue
    widths[round(pcbnew.ToMM(t.GetWidth()), 3)] += 1
    layers[t.GetLayerName()] += 1
    length += pcbnew.ToMM(t.GetLength())
    s, e = t.GetStart(), t.GetEnd()
    a = math.degrees(math.atan2(e.y - s.y, e.x - s.x)) % 180.0
    angles[round(a, 1)] += 1

print("tracks: %d (length %.1f mm), vias: %d" % (sum(widths.values()), length, vias))
print("  widths :", dict(widths))
print("  layers :", dict(layers))
print("  angles :", dict(sorted(angles.items())))

print("components:")
for fp in sorted(b.GetFootprints(), key=lambda f: f.GetReference()):
    x, y = fp.GetPosition().x, fp.GetPosition().y
    cbb = fp.GetCourtyard(pcbnew.F_CrtYd).BBox()
    print("  %-3s %-14s (%6.2f, %5.2f) rot %3.0f  pads %2d  courtyard %.2f x %.2f" % (
        fp.GetReference(), fp.GetFPIDAsString(), pcbnew.ToMM(x), pcbnew.ToMM(y),
        fp.GetOrientationDegrees(), len(fp.Pads()),
        pcbnew.ToMM(cbb.GetWidth()), pcbnew.ToMM(cbb.GetHeight())))

print("nets:")
for code, net in sorted(b.GetNetInfo().NetsByNetcode().items(), key=lambda kv: kv[1].GetNetname()):
    if code == 0:
        continue
    pads = ["%s.%s" % (p.GetParentFootprint().GetReference(), p.GetNumber())
            for p in b.GetPads() if p.GetNetCode() == code]
    print("  %-6s %s" % (net.GetNetname(), " ".join(sorted(pads))))

