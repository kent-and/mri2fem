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

# Freesurfer recon-all first... Not included here for the sake of
# time, and space. Assume that we have run recon-all, and starting
# from the generated surface files here.

# Convert to STL, not that lh.pial.stl is generated
mris_convert ${MRI2FEMDATA}/freesurfer/ernie/surf/lh.pial ./lh.pial.stl

# Generate volume meshes
python3 surface_to_mesh.py

# Convert to lh.xdmf, lh.h5 generated as well.
meshio-convert lh.mesh lh.xdmf

# Run remeshing
python3 remesh_surface.py

# Run smoothing
python3 smooth_surface.py

# Try repairing
python3 svmtk_repair_utilities.py 

# Additional
# Set if False -> if True to generate ernie.mesh here:
python3 surface_to_mesh.py
meshio-convert ernie.mesh ernie.xml
meshio-convert ernie.xml ernie.xdmf

# fenicsproject run
python3 diffusion.py
