# coding: utf-8

from sys import exit

# python Visit script
# -------------------

# start
print("starting visit run")

# file settings
root_plot_path = "/home/dc-bamb1/GRChombo/Analysis/plots/"
data_root_dir = "/rds/user/dc-bamb1/rds-dirac-dp131/dc-bamb1/GRChombo_data/KerrSF/"
#subdir = "run0011_l1_m1_a0.7_Al0_mu2.0_M1_IsoKerr"
subdir = "run0005_l1_m1_a0.7_Al0_mu0.4_M1_IsoKerr"
number = 1600
data_file_name = "KerrSFp_%06d.3d.hdf5" % number
width = 256
absmax = 0.4

# open datafile(s)
OpenDatabase(data_root_dir + subdir + "/" + data_file_name,0)

# add plot
AddPlot("Pseudocolor", "phi", 1, 1)
PseudocolorAtts = PseudocolorAttributes()
PseudocolorAtts.scaling = PseudocolorAtts.Linear  # Linear, Log, Skew
PseudocolorAtts.skewFactor = 1
PseudocolorAtts.limitsMode = PseudocolorAtts.OriginalData  # OriginalData, CurrentPlot
PseudocolorAtts.minFlag = 1
PseudocolorAtts.min = -absmax
PseudocolorAtts.maxFlag = 1
PseudocolorAtts.max = absmax
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

# Annotation attributes
axes_label_size = 2.5
tick_label_size = 2.5
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
AnnotationAtts.axes2D.xAxis.label.font.scale = tick_label_size
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
AnnotationAtts.axes2D.yAxis.label.font.scale = tick_label_size
AnnotationAtts.axes2D.yAxis.label.font.font = AnnotationAtts.axes2D.yAxis.label.font.Times  # Arial, Courier, Times
AnnotationAtts.userInfoFlag = 0
AnnotationAtts.databaseInfoFlag = 0
AnnotationAtts.timeInfoFlag = 0
SetAnnotationAttributes(AnnotationAtts)

legend = GetAnnotationObject(GetPlotList().GetPlots(0).plotName)
legend.xScale = 1
legend.yScale = 3.2
legend.managePosition = 0
legend.position = (0.82, 0.95)
# the font.
legend.fontFamily = legend.Times
legend.fontBold = 0
legend.fontItalic = 0
legend.drawTitle = 0
legend.fontHeight = 0.04
legend.drawMinMax = 1

# Set viewing attributes
View2DAtts = View2DAttributes()
View2DAtts.windowCoords = (512-0.5*width, 512+0.5*width, 512-0.5*width, 512+0.5*width)
View2DAtts.viewportCoords = (0.15, 0.85, 0.12, 0.95)
View2DAtts.fullFrameActivationMode = View2DAtts.Auto  # On, Off, Auto
View2DAtts.fullFrameAutoThreshold = 100
View2DAtts.xScale = View2DAtts.LINEAR  # LINEAR, LOG
View2DAtts.yScale = View2DAtts.LINEAR  # LINEAR, LOG
View2DAtts.windowValid = 1
SetView2D(View2DAtts)

# save plot as png
filename = "BBH_SF_phi_" + subdir + "_n%06d" % number 
s = SaveWindowAttributes()
s.family=0
s.format = s.PNG
s.progressive = 1
s.fileName = root_plot_path + filename
s.resConstraint = s.NoConstraint # ScreenProportions, NoConstraint, EqualWidthHeight
s.width = 512
s.height = 412
SetSaveWindowAttributes(s)
name = SaveWindow()
print("name = %s" % name)
print("saved as " + root_plot_path + filename)
exit()
