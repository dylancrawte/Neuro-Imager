from neuro_imaging_tool.viewer import BrainViewerWrapper, ViewerConfig

cfg = ViewerConfig(surface="pial", volumetric_structures="subcortex", offscreen=False)
viewer = BrainViewerWrapper(cfg)
viewer.load_template_brain()
viewer.add_bundled_dscalar()
viewer.show()
