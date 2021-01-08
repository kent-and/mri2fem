# cp freesurfer/ernie/surf/lh.pial .
# cp freesurfer/ernie/surf/lh.white .

# Convert surfaces to STL
mris_convert lh.pial pial.stl
mris_convert lh.white white.stl

# Use scripts from chp3 to remesh and smoothen.
# Rename stl files lh.pial.stl and lh.white.stl again

# Generate gray-white mesh
python3 two-domain-tagged.py

# Convert to paraview friendly format
meshio-convert ernie-gw.mesh ernie-gw.vtu
 
# ./extract-ventricles.sh

## Set postprocess=true and run again:
 ./extract-ventricles.sh

# cp freesurfer/ernie/surf/rh.pial .
# cp freesurfer/ernie/surf/rh.white .
  
# Convert surfaces to STL
mris_convert rh.pial pial.stl
mris_convert rh.white white.stl

# Use scripts from chp3 to remesh and smoothen.
# Rename stl files rh.pial.stl and rh.white.stl again

python3 fullbrain-five-domain.py

meshio-convert ernie-brain-32.mesh ernie-brain-32.xml
meshio-convert ernie-brain-32.xml ernie-brain-32.xdmf

# Chapter 4.4.1
python3 map_parcellation.py

# Chapter 4.4.2
#python3 convert_to_dolfin_mesh.py --meshfile ernie-gw.mesh --hdf5file ernie-gw.h5
python3 convert_to_dolfin_mesh.py --meshfile ernie-brain-32.mesh --hdf5file ernie-brain-32.h5

#python3 add_parcellations.py --in_hdf5 ernie-gw.h5 --in_parc wmparc.mgz --out_hdf5 results/ernie-gw-subdomains.h5
python3 add_parcellations.py --in_hdf5 ernie-brain-32.h5 --in_parc wmparc.mgz --out_hdf5 results/ernie-brain-subdomains.h5

python3 add_parcellations.py --in_hdf5 ernie-brain-32.h5 --in_parc wmparc.mgz --out_hdf5 results/ernie-brain-subdomains-tags.h5 --add 17 1028 1035 3028 3035

# Chapter 4.5
python3 refine_mesh_tags.py --in_hdf5 ernie-brain-32.h5 --out_hdf5 ernie-brain-32-refined.h5
refine_mesh_tags.py --in_hdf5 ernie-brain-32.h5 --out_hdf5 ernie-brain-32-refine-tags.h5 --add 2
