import SVMTK as svmtk

def create_volume_mesh(stlfile, output, resolution=16):
    # Load input file
    surface = svmtk.Surface(stlfile)
    
    # Generate the volume mesh
    domain = svmtk.Domain(surface)
    domain.create_mesh(resolution)

    # Write the mesh to the output file
    domain.save(output)

# Create mesh    
create_volume_mesh("lh.pial.stl", "lh.mesh")

# Create mesh with resolution 64
create_volume_mesh("lh.pial.stl", "lh64.mesh", 64)

# Create mesh from the smoother surface
if False:
    create_volume_mesh("lh.pial.smooth.stl", "ernie.mesh")

