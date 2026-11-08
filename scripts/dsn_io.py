"""Export DSN / import SES for lab2 board (KiCad 10 pcbnew API)."""
import sys, os
import pcbnew

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PCB = os.path.join(ROOT, "lab2.kicad_pcb")
DSN = os.path.join(ROOT, "build", "lab2.dsn")
SES = os.path.join(ROOT, "build", "lab2.ses")


def main():
    mode = sys.argv[1] if len(sys.argv) > 1 else "export"
    b = pcbnew.LoadBoard(PCB)
    if mode == "export":
        os.makedirs(os.path.dirname(DSN), exist_ok=True)
        nc = b.GetAllNetClasses()["Default"]
        nc.SetClearance(pcbnew.FromMM(0.2))
        nc.SetTrackWidth(pcbnew.FromMM(0.25))
        nc.SetViaDiameter(pcbnew.FromMM(0.8))
        nc.SetViaDrill(pcbnew.FromMM(0.4))
        b.SynchronizeNetsAndNetClasses(False)
        pcbnew.SaveBoard(PCB, b)
        ok = pcbnew.ExportSpecctraDSN(b, DSN)
        print("export ->", ok, DSN, os.path.getsize(DSN) if os.path.exists(DSN) else 0)
    elif mode == "import":
        ok = pcbnew.ImportSpecctraSES(b, SES)
        print("import ->", ok)
        pcbnew.SaveBoard(PCB, b)
        b2 = pcbnew.LoadBoard(PCB)
        print("tracks:", len(b2.GetTracks()), "vias:",
              sum(1 for t in b2.GetTracks() if t.Type() == pcbnew.PCB_VIA_T))
    else:
        raise SystemExit("mode must be export|import")


if __name__ == "__main__":
    main()

