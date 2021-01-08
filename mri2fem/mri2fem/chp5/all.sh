# Chapter 5.1
cd dicom/DTI
mri convert IM 0001 dti.mgz

# Set SUBJECTS_DIR before launching this command:
dt_recon --i dti.mgz --b dti.bvals dti.voxel_space.bvecs --s ernie --o $SUBJECTS_DIR/ernie/dti

# Chapter 5.2.1
cd $SUBJECTS_DIR/ernie/mri
mri_info orig.mgz --orientation

# Chapter 5.2.2
mri_binarize --i wmparc.mgz --gm --dilate 2 --o mask.mgz
python3 check_dti.py --dti tensor.nii.gz --mask mask.mgz 
python3 clean_dti_data.py --dti tensor.nii.gz --mask mask.mgz --out dti-clean.mgz
