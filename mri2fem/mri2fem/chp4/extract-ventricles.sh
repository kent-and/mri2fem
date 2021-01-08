#!/bin/bash

# Input and output filenames
input="wmparc.mgz"
output="ventricles.stl"

# Also match the 4th ventricle and aqueduct?
include_fourth_and_aqueduct=true
if [ "$include_fourth_and_aqueduct" == true ]; then
    matchval="15"
else
    matchval="1"
fi
num_smoothing=3

# Other parameters
postprocess=true
num_closing=2
V_min=100

if [ "$postprocess" = true ]; then
    mri_binarize --i $input --ventricles \
	         --o "tmp.mgz"
    
    mri_volcluster --in "tmp.mgz" \
	           --thmin 1 \
	           --minsize $V_min \
	           --ocn "tmp-ocn.mgz"
    
    mri_binarize --i "tmp-ocn.mgz" \
	         --match 1 \
	         --o "tmp.mgz"
    
    mri_morphology "tmp.mgz" \
	           close $num_closing "tmp.mgz"
    
    mri_binarize --i "tmp.mgz" \
	         --match 1 \
	         --surf-smooth $num_smoothing \
	         --surf $output
    
    rm tmp.mgz
    rm tmp-ocn.mgz
    exit
fi

mri_binarize --i $input --ventricles \
	     --match $matchval \
	     --surf-smooth $num_smoothing \
	     --surf $output
