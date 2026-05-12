# Neuro Imaging Visualisation Workspace

This repository is a small workspace for reproducing and exploring **brain anatomy / cortical surface visualisations** from different neuroimaging studies.

The core tool is a Python wrapper around [Cerebro_Viewer](https://github.com/sina-mansour/Cerebro_Viewer), which renders HCP-style **CIFTI dense scalar** files (`*.dscalar.nii`) on a 3D cortical template using Panda3D. Around that core viewer, this repo adds a few practical helpers for study-specific workflows: static exports, side-by-side comparisons, and GIFTI surface plotting.

The [`studies/`](studies/) folder is the workspace for individual papers or datasets. Each study can keep its source data, generated figures, and notes together so the visualisations are easier to reproduce later.

Current added features:

1. Side-by-side comparison of two CIFTI dscalar maps on the same template, with shared colour limits by default.
2. Static PNG export for Cerebro-rendered CIFTI maps.
3. GIFTI `.func.gii` compatibility for fsaverage surface-level, left/right hemisphere visualisation.

## Quick start

Create a virtual environment and install:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -e .
pip install -U pip setuptools wheel
pip install -e . --config-settings editable_mode=strict
```


The `--config-settings editable_mode=strict` line avoids a common **macOS + Python 3.12+** issue where a normal editable install writes a small `.pth` file that **never gets applied**, so `neuro-viewer` exists but `import neuro_imaging_tool` fails. If you prefer not to use an editable install, use `pip install .` instead (package code is copied into the venv; reinstall after edits).

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

## Troubleshooting

**`ModuleNotFoundError: No module named 'neuro_imaging_tool'` when running `neuro-viewer`.**  
The console script is installed, but Python is not seeing `src/neuro_imaging_tool`. Typical causes: **editable install** used the legacy path-based `.pth` trick, which some environments skip. **Fix:** reinstall with strict editable mode (see Quick start), or run once with `PYTHONPATH=src neuro-viewer ...` from the repo root, or use a non-editable `pip install .`.

If this still does not fix module not found error, try deactivating venv and re booting:

```bash
deactivate 2>/dev/null || true
rm -rf .venv
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -U pip setuptools wheel
python -m pip install -e . --config-settings editable_mode=strict
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

## GIFTI surface visualisation

This repo can also make a static PNG from paired **left/right `.func.gii`** surface metric files. This is separate from the Cerebro `--dscalar` workflow: `.func.gii` files hold values on a specific **fsaverage** surface mesh, so you must choose the matching `--mesh` (`fsaverage`, `fsaverage6`, `fsaverage5`, or `fsaverage4`).

```bash
neuro-viewer \
  --func-gii-left /path/to/left.func.gii \
  --func-gii-right /path/to/right.func.gii \
  --mesh fsaverage5 \
  --output gifti_surface.png \
  --title "Gradient 1 (fsaverage5)" \
  --colormap viridis
```

The output is a 2x2 figure: left lateral, right lateral, left medial, and right medial, using one shared colour scale across both hemispheres. Add `--clims LOW HIGH` to fix the scale.

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
- `src/neuro_imaging_tool/gifti_viewer.py`: static fsaverage GIFTI surface plotting
- `src/neuro_imaging_tool/cli.py`: command-line entrypoint
- `scripts/example.py`: minimal Python usage example
