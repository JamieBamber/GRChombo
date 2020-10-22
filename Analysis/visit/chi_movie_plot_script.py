# coding: utf-8

# python Visit script
# -------------------
from sys import exit
from os import makedirs

# import visit_utils, we will use it to help encode our movie
from visit_utils import *
DeleteAllPlots()

# start
print("starting visit run")

# file settings
data_root_dir = "/hppfs/work/pn34tu/di76bej/GRChombo_data/BinaryBHScalarField/"
run_number = 5
subdir = "run{:04d}_FlatScalar_mu1_G0".format(run_number)
data_file_name = "BinaryBHSFPlot_*.3d.hdf5 database"
width = 32

# open datafile(s)
OpenDatabase(data_root_dir + subdir + "/" + data_file_name, 0)

abs_max = 10

# add plot
AddPlot("Pseudocolor", "chi")
PseudocolorAtts = PseudocolorAttributes()
PseudocolorAtts.scaling = PseudocolorAtts.Linear  # Linear, Log, Skew
PseudocolorAtts.skewFactor = 1
PseudocolorAtts.limitsMode = PseudocolorAtts.OriginalData  # OriginalData, CurrentPlot
PseudocolorAtts.minFlag = 1
PseudocolorAtts.min = 0
PseudocolorAtts.maxFlag = 1
PseudocolorAtts.max = 1
PseudocolorAtts.centering = PseudocolorAtts.Natural  # Natural, Nodal, Zonal
PseudocolorAtts.colorTableName = "inferno"
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
DrawPlots()
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
View2DAtts.windowCoords = (256 - 0.5*width, 256+0.5*width, 256 - 0.5*width, 256+0.5*width)
View2DAtts.viewportCoords = (0.2, 0.95, 0.15, 0.95)
View2DAtts.fullFrameActivationMode = View2DAtts.Auto  # On, Off, Auto
View2DAtts.fullFrameAutoThreshold = 100
View2DAtts.xScale = View2DAtts.LINEAR  # LINEAR, LOG
View2DAtts.yScale = View2DAtts.LINEAR  # LINEAR, LOG
View2DAtts.windowValid = 1
SetView2D(View2DAtts)

# get the number of timesteps
nts = TimeSliderGetNStates()

# set basic save options
root_plot_path = "/dss/dsshome1/04/di76bej/GRChombo/GRChombo/Analysis/plots/Binary_BH/BBH_run{:04d}/".format(run_number)
frame_dir = "BBH_run{:04d}_chi_movie".format(run_number) 
try:
        makedirs(root_plot_path + frame_dir)
except:
        pass
# The 'family' option controls if visit automatically adds a frame number to 
# the rendered files. 
swatts = SaveWindowAttributes()
swatts.family = 0
swatts.width = 1024
swatts.height = 1024
# select PNG as the output file format
swatts.format = swatts.PNG
swatts.progressive = 1

# make movie frames
for ts in range(0, nts):
	# Change to the next timestep
	TimeSliderSetState(ts)
	swatts.fileName = root_plot_path + frame_dir + "/BBH_movie_%06d.png" % ts
	SetPlotOptions(PseudocolorAtts)
	SetSaveWindowAttributes(swatts)
	DrawPlots()
	# render the image to a PNG file
	SaveWindow()
	print("made frame %d of %d" % (ts, nts))

# make movie
"""root_movie_path = "/dss/dsshome1/04/di76bej/GRChombo/GRChombo/Analysis/movies/"
input_pattern = frame_dir + "/BBH_SF_chi_movie_%06d.png"
output_movie = root_movie_path + "BBH_SF_chi_" + subdir + "_movie.mpg"
encoding.encode(input_pattern,output_movie)
print("saved as " + output_movie)"""
exit()
