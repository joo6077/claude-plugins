"""STL 을 음영 그림 PNG 로 찍는다. 화면 없이 모양을 확인할 때 쓴다.

usage: python3 render.py <stl> <png> [위아래각=20] [좌우각=-60]
"""
import sys

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
from stl import mesh


def render(stl_path, png_path, elevation, azimuth):
    model = mesh.Mesh.from_file(stl_path)
    triangles = model.vectors
    normals = np.cross(triangles[:, 1] - triangles[:, 0], triangles[:, 2] - triangles[:, 0])
    normals /= np.linalg.norm(normals, axis=1, keepdims=True) + 1e-12
    light = np.array([0.4, -0.6, 0.7])
    light /= np.linalg.norm(light)
    shade = 0.35 + 0.65 * np.clip(normals @ light, 0, 1)
    colors = np.stack([shade * 0.55, shade * 0.7, shade * 0.95, np.ones_like(shade)], axis=1)

    figure = plt.figure(figsize=(6, 6), dpi=100)
    axes = figure.add_subplot(projection="3d")
    axes.add_collection3d(Poly3DCollection(triangles, facecolors=colors, edgecolor="none"))
    low, high = model.min_, model.max_
    center, half = (low + high) / 2, (high - low).max() / 2
    for set_limit, middle in zip((axes.set_xlim, axes.set_ylim, axes.set_zlim), center):
        set_limit(middle - half, middle + half)
    axes.set_box_aspect((1, 1, 1))
    axes.view_init(elev=elevation, azim=azimuth)
    axes.set_axis_off()
    size = high - low
    axes.set_title(f"{size[0]:.1f} x {size[1]:.1f} x {size[2]:.1f} mm")
    figure.savefig(png_path, bbox_inches="tight")


if __name__ == "__main__":
    if len(sys.argv) < 3:
        sys.exit(__doc__)
    render(sys.argv[1], sys.argv[2],
           float(sys.argv[3]) if len(sys.argv) > 3 else 20.0,
           float(sys.argv[4]) if len(sys.argv) > 4 else -60.0)
