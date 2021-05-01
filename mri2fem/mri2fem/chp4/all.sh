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


# Convert left hemisphere (lh) surfaces to STL
mris_convert ${MRI2FEMDATA}/freesurfer/ernie/surf/lh.pial ./lh.pial.stl
mris_convert ${MRI2FEMDATA}/freesurfer/ernie/surf/lh.white ./lh.white.stl

# Use scripts from chp3 to remesh and smoothen.
# Rename stl files lh.pial.stl and lh.white.stl again

# Generate gray-white mesh
python3 two-domain-tagged.py

# Convert to paraview friendly format
meshio-convert ernie-gw.mesh ernie-gw.vtu
 
# ./extract-ventricles.sh

## Set postprocess=true and run again:
cp ${MRI2FEMDATA}/freesurfer/ernie/mri/wmparc.mgz .
./extract-ventricles.sh


# cp freesurfer/ernie/surf/rh.pial .
# cp freesurfer/ernie/surf/rh.white .
  
# Convert left hemisphere (rh) surfaces to STL
mris_convert ${MRI2FEMDATA}/freesurfer/ernie/surf/rh.pial ./rh.pial.stl
mris_convert ${MRI2FEMDATA}/freesurfer/ernie/surf/rh.white ./rh.white.stl

# Use scripts from chp3 to remesh and smoothen.
# Rename stl files rh.pial.stl and rh.white.stl again
python3 fullbrain-five-domain.py

meshio-convert ernie-brain-32.mesh ernie-brain-32.xml
meshio-convert ernie-brain-32.xml ernie-brain-32.xdmf

# Chapter 4.4.1
python3 map_parcellation.py


# Chapter 4.4.2
#python3 convert_to_dolfin_mesh.py --meshfile ernie-gw.mesh --hdf5file ernie-gw.h5
echo "Creating a tmp directory"  
mkdir -p tmp
echo "Converting to dolfin mesh" 
python3 convert_to_dolfin_mesh.py --meshfile ernie-brain-32.mesh --hdf5file ernie-brain-32.h5


#echo "Adding cell tags from wmparc.mgz to mesh" 
#python3 add_parcellations.py --in_hdf5 ernie-gw.h5 --in_parc wmparc.mgz --out_hdf5 results/ernie-gw-subdomains.h5
#python3 add_parcellations.py --in_hdf5 ernie-brain-32.h5 --in_parc wmparc.mgz --out_hdf5 results/ernie-brain-subdomains.h5

echo "Adding cell tags from wmparc.mgz to mesh" 
python3 add_parcellations.py --in_hdf5 ernie-brain-32.h5 --in_parc wmparc.mgz --out_hdf5 results/ernie-brain-subdomains-tags.h5 --add 17 1028 1035 3028 3035

# Chapter 4.5
echo "Refining mesh cells with specified tags" 
#python3 refine_mesh_tags.py --in_hdf5 ernie-brain-32.h5 --out_hdf5 ernie-brain-32-refined.h5
python3 refine_mesh_tags.py --in_hdf5 ernie-brain-32.h5 --out_hdf5 ernie-brain-32-refine-tags.h5 --refine_tag 17 # 1028 1035 3028 3035 






