import numpy
import nibabel
from nibabel.affines import apply_affine
from dolfin import *

def map_parcellation_to_mesh(parcfile, meshfile):
    # Load image from the parcellation file,
    # extract its data and output its dimensions
    image  = nibabel.load(parcfile)
    data = image.get_fdata() 

    # Examine the dimensions of the image and
    # examine at a value
    print(data.shape)
    print(data[100, 100, 100])

    # Import brain mesh
    mesh = Mesh()
    with XDMFFile(meshfile) as file:
        file.read(mesh)
    print(mesh.num_cells())
    
    # Define mesh-based region representation 
    n = mesh.topology().dim()
    regions = MeshFunction("size_t", mesh, n, 0)
    print(regions[0])
    print(regions.array())
    
    # Find the transformation f from T1 voxel space
    # to RAS space and take its inverse to get the
    # map from RAS to voxel space
    vox2ras = image.header.get_vox2ras_tkr()
    ras2vox = numpy.linalg.inv(vox2ras)

    print("Iterating over all cells...")
    for cell in cells(mesh):
        c = cell.index()

        # Extract RAS coordinates of cell midpoint
        xyz = cell.midpoint()[:]

        # Convert to voxel space
        ijk = apply_affine(ras2vox, xyz)

        # Round off to nearest integers to find voxel indices
        i, j, k = numpy.rint(ijk).astype("int")  
        
        # Insert image data into the mesh function:
        regions.array()[c] = int(data[i, j, k])

    # Store regions in XDMF
    xdmf = XDMFFile(mesh.mpi_comm(),
                    "results/ernie-parcellation.xdmf")
    xdmf.write(regions)
    xdmf.close()

    # and/or store regions in HDF5 format
    hdf5 = HDF5File(mesh.mpi_comm(),
                    "results/h5-ernie-parcellation.h5", "w")
    hdf5.write(mesh, "/mesh")
    hdf5.write(regions, "/regions")
    hdf5.close()
    
map_parcellation_to_mesh("wmparc.mgz", "ernie-brain-32.xdmf")
