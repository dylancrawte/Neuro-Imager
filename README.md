# Neuro Imaging Personal Project

This repository is primarily a wrapper of [Cerebro_Viewer](https://github.com/sina-mansour/Cerebro_Viewer), with added features:

1. Side-by-side comparison of two CIFTI dscalar maps on the same template (shared color limits by default).

## Quick start

Create a virtual environment and install:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -e .
```

Launch the interactive viewer with bundled template data:

```bash
neuro-viewer --surface pial --bundled-dscalar
```

Use your own dscalar file:

```bash
neuro-viewer --dscalar /absolute/path/to/map.dscalar.nii
```

Save a static PNG (offscreen):

```bash
neuro-viewer --bundled-dscalar --offscreen --output brain.png
```

## Side-by-side comparison

Render two `.dscalar.nii` files next to each other with the same template and matching color scale (min/max is taken across **both** maps unless you set `--clims`):

```bash
neuro-viewer \
  --compare /absolute/path/to/a.dscalar.nii /absolute/path/to/b.dscalar.nii \
  --output compare.png \
  --titles "Scan A" "Scan B" \
  --colormap coolwarm
```

Optional fixed scale: `--clims -2 2`. Other template options (`--surface`, `--volumetric-structures`) apply to both panels.

## Colour mapping

Scalar overlays are drawn by [Cerebro](https://cerebro-viewer.readthedocs.io/): each vertex value is turned into an RGBA colour through its `data_to_colors` step (linear mapping from a numeric range into a colormap).

**Colormap.** If you pass `--colormap NAME`, the name is resolved with matplotlib (for example `coolwarm`, `viridis`) and the resulting colormap is passed to Cerebro. If you omit `--colormap`, Cerebro uses its built-in default for that layer.

**Numeric range (`clims`).** Values are clamped/normalized between a lower and upper bound before sampling the colormap:

- **Side-by-side (`--compare`)**  
  By default, the same range is used for **both** panels: the minimum and maximum over **all finite vertices in both CIFTI files together**. That keeps the two maps on a common scale so colours are comparable. Override with `--clims LOW HIGH` when you want a fixed scale (for example a known effect size range).

- **Single brain (`--dscalar` / `--bundled-dscalar`)**  
  You can pass `--clims` and `--colormap` here as well; if `--clims` is omitted, Cerebro scales from the data in that file only.

**What the colours “mean”.** The viewer maps **numbers stored in your file** to colours; it does not assign neuroanatomical labels. Which hue corresponds to “more myelin”, “deeper sulcus”, and so on depends on the **dataset and file convention** (sign, units, preprocessing). For publication-style figures, set `--clims` explicitly and document units next to the figure (this tool does not draw a colour bar on the PNG yet).

## Layout

- `src/neuro_imaging_tool/viewer.py`: thin wrapper around Cerebro APIs and comparison export
- `src/neuro_imaging_tool/cli.py`: command-line entrypoint
- `scripts/example.py`: minimal Python usage example
# Neuro-Imager
