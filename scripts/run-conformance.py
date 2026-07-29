#!/usr/bin/env python3
"""Reference conformance runner (read-only over the corpus).

Usage: run-conformance.py --engine /path/to/oo [--level L1|L2] [--corpus DIR]

Contract: conformance/README.md. Exit 0 iff all selected vectors pass.
"""
import argparse
import pathlib
import subprocess
import sys

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--engine', required=True)
    ap.add_argument('--level', default=None, help='L1 or L2 (default: all)')
    ap.add_argument('--corpus', default=None,
                    help='corpus root (default: <repo>/conformance)')
    args = ap.parse_args()

    root = pathlib.Path(args.corpus) if args.corpus else \
        pathlib.Path(__file__).resolve().parent.parent / 'conformance'
    levels = [args.level] if args.level else ['L1', 'L2']

    total, failed = 0, []
    for lvl in levels:
        for nf in sorted((root / lvl).glob('*.n')):
            total += 1
            vid = f"{lvl}-{nf.stem.split('-')[0]}"
            expect_lines = nf.with_suffix('.expect').read_text(
                encoding='utf-8').rstrip('\n').split('\n')
            # split value expectation from optional %cause line
            if expect_lines and expect_lines[-1].startswith('%cause:'):
                expect = '\n'.join(expect_lines[:-1])
                cause = expect_lines[-1]
            else:
                expect, cause = '\n'.join(expect_lines), None
            r = subprocess.run(
                [args.engine, 'run', str(nf), '--observe', 'out'],
                capture_output=True, text=True, timeout=60)
            got, err = r.stdout.strip(), r.stderr.strip()
            if expect == '_|_':
                ok = got.startswith('_|_') or 'Conflict' in err or 'Error' in err
                if ok and cause and cause.split('#')[-1] not in got + err:
                    print(f'  note {vid}: %cause 未印出(L1/L2 為 SHOULD)')
            else:
                ok = got == expect
            if not ok:
                failed.append((vid, nf.name, got or err[:100]))

    print(f'{total} vectors, {total - len(failed)} pass, {len(failed)} fail')
    for vid, name, got in failed:
        print(f'  FAIL {vid} ({name}): got {got!r}')
    sys.exit(1 if failed else 0)

if __name__ == '__main__':
    main()
