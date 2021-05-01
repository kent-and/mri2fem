import argparse
from dolfin import * 

cpp_code = """
#include<pybind11/pybind11.h>
#include<dolfin/adaptivity/adapt.h>
#include<dolfin/mesh/Mesh.h>
#include<dolfin/mesh/MeshFunction.h>

namespace py = pybind11;

PYBIND11_MODULE(SIGNATURE, m) {
  m.def("adapt", (std::shared_ptr<dolfin::MeshFunction<std::size_t>> (*)(const dolfin::MeshFunction<std::size_t>&, std::shared_ptr<const dolfin::Mesh>)) &dolfin::adapt, py::arg("mesh_function"), py::arg("adapted_mesh"));
  m.def("adapt", (std::shared_ptr<dolfin::Mesh> (*)(const dolfin::Mesh&)) &dolfin::adapt );
  m.def("adapt", (std::shared_ptr<dolfin::Mesh> (*)(const dolfin::Mesh&,const dolfin::MeshFunction<bool>&)) &dolfin::adapt );
}
"""
adapt = compile_cpp_code(cpp_code).adapt

def refine_mesh_tags(in_hdf5, out_hdf5, tags=None):
    # Read the mesh from file. The mesh coordinates define 
    # the Surface RAS space.
    mesh = Mesh()
    hdf = HDF5File(mesh.mpi_comm(), in_hdf5, "r")
    hdf.read(mesh, "/mesh", False)  
    
    # Read subdomains and boundary markers
    d = mesh.topology().dim()
    subdomains = MeshFunction("size_t", mesh, d)
    hdf.read(subdomains, "/subdomains")
    boundaries = MeshFunction("size_t", mesh, d-1)
    hdf.read(boundaries, "/boundaries")
    hdf.close()

    # Initialize connections between all mesh entities, and 
    # use a refinement algorithm that remember parent facets
    mesh.init()
    parameters["refinement_algorithm"] = \
        "plaza_with_parent_facets"

    # Refine globally if no tags given
    if not tags: 
       # Refine all cells in the mesh 
       new_mesh = adapt(mesh)
       
       # Update the subdomain and boundary markers
       adapted_subdomains = adapt(subdomains, new_mesh) 
       adapted_boundaries = adapt(boundaries, new_mesh)      

    else:   
       # Create markers for local refinement
       markers = MeshFunction("bool", mesh, d, False)
       
       # Iterate over given tags, label all cells
       # with this subdomain tag for refinement:
       for tag in tags: 
           markers.array()[subdomains.array()==tag] = True

       # Refine mesh according to the markers
       new_mesh = adapt(mesh, markers)

       # Update subdomain and boundary markers
       adapted_subdomains = adapt(subdomains, new_mesh) 
       adapted_boundaries = adapt(boundaries, new_mesh)  

    print("Original mesh #cells: ", mesh.num_cells())  
    print("Refined mesh #cells: ", new_mesh.num_cells())  

    hdf = HDF5File(new_mesh.mpi_comm(), out_hdf5, "w")
    hdf.write(new_mesh, "/mesh")            
    hdf.write(adapted_subdomains, "/subdomains")
    hdf.write(adapted_boundaries, "/boundaries")
    hdf.close() 

if __name__ == "__main__":
    adapt = compile_cpp_code(cpp_code).adapt
    parser = argparse.ArgumentParser()
    parser.add_argument("--in_hdf5", type=str)      
    parser.add_argument("--out_hdf5", type=str) 
    parser.add_argument("--refine_tag",  type=int, nargs="+") 
    Z = parser.parse_args() 
    
    refine_mesh_tags(Z.in_hdf5, Z.out_hdf5, Z.refine_tag)

  

