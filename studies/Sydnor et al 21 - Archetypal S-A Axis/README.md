# Sydnor et al. 2021 - Archetypal S-A Axis

This study folder contains brain-map data for visualising the archetypal sensorimotor-association (S-A) axis from Sydnor et al. (2021). The axis describes a cortical hierarchy running from sensorimotor cortex toward association cortex.

The files were copied from the local `S-A_ArchetypalAxis` repository. Please cite:

Sydnor, V. J., et al. (2021). *Neurodevelopment of the association cortices: Patterns, mechanisms, and implications for psychopathology*. Neuron. https://doi.org/10.1016/j.neuron.2021.06.016

The source repository did not include a local license file, so keep the citation and provenance with any redistributed figures or data.

## Data

Main S-A axis brain maps:

- `data/FSLRVertex/SensorimotorAssociation_Axis.dscalar.nii` - CIFTI dense scalar map for Cerebro rendering.
- `data/FSaverage5/SensorimotorAssociation_Axis_LH.fsaverage5.func.gii` - left hemisphere fsaverage5 surface metric.
- `data/FSaverage5/SensorimotorAssociation_Axis_RH.fsaverage5.func.gii` - right hemisphere fsaverage5 surface metric.

Selected comparison maps:

- `data/FSLRVertex/T1T2ratio.dscalar.nii` - myelin-sensitive T1w/T2w ratio map.
- `data/FSLRVertex/Cortical.Thickness.dscalar.nii` - cortical thickness map.
- `data/FSLRVertex/G1.fMRI.dscalar.nii` - functional connectivity gradient map.

CSV ranking and parcel files are intentionally not copied here for now; this folder is focused on cortical brain visualisations.

## CIFTI Visualisation

Render the S-A axis CIFTI map with Cerebro:

```bash
cd "$(git rev-parse --show-toplevel)"

MPLBACKEND=Agg neuro-viewer \
  --dscalar "studies/Sydnor et al 21 - Archetypal S-A Axis/data/FSLRVertex/SensorimotorAssociation_Axis.dscalar.nii" \
  --offscreen \
  --output "studies/Sydnor et al 21 - Archetypal S-A Axis/figures/sa_axis_cerebro.png" \
  --colormap viridis
```

## GIFTI fsaverage5 Visualisation

Render both hemispheres on fsaverage5 surfaces:

```bash
cd "$(git rev-parse --show-toplevel)"

MPLBACKEND=Agg neuro-viewer \
  --func-gii-left "studies/Sydnor et al 21 - Archetypal S-A Axis/data/FSaverage5/SensorimotorAssociation_Axis_LH.fsaverage5.func.gii" \
  --func-gii-right "studies/Sydnor et al 21 - Archetypal S-A Axis/data/FSaverage5/SensorimotorAssociation_Axis_RH.fsaverage5.func.gii" \
  --mesh fsaverage5 \
  --output "studies/Sydnor et al 21 - Archetypal S-A Axis/figures/sa_axis_fsaverage5.png" \
  --title "Archetypal S-A axis (fsaverage5)" \
  --colormap viridis
```

## Suggested Comparison Renders

The copied comparison maps can be rendered individually with the same `--dscalar` workflow. For example:

```bash
MPLBACKEND=Agg neuro-viewer \
  --dscalar "studies/Sydnor et al 21 - Archetypal S-A Axis/data/FSLRVertex/T1T2ratio.dscalar.nii" \
  --offscreen \
  --output "studies/Sydnor et al 21 - Archetypal S-A Axis/figures/t1t2ratio_cerebro.png" \
  --colormap viridis
```
