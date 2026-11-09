#!/usr/bin/env python3
# 두 부품을 합친 STL 에서 이음매 근처에 새로 생긴 날카로운 모서리를 센다.
# usage: seam-check.py <합친.stl> <원본A.stl> <원본B.stl> [--angle 도(30)] [--near mm(1.5)]
#   이음매 근처 = 모서리 가운데 점이 원본 A 표면과 원본 B 표면 양쪽에서 near 안에 있는 곳.
#   날카로움 = 이웃한 두 삼각형 면이 꺾인 각도가 angle 보다 큰 모서리 (오목 · 볼록 둘 다).
#   원본 A · B 에 이미 있던 날카로운 모서리 근처(0.3 mm)는 빼고 센다 — 합쳐서 새로 생긴 것만 본다.
# 출력: 마지막 줄 `SEAM sharp=<개수> checked=<이음매 근처 모서리 수> angle=<도> near=<mm>`, 날카로운 자리는 최대 10 줄.
# 종료 코드: 0 통과(날카로움 0) · 1 날카로운 모서리 있음 · 2 입력 오류(파일 없음 · 이음매 근처 모서리 0 개)
import argparse
import sys

import numpy as np
from scipy.spatial import cKDTree
from stl import mesh as stl_mesh

EXCLUDE_MM = 0.3


def load(path):
    try:
        return stl_mesh.Mesh.from_file(path).vectors.astype(np.float64)
    except Exception as error:
        print(f"STL 을 못 읽었다: {path} ({error})", file=sys.stderr)
        sys.exit(2)


def sharp_edges(tris, angle_deg):
    """(가운데 점, 양 끝 점, 꺾인 각도) — 각도가 angle_deg 보다 큰 모서리만. 같은 자리 꼭짓점은 0.001 mm 로 합친다."""
    keys = np.round(tris.reshape(-1, 3) * 1000).astype(np.int64)
    _, vid = np.unique(keys, axis=0, return_inverse=True)
    vid = vid.reshape(-1, 3)
    pts = tris.reshape(-1, 3)
    first = {}
    for i in range(len(vid)):
        first.setdefault(vid[i][0], pts[i * 3]); first.setdefault(vid[i][1], pts[i * 3 + 1]); first.setdefault(vid[i][2], pts[i * 3 + 2])
    normals = np.cross(tris[:, 1] - tris[:, 0], tris[:, 2] - tris[:, 0])
    area = np.linalg.norm(normals, axis=1)
    ok = area > 1e-9
    normals[ok] /= area[ok, None]
    owners = {}
    for f in np.nonzero(ok)[0]:
        a, b, c = vid[f]
        for e in ((a, b), (b, c), (c, a)):
            owners.setdefault((min(e), max(e)), []).append(f)
    mids, ends, angles = [], [], []
    for (a, b), faces in owners.items():
        if len(faces) != 2:
            continue
        cos = float(np.clip(np.dot(normals[faces[0]], normals[faces[1]]), -1, 1))
        angle = np.degrees(np.arccos(cos))
        if angle > angle_deg:
            pa, pb = np.array(first[a]), np.array(first[b])
            mids.append((pa + pb) / 2); ends.append((pa, pb)); angles.append(angle)
    return np.array(mids).reshape(-1, 3), ends, np.array(angles)


def all_edge_mids(tris):
    return np.concatenate([(tris[:, 0] + tris[:, 1]) / 2, (tris[:, 1] + tris[:, 2]) / 2, (tris[:, 2] + tris[:, 0]) / 2])


def surface_samples(tris, step):
    """삼각형마다 간격 step 안팎으로 점을 고르게 뿌린다 — 표면까지 거리를 점 구름 거리로 어림한다."""
    out = [tris.reshape(-1, 3)]
    for t in tris:
        longest = max(np.linalg.norm(t[1] - t[0]), np.linalg.norm(t[2] - t[1]), np.linalg.norm(t[0] - t[2]))
        n = int(np.ceil(longest / step))
        if n < 2:
            continue
        i, j = np.meshgrid(np.arange(n + 1), np.arange(n + 1))
        keep = i + j <= n
        u, v = i[keep] / n, j[keep] / n
        out.append(t[0] + u[:, None] * (t[1] - t[0]) + v[:, None] * (t[2] - t[0]))
    return np.concatenate(out)


def edge_samples(ends, step):
    out = []
    for pa, pb in ends:
        n = max(1, int(np.ceil(np.linalg.norm(pb - pa) / step)))
        out.append(pa + np.linspace(0, 1, n + 1)[:, None] * (pb - pa))
    return np.concatenate(out) if out else np.zeros((0, 3))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("merged"); parser.add_argument("a"); parser.add_argument("b")
    parser.add_argument("--angle", type=float, default=30.0)
    parser.add_argument("--near", type=float, default=1.5)
    args = parser.parse_args()
    merged, a, b = load(args.merged), load(args.a), load(args.b)
    step = args.near / 4
    tree_a, tree_b = cKDTree(surface_samples(a, step)), cKDTree(surface_samples(b, step))
    near_limit = args.near + step

    def near_both(points):
        if len(points) == 0:
            return np.zeros(0, bool)
        # 거리 상한을 주지 않으면 멀리 떨어진 점마다 나무 전체를 뒤져 실제 부품에서 5 분 넘게 걸린다
        hit = np.isfinite(tree_b.query(points, distance_upper_bound=near_limit)[0])
        hit[hit] = np.isfinite(tree_a.query(points[hit], distance_upper_bound=near_limit)[0])
        return hit

    checked = int(near_both(all_edge_mids(merged)).sum())
    if checked == 0:
        print(f"이음매 근처 모서리가 0 개다 — 두 원본이 합친 STL 과 같은 좌표인지 본다 (near={args.near})", file=sys.stderr)
        sys.exit(2)
    mids, _, angles = sharp_edges(merged, args.angle)
    seam = near_both(mids)
    base = [e for t in (a, b) for e in sharp_edges(t, args.angle)[1]]
    if base:
        dist = cKDTree(edge_samples(base, 0.1)).query(mids)[0] if len(mids) else np.zeros(0)
        seam &= dist > EXCLUDE_MM
    hits = np.nonzero(seam)[0]
    for k in hits[np.argsort(-angles[hits])][:10]:
        x, y, z = mids[k]
        print(f"SHARP angle={angles[k]:.0f} at=({x:.1f},{y:.1f},{z:.1f})")
    print(f"SEAM sharp={len(hits)} checked={checked} angle={args.angle:g} near={args.near:g}")
    sys.exit(1 if len(hits) else 0)


if __name__ == "__main__":
    main()
