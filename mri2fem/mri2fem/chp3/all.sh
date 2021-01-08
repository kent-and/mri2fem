# Freesurfer recon-all first... Not included here for the sake of
# time, and space. Assume that we have run recon-all, and starting
# from the generated surface files here.

# Convert to STL, not that lh.pial.stl is generated
mris_convert lh.pial pial.stl

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
