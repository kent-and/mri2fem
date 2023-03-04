#------------------------------------------------------------------------------
# This script was adapted from Jorgen Dokken's FEniCS forum thread regarding 
# the conversion of GMSH files to FEniCS' XDMF format using meshio.  Recent 
# versions of meshio convert produce XDMF meshes whose file format is not 
# compatible with FEniCS.  This issue may be addressed with the release of the 
# next generation of the FEniCS library (FEniCSX), which is still under 
# development.  Until then, this script works around the issue.  The original 
# thread can be found at the following URL
#
# https://fenicsproject.discourse.group/t/transitioning-from-mesh-xml-to-mesh-xdmf-from-dolfin-convert-to-meshio/412/76
#
#-----------------------------------------------------------------------------
import meshio
import sys

# medit files are the default file types made by the SVMTk 
def convert(meshFile, fileFormatAccess="medit:ref"):
    msh = meshio.read(meshFile)
    
    for cell in msh.cells:
        if cell.type == "triangle":
            triangle_cells = cell.data
        elif  cell.type == "tetra":
            tetra_cells = cell.data
    
    for key in msh.cell_data_dict[fileFormatAccess].keys():
        if key == "triangle":
            triangle_data = msh.cell_data_dict[fileFormatAccess][key]
        elif key == "tetra":
            tetra_data = msh.cell_data_dict[fileFormatAccess][key]
    tetra_mesh = meshio.Mesh(points=msh.points, cells={"tetra": tetra_cells})
    triangle_mesh =meshio.Mesh(points=msh.points,
                               cells=[("triangle", triangle_cells)],
                               cell_data={"name_to_read":[triangle_data]})
    
    # separate the name from the extension
    p = meshFile.rfind('.')

    print("")
    print(f"Writing FEniCS compatible mesh files: {meshFile[:p]}.xdmf and {meshFile[:p]}.h5")
    print("You will need both of these files to be present when calling XDMFFile(...) in FEniCS")
    print("---> Saving *triangular* mesh conversion (for tetrahedral meshes, use SVMTk-tet-mesh-to-FEniCS-XDMF.py)")
    meshio.write(f"{meshFile[:p]}.xdmf", triangle_mesh)

if __name__ == "__main__":
    if(len(sys.argv) < 2):
        print("")
        print("Convert a mesh to a FEniCS-compatible XDMF format")
        print("-------------------------------------------------")
        print("Usage  : python3 scriptname meshfilename.extension")
        print("Example (SVMTk meshes): python3 scriptname myfile.mesh") 
        print("Example (GMSH meshes) : python3 scriptname myfile.msh")
        print("")
        sys.exit()
    else:
        print("----------------------------------------------------")
        print("A simple utility to convert SVMTk mesh (medit) files")
        print("to a compatible (legacy) FEniCS XDMF file format.   ")
        print("----------------------------------------------------")
        print("")

    filen = sys.argv[1]
    p = filen.rfind('.')
    supported = {"mesh": "medit:ref", "msh":"gmsh:physical"};
    if p != -1:
        ext = filen[p+1:]
        if ext in supported:
            print(f"Converting {filen} to FEniCS XDMF format")
            print("")
            convert(filen,fileFormatAccess=supported[ext])
        else:
            print(f"The file extension {filen[p:]} is not supported")
            supp = "Supported file extensions are: "
            for key in supported:
                supp += "." + key + " "
            print(supp)
            print("")
    else:
        print("The first argument must be the name of the file that you wish to convert")
        print("Example: python3 SVMTk-tri-mesh-to-FEniCS-XDMF.py myfile.mesh")
