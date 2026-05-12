from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import nibabel as nib
import numpy as np
from nilearn import datasets, plotting, surface


SUPPORTED_FSAVERAGE_MESHES = ("fsaverage", "fsaverage6", "fsaverage5", "fsaverage4")


def _ensure_parent_dir(path: str | Path) -> None:
    Path(path).expanduser().parent.mkdir(parents=True, exist_ok=True)


def load_gifti_metric(path: str | Path) -> np.ndarray:
    """Load the first data array from a GIFTI functional metric file."""
    img = nib.load(str(path))
    if not getattr(img, "darrays", None):
        raise ValueError(f"No data arrays found in {path}")

    data = np.asarray(img.darrays[0].data, dtype=np.float64).ravel()
    if data.size == 0:
        raise ValueError(f"No scalar data found in {path}")
    return data


def _shared_clims(left_data: np.ndarray, right_data: np.ndarray) -> tuple[float, float]:
    finite = np.concatenate(
        [left_data[np.isfinite(left_data)], right_data[np.isfinite(right_data)]]
    )
    if finite.size == 0:
        raise ValueError("No finite scalar values found across the GIFTI files")
    return float(finite.min()), float(finite.max())


def _mesh_attr(mesh_data: object, name: str) -> str:
    value = getattr(mesh_data, name)
    return str(value)


def _validate_metric_size(metric: np.ndarray, surf_mesh: str, label: str) -> None:
    coords, _faces = surface.load_surf_mesh(surf_mesh)
    if metric.size != coords.shape[0]:
        raise ValueError(
            f"{label} metric has {metric.size} values, but the selected mesh has "
            f"{coords.shape[0]} vertices. Choose the matching --mesh value."
        )


def save_func_gii_png(
    left_path: str | Path,
    right_path: str | Path,
    output_path: str | Path,
    *,
    mesh: str = "fsaverage5",
    colormap: str = "viridis",
    clims: tuple[float, float] | None = None,
    title: str | None = None,
    figsize: tuple[int, int] = (14, 8),
) -> None:
    """Render left/right fsaverage GIFTI metric files as a static PNG."""
    if mesh not in SUPPORTED_FSAVERAGE_MESHES:
        supported = ", ".join(SUPPORTED_FSAVERAGE_MESHES)
        raise ValueError(f"Unsupported mesh '{mesh}'. Supported values: {supported}")

    left_data = load_gifti_metric(left_path)
    right_data = load_gifti_metric(right_path)
    vmin, vmax = clims if clims is not None else _shared_clims(left_data, right_data)

    fsaverage = datasets.fetch_surf_fsaverage(mesh=mesh)
    left_mesh = _mesh_attr(fsaverage, "pial_left")
    right_mesh = _mesh_attr(fsaverage, "pial_right")
    left_bg = _mesh_attr(fsaverage, "sulc_left")
    right_bg = _mesh_attr(fsaverage, "sulc_right")

    _validate_metric_size(left_data, left_mesh, "Left")
    _validate_metric_size(right_data, right_mesh, "Right")

    fig, axes = plt.subplots(2, 2, figsize=figsize, subplot_kw={"projection": "3d"})
    plot_specs = [
        (axes[0, 0], left_mesh, left_data, left_bg, "left", "lateral", "Left lateral"),
        (axes[0, 1], right_mesh, right_data, right_bg, "right", "lateral", "Right lateral"),
        (axes[1, 0], left_mesh, left_data, left_bg, "left", "medial", "Left medial"),
        (axes[1, 1], right_mesh, right_data, right_bg, "right", "medial", "Right medial"),
    ]

    for ax, surf_mesh, metric, bg_map, hemi, view, panel_title in plot_specs:
        plotting.plot_surf_stat_map(
            surf_mesh,
            metric,
            hemi=hemi,
            view=view,
            bg_map=bg_map,
            cmap=colormap,
            colorbar=False,
            vmin=vmin,
            vmax=vmax,
            axes=ax,
            figure=fig,
            title=panel_title,
        )

    if title is not None:
        fig.suptitle(title)

    scalar_map = plt.cm.ScalarMappable(
        norm=plt.Normalize(vmin=vmin, vmax=vmax),
        cmap=plt.get_cmap(colormap),
    )
    scalar_map.set_array([])
    fig.colorbar(scalar_map, ax=axes.ravel().tolist(), shrink=0.7, label="Scalar value")

    _ensure_parent_dir(output_path)
    fig.savefig(output_path, dpi=200, bbox_inches="tight")
    plt.close(fig)
