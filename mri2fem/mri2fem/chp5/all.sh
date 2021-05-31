#!/bin/bash

cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd 

echo "FreeSurfer configuration is required to run this script" 
if [ ! -z "${FREESURFER_HOME}" ];
then
   echo "FreeSurfer found"  
else 
   echo "FreeSurfer not found" 
   exit 
fi

echo "Checking if path to mri2fem dataset is set" 
if  [ ! -z "${MRI2FEMDATA}" ];  
then
   echo "mri2fem dataset found"
else
   echo "mri2fem dataset not found"
   echo "Run setup in mri2fem-dataset folder" 
   echo "source Setup_mri2fem_dataset.sh" 
   exit
fi

# Chapter 5.1
#ls ${MRI2FEMDATA}/dicom/ernie/DTI
mri_convert ${MRI2FEMDATA}/dicom/ernie/DTI/IM_1496 dti.mgz


# If dir ernie-dti exists, then skip dt_recon.
if  [ ! -d "ernie-dti" ];  
then 
    # dt_recon will be skipped if FSL is not installed 
    # SUBJECTS_DIR is set following --sd
    echo "Ouput directory for dt_recon found, skipping dt_recon"
    dt_recon --i dti.mgz --b dti.bvals dti.voxel_space.bvecs --sd ${MRI2FEMDATA}/freesurfer --s ernie --o ernie-dti  
fi 

# Chapter 5.2.1
cp ${MRI2FEMDATA}/freesurfer/ernie/mri/orig.mgz .  
cp ${MRI2FEMDATA}/freesurfer/ernie/mri/wmparc.mgz .  
mri_info orig.mgz --orientation

# Chapter 5.2.2
# Checks if dt_recon ouput exists in current dir.
# Otherwise copy from the mri2fem dataset
if [ -d "ernie-dti" ]; 
then
   echo "Copying tensor.nii.gz from dt_recon ouput"
   cp ernie-dti/tensor.nii.gz .  
else 
   echo "Copying tensor.nii.gz from mri2fem dataset"
   cp ${MRI2FEMDATA}/freesurfer/ernie-dti/tensor.nii.gz . 
fi
 
mri_binarize --i wmparc.mgz --gm --dilate 2 --o mask.mgz
python3 check_dti.py --dti tensor.nii.gz --mask mask.mgz 
python3 clean_dti_data.py --dti tensor.nii.gz --mask mask.mgz --out clean-tensor.mgz
python3 check_dti.py --dti clean-tensor.mgz --mask mask.mgz 
python3 dti_data_to_mesh.py --mesh ../chp4/ernie-brain-32.h5 --dti clean-tensor.mgz --out ernie-brain-dti.h5
