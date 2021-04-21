# coding: utf-8

from sys import exit

# python Visit script
# -------------------

# start
print("starting visit run")

# file settings
data_root_dir = "/p/project/pra116/bamber1/BinaryBHScalarField/"
#data_root_dir = "/hppfs/work/pn34tu/di76bej/GRChombo_data/BinaryBHScalarField/"
subdir = "run0023v2_mu0.5_delay0_G0.0000000001_ratio1"
#data_root_dir = "/dss/dsshome1/04/di76bej/GRChombo/GRChombo/Examples/BinaryBHScalarField/"
#subdir = "test0001"
number = 0
width = 512

type = "Chk"

data_file_name = "BinaryBHSF" + type + "_%06d.3d.hdf5" % number

def plot_graph(subdir, var):
    # open datafile(s)
    DeleteAllPlots()
    OpenDatabase(data_root_dir + subdir + "/" + data_file_name,0)

    # add plot
    AddPlot("Pseudocolor", var, 1, 1)
    DrawPlots()
    PseudocolorAtts = PseudocolorAttributes()
    PseudocolorAtts.scaling = PseudocolorAtts.Linear  # Linear, Log, Skew
    PseudocolorAtts.skewFactor = 1
    PseudocolorAtts.limitsMode = PseudocolorAtts.OriginalData # OriginalData, CurrentPlot
    PseudocolorAtts.minFlag = 1
    PseudocolorAtts.min = -2
    PseudocolorAtts.maxFlag = 1
    PseudocolorAtts.max = 2
    PseudocolorAtts.centering = PseudocolorAtts.Natural  # Natural, Nodal, Zonal
    PseudocolorAtts.colorTableName = "RdBu"
    PseudocolorAtts.invertColorTable = 0
    PseudocolorAtts.opacityType = PseudocolorAtts.FullyOpaque  # ColorTable, FullyOpaque, Constant, Ramp, VariableRange
    PseudocolorAtts.opacity = 1
    PseudocolorAtts.pointSize = 0.05
    PseudocolorAtts.pointType = PseudocolorAtts.Point  # Box, Axis, Icosahedron, Octahedron, Tetrahedron, SphereGeometry, Point, Sphere
    PseudocolorAtts.pointSizeVarEnabled = 0
    PseudocolorAtts.pointSizeVar = "default"
    PseudocolorAtts.pointSizePixels = 2
    PseudocolorAtts.lineStyle = PseudocolorAtts.SOLID  # SOLID, DASH, DOT, DOTDASH
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
    #root_plot_path = "/dss/dsshome1/04/di76bej/GRChombo/GRChombo/Analysis/plots/"
    root_plot_path = "/p/scratch/pra116/bamber1/plots/GR_Binary_BH/"
    filename = subdir + "_" + var + "_" + type + "_n%06d" % number 
    s = SaveWindowAttributes()
    s.family = 0
    s.format = s.PNG
    s.progressive = 1
    s.fileName = root_plot_path + filename
    SetSaveWindowAttributes(s)
    name = SaveWindow()
    print("name = %s" % name)
    print("saved as " + root_plot_path + filename)

fields = ["chi","h11","h12","h13","h22", "h23", "h33","K","A11","A12","A13","A22", "A23", "A33","Theta","Gamma1", "Gamma2", "Gamma3","lapse","shift1", "shift2", "shift3","B1","B2","B3","phi","Pi"]
    
plot_graph("run0023_mu0.5_delay0_G0.0000000001_ratio1", "h11")
plot_graph("run0023_mu0.5_delay0_G0.0000000001_ratio1", "A22")
plot_graph("run0023_mu0.5_delay0_G0.0000000001_ratio1", "Theta")
plot_graph("run0023_mu0.5_delay0_G0.0000000001_ratio1", "Gamma1")
plot_graph("run0023_mu0.5_delay0_G0.0000000001_ratio1", "B1")
#plot_graph("run0023_InitialConditionsSolver", "lapse")

exit()
