# coding: utf-8

from sys import exit

# python Visit script
# -------------------

# start
print("starting visit run")

# file settings
data_root_dir = "/hppfs/work/pn34tu/di76bej/GRChombo_data/BinaryBHScalarField/"
run_number = 2
subdir = "run{:04d}_FlatScalar_mu0.4_G0".format(run_number)
number = 300
data_file_name = "BinaryBHSFPlot_%06d.3d.hdf5" % number

# open datafile(s)
OpenDatabase(data_root_dir + "failures/" + subdir + "/" + data_file_name,0)

abs_max = 20

# add plot
AddPlot("Pseudocolor", "phi", 1, 1)
PseudocolorAtts = PseudocolorAttributes()
PseudocolorAtts.scaling = PseudocolorAtts.Linear  # Linear, Log, Skew
PseudocolorAtts.skewFactor = 1
PseudocolorAtts.limitsMode = PseudocolorAtts.OriginalData  # OriginalData, CurrentPlot
PseudocolorAtts.minFlag = 1
PseudocolorAtts.min = -abs_max
PseudocolorAtts.maxFlag = 1
PseudocolorAtts.max = abs_max
PseudocolorAtts.centering = PseudocolorAtts.Natural  # Natural, Nodal, Zonal
PseudocolorAtts.colorTableName = "PuOr" # inferno 
PseudocolorAtts.invertColorTable = 1
PseudocolorAtts.opacityType = PseudocolorAtts.FullyOpaque  # ColorTable, FullyOpaque, Constant, Ramp, VariableRange
PseudocolorAtts.opacity = 1
PseudocolorAtts.pointSize = 0.05
PseudocolorAtts.pointType = PseudocolorAtts.Point  # Box, Axis, Icosahedron, Octahedron, Tetrahedron, SphereGeometry, Point, Sphere
PseudocolorAtts.pointSizeVarEnabled = 0
PseudocolorAtts.pointSizeVar = "default"
PseudocolorAtts.pointSizePixels = 2
PseudocolorAtts.lineStyle = PseudocolorAtts.SOLID  # SOLID, DASH, DOT, DOTDASH
PseudocolorAtts.lineType = PseudocolorAtts.Line  # Line, Tube, Ribbon
PseudocolorAtts.lineWidth = 0
SetPlotOptions(PseudocolorAtts)

# add operator 
AddOperator("Slice", 1)
SliceAtts = SliceAttributes()
SliceAtts.originType = SliceAtts.Intercept  # Point, Intercept, Percent, Zone, Node
SliceAtts.originPoint = (0, 0, 0)
SliceAtts.originIntercept = 0.001
SliceAtts.originPercent = 0
SliceAtts.originZone = 0
SliceAtts.originNode = 0
SliceAtts.normal = (0, 0, 1)
SliceAtts.axisType = SliceAtts.ZAxis  # XAxis, YAxis, ZAxis, Arbitrary, ThetaPhi
SliceAtts.upAxis = (0, 1, 0)
SliceAtts.project2d = 1
SliceAtts.flip = 0
SliceAtts.originZoneDomain = 0
SliceAtts.originNodeDomain = 0
SliceAtts.meshName = "Mesh"
SliceAtts.theta = 0
SliceAtts.phi = 90
SetOperatorOptions(SliceAtts, 1)

# include all levels
silr = SILRestriction()
silr.TurnOnAll()
SetPlotSILRestriction(silr ,1)
DrawPlots()

# Set viewing attributes
View2DAtts = View2DAttributes()
width=64
View2DAtts.windowCoords = (256-0.5*width, 256+0.5*width, 
256-0.5*width,256+0.5*width)
View2DAtts.viewportCoords = (0.2, 0.95, 0.15, 0.95)
View2DAtts.fullFrameActivationMode = View2DAtts.Auto  # On, Off, Auto
View2DAtts.fullFrameAutoThreshold = 100
View2DAtts.xScale = View2DAtts.LINEAR  # LINEAR, LOG
View2DAtts.yScale = View2DAtts.LINEAR  # LINEAR, LOG
View2DAtts.windowValid = 1
SetView2D(View2DAtts)

# save plot as png
root_plot_path = "/dss/dsshome1/04/di76bej/GRChombo/GRChombo/Analysis/plots/"
filename = "BBH_SF_phi_failure" + subdir + "_n%06d" % number
s = SaveWindowAttributes()
s.family=0
s.format = s.PNG
s.progressive = 1
s.fileName = root_plot_path + filename
SetSaveWindowAttributes(s)
name = SaveWindow()
print("name = %s" % name)
print("saved as " + root_plot_path + filename)
exit()
