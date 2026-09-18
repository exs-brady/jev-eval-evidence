"""Re-prove this bundle: the parity chain, then every file hash.

    python3 verify.py
"""
import hashlib
import json
import pathlib
import sys

root = pathlib.Path(__file__).resolve().parent
bad = 0

print("prompt parity")
idx = json.loads((root / "prompts/prompts.json").read_text())
known = set()
for tid, m in sorted(idx.items()):
    txt = (root / "prompts" / m["file"]).read_text()
    got = hashlib.sha256((tid + "\n" + txt).encode()).hexdigest()[:16]
    ok = got == m["prompt_sha"]
    bad += not ok
    known.add(got)
    print(f"  {tid:<18} {got}  {'ok' if ok else 'MISMATCH, published ' + m['prompt_sha']}")

n, unknown = 0, {}
for f in sorted((root / "runs").rglob("*.jsonl")):
    for line in f.read_text().splitlines():
        if line.strip():
            n += 1
            s = json.loads(line)["prompt_sha"]
            if s not in known:
                unknown[s] = unknown.get(s, 0) + 1
print(f"  {n} run rows carry {len(known | set(unknown))} distinct prompt hashes; "
      f"{len(unknown)} not published")
bad += len(unknown)

print("file hashes")
man = json.loads((root / "MANIFEST.json").read_text())
miss = [r for r in man if not (root / r).exists()]
diff = [r for r in man if (root / r).exists()
        and hashlib.sha256((root / r).read_bytes()).hexdigest() != man[r]]
print(f"  {len(man)} files; {len(miss)} missing; {len(diff)} changed")
for r in (miss + diff)[:10]:
    print("   !", r)
bad += len(miss) + len(diff)

print("\nOK" if not bad else f"\n{bad} PROBLEMS")
sys.exit(1 if bad else 0)
