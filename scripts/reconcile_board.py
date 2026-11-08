"""Reconcile lab2 board with schematic: FPIDs, library descriptions, net name paths."""
import os
import pcbnew

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PCB = os.path.join(ROOT, "lab2.kicad_pcb")

FPIDS = {
    "J1": ("J1_1x5_P2.54", "Lab2 1x5 connector"),
    "U1": ("U1_8x8", "Lab2 module U1_lab2"),
    "U2": ("U2_4x4", "Lab2 module U2_lab2"),
    "U3": ("U3_4x4", "Lab2 module U3_lab2"),
    "U4": ("U4_4x4", "Lab2 module U4_lab2"),
    "U5": ("U5_12x12", "Lab2 module U5_lab2"),
}


def main():
    b = pcbnew.LoadBoard(PCB)

    for fp in b.GetFootprints():
        ref = fp.GetReference()
        name, desc = FPIDS[ref]
        fp.SetFPID(pcbnew.LIB_ID("lab2", name))
        fp.SetLibDescription(desc)
        d = fp.GetField(5)
        if d is not None:
            d.SetText(desc)
        # make sure link is not flagged as a local override
        fp.SetAttributes(fp.GetAttributes() & ~pcbnew.FP_BOARD_ONLY)

    # schematic root-sheet local labels become "/NAME" net names on the board
    for code, net in b.GetNetInfo().NetsByNetcode().items():
        if code == 0:
            continue
        name = net.GetNetname()
        if not name.startswith("/"):
            net.SetNetname("/" + name)

    pcbnew.SaveBoard(PCB, b)
    b2 = pcbnew.LoadBoard(PCB)
    print("footprints:", [(f.GetReference(), f.GetFPIDAsString()) for f in b2.GetFootprints()])
    print("nets:", sorted(n.GetNetname() for n in b2.GetNetInfo().NetsByNetcode().values() if n.GetNetCode()))
    print("tracks:", len(b2.GetTracks()))


if __name__ == "__main__":
    main()
