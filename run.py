#!/usr/bin/env python
# -*- coding: utf-8 -*-
r"""큐넷 워처 진입점 — 비공개 코어를 얹어 실행한다.

왜 저장소가 둘로 갈렸나:
    큐넷 좌석 조회 경로는 "접수 창이 열려 있는 48시간 안에만 알아낼 수 있는" 지식이라
    이 프로젝트의 사실상 유일한 진입장벽이다. 그래서 조회 코드는 비공개 저장소에 둔다.
    반면 깃헙 액션 실행 시간은 **워크플로가 도는 저장소** 기준으로 과금되고
    공개 저장소는 무제한 무료다. 그래서 실행만 여기(공개)에서 하고
    코어는 배포 키로 체크아웃해 얹는다.

    비공개 저장소를 통째로 CI 로 옮기면 월 2,000분 한도에 걸리고,
    전부 공개하면 진입장벽이 사라진다. 이 구성은 둘 다 피한다.

배포 키를 쓰는 이유:
    PAT 는 계정 전체에 권한이 열린다. 배포 키는 그 저장소 하나에만 유효하다.
    공개 저장소의 시크릿에 넣는 값이므로 권한 범위는 좁을수록 좋다.

실행: python run.py            (core/ 에 코어가 체크아웃돼 있어야 한다)
"""
import os
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
CORE = Path(os.environ.get("QNET_CORE_DIR") or (HERE / "core"))

if not (CORE / "watch.py").exists():
    print(f"[run] 코어를 찾지 못했습니다: {CORE}", file=sys.stderr)
    print("[run] 워크플로의 코어 체크아웃 단계와 배포 키를 확인하세요.", file=sys.stderr)
    sys.exit(2)

# 코어 모듈(watch/schedule/detail)이 서로를 평범한 import 로 찾게 한다.
sys.path.insert(0, str(CORE))

# 산출물은 코어 저장소의 data/ 로 몰아 커밋을 단순하게 만든다.
os.environ.setdefault("QNET_DATA_DIR", str(CORE / "data"))

import watch  # noqa: E402  (경로를 세운 뒤에 불러와야 한다)

if __name__ == "__main__":
    sys.exit(watch.main())
