"""Add title blocks (student / variant info) to schematic and PCB."""
import os
import re
import pcbnew

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SCH = os.path.join(ROOT, "lab2.kicad_sch")
PCB = os.path.join(ROOT, "lab2.kicad_pcb")

TITLE = "\u041b\u0420 II \u2014 \u0434\u0440\u0443\u043a\u043e\u0432\u0430\u043d\u0430 \u043f\u043b\u0430\u0442\u0430 (\u0432\u0430\u0440\u0456\u0430\u043d\u0442 30)"
COMPANY = "\u042f\u0449\u0443\u043a \u0413\u0435\u043e\u0440\u0433\u0456\u0439 \u041e\u043b\u0435\u0433\u043e\u0432\u0438\u0447"
GUID = "GUID (md5): 7cc66fd9-e47b-cdd7-b82c-09c580a12247"
REV = "1.0"
DATE = "2026-11-08"


def schematic():
    s = open(SCH, encoding="utf-8-sig").read()
    s = re.sub(r"\t\(title_block.*?\n\t\)\n", "", s, flags=re.S)
    tb = (
        "\t(title_block\n"
        '\t\t(title "%s")\n' % TITLE +
        '\t\t(date "%s")\n' % DATE +
        '\t\t(rev "%s")\n' % REV +
        '\t\t(company "%s")\n' % COMPANY +
        '\t\t(comment 1 "%s")\n' % GUID +
        "\t)\n"
    )
    s = s.replace('\t(paper "A4")\n', '\t(paper "A4")\n' + tb, 1)
    open(SCH, "w", encoding="utf-8", newline="\n").write(s)


def board():
    b = pcbnew.LoadBoard(PCB)
    tb = b.GetTitleBlock()
    tb.SetTitle(TITLE)
    tb.SetCompany(COMPANY)
    tb.SetRevision(REV)
    tb.SetDate(DATE)
    tb.SetComment(0, GUID)
    b.SetTitleBlock(tb)
    pcbnew.SaveBoard(PCB, b)


schematic()
board()
print("title blocks written")
