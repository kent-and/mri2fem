import SVMTK as svmtk

def remesh_surface(stl_input, output, L, n,
                   do_not_move_boundary_edges=False):

    # Load input STL file
    surface = svmtk.Surface(stl_input)

    # Remesh surface
    surface.isotropic_remeshing(L, n,
                                do_not_move_boundary_edges)

    # Save remeshed STL surface 
    surface.save(output)                                      

remesh_surface("lh.pial.stl", "lh.pial.remesh.stl", 1.0, 3)
