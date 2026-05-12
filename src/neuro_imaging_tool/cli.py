from __future__ import annotations

import argparse
from pathlib import Path
from typing import Any

from .gifti_viewer import SUPPORTED_FSAVERAGE_MESHES, save_func_gii_png
from .viewer import BrainViewerWrapper, ViewerConfig, colormap_for_layer, save_comparison_png


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Personal neuroimaging viewer (Cerebro wrapper)")
    parser.add_argument("--surface", default="pial", help="Template surface: pial, inflated, midthickness, etc.")
    parser.add_argument(
        "--volumetric-structures",
        default="none",
        choices=["none", "subcortex", "all"],
        help="Which volumetric structures to show",
    )
    parser.add_argument("--dscalar", type=Path, help="Path to a CIFTI dscalar file")
    parser.add_argument(
        "--bundled-dscalar",
        action="store_true",
        help="Use bundled HCP example dscalar",
    )
    parser.add_argument(
        "--compare",
        nargs=2,
        type=Path,
        metavar=("DSCALAR_A", "DSCALAR_B"),
        help="Compare two CIFTI dscalar files side by side (requires --output)",
    )
    parser.add_argument(
        "--clims",
        nargs=2,
        type=float,
        metavar=("LOW", "HIGH"),
        help="Fixed color limits for overlays (passed to Cerebro when adding dscalar layers)",
    )
    parser.add_argument(
        "--colormap",
        help="Matplotlib colormap name passed to Cerebro data_to_colors (e.g. coolwarm)",
    )
    parser.add_argument(
        "--titles",
        nargs=2,
        metavar=("TITLE_A", "TITLE_B"),
        help="Panel titles for --compare",
    )
    parser.add_argument("--title", help="Figure title for GIFTI surface PNG export")
    parser.add_argument(
        "--func-gii-left",
        type=Path,
        help="Left-hemisphere GIFTI metric file for static surface PNG export",
    )
    parser.add_argument(
        "--func-gii-right",
        type=Path,
        help="Right-hemisphere GIFTI metric file for static surface PNG export",
    )
    parser.add_argument(
        "--mesh",
        default="fsaverage5",
        choices=SUPPORTED_FSAVERAGE_MESHES,
        help="fsaverage mesh resolution for --func-gii-left/--func-gii-right",
    )
    parser.add_argument("--offscreen", action="store_true", help="Render offscreen and optionally save PNG")
    parser.add_argument("--output", type=Path, help="Output PNG path (use with --offscreen or --compare)")
    return parser


def parse_args() -> argparse.Namespace:
    return _build_parser().parse_args()


def main() -> None:
    parser = _build_parser()
    args = parser.parse_args()

    gifti_mode = args.func_gii_left is not None or args.func_gii_right is not None
    if gifti_mode:
        if args.dscalar is not None or args.bundled_dscalar or args.compare is not None:
            parser.error("--func-gii-left/--func-gii-right cannot be used with CIFTI modes")
        if args.offscreen:
            parser.error("--func-gii-left/--func-gii-right always saves a static PNG; do not pass --offscreen")
        if args.func_gii_left is None or args.func_gii_right is None:
            parser.error("--func-gii-left and --func-gii-right must be provided together")
        if args.output is None:
            parser.error("--func-gii-left/--func-gii-right requires --output PATH.png")
        for p in (args.func_gii_left, args.func_gii_right):
            if not p.is_file():
                parser.error(f"not a file: {p}")
        clims = tuple(args.clims) if args.clims is not None else None
        save_func_gii_png(
            args.func_gii_left,
            args.func_gii_right,
            args.output,
            mesh=args.mesh,
            colormap=args.colormap or "viridis",
            clims=clims,
            title=args.title,
        )
        print(f"Saved GIFTI surface render to: {args.output}")
        return

    if args.compare is not None:
        if args.dscalar is not None or args.bundled_dscalar:
            parser.error("--compare cannot be used with --dscalar or --bundled-dscalar")
        if args.offscreen:
            parser.error("--compare always saves offscreen; do not pass --offscreen")
        if args.output is None:
            parser.error("--compare requires --output PATH.png")
        for p in args.compare:
            if not p.is_file():
                parser.error(f"not a file: {p}")
        titles = tuple(args.titles) if args.titles is not None else None
        clims = tuple(args.clims) if args.clims is not None else None
        save_comparison_png(
            args.compare[0],
            args.compare[1],
            args.output,
            surface=args.surface,
            volumetric_structures=args.volumetric_structures,
            titles=titles,
            colormap=args.colormap,
            clims=clims,
        )
        print(f"Saved comparison to: {args.output}")
        return

    config = ViewerConfig(
        surface=args.surface,
        volumetric_structures=args.volumetric_structures,
        offscreen=args.offscreen,
    )
    wrapper = BrainViewerWrapper(config)
    wrapper.load_template_brain()

    layer_kw: dict[str, Any] = {}
    cm = colormap_for_layer(args.colormap)
    if cm is not None:
        layer_kw["colormap"] = cm
    if args.clims is not None:
        layer_kw["clims"] = tuple(args.clims)

    if args.bundled_dscalar:
        wrapper.add_bundled_dscalar(**layer_kw)
    if args.dscalar is not None:
        wrapper.add_dscalar(args.dscalar, **layer_kw)

    if args.offscreen:
        if args.output:
            wrapper.save_png(args.output)
            print(f"Saved brain render to: {args.output}")
        else:
            print("Offscreen render configured. Add --output <path.png> to save an image.")
        return

    wrapper.show()


if __name__ == "__main__":
    main()
