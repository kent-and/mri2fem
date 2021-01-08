import argparse
import numpy
import nibabel
from nibabel.affines import apply_affine
from dolfin import * 

def adjacent_tag(data, i, j, k, Mmin=3, Mmax=10):
    # Given an image voxel index (i, j, k), examine the
    # image data in the voxel neighborhood, and identify
    # the most common non-zero value among these. Start at
    # a neighborhood of radius Mmin, and increase if needed.
    for m in range(Mmin, Mmax):

        # Extract the data values from the neighborhood 
        values = data[i-m:i+m+1, j-m:j+m+1, k-m:k+m+1]

        # Reshape values from (2m+1, 2m+1, 2m+1) to list:
        v = values.reshape(1, -1)

        # Identify unique non-zero (positive) values and
        # the number of each 
        pairs, counts = numpy.unique(v[v > 0],
                                     return_counts=True)  

        # Return the most common non-zero tag:
        success = counts.size > 0
        if success:
           return pairs[counts.argmax()]    

    return 0

def add_parcellations(hdf5file, parcfile, out_hdf5,
                      specific_tags=None):
    # If specific_tags is None, include all parcellations found
    
    # Read the mesh and mesh data from .h5:
    mesh = Mesh()
    hdf = HDF5File(mesh.mpi_comm(), hdf5file, "r")
    hdf.read(mesh, "/mesh", False)  

    d = mesh.topology().dim()
    subdomains = MeshFunction("size_t", mesh, d)
    hdf.read(subdomains, "/subdomains")
    boundaries = MeshFunction("size_t", mesh, d-1)
    hdf.read(boundaries, "/boundaries")
    hdf.close()
    
    # Load parcellation image and data 
    image = nibabel.load(parcfile)
    data = image.get_fdata() 
    
    # Find the transformation to T1 voxel space from 
    # surface RAS (aka mesh) coordinates 
    vox2ras = image.header.get_vox2ras_tkr()
    ras2vox = numpy.linalg.inv(vox2ras)

    # Extract RAS coordinates of cell midpoints
    xyz = numpy.array([cell.midpoint()[:]
                       for cell in cells(mesh)])
    
    ## This version is equivalent, and faster, more extendable to other
    ## spaces, but requires more background knowledge.
    #DG0 = FunctionSpace(mesh, "DG", 0)
    #imap = DG0.dofmap().index_map()
    #num_dofs_local =  imap.local_range()[1]-imap.local_range()[0]
    #xyz = DG0.tabulate_dof_coordinates().reshape((num_dofs_local,-1))
    
    # Convert to voxel space and voxel indices: for cell c,
    # i[c], j[c], k[c] give the corresponding voxel indices.
    abc = apply_affine(ras2vox, xyz).T  
    ijk = numpy.rint(abc).astype("int")  
    (i, j, k) = ijk
    
    # Create a map from voxel index to subdomain tag
    # Note use of NumPy's "fancy" indexing:
    vox2sub = numpy.zeros(data.shape) 
    vox2sub[i, j, k] = subdomains.array() 
    
    # Create new array for the parcellation tags:
    N = mesh.num_cells()
    regions = numpy.zeros(N)

    # Extract unique mesh subdomain tags,
    # and iterate over these:
    subdomain_tags = numpy.unique(subdomains.array())
    for tag in subdomain_tags:
        # Zero out voxel data not associated with the current
        # subdomain 
        masked_data = (vox2sub == tag)*data
        
        # Iterate of all cells in this subdomain 
        for c in range(N):         
            if (subdomains[c] == tag):
                # Find and set the most common (non-zero)
                # adjacent parcellation tag
                regions[c] = adjacent_tag(masked_data,
                                          i[c], j[c], k[c])

    # Update the subdomains array with the parcellation tags 
    if not specific_tags:
        subdomains.array()[:] = regions
    else:
        for tag in specific_tags: 
            subdomains.array()[regions == tag] = tag     
           
    # Now store everything to a new file
    hdf = HDF5File(mesh.mpi_comm(), out_hdf5, "w")
    hdf.write(mesh, "/mesh")            
    hdf.write(subdomains, "/subdomains")
    hdf.write(boundaries, "/boundaries")
    hdf.close() 

    # Store subdomains in XDMF for easy visualization
    xdmfname = ".".join(Z.out_hdf5.split(".")[0:-1]) + "-tmp.xdmf"
    xdmf = XDMFFile(mesh.mpi_comm(), xdmfname)
    xdmf.write(subdomains)
    xdmf.close()

if __name__ =='__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--in_parc', type=str) 
    parser.add_argument('--in_hdf5', type=str)      
    parser.add_argument('--out_hdf5', type=str) 
    parser.add_argument('--add', type=int, nargs='+') 

    Z = parser.parse_args() 
    add_parcellations(Z.in_hdf5, Z.in_parc, Z.out_hdf5, Z.add)
