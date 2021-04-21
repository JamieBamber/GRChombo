# coding: utf-8

# python Visit script
# -------------------
from sys import exit
from os import makedirs

# import visit_utils, we will use it to help encode our movie
from visit_utils import *
DeleteAllPlots()

L=1024
N=256
abs_max=10

# start
print("starting visit run")

# data_root_dir = "/p/project/pra116/bamber1/NewtonianBinaryBHScalar/"
data_root_dir = "/p/scratch/pra116/bamber1/NewtonianBinaryScalar/"
root_plot_path = "/p/scratch/pra116/bamber1/plots/Newtonian_Binary_BH/"

class data_dir:
        def __init__(self, num, M, d, mu, dt_mult, l, m, Al):
                self.num = num
                self.M = float(M)
                self.d = float(d)
                self.mu = float(mu)
                self.dt_mult = dt_mult
                self.l = l
                self.m = m
                self.Al = float(Al)
                self.name = "run{:04d}_M{:s}_d{:s}_mu{:s}_dt_mult{:s}_l{:d}_m{:d}_Al{:s}_L{:d}_N{:d}".format(num, M, d, mu, dt_mult, l, m, Al, L, N)

data_dirs = []
def add_data_dir(num, M, d, mu, dt_mult, l, m, Al):
        x = data_dir(num, M, d, mu, dt_mult, l, m, Al)
        data_dirs.append(x)

#add_data_dir(7, "0.2", "10", "0.02", "0.5", 0, 0, "0")
#add_data_dir(8, "0.2", "10", "0.025", "0.5", 0, 0, "0")
#add_data_dir(9, "0.2", "10", "0.015", "0.5", 0, 0, "0")
#add_data_dir(10, "0.2", "10", "0.01", "0.5", 0, 0, "0")
#add_data_dir(11, "0.2", "10", "0.03", "0.5", 0, 0, "0")
#add_data_dir(12, "0.2", "10", "0.02", "0.5", 1, -1, "0")
#add_data_dir(13, "0.2", "10", "0.02", "0.5", 1, 1, "0")
#add_data_dir(15, "0.48847892320123", "12.21358", "1", "0.0625", 0, 0, "0")
#add_data_dir(16, "0.48847892320123", "12.21358", "1", "0.0625", 1, -1, "0")
#add_data_dir(17, "0.48847892320123", "12.21358", "1", "0.0625", 1, 1, "0")
#add_data_dir(18, "0.2", "10", "1", "0.0625", 0, 0, "0")
#add_data_dir(19, "0.2", "10", "0.1", "0.125", 0, 0, "0")
add_data_dir(20, "0.2", "10", "0.5", "0.0625", 0, 0, "0")

# file settings
data_file_name = "Newton_plt*.3d.hdf5 database"

def make_rho_movie(dd):
	width=100
	start_frame = 0
	
	# open datafile(s)
	OpenDatabase(data_root_dir + dd.name + "/" + data_file_name, 0)
	print( "loaded database " + data_root_dir + dd.name + "/" + data_file_name)

	# normalise
	# rho0 = 0.5*(0.4**2)*(0.1**2)
	DefineScalarExpression("norm_Cphi","Cphi/{:.6f}".format(0.5*(dd.mu**2)))
	
	# add plot
	AddPlot("Pseudocolor", "norm_Cphi")
	AddOperator("Slice", 1)
	DrawPlots()
	PseudocolorAtts = PseudocolorAttributes()
	PseudocolorAtts.scaling = PseudocolorAtts.Linear  # Linear, Log, Skew
	PseudocolorAtts.skewFactor = 1
	PseudocolorAtts.limitsMode = PseudocolorAtts.CurrentPlot  # OriginalData, CurrentPlot
	PseudocolorAtts.minFlag = 1
	PseudocolorAtts.min = -abs_max
	PseudocolorAtts.maxFlag = 1
	PseudocolorAtts.max = abs_max
	PseudocolorAtts.centering = PseudocolorAtts.Natural  # Natural, Nodal, Zonal
	PseudocolorAtts.colorTableName = "RdBu"
	PseudocolorAtts.invertColorTable = 1
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
	AnnotationAtts = GetAnnotationAttributes()
        #AnnotationAttributes()
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
	AnnotationAtts.axes2D.yAxis.label.font.font = AnnotationAtts.axes2D.yAxis.label.font.Times  # Arial, Courier, Times"""
	AnnotationAtts.userInfoFlag = 0
	AnnotationAtts.databaseInfoFlag = 0
	AnnotationAtts.timeInfoFlag = 0
	SetAnnotationAttributes(AnnotationAtts)	

	legend = GetAnnotationObject(GetPlotList().GetPlots(0).plotName)
	legend.xScale = 1
	legend.yScale = 3.2
	legend.managePosition = 0
	legend.position = (0.8, 0.95)
	# the font.
	legend.numberFormat = "%.2f"
	legend.fontFamily = legend.Times
	legend.fontBold = 0
	legend.fontItalic = 0
	legend.drawTitle = 0
	legend.fontHeight = 0.05
	legend.drawMinMax = 0
	# number format
	# turning off the labels.
	legend.drawLabels = 1
	legend.drawMinMax = 1
	
	# turning off the title.
	legend.drawTitle = 0

        slider = CreateAnnotationObject("TimeSlider")
        """ slider options:
        visible = 1
        active = 1"""
        slider.position = (0.16, 0.94)
        slider.width = 0.6
        slider.height = 0.12
        slider.textColor = (0, 0, 0, 255)
        #slider.position = (0.15, 0.91)
        #slider.width = 0.6
        #slider.height = 0.07
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
        
	# Set viewing attributes
	View2DAtts = View2DAttributes()
	View2DAtts.windowCoords = (L/2-0.5*width, L/2+0.5*width, L/2-0.5*width, L/2+0.5*width)
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
	frame_dir = "BBH_Newtonian_{:s}_Cphi_movie".format(dd.name)
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
        Nmax=1565
        # dt_0 = 2
        # dt_mult = 0.5
        # plot_interval = 20
        # period T = 100π ~ 315
        # Nmax ~ (100T)/(2*0.5*20) ~ 5T ~ 1565
        Nframes=int(nts/frame_step)
        print("Nframes = " + str(Nframes))
        
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

#make_rho_movie(data_dirs[0])
        
for dd in data_dirs:
        make_rho_movie(dd)

exit()

