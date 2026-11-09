"""Reconcile lab2 board with schematic: FPIDs, library descriptions, net name paths."""
import os
import pcbnew

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PCB = os.path.join(ROOT, "lab2.kicad_pcb")

FPIDS = {
    "J1": ("J1_1x5_P2.54", "Lab2 1x5 pin header, 2.54 mm"),
    "U1": ("U1_SOIC-8_P1.27", "Lab2 SOIC-8 IC, 1.27 mm pitch"),
    "U2": ("SW_PUSH_6mm", "Lab2 6 mm push button"),
    "U3": ("SW_PUSH_6mm", "Lab2 6 mm push button"),
    "U4": ("SW_PUSH_6mm", "Lab2 6 mm push button"),
    "U5": ("U5_2x06_P2.54", "Lab2 2x6 test header, 2.54 mm"),
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
