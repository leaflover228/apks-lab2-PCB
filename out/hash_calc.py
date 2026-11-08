#!/usr/bin/env python3
"""hash_calc.py - обчислення контрольних сум результатів ЛР II (варіант 30).

Приклад:
    python out/hash_calc.py                # хеші всіх файлів у out/
    python out/hash_calc.py lab2.kicad_pcb # хеш конкретного файлу

Друкує MD5 та SHA-256 для кожного файлу, а також MD5 від GUID студента
(ідентифікатор варіанта з AGENTS.md).
"""
import hashlib
import os
import sys

GUID = "7cc66fd9-e47b-cdd7-b82c-09c580a12247"

SKIP_DIRS = {"__pycache__"}


def file_hash(path, algo="md5", chunk=1 << 20):
    h = hashlib.new(algo)
    with open(path, "rb") as fh:
        for block in iter(lambda: fh.read(chunk), b""):
            h.update(block)
    return h.hexdigest()


def walk(targets):
    for target in targets:
        if os.path.isdir(target):
            for root, dirs, files in os.walk(target):
                dirs[:] = sorted(d for d in dirs if d not in SKIP_DIRS)
                for name in sorted(files):
                    if name == os.path.basename(__file__):
                        continue
                    yield os.path.join(root, name)
        elif os.path.isfile(target):
            yield target
        else:
            print("!! не знайдено: %s" % target, file=sys.stderr)


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    targets = sys.argv[1:] or [here]
    rows = []
    for path in walk(targets):
        size = os.path.getsize(path)
        rows.append((os.path.relpath(path, here), size,
                     file_hash(path, "md5"), file_hash(path, "sha256")))

    print("GUID: %s" % GUID)
    print("MD5(GUID): %s" % hashlib.md5(GUID.encode("utf-8")).hexdigest())
    print("Варіант: 30")
    print()
    print("%-32s %10s  %-32s  %s" % ("файл", "байт", "MD5", "SHA-256"))
    print("-" * 120)
    for name, size, md5, sha in rows:
        print("%-32s %10d  %-32s  %s" % (name, size, md5, sha))

    out_txt = os.path.join(here, "hashes.txt")
    with open(out_txt, "w", encoding="utf-8") as fh:
        fh.write("GUID: %s\nMD5(GUID): %s\nВаріант: 30\n\n" %
                 (GUID, hashlib.md5(GUID.encode("utf-8")).hexdigest()))
        for name, size, md5, sha in rows:
            fh.write("%s  %d  %s  %s\n" % (name, size, md5, sha))
    print("\nЗбережено: %s" % out_txt)


if __name__ == "__main__":
    main()
