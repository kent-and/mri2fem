import SVMTK as svmtk

# Import the STL surface
lpial = svmtk.Surface("lh.pial.smooth.stl") 

# Find and fill holes 
lpial.fill_holes()

# Separate narrow gaps
# Default argument is -0.33. 
lpial.separate_narrow_gaps(-0.25)
