# -*- coding: utf-8 -*-
import re
from collections import defaultdict, Counter
from pathlib import Path

#SRC = Path("output_list_bulk.txt")            # 입력 파일 경로
SRC = Path("template.txt")            # 입력 파일 경로
OUT_DIR = Path("./outfiles")                           # 출력 디렉터리

text = SRC.read_text(encoding="utf-8", errors="ignore")

# 문단 분리: 빈 줄(연속 개수 무관) 기준
paragraphs = [p.strip("\n") for p in re.split(r"\n{2,}", text.strip()) if p.strip("\n")]

year_re = re.compile(r"/(?P<year>\d{4})년/")
buckets = defaultdict(list)
last_year = None

for p in paragraphs:
    years = [m.group("year") for m in year_re.finditer(p)]
    years = list(dict.fromkeys(years))  # 중복 제거 + 순서 보존
    if years:
        for y in years:
            buckets[y].append(p)
        last_year = years[-1]
    else:
        if last_year is not None:
            buckets[last_year].append(p)
        else:
            buckets["unknown"].append(p)

OUT_DIR.mkdir(parents=True, exist_ok=True)
for year, blocks in sorted(buckets.items()):
    out = OUT_DIR / f"output_{year}.txt"
    out.write_text("\n\n".join(blocks).rstrip(), encoding="utf-8")

print("done:", sorted(f.name for f in OUT_DIR.glob("output_*.txt")))