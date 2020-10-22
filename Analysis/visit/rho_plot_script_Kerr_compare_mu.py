# coding: utf-8

from sys import exit

# python Visit script
# -------------------

# start
print("starting visit run")

class data_dir:
        def __init__(self, run_number, l, m, a, mu, number):
                self.rnum = run_number
                self.l = l
                self.m = m
                self.a = float(a)
                self.mu = mu
		self.number = number
                self.name = "run{:04d}_KNL_l{:d}_m{:d}_a{:s}_Al0_mu{:s}_M1_correct_Ylm_new_rho".format(run_number, l, m, a, mu)

data_dirs = []
def add_data_dir(run_number, l, m, a, mu, number):
        x = data_dir(run_number, l, m, a, mu, number)
        data_dirs.append(x)

# choose datasets to compare
add_data_dir(59, 1, 1, "0.7", "0.05", 380)
add_data_dir(39, 1, 1, "0.7", "0.4", 380)
add_data_dir(61, 1, 1, "0.7", "1", 760)
add_data_dir(60, 1, 1, "0.7", "2", 1520)

# file settings
data_root_dir = "/rds/user/dc-bamb1/rds-dirac-dp131/dc-bamb1/GRChombo_data/KerrSF/"
L=1024
width=400
phi0=0.1
max_rho_ratio=10

def make_plot(dd):
	ClearWindow()
	ClearAllWindows()
	mu=float(dd.mu)
	
	# open datafile(s)
	data_file_name = "KerrSFp_%06d.3d.hdf5" % dd.number
	database_name = data_root_dir + dd.name + "/" + data_file_name
	OpenDatabase(database_name,0)
	
	# add plot
	AddPlot("Pseudocolor", "rho", 1, 1)
	PseudocolorAtts = PseudocolorAttributes()
	PseudocolorAtts.scaling = PseudocolorAtts.Linear  # Linear, Log, Skew
	PseudocolorAtts.skewFactor = 1
	PseudocolorAtts.limitsMode = PseudocolorAtts.OriginalData  # OriginalData, CurrentPlot
	PseudocolorAtts.minFlag = 1
	PseudocolorAtts.min = 0
	PseudocolorAtts.maxFlag = 1
	PseudocolorAtts.max = max_rho_ratio*0.5*(phi0*mu)**2
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
	View2DAtts.windowCoords = (0.5*(L-width), 0.5*(L+width), 0.5*(L-width), 0.5*(L+width))
	View2DAtts.viewportCoords = (0.2, 0.95, 0.15, 0.95)
	View2DAtts.fullFrameActivationMode = View2DAtts.Auto  # On, Off, Auto
	View2DAtts.fullFrameAutoThreshold = 100
	View2DAtts.xScale = View2DAtts.LINEAR  # LINEAR, LOG
	View2DAtts.yScale = View2DAtts.LINEAR  # LINEAR, LOG
	View2DAtts.windowValid = 1
	SetView2D(View2DAtts)
	
	# save plot as png
	root_plot_path = "/home/dc-bamb1/GRChombo/Analysis/plots/"
	#root_plot_path = "/dss/dsshome1/04/di76bej/GRChombo/GRChombo/Analysis/plots/"
	filename = "KerrSF_rho_" + dd.name + "_n%06d" % dd.number 
	s = SaveWindowAttributes()
	s.format = s.PNG
	s.progressive = 0
	s.family = 0
	s.fileName = root_plot_path + filename
	SetSaveWindowAttributes(s)
	name = SaveWindow()
	print("name = %s" % name)
	print("saved as " + root_plot_path + filename)
	DeleteActivePlots()
	ClearWindow()
	ClearAllWindows()
	CloseDatabase(database_name)

for dd in data_dirs:
	make_plot(dd)

exit()
	
