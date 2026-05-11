# Freidrich et al. — study folder

This folder holds materials related to **cortical functional gradients** and their use alongside **interhemispheric** anatomy. The cortical input is the same *kind* of data described in Margulies et al. (2016): a **principal gradient** of resting-state functional connectivity, running from **unimodal / sensory–motor** cortex toward **transmodal / default-mode–associated** cortex.

---

## Cortical visualisation (`hcp_gradients_cerebro.png`)

This image is produced with the repository’s **Cerebro** wrapper from the local CIFTI file  
`studies/Freidrich et al 24/data/Gradients_Margulies2016/hcp.gradients.dscalar.nii` (see commands below). It is **not** a figure panel copied from the paper; it is the same *class* of data the authors used as the **cortical principal gradient** prior to callosal analysis (cf. Friedrich et al., 2020, Figure 2A: cortical principal gradient).

<table>
<tr>
<td align="center" valign="top" width="62%">

<img src="figures/hcp_gradients_cerebro.png" alt="Left hemisphere: principal gradient on HCP cortical mesh (viridis)" width="480"/>

<p><em>Cortical map from <code>hcp.gradients.dscalar.nii</code> — first / default scalar map, <code>viridis</code> overlay on the HCP template (Cerebro export).</em></p>

</td>
<td valign="top" width="38%">

<img src="figures/viridis_gradient_key.svg" alt="Viridis colour scale: low purple to high yellow" width="200"/>

<p><strong>What the colours show</strong></p>

<p>Each vertex is coloured by its <strong>numeric value</strong> in the loaded map after the viewer’s automatic scaling (<a href="../../README.md#colour-mapping">colour mapping</a> in the main README). This export used <code>--colormap viridis</code> and did not set <code>--clims</code>, so Cerebro rescales the displayed map to the data range in that file.</p>

<p><strong>Typical neuroscientific reading</strong> (Margulies et al., 2016 <em>principal gradient</em>):</p>

<ul>
<li><strong>Yellow / bright end</strong> — higher scalar values; often overlap <strong>transmodal / default-mode–related</strong> association cortex (wording depends on embedding sign).</li>
<li><strong>Purple / dark end</strong> — lower values; often overlap <strong>unimodal / sensory–motor</strong> style regions.</li>
<li><strong>Teal–green</strong> — intermediate positions along the same large-scale axis.</li>
</ul>

<p><strong>Friedrich et al. (2020)</strong> use this cortical field as input, bin it into gradient-percentage masks, and relate those masks to <strong>callosal</strong> tractography — this figure shows only the <strong>cortex</strong>, not the corpus callosum.</p>

<p>If the CIFTI holds <strong>multiple</strong> maps, Cerebro may show only the <strong>default</strong> column until <code>dscalar_index</code> is exposed in the CLI.</p>

</td>
</tr>
</table>

**Surface geometry:** HCP-style **group cortical mesh** in CIFTI space (Cerebro template), **lateral left hemisphere** — not an individual’s native anatomy.

---

## Commands (from repository root)

`neuro-viewer` creates parent directories for `--output` automatically.

```bash
cd "$(git rev-parse --show-toplevel)"

MPLBACKEND=Agg neuro-viewer \
  --dscalar "studies/Freidrich et al 24/data/Gradients_Margulies2016/hcp.gradients.dscalar.nii" \
  --offscreen \
  --output "studies/Freidrich et al 24/figures/hcp_gradients_cerebro.png" \
  --colormap viridis
```

Optional **side-by-side** comparison (e.g. gradients CIFTI vs an example morphometry map):

```bash
cd "$(git rev-parse --show-toplevel)"

MPLBACKEND=Agg neuro-viewer \
  --compare \
  "studies/Freidrich et al 24/data/Gradients_Margulies2016/hcp.gradients.dscalar.nii" \
  "src/data/dscalars/S1200.MyelinMap_BC_MSMAll.32k_fs_LR.dscalar.nii" \
  --output "studies/Freidrich et al 24/figures/gradients_vs_myelin.png" \
  --titles "Principal gradient (CIFTI)" "HCP-style myelin (example)" \
  --colormap coolwarm
```

Other files under `data/Gradients_Margulies2016/` (`fsaverage/*.gii`, MNI `volumes/*.nii.gz`) are **not** used by these commands; see the main [README](../../README.md) for supported formats.

---

## References

Friedrich, P., Forkel, S. J., & Thiebaut de Schotten, M. (2020). Mapping the principal gradient onto the corpus callosum. *NeuroImage*, *223*, 117317. [https://doi.org/10.1016/j.neuroimage.2020.117317](https://doi.org/10.1016/j.neuroimage.2020.117317) — [PMC7116113](https://pmc.ncbi.nlm.nih.gov/articles/PMC7116113/)

Margulies, D. S., Ghosh, S. S., Goulas, A., Falkiewicz, M., Huntenburg, J. M., Langs, G., … Smallwood, J. (2016). Situating the default-mode network along a principal gradient of macroscale cortical organization. *Proceedings of the National Academy of Sciences*, *113*(44), 12574–12579.
