"""Build lab2 PCB: footprints, nets, board outline. KiCad 10 pcbnew API."""
import sys, os
import pcbnew

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LIB = os.path.join(ROOT, "lib", "lab2.pretty")
OUT = os.path.join(ROOT, "lab2.kicad_pcb")

MM = pcbnew.FromMM

COMPONENTS = [
    # ref, footprint, value, x, y, rotation
    ("J1", "J1_1x5_P2.54", "Conn_1x5", 4, 25, 0),
    ("U1", "U1_8x8", "U1_8x8", 28, 14, 0),
    ("U2", "U2_4x4", "U2_4x4", 16, 38, 0),
    ("U3", "U3_4x4", "U3_4x4", 30, 30, 0),
    ("U4", "U4_4x4", "U4_4x4", 44, 42, 0),
    ("U5", "U5_12x12", "U5_12x12", 52, 26, 0),
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

BOARD_W, BOARD_H = 80.0, 50.0


def add_edge(b, x1, y1, x2, y2, width=0.1):
    s = pcbnew.PCB_SHAPE(b)
    s.SetShape(pcbnew.SHAPE_T_SEGMENT)
    s.SetStart(pcbnew.VECTOR2I(MM(x1), MM(y1)))
    s.SetEnd(pcbnew.VECTOR2I(MM(x2), MM(y2)))
    s.SetLayer(pcbnew.Edge_Cuts)
    s.SetWidth(MM(width))
    b.Add(s)


def main():
    b = pcbnew.CreateEmptyBoard()
    b.SetFileName(OUT)

    ds = b.GetDesignSettings()
    ds.SetBoardThickness(MM(1.6))
    try:
        nc = ds.GetDefaultNetClass()
        nc.SetClearance(MM(0.2))
        nc.SetTrackWidth(MM(0.25))
        nc.SetViaDiameter(MM(0.8))
        nc.SetViaDrill(MM(0.4))
    except Exception as e:
        print("netclass warn:", e)

    for name in NETS:
        b.Add(pcbnew.NETINFO_ITEM(b, name))

    fps = {}
    for ref, fpname, value, x, y, rot in COMPONENTS:
        fp = pcbnew.FootprintLoad(LIB, fpname)
        if fp is None:
            raise RuntimeError("footprint not loaded: " + fpname)
        fp.SetReference(ref)
        fp.SetValue(value)
        fp.SetPosition(pcbnew.VECTOR2I(MM(x), MM(y)))
        if rot:
            fp.SetOrientationDegrees(rot)
        b.Add(fp)
        fps[ref] = fp
        print("placed %s at (%.2f,%.2f) rot %d pads=%d" %
              (ref, x, y, rot, len(fp.Pads())))

    # assign nets
    for netname, pins in NETS.items():
        net = b.FindNet(netname)
        if net is None:
            raise RuntimeError("net missing: " + netname)
        for ref, padnum in pins:
            pad = fps[ref].FindPadByNumber(padnum)
            if pad is None:
                raise RuntimeError("pad %s.%s missing" % (ref, padnum))
            pad.SetNet(net)

    # board outline
    add_edge(b, 0, 0, BOARD_W, 0)
    add_edge(b, BOARD_W, 0, BOARD_W, BOARD_H)
    add_edge(b, BOARD_W, BOARD_H, 0, BOARD_H)
    add_edge(b, 0, BOARD_H, 0, 0)

    pcbnew.SaveBoard(OUT, b)
    print("saved", OUT)

    # verify
    b2 = pcbnew.LoadBoard(OUT)
    print("footprints:", len(b2.GetFootprints()))
    print("nets:", b2.GetNetCount() - 1)
    unassigned = []
    for fp in b2.GetFootprints():
        for p in fp.Pads():
            if p.GetNetCode() == 0:
                unassigned.append("%s.%s" % (fp.GetReference(), p.GetNumber()))
    print("unassigned pads:", unassigned)
    print("nets detail:")
    for netname in sorted(NETS):
        pads = ["%s.%s" % (p.GetParentFootprint().GetReference(), p.GetNumber())
                for p in b2.GetPads() if p.GetNetname() == netname]
        print("  %-4s %s" % (netname, " ".join(sorted(pads))))


if __name__ == "__main__":
    main()
