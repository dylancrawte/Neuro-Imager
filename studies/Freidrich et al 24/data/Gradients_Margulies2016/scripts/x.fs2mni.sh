#!/bin/bash


sub_id=MNI
input_prefix=hcp.embed.grad_1.fsa.func
output_prefix=hcp.embed.grad_1
output_dir=/Users/dmargulies/Dropbox/01_code/gradient_analysis/gradient_data/embedded/fsaverage

cp ${output_dir}/hcp.embed.grad_1.L.fsa.func.gii ${output_dir}/lh.hcp.embed.grad_1.fsa.func.gii
cp ${output_dir}/hcp.embed.grad_1.R.fsa.func.gii ${output_dir}/rh.hcp.embed.grad_1.fsa.func.gii

for hemi in lh rh
do
  input=${output_dir}/$hemi.${input_prefix}.gii
  output=$output_dir/$hemi.${output_prefix}.nii.gz
  template=$SUBJECTS_DIR/$sub_id/mri/norm.mgz

  #Project to subject's surface space
  cmd="mri_surf2surf --srcsubject fsaverage --srcsurfval ${input} --hemi ${hemi} --trgsubject ${sub_id} --trgsurfval ${output} --reshape --mapmethod nnf"
  echo $cmd
  eval $cmd

  #Project to subject's T1 space
  cmd="mri_surf2vol --surfval $output --hemi $hemi --subject $sub_id --identity $sub_id --fillribbon --o $output --template $template"
  echo $cmd
  eval $cmd
done


UTILITIES_DIR=utilities
DEFAULT_MASK=../bin/liberal_cortex_masks_FS4.5.0/FSL_MNI152_FS4.5.0_cortex_estimate.nii.gz

#Set up file names
input_lh=${output_dir}/lh.${output_prefix}.nii.gz
input_rh=${output_dir}/rh.${output_prefix}.nii.gz
output=${output_dir}/${output_prefix}.nii.gz
output_seg=$output_dir/seg.$output_prefix.nii.gz

#Grow the output volume and make seg file
matlab -nodesktop -nojvm -nosplash -r "addpath('$UTILITIES_DIR/','/Applications/freesurfer/matlab'); \
                                       [output_vol, output_seg_vol] = CBIG_RF_propagate_in_vol('$input_lh', '$input_rh', '$mask'); \
                                       MRIwrite(output_vol, '$output'); \
                                       MRIwrite(output_seg_vol, '$output_seg'); \
                                       exit"

i=0
flirt -in /Users/dmargulies/Dropbox/01_code/gradient_analysis/gradient_data/embedded/fsaverage/volume.${i}.nii.gz -applyxfm -init ./MNI152_brainto2mm_brain.mat -out /Users/dmargulies/Dropbox/01_code/gradient_analysis/gradient_data/embedded/fsaverage/volume.${i}.2mm.nii.gz -paddingsize 0.0 -interp nearestneighbour -ref /Applications/fsl/data/standard/MNI152_T1_2mm.nii.gz
fslstats ${output_dir}/volume.${i}.2mm.nii -R
fslmaths ${output_dir}/volume.${i}.2mm.nii -abs -bin ${output_dir}/mask.nii.gz
fslmaths ${output_dir}/mask.nii.gz -mul 5.425259 ${output_dir}/mask.nii.gz
fslmaths ${output_dir}/volume.${i}.2mm.nii -add ${output_dir}/mask.nii.gz ${output_dir}/volume.${i}.2mm.nii
for j in `seq 0 5 95`; do
    let k="${j} + 5"
    fslmaths ${output_dir}/volume.${i}.2mm.nii \
       -thr `fslstats ${output_dir}/volume.${i}.2mm.nii -P ${j}` \
       -uthr `fslstats ${output_dir}/volume.${i}.2mm.nii -P ${k}` \
       -bin ${output_dir}/volume_$(printf %02d $j)_$(printf %02d $k).nii
done
