#!/bin/bash



for c_orig in 0 1 2 3 4; do

c=$(( c_orig+1 ))

wb_command -cifti-separate ../ciftis/hcp.embed.${c_orig}.dscalar.nii COLUMN -metric CORTEX_LEFT ../ciftis/hcp.embed.grad_${c}.L.func.gii -metric CORTEX_RIGHT ../ciftis/hcp.embed.grad_${c}.R.func.gii

  for h in L R; do

    wb_command -metric-resample ../ciftis/hcp.embed.grad_${c}.${h}.func.gii standard_mesh_atlases/resample_fsaverage/fs_LR-deformed_to-fsaverage.${h}.sphere.32k_fs_LR.surf.gii standard_mesh_atlases/resample_fsaverage/fsaverage_std_sphere.${h}.164k_fsavg_${h}.surf.gii ADAP_BARY_AREA hcp.embed.grad_${c}.${h}.fsa.func.gii -area-metrics standard_mesh_atlases/resample_fsaverage/fs_LR.${h}.midthickness_va_avg.32k_fs_LR.shape.gii standard_mesh_atlases/resample_fsaverage/fsaverage.${h}.midthickness_va_avg.164k_fsavg_${h}.shape.gii

    wb_command -metric-resample ../ciftis/hcp.embed.grad_${c}.${h}.func.gii standard_mesh_atlases/resample_fsaverage/fs_LR-deformed_to-fsaverage.${h}.sphere.32k_fs_LR.surf.gii standard_mesh_atlases/resample_fsaverage/fsaverage6_std_sphere.${h}.41k_fsavg_${h}.surf.gii ADAP_BARY_AREA hcp.embed.grad_${c}.${h}.fsa6.func.gii -area-metrics standard_mesh_atlases/resample_fsaverage/fs_LR.${h}.midthickness_va_avg.32k_fs_LR.shape.gii standard_mesh_atlases/resample_fsaverage/fsaverage6.${h}.midthickness_va_avg.41k_fsavg_${h}.shape.gii

    wb_command -metric-resample ../ciftis/hcp.embed.grad_${c}.${h}.func.gii standard_mesh_atlases/resample_fsaverage/fs_LR-deformed_to-fsaverage.${h}.sphere.32k_fs_LR.surf.gii standard_mesh_atlases/resample_fsaverage/fsaverage5_std_sphere.${h}.10k_fsavg_${h}.surf.gii ADAP_BARY_AREA hcp.embed.grad_${c}.${h}.fsa5.func.gii -area-metrics standard_mesh_atlases/resample_fsaverage/fs_LR.${h}.midthickness_va_avg.32k_fs_LR.shape.gii standard_mesh_atlases/resample_fsaverage/fsaverage5.${h}.midthickness_va_avg.10k_fsavg_${h}.shape.gii

    wb_command -metric-resample ../ciftis/hcp.embed.grad_${c}.${h}.func.gii standard_mesh_atlases/resample_fsaverage/fs_LR-deformed_to-fsaverage.${h}.sphere.32k_fs_LR.surf.gii standard_mesh_atlases/resample_fsaverage/fsaverage4_std_sphere.${h}.3k_fsavg_${h}.surf.gii ADAP_BARY_AREA hcp.embed.grad_${c}.${h}.fsa4.func.gii -area-metrics standard_mesh_atlases/resample_fsaverage/fs_LR.${h}.midthickness_va_avg.32k_fs_LR.shape.gii standard_mesh_atlases/resample_fsaverage/fsaverage4.${h}.midthickness_va_avg.3k_fsavg_${h}.shape.gii

  done

done
