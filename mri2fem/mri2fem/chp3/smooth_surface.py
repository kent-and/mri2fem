import SVMTK as svmtk

def smoothen_surface(stl_input, output,
                     n=1, eps=1.0, preserve_volume=True):
    # Load input STL file
    surface = svmtk.Surface(stl_input)

    # Smooth using Taubin smoothing
    # if volume should be preserved,
    # otherwise use Laplacian smoothing
    if preserve_volume:
        surface.smooth_taubin(n)
    else:
        surface.smooth_laplacian(eps, n)
        
    # Save smoothened STL surface
    surface.save(output)

smoothen_surface("lh.pial.remesh.stl", "lh.pial.smooth.stl",
                 n=10, eps=1.0)

# Try smoothing without not preserving volume
if False:
    smoothen_surface("lh.pial.remesh.stl", "lh.pial.laplacian.stl",
                     n=10, eps=1.0, preserve_volume=False)
