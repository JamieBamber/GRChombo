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

# class to store the run information
class data_dir:
        def __init__(self, num, mu, delay, G, ratio):
                self.num = num
                self.mu = float(mu)
		self.delay = delay
                self.G = G
		self.ratio = ratio
                self.name = "run{:04d}_mu{:s}_delay{:d}_G{:s}_ratio{:d}".format(num, mu, delay, G, ratio)
#
data_dirs = []
def add_data_dir(num, mu, delay, G, ratio):
        x = data_dir(num, mu, delay, G, ratio)
        data_dirs.append(x)

#
#add_data_dir(11, "1", 0, "0", 1)
#add_data_dir(12, "1", 10000, "0", 1)
#add_data_dir(13, "0.08187607564", 0, "0", 1)
#add_data_dir(14, "1", 0, "0", 2)
#add_data_dir(15, "1", 10000, "0", 2)
#add_data_dir(16, "0.5", 0, "0", 1)
#add_data_dir(17, "0.5", 10000, "0", 1)
#add_data_dir(18, "0.5", 0, "0.000001", 1)
#add_data_dir(19, "1", 1, "0", 1) # resume from stationary BH distribution                                                                            #add_data_#add_data_dir(20, "0.5", 0, "0", 1) # resume from stationary BH distribution                     
add_data_dir(21, "0.5", 0, "0.01", 1)

# file settings
data_root_dir = "/p/project/pra116/bamber1/BinaryBHScalarField/"
root_plot_path = "/p/scratch/pra116/bamber1/plots/GR_Binary_BH/"

data_file_name = "BinaryBHSFPlot_*.3d.hdf5 database"

def make_rho_movie(dd):
	width=64
	start_frame = 87
	
	# open datafile(s)
	OpenDatabase(data_root_dir + dd.name + "/" + data_file_name, 0)
	print( "loaded database " + data_root_dir + dd.name + "/" + data_file_name)

	# normalise
	# rho0 = 0.5*(0.4**2)*(0.1**2)
	DefineScalarExpression("norm_rho","rho/{:.6f}".format(0.5*(dd.mu**2)))
	
	# add plot
	AddPlot("Pseudocolor", "norm_rho")
	AddOperator("Slice", 1)
	DrawPlots()
	PseudocolorAtts = PseudocolorAttributes()
	PseudocolorAtts.scaling = PseudocolorAtts.Log  # Linear, Log, Skew
	PseudocolorAtts.skewFactor = 1
	PseudocolorAtts.limitsMode = PseudocolorAtts.CurrentPlot  # OriginalData, CurrentPlot
	PseudocolorAtts.minFlag = 1
	PseudocolorAtts.min = 0.1
	PseudocolorAtts.maxFlag = 1
	PseudocolorAtts.max = 10000
	PseudocolorAtts.centering = PseudocolorAtts.Natural  # Natural, Nodal, Zonal
	PseudocolorAtts.colorTableName = "inferno"
	PseudocolorAtts.invertColorTable = 0
	PseudocolorAtts.opacityType = PseudocolorAtts.FullyOpaque  # ColorTable, FullyOpaque, Constant, Ramp, VariableRange
	PseudocolorAtts.opacity = 1
	PseudocolorAtts.pointSize = 0.05
	PseudocolorAtts.pointType = PseudocolorAtts.Point  # Box, Axis, Icosahedron, Octahedron, Tetrahedron, SphereGeometry, Point, Sphere
	PseudocolorAtts.pointSizeVarEnabled = 0
	PseudocolorAtts.pointSizeVar = "default"
	PseudocolorAtts.pointSizePixels = 2
	PseudocolorAtts.lineType = PseudocolorAtts.Line  # Line, Tube, Ribbon
	PseudocolorAtts.lineWidth = 0
	SetPlotOptions(PseudocolorAtts)
	DrawPlots()
	# add operator 
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

	# Annotation attributes
	ticks_label_scale = 2.5
	axes_label_size = 2.5
	axes_labels = 1
	AnnotationAtts = AnnotationAttributes()
	AnnotationAtts.axes2D.visible = 1
	AnnotationAtts.axes2D.autoSetTicks = 1
	AnnotationAtts.axes2D.autoSetScaling = 1
	AnnotationAtts.axes2D.lineWidth = 0
	AnnotationAtts.axes2D.tickLocation = AnnotationAtts.axes2D.Outside  # Inside, Outside, Both
	AnnotationAtts.axes2D.tickAxes = AnnotationAtts.axes2D.BottomLeft  # Off, Bottom, Left, BottomLeft, All
	AnnotationAtts.axes2D.xAxis.title.visible = 1
	AnnotationAtts.axes2D.xAxis.title.font.font = AnnotationAtts.axes2D.xAxis.title.font.Times  # Arial, Courier, Times
	AnnotationAtts.axes2D.xAxis.title.font.scale = axes_label_size
	AnnotationAtts.axes2D.xAxis.title.font.useForegroundColor = 1
	AnnotationAtts.axes2D.xAxis.title.font.color = (0, 0, 0, 255)
	AnnotationAtts.axes2D.xAxis.title.font.bold = 0
	AnnotationAtts.axes2D.xAxis.title.font.italic = 0
	AnnotationAtts.axes2D.xAxis.title.userTitle = 1
	AnnotationAtts.axes2D.xAxis.title.userUnits = 0
	AnnotationAtts.axes2D.xAxis.title.title = "x"
	AnnotationAtts.axes2D.xAxis.title.units = ""
	AnnotationAtts.axes2D.xAxis.label.visible = 1
	AnnotationAtts.axes2D.xAxis.label.font.font = AnnotationAtts.axes2D.xAxis.label.font.Times  # Arial, Courier, Times
	AnnotationAtts.axes2D.xAxis.label.font.scale = ticks_label_scale
	AnnotationAtts.axes2D.xAxis.label.font.useForegroundColor = 1
	AnnotationAtts.axes2D.xAxis.label.font.color = (0, 0, 0, 255)
	AnnotationAtts.axes2D.xAxis.label.font.bold = 0
	AnnotationAtts.axes2D.xAxis.label.font.italic = 1
	AnnotationAtts.axes2D.xAxis.label.scaling = 0
	AnnotationAtts.axes2D.xAxis.tickMarks.visible = 1
	AnnotationAtts.axes2D.xAxis.tickMarks.majorMinimum = 0
	AnnotationAtts.axes2D.xAxis.tickMarks.majorMaximum = 1
	AnnotationAtts.axes2D.xAxis.grid = 0
	AnnotationAtts.axes2D.yAxis.title.visible = 1
	AnnotationAtts.axes2D.yAxis.title.font.font = AnnotationAtts.axes2D.yAxis.title.font.Times  # Arial, Courier, Times
	AnnotationAtts.axes2D.yAxis.title.font.scale = axes_label_size
	AnnotationAtts.axes2D.yAxis.title.font.useForegroundColor = 1
	AnnotationAtts.axes2D.yAxis.title.font.color = (0, 0, 0, 255)
	AnnotationAtts.axes2D.yAxis.title.font.bold = 0
	AnnotationAtts.axes2D.yAxis.title.font.italic = 0
	AnnotationAtts.axes2D.yAxis.title.userTitle = 1
	AnnotationAtts.axes2D.yAxis.title.userUnits = 0
	AnnotationAtts.axes2D.yAxis.label.font.bold = 0
	AnnotationAtts.axes2D.yAxis.title.title = "y"
	AnnotationAtts.axes2D.yAxis.title.units = ""
	AnnotationAtts.axes2D.yAxis.label.visible = 1
	AnnotationAtts.axes2D.yAxis.label.font.scale = ticks_label_scale
	AnnotationAtts.axes2D.yAxis.label.font.font = AnnotationAtts.axes2D.yAxis.label.font.Times  # Arial, Courier, Times
	AnnotationAtts.userInfoFlag = 0
	AnnotationAtts.databaseInfoFlag = 0
	AnnotationAtts.timeInfoFlag = 0
	SetAnnotationAttributes(AnnotationAtts)	

        slider = CreateAnnotationObject("TimeSlider")
        """ slider options:                                                                            
        visible = 1                                                                                    
        active = 1"""
        slider.position = (0.16, 0.94)
        slider.width = 0.6
        slider.height = 0.12
        slider.textColor = (0, 0, 0, 255)
        slider.useForegroundForTextColor = 1
        slider.text = "time = $time"
        slider.timeFormatString = "%g"
        # timeDisplay = AllFrames  # AllFrames, FramesForPlot, StatesForPlot, UserSpecified            
        # percentComplete = 0                                                                          
        #slider.startColor = (0, 34, 255, 255)
        #slider.endColor = (200, 200, 200, 153)
        slider.startColor = (255, 255, 255, 0)                                                        
        slider.endColor = (255, 255, 255, 0)
        slider.rounded = 0
        slider.shaded = 0
        
	legend = GetAnnotationObject(GetPlotList().GetPlots(0).plotName)
	legend.xScale = 1
	legend.yScale = 3.2
	legend.managePosition = 0
	legend.position = (0.8, 0.95)
	# the font.
	legend.numberFormat = "%.1f"
	legend.fontFamily = legend.Times
	legend.fontBold = 0
	legend.fontItalic = 0
	legend.drawTitle = 0
	legend.fontHeight = 0.05
	legend.drawMinMax = 0
	# number format
	# turning off the labels.
	legend.drawLabels = 1
	legend.drawMinMax = 0
	
	# turning off the title.
	legend.drawTitle = 0
	
	# Set viewing attributes
	View2DAtts = View2DAttributes()
	View2DAtts.windowCoords = (256-0.5*width, 256+0.5*width, 256-0.5*width, 256+0.5*width)
	View2DAtts.viewportCoords = (0.16, 0.91, 0.14, 0.93)
	View2DAtts.fullFrameActivationMode = View2DAtts.Auto  # On, Off, Auto
	View2DAtts.fullFrameAutoThreshold = 100
	View2DAtts.xScale = View2DAtts.LINEAR  # LINEAR, LOG
	View2DAtts.yScale = View2DAtts.LINEAR  # LINEAR, LOG
	View2DAtts.windowValid = 1
	SetView2D(View2DAtts)
	
	print("made first plot")
	
	# get the number of timesteps
	nts = TimeSliderGetNStates()
	
	# set basic save options
	frame_dir = "BBH_GR_{:s}_rho_movie".format(dd.name)
	try:
        	makedirs(root_plot_path)
	except:
        	pass
	try:
		makedirs(root_plot_path + frame_dir)
	except:
		pass
	# The 'family' option controls if visit automatically adds a frame number to 
	# the rendered files. 
	swatts = SaveWindowAttributes()
	swatts.family = 0
	swatts.resConstraint = swatts.NoConstraint # ScreenProportions, NoConstraint, EqualWidthHeight
	swatts.width = 512
	swatts.height = 422
	# select PNG as the output file format
	swatts.format = swatts.PNG
	swatts.progressive = 1
	
	frame_step=1
	Nframes=int(nts/frame_step)
	
	# make movie frames
	print("starting with frame ", start_frame)
	for ts in range(start_frame, Nframes):
		# Change to the next timestep
		TimeSliderSetState(ts*frame_step)
		swatts.fileName = root_plot_path + frame_dir + "/frame_%06d.png" % ts
		SetPlotOptions(PseudocolorAtts)
		SetSaveWindowAttributes(swatts)
		DrawPlots()
		# render the image to a PNG file
		SaveWindow()
		print("made frame %d of %d" % (ts, Nframes))
	
	# make movie
	# root_movie_path = "/dss/dsshome1/04/di76bej/GRChombo/GRChombo/Analysis/movies/"
	# input_pattern = frame_dir + "BBH_movie_%06d.png"
	# output_movie = root_movie_path + "BBH_SF_rho_" + subdir + "_movie"
	# encoding.encode(input_pattern,output_movie)
	
	# print("saved as " + output_movie)
	# print("done visit run")
	DeleteAllPlots()

for dd in data_dirs:
        make_rho_movie(dd)

exit()

