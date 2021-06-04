#!/bin/bash

cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd 

echo "This requires that the scripts in chp4 and chp5 are complete" 
if [ -f ../chp4/lh.pial.stl -a -f ../chp4/rh.pial.stl -a  -f ../chp4/lh.white.stl -a  -f ../chp4/rh.white.stl -a -f ../chp4/lh.ventricles.stl ]; 
then
    echo "Required chp4 files found"
    
    # Making folder to store sufaces from chp4     
    mkdir -p surfaces
    
    # Copying surfaces files from chp4 
    cp ../chp4/lh.pial.stl ../chp4/rh.pial.stl ../chp4/lh.white.stl ../chp4/rh.white.stl  ../chp4/lh.ventricles.stl surfaces
else 
    echo "Required chp4 files not found"
    exit
fi

if [ -f ../chp5/clean-tensor.mgz ]; 
then
    echo "Required chp5 files found"
else 
    echo "Required chp5 files not found"
    exit
fi

# make 16, 32, 64, 128 mesh. Note that 128 mesh uses significant amount of RAM.
python3 create_mesh_refinements.py

# 16 mesh 
# convert to h5
mkdir -p tmp
python3 ../chp4/convert_to_dolfin_mesh.py --meshfile brain_16.mesh --hdf5file brain_16.h5
# mark subdomains  
python3 ../chp4/add_parcellations.py --in_hdf5 brain_16.h5 --in_parc ../chp4/wmparc.mgz --out_hdf5 brain_16_tags.h5 --add 17 1028 1035 3028 3035
# add dti to the h5 file 
python3 ../chp5/dti_data_to_mesh.py  --dti ../chp5/clean-tensor.mgz --mesh brain_16_tags.h5 --label 1 0.4 0.6 --out DTI_16.h5 
# run simulation 
python3 chp6-diffusion-mritracer.py --mesh DTI_16.h5 --lumped lumped --label uniform16lumped 
python3 chp6-diffusion-mritracer.py --mesh DTI_16.h5 --lumped not --label uniform16notlumped 

# same procedure for 32 
python3 ../chp4/convert_to_dolfin_mesh.py --meshfile brain_32.mesh --hdf5file brain_32.h5
python3 ../chp4/add_parcellations.py --in_hdf5 brain_32.h5 --in_parc ../chp4/wmparc.mgz --out_hdf5 brain_32_tags.h5 --add 17 1028 1035 3028 3035
python3 ../chp5/dti_data_to_mesh.py  --dti ../chp5/clean-tensor.mgz --mesh brain_32_tags.h5 --label 1 0.4 0.6  --out DTI_32.h5 
python3 chp6-diffusion-mritracer.py --mesh DTI_32.h5 --lumped lumped --label uniform32lumped 
python3 chp6-diffusion-mritracer.py --mesh DTI_32.h5 --lumped not --label uniform32notlumped 

# same procedure for 64 
python3 ../chp4/convert_to_dolfin_mesh.py --meshfile brain_64.mesh --hdf5file brain_64.h5
python3 ../chp4/add_parcellations.py --in_hdf5 brain_64.h5 --in_parc ../chp4/wmparc.mgz --out_hdf5 brain_64_tags.h5 --add 17 1028 1035 3028 3035
python3 ../chp5/dti_data_to_mesh.py  --dti ../chp5/clean-tensor.mgz  --mesh brain_64_tags.h5 --label 1 0.4 0.6  --out DTI_64.h5 
python3 chp6-diffusion-mritracer.py --mesh DTI_64.h5 --lumped lumped --label uniform64lumped 
python3 chp6-diffusion-mritracer.py --mesh DTI_64.h5 --lumped not --label uniform64notlumped 

# same procedure for 128  
python3 ../chp4/convert_to_dolfin_mesh.py --meshfile brain_128.mesh --hdf5file brain_128.h5
python3 ../chp4/add_parcellations.py --in_hdf5 brain_128.h5 --in_parc ../chp4/wmparc.mgz --out_hdf5 brain_128_tags.h5 --add 17 1028 1035 3028 3035
python3 ../chp5/dti_data_to_mesh.py  --dti ../chp5/clean-tensor.mgz --mesh brain_128_tags.h5 --label 1 0.4 0.6  --out DTI_128.h5 
python3 chp6-diffusion-mritracer.py --mesh DTI_128.h5 --lumped lumped --label uniform128lumped 
python3 chp6-diffusion-mritracer.py --mesh DTI_128.h5 --lumped not --label uniform128notlumped 

python chp6-tracer-plot-regions.py
python chp6-tracer-plot-lump.py

# ----------------------------------------------------------------------------------------
# make meshes with local refinement around hippocampus 
cp brain_16.mesh Mesh_16.mesh 
python3 ../chp4/convert_to_dolfin_mesh.py --meshfile Mesh_16.mesh --hdf5file Mesh_16.h5
python3 ../chp4/add_parcellations.py --in_hdf5 Mesh_16.h5 --in_parc ../chp4/wmparc.mgz --out_hdf5 Mesh_16_tags.h5 --add 17 
python3 ../chp4/refine_mesh_tags.py  --in_hdf5 Mesh_16_tags.h5 --out_hdf5 Mesh_16_ref1.h5 --refine_tag 17      
python3 ../chp5/dti_data_to_mesh.py  --dti ../chp5/clean-tensor.mgz --mesh Mesh_16_ref1.h5 --label 1 0.4 0.6  --out DTI_16_ref1.h5 

# refine 2 times  
python3 ../chp4/refine_mesh_tags.py  --in_hdf5 Mesh_16_ref1.h5 --out_hdf5 Mesh_16_ref2.h5 --refine_tag 17      
python3 ../chp5/dti_data_to_mesh.py  --dti ../chp5/clean-tensor.mgz --mesh Mesh_16_ref2.h5 --label 1 0.4 0.6  --out DTI_16_ref2.h5 

# refine 3 times  
python3 ../chp4/refine_mesh_tags.py  --in_hdf5 Mesh_16_ref2.h5 --out_hdf5 Mesh_16_ref3.h5 --refine_tag 17      
python3 ../chp5/dti_data_to_mesh.py  --dti ../chp5/clean-tensor.mgz --mesh Mesh_16_ref3.h5 --label 1 0.4 0.6  --out DTI_16_ref3.h5 

# refine 4 times  
python3 ../chp4/refine_mesh_tags.py  --in_hdf5 Mesh_16_ref3.h5 --out_hdf5 Mesh_16_ref4.h5 --refine_tag 17      
python3 ../chp5/dti_data_to_mesh.py --dti ../chp5/clean-tensor.mgz --mesh Mesh_16_ref4.h5 --label 1 0.4 0.6  --out DTI_16_ref4.h5 

# run simulations  with locally refined regions around hippocampus 
python3 chp6-diffusion-mritracer-ref.py --mesh DTI_16_ref1.h5 --lumped lumped --label=DTI16lumped_ref1 
python3 chp6-diffusion-mritracer-ref.py --mesh DTI_16_ref2.h5 --lumped lumped --label=DTI16lumped_ref2  
python3 chp6-diffusion-mritracer-ref.py --mesh DTI_16_ref3.h5 --lumped lumped --label=DTI16lumped_ref3 
python3 chp6-diffusion-mritracer-ref.py --mesh DTI_16_ref4.h5 --lumped lumped --label=DTI16lumped_ref4 

python3 chp6-diffusion-mritracer-ref.py --mesh DTI_16_ref1.h5 --lumped not --label=DTI16notlumped_ref1 
python3 chp6-diffusion-mritracer-ref.py --mesh DTI_16_ref2.h5 --lumped not --label=DTI16notlumped_ref2 
python3 chp6-diffusion-mritracer-ref.py --mesh DTI_16_ref3.h5 --lumped not --label=DTI16notlumped_ref3 
python3 chp6-diffusion-mritracer-ref.py --mesh DTI_16_ref4.h5 --lumped not --label=DTI16notlumped_ref4 

python3 chp6-tracer-plot-ref.py




