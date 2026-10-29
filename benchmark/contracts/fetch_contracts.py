#!/usr/bin/env python3
"""Download the 99 contracts of this test from CUAD v1 and check them.

    python3 benchmark/contracts/fetch_contracts.py                  # downloads CUAD_v1.zip (about 106 MB) from Zenodo, then extracts and checks
    python3 benchmark/contracts/fetch_contracts.py --zip CUAD_v1.zip # use a copy you already have

CUAD v1 is published by The Atticus Project under CC BY 4.0: https://doi.org/10.5281/zenodo.4595826
The zip's md5 is checked, then every extracted PDF's SHA-256 against contracts.csv. Nothing is written outside benchmark/contracts/.
"""
import argparse, csv, hashlib, os, shutil, sys, urllib.request, zipfile

HERE = os.path.dirname(os.path.abspath(__file__))
URL = 'https://zenodo.org/api/records/4595826/files/CUAD_v1.zip/content'
MD5 = 'c38f490a984420b8a62600db401fafd5'
SIZE = 105883672


def md5_of(path):
    h = hashlib.md5()
    with open(path, 'rb') as fh:
        for block in iter(lambda: fh.read(1 << 20), b''):
            h.update(block)
    return h.hexdigest()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--zip', help='path to an existing CUAD_v1.zip')
    ap.add_argument('--out', default=os.path.join(HERE, 'pdf'), help='where to put the 99 PDFs (default benchmark/contracts/pdf)')
    args = ap.parse_args()
    rows = [r for r in csv.DictReader(open(os.path.join(HERE, 'contracts.csv'), encoding='utf-8')) if r['in_test'] == 'yes']
    assert len(rows) == 99, len(rows)
    zpath = args.zip
    if not zpath:
        zpath = os.path.join(HERE, 'CUAD_v1.zip')
        if not (os.path.exists(zpath) and os.path.getsize(zpath) == SIZE):
            print(f'downloading CUAD_v1.zip ({SIZE / 1e6:.0f} MB) from Zenodo ...')
            urllib.request.urlretrieve(URL, zpath, lambda b, bs, ts: print(f'\r  {min(100, int(b * bs * 100 / (ts if ts > 0 else SIZE)))}%', end='', flush=True))
            print()
    print('checking the zip ...')
    got = md5_of(zpath)
    if got != MD5:
        sys.exit(f'md5 mismatch: {got} (expected {MD5}). This is not the CUAD v1 zip; nothing was extracted.')
    os.makedirs(args.out, exist_ok=True)
    bad = 0
    with zipfile.ZipFile(zpath) as z:
        names = set(z.namelist())
        for r in rows:
            inner = r['path_in_cuad_zip']
            if inner not in names:
                print('  MISSING in zip:', inner)
                bad += 1
                continue
            dst = os.path.join(args.out, r['file_name'])
            with z.open(inner) as src, open(dst, 'wb') as out:
                shutil.copyfileobj(src, out)
            sha = hashlib.sha256(open(dst, 'rb').read()).hexdigest()
            if sha != r['sha256']:
                print('  SHA-256 MISMATCH:', r['file_name'])
                bad += 1
    if bad:
        sys.exit(f'{bad} problem(s). Do not use this folder.')
    print(f'ok: {len(rows)} contracts in {args.out}, every SHA-256 matches contracts.csv')


if __name__ == '__main__':
    main()
