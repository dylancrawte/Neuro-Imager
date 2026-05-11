from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any

import matplotlib.pyplot as plt
import nibabel as nib
import numpy as np
from cerebro import cerebro_brain_utils as cbu
from cerebro import cerebro_brain_viewer as cbv


@dataclass
class ViewerConfig:
    surface: str = "pial"
    volumetric_structures: str = "none"
    offscreen: bool = False
    background_color: tuple[float, float, float, float] = (1.0, 1.0, 1.0, 0.0)


def _ensure_parent_dir(path: str | Path) -> None:
    Path(path).expanduser().parent.mkdir(parents=True, exist_ok=True)


def colormap_for_layer(colormap: str | Any | None) -> Any | None:
    """Cerebro `data_to_colors` expects a callable colormap, not a string name."""
    if colormap is None:
        return None
    if isinstance(colormap, str):
        return plt.get_cmap(colormap)
    return colormap


class BrainViewerWrapper:
    """Thin convenience layer over Cerebro_brain_viewer for personal projects."""

    def __init__(self, config: ViewerConfig | None = None) -> None:
        self.config = config or ViewerConfig()
        self.viewer = cbv.Cerebro_brain_viewer(
            offscreen=self.config.offscreen,
            background_color=self.config.background_color,
        )

    def load_template_brain(self) -> None:
        self.viewer.load_template_GIFTI_cortical_surface_models(self.config.surface)
        self.viewer.visualize_cifti_space(
            volumetric_structures=self.config.volumetric_structures
        )

    def add_bundled_dscalar(self, **kwargs: Any) -> None:
        dscalar_file = cbu.get_data_file("templates/HCP/dscalars/hcp.gradients.dscalar.nii")
        self.viewer.add_cifti_dscalar_layer(dscalar_file=dscalar_file, **kwargs)

    def add_dscalar(self, dscalar_file: str | Path, **kwargs: Any) -> None:
        self.viewer.add_cifti_dscalar_layer(dscalar_file=str(dscalar_file), **kwargs)

    def show(self) -> None:
        self.viewer.show()

    def save_png(self, output_path: str | Path, figsize: tuple[int, int] = (10, 8)) -> None:
        _ensure_parent_dir(output_path)
        fig, ax = plt.subplots(figsize=figsize)
        ax.axis("off")
        self.viewer.offscreen_draw_to_matplotlib_axes(ax)
        fig.savefig(output_path, dpi=200, bbox_inches="tight", pad_inches=0)
        plt.close(fig)


def shared_dscalar_clims(left: Path, right: Path) -> tuple[float, float]:
    """Min/max over finite values in both dscalar files (same scale for comparison)."""
    stacked_parts: list[np.ndarray] = []
    for path in (left, right):
        data = np.asarray(nib.load(str(path)).get_fdata(), dtype=np.float64).ravel()
        data = data[np.isfinite(data)]
        if data.size == 0:
            raise ValueError(f"No finite scalar values in {path}")
        stacked_parts.append(data)
    stacked = np.concatenate(stacked_parts)
    return float(stacked.min()), float(stacked.max())


def _offscreen_render_to_axes(
    ax: Any,
    *,
    config: ViewerConfig,
    dscalar_path: Path,
    layer_kwargs: dict[str, Any],
) -> None:
    """One offscreen viewer at a time to reduce GL context contention."""
    cfg = ViewerConfig(
        surface=config.surface,
        volumetric_structures=config.volumetric_structures,
        offscreen=True,
        background_color=config.background_color,
    )
    wrapper = BrainViewerWrapper(cfg)
    wrapper.load_template_brain()
    wrapper.add_dscalar(dscalar_path, **layer_kwargs)
    wrapper.viewer.offscreen_draw_to_matplotlib_axes(ax)


def save_comparison_png(
    left_dscalar: str | Path,
    right_dscalar: str | Path,
    output_path: str | Path,
    *,
    surface: str = "pial",
    volumetric_structures: str = "none",
    background_color: tuple[float, float, float, float] = (1.0, 1.0, 1.0, 0.0),
    titles: tuple[str, str] | None = None,
    colormap: str | None = None,
    clims: tuple[float, float] | None = None,
    figsize: tuple[int, int] = (20, 8),
) -> None:
    left_path = Path(left_dscalar)
    right_path = Path(right_dscalar)
    layer_kwargs: dict[str, Any] = {}
    cm = colormap_for_layer(colormap)
    if cm is not None:
        layer_kwargs["colormap"] = cm
    layer_kwargs["clims"] = clims if clims is not None else shared_dscalar_clims(left_path, right_path)

    base = ViewerConfig(
        surface=surface,
        volumetric_structures=volumetric_structures,
        offscreen=True,
        background_color=background_color,
    )

    fig, axes = plt.subplots(1, 2, figsize=figsize)
    for ax in axes:
        ax.axis("off")

    _offscreen_render_to_axes(axes[0], config=base, dscalar_path=left_path, layer_kwargs=layer_kwargs)
    _offscreen_render_to_axes(axes[1], config=base, dscalar_path=right_path, layer_kwargs=layer_kwargs)

    if titles is not None:
        axes[0].set_title(titles[0])
        axes[1].set_title(titles[1])

    _ensure_parent_dir(output_path)
    fig.savefig(output_path, dpi=200, bbox_inches="tight", pad_inches=0)
    plt.close(fig)
