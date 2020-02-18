# Visit 2.13.3 log file
ScriptVersion = "2.13.3"
if ScriptVersion != Version():
    print "This script is for VisIt %s. It may not work with version %s" % (ScriptVersion, Version())
ShowAllWindows()
# MAINTENANCE ISSUE: SetSuppressMessagesRPC is not handled in Logging.C. Please contact a VisIt developer.
SaveSession("/Users/Jamie/.visit/crash_recovery.4536.session")
# MAINTENANCE ISSUE: SetSuppressMessagesRPC is not handled in Logging.C. Please contact a VisIt developer.
# MAINTENANCE ISSUE: SetSuppressMessagesRPC is not handled in Logging.C. Please contact a VisIt developer.
SaveSession("/Users/Jamie/.visit/crash_recovery.4536.session")
# MAINTENANCE ISSUE: SetSuppressMessagesRPC is not handled in Logging.C. Please contact a VisIt developer.
OpenDatabase("login-cpu.hpc.cam.ac.uk:/rds/user/dc-bamb1/rds-dirac-dp131/dc-bamb1/GRChombo_data/KerrSF/run0039_KNL_l1_m1_a0.7_Al0_mu0.4_M1_correct_Ylm_KerrSchild/KerrSFp_*.3d.hdf5 database", 0)
metadata = GetMetaData("login-cpu.hpc.cam.ac.uk:/rds/user/dc-bamb1/rds-dirac-dp131/dc-bamb1/GRChombo_data/KerrSF/run0039_KNL_l1_m1_a0.7_Al0_mu0.4_M1_correct_Ylm_KerrSchild/KerrSFp_*.3d.hdf5 database", -1)
AddPlot("Mesh", "Mesh", 1, 1)
MeshAtts = MeshAttributes()
MeshAtts.legendFlag = 0
MeshAtts.lineStyle = MeshAtts.SOLID  # SOLID, DASH, DOT, DOTDASH
MeshAtts.lineWidth = 0
MeshAtts.meshColor = (0, 0, 0, 255)
MeshAtts.meshColorSource = MeshAtts.Foreground  # Foreground, MeshCustom
MeshAtts.opaqueColorSource = MeshAtts.Background  # Background, OpaqueCustom
MeshAtts.opaqueMode = MeshAtts.Auto  # Auto, On, Off
MeshAtts.pointSize = 0.05
MeshAtts.opaqueColor = (255, 255, 255, 255)
MeshAtts.smoothingLevel = MeshAtts.None  # None, Fast, High
MeshAtts.pointSizeVarEnabled = 0
MeshAtts.pointSizeVar = "default"
MeshAtts.pointType = MeshAtts.Point  # Box, Axis, Icosahedron, Octahedron, Tetrahedron, SphereGeometry, Point, Sphere
MeshAtts.showInternal = 0
MeshAtts.pointSizePixels = 2
MeshAtts.opacity = 1
SetPlotOptions(MeshAtts)
HideActivePlots()
AddOperator("ThreeSlice", 1)
ThreeSliceAtts = ThreeSliceAttributes()
ThreeSliceAtts.x = 512
ThreeSliceAtts.y = 512
ThreeSliceAtts.z = 256
ThreeSliceAtts.interactive = 1
SetOperatorOptions(ThreeSliceAtts, 1)
AddPlot("Pseudocolor", "phi", 1, 1)
AddOperator("ThreeSlice", 1)
ThreeSliceAtts = ThreeSliceAttributes()
ThreeSliceAtts.x = 512
ThreeSliceAtts.y = 512
ThreeSliceAtts.z = 256
ThreeSliceAtts.interactive = 1
SetOperatorOptions(ThreeSliceAtts, 1)
DrawPlots()
SetActivePlots(1)
SetActivePlots(1)
RemoveOperator(0, 1)
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
SliceAtts.interactive = 1
SliceAtts.flip = 0
SliceAtts.originZoneDomain = 0
SliceAtts.originNodeDomain = 0
SliceAtts.meshName = "Mesh"
SliceAtts.theta = 0
SliceAtts.phi = 90
SetOperatorOptions(SliceAtts, 1)
DrawPlots()
silr = SILRestriction()
silr.TurnOnAll()
SetPlotSILRestriction(silr ,1)
PseudocolorAtts = PseudocolorAttributes()
PseudocolorAtts.scaling = PseudocolorAtts.Linear  # Linear, Log, Skew
PseudocolorAtts.skewFactor = 1
PseudocolorAtts.limitsMode = PseudocolorAtts.OriginalData  # OriginalData, CurrentPlot
PseudocolorAtts.minFlag = 1
PseudocolorAtts.min = -0.2
PseudocolorAtts.maxFlag = 1
PseudocolorAtts.max = 0.2
PseudocolorAtts.centering = PseudocolorAtts.Natural  # Natural, Nodal, Zonal
PseudocolorAtts.colorTableName = "RdBu"
PseudocolorAtts.invertColorTable = 1
PseudocolorAtts.opacityType = PseudocolorAtts.FullyOpaque  # ColorTable, FullyOpaque, Constant, Ramp, VariableRange
PseudocolorAtts.opacityVariable = ""
PseudocolorAtts.opacity = 1
PseudocolorAtts.opacityVarMin = 0
PseudocolorAtts.opacityVarMax = 1
PseudocolorAtts.opacityVarMinFlag = 0
PseudocolorAtts.opacityVarMaxFlag = 0
PseudocolorAtts.pointSize = 0.05
PseudocolorAtts.pointType = PseudocolorAtts.Point  # Box, Axis, Icosahedron, Octahedron, Tetrahedron, SphereGeometry, Point, Sphere
PseudocolorAtts.pointSizeVarEnabled = 0
PseudocolorAtts.pointSizeVar = "default"
PseudocolorAtts.pointSizePixels = 2
PseudocolorAtts.lineStyle = PseudocolorAtts.SOLID  # SOLID, DASH, DOT, DOTDASH
PseudocolorAtts.lineType = PseudocolorAtts.Line  # Line, Tube, Ribbon
PseudocolorAtts.lineWidth = 0
PseudocolorAtts.tubeResolution = 10
PseudocolorAtts.tubeRadiusSizeType = PseudocolorAtts.FractionOfBBox  # Absolute, FractionOfBBox
PseudocolorAtts.tubeRadiusAbsolute = 0.125
PseudocolorAtts.tubeRadiusBBox = 0.005
PseudocolorAtts.tubeRadiusVarEnabled = 0
PseudocolorAtts.tubeRadiusVar = ""
PseudocolorAtts.tubeRadiusVarRatio = 10
PseudocolorAtts.tailStyle = PseudocolorAtts.None  # None, Spheres, Cones
PseudocolorAtts.headStyle = PseudocolorAtts.None  # None, Spheres, Cones
PseudocolorAtts.endPointRadiusSizeType = PseudocolorAtts.FractionOfBBox  # Absolute, FractionOfBBox
PseudocolorAtts.endPointRadiusAbsolute = 0.125
PseudocolorAtts.endPointRadiusBBox = 0.05
PseudocolorAtts.endPointResolution = 10
PseudocolorAtts.endPointRatio = 5
PseudocolorAtts.endPointRadiusVarEnabled = 0
PseudocolorAtts.endPointRadiusVar = ""
PseudocolorAtts.endPointRadiusVarRatio = 10
PseudocolorAtts.renderSurfaces = 1
PseudocolorAtts.renderWireframe = 0
PseudocolorAtts.renderPoints = 0
PseudocolorAtts.smoothingLevel = 0
PseudocolorAtts.legendFlag = 1
PseudocolorAtts.lightingFlag = 1
PseudocolorAtts.wireframeColor = (0, 0, 0, 0)
PseudocolorAtts.pointColor = (0, 0, 0, 0)
SetPlotOptions(PseudocolorAtts)
SetTimeSliderState(154)
SetTimeSliderState(193)
AddWindow()
SetActiveWindow(2)
OpenDatabase("login-cpu.hpc.cam.ac.uk:/rds/user/dc-bamb1/rds-dirac-dp131/dc-bamb1/GRChombo_data/KerrSF/run0039_KNL_l1_m1_a0.7_Al0_mu0.4_M1_correct_Ylm/KerrSFp_*.3d.hdf5 database", 0)
metadata = GetMetaData("login-cpu.hpc.cam.ac.uk:/rds/user/dc-bamb1/rds-dirac-dp131/dc-bamb1/GRChombo_data/KerrSF/run0039_KNL_l1_m1_a0.7_Al0_mu0.4_M1_correct_Ylm/KerrSFp_*.3d.hdf5 database", -1)
SetActivePlots((0, 1))
SetActivePlots((0, 1))
SetActivePlots(0)
SetActivePlots(0)
SetActivePlots(0)
SetActivePlots(0)
SetActivePlots(0)
SetActivePlots(0)
SetActivePlots(0)
# MAINTENANCE ISSUE: SetSuppressMessagesRPC is not handled in Logging.C. Please contact a VisIt developer.
SaveSession("/Users/Jamie/.visit/crash_recovery.4536.session")
# MAINTENANCE ISSUE: SetSuppressMessagesRPC is not handled in Logging.C. Please contact a VisIt developer.
AddPlot("Mesh", "Mesh", 1, 1)
MeshAtts = MeshAttributes()
MeshAtts.legendFlag = 0
MeshAtts.lineStyle = MeshAtts.SOLID  # SOLID, DASH, DOT, DOTDASH
MeshAtts.lineWidth = 0
MeshAtts.meshColor = (0, 0, 0, 255)
MeshAtts.meshColorSource = MeshAtts.Foreground  # Foreground, MeshCustom
MeshAtts.opaqueColorSource = MeshAtts.Background  # Background, OpaqueCustom
MeshAtts.opaqueMode = MeshAtts.Auto  # Auto, On, Off
MeshAtts.pointSize = 0.05
MeshAtts.opaqueColor = (255, 255, 255, 255)
MeshAtts.smoothingLevel = MeshAtts.None  # None, Fast, High
MeshAtts.pointSizeVarEnabled = 0
MeshAtts.pointSizeVar = "default"
MeshAtts.pointType = MeshAtts.Point  # Box, Axis, Icosahedron, Octahedron, Tetrahedron, SphereGeometry, Point, Sphere
MeshAtts.showInternal = 0
MeshAtts.pointSizePixels = 2
MeshAtts.opacity = 1
SetPlotOptions(MeshAtts)
HideActivePlots()
AddOperator("ThreeSlice", 1)
ThreeSliceAtts = ThreeSliceAttributes()
ThreeSliceAtts.x = 512
ThreeSliceAtts.y = 512
ThreeSliceAtts.z = 256
ThreeSliceAtts.interactive = 1
SetOperatorOptions(ThreeSliceAtts, 1)
AddPlot("Pseudocolor", "phi", 1, 1)
AddOperator("ThreeSlice", 1)
ThreeSliceAtts = ThreeSliceAttributes()
ThreeSliceAtts.x = 512
ThreeSliceAtts.y = 512
ThreeSliceAtts.z = 256
ThreeSliceAtts.interactive = 1
SetOperatorOptions(ThreeSliceAtts, 1)
DrawPlots()
# Begin spontaneous state
View3DAtts = View3DAttributes()
View3DAtts.viewNormal = (0, 0, 1)
View3DAtts.focus = (512, 512, 256)
View3DAtts.viewUp = (0, 1, 0)
View3DAtts.viewAngle = 30
View3DAtts.parallelScale = 768
View3DAtts.nearPlane = -1536
View3DAtts.farPlane = 1536
View3DAtts.imagePan = (0, 0)
View3DAtts.imageZoom = 1
View3DAtts.perspective = 1
View3DAtts.eyeAngle = 2
View3DAtts.centerOfRotationSet = 0
View3DAtts.centerOfRotation = (512, 512, 256)
View3DAtts.axis3DScaleFlag = 0
View3DAtts.axis3DScales = (1, 1, 1)
View3DAtts.shear = (0, 0, 1)
View3DAtts.windowValid = 1
SetView3D(View3DAtts)
# End spontaneous state

SetActivePlots(3)
SetActivePlots(3)
RemoveOperator(0, 1)
RemoveOperator(0, 1)
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
SliceAtts.interactive = 1
SliceAtts.flip = 0
SliceAtts.originZoneDomain = 0
SliceAtts.originNodeDomain = 0
SliceAtts.meshName = "Mesh"
SliceAtts.theta = 0
SliceAtts.phi = 90
SetOperatorOptions(SliceAtts, 1)
silr = SILRestriction()
silr.TurnOnAll()
SetPlotSILRestriction(silr ,1)
SetActiveTimeSlider("login-cpu.hpc.cam.ac.uk:/rds/user/dc-bamb1/rds-dirac-dp131/dc-bamb1/GRChombo_data/KerrSF/run0039_KNL_l1_m1_a0.7_Al0_mu0.4_M1_correct_Ylm_KerrSchild/KerrSFp_*.3d.hdf5 database")
SetActiveTimeSlider("login-cpu.hpc.cam.ac.uk:/rds/user/dc-bamb1/rds-dirac-dp131/dc-bamb1/GRChombo_data/KerrSF/run0039_KNL_l1_m1_a0.7_Al0_mu0.4_M1_correct_Ylm/KerrSFp_*.3d.hdf5 database")
SetTimeSliderState(193)
SetActiveTimeSlider("login-cpu.hpc.cam.ac.uk:/rds/user/dc-bamb1/rds-dirac-dp131/dc-bamb1/GRChombo_data/KerrSF/run0039_KNL_l1_m1_a0.7_Al0_mu0.4_M1_correct_Ylm_KerrSchild/KerrSFp_*.3d.hdf5 database")
SetActiveTimeSlider("login-cpu.hpc.cam.ac.uk:/rds/user/dc-bamb1/rds-dirac-dp131/dc-bamb1/GRChombo_data/KerrSF/run0039_KNL_l1_m1_a0.7_Al0_mu0.4_M1_correct_Ylm/KerrSFp_*.3d.hdf5 database")
PseudocolorAtts = PseudocolorAttributes()
PseudocolorAtts.scaling = PseudocolorAtts.Linear  # Linear, Log, Skew
PseudocolorAtts.skewFactor = 1
PseudocolorAtts.limitsMode = PseudocolorAtts.OriginalData  # OriginalData, CurrentPlot
PseudocolorAtts.minFlag = 1
PseudocolorAtts.min = -0.2
PseudocolorAtts.maxFlag = 1
PseudocolorAtts.max = 0.2
PseudocolorAtts.centering = PseudocolorAtts.Natural  # Natural, Nodal, Zonal
PseudocolorAtts.colorTableName = "PuOr"
PseudocolorAtts.invertColorTable = 1
PseudocolorAtts.opacityType = PseudocolorAtts.FullyOpaque  # ColorTable, FullyOpaque, Constant, Ramp, VariableRange
PseudocolorAtts.opacityVariable = ""
PseudocolorAtts.opacity = 1
PseudocolorAtts.opacityVarMin = 0
PseudocolorAtts.opacityVarMax = 1
PseudocolorAtts.opacityVarMinFlag = 0
PseudocolorAtts.opacityVarMaxFlag = 0
PseudocolorAtts.pointSize = 0.05
PseudocolorAtts.pointType = PseudocolorAtts.Point  # Box, Axis, Icosahedron, Octahedron, Tetrahedron, SphereGeometry, Point, Sphere
PseudocolorAtts.pointSizeVarEnabled = 0
PseudocolorAtts.pointSizeVar = "default"
PseudocolorAtts.pointSizePixels = 2
PseudocolorAtts.lineStyle = PseudocolorAtts.SOLID  # SOLID, DASH, DOT, DOTDASH
PseudocolorAtts.lineType = PseudocolorAtts.Line  # Line, Tube, Ribbon
PseudocolorAtts.lineWidth = 0
PseudocolorAtts.tubeResolution = 10
PseudocolorAtts.tubeRadiusSizeType = PseudocolorAtts.FractionOfBBox  # Absolute, FractionOfBBox
PseudocolorAtts.tubeRadiusAbsolute = 0.125
PseudocolorAtts.tubeRadiusBBox = 0.005
PseudocolorAtts.tubeRadiusVarEnabled = 0
PseudocolorAtts.tubeRadiusVar = ""
PseudocolorAtts.tubeRadiusVarRatio = 10
PseudocolorAtts.tailStyle = PseudocolorAtts.None  # None, Spheres, Cones
PseudocolorAtts.headStyle = PseudocolorAtts.None  # None, Spheres, Cones
PseudocolorAtts.endPointRadiusSizeType = PseudocolorAtts.FractionOfBBox  # Absolute, FractionOfBBox
PseudocolorAtts.endPointRadiusAbsolute = 0.125
PseudocolorAtts.endPointRadiusBBox = 0.05
PseudocolorAtts.endPointResolution = 10
PseudocolorAtts.endPointRatio = 5
PseudocolorAtts.endPointRadiusVarEnabled = 0
PseudocolorAtts.endPointRadiusVar = ""
PseudocolorAtts.endPointRadiusVarRatio = 10
PseudocolorAtts.renderSurfaces = 1
PseudocolorAtts.renderWireframe = 0
PseudocolorAtts.renderPoints = 0
PseudocolorAtts.smoothingLevel = 0
PseudocolorAtts.legendFlag = 1
PseudocolorAtts.lightingFlag = 1
PseudocolorAtts.wireframeColor = (0, 0, 0, 0)
PseudocolorAtts.pointColor = (0, 0, 0, 0)
SetPlotOptions(PseudocolorAtts)
DrawPlots()
SetActivePlots((2, 3))
SetActivePlots(2)
SetActivePlots((0, 2))
SetActivePlots(0)
HideActivePlots()
# MAINTENANCE ISSUE: SetSuppressMessagesRPC is not handled in Logging.C. Please contact a VisIt developer.
SaveSession("/Users/Jamie/.visit/crash_recovery.4536.session")
# MAINTENANCE ISSUE: SetSuppressMessagesRPC is not handled in Logging.C. Please contact a VisIt developer.
SetActiveWindow(1)
SetActiveWindow(1)
# Begin spontaneous state
View2DAtts = View2DAttributes()
View2DAtts.windowCoords = (306, 717, 306, 717)
View2DAtts.viewportCoords = (0.2, 0.95, 0.15, 0.95)
View2DAtts.fullFrameActivationMode = View2DAtts.Auto  # On, Off, Auto
View2DAtts.fullFrameAutoThreshold = 100
View2DAtts.xScale = View2DAtts.LINEAR  # LINEAR, LOG
View2DAtts.yScale = View2DAtts.LINEAR  # LINEAR, LOG
View2DAtts.windowValid = 1
SetView2D(View2DAtts)
# End spontaneous state

ViewCurveAtts = ViewCurveAttributes()
ViewCurveAtts.domainCoords = (0, 1)
ViewCurveAtts.rangeCoords = (0, 1)
ViewCurveAtts.viewportCoords = (0.2, 0.95, 0.15, 0.95)
ViewCurveAtts.domainScale = ViewCurveAtts.LINEAR  # LINEAR, LOG
ViewCurveAtts.rangeScale = ViewCurveAtts.LINEAR  # LINEAR, LOG
SetViewCurve(ViewCurveAtts)
View2DAtts = View2DAttributes()
View2DAtts.windowCoords = (306, 717, 306, 717)
View2DAtts.viewportCoords = (0.2, 0.95, 0.15, 0.95)
View2DAtts.fullFrameActivationMode = View2DAtts.Auto  # On, Off, Auto
View2DAtts.fullFrameAutoThreshold = 100
View2DAtts.xScale = View2DAtts.LINEAR  # LINEAR, LOG
View2DAtts.yScale = View2DAtts.LINEAR  # LINEAR, LOG
View2DAtts.windowValid = 1
SetView2D(View2DAtts)
View3DAtts = View3DAttributes()
View3DAtts.viewNormal = (0, 0, 1)
View3DAtts.focus = (512, 512, 256)
View3DAtts.viewUp = (0, 1, 0)
View3DAtts.viewAngle = 30
View3DAtts.parallelScale = 768
View3DAtts.nearPlane = -1536
View3DAtts.farPlane = 1536
View3DAtts.imagePan = (0, 0)
View3DAtts.imageZoom = 1
View3DAtts.perspective = 1
View3DAtts.eyeAngle = 2
View3DAtts.centerOfRotationSet = 0
View3DAtts.centerOfRotation = (512, 512, 256)
View3DAtts.axis3DScaleFlag = 0
View3DAtts.axis3DScales = (1, 1, 1)
View3DAtts.shear = (0, 0, 1)
View3DAtts.windowValid = 1
SetView3D(View3DAtts)
ViewAxisArrayAtts = ViewAxisArrayAttributes()
ViewAxisArrayAtts.domainCoords = (0, 1)
ViewAxisArrayAtts.rangeCoords = (0, 1)
ViewAxisArrayAtts.viewportCoords = (0.15, 0.9, 0.1, 0.85)
SetViewAxisArray(ViewAxisArrayAtts)
SetActiveWindow(2)
SetActiveWindow(2)
# Begin spontaneous state
View2DAtts = View2DAttributes()
View2DAtts.windowCoords = (306, 717, 306, 717)
View2DAtts.viewportCoords = (0.2, 0.95, 0.15, 0.95)
View2DAtts.fullFrameActivationMode = View2DAtts.Auto  # On, Off, Auto
View2DAtts.fullFrameAutoThreshold = 100
View2DAtts.xScale = View2DAtts.LINEAR  # LINEAR, LOG
View2DAtts.yScale = View2DAtts.LINEAR  # LINEAR, LOG
View2DAtts.windowValid = 1
SetView2D(View2DAtts)
# End spontaneous state

ViewCurveAtts = ViewCurveAttributes()
ViewCurveAtts.domainCoords = (0, 1)
ViewCurveAtts.rangeCoords = (0, 1)
ViewCurveAtts.viewportCoords = (0.2, 0.95, 0.15, 0.95)
ViewCurveAtts.domainScale = ViewCurveAtts.LINEAR  # LINEAR, LOG
ViewCurveAtts.rangeScale = ViewCurveAtts.LINEAR  # LINEAR, LOG
SetViewCurve(ViewCurveAtts)
View2DAtts = View2DAttributes()
View2DAtts.windowCoords = (306, 717, 306, 717)
View2DAtts.viewportCoords = (0.2, 0.95, 0.15, 0.95)
View2DAtts.fullFrameActivationMode = View2DAtts.Auto  # On, Off, Auto
View2DAtts.fullFrameAutoThreshold = 100
View2DAtts.xScale = View2DAtts.LINEAR  # LINEAR, LOG
View2DAtts.yScale = View2DAtts.LINEAR  # LINEAR, LOG
View2DAtts.windowValid = 1
SetView2D(View2DAtts)
View3DAtts = View3DAttributes()
View3DAtts.viewNormal = (0, 0, 1)
View3DAtts.focus = (512, 512, 256)
View3DAtts.viewUp = (0, 1, 0)
View3DAtts.viewAngle = 30
View3DAtts.parallelScale = 768
View3DAtts.nearPlane = -1536
View3DAtts.farPlane = 1536
View3DAtts.imagePan = (0, 0)
View3DAtts.imageZoom = 1
View3DAtts.perspective = 1
View3DAtts.eyeAngle = 2
View3DAtts.centerOfRotationSet = 0
View3DAtts.centerOfRotation = (512, 512, 256)
View3DAtts.axis3DScaleFlag = 0
View3DAtts.axis3DScales = (1, 1, 1)
View3DAtts.shear = (0, 0, 1)
View3DAtts.windowValid = 1
SetView3D(View3DAtts)
ViewAxisArrayAtts = ViewAxisArrayAttributes()
ViewAxisArrayAtts.domainCoords = (0, 1)
ViewAxisArrayAtts.rangeCoords = (0, 1)
ViewAxisArrayAtts.viewportCoords = (0.15, 0.9, 0.1, 0.85)
SetViewAxisArray(ViewAxisArrayAtts)
PseudocolorAtts = PseudocolorAttributes()
PseudocolorAtts.scaling = PseudocolorAtts.Linear  # Linear, Log, Skew
PseudocolorAtts.skewFactor = 1
PseudocolorAtts.limitsMode = PseudocolorAtts.OriginalData  # OriginalData, CurrentPlot
PseudocolorAtts.minFlag = 1
PseudocolorAtts.min = -1
PseudocolorAtts.maxFlag = 1
PseudocolorAtts.max = 1
PseudocolorAtts.centering = PseudocolorAtts.Natural  # Natural, Nodal, Zonal
PseudocolorAtts.colorTableName = "RdBu"
PseudocolorAtts.invertColorTable = 1
PseudocolorAtts.opacityType = PseudocolorAtts.FullyOpaque  # ColorTable, FullyOpaque, Constant, Ramp, VariableRange
PseudocolorAtts.opacityVariable = ""
PseudocolorAtts.opacity = 1
PseudocolorAtts.opacityVarMin = 0
PseudocolorAtts.opacityVarMax = 1
PseudocolorAtts.opacityVarMinFlag = 0
PseudocolorAtts.opacityVarMaxFlag = 0
PseudocolorAtts.pointSize = 0.05
PseudocolorAtts.pointType = PseudocolorAtts.Point  # Box, Axis, Icosahedron, Octahedron, Tetrahedron, SphereGeometry, Point, Sphere
PseudocolorAtts.pointSizeVarEnabled = 0
PseudocolorAtts.pointSizeVar = "default"
PseudocolorAtts.pointSizePixels = 2
PseudocolorAtts.lineStyle = PseudocolorAtts.SOLID  # SOLID, DASH, DOT, DOTDASH
PseudocolorAtts.lineType = PseudocolorAtts.Line  # Line, Tube, Ribbon
PseudocolorAtts.lineWidth = 0
PseudocolorAtts.tubeResolution = 10
PseudocolorAtts.tubeRadiusSizeType = PseudocolorAtts.FractionOfBBox  # Absolute, FractionOfBBox
PseudocolorAtts.tubeRadiusAbsolute = 0.125
PseudocolorAtts.tubeRadiusBBox = 0.005
PseudocolorAtts.tubeRadiusVarEnabled = 0
PseudocolorAtts.tubeRadiusVar = ""
PseudocolorAtts.tubeRadiusVarRatio = 10
PseudocolorAtts.tailStyle = PseudocolorAtts.None  # None, Spheres, Cones
PseudocolorAtts.headStyle = PseudocolorAtts.None  # None, Spheres, Cones
PseudocolorAtts.endPointRadiusSizeType = PseudocolorAtts.FractionOfBBox  # Absolute, FractionOfBBox
PseudocolorAtts.endPointRadiusAbsolute = 0.125
PseudocolorAtts.endPointRadiusBBox = 0.05
PseudocolorAtts.endPointResolution = 10
PseudocolorAtts.endPointRatio = 5
PseudocolorAtts.endPointRadiusVarEnabled = 0
PseudocolorAtts.endPointRadiusVar = ""
PseudocolorAtts.endPointRadiusVarRatio = 10
PseudocolorAtts.renderSurfaces = 1
PseudocolorAtts.renderWireframe = 0
PseudocolorAtts.renderPoints = 0
PseudocolorAtts.smoothingLevel = 0
PseudocolorAtts.legendFlag = 1
PseudocolorAtts.lightingFlag = 1
PseudocolorAtts.wireframeColor = (0, 0, 0, 0)
PseudocolorAtts.pointColor = (0, 0, 0, 0)
SetPlotOptions(PseudocolorAtts)
SetActiveWindow(1)
SetActiveWindow(1)
PseudocolorAtts = PseudocolorAttributes()
PseudocolorAtts.scaling = PseudocolorAtts.Linear  # Linear, Log, Skew
PseudocolorAtts.skewFactor = 1
PseudocolorAtts.limitsMode = PseudocolorAtts.OriginalData  # OriginalData, CurrentPlot
PseudocolorAtts.minFlag = 1
PseudocolorAtts.min = -1
PseudocolorAtts.maxFlag = 1
PseudocolorAtts.max = 1
PseudocolorAtts.centering = PseudocolorAtts.Natural  # Natural, Nodal, Zonal
PseudocolorAtts.colorTableName = "RdBu"
PseudocolorAtts.invertColorTable = 1
PseudocolorAtts.opacityType = PseudocolorAtts.FullyOpaque  # ColorTable, FullyOpaque, Constant, Ramp, VariableRange
PseudocolorAtts.opacityVariable = ""
PseudocolorAtts.opacity = 1
PseudocolorAtts.opacityVarMin = 0
PseudocolorAtts.opacityVarMax = 1
PseudocolorAtts.opacityVarMinFlag = 0
PseudocolorAtts.opacityVarMaxFlag = 0
PseudocolorAtts.pointSize = 0.05
PseudocolorAtts.pointType = PseudocolorAtts.Point  # Box, Axis, Icosahedron, Octahedron, Tetrahedron, SphereGeometry, Point, Sphere
PseudocolorAtts.pointSizeVarEnabled = 0
PseudocolorAtts.pointSizeVar = "default"
PseudocolorAtts.pointSizePixels = 2
PseudocolorAtts.lineStyle = PseudocolorAtts.SOLID  # SOLID, DASH, DOT, DOTDASH
PseudocolorAtts.lineType = PseudocolorAtts.Line  # Line, Tube, Ribbon
PseudocolorAtts.lineWidth = 0
PseudocolorAtts.tubeResolution = 10
PseudocolorAtts.tubeRadiusSizeType = PseudocolorAtts.FractionOfBBox  # Absolute, FractionOfBBox
PseudocolorAtts.tubeRadiusAbsolute = 0.125
PseudocolorAtts.tubeRadiusBBox = 0.005
PseudocolorAtts.tubeRadiusVarEnabled = 0
PseudocolorAtts.tubeRadiusVar = ""
PseudocolorAtts.tubeRadiusVarRatio = 10
PseudocolorAtts.tailStyle = PseudocolorAtts.None  # None, Spheres, Cones
PseudocolorAtts.headStyle = PseudocolorAtts.None  # None, Spheres, Cones
PseudocolorAtts.endPointRadiusSizeType = PseudocolorAtts.FractionOfBBox  # Absolute, FractionOfBBox
PseudocolorAtts.endPointRadiusAbsolute = 0.125
PseudocolorAtts.endPointRadiusBBox = 0.05
PseudocolorAtts.endPointResolution = 10
PseudocolorAtts.endPointRatio = 5
PseudocolorAtts.endPointRadiusVarEnabled = 0
PseudocolorAtts.endPointRadiusVar = ""
PseudocolorAtts.endPointRadiusVarRatio = 10
PseudocolorAtts.renderSurfaces = 1
PseudocolorAtts.renderWireframe = 0
PseudocolorAtts.renderPoints = 0
PseudocolorAtts.smoothingLevel = 0
PseudocolorAtts.legendFlag = 1
PseudocolorAtts.lightingFlag = 1
PseudocolorAtts.wireframeColor = (0, 0, 0, 0)
PseudocolorAtts.pointColor = (0, 0, 0, 0)
SetPlotOptions(PseudocolorAtts)
SetActiveWindow(2)
SetActiveWindow(2)
PseudocolorAtts = PseudocolorAttributes()
PseudocolorAtts.scaling = PseudocolorAtts.Linear  # Linear, Log, Skew
PseudocolorAtts.skewFactor = 1
PseudocolorAtts.limitsMode = PseudocolorAtts.OriginalData  # OriginalData, CurrentPlot
PseudocolorAtts.minFlag = 1
PseudocolorAtts.min = -0.2
PseudocolorAtts.maxFlag = 1
PseudocolorAtts.max = 0.2
PseudocolorAtts.centering = PseudocolorAtts.Natural  # Natural, Nodal, Zonal
PseudocolorAtts.colorTableName = "RdBu"
PseudocolorAtts.invertColorTable = 1
PseudocolorAtts.opacityType = PseudocolorAtts.FullyOpaque  # ColorTable, FullyOpaque, Constant, Ramp, VariableRange
PseudocolorAtts.opacityVariable = ""
PseudocolorAtts.opacity = 1
PseudocolorAtts.opacityVarMin = 0
PseudocolorAtts.opacityVarMax = 1
PseudocolorAtts.opacityVarMinFlag = 0
PseudocolorAtts.opacityVarMaxFlag = 0
PseudocolorAtts.pointSize = 0.05
PseudocolorAtts.pointType = PseudocolorAtts.Point  # Box, Axis, Icosahedron, Octahedron, Tetrahedron, SphereGeometry, Point, Sphere
PseudocolorAtts.pointSizeVarEnabled = 0
PseudocolorAtts.pointSizeVar = "default"
PseudocolorAtts.pointSizePixels = 2
PseudocolorAtts.lineStyle = PseudocolorAtts.SOLID  # SOLID, DASH, DOT, DOTDASH
PseudocolorAtts.lineType = PseudocolorAtts.Line  # Line, Tube, Ribbon
PseudocolorAtts.lineWidth = 0
PseudocolorAtts.tubeResolution = 10
PseudocolorAtts.tubeRadiusSizeType = PseudocolorAtts.FractionOfBBox  # Absolute, FractionOfBBox
PseudocolorAtts.tubeRadiusAbsolute = 0.125
PseudocolorAtts.tubeRadiusBBox = 0.005
PseudocolorAtts.tubeRadiusVarEnabled = 0
PseudocolorAtts.tubeRadiusVar = ""
PseudocolorAtts.tubeRadiusVarRatio = 10
PseudocolorAtts.tailStyle = PseudocolorAtts.None  # None, Spheres, Cones
PseudocolorAtts.headStyle = PseudocolorAtts.None  # None, Spheres, Cones
PseudocolorAtts.endPointRadiusSizeType = PseudocolorAtts.FractionOfBBox  # Absolute, FractionOfBBox
PseudocolorAtts.endPointRadiusAbsolute = 0.125
PseudocolorAtts.endPointRadiusBBox = 0.05
PseudocolorAtts.endPointResolution = 10
PseudocolorAtts.endPointRatio = 5
PseudocolorAtts.endPointRadiusVarEnabled = 0
PseudocolorAtts.endPointRadiusVar = ""
PseudocolorAtts.endPointRadiusVarRatio = 10
PseudocolorAtts.renderSurfaces = 1
PseudocolorAtts.renderWireframe = 0
PseudocolorAtts.renderPoints = 0
PseudocolorAtts.smoothingLevel = 0
PseudocolorAtts.legendFlag = 1
PseudocolorAtts.lightingFlag = 1
PseudocolorAtts.wireframeColor = (0, 0, 0, 0)
PseudocolorAtts.pointColor = (0, 0, 0, 0)
SetPlotOptions(PseudocolorAtts)
PseudocolorAtts = PseudocolorAttributes()
PseudocolorAtts.scaling = PseudocolorAtts.Linear  # Linear, Log, Skew
PseudocolorAtts.skewFactor = 1
PseudocolorAtts.limitsMode = PseudocolorAtts.OriginalData  # OriginalData, CurrentPlot
PseudocolorAtts.minFlag = 1
PseudocolorAtts.min = -1
PseudocolorAtts.maxFlag = 1
PseudocolorAtts.max = 1
PseudocolorAtts.centering = PseudocolorAtts.Natural  # Natural, Nodal, Zonal
PseudocolorAtts.colorTableName = "RdBu"
PseudocolorAtts.invertColorTable = 1
PseudocolorAtts.opacityType = PseudocolorAtts.FullyOpaque  # ColorTable, FullyOpaque, Constant, Ramp, VariableRange
PseudocolorAtts.opacityVariable = ""
PseudocolorAtts.opacity = 1
PseudocolorAtts.opacityVarMin = 0
PseudocolorAtts.opacityVarMax = 1
PseudocolorAtts.opacityVarMinFlag = 0
PseudocolorAtts.opacityVarMaxFlag = 0
PseudocolorAtts.pointSize = 0.05
PseudocolorAtts.pointType = PseudocolorAtts.Point  # Box, Axis, Icosahedron, Octahedron, Tetrahedron, SphereGeometry, Point, Sphere
PseudocolorAtts.pointSizeVarEnabled = 0
PseudocolorAtts.pointSizeVar = "default"
PseudocolorAtts.pointSizePixels = 2
PseudocolorAtts.lineStyle = PseudocolorAtts.SOLID  # SOLID, DASH, DOT, DOTDASH
PseudocolorAtts.lineType = PseudocolorAtts.Line  # Line, Tube, Ribbon
PseudocolorAtts.lineWidth = 0
PseudocolorAtts.tubeResolution = 10
PseudocolorAtts.tubeRadiusSizeType = PseudocolorAtts.FractionOfBBox  # Absolute, FractionOfBBox
PseudocolorAtts.tubeRadiusAbsolute = 0.125
PseudocolorAtts.tubeRadiusBBox = 0.005
PseudocolorAtts.tubeRadiusVarEnabled = 0
PseudocolorAtts.tubeRadiusVar = ""
PseudocolorAtts.tubeRadiusVarRatio = 10
PseudocolorAtts.tailStyle = PseudocolorAtts.None  # None, Spheres, Cones
PseudocolorAtts.headStyle = PseudocolorAtts.None  # None, Spheres, Cones
PseudocolorAtts.endPointRadiusSizeType = PseudocolorAtts.FractionOfBBox  # Absolute, FractionOfBBox
PseudocolorAtts.endPointRadiusAbsolute = 0.125
PseudocolorAtts.endPointRadiusBBox = 0.05
PseudocolorAtts.endPointResolution = 10
PseudocolorAtts.endPointRatio = 5
PseudocolorAtts.endPointRadiusVarEnabled = 0
PseudocolorAtts.endPointRadiusVar = ""
PseudocolorAtts.endPointRadiusVarRatio = 10
PseudocolorAtts.renderSurfaces = 1
PseudocolorAtts.renderWireframe = 0
PseudocolorAtts.renderPoints = 0
PseudocolorAtts.smoothingLevel = 0
PseudocolorAtts.legendFlag = 1
PseudocolorAtts.lightingFlag = 1
PseudocolorAtts.wireframeColor = (0, 0, 0, 0)
PseudocolorAtts.pointColor = (0, 0, 0, 0)
SetPlotOptions(PseudocolorAtts)
PseudocolorAtts = PseudocolorAttributes()
PseudocolorAtts.scaling = PseudocolorAtts.Linear  # Linear, Log, Skew
PseudocolorAtts.skewFactor = 1
PseudocolorAtts.limitsMode = PseudocolorAtts.OriginalData  # OriginalData, CurrentPlot
PseudocolorAtts.minFlag = 1
PseudocolorAtts.min = -1
PseudocolorAtts.maxFlag = 1
PseudocolorAtts.max = 1
PseudocolorAtts.centering = PseudocolorAtts.Natural  # Natural, Nodal, Zonal
PseudocolorAtts.colorTableName = "RdBu"
PseudocolorAtts.invertColorTable = 1
PseudocolorAtts.opacityType = PseudocolorAtts.FullyOpaque  # ColorTable, FullyOpaque, Constant, Ramp, VariableRange
PseudocolorAtts.opacityVariable = ""
PseudocolorAtts.opacity = 1
PseudocolorAtts.opacityVarMin = 0
PseudocolorAtts.opacityVarMax = 1
PseudocolorAtts.opacityVarMinFlag = 0
PseudocolorAtts.opacityVarMaxFlag = 0
PseudocolorAtts.pointSize = 0.05
PseudocolorAtts.pointType = PseudocolorAtts.Point  # Box, Axis, Icosahedron, Octahedron, Tetrahedron, SphereGeometry, Point, Sphere
PseudocolorAtts.pointSizeVarEnabled = 0
PseudocolorAtts.pointSizeVar = "default"
PseudocolorAtts.pointSizePixels = 2
PseudocolorAtts.lineStyle = PseudocolorAtts.SOLID  # SOLID, DASH, DOT, DOTDASH
PseudocolorAtts.lineType = PseudocolorAtts.Line  # Line, Tube, Ribbon
PseudocolorAtts.lineWidth = 0
PseudocolorAtts.tubeResolution = 10
PseudocolorAtts.tubeRadiusSizeType = PseudocolorAtts.FractionOfBBox  # Absolute, FractionOfBBox
PseudocolorAtts.tubeRadiusAbsolute = 0.125
PseudocolorAtts.tubeRadiusBBox = 0.005
PseudocolorAtts.tubeRadiusVarEnabled = 0
PseudocolorAtts.tubeRadiusVar = ""
PseudocolorAtts.tubeRadiusVarRatio = 10
PseudocolorAtts.tailStyle = PseudocolorAtts.None  # None, Spheres, Cones
PseudocolorAtts.headStyle = PseudocolorAtts.None  # None, Spheres, Cones
PseudocolorAtts.endPointRadiusSizeType = PseudocolorAtts.FractionOfBBox  # Absolute, FractionOfBBox
PseudocolorAtts.endPointRadiusAbsolute = 0.125
PseudocolorAtts.endPointRadiusBBox = 0.05
PseudocolorAtts.endPointResolution = 10
PseudocolorAtts.endPointRatio = 5
PseudocolorAtts.endPointRadiusVarEnabled = 0
PseudocolorAtts.endPointRadiusVar = ""
PseudocolorAtts.endPointRadiusVarRatio = 10
PseudocolorAtts.renderSurfaces = 1
PseudocolorAtts.renderWireframe = 0
PseudocolorAtts.renderPoints = 0
PseudocolorAtts.smoothingLevel = 0
PseudocolorAtts.legendFlag = 1
PseudocolorAtts.lightingFlag = 1
PseudocolorAtts.wireframeColor = (0, 0, 0, 0)
PseudocolorAtts.pointColor = (0, 0, 0, 0)
SetPlotOptions(PseudocolorAtts)
SetActivePlots((0, 1))
SetActivePlots(1)
# Begin spontaneous state
View2DAtts = View2DAttributes()
View2DAtts.windowCoords = (306, 717, 306, 717)
View2DAtts.viewportCoords = (0.2, 0.95, 0.15, 0.95)
View2DAtts.fullFrameActivationMode = View2DAtts.Auto  # On, Off, Auto
View2DAtts.fullFrameAutoThreshold = 100
View2DAtts.xScale = View2DAtts.LINEAR  # LINEAR, LOG
View2DAtts.yScale = View2DAtts.LINEAR  # LINEAR, LOG
View2DAtts.windowValid = 1
SetView2D(View2DAtts)
# End spontaneous state

SetActivePlots((1, 3))
SetActivePlots(3)
PseudocolorAtts = PseudocolorAttributes()
PseudocolorAtts.scaling = PseudocolorAtts.Linear  # Linear, Log, Skew
PseudocolorAtts.skewFactor = 1
PseudocolorAtts.limitsMode = PseudocolorAtts.OriginalData  # OriginalData, CurrentPlot
PseudocolorAtts.minFlag = 1
PseudocolorAtts.min = -1
PseudocolorAtts.maxFlag = 1
PseudocolorAtts.max = 1
PseudocolorAtts.centering = PseudocolorAtts.Natural  # Natural, Nodal, Zonal
PseudocolorAtts.colorTableName = "PuOr"
PseudocolorAtts.invertColorTable = 1
PseudocolorAtts.opacityType = PseudocolorAtts.FullyOpaque  # ColorTable, FullyOpaque, Constant, Ramp, VariableRange
PseudocolorAtts.opacityVariable = ""
PseudocolorAtts.opacity = 1
PseudocolorAtts.opacityVarMin = 0
PseudocolorAtts.opacityVarMax = 1
PseudocolorAtts.opacityVarMinFlag = 0
PseudocolorAtts.opacityVarMaxFlag = 0
PseudocolorAtts.pointSize = 0.05
PseudocolorAtts.pointType = PseudocolorAtts.Point  # Box, Axis, Icosahedron, Octahedron, Tetrahedron, SphereGeometry, Point, Sphere
PseudocolorAtts.pointSizeVarEnabled = 0
PseudocolorAtts.pointSizeVar = "default"
PseudocolorAtts.pointSizePixels = 2
PseudocolorAtts.lineStyle = PseudocolorAtts.SOLID  # SOLID, DASH, DOT, DOTDASH
PseudocolorAtts.lineType = PseudocolorAtts.Line  # Line, Tube, Ribbon
PseudocolorAtts.lineWidth = 0
PseudocolorAtts.tubeResolution = 10
PseudocolorAtts.tubeRadiusSizeType = PseudocolorAtts.FractionOfBBox  # Absolute, FractionOfBBox
PseudocolorAtts.tubeRadiusAbsolute = 0.125
PseudocolorAtts.tubeRadiusBBox = 0.005
PseudocolorAtts.tubeRadiusVarEnabled = 0
PseudocolorAtts.tubeRadiusVar = ""
PseudocolorAtts.tubeRadiusVarRatio = 10
PseudocolorAtts.tailStyle = PseudocolorAtts.None  # None, Spheres, Cones
PseudocolorAtts.headStyle = PseudocolorAtts.None  # None, Spheres, Cones
PseudocolorAtts.endPointRadiusSizeType = PseudocolorAtts.FractionOfBBox  # Absolute, FractionOfBBox
PseudocolorAtts.endPointRadiusAbsolute = 0.125
PseudocolorAtts.endPointRadiusBBox = 0.05
PseudocolorAtts.endPointResolution = 10
PseudocolorAtts.endPointRatio = 5
PseudocolorAtts.endPointRadiusVarEnabled = 0
PseudocolorAtts.endPointRadiusVar = ""
PseudocolorAtts.endPointRadiusVarRatio = 10
PseudocolorAtts.renderSurfaces = 1
PseudocolorAtts.renderWireframe = 0
PseudocolorAtts.renderPoints = 0
PseudocolorAtts.smoothingLevel = 0
PseudocolorAtts.legendFlag = 1
PseudocolorAtts.lightingFlag = 1
PseudocolorAtts.wireframeColor = (0, 0, 0, 0)
PseudocolorAtts.pointColor = (0, 0, 0, 0)
SetPlotOptions(PseudocolorAtts)
# Begin spontaneous state
View2DAtts = View2DAttributes()
View2DAtts.windowCoords = (406, 617, 406, 617)
View2DAtts.viewportCoords = (0.2, 0.95, 0.15, 0.95)
View2DAtts.fullFrameActivationMode = View2DAtts.Auto  # On, Off, Auto
View2DAtts.fullFrameAutoThreshold = 100
View2DAtts.xScale = View2DAtts.LINEAR  # LINEAR, LOG
View2DAtts.yScale = View2DAtts.LINEAR  # LINEAR, LOG
View2DAtts.windowValid = 1
SetView2D(View2DAtts)
# End spontaneous state

ViewCurveAtts = ViewCurveAttributes()
ViewCurveAtts.domainCoords = (0, 1)
ViewCurveAtts.rangeCoords = (0, 1)
ViewCurveAtts.viewportCoords = (0.2, 0.95, 0.15, 0.95)
ViewCurveAtts.domainScale = ViewCurveAtts.LINEAR  # LINEAR, LOG
ViewCurveAtts.rangeScale = ViewCurveAtts.LINEAR  # LINEAR, LOG
SetViewCurve(ViewCurveAtts)
View2DAtts = View2DAttributes()
View2DAtts.windowCoords = (406, 617, 406, 617)
View2DAtts.viewportCoords = (0.2, 0.95, 0.15, 0.95)
View2DAtts.fullFrameActivationMode = View2DAtts.Auto  # On, Off, Auto
View2DAtts.fullFrameAutoThreshold = 100
View2DAtts.xScale = View2DAtts.LINEAR  # LINEAR, LOG
View2DAtts.yScale = View2DAtts.LINEAR  # LINEAR, LOG
View2DAtts.windowValid = 1
SetView2D(View2DAtts)
View3DAtts = View3DAttributes()
View3DAtts.viewNormal = (0, 0, 1)
View3DAtts.focus = (512, 512, 256)
View3DAtts.viewUp = (0, 1, 0)
View3DAtts.viewAngle = 30
View3DAtts.parallelScale = 768
View3DAtts.nearPlane = -1536
View3DAtts.farPlane = 1536
View3DAtts.imagePan = (0, 0)
View3DAtts.imageZoom = 1
View3DAtts.perspective = 1
View3DAtts.eyeAngle = 2
View3DAtts.centerOfRotationSet = 0
View3DAtts.centerOfRotation = (512, 512, 256)
View3DAtts.axis3DScaleFlag = 0
View3DAtts.axis3DScales = (1, 1, 1)
View3DAtts.shear = (0, 0, 1)
View3DAtts.windowValid = 1
SetView3D(View3DAtts)
ViewAxisArrayAtts = ViewAxisArrayAttributes()
ViewAxisArrayAtts.domainCoords = (0, 1)
ViewAxisArrayAtts.rangeCoords = (0, 1)
ViewAxisArrayAtts.viewportCoords = (0.15, 0.9, 0.1, 0.85)
SetViewAxisArray(ViewAxisArrayAtts)
SetActiveWindow(1)
SetActiveWindow(1)
# Begin spontaneous state
View2DAtts = View2DAttributes()
View2DAtts.windowCoords = (406, 617, 406, 617)
View2DAtts.viewportCoords = (0.2, 0.95, 0.15, 0.95)
View2DAtts.fullFrameActivationMode = View2DAtts.Auto  # On, Off, Auto
View2DAtts.fullFrameAutoThreshold = 100
View2DAtts.xScale = View2DAtts.LINEAR  # LINEAR, LOG
View2DAtts.yScale = View2DAtts.LINEAR  # LINEAR, LOG
View2DAtts.windowValid = 1
SetView2D(View2DAtts)
# End spontaneous state

ViewCurveAtts = ViewCurveAttributes()
ViewCurveAtts.domainCoords = (0, 1)
ViewCurveAtts.rangeCoords = (0, 1)
ViewCurveAtts.viewportCoords = (0.2, 0.95, 0.15, 0.95)
ViewCurveAtts.domainScale = ViewCurveAtts.LINEAR  # LINEAR, LOG
ViewCurveAtts.rangeScale = ViewCurveAtts.LINEAR  # LINEAR, LOG
SetViewCurve(ViewCurveAtts)
View2DAtts = View2DAttributes()
View2DAtts.windowCoords = (406, 617, 406, 617)
View2DAtts.viewportCoords = (0.2, 0.95, 0.15, 0.95)
View2DAtts.fullFrameActivationMode = View2DAtts.Auto  # On, Off, Auto
View2DAtts.fullFrameAutoThreshold = 100
View2DAtts.xScale = View2DAtts.LINEAR  # LINEAR, LOG
View2DAtts.yScale = View2DAtts.LINEAR  # LINEAR, LOG
View2DAtts.windowValid = 1
SetView2D(View2DAtts)
View3DAtts = View3DAttributes()
View3DAtts.viewNormal = (0, 0, 1)
View3DAtts.focus = (512, 512, 256)
View3DAtts.viewUp = (0, 1, 0)
View3DAtts.viewAngle = 30
View3DAtts.parallelScale = 768
View3DAtts.nearPlane = -1536
View3DAtts.farPlane = 1536
View3DAtts.imagePan = (0, 0)
View3DAtts.imageZoom = 1
View3DAtts.perspective = 1
View3DAtts.eyeAngle = 2
View3DAtts.centerOfRotationSet = 0
View3DAtts.centerOfRotation = (512, 512, 256)
View3DAtts.axis3DScaleFlag = 0
View3DAtts.axis3DScales = (1, 1, 1)
View3DAtts.shear = (0, 0, 1)
View3DAtts.windowValid = 1
SetView3D(View3DAtts)
ViewAxisArrayAtts = ViewAxisArrayAttributes()
ViewAxisArrayAtts.domainCoords = (0, 1)
ViewAxisArrayAtts.rangeCoords = (0, 1)
ViewAxisArrayAtts.viewportCoords = (0.15, 0.9, 0.1, 0.85)
SetViewAxisArray(ViewAxisArrayAtts)
# MAINTENANCE ISSUE: SetSuppressMessagesRPC is not handled in Logging.C. Please contact a VisIt developer.
SaveSession("/Users/Jamie/.visit/crash_recovery.4536.session")
# MAINTENANCE ISSUE: SetSuppressMessagesRPC is not handled in Logging.C. Please contact a VisIt developer.
# Begin spontaneous state
View2DAtts = View2DAttributes()
View2DAtts.windowCoords = (456, 567, 456, 567)
View2DAtts.viewportCoords = (0.2, 0.95, 0.15, 0.95)
View2DAtts.fullFrameActivationMode = View2DAtts.Auto  # On, Off, Auto
View2DAtts.fullFrameAutoThreshold = 100
View2DAtts.xScale = View2DAtts.LINEAR  # LINEAR, LOG
View2DAtts.yScale = View2DAtts.LINEAR  # LINEAR, LOG
View2DAtts.windowValid = 1
SetView2D(View2DAtts)
# End spontaneous state

ViewCurveAtts = ViewCurveAttributes()
ViewCurveAtts.domainCoords = (0, 1)
ViewCurveAtts.rangeCoords = (0, 1)
ViewCurveAtts.viewportCoords = (0.2, 0.95, 0.15, 0.95)
ViewCurveAtts.domainScale = ViewCurveAtts.LINEAR  # LINEAR, LOG
ViewCurveAtts.rangeScale = ViewCurveAtts.LINEAR  # LINEAR, LOG
SetViewCurve(ViewCurveAtts)
View2DAtts = View2DAttributes()
View2DAtts.windowCoords = (456, 567, 456, 567)
View2DAtts.viewportCoords = (0.2, 0.95, 0.15, 0.95)
View2DAtts.fullFrameActivationMode = View2DAtts.Auto  # On, Off, Auto
View2DAtts.fullFrameAutoThreshold = 100
View2DAtts.xScale = View2DAtts.LINEAR  # LINEAR, LOG
View2DAtts.yScale = View2DAtts.LINEAR  # LINEAR, LOG
View2DAtts.windowValid = 1
SetView2D(View2DAtts)
View3DAtts = View3DAttributes()
View3DAtts.viewNormal = (0, 0, 1)
View3DAtts.focus = (512, 512, 256)
View3DAtts.viewUp = (0, 1, 0)
View3DAtts.viewAngle = 30
View3DAtts.parallelScale = 768
View3DAtts.nearPlane = -1536
View3DAtts.farPlane = 1536
View3DAtts.imagePan = (0, 0)
View3DAtts.imageZoom = 1
View3DAtts.perspective = 1
View3DAtts.eyeAngle = 2
View3DAtts.centerOfRotationSet = 0
View3DAtts.centerOfRotation = (512, 512, 256)
View3DAtts.axis3DScaleFlag = 0
View3DAtts.axis3DScales = (1, 1, 1)
View3DAtts.shear = (0, 0, 1)
View3DAtts.windowValid = 1
SetView3D(View3DAtts)
ViewAxisArrayAtts = ViewAxisArrayAttributes()
ViewAxisArrayAtts.domainCoords = (0, 1)
ViewAxisArrayAtts.rangeCoords = (0, 1)
ViewAxisArrayAtts.viewportCoords = (0.15, 0.9, 0.1, 0.85)
SetViewAxisArray(ViewAxisArrayAtts)
SetActiveWindow(2)
SetActiveWindow(2)
# Begin spontaneous state
View2DAtts = View2DAttributes()
View2DAtts.windowCoords = (456, 567, 456, 567)
View2DAtts.viewportCoords = (0.2, 0.95, 0.15, 0.95)
View2DAtts.fullFrameActivationMode = View2DAtts.Auto  # On, Off, Auto
View2DAtts.fullFrameAutoThreshold = 100
View2DAtts.xScale = View2DAtts.LINEAR  # LINEAR, LOG
View2DAtts.yScale = View2DAtts.LINEAR  # LINEAR, LOG
View2DAtts.windowValid = 1
SetView2D(View2DAtts)
# End spontaneous state

ViewCurveAtts = ViewCurveAttributes()
ViewCurveAtts.domainCoords = (0, 1)
ViewCurveAtts.rangeCoords = (0, 1)
ViewCurveAtts.viewportCoords = (0.2, 0.95, 0.15, 0.95)
ViewCurveAtts.domainScale = ViewCurveAtts.LINEAR  # LINEAR, LOG
ViewCurveAtts.rangeScale = ViewCurveAtts.LINEAR  # LINEAR, LOG
SetViewCurve(ViewCurveAtts)
View2DAtts = View2DAttributes()
View2DAtts.windowCoords = (456, 567, 456, 567)
View2DAtts.viewportCoords = (0.2, 0.95, 0.15, 0.95)
View2DAtts.fullFrameActivationMode = View2DAtts.Auto  # On, Off, Auto
View2DAtts.fullFrameAutoThreshold = 100
View2DAtts.xScale = View2DAtts.LINEAR  # LINEAR, LOG
View2DAtts.yScale = View2DAtts.LINEAR  # LINEAR, LOG
View2DAtts.windowValid = 1
SetView2D(View2DAtts)
View3DAtts = View3DAttributes()
View3DAtts.viewNormal = (0, 0, 1)
View3DAtts.focus = (512, 512, 256)
View3DAtts.viewUp = (0, 1, 0)
View3DAtts.viewAngle = 30
View3DAtts.parallelScale = 768
View3DAtts.nearPlane = -1536
View3DAtts.farPlane = 1536
View3DAtts.imagePan = (0, 0)
View3DAtts.imageZoom = 1
View3DAtts.perspective = 1
View3DAtts.eyeAngle = 2
View3DAtts.centerOfRotationSet = 0
View3DAtts.centerOfRotation = (512, 512, 256)
View3DAtts.axis3DScaleFlag = 0
View3DAtts.axis3DScales = (1, 1, 1)
View3DAtts.shear = (0, 0, 1)
View3DAtts.windowValid = 1
SetView3D(View3DAtts)
ViewAxisArrayAtts = ViewAxisArrayAttributes()
ViewAxisArrayAtts.domainCoords = (0, 1)
ViewAxisArrayAtts.rangeCoords = (0, 1)
ViewAxisArrayAtts.viewportCoords = (0.15, 0.9, 0.1, 0.85)
SetViewAxisArray(ViewAxisArrayAtts)
# Begin spontaneous state
View2DAtts = View2DAttributes()
View2DAtts.windowCoords = (456, 568, 456, 568)
View2DAtts.viewportCoords = (0.2, 0.95, 0.15, 0.95)
View2DAtts.fullFrameActivationMode = View2DAtts.Auto  # On, Off, Auto
View2DAtts.fullFrameAutoThreshold = 100
View2DAtts.xScale = View2DAtts.LINEAR  # LINEAR, LOG
View2DAtts.yScale = View2DAtts.LINEAR  # LINEAR, LOG
View2DAtts.windowValid = 1
SetView2D(View2DAtts)
# End spontaneous state

ViewCurveAtts = ViewCurveAttributes()
ViewCurveAtts.domainCoords = (0, 1)
ViewCurveAtts.rangeCoords = (0, 1)
ViewCurveAtts.viewportCoords = (0.2, 0.95, 0.15, 0.95)
ViewCurveAtts.domainScale = ViewCurveAtts.LINEAR  # LINEAR, LOG
ViewCurveAtts.rangeScale = ViewCurveAtts.LINEAR  # LINEAR, LOG
SetViewCurve(ViewCurveAtts)
View2DAtts = View2DAttributes()
View2DAtts.windowCoords = (456, 568, 456, 568)
View2DAtts.viewportCoords = (0.2, 0.95, 0.15, 0.95)
View2DAtts.fullFrameActivationMode = View2DAtts.Auto  # On, Off, Auto
View2DAtts.fullFrameAutoThreshold = 100
View2DAtts.xScale = View2DAtts.LINEAR  # LINEAR, LOG
View2DAtts.yScale = View2DAtts.LINEAR  # LINEAR, LOG
View2DAtts.windowValid = 1
SetView2D(View2DAtts)
View3DAtts = View3DAttributes()
View3DAtts.viewNormal = (0, 0, 1)
View3DAtts.focus = (512, 512, 256)
View3DAtts.viewUp = (0, 1, 0)
View3DAtts.viewAngle = 30
View3DAtts.parallelScale = 768
View3DAtts.nearPlane = -1536
View3DAtts.farPlane = 1536
View3DAtts.imagePan = (0, 0)
View3DAtts.imageZoom = 1
View3DAtts.perspective = 1
View3DAtts.eyeAngle = 2
View3DAtts.centerOfRotationSet = 0
View3DAtts.centerOfRotation = (512, 512, 256)
View3DAtts.axis3DScaleFlag = 0
View3DAtts.axis3DScales = (1, 1, 1)
View3DAtts.shear = (0, 0, 1)
View3DAtts.windowValid = 1
SetView3D(View3DAtts)
ViewAxisArrayAtts = ViewAxisArrayAttributes()
ViewAxisArrayAtts.domainCoords = (0, 1)
ViewAxisArrayAtts.rangeCoords = (0, 1)
ViewAxisArrayAtts.viewportCoords = (0.15, 0.9, 0.1, 0.85)
SetViewAxisArray(ViewAxisArrayAtts)
SetActiveWindow(1)
SetActiveWindow(1)
# Begin spontaneous state
View2DAtts = View2DAttributes()
View2DAtts.windowCoords = (456, 568, 456, 568)
View2DAtts.viewportCoords = (0.2, 0.95, 0.15, 0.95)
View2DAtts.fullFrameActivationMode = View2DAtts.Auto  # On, Off, Auto
View2DAtts.fullFrameAutoThreshold = 100
View2DAtts.xScale = View2DAtts.LINEAR  # LINEAR, LOG
View2DAtts.yScale = View2DAtts.LINEAR  # LINEAR, LOG
View2DAtts.windowValid = 1
SetView2D(View2DAtts)
# End spontaneous state

ViewCurveAtts = ViewCurveAttributes()
ViewCurveAtts.domainCoords = (0, 1)
ViewCurveAtts.rangeCoords = (0, 1)
ViewCurveAtts.viewportCoords = (0.2, 0.95, 0.15, 0.95)
ViewCurveAtts.domainScale = ViewCurveAtts.LINEAR  # LINEAR, LOG
ViewCurveAtts.rangeScale = ViewCurveAtts.LINEAR  # LINEAR, LOG
SetViewCurve(ViewCurveAtts)
View2DAtts = View2DAttributes()
View2DAtts.windowCoords = (456, 568, 456, 568)
View2DAtts.viewportCoords = (0.2, 0.95, 0.15, 0.95)
View2DAtts.fullFrameActivationMode = View2DAtts.Auto  # On, Off, Auto
View2DAtts.fullFrameAutoThreshold = 100
View2DAtts.xScale = View2DAtts.LINEAR  # LINEAR, LOG
View2DAtts.yScale = View2DAtts.LINEAR  # LINEAR, LOG
View2DAtts.windowValid = 1
SetView2D(View2DAtts)
View3DAtts = View3DAttributes()
View3DAtts.viewNormal = (0, 0, 1)
View3DAtts.focus = (512, 512, 256)
View3DAtts.viewUp = (0, 1, 0)
View3DAtts.viewAngle = 30
View3DAtts.parallelScale = 768
View3DAtts.nearPlane = -1536
View3DAtts.farPlane = 1536
View3DAtts.imagePan = (0, 0)
View3DAtts.imageZoom = 1
View3DAtts.perspective = 1
View3DAtts.eyeAngle = 2
View3DAtts.centerOfRotationSet = 0
View3DAtts.centerOfRotation = (512, 512, 256)
View3DAtts.axis3DScaleFlag = 0
View3DAtts.axis3DScales = (1, 1, 1)
View3DAtts.shear = (0, 0, 1)
View3DAtts.windowValid = 1
SetView3D(View3DAtts)
ViewAxisArrayAtts = ViewAxisArrayAttributes()
ViewAxisArrayAtts.domainCoords = (0, 1)
ViewAxisArrayAtts.rangeCoords = (0, 1)
ViewAxisArrayAtts.viewportCoords = (0.15, 0.9, 0.1, 0.85)
SetViewAxisArray(ViewAxisArrayAtts)
# MAINTENANCE ISSUE: SetSuppressMessagesRPC is not handled in Logging.C. Please contact a VisIt developer.
SaveSession("/Users/Jamie/.visit/crash_recovery.4536.session")
# MAINTENANCE ISSUE: SetSuppressMessagesRPC is not handled in Logging.C. Please contact a VisIt developer.
# Begin spontaneous state
View2DAtts = View2DAttributes()
View2DAtts.windowCoords = (456, 568, 456, 568)
View2DAtts.viewportCoords = (0.2, 0.95, 0.15, 0.95)
View2DAtts.fullFrameActivationMode = View2DAtts.Auto  # On, Off, Auto
View2DAtts.fullFrameAutoThreshold = 100
View2DAtts.xScale = View2DAtts.LINEAR  # LINEAR, LOG
View2DAtts.yScale = View2DAtts.LINEAR  # LINEAR, LOG
View2DAtts.windowValid = 1
SetView2D(View2DAtts)
# End spontaneous state

SetActivePlots((0, 1))
SetActivePlots(0)
SetActivePlots(0)
SetActivePlots(0)
SetActivePlots(0)
SetActivePlots(0)
SetActivePlots((0, 1))
SetActivePlots((0, 1))
SetActivePlots(1)
SetActivePlots(1)
SetActivePlots(1)
SetActivePlots(1)
SetActivePlots(1)
SetActivePlots(1)
AddOperator("Elevate", 1)
DrawPlots()
# Begin spontaneous state
View3DAtts = View3DAttributes()
View3DAtts.viewNormal = (0, 0, 1)
View3DAtts.focus = (512, 512, 5.55112e-17)
View3DAtts.viewUp = (0, 1, 0)
View3DAtts.viewAngle = 30
View3DAtts.parallelScale = 724.078
View3DAtts.nearPlane = -1448.16
View3DAtts.farPlane = 1448.16
View3DAtts.imagePan = (0, 0)
View3DAtts.imageZoom = 1
View3DAtts.perspective = 1
View3DAtts.eyeAngle = 2
View3DAtts.centerOfRotationSet = 0
View3DAtts.centerOfRotation = (512, 512, 5.55112e-17)
View3DAtts.axis3DScaleFlag = 0
View3DAtts.axis3DScales = (1, 1, 1)
View3DAtts.shear = (0, 0, 1)
View3DAtts.windowValid = 1
SetView3D(View3DAtts)
# End spontaneous state

# Begin spontaneous state
View3DAtts = View3DAttributes()
View3DAtts.viewNormal = (-0.224409, -0.808096, 0.54463)
View3DAtts.focus = (512, 512, 5.55112e-17)
View3DAtts.viewUp = (0.0555088, 0.547377, 0.835043)
View3DAtts.viewAngle = 30
View3DAtts.parallelScale = 724.078
View3DAtts.nearPlane = -1448.16
View3DAtts.farPlane = 1448.16
View3DAtts.imagePan = (0, 0)
View3DAtts.imageZoom = 1
View3DAtts.perspective = 1
View3DAtts.eyeAngle = 2
View3DAtts.centerOfRotationSet = 0
View3DAtts.centerOfRotation = (512, 512, 5.55112e-17)
View3DAtts.axis3DScaleFlag = 0
View3DAtts.axis3DScales = (1, 1, 1)
View3DAtts.shear = (0, 0, 1)
View3DAtts.windowValid = 1
SetView3D(View3DAtts)
# End spontaneous state

# MAINTENANCE ISSUE: SetSuppressMessagesRPC is not handled in Logging.C. Please contact a VisIt developer.
SaveSession("/Users/Jamie/.visit/crash_recovery.4536.session")
# MAINTENANCE ISSUE: SetSuppressMessagesRPC is not handled in Logging.C. Please contact a VisIt developer.
# Begin spontaneous state
View3DAtts = View3DAttributes()
View3DAtts.viewNormal = (-0.224409, -0.808096, 0.54463)
View3DAtts.focus = (512, 512, 5.55112e-17)
View3DAtts.viewUp = (0.0555088, 0.547377, 0.835043)
View3DAtts.viewAngle = 30
View3DAtts.parallelScale = 724.078
View3DAtts.nearPlane = -1448.16
View3DAtts.farPlane = 1448.16
View3DAtts.imagePan = (0, 0)
View3DAtts.imageZoom = 0.826446
View3DAtts.perspective = 1
View3DAtts.eyeAngle = 2
View3DAtts.centerOfRotationSet = 0
View3DAtts.centerOfRotation = (512, 512, 5.55112e-17)
View3DAtts.axis3DScaleFlag = 0
View3DAtts.axis3DScales = (1, 1, 1)
View3DAtts.shear = (0, 0, 1)
View3DAtts.windowValid = 1
SetView3D(View3DAtts)
# End spontaneous state

# Begin spontaneous state
View3DAtts = View3DAttributes()
View3DAtts.viewNormal = (-0.224409, -0.808096, 0.54463)
View3DAtts.focus = (512, 512, 5.55112e-17)
View3DAtts.viewUp = (0.0555088, 0.547377, 0.835043)
View3DAtts.viewAngle = 30
View3DAtts.parallelScale = 724.078
View3DAtts.nearPlane = -1448.16
View3DAtts.farPlane = 1448.16
View3DAtts.imagePan = (0, 0)
View3DAtts.imageZoom = 0.683013
View3DAtts.perspective = 1
View3DAtts.eyeAngle = 2
View3DAtts.centerOfRotationSet = 0
View3DAtts.centerOfRotation = (512, 512, 5.55112e-17)
View3DAtts.axis3DScaleFlag = 0
View3DAtts.axis3DScales = (1, 1, 1)
View3DAtts.shear = (0, 0, 1)
View3DAtts.windowValid = 1
SetView3D(View3DAtts)
# End spontaneous state

# Begin spontaneous state
View3DAtts = View3DAttributes()
View3DAtts.viewNormal = (-0.224409, -0.808096, 0.54463)
View3DAtts.focus = (512, 512, 5.55112e-17)
View3DAtts.viewUp = (0.0555088, 0.547377, 0.835043)
View3DAtts.viewAngle = 30
View3DAtts.parallelScale = 724.078
View3DAtts.nearPlane = -1448.16
View3DAtts.farPlane = 1448.16
View3DAtts.imagePan = (0, 0)
View3DAtts.imageZoom = 0.826446
View3DAtts.perspective = 1
View3DAtts.eyeAngle = 2
View3DAtts.centerOfRotationSet = 0
View3DAtts.centerOfRotation = (512, 512, 5.55112e-17)
View3DAtts.axis3DScaleFlag = 0
View3DAtts.axis3DScales = (1, 1, 1)
View3DAtts.shear = (0, 0, 1)
View3DAtts.windowValid = 1
SetView3D(View3DAtts)
# End spontaneous state

# Begin spontaneous state
View3DAtts = View3DAttributes()
View3DAtts.viewNormal = (-0.224409, -0.808096, 0.54463)
View3DAtts.focus = (512, 512, 5.55112e-17)
View3DAtts.viewUp = (0.0555088, 0.547377, 0.835043)
View3DAtts.viewAngle = 30
View3DAtts.parallelScale = 724.078
View3DAtts.nearPlane = -1448.16
View3DAtts.farPlane = 1448.16
View3DAtts.imagePan = (0, 0)
View3DAtts.imageZoom = 1
View3DAtts.perspective = 1
View3DAtts.eyeAngle = 2
View3DAtts.centerOfRotationSet = 0
View3DAtts.centerOfRotation = (512, 512, 5.55112e-17)
View3DAtts.axis3DScaleFlag = 0
View3DAtts.axis3DScales = (1, 1, 1)
View3DAtts.shear = (0, 0, 1)
View3DAtts.windowValid = 1
SetView3D(View3DAtts)
# End spontaneous state

# Begin spontaneous state
View3DAtts = View3DAttributes()
View3DAtts.viewNormal = (-0.224409, -0.808096, 0.54463)
View3DAtts.focus = (512, 512, 5.55112e-17)
View3DAtts.viewUp = (0.0555088, 0.547377, 0.835043)
View3DAtts.viewAngle = 30
View3DAtts.parallelScale = 724.078
View3DAtts.nearPlane = -1448.16
View3DAtts.farPlane = 1448.16
View3DAtts.imagePan = (0, 0)
View3DAtts.imageZoom = 1.21
View3DAtts.perspective = 1
View3DAtts.eyeAngle = 2
View3DAtts.centerOfRotationSet = 0
View3DAtts.centerOfRotation = (512, 512, 5.55112e-17)
View3DAtts.axis3DScaleFlag = 0
View3DAtts.axis3DScales = (1, 1, 1)
View3DAtts.shear = (0, 0, 1)
View3DAtts.windowValid = 1
SetView3D(View3DAtts)
# End spontaneous state

# Begin spontaneous state
View3DAtts = View3DAttributes()
View3DAtts.viewNormal = (-0.224409, -0.808096, 0.54463)
View3DAtts.focus = (512, 512, 5.55112e-17)
View3DAtts.viewUp = (0.0555088, 0.547377, 0.835043)
View3DAtts.viewAngle = 30
View3DAtts.parallelScale = 724.078
View3DAtts.nearPlane = -1448.16
View3DAtts.farPlane = 1448.16
View3DAtts.imagePan = (0, 0)
View3DAtts.imageZoom = 1.4641
View3DAtts.perspective = 1
View3DAtts.eyeAngle = 2
View3DAtts.centerOfRotationSet = 0
View3DAtts.centerOfRotation = (512, 512, 5.55112e-17)
View3DAtts.axis3DScaleFlag = 0
View3DAtts.axis3DScales = (1, 1, 1)
View3DAtts.shear = (0, 0, 1)
View3DAtts.windowValid = 1
SetView3D(View3DAtts)
# End spontaneous state

# Begin spontaneous state
View3DAtts = View3DAttributes()
View3DAtts.viewNormal = (-0.224409, -0.808096, 0.54463)
View3DAtts.focus = (512, 512, 5.55112e-17)
View3DAtts.viewUp = (0.0555088, 0.547377, 0.835043)
View3DAtts.viewAngle = 30
View3DAtts.parallelScale = 724.078
View3DAtts.nearPlane = -1448.16
View3DAtts.farPlane = 1448.16
View3DAtts.imagePan = (0, 0)
View3DAtts.imageZoom = 1.77156
View3DAtts.perspective = 1
View3DAtts.eyeAngle = 2
View3DAtts.centerOfRotationSet = 0
View3DAtts.centerOfRotation = (512, 512, 5.55112e-17)
View3DAtts.axis3DScaleFlag = 0
View3DAtts.axis3DScales = (1, 1, 1)
View3DAtts.shear = (0, 0, 1)
View3DAtts.windowValid = 1
SetView3D(View3DAtts)
# End spontaneous state

# Begin spontaneous state
View3DAtts = View3DAttributes()
View3DAtts.viewNormal = (-0.224409, -0.808096, 0.54463)
View3DAtts.focus = (512, 512, 5.55112e-17)
View3DAtts.viewUp = (0.0555088, 0.547377, 0.835043)
View3DAtts.viewAngle = 30
View3DAtts.parallelScale = 724.078
View3DAtts.nearPlane = -1448.16
View3DAtts.farPlane = 1448.16
View3DAtts.imagePan = (0, 0)
View3DAtts.imageZoom = 2.14359
View3DAtts.perspective = 1
View3DAtts.eyeAngle = 2
View3DAtts.centerOfRotationSet = 0
View3DAtts.centerOfRotation = (512, 512, 5.55112e-17)
View3DAtts.axis3DScaleFlag = 0
View3DAtts.axis3DScales = (1, 1, 1)
View3DAtts.shear = (0, 0, 1)
View3DAtts.windowValid = 1
SetView3D(View3DAtts)
# End spontaneous state

# Begin spontaneous state
View3DAtts = View3DAttributes()
View3DAtts.viewNormal = (-0.224409, -0.808096, 0.54463)
View3DAtts.focus = (512, 512, 5.55112e-17)
View3DAtts.viewUp = (0.0555088, 0.547377, 0.835043)
View3DAtts.viewAngle = 30
View3DAtts.parallelScale = 724.078
View3DAtts.nearPlane = -1448.16
View3DAtts.farPlane = 1448.16
View3DAtts.imagePan = (0, 0)
View3DAtts.imageZoom = 2.59374
View3DAtts.perspective = 1
View3DAtts.eyeAngle = 2
View3DAtts.centerOfRotationSet = 0
View3DAtts.centerOfRotation = (512, 512, 5.55112e-17)
View3DAtts.axis3DScaleFlag = 0
View3DAtts.axis3DScales = (1, 1, 1)
View3DAtts.shear = (0, 0, 1)
View3DAtts.windowValid = 1
SetView3D(View3DAtts)
# End spontaneous state

# Begin spontaneous state
View3DAtts = View3DAttributes()
View3DAtts.viewNormal = (-0.224409, -0.808096, 0.54463)
View3DAtts.focus = (512, 512, 5.55112e-17)
View3DAtts.viewUp = (0.0555088, 0.547377, 0.835043)
View3DAtts.viewAngle = 30
View3DAtts.parallelScale = 724.078
View3DAtts.nearPlane = -1448.16
View3DAtts.farPlane = 1448.16
View3DAtts.imagePan = (0, 0)
View3DAtts.imageZoom = 3.13843
View3DAtts.perspective = 1
View3DAtts.eyeAngle = 2
View3DAtts.centerOfRotationSet = 0
View3DAtts.centerOfRotation = (512, 512, 5.55112e-17)
View3DAtts.axis3DScaleFlag = 0
View3DAtts.axis3DScales = (1, 1, 1)
View3DAtts.shear = (0, 0, 1)
View3DAtts.windowValid = 1
SetView3D(View3DAtts)
# End spontaneous state

# Begin spontaneous state
View3DAtts = View3DAttributes()
View3DAtts.viewNormal = (-0.224409, -0.808096, 0.54463)
View3DAtts.focus = (512, 512, 5.55112e-17)
View3DAtts.viewUp = (0.0555088, 0.547377, 0.835043)
View3DAtts.viewAngle = 30
View3DAtts.parallelScale = 724.078
View3DAtts.nearPlane = -1448.16
View3DAtts.farPlane = 1448.16
View3DAtts.imagePan = (0, 0)
View3DAtts.imageZoom = 3.7975
View3DAtts.perspective = 1
View3DAtts.eyeAngle = 2
View3DAtts.centerOfRotationSet = 0
View3DAtts.centerOfRotation = (512, 512, 5.55112e-17)
View3DAtts.axis3DScaleFlag = 0
View3DAtts.axis3DScales = (1, 1, 1)
View3DAtts.shear = (0, 0, 1)
View3DAtts.windowValid = 1
SetView3D(View3DAtts)
# End spontaneous state

# Begin spontaneous state
View3DAtts = View3DAttributes()
View3DAtts.viewNormal = (-0.224409, -0.808096, 0.54463)
View3DAtts.focus = (512, 512, 5.55112e-17)
View3DAtts.viewUp = (0.0555088, 0.547377, 0.835043)
View3DAtts.viewAngle = 30
View3DAtts.parallelScale = 724.078
View3DAtts.nearPlane = -1448.16
View3DAtts.farPlane = 1448.16
View3DAtts.imagePan = (0, 0)
View3DAtts.imageZoom = 4.59497
View3DAtts.perspective = 1
View3DAtts.eyeAngle = 2
View3DAtts.centerOfRotationSet = 0
View3DAtts.centerOfRotation = (512, 512, 5.55112e-17)
View3DAtts.axis3DScaleFlag = 0
View3DAtts.axis3DScales = (1, 1, 1)
View3DAtts.shear = (0, 0, 1)
View3DAtts.windowValid = 1
SetView3D(View3DAtts)
# End spontaneous state

# Begin spontaneous state
View3DAtts = View3DAttributes()
View3DAtts.viewNormal = (-0.224409, -0.808096, 0.54463)
View3DAtts.focus = (512, 512, 5.55112e-17)
View3DAtts.viewUp = (0.0555088, 0.547377, 0.835043)
View3DAtts.viewAngle = 30
View3DAtts.parallelScale = 724.078
View3DAtts.nearPlane = -1448.16
View3DAtts.farPlane = 1448.16
View3DAtts.imagePan = (0, 0)
View3DAtts.imageZoom = 5.55992
View3DAtts.perspective = 1
View3DAtts.eyeAngle = 2
View3DAtts.centerOfRotationSet = 0
View3DAtts.centerOfRotation = (512, 512, 5.55112e-17)
View3DAtts.axis3DScaleFlag = 0
View3DAtts.axis3DScales = (1, 1, 1)
View3DAtts.shear = (0, 0, 1)
View3DAtts.windowValid = 1
SetView3D(View3DAtts)
# End spontaneous state

# Begin spontaneous state
View3DAtts = View3DAttributes()
View3DAtts.viewNormal = (-0.224409, -0.808096, 0.54463)
View3DAtts.focus = (512, 512, 5.55112e-17)
View3DAtts.viewUp = (0.0555088, 0.547377, 0.835043)
View3DAtts.viewAngle = 30
View3DAtts.parallelScale = 724.078
View3DAtts.nearPlane = -1448.16
View3DAtts.farPlane = 1448.16
View3DAtts.imagePan = (0, 0)
View3DAtts.imageZoom = 4.59497
View3DAtts.perspective = 1
View3DAtts.eyeAngle = 2
View3DAtts.centerOfRotationSet = 0
View3DAtts.centerOfRotation = (512, 512, 5.55112e-17)
View3DAtts.axis3DScaleFlag = 0
View3DAtts.axis3DScales = (1, 1, 1)
View3DAtts.shear = (0, 0, 1)
View3DAtts.windowValid = 1
SetView3D(View3DAtts)
# End spontaneous state

# Begin spontaneous state
View3DAtts = View3DAttributes()
View3DAtts.viewNormal = (-0.224409, -0.808096, 0.54463)
View3DAtts.focus = (512, 512, 5.55112e-17)
View3DAtts.viewUp = (0.0555088, 0.547377, 0.835043)
View3DAtts.viewAngle = 30
View3DAtts.parallelScale = 724.078
View3DAtts.nearPlane = -1448.16
View3DAtts.farPlane = 1448.16
View3DAtts.imagePan = (0, 0)
View3DAtts.imageZoom = 3.7975
View3DAtts.perspective = 1
View3DAtts.eyeAngle = 2
View3DAtts.centerOfRotationSet = 0
View3DAtts.centerOfRotation = (512, 512, 5.55112e-17)
View3DAtts.axis3DScaleFlag = 0
View3DAtts.axis3DScales = (1, 1, 1)
View3DAtts.shear = (0, 0, 1)
View3DAtts.windowValid = 1
SetView3D(View3DAtts)
# End spontaneous state

# Begin spontaneous state
View3DAtts = View3DAttributes()
View3DAtts.viewNormal = (-0.224409, -0.808096, 0.54463)
View3DAtts.focus = (512, 512, 5.55112e-17)
View3DAtts.viewUp = (0.0555088, 0.547377, 0.835043)
View3DAtts.viewAngle = 30
View3DAtts.parallelScale = 724.078
View3DAtts.nearPlane = -1448.16
View3DAtts.farPlane = 1448.16
View3DAtts.imagePan = (0, 0)
View3DAtts.imageZoom = 3.13843
View3DAtts.perspective = 1
View3DAtts.eyeAngle = 2
View3DAtts.centerOfRotationSet = 0
View3DAtts.centerOfRotation = (512, 512, 5.55112e-17)
View3DAtts.axis3DScaleFlag = 0
View3DAtts.axis3DScales = (1, 1, 1)
View3DAtts.shear = (0, 0, 1)
View3DAtts.windowValid = 1
SetView3D(View3DAtts)
# End spontaneous state

# Begin spontaneous state
View3DAtts = View3DAttributes()
View3DAtts.viewNormal = (-0.224409, -0.808096, 0.54463)
View3DAtts.focus = (512, 512, 5.55112e-17)
View3DAtts.viewUp = (0.0555088, 0.547377, 0.835043)
View3DAtts.viewAngle = 30
View3DAtts.parallelScale = 724.078
View3DAtts.nearPlane = -1448.16
View3DAtts.farPlane = 1448.16
View3DAtts.imagePan = (0, 0)
View3DAtts.imageZoom = 2.59374
View3DAtts.perspective = 1
View3DAtts.eyeAngle = 2
View3DAtts.centerOfRotationSet = 0
View3DAtts.centerOfRotation = (512, 512, 5.55112e-17)
View3DAtts.axis3DScaleFlag = 0
View3DAtts.axis3DScales = (1, 1, 1)
View3DAtts.shear = (0, 0, 1)
View3DAtts.windowValid = 1
SetView3D(View3DAtts)
# End spontaneous state

# Begin spontaneous state
View3DAtts = View3DAttributes()
View3DAtts.viewNormal = (-0.224409, -0.808096, 0.54463)
View3DAtts.focus = (512, 512, 5.55112e-17)
View3DAtts.viewUp = (0.0555088, 0.547377, 0.835043)
View3DAtts.viewAngle = 30
View3DAtts.parallelScale = 724.078
View3DAtts.nearPlane = -1448.16
View3DAtts.farPlane = 1448.16
View3DAtts.imagePan = (0, 0)
View3DAtts.imageZoom = 3.13843
View3DAtts.perspective = 1
View3DAtts.eyeAngle = 2
View3DAtts.centerOfRotationSet = 0
View3DAtts.centerOfRotation = (512, 512, 5.55112e-17)
View3DAtts.axis3DScaleFlag = 0
View3DAtts.axis3DScales = (1, 1, 1)
View3DAtts.shear = (0, 0, 1)
View3DAtts.windowValid = 1
SetView3D(View3DAtts)
# End spontaneous state

# Begin spontaneous state
View3DAtts = View3DAttributes()
View3DAtts.viewNormal = (-0.224409, -0.808096, 0.54463)
View3DAtts.focus = (512, 512, 5.55112e-17)
View3DAtts.viewUp = (0.0555088, 0.547377, 0.835043)
View3DAtts.viewAngle = 30
View3DAtts.parallelScale = 724.078
View3DAtts.nearPlane = -1448.16
View3DAtts.farPlane = 1448.16
View3DAtts.imagePan = (0, 0)
View3DAtts.imageZoom = 3.7975
View3DAtts.perspective = 1
View3DAtts.eyeAngle = 2
View3DAtts.centerOfRotationSet = 0
View3DAtts.centerOfRotation = (512, 512, 5.55112e-17)
View3DAtts.axis3DScaleFlag = 0
View3DAtts.axis3DScales = (1, 1, 1)
View3DAtts.shear = (0, 0, 1)
View3DAtts.windowValid = 1
SetView3D(View3DAtts)
# End spontaneous state

# Begin spontaneous state
View3DAtts = View3DAttributes()
View3DAtts.viewNormal = (-0.224409, -0.808096, 0.54463)
View3DAtts.focus = (512, 512, 5.55112e-17)
View3DAtts.viewUp = (0.0555088, 0.547377, 0.835043)
View3DAtts.viewAngle = 30
View3DAtts.parallelScale = 724.078
View3DAtts.nearPlane = -1448.16
View3DAtts.farPlane = 1448.16
View3DAtts.imagePan = (0, 0)
View3DAtts.imageZoom = 4.59497
View3DAtts.perspective = 1
View3DAtts.eyeAngle = 2
View3DAtts.centerOfRotationSet = 0
View3DAtts.centerOfRotation = (512, 512, 5.55112e-17)
View3DAtts.axis3DScaleFlag = 0
View3DAtts.axis3DScales = (1, 1, 1)
View3DAtts.shear = (0, 0, 1)
View3DAtts.windowValid = 1
SetView3D(View3DAtts)
# End spontaneous state

# Begin spontaneous state
View3DAtts = View3DAttributes()
View3DAtts.viewNormal = (-0.224409, -0.808096, 0.54463)
View3DAtts.focus = (512, 512, 5.55112e-17)
View3DAtts.viewUp = (0.0555088, 0.547377, 0.835043)
View3DAtts.viewAngle = 30
View3DAtts.parallelScale = 724.078
View3DAtts.nearPlane = -1448.16
View3DAtts.farPlane = 1448.16
View3DAtts.imagePan = (0, 0)
View3DAtts.imageZoom = 5.55992
View3DAtts.perspective = 1
View3DAtts.eyeAngle = 2
View3DAtts.centerOfRotationSet = 0
View3DAtts.centerOfRotation = (512, 512, 5.55112e-17)
View3DAtts.axis3DScaleFlag = 0
View3DAtts.axis3DScales = (1, 1, 1)
View3DAtts.shear = (0, 0, 1)
View3DAtts.windowValid = 1
SetView3D(View3DAtts)
# End spontaneous state

# Begin spontaneous state
View3DAtts = View3DAttributes()
View3DAtts.viewNormal = (-0.224409, -0.808096, 0.54463)
View3DAtts.focus = (512, 512, 5.55112e-17)
View3DAtts.viewUp = (0.0555088, 0.547377, 0.835043)
View3DAtts.viewAngle = 30
View3DAtts.parallelScale = 724.078
View3DAtts.nearPlane = -1448.16
View3DAtts.farPlane = 1448.16
View3DAtts.imagePan = (0, 0)
View3DAtts.imageZoom = 6.7275
View3DAtts.perspective = 1
View3DAtts.eyeAngle = 2
View3DAtts.centerOfRotationSet = 0
View3DAtts.centerOfRotation = (512, 512, 5.55112e-17)
View3DAtts.axis3DScaleFlag = 0
View3DAtts.axis3DScales = (1, 1, 1)
View3DAtts.shear = (0, 0, 1)
View3DAtts.windowValid = 1
SetView3D(View3DAtts)
# End spontaneous state

# Begin spontaneous state
View3DAtts = View3DAttributes()
View3DAtts.viewNormal = (-0.224409, -0.808096, 0.54463)
View3DAtts.focus = (512, 512, 5.55112e-17)
View3DAtts.viewUp = (0.0555088, 0.547377, 0.835043)
View3DAtts.viewAngle = 30
View3DAtts.parallelScale = 724.078
View3DAtts.nearPlane = -1448.16
View3DAtts.farPlane = 1448.16
View3DAtts.imagePan = (0, 0)
View3DAtts.imageZoom = 8.14027
View3DAtts.perspective = 1
View3DAtts.eyeAngle = 2
View3DAtts.centerOfRotationSet = 0
View3DAtts.centerOfRotation = (512, 512, 5.55112e-17)
View3DAtts.axis3DScaleFlag = 0
View3DAtts.axis3DScales = (1, 1, 1)
View3DAtts.shear = (0, 0, 1)
View3DAtts.windowValid = 1
SetView3D(View3DAtts)
# End spontaneous state

# Begin spontaneous state
View3DAtts = View3DAttributes()
View3DAtts.viewNormal = (-0.224409, -0.808096, 0.54463)
View3DAtts.focus = (512, 512, 5.55112e-17)
View3DAtts.viewUp = (0.0555088, 0.547377, 0.835043)
View3DAtts.viewAngle = 30
View3DAtts.parallelScale = 724.078
View3DAtts.nearPlane = -1448.16
View3DAtts.farPlane = 1448.16
View3DAtts.imagePan = (0, 0)
View3DAtts.imageZoom = 9.84973
View3DAtts.perspective = 1
View3DAtts.eyeAngle = 2
View3DAtts.centerOfRotationSet = 0
View3DAtts.centerOfRotation = (512, 512, 5.55112e-17)
View3DAtts.axis3DScaleFlag = 0
View3DAtts.axis3DScales = (1, 1, 1)
View3DAtts.shear = (0, 0, 1)
View3DAtts.windowValid = 1
SetView3D(View3DAtts)
# End spontaneous state

# Begin spontaneous state
View3DAtts = View3DAttributes()
View3DAtts.viewNormal = (-0.224409, -0.808096, 0.54463)
View3DAtts.focus = (512, 512, 5.55112e-17)
View3DAtts.viewUp = (0.0555088, 0.547377, 0.835043)
View3DAtts.viewAngle = 30
View3DAtts.parallelScale = 724.078
View3DAtts.nearPlane = -1448.16
View3DAtts.farPlane = 1448.16
View3DAtts.imagePan = (0, 0)
View3DAtts.imageZoom = 11.9182
View3DAtts.perspective = 1
View3DAtts.eyeAngle = 2
View3DAtts.centerOfRotationSet = 0
View3DAtts.centerOfRotation = (512, 512, 5.55112e-17)
View3DAtts.axis3DScaleFlag = 0
View3DAtts.axis3DScales = (1, 1, 1)
View3DAtts.shear = (0, 0, 1)
View3DAtts.windowValid = 1
SetView3D(View3DAtts)
# End spontaneous state

# Begin spontaneous state
View3DAtts = View3DAttributes()
View3DAtts.viewNormal = (-0.224409, -0.808096, 0.54463)
View3DAtts.focus = (512, 512, 5.55112e-17)
View3DAtts.viewUp = (0.0555088, 0.547377, 0.835043)
View3DAtts.viewAngle = 30
View3DAtts.parallelScale = 724.078
View3DAtts.nearPlane = -1448.16
View3DAtts.farPlane = 1448.16
View3DAtts.imagePan = (0, 0)
View3DAtts.imageZoom = 14.421
View3DAtts.perspective = 1
View3DAtts.eyeAngle = 2
View3DAtts.centerOfRotationSet = 0
View3DAtts.centerOfRotation = (512, 512, 5.55112e-17)
View3DAtts.axis3DScaleFlag = 0
View3DAtts.axis3DScales = (1, 1, 1)
View3DAtts.shear = (0, 0, 1)
View3DAtts.windowValid = 1
SetView3D(View3DAtts)
# End spontaneous state

# Begin spontaneous state
View3DAtts = View3DAttributes()
View3DAtts.viewNormal = (-0.224409, -0.808096, 0.54463)
View3DAtts.focus = (512, 512, 5.55112e-17)
View3DAtts.viewUp = (0.0555088, 0.547377, 0.835043)
View3DAtts.viewAngle = 30
View3DAtts.parallelScale = 724.078
View3DAtts.nearPlane = -1448.16
View3DAtts.farPlane = 1448.16
View3DAtts.imagePan = (0, 0)
View3DAtts.imageZoom = 11.9182
View3DAtts.perspective = 1
View3DAtts.eyeAngle = 2
View3DAtts.centerOfRotationSet = 0
View3DAtts.centerOfRotation = (512, 512, 5.55112e-17)
View3DAtts.axis3DScaleFlag = 0
View3DAtts.axis3DScales = (1, 1, 1)
View3DAtts.shear = (0, 0, 1)
View3DAtts.windowValid = 1
SetView3D(View3DAtts)
# End spontaneous state

# Begin spontaneous state
View3DAtts = View3DAttributes()
View3DAtts.viewNormal = (-0.224409, -0.808096, 0.54463)
View3DAtts.focus = (512, 512, 5.55112e-17)
View3DAtts.viewUp = (0.0555088, 0.547377, 0.835043)
View3DAtts.viewAngle = 30
View3DAtts.parallelScale = 724.078
View3DAtts.nearPlane = -1448.16
View3DAtts.farPlane = 1448.16
View3DAtts.imagePan = (0, 0)
View3DAtts.imageZoom = 9.84973
View3DAtts.perspective = 1
View3DAtts.eyeAngle = 2
View3DAtts.centerOfRotationSet = 0
View3DAtts.centerOfRotation = (512, 512, 5.55112e-17)
View3DAtts.axis3DScaleFlag = 0
View3DAtts.axis3DScales = (1, 1, 1)
View3DAtts.shear = (0, 0, 1)
View3DAtts.windowValid = 1
SetView3D(View3DAtts)
# End spontaneous state

# Begin spontaneous state
View3DAtts = View3DAttributes()
View3DAtts.viewNormal = (-0.224409, -0.808096, 0.54463)
View3DAtts.focus = (512, 512, 5.55112e-17)
View3DAtts.viewUp = (0.0555088, 0.547377, 0.835043)
View3DAtts.viewAngle = 30
View3DAtts.parallelScale = 724.078
View3DAtts.nearPlane = -1448.16
View3DAtts.farPlane = 1448.16
View3DAtts.imagePan = (0, 0)
View3DAtts.imageZoom = 8.14027
View3DAtts.perspective = 1
View3DAtts.eyeAngle = 2
View3DAtts.centerOfRotationSet = 0
View3DAtts.centerOfRotation = (512, 512, 5.55112e-17)
View3DAtts.axis3DScaleFlag = 0
View3DAtts.axis3DScales = (1, 1, 1)
View3DAtts.shear = (0, 0, 1)
View3DAtts.windowValid = 1
SetView3D(View3DAtts)
# End spontaneous state

# Begin spontaneous state
View3DAtts = View3DAttributes()
View3DAtts.viewNormal = (-0.224409, -0.808096, 0.54463)
View3DAtts.focus = (512, 512, 5.55112e-17)
View3DAtts.viewUp = (0.0555088, 0.547377, 0.835043)
View3DAtts.viewAngle = 30
View3DAtts.parallelScale = 724.078
View3DAtts.nearPlane = -1448.16
View3DAtts.farPlane = 1448.16
View3DAtts.imagePan = (0, 0)
View3DAtts.imageZoom = 6.7275
View3DAtts.perspective = 1
View3DAtts.eyeAngle = 2
View3DAtts.centerOfRotationSet = 0
View3DAtts.centerOfRotation = (512, 512, 5.55112e-17)
View3DAtts.axis3DScaleFlag = 0
View3DAtts.axis3DScales = (1, 1, 1)
View3DAtts.shear = (0, 0, 1)
View3DAtts.windowValid = 1
SetView3D(View3DAtts)
# End spontaneous state

# Begin spontaneous state
View3DAtts = View3DAttributes()
View3DAtts.viewNormal = (-0.224409, -0.808096, 0.54463)
View3DAtts.focus = (512, 512, 5.55112e-17)
View3DAtts.viewUp = (0.0555088, 0.547377, 0.835043)
View3DAtts.viewAngle = 30
View3DAtts.parallelScale = 724.078
View3DAtts.nearPlane = -1448.16
View3DAtts.farPlane = 1448.16
View3DAtts.imagePan = (0, 0)
View3DAtts.imageZoom = 5.55992
View3DAtts.perspective = 1
View3DAtts.eyeAngle = 2
View3DAtts.centerOfRotationSet = 0
View3DAtts.centerOfRotation = (512, 512, 5.55112e-17)
View3DAtts.axis3DScaleFlag = 0
View3DAtts.axis3DScales = (1, 1, 1)
View3DAtts.shear = (0, 0, 1)
View3DAtts.windowValid = 1
SetView3D(View3DAtts)
# End spontaneous state

# Begin spontaneous state
View3DAtts = View3DAttributes()
View3DAtts.viewNormal = (-0.224409, -0.808096, 0.54463)
View3DAtts.focus = (512, 512, 5.55112e-17)
View3DAtts.viewUp = (0.0555088, 0.547377, 0.835043)
View3DAtts.viewAngle = 30
View3DAtts.parallelScale = 724.078
View3DAtts.nearPlane = -1448.16
View3DAtts.farPlane = 1448.16
View3DAtts.imagePan = (0, 0)
View3DAtts.imageZoom = 6.7275
View3DAtts.perspective = 1
View3DAtts.eyeAngle = 2
View3DAtts.centerOfRotationSet = 0
View3DAtts.centerOfRotation = (512, 512, 5.55112e-17)
View3DAtts.axis3DScaleFlag = 0
View3DAtts.axis3DScales = (1, 1, 1)
View3DAtts.shear = (0, 0, 1)
View3DAtts.windowValid = 1
SetView3D(View3DAtts)
# End spontaneous state

# Begin spontaneous state
View3DAtts = View3DAttributes()
View3DAtts.viewNormal = (-0.224409, -0.808096, 0.54463)
View3DAtts.focus = (512, 512, 5.55112e-17)
View3DAtts.viewUp = (0.0555088, 0.547377, 0.835043)
View3DAtts.viewAngle = 30
View3DAtts.parallelScale = 724.078
View3DAtts.nearPlane = -1448.16
View3DAtts.farPlane = 1448.16
View3DAtts.imagePan = (0, 0)
View3DAtts.imageZoom = 8.14027
View3DAtts.perspective = 1
View3DAtts.eyeAngle = 2
View3DAtts.centerOfRotationSet = 0
View3DAtts.centerOfRotation = (512, 512, 5.55112e-17)
View3DAtts.axis3DScaleFlag = 0
View3DAtts.axis3DScales = (1, 1, 1)
View3DAtts.shear = (0, 0, 1)
View3DAtts.windowValid = 1
SetView3D(View3DAtts)
# End spontaneous state

# Begin spontaneous state
View3DAtts = View3DAttributes()
View3DAtts.viewNormal = (-0.224409, -0.808096, 0.54463)
View3DAtts.focus = (512, 512, 5.55112e-17)
View3DAtts.viewUp = (0.0555088, 0.547377, 0.835043)
View3DAtts.viewAngle = 30
View3DAtts.parallelScale = 724.078
View3DAtts.nearPlane = -1448.16
View3DAtts.farPlane = 1448.16
View3DAtts.imagePan = (0, 0)
View3DAtts.imageZoom = 9.84973
View3DAtts.perspective = 1
View3DAtts.eyeAngle = 2
View3DAtts.centerOfRotationSet = 0
View3DAtts.centerOfRotation = (512, 512, 5.55112e-17)
View3DAtts.axis3DScaleFlag = 0
View3DAtts.axis3DScales = (1, 1, 1)
View3DAtts.shear = (0, 0, 1)
View3DAtts.windowValid = 1
SetView3D(View3DAtts)
# End spontaneous state

# Begin spontaneous state
View3DAtts = View3DAttributes()
View3DAtts.viewNormal = (-0.224409, -0.808096, 0.54463)
View3DAtts.focus = (512, 512, 5.55112e-17)
View3DAtts.viewUp = (0.0555088, 0.547377, 0.835043)
View3DAtts.viewAngle = 30
View3DAtts.parallelScale = 724.078
View3DAtts.nearPlane = -1448.16
View3DAtts.farPlane = 1448.16
View3DAtts.imagePan = (0, 0)
View3DAtts.imageZoom = 11.9182
View3DAtts.perspective = 1
View3DAtts.eyeAngle = 2
View3DAtts.centerOfRotationSet = 0
View3DAtts.centerOfRotation = (512, 512, 5.55112e-17)
View3DAtts.axis3DScaleFlag = 0
View3DAtts.axis3DScales = (1, 1, 1)
View3DAtts.shear = (0, 0, 1)
View3DAtts.windowValid = 1
SetView3D(View3DAtts)
# End spontaneous state

# Begin spontaneous state
View3DAtts = View3DAttributes()
View3DAtts.viewNormal = (-0.224409, -0.808096, 0.54463)
View3DAtts.focus = (512, 512, 5.55112e-17)
View3DAtts.viewUp = (0.0555088, 0.547377, 0.835043)
View3DAtts.viewAngle = 30
View3DAtts.parallelScale = 724.078
View3DAtts.nearPlane = -1448.16
View3DAtts.farPlane = 1448.16
View3DAtts.imagePan = (0, 0)
View3DAtts.imageZoom = 14.421
View3DAtts.perspective = 1
View3DAtts.eyeAngle = 2
View3DAtts.centerOfRotationSet = 0
View3DAtts.centerOfRotation = (512, 512, 5.55112e-17)
View3DAtts.axis3DScaleFlag = 0
View3DAtts.axis3DScales = (1, 1, 1)
View3DAtts.shear = (0, 0, 1)
View3DAtts.windowValid = 1
SetView3D(View3DAtts)
# End spontaneous state

# Begin spontaneous state
View3DAtts = View3DAttributes()
View3DAtts.viewNormal = (-0.224409, -0.808096, 0.54463)
View3DAtts.focus = (512, 512, 5.55112e-17)
View3DAtts.viewUp = (0.0555088, 0.547377, 0.835043)
View3DAtts.viewAngle = 30
View3DAtts.parallelScale = 724.078
View3DAtts.nearPlane = -1448.16
View3DAtts.farPlane = 1448.16
View3DAtts.imagePan = (0, 0)
View3DAtts.imageZoom = 17.4494
View3DAtts.perspective = 1
View3DAtts.eyeAngle = 2
View3DAtts.centerOfRotationSet = 0
View3DAtts.centerOfRotation = (512, 512, 5.55112e-17)
View3DAtts.axis3DScaleFlag = 0
View3DAtts.axis3DScales = (1, 1, 1)
View3DAtts.shear = (0, 0, 1)
View3DAtts.windowValid = 1
SetView3D(View3DAtts)
# End spontaneous state

# Begin spontaneous state
View3DAtts = View3DAttributes()
View3DAtts.viewNormal = (-0.224409, -0.808096, 0.54463)
View3DAtts.focus = (512, 512, 5.55112e-17)
View3DAtts.viewUp = (0.0555088, 0.547377, 0.835043)
View3DAtts.viewAngle = 30
View3DAtts.parallelScale = 724.078
View3DAtts.nearPlane = -1448.16
View3DAtts.farPlane = 1448.16
View3DAtts.imagePan = (0, 0)
View3DAtts.imageZoom = 21.1138
View3DAtts.perspective = 1
View3DAtts.eyeAngle = 2
View3DAtts.centerOfRotationSet = 0
View3DAtts.centerOfRotation = (512, 512, 5.55112e-17)
View3DAtts.axis3DScaleFlag = 0
View3DAtts.axis3DScales = (1, 1, 1)
View3DAtts.shear = (0, 0, 1)
View3DAtts.windowValid = 1
SetView3D(View3DAtts)
# End spontaneous state

# Begin spontaneous state
View3DAtts = View3DAttributes()
View3DAtts.viewNormal = (-0.224409, -0.808096, 0.54463)
View3DAtts.focus = (512, 512, 5.55112e-17)
View3DAtts.viewUp = (0.0555088, 0.547377, 0.835043)
View3DAtts.viewAngle = 30
View3DAtts.parallelScale = 724.078
View3DAtts.nearPlane = -1448.16
View3DAtts.farPlane = 1448.16
View3DAtts.imagePan = (0, 0)
View3DAtts.imageZoom = 25.5477
View3DAtts.perspective = 1
View3DAtts.eyeAngle = 2
View3DAtts.centerOfRotationSet = 0
View3DAtts.centerOfRotation = (512, 512, 5.55112e-17)
View3DAtts.axis3DScaleFlag = 0
View3DAtts.axis3DScales = (1, 1, 1)
View3DAtts.shear = (0, 0, 1)
View3DAtts.windowValid = 1
SetView3D(View3DAtts)
# End spontaneous state

# Begin spontaneous state
View3DAtts = View3DAttributes()
View3DAtts.viewNormal = (-0.224409, -0.808096, 0.54463)
View3DAtts.focus = (512, 512, 5.55112e-17)
View3DAtts.viewUp = (0.0555088, 0.547377, 0.835043)
View3DAtts.viewAngle = 30
View3DAtts.parallelScale = 724.078
View3DAtts.nearPlane = -1448.16
View3DAtts.farPlane = 1448.16
View3DAtts.imagePan = (0, 0)
View3DAtts.imageZoom = 30.9127
View3DAtts.perspective = 1
View3DAtts.eyeAngle = 2
View3DAtts.centerOfRotationSet = 0
View3DAtts.centerOfRotation = (512, 512, 5.55112e-17)
View3DAtts.axis3DScaleFlag = 0
View3DAtts.axis3DScales = (1, 1, 1)
View3DAtts.shear = (0, 0, 1)
View3DAtts.windowValid = 1
SetView3D(View3DAtts)
# End spontaneous state

# Begin spontaneous state
View3DAtts = View3DAttributes()
View3DAtts.viewNormal = (-0.224409, -0.808096, 0.54463)
View3DAtts.focus = (512, 512, 5.55112e-17)
View3DAtts.viewUp = (0.0555088, 0.547377, 0.835043)
View3DAtts.viewAngle = 30
View3DAtts.parallelScale = 724.078
View3DAtts.nearPlane = -1448.16
View3DAtts.farPlane = 1448.16
View3DAtts.imagePan = (0, 0)
View3DAtts.imageZoom = 25.5477
View3DAtts.perspective = 1
View3DAtts.eyeAngle = 2
View3DAtts.centerOfRotationSet = 0
View3DAtts.centerOfRotation = (512, 512, 5.55112e-17)
View3DAtts.axis3DScaleFlag = 0
View3DAtts.axis3DScales = (1, 1, 1)
View3DAtts.shear = (0, 0, 1)
View3DAtts.windowValid = 1
SetView3D(View3DAtts)
# End spontaneous state

# Begin spontaneous state
View3DAtts = View3DAttributes()
View3DAtts.viewNormal = (-0.224409, -0.808096, 0.54463)
View3DAtts.focus = (512, 512, 5.55112e-17)
View3DAtts.viewUp = (0.0555088, 0.547377, 0.835043)
View3DAtts.viewAngle = 30
View3DAtts.parallelScale = 724.078
View3DAtts.nearPlane = -1448.16
View3DAtts.farPlane = 1448.16
View3DAtts.imagePan = (0, 0)
View3DAtts.imageZoom = 21.1138
View3DAtts.perspective = 1
View3DAtts.eyeAngle = 2
View3DAtts.centerOfRotationSet = 0
View3DAtts.centerOfRotation = (512, 512, 5.55112e-17)
View3DAtts.axis3DScaleFlag = 0
View3DAtts.axis3DScales = (1, 1, 1)
View3DAtts.shear = (0, 0, 1)
View3DAtts.windowValid = 1
SetView3D(View3DAtts)
# End spontaneous state

# Begin spontaneous state
View3DAtts = View3DAttributes()
View3DAtts.viewNormal = (-0.224409, -0.808096, 0.54463)
View3DAtts.focus = (512, 512, 5.55112e-17)
View3DAtts.viewUp = (0.0555088, 0.547377, 0.835043)
View3DAtts.viewAngle = 30
View3DAtts.parallelScale = 724.078
View3DAtts.nearPlane = -1448.16
View3DAtts.farPlane = 1448.16
View3DAtts.imagePan = (0, 0)
View3DAtts.imageZoom = 17.4494
View3DAtts.perspective = 1
View3DAtts.eyeAngle = 2
View3DAtts.centerOfRotationSet = 0
View3DAtts.centerOfRotation = (512, 512, 5.55112e-17)
View3DAtts.axis3DScaleFlag = 0
View3DAtts.axis3DScales = (1, 1, 1)
View3DAtts.shear = (0, 0, 1)
View3DAtts.windowValid = 1
SetView3D(View3DAtts)
# End spontaneous state

# Begin spontaneous state
View3DAtts = View3DAttributes()
View3DAtts.viewNormal = (-0.224409, -0.808096, 0.54463)
View3DAtts.focus = (512, 512, 5.55112e-17)
View3DAtts.viewUp = (0.0555088, 0.547377, 0.835043)
View3DAtts.viewAngle = 30
View3DAtts.parallelScale = 724.078
View3DAtts.nearPlane = -1448.16
View3DAtts.farPlane = 1448.16
View3DAtts.imagePan = (0, 0)
View3DAtts.imageZoom = 14.421
View3DAtts.perspective = 1
View3DAtts.eyeAngle = 2
View3DAtts.centerOfRotationSet = 0
View3DAtts.centerOfRotation = (512, 512, 5.55112e-17)
View3DAtts.axis3DScaleFlag = 0
View3DAtts.axis3DScales = (1, 1, 1)
View3DAtts.shear = (0, 0, 1)
View3DAtts.windowValid = 1
SetView3D(View3DAtts)
# End spontaneous state

# Begin spontaneous state
View3DAtts = View3DAttributes()
View3DAtts.viewNormal = (-0.224409, -0.808096, 0.54463)
View3DAtts.focus = (512, 512, 5.55112e-17)
View3DAtts.viewUp = (0.0555088, 0.547377, 0.835043)
View3DAtts.viewAngle = 30
View3DAtts.parallelScale = 724.078
View3DAtts.nearPlane = -1448.16
View3DAtts.farPlane = 1448.16
View3DAtts.imagePan = (0, 0)
View3DAtts.imageZoom = 17.4494
View3DAtts.perspective = 1
View3DAtts.eyeAngle = 2
View3DAtts.centerOfRotationSet = 0
View3DAtts.centerOfRotation = (512, 512, 5.55112e-17)
View3DAtts.axis3DScaleFlag = 0
View3DAtts.axis3DScales = (1, 1, 1)
View3DAtts.shear = (0, 0, 1)
View3DAtts.windowValid = 1
SetView3D(View3DAtts)
# End spontaneous state

# Begin spontaneous state
View3DAtts = View3DAttributes()
View3DAtts.viewNormal = (-0.224409, -0.808096, 0.54463)
View3DAtts.focus = (512, 512, 5.55112e-17)
View3DAtts.viewUp = (0.0555088, 0.547377, 0.835043)
View3DAtts.viewAngle = 30
View3DAtts.parallelScale = 724.078
View3DAtts.nearPlane = -1448.16
View3DAtts.farPlane = 1448.16
View3DAtts.imagePan = (0, 0)
View3DAtts.imageZoom = 21.1138
View3DAtts.perspective = 1
View3DAtts.eyeAngle = 2
View3DAtts.centerOfRotationSet = 0
View3DAtts.centerOfRotation = (512, 512, 5.55112e-17)
View3DAtts.axis3DScaleFlag = 0
View3DAtts.axis3DScales = (1, 1, 1)
View3DAtts.shear = (0, 0, 1)
View3DAtts.windowValid = 1
SetView3D(View3DAtts)
# End spontaneous state

# Begin spontaneous state
View3DAtts = View3DAttributes()
View3DAtts.viewNormal = (-0.224409, -0.808096, 0.54463)
View3DAtts.focus = (512, 512, 5.55112e-17)
View3DAtts.viewUp = (0.0555088, 0.547377, 0.835043)
View3DAtts.viewAngle = 30
View3DAtts.parallelScale = 724.078
View3DAtts.nearPlane = -1448.16
View3DAtts.farPlane = 1448.16
View3DAtts.imagePan = (0, 0)
View3DAtts.imageZoom = 17.4494
View3DAtts.perspective = 1
View3DAtts.eyeAngle = 2
View3DAtts.centerOfRotationSet = 0
View3DAtts.centerOfRotation = (512, 512, 5.55112e-17)
View3DAtts.axis3DScaleFlag = 0
View3DAtts.axis3DScales = (1, 1, 1)
View3DAtts.shear = (0, 0, 1)
View3DAtts.windowValid = 1
SetView3D(View3DAtts)
# End spontaneous state

# Begin spontaneous state
View3DAtts = View3DAttributes()
View3DAtts.viewNormal = (-0.224409, -0.808096, 0.54463)
View3DAtts.focus = (512, 512, 5.55112e-17)
View3DAtts.viewUp = (0.0555088, 0.547377, 0.835043)
View3DAtts.viewAngle = 30
View3DAtts.parallelScale = 724.078
View3DAtts.nearPlane = -1448.16
View3DAtts.farPlane = 1448.16
View3DAtts.imagePan = (0, 0)
View3DAtts.imageZoom = 14.421
View3DAtts.perspective = 1
View3DAtts.eyeAngle = 2
View3DAtts.centerOfRotationSet = 0
View3DAtts.centerOfRotation = (512, 512, 5.55112e-17)
View3DAtts.axis3DScaleFlag = 0
View3DAtts.axis3DScales = (1, 1, 1)
View3DAtts.shear = (0, 0, 1)
View3DAtts.windowValid = 1
SetView3D(View3DAtts)
# End spontaneous state

# Begin spontaneous state
View3DAtts = View3DAttributes()
View3DAtts.viewNormal = (-0.242425, -0.780239, 0.576591)
View3DAtts.focus = (512, 512, 5.55112e-17)
View3DAtts.viewUp = (0.0615999, 0.580741, 0.811754)
View3DAtts.viewAngle = 30
View3DAtts.parallelScale = 724.078
View3DAtts.nearPlane = -1448.16
View3DAtts.farPlane = 1448.16
View3DAtts.imagePan = (0, 0)
View3DAtts.imageZoom = 14.421
View3DAtts.perspective = 1
View3DAtts.eyeAngle = 2
View3DAtts.centerOfRotationSet = 0
View3DAtts.centerOfRotation = (512, 512, 5.55112e-17)
View3DAtts.axis3DScaleFlag = 0
View3DAtts.axis3DScales = (1, 1, 1)
View3DAtts.shear = (0, 0, 1)
View3DAtts.windowValid = 1
SetView3D(View3DAtts)
# End spontaneous state

# Begin spontaneous state
View3DAtts = View3DAttributes()
View3DAtts.viewNormal = (-0.242425, -0.780239, 0.576591)
View3DAtts.focus = (512, 512, 5.55112e-17)
View3DAtts.viewUp = (0.0615999, 0.580741, 0.811754)
View3DAtts.viewAngle = 30
View3DAtts.parallelScale = 724.078
View3DAtts.nearPlane = -1448.16
View3DAtts.farPlane = 1448.16
View3DAtts.imagePan = (0, 0)
View3DAtts.imageZoom = 14.421
View3DAtts.perspective = 1
View3DAtts.eyeAngle = 2
View3DAtts.centerOfRotationSet = 0
View3DAtts.centerOfRotation = (512, 512, 5.55112e-17)
View3DAtts.axis3DScaleFlag = 0
View3DAtts.axis3DScales = (1, 1, 1)
View3DAtts.shear = (0, 0, 1)
View3DAtts.windowValid = 1
SetView3D(View3DAtts)
# End spontaneous state

ViewCurveAtts = ViewCurveAttributes()
ViewCurveAtts.domainCoords = (0, 1)
ViewCurveAtts.rangeCoords = (0, 1)
ViewCurveAtts.viewportCoords = (0.2, 0.95, 0.15, 0.95)
ViewCurveAtts.domainScale = ViewCurveAtts.LINEAR  # LINEAR, LOG
ViewCurveAtts.rangeScale = ViewCurveAtts.LINEAR  # LINEAR, LOG
SetViewCurve(ViewCurveAtts)
View2DAtts = View2DAttributes()
View2DAtts.windowCoords = (456, 568, 456, 568)
View2DAtts.viewportCoords = (0.2, 0.95, 0.15, 0.95)
View2DAtts.fullFrameActivationMode = View2DAtts.Auto  # On, Off, Auto
View2DAtts.fullFrameAutoThreshold = 100
View2DAtts.xScale = View2DAtts.LINEAR  # LINEAR, LOG
View2DAtts.yScale = View2DAtts.LINEAR  # LINEAR, LOG
View2DAtts.windowValid = 1
SetView2D(View2DAtts)
View3DAtts = View3DAttributes()
View3DAtts.viewNormal = (-0.242425, -0.780239, 0.576591)
View3DAtts.focus = (512, 512, 5.55112e-17)
View3DAtts.viewUp = (0.0615999, 0.580741, 0.811754)
View3DAtts.viewAngle = 30
View3DAtts.parallelScale = 724.078
View3DAtts.nearPlane = -1448.16
View3DAtts.farPlane = 1448.16
View3DAtts.imagePan = (0, 0)
View3DAtts.imageZoom = 14.421
View3DAtts.perspective = 1
View3DAtts.eyeAngle = 2
View3DAtts.centerOfRotationSet = 0
View3DAtts.centerOfRotation = (512, 512, 5.55112e-17)
View3DAtts.axis3DScaleFlag = 0
View3DAtts.axis3DScales = (1, 1, 1)
View3DAtts.shear = (0, 0, 1)
View3DAtts.windowValid = 1
SetView3D(View3DAtts)
ViewAxisArrayAtts = ViewAxisArrayAttributes()
ViewAxisArrayAtts.domainCoords = (0, 1)
ViewAxisArrayAtts.rangeCoords = (0, 1)
ViewAxisArrayAtts.viewportCoords = (0.15, 0.9, 0.1, 0.85)
SetViewAxisArray(ViewAxisArrayAtts)
SetViewExtentsType(1)
# Begin spontaneous state
View3DAtts = View3DAttributes()
View3DAtts.viewNormal = (-0.242425, -0.780239, 0.576591)
View3DAtts.focus = (512, 512, 0)
View3DAtts.viewUp = (0.0615999, 0.580741, 0.811754)
View3DAtts.viewAngle = 30
View3DAtts.parallelScale = 724.078
View3DAtts.nearPlane = -1448.16
View3DAtts.farPlane = 1448.16
View3DAtts.imagePan = (0, 0)
View3DAtts.imageZoom = 14.421
View3DAtts.perspective = 1
View3DAtts.eyeAngle = 2
View3DAtts.centerOfRotationSet = 0
View3DAtts.centerOfRotation = (512, 512, 0)
View3DAtts.axis3DScaleFlag = 0
View3DAtts.axis3DScales = (1, 1, 1)
View3DAtts.shear = (0, 0, 1)
View3DAtts.windowValid = 1
SetView3D(View3DAtts)
# End spontaneous state

ViewCurveAtts = ViewCurveAttributes()
ViewCurveAtts.domainCoords = (0, 1)
ViewCurveAtts.rangeCoords = (0, 1)
ViewCurveAtts.viewportCoords = (0.2, 0.95, 0.15, 0.95)
ViewCurveAtts.domainScale = ViewCurveAtts.LINEAR  # LINEAR, LOG
ViewCurveAtts.rangeScale = ViewCurveAtts.LINEAR  # LINEAR, LOG
SetViewCurve(ViewCurveAtts)
View2DAtts = View2DAttributes()
View2DAtts.windowCoords = (456, 568, 456, 568)
View2DAtts.viewportCoords = (0.2, 0.95, 0.15, 0.95)
View2DAtts.fullFrameActivationMode = View2DAtts.Auto  # On, Off, Auto
View2DAtts.fullFrameAutoThreshold = 100
View2DAtts.xScale = View2DAtts.LINEAR  # LINEAR, LOG
View2DAtts.yScale = View2DAtts.LINEAR  # LINEAR, LOG
View2DAtts.windowValid = 1
SetView2D(View2DAtts)
View3DAtts = View3DAttributes()
View3DAtts.viewNormal = (-0.242425, -0.780239, 0.576591)
View3DAtts.focus = (512, 512, 0)
View3DAtts.viewUp = (0.0615999, 0.580741, 0.811754)
View3DAtts.viewAngle = 30
View3DAtts.parallelScale = 724.078
View3DAtts.nearPlane = -1448.16
View3DAtts.farPlane = 1448.16
View3DAtts.imagePan = (0, 0)
View3DAtts.imageZoom = 14.421
View3DAtts.perspective = 1
View3DAtts.eyeAngle = 2
View3DAtts.centerOfRotationSet = 0
View3DAtts.centerOfRotation = (512, 512, 0)
View3DAtts.axis3DScaleFlag = 0
View3DAtts.axis3DScales = (1, 1, 1)
View3DAtts.shear = (0, 0, 1)
View3DAtts.windowValid = 1
SetView3D(View3DAtts)
ViewAxisArrayAtts = ViewAxisArrayAttributes()
ViewAxisArrayAtts.domainCoords = (0, 1)
ViewAxisArrayAtts.rangeCoords = (0, 1)
ViewAxisArrayAtts.viewportCoords = (0.15, 0.9, 0.1, 0.85)
SetViewAxisArray(ViewAxisArrayAtts)
# Begin spontaneous state
View3DAtts = View3DAttributes()
View3DAtts.viewNormal = (-0.242425, -0.780239, 0.576591)
View3DAtts.focus = (512, 512, 0)
View3DAtts.viewUp = (0.0615999, 0.580741, 0.811754)
View3DAtts.viewAngle = 30
View3DAtts.parallelScale = 724.078
View3DAtts.nearPlane = -1448.16
View3DAtts.farPlane = 1448.16
View3DAtts.imagePan = (0, 0)
View3DAtts.imageZoom = 14.421
View3DAtts.perspective = 1
View3DAtts.eyeAngle = 2
View3DAtts.centerOfRotationSet = 0
View3DAtts.centerOfRotation = (512, 512, 0)
View3DAtts.axis3DScaleFlag = 1
View3DAtts.axis3DScales = (1, 1, 1)
View3DAtts.shear = (0, 0, 1)
View3DAtts.windowValid = 1
SetView3D(View3DAtts)
# End spontaneous state

# Begin spontaneous state
View3DAtts = View3DAttributes()
View3DAtts.viewNormal = (-0.242425, -0.780239, 0.576591)
View3DAtts.focus = (512, 512, 0)
View3DAtts.viewUp = (0.0615999, 0.580741, 0.811754)
View3DAtts.viewAngle = 30
View3DAtts.parallelScale = 724.078
View3DAtts.nearPlane = -1448.16
View3DAtts.farPlane = 1448.16
View3DAtts.imagePan = (0, 0)
View3DAtts.imageZoom = 14.421
View3DAtts.perspective = 1
View3DAtts.eyeAngle = 2
View3DAtts.centerOfRotationSet = 0
View3DAtts.centerOfRotation = (512, 512, 0)
View3DAtts.axis3DScaleFlag = 1
View3DAtts.axis3DScales = (1, 1, 1000)
View3DAtts.shear = (0, 0, 1)
View3DAtts.windowValid = 1
SetView3D(View3DAtts)
# End spontaneous state

ViewCurveAtts = ViewCurveAttributes()
ViewCurveAtts.domainCoords = (0, 1)
ViewCurveAtts.rangeCoords = (0, 1)
ViewCurveAtts.viewportCoords = (0.2, 0.95, 0.15, 0.95)
ViewCurveAtts.domainScale = ViewCurveAtts.LINEAR  # LINEAR, LOG
ViewCurveAtts.rangeScale = ViewCurveAtts.LINEAR  # LINEAR, LOG
SetViewCurve(ViewCurveAtts)
View2DAtts = View2DAttributes()
View2DAtts.windowCoords = (456, 568, 456, 568)
View2DAtts.viewportCoords = (0.2, 0.95, 0.15, 0.95)
View2DAtts.fullFrameActivationMode = View2DAtts.Auto  # On, Off, Auto
View2DAtts.fullFrameAutoThreshold = 100
View2DAtts.xScale = View2DAtts.LINEAR  # LINEAR, LOG
View2DAtts.yScale = View2DAtts.LINEAR  # LINEAR, LOG
View2DAtts.windowValid = 1
SetView2D(View2DAtts)
View3DAtts = View3DAttributes()
View3DAtts.viewNormal = (-0.242425, -0.780239, 0.576591)
View3DAtts.focus = (512, 512, 0)
View3DAtts.viewUp = (0.0615999, 0.580741, 0.811754)
View3DAtts.viewAngle = 30
View3DAtts.parallelScale = 724.078
View3DAtts.nearPlane = -1448.16
View3DAtts.farPlane = 1448.16
View3DAtts.imagePan = (0, 0)
View3DAtts.imageZoom = 14.421
View3DAtts.perspective = 1
View3DAtts.eyeAngle = 2
View3DAtts.centerOfRotationSet = 0
View3DAtts.centerOfRotation = (512, 512, 0)
View3DAtts.axis3DScaleFlag = 1
View3DAtts.axis3DScales = (1, 1, 1000)
View3DAtts.shear = (0, 0, 1)
View3DAtts.windowValid = 1
SetView3D(View3DAtts)
ViewAxisArrayAtts = ViewAxisArrayAttributes()
ViewAxisArrayAtts.domainCoords = (0, 1)
ViewAxisArrayAtts.rangeCoords = (0, 1)
ViewAxisArrayAtts.viewportCoords = (0.15, 0.9, 0.1, 0.85)
SetViewAxisArray(ViewAxisArrayAtts)
# Begin spontaneous state
View3DAtts = View3DAttributes()
View3DAtts.viewNormal = (-0.242425, -0.780239, 0.576591)
View3DAtts.focus = (512, 512, 0)
View3DAtts.viewUp = (0.0615999, 0.580741, 0.811754)
View3DAtts.viewAngle = 30
View3DAtts.parallelScale = 724.078
View3DAtts.nearPlane = -1448.16
View3DAtts.farPlane = 1448.16
View3DAtts.imagePan = (0, 0)
View3DAtts.imageZoom = 14.421
View3DAtts.perspective = 1
View3DAtts.eyeAngle = 2
View3DAtts.centerOfRotationSet = 0
View3DAtts.centerOfRotation = (512, 512, 0)
View3DAtts.axis3DScaleFlag = 1
View3DAtts.axis3DScales = (1, 1, 100)
View3DAtts.shear = (0, 0, 1)
View3DAtts.windowValid = 1
SetView3D(View3DAtts)
# End spontaneous state

ViewCurveAtts = ViewCurveAttributes()
ViewCurveAtts.domainCoords = (0, 1)
ViewCurveAtts.rangeCoords = (0, 1)
ViewCurveAtts.viewportCoords = (0.2, 0.95, 0.15, 0.95)
ViewCurveAtts.domainScale = ViewCurveAtts.LINEAR  # LINEAR, LOG
ViewCurveAtts.rangeScale = ViewCurveAtts.LINEAR  # LINEAR, LOG
SetViewCurve(ViewCurveAtts)
View2DAtts = View2DAttributes()
View2DAtts.windowCoords = (456, 568, 456, 568)
View2DAtts.viewportCoords = (0.2, 0.95, 0.15, 0.95)
View2DAtts.fullFrameActivationMode = View2DAtts.Auto  # On, Off, Auto
View2DAtts.fullFrameAutoThreshold = 100
View2DAtts.xScale = View2DAtts.LINEAR  # LINEAR, LOG
View2DAtts.yScale = View2DAtts.LINEAR  # LINEAR, LOG
View2DAtts.windowValid = 1
SetView2D(View2DAtts)
View3DAtts = View3DAttributes()
View3DAtts.viewNormal = (-0.242425, -0.780239, 0.576591)
View3DAtts.focus = (512, 512, 0)
View3DAtts.viewUp = (0.0615999, 0.580741, 0.811754)
View3DAtts.viewAngle = 30
View3DAtts.parallelScale = 724.078
View3DAtts.nearPlane = -1448.16
View3DAtts.farPlane = 1448.16
View3DAtts.imagePan = (0, 0)
View3DAtts.imageZoom = 14.421
View3DAtts.perspective = 1
View3DAtts.eyeAngle = 2
View3DAtts.centerOfRotationSet = 0
View3DAtts.centerOfRotation = (512, 512, 0)
View3DAtts.axis3DScaleFlag = 1
View3DAtts.axis3DScales = (1, 1, 100)
View3DAtts.shear = (0, 0, 1)
View3DAtts.windowValid = 1
SetView3D(View3DAtts)
ViewAxisArrayAtts = ViewAxisArrayAttributes()
ViewAxisArrayAtts.domainCoords = (0, 1)
ViewAxisArrayAtts.rangeCoords = (0, 1)
ViewAxisArrayAtts.viewportCoords = (0.15, 0.9, 0.1, 0.85)
SetViewAxisArray(ViewAxisArrayAtts)
# Begin spontaneous state
View3DAtts = View3DAttributes()
View3DAtts.viewNormal = (-0.242425, -0.780239, 0.576591)
View3DAtts.focus = (512, 512, 0)
View3DAtts.viewUp = (0.0615999, 0.580741, 0.811754)
View3DAtts.viewAngle = 30
View3DAtts.parallelScale = 724.078
View3DAtts.nearPlane = -1448.16
View3DAtts.farPlane = 1448.16
View3DAtts.imagePan = (0, 0)
View3DAtts.imageZoom = 14.421
View3DAtts.perspective = 1
View3DAtts.eyeAngle = 2
View3DAtts.centerOfRotationSet = 0
View3DAtts.centerOfRotation = (512, 512, 0)
View3DAtts.axis3DScaleFlag = 1
View3DAtts.axis3DScales = (1, 1, 10)
View3DAtts.shear = (0, 0, 1)
View3DAtts.windowValid = 1
SetView3D(View3DAtts)
# End spontaneous state

ViewCurveAtts = ViewCurveAttributes()
ViewCurveAtts.domainCoords = (0, 1)
ViewCurveAtts.rangeCoords = (0, 1)
ViewCurveAtts.viewportCoords = (0.2, 0.95, 0.15, 0.95)
ViewCurveAtts.domainScale = ViewCurveAtts.LINEAR  # LINEAR, LOG
ViewCurveAtts.rangeScale = ViewCurveAtts.LINEAR  # LINEAR, LOG
SetViewCurve(ViewCurveAtts)
View2DAtts = View2DAttributes()
View2DAtts.windowCoords = (456, 568, 456, 568)
View2DAtts.viewportCoords = (0.2, 0.95, 0.15, 0.95)
View2DAtts.fullFrameActivationMode = View2DAtts.Auto  # On, Off, Auto
View2DAtts.fullFrameAutoThreshold = 100
View2DAtts.xScale = View2DAtts.LINEAR  # LINEAR, LOG
View2DAtts.yScale = View2DAtts.LINEAR  # LINEAR, LOG
View2DAtts.windowValid = 1
SetView2D(View2DAtts)
View3DAtts = View3DAttributes()
View3DAtts.viewNormal = (-0.242425, -0.780239, 0.576591)
View3DAtts.focus = (512, 512, 0)
View3DAtts.viewUp = (0.0615999, 0.580741, 0.811754)
View3DAtts.viewAngle = 30
View3DAtts.parallelScale = 724.078
View3DAtts.nearPlane = -1448.16
View3DAtts.farPlane = 1448.16
View3DAtts.imagePan = (0, 0)
View3DAtts.imageZoom = 14.421
View3DAtts.perspective = 1
View3DAtts.eyeAngle = 2
View3DAtts.centerOfRotationSet = 0
View3DAtts.centerOfRotation = (512, 512, 0)
View3DAtts.axis3DScaleFlag = 1
View3DAtts.axis3DScales = (1, 1, 10)
View3DAtts.shear = (0, 0, 1)
View3DAtts.windowValid = 1
SetView3D(View3DAtts)
ViewAxisArrayAtts = ViewAxisArrayAttributes()
ViewAxisArrayAtts.domainCoords = (0, 1)
ViewAxisArrayAtts.rangeCoords = (0, 1)
ViewAxisArrayAtts.viewportCoords = (0.15, 0.9, 0.1, 0.85)
SetViewAxisArray(ViewAxisArrayAtts)
# Begin spontaneous state
View3DAtts = View3DAttributes()
View3DAtts.viewNormal = (-0.242425, -0.780239, 0.576591)
View3DAtts.focus = (512, 512, 0)
View3DAtts.viewUp = (0.0615999, 0.580741, 0.811754)
View3DAtts.viewAngle = 30
View3DAtts.parallelScale = 724.078
View3DAtts.nearPlane = -1448.16
View3DAtts.farPlane = 1448.16
View3DAtts.imagePan = (0, 0)
View3DAtts.imageZoom = 14.421
View3DAtts.perspective = 1
View3DAtts.eyeAngle = 2
View3DAtts.centerOfRotationSet = 0
View3DAtts.centerOfRotation = (512, 512, 0)
View3DAtts.axis3DScaleFlag = 1
View3DAtts.axis3DScales = (1, 1, 20)
View3DAtts.shear = (0, 0, 1)
View3DAtts.windowValid = 1
SetView3D(View3DAtts)
# End spontaneous state

ViewCurveAtts = ViewCurveAttributes()
ViewCurveAtts.domainCoords = (0, 1)
ViewCurveAtts.rangeCoords = (0, 1)
ViewCurveAtts.viewportCoords = (0.2, 0.95, 0.15, 0.95)
ViewCurveAtts.domainScale = ViewCurveAtts.LINEAR  # LINEAR, LOG
ViewCurveAtts.rangeScale = ViewCurveAtts.LINEAR  # LINEAR, LOG
SetViewCurve(ViewCurveAtts)
View2DAtts = View2DAttributes()
View2DAtts.windowCoords = (456, 568, 456, 568)
View2DAtts.viewportCoords = (0.2, 0.95, 0.15, 0.95)
View2DAtts.fullFrameActivationMode = View2DAtts.Auto  # On, Off, Auto
View2DAtts.fullFrameAutoThreshold = 100
View2DAtts.xScale = View2DAtts.LINEAR  # LINEAR, LOG
View2DAtts.yScale = View2DAtts.LINEAR  # LINEAR, LOG
View2DAtts.windowValid = 1
SetView2D(View2DAtts)
View3DAtts = View3DAttributes()
View3DAtts.viewNormal = (-0.242425, -0.780239, 0.576591)
View3DAtts.focus = (512, 512, 0)
View3DAtts.viewUp = (0.0615999, 0.580741, 0.811754)
View3DAtts.viewAngle = 30
View3DAtts.parallelScale = 724.078
View3DAtts.nearPlane = -1448.16
View3DAtts.farPlane = 1448.16
View3DAtts.imagePan = (0, 0)
View3DAtts.imageZoom = 14.421
View3DAtts.perspective = 1
View3DAtts.eyeAngle = 2
View3DAtts.centerOfRotationSet = 0
View3DAtts.centerOfRotation = (512, 512, 0)
View3DAtts.axis3DScaleFlag = 1
View3DAtts.axis3DScales = (1, 1, 20)
View3DAtts.shear = (0, 0, 1)
View3DAtts.windowValid = 1
SetView3D(View3DAtts)
ViewAxisArrayAtts = ViewAxisArrayAttributes()
ViewAxisArrayAtts.domainCoords = (0, 1)
ViewAxisArrayAtts.rangeCoords = (0, 1)
ViewAxisArrayAtts.viewportCoords = (0.15, 0.9, 0.1, 0.85)
SetViewAxisArray(ViewAxisArrayAtts)
# Begin spontaneous state
View3DAtts = View3DAttributes()
View3DAtts.viewNormal = (-0.242425, -0.780239, 0.576591)
View3DAtts.focus = (512, 512, 0)
View3DAtts.viewUp = (0.0615999, 0.580741, 0.811754)
View3DAtts.viewAngle = 30
View3DAtts.parallelScale = 724.078
View3DAtts.nearPlane = -1448.16
View3DAtts.farPlane = 1448.16
View3DAtts.imagePan = (0, 0)
View3DAtts.imageZoom = 11.9182
View3DAtts.perspective = 1
View3DAtts.eyeAngle = 2
View3DAtts.centerOfRotationSet = 0
View3DAtts.centerOfRotation = (512, 512, 0)
View3DAtts.axis3DScaleFlag = 1
View3DAtts.axis3DScales = (1, 1, 20)
View3DAtts.shear = (0, 0, 1)
View3DAtts.windowValid = 1
SetView3D(View3DAtts)
# End spontaneous state

# Begin spontaneous state
View3DAtts = View3DAttributes()
View3DAtts.viewNormal = (-0.242425, -0.780239, 0.576591)
View3DAtts.focus = (512, 512, 0)
View3DAtts.viewUp = (0.0615999, 0.580741, 0.811754)
View3DAtts.viewAngle = 30
View3DAtts.parallelScale = 724.078
View3DAtts.nearPlane = -1448.16
View3DAtts.farPlane = 1448.16
View3DAtts.imagePan = (0, 0)
View3DAtts.imageZoom = 9.84974
View3DAtts.perspective = 1
View3DAtts.eyeAngle = 2
View3DAtts.centerOfRotationSet = 0
View3DAtts.centerOfRotation = (512, 512, 0)
View3DAtts.axis3DScaleFlag = 1
View3DAtts.axis3DScales = (1, 1, 20)
View3DAtts.shear = (0, 0, 1)
View3DAtts.windowValid = 1
SetView3D(View3DAtts)
# End spontaneous state

# Begin spontaneous state
View3DAtts = View3DAttributes()
View3DAtts.viewNormal = (-0.242425, -0.780239, 0.576591)
View3DAtts.focus = (512, 512, 0)
View3DAtts.viewUp = (0.0615999, 0.580741, 0.811754)
View3DAtts.viewAngle = 30
View3DAtts.parallelScale = 724.078
View3DAtts.nearPlane = -1448.16
View3DAtts.farPlane = 1448.16
View3DAtts.imagePan = (0, 0)
View3DAtts.imageZoom = 8.14028
View3DAtts.perspective = 1
View3DAtts.eyeAngle = 2
View3DAtts.centerOfRotationSet = 0
View3DAtts.centerOfRotation = (512, 512, 0)
View3DAtts.axis3DScaleFlag = 1
View3DAtts.axis3DScales = (1, 1, 20)
View3DAtts.shear = (0, 0, 1)
View3DAtts.windowValid = 1
SetView3D(View3DAtts)
# End spontaneous state

# Begin spontaneous state
View3DAtts = View3DAttributes()
View3DAtts.viewNormal = (-0.242425, -0.780239, 0.576591)
View3DAtts.focus = (512, 512, 0)
View3DAtts.viewUp = (0.0615999, 0.580741, 0.811754)
View3DAtts.viewAngle = 30
View3DAtts.parallelScale = 724.078
View3DAtts.nearPlane = -1448.16
View3DAtts.farPlane = 1448.16
View3DAtts.imagePan = (0, 0)
View3DAtts.imageZoom = 6.7275
View3DAtts.perspective = 1
View3DAtts.eyeAngle = 2
View3DAtts.centerOfRotationSet = 0
View3DAtts.centerOfRotation = (512, 512, 0)
View3DAtts.axis3DScaleFlag = 1
View3DAtts.axis3DScales = (1, 1, 20)
View3DAtts.shear = (0, 0, 1)
View3DAtts.windowValid = 1
SetView3D(View3DAtts)
# End spontaneous state

# Begin spontaneous state
View3DAtts = View3DAttributes()
View3DAtts.viewNormal = (-0.242425, -0.780239, 0.576591)
View3DAtts.focus = (512, 512, 0)
View3DAtts.viewUp = (0.0615999, 0.580741, 0.811754)
View3DAtts.viewAngle = 30
View3DAtts.parallelScale = 724.078
View3DAtts.nearPlane = -1448.16
View3DAtts.farPlane = 1448.16
View3DAtts.imagePan = (0, 0)
View3DAtts.imageZoom = 5.55992
View3DAtts.perspective = 1
View3DAtts.eyeAngle = 2
View3DAtts.centerOfRotationSet = 0
View3DAtts.centerOfRotation = (512, 512, 0)
View3DAtts.axis3DScaleFlag = 1
View3DAtts.axis3DScales = (1, 1, 20)
View3DAtts.shear = (0, 0, 1)
View3DAtts.windowValid = 1
SetView3D(View3DAtts)
# End spontaneous state

# Begin spontaneous state
View3DAtts = View3DAttributes()
View3DAtts.viewNormal = (-0.242425, -0.780239, 0.576591)
View3DAtts.focus = (512, 512, 0)
View3DAtts.viewUp = (0.0615999, 0.580741, 0.811754)
View3DAtts.viewAngle = 30
View3DAtts.parallelScale = 724.078
View3DAtts.nearPlane = -1448.16
View3DAtts.farPlane = 1448.16
View3DAtts.imagePan = (0, 0)
View3DAtts.imageZoom = 4.59498
View3DAtts.perspective = 1
View3DAtts.eyeAngle = 2
View3DAtts.centerOfRotationSet = 0
View3DAtts.centerOfRotation = (512, 512, 0)
View3DAtts.axis3DScaleFlag = 1
View3DAtts.axis3DScales = (1, 1, 20)
View3DAtts.shear = (0, 0, 1)
View3DAtts.windowValid = 1
SetView3D(View3DAtts)
# End spontaneous state

# Begin spontaneous state
View3DAtts = View3DAttributes()
View3DAtts.viewNormal = (-0.242425, -0.780239, 0.576591)
View3DAtts.focus = (512, 512, 0)
View3DAtts.viewUp = (0.0615999, 0.580741, 0.811754)
View3DAtts.viewAngle = 30
View3DAtts.parallelScale = 724.078
View3DAtts.nearPlane = -1448.16
View3DAtts.farPlane = 1448.16
View3DAtts.imagePan = (0, 0)
View3DAtts.imageZoom = 3.7975
View3DAtts.perspective = 1
View3DAtts.eyeAngle = 2
View3DAtts.centerOfRotationSet = 0
View3DAtts.centerOfRotation = (512, 512, 0)
View3DAtts.axis3DScaleFlag = 1
View3DAtts.axis3DScales = (1, 1, 20)
View3DAtts.shear = (0, 0, 1)
View3DAtts.windowValid = 1
SetView3D(View3DAtts)
# End spontaneous state

# Begin spontaneous state
View3DAtts = View3DAttributes()
View3DAtts.viewNormal = (-0.242425, -0.780239, 0.576591)
View3DAtts.focus = (512, 512, 0)
View3DAtts.viewUp = (0.0615999, 0.580741, 0.811754)
View3DAtts.viewAngle = 30
View3DAtts.parallelScale = 724.078
View3DAtts.nearPlane = -1448.16
View3DAtts.farPlane = 1448.16
View3DAtts.imagePan = (0, 0)
View3DAtts.imageZoom = 3.13843
View3DAtts.perspective = 1
View3DAtts.eyeAngle = 2
View3DAtts.centerOfRotationSet = 0
View3DAtts.centerOfRotation = (512, 512, 0)
View3DAtts.axis3DScaleFlag = 1
View3DAtts.axis3DScales = (1, 1, 20)
View3DAtts.shear = (0, 0, 1)
View3DAtts.windowValid = 1
SetView3D(View3DAtts)
# End spontaneous state

# Begin spontaneous state
View3DAtts = View3DAttributes()
View3DAtts.viewNormal = (-0.242425, -0.780239, 0.576591)
View3DAtts.focus = (512, 512, 0)
View3DAtts.viewUp = (0.0615999, 0.580741, 0.811754)
View3DAtts.viewAngle = 30
View3DAtts.parallelScale = 724.078
View3DAtts.nearPlane = -1448.16
View3DAtts.farPlane = 1448.16
View3DAtts.imagePan = (0, 0)
View3DAtts.imageZoom = 2.59374
View3DAtts.perspective = 1
View3DAtts.eyeAngle = 2
View3DAtts.centerOfRotationSet = 0
View3DAtts.centerOfRotation = (512, 512, 0)
View3DAtts.axis3DScaleFlag = 1
View3DAtts.axis3DScales = (1, 1, 20)
View3DAtts.shear = (0, 0, 1)
View3DAtts.windowValid = 1
SetView3D(View3DAtts)
# End spontaneous state

# Begin spontaneous state
View3DAtts = View3DAttributes()
View3DAtts.viewNormal = (-0.242425, -0.780239, 0.576591)
View3DAtts.focus = (512, 512, 0)
View3DAtts.viewUp = (0.0615999, 0.580741, 0.811754)
View3DAtts.viewAngle = 30
View3DAtts.parallelScale = 724.078
View3DAtts.nearPlane = -1448.16
View3DAtts.farPlane = 1448.16
View3DAtts.imagePan = (0, 0)
View3DAtts.imageZoom = 2.14359
View3DAtts.perspective = 1
View3DAtts.eyeAngle = 2
View3DAtts.centerOfRotationSet = 0
View3DAtts.centerOfRotation = (512, 512, 0)
View3DAtts.axis3DScaleFlag = 1
View3DAtts.axis3DScales = (1, 1, 20)
View3DAtts.shear = (0, 0, 1)
View3DAtts.windowValid = 1
SetView3D(View3DAtts)
# End spontaneous state

# Begin spontaneous state
View3DAtts = View3DAttributes()
View3DAtts.viewNormal = (-0.242425, -0.780239, 0.576591)
View3DAtts.focus = (512, 512, 0)
View3DAtts.viewUp = (0.0615999, 0.580741, 0.811754)
View3DAtts.viewAngle = 30
View3DAtts.parallelScale = 724.078
View3DAtts.nearPlane = -1448.16
View3DAtts.farPlane = 1448.16
View3DAtts.imagePan = (0, 0)
View3DAtts.imageZoom = 1.77156
View3DAtts.perspective = 1
View3DAtts.eyeAngle = 2
View3DAtts.centerOfRotationSet = 0
View3DAtts.centerOfRotation = (512, 512, 0)
View3DAtts.axis3DScaleFlag = 1
View3DAtts.axis3DScales = (1, 1, 20)
View3DAtts.shear = (0, 0, 1)
View3DAtts.windowValid = 1
SetView3D(View3DAtts)
# End spontaneous state

# Begin spontaneous state
View3DAtts = View3DAttributes()
View3DAtts.viewNormal = (-0.242425, -0.780239, 0.576591)
View3DAtts.focus = (512, 512, 0)
View3DAtts.viewUp = (0.0615999, 0.580741, 0.811754)
View3DAtts.viewAngle = 30
View3DAtts.parallelScale = 724.078
View3DAtts.nearPlane = -1448.16
View3DAtts.farPlane = 1448.16
View3DAtts.imagePan = (0, 0)
View3DAtts.imageZoom = 1.4641
View3DAtts.perspective = 1
View3DAtts.eyeAngle = 2
View3DAtts.centerOfRotationSet = 0
View3DAtts.centerOfRotation = (512, 512, 0)
View3DAtts.axis3DScaleFlag = 1
View3DAtts.axis3DScales = (1, 1, 20)
View3DAtts.shear = (0, 0, 1)
View3DAtts.windowValid = 1
SetView3D(View3DAtts)
# End spontaneous state

# Begin spontaneous state
View3DAtts = View3DAttributes()
View3DAtts.viewNormal = (-0.242425, -0.780239, 0.576591)
View3DAtts.focus = (512, 512, 0)
View3DAtts.viewUp = (0.0615999, 0.580741, 0.811754)
View3DAtts.viewAngle = 30
View3DAtts.parallelScale = 724.078
View3DAtts.nearPlane = -1448.16
View3DAtts.farPlane = 1448.16
View3DAtts.imagePan = (0, 0)
View3DAtts.imageZoom = 1.21
View3DAtts.perspective = 1
View3DAtts.eyeAngle = 2
View3DAtts.centerOfRotationSet = 0
View3DAtts.centerOfRotation = (512, 512, 0)
View3DAtts.axis3DScaleFlag = 1
View3DAtts.axis3DScales = (1, 1, 20)
View3DAtts.shear = (0, 0, 1)
View3DAtts.windowValid = 1
SetView3D(View3DAtts)
# End spontaneous state

# Begin spontaneous state
View3DAtts = View3DAttributes()
View3DAtts.viewNormal = (-0.242425, -0.780239, 0.576591)
View3DAtts.focus = (512, 512, 0)
View3DAtts.viewUp = (0.0615999, 0.580741, 0.811754)
View3DAtts.viewAngle = 30
View3DAtts.parallelScale = 724.078
View3DAtts.nearPlane = -1448.16
View3DAtts.farPlane = 1448.16
View3DAtts.imagePan = (0, 0)
View3DAtts.imageZoom = 1
View3DAtts.perspective = 1
View3DAtts.eyeAngle = 2
View3DAtts.centerOfRotationSet = 0
View3DAtts.centerOfRotation = (512, 512, 0)
View3DAtts.axis3DScaleFlag = 1
View3DAtts.axis3DScales = (1, 1, 20)
View3DAtts.shear = (0, 0, 1)
View3DAtts.windowValid = 1
SetView3D(View3DAtts)
# End spontaneous state

# Begin spontaneous state
View3DAtts = View3DAttributes()
View3DAtts.viewNormal = (-0.242425, -0.780239, 0.576591)
View3DAtts.focus = (512, 512, 0)
View3DAtts.viewUp = (0.0615999, 0.580741, 0.811754)
View3DAtts.viewAngle = 30
View3DAtts.parallelScale = 724.078
View3DAtts.nearPlane = -1448.16
View3DAtts.farPlane = 1448.16
View3DAtts.imagePan = (0, 0)
View3DAtts.imageZoom = 0.826447
View3DAtts.perspective = 1
View3DAtts.eyeAngle = 2
View3DAtts.centerOfRotationSet = 0
View3DAtts.centerOfRotation = (512, 512, 0)
View3DAtts.axis3DScaleFlag = 1
View3DAtts.axis3DScales = (1, 1, 20)
View3DAtts.shear = (0, 0, 1)
View3DAtts.windowValid = 1
SetView3D(View3DAtts)
# End spontaneous state

# Begin spontaneous state
View3DAtts = View3DAttributes()
View3DAtts.viewNormal = (-0.242425, -0.780239, 0.576591)
View3DAtts.focus = (512, 512, 0)
View3DAtts.viewUp = (0.0615999, 0.580741, 0.811754)
View3DAtts.viewAngle = 30
View3DAtts.parallelScale = 724.078
View3DAtts.nearPlane = -1448.16
View3DAtts.farPlane = 1448.16
View3DAtts.imagePan = (0, 0)
View3DAtts.imageZoom = 0.683014
View3DAtts.perspective = 1
View3DAtts.eyeAngle = 2
View3DAtts.centerOfRotationSet = 0
View3DAtts.centerOfRotation = (512, 512, 0)
View3DAtts.axis3DScaleFlag = 1
View3DAtts.axis3DScales = (1, 1, 20)
View3DAtts.shear = (0, 0, 1)
View3DAtts.windowValid = 1
SetView3D(View3DAtts)
# End spontaneous state

# Begin spontaneous state
View3DAtts = View3DAttributes()
View3DAtts.viewNormal = (-0.242425, -0.780239, 0.576591)
View3DAtts.focus = (512, 512, 0)
View3DAtts.viewUp = (0.0615999, 0.580741, 0.811754)
View3DAtts.viewAngle = 30
View3DAtts.parallelScale = 724.078
View3DAtts.nearPlane = -1448.16
View3DAtts.farPlane = 1448.16
View3DAtts.imagePan = (0, 0)
View3DAtts.imageZoom = 0.564474
View3DAtts.perspective = 1
View3DAtts.eyeAngle = 2
View3DAtts.centerOfRotationSet = 0
View3DAtts.centerOfRotation = (512, 512, 0)
View3DAtts.axis3DScaleFlag = 1
View3DAtts.axis3DScales = (1, 1, 20)
View3DAtts.shear = (0, 0, 1)
View3DAtts.windowValid = 1
SetView3D(View3DAtts)
# End spontaneous state

# Begin spontaneous state
View3DAtts = View3DAttributes()
View3DAtts.viewNormal = (-0.242425, -0.780239, 0.576591)
View3DAtts.focus = (512, 512, 0)
View3DAtts.viewUp = (0.0615999, 0.580741, 0.811754)
View3DAtts.viewAngle = 30
View3DAtts.parallelScale = 724.078
View3DAtts.nearPlane = -1448.16
View3DAtts.farPlane = 1448.16
View3DAtts.imagePan = (0, 0)
View3DAtts.imageZoom = 0.683014
View3DAtts.perspective = 1
View3DAtts.eyeAngle = 2
View3DAtts.centerOfRotationSet = 0
View3DAtts.centerOfRotation = (512, 512, 0)
View3DAtts.axis3DScaleFlag = 1
View3DAtts.axis3DScales = (1, 1, 20)
View3DAtts.shear = (0, 0, 1)
View3DAtts.windowValid = 1
SetView3D(View3DAtts)
# End spontaneous state

# Begin spontaneous state
View3DAtts = View3DAttributes()
View3DAtts.viewNormal = (-0.242425, -0.780239, 0.576591)
View3DAtts.focus = (512, 512, 0)
View3DAtts.viewUp = (0.0615999, 0.580741, 0.811754)
View3DAtts.viewAngle = 30
View3DAtts.parallelScale = 724.078
View3DAtts.nearPlane = -1448.16
View3DAtts.farPlane = 1448.16
View3DAtts.imagePan = (0, 0)
View3DAtts.imageZoom = 0.826447
View3DAtts.perspective = 1
View3DAtts.eyeAngle = 2
View3DAtts.centerOfRotationSet = 0
View3DAtts.centerOfRotation = (512, 512, 0)
View3DAtts.axis3DScaleFlag = 1
View3DAtts.axis3DScales = (1, 1, 20)
View3DAtts.shear = (0, 0, 1)
View3DAtts.windowValid = 1
SetView3D(View3DAtts)
# End spontaneous state

# Begin spontaneous state
View3DAtts = View3DAttributes()
View3DAtts.viewNormal = (-0.242425, -0.780239, 0.576591)
View3DAtts.focus = (512, 512, 0)
View3DAtts.viewUp = (0.0615999, 0.580741, 0.811754)
View3DAtts.viewAngle = 30
View3DAtts.parallelScale = 724.078
View3DAtts.nearPlane = -1448.16
View3DAtts.farPlane = 1448.16
View3DAtts.imagePan = (0, 0)
View3DAtts.imageZoom = 1
View3DAtts.perspective = 1
View3DAtts.eyeAngle = 2
View3DAtts.centerOfRotationSet = 0
View3DAtts.centerOfRotation = (512, 512, 0)
View3DAtts.axis3DScaleFlag = 1
View3DAtts.axis3DScales = (1, 1, 20)
View3DAtts.shear = (0, 0, 1)
View3DAtts.windowValid = 1
SetView3D(View3DAtts)
# End spontaneous state

# Begin spontaneous state
View3DAtts = View3DAttributes()
View3DAtts.viewNormal = (-0.242425, -0.780239, 0.576591)
View3DAtts.focus = (512, 512, 0)
View3DAtts.viewUp = (0.0615999, 0.580741, 0.811754)
View3DAtts.viewAngle = 30
View3DAtts.parallelScale = 724.078
View3DAtts.nearPlane = -1448.16
View3DAtts.farPlane = 1448.16
View3DAtts.imagePan = (0, 0)
View3DAtts.imageZoom = 0.826447
View3DAtts.perspective = 1
View3DAtts.eyeAngle = 2
View3DAtts.centerOfRotationSet = 0
View3DAtts.centerOfRotation = (512, 512, 0)
View3DAtts.axis3DScaleFlag = 1
View3DAtts.axis3DScales = (1, 1, 20)
View3DAtts.shear = (0, 0, 1)
View3DAtts.windowValid = 1
SetView3D(View3DAtts)
# End spontaneous state

# Begin spontaneous state
View3DAtts = View3DAttributes()
View3DAtts.viewNormal = (-0.242425, -0.780239, 0.576591)
View3DAtts.focus = (512, 512, 0)
View3DAtts.viewUp = (0.0615999, 0.580741, 0.811754)
View3DAtts.viewAngle = 30
View3DAtts.parallelScale = 724.078
View3DAtts.nearPlane = -1448.16
View3DAtts.farPlane = 1448.16
View3DAtts.imagePan = (0, 0)
View3DAtts.imageZoom = 0.683014
View3DAtts.perspective = 1
View3DAtts.eyeAngle = 2
View3DAtts.centerOfRotationSet = 0
View3DAtts.centerOfRotation = (512, 512, 0)
View3DAtts.axis3DScaleFlag = 1
View3DAtts.axis3DScales = (1, 1, 20)
View3DAtts.shear = (0, 0, 1)
View3DAtts.windowValid = 1
SetView3D(View3DAtts)
# End spontaneous state

# Begin spontaneous state
View3DAtts = View3DAttributes()
View3DAtts.viewNormal = (-0.242425, -0.780239, 0.576591)
View3DAtts.focus = (512, 512, 0)
View3DAtts.viewUp = (0.0615999, 0.580741, 0.811754)
View3DAtts.viewAngle = 30
View3DAtts.parallelScale = 724.078
View3DAtts.nearPlane = -1448.16
View3DAtts.farPlane = 1448.16
View3DAtts.imagePan = (0, 0)
View3DAtts.imageZoom = 0.564474
View3DAtts.perspective = 1
View3DAtts.eyeAngle = 2
View3DAtts.centerOfRotationSet = 0
View3DAtts.centerOfRotation = (512, 512, 0)
View3DAtts.axis3DScaleFlag = 1
View3DAtts.axis3DScales = (1, 1, 20)
View3DAtts.shear = (0, 0, 1)
View3DAtts.windowValid = 1
SetView3D(View3DAtts)
# End spontaneous state

# Begin spontaneous state
View3DAtts = View3DAttributes()
View3DAtts.viewNormal = (-0.242425, -0.780239, 0.576591)
View3DAtts.focus = (512, 512, 0)
View3DAtts.viewUp = (0.0615999, 0.580741, 0.811754)
View3DAtts.viewAngle = 30
View3DAtts.parallelScale = 724.078
View3DAtts.nearPlane = -1448.16
View3DAtts.farPlane = 1448.16
View3DAtts.imagePan = (0, 0)
View3DAtts.imageZoom = 0.466508
View3DAtts.perspective = 1
View3DAtts.eyeAngle = 2
View3DAtts.centerOfRotationSet = 0
View3DAtts.centerOfRotation = (512, 512, 0)
View3DAtts.axis3DScaleFlag = 1
View3DAtts.axis3DScales = (1, 1, 20)
View3DAtts.shear = (0, 0, 1)
View3DAtts.windowValid = 1
SetView3D(View3DAtts)
# End spontaneous state

# Begin spontaneous state
View3DAtts = View3DAttributes()
View3DAtts.viewNormal = (-0.242425, -0.780239, 0.576591)
View3DAtts.focus = (512, 512, 0)
View3DAtts.viewUp = (0.0615999, 0.580741, 0.811754)
View3DAtts.viewAngle = 30
View3DAtts.parallelScale = 724.078
View3DAtts.nearPlane = -1448.16
View3DAtts.farPlane = 1448.16
View3DAtts.imagePan = (0, 0)
View3DAtts.imageZoom = 0.564474
View3DAtts.perspective = 1
View3DAtts.eyeAngle = 2
View3DAtts.centerOfRotationSet = 0
View3DAtts.centerOfRotation = (512, 512, 0)
View3DAtts.axis3DScaleFlag = 1
View3DAtts.axis3DScales = (1, 1, 20)
View3DAtts.shear = (0, 0, 1)
View3DAtts.windowValid = 1
SetView3D(View3DAtts)
# End spontaneous state

# Begin spontaneous state
View3DAtts = View3DAttributes()
View3DAtts.viewNormal = (-0.242425, -0.780239, 0.576591)
View3DAtts.focus = (512, 512, 0)
View3DAtts.viewUp = (0.0615999, 0.580741, 0.811754)
View3DAtts.viewAngle = 30
View3DAtts.parallelScale = 724.078
View3DAtts.nearPlane = -1448.16
View3DAtts.farPlane = 1448.16
View3DAtts.imagePan = (0, 0)
View3DAtts.imageZoom = 0.683014
View3DAtts.perspective = 1
View3DAtts.eyeAngle = 2
View3DAtts.centerOfRotationSet = 0
View3DAtts.centerOfRotation = (512, 512, 0)
View3DAtts.axis3DScaleFlag = 1
View3DAtts.axis3DScales = (1, 1, 20)
View3DAtts.shear = (0, 0, 1)
View3DAtts.windowValid = 1
SetView3D(View3DAtts)
# End spontaneous state

# Begin spontaneous state
View3DAtts = View3DAttributes()
View3DAtts.viewNormal = (-0.242425, -0.780239, 0.576591)
View3DAtts.focus = (512, 512, 0)
View3DAtts.viewUp = (0.0615999, 0.580741, 0.811754)
View3DAtts.viewAngle = 30
View3DAtts.parallelScale = 724.078
View3DAtts.nearPlane = -1448.16
View3DAtts.farPlane = 1448.16
View3DAtts.imagePan = (0, 0)
View3DAtts.imageZoom = 0.826447
View3DAtts.perspective = 1
View3DAtts.eyeAngle = 2
View3DAtts.centerOfRotationSet = 0
View3DAtts.centerOfRotation = (512, 512, 0)
View3DAtts.axis3DScaleFlag = 1
View3DAtts.axis3DScales = (1, 1, 20)
View3DAtts.shear = (0, 0, 1)
View3DAtts.windowValid = 1
SetView3D(View3DAtts)
# End spontaneous state

# Begin spontaneous state
View3DAtts = View3DAttributes()
View3DAtts.viewNormal = (-0.242425, -0.780239, 0.576591)
View3DAtts.focus = (512, 512, 0)
View3DAtts.viewUp = (0.0615999, 0.580741, 0.811754)
View3DAtts.viewAngle = 30
View3DAtts.parallelScale = 724.078
View3DAtts.nearPlane = -1448.16
View3DAtts.farPlane = 1448.16
View3DAtts.imagePan = (0, 0)
View3DAtts.imageZoom = 1
View3DAtts.perspective = 1
View3DAtts.eyeAngle = 2
View3DAtts.centerOfRotationSet = 0
View3DAtts.centerOfRotation = (512, 512, 0)
View3DAtts.axis3DScaleFlag = 1
View3DAtts.axis3DScales = (1, 1, 20)
View3DAtts.shear = (0, 0, 1)
View3DAtts.windowValid = 1
SetView3D(View3DAtts)
# End spontaneous state

# Begin spontaneous state
View3DAtts = View3DAttributes()
View3DAtts.viewNormal = (-0.242425, -0.780239, 0.576591)
View3DAtts.focus = (512, 512, 0)
View3DAtts.viewUp = (0.0615999, 0.580741, 0.811754)
View3DAtts.viewAngle = 30
View3DAtts.parallelScale = 724.078
View3DAtts.nearPlane = -1448.16
View3DAtts.farPlane = 1448.16
View3DAtts.imagePan = (0, 0)
View3DAtts.imageZoom = 1.21
View3DAtts.perspective = 1
View3DAtts.eyeAngle = 2
View3DAtts.centerOfRotationSet = 0
View3DAtts.centerOfRotation = (512, 512, 0)
View3DAtts.axis3DScaleFlag = 1
View3DAtts.axis3DScales = (1, 1, 20)
View3DAtts.shear = (0, 0, 1)
View3DAtts.windowValid = 1
SetView3D(View3DAtts)
# End spontaneous state

# Begin spontaneous state
View3DAtts = View3DAttributes()
View3DAtts.viewNormal = (-0.242425, -0.780239, 0.576591)
View3DAtts.focus = (512, 512, 0)
View3DAtts.viewUp = (0.0615999, 0.580741, 0.811754)
View3DAtts.viewAngle = 30
View3DAtts.parallelScale = 724.078
View3DAtts.nearPlane = -1448.16
View3DAtts.farPlane = 1448.16
View3DAtts.imagePan = (0, 0)
View3DAtts.imageZoom = 1.4641
View3DAtts.perspective = 1
View3DAtts.eyeAngle = 2
View3DAtts.centerOfRotationSet = 0
View3DAtts.centerOfRotation = (512, 512, 0)
View3DAtts.axis3DScaleFlag = 1
View3DAtts.axis3DScales = (1, 1, 20)
View3DAtts.shear = (0, 0, 1)
View3DAtts.windowValid = 1
SetView3D(View3DAtts)
# End spontaneous state

# Begin spontaneous state
View3DAtts = View3DAttributes()
View3DAtts.viewNormal = (-0.242425, -0.780239, 0.576591)
View3DAtts.focus = (512, 512, 0)
View3DAtts.viewUp = (0.0615999, 0.580741, 0.811754)
View3DAtts.viewAngle = 30
View3DAtts.parallelScale = 724.078
View3DAtts.nearPlane = -1448.16
View3DAtts.farPlane = 1448.16
View3DAtts.imagePan = (0, 0)
View3DAtts.imageZoom = 1.77156
View3DAtts.perspective = 1
View3DAtts.eyeAngle = 2
View3DAtts.centerOfRotationSet = 0
View3DAtts.centerOfRotation = (512, 512, 0)
View3DAtts.axis3DScaleFlag = 1
View3DAtts.axis3DScales = (1, 1, 20)
View3DAtts.shear = (0, 0, 1)
View3DAtts.windowValid = 1
SetView3D(View3DAtts)
# End spontaneous state

# Begin spontaneous state
View3DAtts = View3DAttributes()
View3DAtts.viewNormal = (-0.242425, -0.780239, 0.576591)
View3DAtts.focus = (512, 512, 0)
View3DAtts.viewUp = (0.0615999, 0.580741, 0.811754)
View3DAtts.viewAngle = 30
View3DAtts.parallelScale = 724.078
View3DAtts.nearPlane = -1448.16
View3DAtts.farPlane = 1448.16
View3DAtts.imagePan = (0, 0)
View3DAtts.imageZoom = 2.14359
View3DAtts.perspective = 1
View3DAtts.eyeAngle = 2
View3DAtts.centerOfRotationSet = 0
View3DAtts.centerOfRotation = (512, 512, 0)
View3DAtts.axis3DScaleFlag = 1
View3DAtts.axis3DScales = (1, 1, 20)
View3DAtts.shear = (0, 0, 1)
View3DAtts.windowValid = 1
SetView3D(View3DAtts)
# End spontaneous state

# Begin spontaneous state
View3DAtts = View3DAttributes()
View3DAtts.viewNormal = (-0.242425, -0.780239, 0.576591)
View3DAtts.focus = (512, 512, 0)
View3DAtts.viewUp = (0.0615999, 0.580741, 0.811754)
View3DAtts.viewAngle = 30
View3DAtts.parallelScale = 724.078
View3DAtts.nearPlane = -1448.16
View3DAtts.farPlane = 1448.16
View3DAtts.imagePan = (0, 0)
View3DAtts.imageZoom = 2.59374
View3DAtts.perspective = 1
View3DAtts.eyeAngle = 2
View3DAtts.centerOfRotationSet = 0
View3DAtts.centerOfRotation = (512, 512, 0)
View3DAtts.axis3DScaleFlag = 1
View3DAtts.axis3DScales = (1, 1, 20)
View3DAtts.shear = (0, 0, 1)
View3DAtts.windowValid = 1
SetView3D(View3DAtts)
# End spontaneous state

# Begin spontaneous state
View3DAtts = View3DAttributes()
View3DAtts.viewNormal = (-0.242425, -0.780239, 0.576591)
View3DAtts.focus = (512, 512, 0)
View3DAtts.viewUp = (0.0615999, 0.580741, 0.811754)
View3DAtts.viewAngle = 30
View3DAtts.parallelScale = 724.078
View3DAtts.nearPlane = -1448.16
View3DAtts.farPlane = 1448.16
View3DAtts.imagePan = (0, 0)
View3DAtts.imageZoom = 2.14359
View3DAtts.perspective = 1
View3DAtts.eyeAngle = 2
View3DAtts.centerOfRotationSet = 0
View3DAtts.centerOfRotation = (512, 512, 0)
View3DAtts.axis3DScaleFlag = 1
View3DAtts.axis3DScales = (1, 1, 20)
View3DAtts.shear = (0, 0, 1)
View3DAtts.windowValid = 1
SetView3D(View3DAtts)
# End spontaneous state

# Begin spontaneous state
View3DAtts = View3DAttributes()
View3DAtts.viewNormal = (-0.242425, -0.780239, 0.576591)
View3DAtts.focus = (512, 512, 0)
View3DAtts.viewUp = (0.0615999, 0.580741, 0.811754)
View3DAtts.viewAngle = 30
View3DAtts.parallelScale = 724.078
View3DAtts.nearPlane = -1448.16
View3DAtts.farPlane = 1448.16
View3DAtts.imagePan = (0, 0)
View3DAtts.imageZoom = 1.77156
View3DAtts.perspective = 1
View3DAtts.eyeAngle = 2
View3DAtts.centerOfRotationSet = 0
View3DAtts.centerOfRotation = (512, 512, 0)
View3DAtts.axis3DScaleFlag = 1
View3DAtts.axis3DScales = (1, 1, 20)
View3DAtts.shear = (0, 0, 1)
View3DAtts.windowValid = 1
SetView3D(View3DAtts)
# End spontaneous state

# Begin spontaneous state
View3DAtts = View3DAttributes()
View3DAtts.viewNormal = (-0.242425, -0.780239, 0.576591)
View3DAtts.focus = (512, 512, 0)
View3DAtts.viewUp = (0.0615999, 0.580741, 0.811754)
View3DAtts.viewAngle = 30
View3DAtts.parallelScale = 724.078
View3DAtts.nearPlane = -1448.16
View3DAtts.farPlane = 1448.16
View3DAtts.imagePan = (0, 0)
View3DAtts.imageZoom = 1.4641
View3DAtts.perspective = 1
View3DAtts.eyeAngle = 2
View3DAtts.centerOfRotationSet = 0
View3DAtts.centerOfRotation = (512, 512, 0)
View3DAtts.axis3DScaleFlag = 1
View3DAtts.axis3DScales = (1, 1, 20)
View3DAtts.shear = (0, 0, 1)
View3DAtts.windowValid = 1
SetView3D(View3DAtts)
# End spontaneous state

# Begin spontaneous state
View3DAtts = View3DAttributes()
View3DAtts.viewNormal = (-0.242425, -0.780239, 0.576591)
View3DAtts.focus = (512, 512, 0)
View3DAtts.viewUp = (0.0615999, 0.580741, 0.811754)
View3DAtts.viewAngle = 30
View3DAtts.parallelScale = 724.078
View3DAtts.nearPlane = -1448.16
View3DAtts.farPlane = 1448.16
View3DAtts.imagePan = (0, 0)
View3DAtts.imageZoom = 1.21
View3DAtts.perspective = 1
View3DAtts.eyeAngle = 2
View3DAtts.centerOfRotationSet = 0
View3DAtts.centerOfRotation = (512, 512, 0)
View3DAtts.axis3DScaleFlag = 1
View3DAtts.axis3DScales = (1, 1, 20)
View3DAtts.shear = (0, 0, 1)
View3DAtts.windowValid = 1
SetView3D(View3DAtts)
# End spontaneous state

# Begin spontaneous state
View3DAtts = View3DAttributes()
View3DAtts.viewNormal = (-0.242425, -0.780239, 0.576591)
View3DAtts.focus = (512, 512, 0)
View3DAtts.viewUp = (0.0615999, 0.580741, 0.811754)
View3DAtts.viewAngle = 30
View3DAtts.parallelScale = 724.078
View3DAtts.nearPlane = -1448.16
View3DAtts.farPlane = 1448.16
View3DAtts.imagePan = (0, 0)
View3DAtts.imageZoom = 1.4641
View3DAtts.perspective = 1
View3DAtts.eyeAngle = 2
View3DAtts.centerOfRotationSet = 0
View3DAtts.centerOfRotation = (512, 512, 0)
View3DAtts.axis3DScaleFlag = 1
View3DAtts.axis3DScales = (1, 1, 20)
View3DAtts.shear = (0, 0, 1)
View3DAtts.windowValid = 1
SetView3D(View3DAtts)
# End spontaneous state

# Begin spontaneous state
View3DAtts = View3DAttributes()
View3DAtts.viewNormal = (-0.242425, -0.780239, 0.576591)
View3DAtts.focus = (512, 512, 0)
View3DAtts.viewUp = (0.0615999, 0.580741, 0.811754)
View3DAtts.viewAngle = 30
View3DAtts.parallelScale = 724.078
View3DAtts.nearPlane = -1448.16
View3DAtts.farPlane = 1448.16
View3DAtts.imagePan = (0, 0)
View3DAtts.imageZoom = 1.77156
View3DAtts.perspective = 1
View3DAtts.eyeAngle = 2
View3DAtts.centerOfRotationSet = 0
View3DAtts.centerOfRotation = (512, 512, 0)
View3DAtts.axis3DScaleFlag = 1
View3DAtts.axis3DScales = (1, 1, 20)
View3DAtts.shear = (0, 0, 1)
View3DAtts.windowValid = 1
SetView3D(View3DAtts)
# End spontaneous state

# Begin spontaneous state
View3DAtts = View3DAttributes()
View3DAtts.viewNormal = (-0.242425, -0.780239, 0.576591)
View3DAtts.focus = (512, 512, 0)
View3DAtts.viewUp = (0.0615999, 0.580741, 0.811754)
View3DAtts.viewAngle = 30
View3DAtts.parallelScale = 724.078
View3DAtts.nearPlane = -1448.16
View3DAtts.farPlane = 1448.16
View3DAtts.imagePan = (0, 0)
View3DAtts.imageZoom = 2.14359
View3DAtts.perspective = 1
View3DAtts.eyeAngle = 2
View3DAtts.centerOfRotationSet = 0
View3DAtts.centerOfRotation = (512, 512, 0)
View3DAtts.axis3DScaleFlag = 1
View3DAtts.axis3DScales = (1, 1, 20)
View3DAtts.shear = (0, 0, 1)
View3DAtts.windowValid = 1
SetView3D(View3DAtts)
# End spontaneous state

# Begin spontaneous state
View3DAtts = View3DAttributes()
View3DAtts.viewNormal = (-0.242425, -0.780239, 0.576591)
View3DAtts.focus = (512, 512, 0)
View3DAtts.viewUp = (0.0615999, 0.580741, 0.811754)
View3DAtts.viewAngle = 30
View3DAtts.parallelScale = 724.078
View3DAtts.nearPlane = -1448.16
View3DAtts.farPlane = 1448.16
View3DAtts.imagePan = (0, 0)
View3DAtts.imageZoom = 2.59374
View3DAtts.perspective = 1
View3DAtts.eyeAngle = 2
View3DAtts.centerOfRotationSet = 0
View3DAtts.centerOfRotation = (512, 512, 0)
View3DAtts.axis3DScaleFlag = 1
View3DAtts.axis3DScales = (1, 1, 20)
View3DAtts.shear = (0, 0, 1)
View3DAtts.windowValid = 1
SetView3D(View3DAtts)
# End spontaneous state

# Begin spontaneous state
View3DAtts = View3DAttributes()
View3DAtts.viewNormal = (-0.242425, -0.780239, 0.576591)
View3DAtts.focus = (512, 512, 0)
View3DAtts.viewUp = (0.0615999, 0.580741, 0.811754)
View3DAtts.viewAngle = 30
View3DAtts.parallelScale = 724.078
View3DAtts.nearPlane = -1448.16
View3DAtts.farPlane = 1448.16
View3DAtts.imagePan = (0, 0)
View3DAtts.imageZoom = 3.13843
View3DAtts.perspective = 1
View3DAtts.eyeAngle = 2
View3DAtts.centerOfRotationSet = 0
View3DAtts.centerOfRotation = (512, 512, 0)
View3DAtts.axis3DScaleFlag = 1
View3DAtts.axis3DScales = (1, 1, 20)
View3DAtts.shear = (0, 0, 1)
View3DAtts.windowValid = 1
SetView3D(View3DAtts)
# End spontaneous state

# Begin spontaneous state
View3DAtts = View3DAttributes()
View3DAtts.viewNormal = (-0.242425, -0.780239, 0.576591)
View3DAtts.focus = (512, 512, 0)
View3DAtts.viewUp = (0.0615999, 0.580741, 0.811754)
View3DAtts.viewAngle = 30
View3DAtts.parallelScale = 724.078
View3DAtts.nearPlane = -1448.16
View3DAtts.farPlane = 1448.16
View3DAtts.imagePan = (0, 0)
View3DAtts.imageZoom = 3.7975
View3DAtts.perspective = 1
View3DAtts.eyeAngle = 2
View3DAtts.centerOfRotationSet = 0
View3DAtts.centerOfRotation = (512, 512, 0)
View3DAtts.axis3DScaleFlag = 1
View3DAtts.axis3DScales = (1, 1, 20)
View3DAtts.shear = (0, 0, 1)
View3DAtts.windowValid = 1
SetView3D(View3DAtts)
# End spontaneous state

# Begin spontaneous state
View3DAtts = View3DAttributes()
View3DAtts.viewNormal = (-0.242425, -0.780239, 0.576591)
View3DAtts.focus = (512, 512, 0)
View3DAtts.viewUp = (0.0615999, 0.580741, 0.811754)
View3DAtts.viewAngle = 30
View3DAtts.parallelScale = 724.078
View3DAtts.nearPlane = -1448.16
View3DAtts.farPlane = 1448.16
View3DAtts.imagePan = (0, 0)
View3DAtts.imageZoom = 4.59498
View3DAtts.perspective = 1
View3DAtts.eyeAngle = 2
View3DAtts.centerOfRotationSet = 0
View3DAtts.centerOfRotation = (512, 512, 0)
View3DAtts.axis3DScaleFlag = 1
View3DAtts.axis3DScales = (1, 1, 20)
View3DAtts.shear = (0, 0, 1)
View3DAtts.windowValid = 1
SetView3D(View3DAtts)
# End spontaneous state

# Begin spontaneous state
View3DAtts = View3DAttributes()
View3DAtts.viewNormal = (-0.242425, -0.780239, 0.576591)
View3DAtts.focus = (512, 512, 0)
View3DAtts.viewUp = (0.0615999, 0.580741, 0.811754)
View3DAtts.viewAngle = 30
View3DAtts.parallelScale = 724.078
View3DAtts.nearPlane = -1448.16
View3DAtts.farPlane = 1448.16
View3DAtts.imagePan = (0, 0)
View3DAtts.imageZoom = 5.55992
View3DAtts.perspective = 1
View3DAtts.eyeAngle = 2
View3DAtts.centerOfRotationSet = 0
View3DAtts.centerOfRotation = (512, 512, 0)
View3DAtts.axis3DScaleFlag = 1
View3DAtts.axis3DScales = (1, 1, 20)
View3DAtts.shear = (0, 0, 1)
View3DAtts.windowValid = 1
SetView3D(View3DAtts)
# End spontaneous state

# Begin spontaneous state
View3DAtts = View3DAttributes()
View3DAtts.viewNormal = (-0.242425, -0.780239, 0.576591)
View3DAtts.focus = (512, 512, 0)
View3DAtts.viewUp = (0.0615999, 0.580741, 0.811754)
View3DAtts.viewAngle = 30
View3DAtts.parallelScale = 724.078
View3DAtts.nearPlane = -1448.16
View3DAtts.farPlane = 1448.16
View3DAtts.imagePan = (0, 0)
View3DAtts.imageZoom = 6.7275
View3DAtts.perspective = 1
View3DAtts.eyeAngle = 2
View3DAtts.centerOfRotationSet = 0
View3DAtts.centerOfRotation = (512, 512, 0)
View3DAtts.axis3DScaleFlag = 1
View3DAtts.axis3DScales = (1, 1, 20)
View3DAtts.shear = (0, 0, 1)
View3DAtts.windowValid = 1
SetView3D(View3DAtts)
# End spontaneous state

# Begin spontaneous state
View3DAtts = View3DAttributes()
View3DAtts.viewNormal = (-0.242425, -0.780239, 0.576591)
View3DAtts.focus = (512, 512, 0)
View3DAtts.viewUp = (0.0615999, 0.580741, 0.811754)
View3DAtts.viewAngle = 30
View3DAtts.parallelScale = 724.078
View3DAtts.nearPlane = -1448.16
View3DAtts.farPlane = 1448.16
View3DAtts.imagePan = (0, 0)
View3DAtts.imageZoom = 8.14028
View3DAtts.perspective = 1
View3DAtts.eyeAngle = 2
View3DAtts.centerOfRotationSet = 0
View3DAtts.centerOfRotation = (512, 512, 0)
View3DAtts.axis3DScaleFlag = 1
View3DAtts.axis3DScales = (1, 1, 20)
View3DAtts.shear = (0, 0, 1)
View3DAtts.windowValid = 1
SetView3D(View3DAtts)
# End spontaneous state

# Begin spontaneous state
View3DAtts = View3DAttributes()
View3DAtts.viewNormal = (-0.242425, -0.780239, 0.576591)
View3DAtts.focus = (512, 512, 0)
View3DAtts.viewUp = (0.0615999, 0.580741, 0.811754)
View3DAtts.viewAngle = 30
View3DAtts.parallelScale = 724.078
View3DAtts.nearPlane = -1448.16
View3DAtts.farPlane = 1448.16
View3DAtts.imagePan = (0, 0)
View3DAtts.imageZoom = 9.84974
View3DAtts.perspective = 1
View3DAtts.eyeAngle = 2
View3DAtts.centerOfRotationSet = 0
View3DAtts.centerOfRotation = (512, 512, 0)
View3DAtts.axis3DScaleFlag = 1
View3DAtts.axis3DScales = (1, 1, 20)
View3DAtts.shear = (0, 0, 1)
View3DAtts.windowValid = 1
SetView3D(View3DAtts)
# End spontaneous state

# Begin spontaneous state
View3DAtts = View3DAttributes()
View3DAtts.viewNormal = (-0.242425, -0.780239, 0.576591)
View3DAtts.focus = (512, 512, 0)
View3DAtts.viewUp = (0.0615999, 0.580741, 0.811754)
View3DAtts.viewAngle = 30
View3DAtts.parallelScale = 724.078
View3DAtts.nearPlane = -1448.16
View3DAtts.farPlane = 1448.16
View3DAtts.imagePan = (0, 0)
View3DAtts.imageZoom = 8.14028
View3DAtts.perspective = 1
View3DAtts.eyeAngle = 2
View3DAtts.centerOfRotationSet = 0
View3DAtts.centerOfRotation = (512, 512, 0)
View3DAtts.axis3DScaleFlag = 1
View3DAtts.axis3DScales = (1, 1, 20)
View3DAtts.shear = (0, 0, 1)
View3DAtts.windowValid = 1
SetView3D(View3DAtts)
# End spontaneous state

# Begin spontaneous state
View3DAtts = View3DAttributes()
View3DAtts.viewNormal = (-0.242425, -0.780239, 0.576591)
View3DAtts.focus = (512, 512, 0)
View3DAtts.viewUp = (0.0615999, 0.580741, 0.811754)
View3DAtts.viewAngle = 30
View3DAtts.parallelScale = 724.078
View3DAtts.nearPlane = -1448.16
View3DAtts.farPlane = 1448.16
View3DAtts.imagePan = (0, 0)
View3DAtts.imageZoom = 6.7275
View3DAtts.perspective = 1
View3DAtts.eyeAngle = 2
View3DAtts.centerOfRotationSet = 0
View3DAtts.centerOfRotation = (512, 512, 0)
View3DAtts.axis3DScaleFlag = 1
View3DAtts.axis3DScales = (1, 1, 20)
View3DAtts.shear = (0, 0, 1)
View3DAtts.windowValid = 1
SetView3D(View3DAtts)
# End spontaneous state

# Begin spontaneous state
View3DAtts = View3DAttributes()
View3DAtts.viewNormal = (-0.529769, 0.679805, 0.507158)
View3DAtts.focus = (512, 512, 0)
View3DAtts.viewUp = (0.427732, -0.302209, 0.851889)
View3DAtts.viewAngle = 30
View3DAtts.parallelScale = 724.078
View3DAtts.nearPlane = -1448.16
View3DAtts.farPlane = 1448.16
View3DAtts.imagePan = (0, 0)
View3DAtts.imageZoom = 6.7275
View3DAtts.perspective = 1
View3DAtts.eyeAngle = 2
View3DAtts.centerOfRotationSet = 0
View3DAtts.centerOfRotation = (512, 512, 0)
View3DAtts.axis3DScaleFlag = 1
View3DAtts.axis3DScales = (1, 1, 20)
View3DAtts.shear = (0, 0, 1)
View3DAtts.windowValid = 1
SetView3D(View3DAtts)
# End spontaneous state

RemoveOperator(1, 1)
DrawPlots()
# Begin spontaneous state
View3DAtts = View3DAttributes()
View3DAtts.viewNormal = (-0.529769, 0.679805, 0.507158)
View3DAtts.focus = (512, 512, 0)
View3DAtts.viewUp = (0.427732, -0.302209, 0.851889)
View3DAtts.viewAngle = 30
View3DAtts.parallelScale = 724.078
View3DAtts.nearPlane = -1448.16
View3DAtts.farPlane = 1448.16
View3DAtts.imagePan = (0, 0)
View3DAtts.imageZoom = 6.7275
View3DAtts.perspective = 1
View3DAtts.eyeAngle = 2
View3DAtts.centerOfRotationSet = 0
View3DAtts.centerOfRotation = (512, 512, 0)
View3DAtts.axis3DScaleFlag = 1
View3DAtts.axis3DScales = (1, 1, 20)
View3DAtts.shear = (0, 0, 1)
View3DAtts.windowValid = 1
SetView3D(View3DAtts)
# End spontaneous state

ViewCurveAtts = ViewCurveAttributes()
ViewCurveAtts.domainCoords = (0, 1)
ViewCurveAtts.rangeCoords = (0, 1)
ViewCurveAtts.viewportCoords = (0.2, 0.95, 0.15, 0.95)
ViewCurveAtts.domainScale = ViewCurveAtts.LINEAR  # LINEAR, LOG
ViewCurveAtts.rangeScale = ViewCurveAtts.LINEAR  # LINEAR, LOG
SetViewCurve(ViewCurveAtts)
View2DAtts = View2DAttributes()
View2DAtts.windowCoords = (456, 568, 456, 568)
View2DAtts.viewportCoords = (0.2, 0.95, 0.15, 0.95)
View2DAtts.fullFrameActivationMode = View2DAtts.Auto  # On, Off, Auto
View2DAtts.fullFrameAutoThreshold = 100
View2DAtts.xScale = View2DAtts.LINEAR  # LINEAR, LOG
View2DAtts.yScale = View2DAtts.LINEAR  # LINEAR, LOG
View2DAtts.windowValid = 1
SetView2D(View2DAtts)
View3DAtts = View3DAttributes()
View3DAtts.viewNormal = (-0.529769, 0.679805, 0.507158)
View3DAtts.focus = (512, 512, 0)
View3DAtts.viewUp = (0.427732, -0.302209, 0.851889)
View3DAtts.viewAngle = 30
View3DAtts.parallelScale = 724.078
View3DAtts.nearPlane = -1448.16
View3DAtts.farPlane = 1448.16
View3DAtts.imagePan = (0, 0)
View3DAtts.imageZoom = 6.7275
View3DAtts.perspective = 1
View3DAtts.eyeAngle = 2
View3DAtts.centerOfRotationSet = 0
View3DAtts.centerOfRotation = (512, 512, 0)
View3DAtts.axis3DScaleFlag = 1
View3DAtts.axis3DScales = (1, 1, 20)
View3DAtts.shear = (0, 0, 1)
View3DAtts.windowValid = 1
SetView3D(View3DAtts)
ViewAxisArrayAtts = ViewAxisArrayAttributes()
ViewAxisArrayAtts.domainCoords = (0, 1)
ViewAxisArrayAtts.rangeCoords = (0, 1)
ViewAxisArrayAtts.viewportCoords = (0.15, 0.9, 0.1, 0.85)
SetViewAxisArray(ViewAxisArrayAtts)
SetActiveWindow(2)
SetActiveWindow(2)
# Begin spontaneous state
View2DAtts = View2DAttributes()
View2DAtts.windowCoords = (366.75, 657.25, 356.64, 667.36)
View2DAtts.viewportCoords = (0.2, 0.95, 0.15, 0.95)
View2DAtts.fullFrameActivationMode = View2DAtts.Auto  # On, Off, Auto
View2DAtts.fullFrameAutoThreshold = 100
View2DAtts.xScale = View2DAtts.LINEAR  # LINEAR, LOG
View2DAtts.yScale = View2DAtts.LINEAR  # LINEAR, LOG
View2DAtts.windowValid = 1
SetView2D(View2DAtts)
# End spontaneous state

ViewCurveAtts = ViewCurveAttributes()
ViewCurveAtts.domainCoords = (0, 1)
ViewCurveAtts.rangeCoords = (0, 1)
ViewCurveAtts.viewportCoords = (0.2, 0.95, 0.15, 0.95)
ViewCurveAtts.domainScale = ViewCurveAtts.LINEAR  # LINEAR, LOG
ViewCurveAtts.rangeScale = ViewCurveAtts.LINEAR  # LINEAR, LOG
SetViewCurve(ViewCurveAtts)
View2DAtts = View2DAttributes()
View2DAtts.windowCoords = (366.75, 657.25, 356.64, 667.36)
View2DAtts.viewportCoords = (0.2, 0.95, 0.15, 0.95)
View2DAtts.fullFrameActivationMode = View2DAtts.Auto  # On, Off, Auto
View2DAtts.fullFrameAutoThreshold = 100
View2DAtts.xScale = View2DAtts.LINEAR  # LINEAR, LOG
View2DAtts.yScale = View2DAtts.LINEAR  # LINEAR, LOG
View2DAtts.windowValid = 1
SetView2D(View2DAtts)
View3DAtts = View3DAttributes()
View3DAtts.viewNormal = (0, 0, 1)
View3DAtts.focus = (512, 512, 256)
View3DAtts.viewUp = (0, 1, 0)
View3DAtts.viewAngle = 30
View3DAtts.parallelScale = 768
View3DAtts.nearPlane = -1536
View3DAtts.farPlane = 1536
View3DAtts.imagePan = (0, 0)
View3DAtts.imageZoom = 1
View3DAtts.perspective = 1
View3DAtts.eyeAngle = 2
View3DAtts.centerOfRotationSet = 0
View3DAtts.centerOfRotation = (512, 512, 256)
View3DAtts.axis3DScaleFlag = 0
View3DAtts.axis3DScales = (1, 1, 1)
View3DAtts.shear = (0, 0, 1)
View3DAtts.windowValid = 1
SetView3D(View3DAtts)
ViewAxisArrayAtts = ViewAxisArrayAttributes()
ViewAxisArrayAtts.domainCoords = (0, 1)
ViewAxisArrayAtts.rangeCoords = (0, 1)
ViewAxisArrayAtts.viewportCoords = (0.15, 0.9, 0.1, 0.85)
SetViewAxisArray(ViewAxisArrayAtts)
# Begin spontaneous state
View2DAtts = View2DAttributes()
View2DAtts.windowCoords = (456, 568, 456, 568)
View2DAtts.viewportCoords = (0.2, 0.95, 0.15, 0.95)
View2DAtts.fullFrameActivationMode = View2DAtts.Auto  # On, Off, Auto
View2DAtts.fullFrameAutoThreshold = 100
View2DAtts.xScale = View2DAtts.LINEAR  # LINEAR, LOG
View2DAtts.yScale = View2DAtts.LINEAR  # LINEAR, LOG
View2DAtts.windowValid = 1
SetView2D(View2DAtts)
# End spontaneous state

ViewCurveAtts = ViewCurveAttributes()
ViewCurveAtts.domainCoords = (0, 1)
ViewCurveAtts.rangeCoords = (0, 1)
ViewCurveAtts.viewportCoords = (0.2, 0.95, 0.15, 0.95)
ViewCurveAtts.domainScale = ViewCurveAtts.LINEAR  # LINEAR, LOG
ViewCurveAtts.rangeScale = ViewCurveAtts.LINEAR  # LINEAR, LOG
SetViewCurve(ViewCurveAtts)
View2DAtts = View2DAttributes()
View2DAtts.windowCoords = (456, 568, 456, 568)
View2DAtts.viewportCoords = (0.2, 0.95, 0.15, 0.95)
View2DAtts.fullFrameActivationMode = View2DAtts.Auto  # On, Off, Auto
View2DAtts.fullFrameAutoThreshold = 100
View2DAtts.xScale = View2DAtts.LINEAR  # LINEAR, LOG
View2DAtts.yScale = View2DAtts.LINEAR  # LINEAR, LOG
View2DAtts.windowValid = 1
SetView2D(View2DAtts)
View3DAtts = View3DAttributes()
View3DAtts.viewNormal = (0, 0, 1)
View3DAtts.focus = (512, 512, 256)
View3DAtts.viewUp = (0, 1, 0)
View3DAtts.viewAngle = 30
View3DAtts.parallelScale = 768
View3DAtts.nearPlane = -1536
View3DAtts.farPlane = 1536
View3DAtts.imagePan = (0, 0)
View3DAtts.imageZoom = 1
View3DAtts.perspective = 1
View3DAtts.eyeAngle = 2
View3DAtts.centerOfRotationSet = 0
View3DAtts.centerOfRotation = (512, 512, 256)
View3DAtts.axis3DScaleFlag = 0
View3DAtts.axis3DScales = (1, 1, 1)
View3DAtts.shear = (0, 0, 1)
View3DAtts.windowValid = 1
SetView3D(View3DAtts)
ViewAxisArrayAtts = ViewAxisArrayAttributes()
ViewAxisArrayAtts.domainCoords = (0, 1)
ViewAxisArrayAtts.rangeCoords = (0, 1)
ViewAxisArrayAtts.viewportCoords = (0.15, 0.9, 0.1, 0.85)
SetViewAxisArray(ViewAxisArrayAtts)
# Begin spontaneous state
View2DAtts = View2DAttributes()
View2DAtts.windowCoords = (456, 568, 456, 568)
View2DAtts.viewportCoords = (0.2, 0.95, 0.15, 0.95)
View2DAtts.fullFrameActivationMode = View2DAtts.Auto  # On, Off, Auto
View2DAtts.fullFrameAutoThreshold = 100
View2DAtts.xScale = View2DAtts.LINEAR  # LINEAR, LOG
View2DAtts.yScale = View2DAtts.LINEAR  # LINEAR, LOG
View2DAtts.windowValid = 1
SetView2D(View2DAtts)
# End spontaneous state

ViewCurveAtts = ViewCurveAttributes()
ViewCurveAtts.domainCoords = (0, 1)
ViewCurveAtts.rangeCoords = (0, 1)
ViewCurveAtts.viewportCoords = (0.2, 0.95, 0.15, 0.95)
ViewCurveAtts.domainScale = ViewCurveAtts.LINEAR  # LINEAR, LOG
ViewCurveAtts.rangeScale = ViewCurveAtts.LINEAR  # LINEAR, LOG
SetViewCurve(ViewCurveAtts)
View2DAtts = View2DAttributes()
View2DAtts.windowCoords = (456, 568, 456, 568)
View2DAtts.viewportCoords = (0.2, 0.95, 0.15, 0.95)
View2DAtts.fullFrameActivationMode = View2DAtts.Auto  # On, Off, Auto
View2DAtts.fullFrameAutoThreshold = 100
View2DAtts.xScale = View2DAtts.LINEAR  # LINEAR, LOG
View2DAtts.yScale = View2DAtts.LINEAR  # LINEAR, LOG
View2DAtts.windowValid = 1
SetView2D(View2DAtts)
View3DAtts = View3DAttributes()
View3DAtts.viewNormal = (0, 0, 1)
View3DAtts.focus = (512, 512, 256)
View3DAtts.viewUp = (0, 1, 0)
View3DAtts.viewAngle = 30
View3DAtts.parallelScale = 768
View3DAtts.nearPlane = -1536
View3DAtts.farPlane = 1536
View3DAtts.imagePan = (0, 0)
View3DAtts.imageZoom = 1
View3DAtts.perspective = 1
View3DAtts.eyeAngle = 2
View3DAtts.centerOfRotationSet = 0
View3DAtts.centerOfRotation = (512, 512, 256)
View3DAtts.axis3DScaleFlag = 0
View3DAtts.axis3DScales = (1, 1, 1)
View3DAtts.shear = (0, 0, 1)
View3DAtts.windowValid = 1
SetView3D(View3DAtts)
ViewAxisArrayAtts = ViewAxisArrayAttributes()
ViewAxisArrayAtts.domainCoords = (0, 1)
ViewAxisArrayAtts.rangeCoords = (0, 1)
ViewAxisArrayAtts.viewportCoords = (0.15, 0.9, 0.1, 0.85)
SetViewAxisArray(ViewAxisArrayAtts)
# Begin spontaneous state
View2DAtts = View2DAttributes()
View2DAtts.windowCoords = (456, 568, 456, 568)
View2DAtts.viewportCoords = (0.2, 0.95, 0.15, 0.95)
View2DAtts.fullFrameActivationMode = View2DAtts.Auto  # On, Off, Auto
View2DAtts.fullFrameAutoThreshold = 100
View2DAtts.xScale = View2DAtts.LINEAR  # LINEAR, LOG
View2DAtts.yScale = View2DAtts.LINEAR  # LINEAR, LOG
View2DAtts.windowValid = 1
SetView2D(View2DAtts)
# End spontaneous state

# Begin spontaneous state
View2DAtts = View2DAttributes()
View2DAtts.windowCoords = (456, 568, 456, 568)
View2DAtts.viewportCoords = (0.2, 0.95, 0.15, 0.95)
View2DAtts.fullFrameActivationMode = View2DAtts.Auto  # On, Off, Auto
View2DAtts.fullFrameAutoThreshold = 100
View2DAtts.xScale = View2DAtts.LINEAR  # LINEAR, LOG
View2DAtts.yScale = View2DAtts.LINEAR  # LINEAR, LOG
View2DAtts.windowValid = 1
SetView2D(View2DAtts)
# End spontaneous state

# MAINTENANCE ISSUE: SetSuppressMessagesRPC is not handled in Logging.C. Please contact a VisIt developer.
SaveSession("/Users/Jamie/.visit/crash_recovery.4536.session")
# MAINTENANCE ISSUE: SetSuppressMessagesRPC is not handled in Logging.C. Please contact a VisIt developer.
# MAINTENANCE ISSUE: SetSuppressMessagesRPC is not handled in Logging.C. Please contact a VisIt developer.
SaveSession("/Users/Jamie/.visit/crash_recovery.4536.session")
# MAINTENANCE ISSUE: SetSuppressMessagesRPC is not handled in Logging.C. Please contact a VisIt developer.
# MAINTENANCE ISSUE: SetSuppressMessagesRPC is not handled in Logging.C. Please contact a VisIt developer.
SaveSession("/Users/Jamie/.visit/crash_recovery.4536.session")
# MAINTENANCE ISSUE: SetSuppressMessagesRPC is not handled in Logging.C. Please contact a VisIt developer.
# MAINTENANCE ISSUE: SetSuppressMessagesRPC is not handled in Logging.C. Please contact a VisIt developer.
SaveSession("/Users/Jamie/.visit/crash_recovery.4536.session")
# MAINTENANCE ISSUE: SetSuppressMessagesRPC is not handled in Logging.C. Please contact a VisIt developer.
# MAINTENANCE ISSUE: SetSuppressMessagesRPC is not handled in Logging.C. Please contact a VisIt developer.
SaveSession("/Users/Jamie/.visit/crash_recovery.4536.session")
# MAINTENANCE ISSUE: SetSuppressMessagesRPC is not handled in Logging.C. Please contact a VisIt developer.
# MAINTENANCE ISSUE: SetSuppressMessagesRPC is not handled in Logging.C. Please contact a VisIt developer.
SaveSession("/Users/Jamie/.visit/crash_recovery.4536.session")
# MAINTENANCE ISSUE: SetSuppressMessagesRPC is not handled in Logging.C. Please contact a VisIt developer.
# Begin spontaneous state
View2DAtts = View2DAttributes()
View2DAtts.windowCoords = (456, 568, 456, 568)
View2DAtts.viewportCoords = (0.2, 0.95, 0.15, 0.95)
View2DAtts.fullFrameActivationMode = View2DAtts.Auto  # On, Off, Auto
View2DAtts.fullFrameAutoThreshold = 100
View2DAtts.xScale = View2DAtts.LINEAR  # LINEAR, LOG
View2DAtts.yScale = View2DAtts.LINEAR  # LINEAR, LOG
View2DAtts.windowValid = 1
SetView2D(View2DAtts)
# End spontaneous state

DeleteActivePlots()
DeleteActivePlots()
OpenDatabase("login-cpu.hpc.cam.ac.uk:/rds/user/dc-bamb1/rds-dirac-dp131/dc-bamb1/GRChombo_data/KerrSF/run0039_KNL_l1_m1_a0.7_Al0_mu0.4_M1_correct_Ylm_KerrSchild/KerrSFp_*.3d.hdf5 database")
OpenDatabase("login-cpu.hpc.cam.ac.uk:/rds/user/dc-bamb1/rds-dirac-dp131/dc-bamb1/GRChombo_data/KerrSF/run0039_KNL_l1_m1_a0.7_Al0_mu0.4_M1_correct_Ylm/KerrSFp_*.3d.hdf5 database")
OpenDatabase("login-cpu.hpc.cam.ac.uk:/rds/user/dc-bamb1/rds-dirac-dp131/dc-bamb1/GRChombo_data/KerrSF/run0032_KNL_l1_m1_a0_Al0_mu0.4_M1_correct_Ylm/KerrSFp_*.3d.hdf5 database", 0)
metadata = GetMetaData("login-cpu.hpc.cam.ac.uk:/rds/user/dc-bamb1/rds-dirac-dp131/dc-bamb1/GRChombo_data/KerrSF/run0032_KNL_l1_m1_a0_Al0_mu0.4_M1_correct_Ylm/KerrSFp_*.3d.hdf5 database", -1)
AddPlot("Mesh", "Mesh", 1, 1)
MeshAtts = MeshAttributes()
MeshAtts.legendFlag = 0
MeshAtts.lineStyle = MeshAtts.SOLID  # SOLID, DASH, DOT, DOTDASH
MeshAtts.lineWidth = 0
MeshAtts.meshColor = (0, 0, 0, 255)
MeshAtts.meshColorSource = MeshAtts.Foreground  # Foreground, MeshCustom
MeshAtts.opaqueColorSource = MeshAtts.Background  # Background, OpaqueCustom
MeshAtts.opaqueMode = MeshAtts.Auto  # Auto, On, Off
MeshAtts.pointSize = 0.05
MeshAtts.opaqueColor = (255, 255, 255, 255)
MeshAtts.smoothingLevel = MeshAtts.None  # None, Fast, High
MeshAtts.pointSizeVarEnabled = 0
MeshAtts.pointSizeVar = "default"
MeshAtts.pointType = MeshAtts.Point  # Box, Axis, Icosahedron, Octahedron, Tetrahedron, SphereGeometry, Point, Sphere
MeshAtts.showInternal = 0
MeshAtts.pointSizePixels = 2
MeshAtts.opacity = 1
SetPlotOptions(MeshAtts)
HideActivePlots()
AddOperator("ThreeSlice", 1)
ThreeSliceAtts = ThreeSliceAttributes()
ThreeSliceAtts.x = 512
ThreeSliceAtts.y = 512
ThreeSliceAtts.z = 256
ThreeSliceAtts.interactive = 1
SetOperatorOptions(ThreeSliceAtts, 1)
AddPlot("Pseudocolor", "phi", 1, 1)
AddOperator("ThreeSlice", 1)
ThreeSliceAtts = ThreeSliceAttributes()
ThreeSliceAtts.x = 512
ThreeSliceAtts.y = 512
ThreeSliceAtts.z = 256
ThreeSliceAtts.interactive = 1
SetOperatorOptions(ThreeSliceAtts, 1)
DrawPlots()
# MAINTENANCE ISSUE: SetSuppressMessagesRPC is not handled in Logging.C. Please contact a VisIt developer.
SaveSession("/Users/Jamie/.visit/crash_recovery.4536.session")
# MAINTENANCE ISSUE: SetSuppressMessagesRPC is not handled in Logging.C. Please contact a VisIt developer.
# MAINTENANCE ISSUE: SetSuppressMessagesRPC is not handled in Logging.C. Please contact a VisIt developer.
SaveSession("/Users/Jamie/.visit/crash_recovery.4536.session")
# MAINTENANCE ISSUE: SetSuppressMessagesRPC is not handled in Logging.C. Please contact a VisIt developer.
# MAINTENANCE ISSUE: SetSuppressMessagesRPC is not handled in Logging.C. Please contact a VisIt developer.
SaveSession("/Users/Jamie/.visit/crash_recovery.4536.session")
# MAINTENANCE ISSUE: SetSuppressMessagesRPC is not handled in Logging.C. Please contact a VisIt developer.
# MAINTENANCE ISSUE: SetSuppressMessagesRPC is not handled in Logging.C. Please contact a VisIt developer.
SaveSession("/Users/Jamie/.visit/crash_recovery.4536.session")
# MAINTENANCE ISSUE: SetSuppressMessagesRPC is not handled in Logging.C. Please contact a VisIt developer.
# MAINTENANCE ISSUE: SetSuppressMessagesRPC is not handled in Logging.C. Please contact a VisIt developer.
SaveSession("/Users/Jamie/.visit/crash_recovery.4536.session")
# MAINTENANCE ISSUE: SetSuppressMessagesRPC is not handled in Logging.C. Please contact a VisIt developer.
# MAINTENANCE ISSUE: SetSuppressMessagesRPC is not handled in Logging.C. Please contact a VisIt developer.
SaveSession("/Users/Jamie/.visit/crash_recovery.4536.session")
# MAINTENANCE ISSUE: SetSuppressMessagesRPC is not handled in Logging.C. Please contact a VisIt developer.
# MAINTENANCE ISSUE: SetSuppressMessagesRPC is not handled in Logging.C. Please contact a VisIt developer.
SaveSession("/Users/Jamie/.visit/crash_recovery.4536.session")
# MAINTENANCE ISSUE: SetSuppressMessagesRPC is not handled in Logging.C. Please contact a VisIt developer.
# MAINTENANCE ISSUE: SetSuppressMessagesRPC is not handled in Logging.C. Please contact a VisIt developer.
SaveSession("/Users/Jamie/.visit/crash_recovery.4536.session")
# MAINTENANCE ISSUE: SetSuppressMessagesRPC is not handled in Logging.C. Please contact a VisIt developer.
# MAINTENANCE ISSUE: SetSuppressMessagesRPC is not handled in Logging.C. Please contact a VisIt developer.
SaveSession("/Users/Jamie/.visit/crash_recovery.4536.session")
# MAINTENANCE ISSUE: SetSuppressMessagesRPC is not handled in Logging.C. Please contact a VisIt developer.
# MAINTENANCE ISSUE: SetSuppressMessagesRPC is not handled in Logging.C. Please contact a VisIt developer.
SaveSession("/Users/Jamie/.visit/crash_recovery.4536.session")
# MAINTENANCE ISSUE: SetSuppressMessagesRPC is not handled in Logging.C. Please contact a VisIt developer.
# MAINTENANCE ISSUE: SetSuppressMessagesRPC is not handled in Logging.C. Please contact a VisIt developer.
SaveSession("/Users/Jamie/.visit/crash_recovery.4536.session")
# MAINTENANCE ISSUE: SetSuppressMessagesRPC is not handled in Logging.C. Please contact a VisIt developer.
# MAINTENANCE ISSUE: SetSuppressMessagesRPC is not handled in Logging.C. Please contact a VisIt developer.
SaveSession("/Users/Jamie/.visit/crash_recovery.4536.session")
# MAINTENANCE ISSUE: SetSuppressMessagesRPC is not handled in Logging.C. Please contact a VisIt developer.
# MAINTENANCE ISSUE: SetSuppressMessagesRPC is not handled in Logging.C. Please contact a VisIt developer.
SaveSession("/Users/Jamie/.visit/crash_recovery.4536.session")
# MAINTENANCE ISSUE: SetSuppressMessagesRPC is not handled in Logging.C. Please contact a VisIt developer.
# MAINTENANCE ISSUE: SetSuppressMessagesRPC is not handled in Logging.C. Please contact a VisIt developer.
SaveSession("/Users/Jamie/.visit/crash_recovery.4536.session")
# MAINTENANCE ISSUE: SetSuppressMessagesRPC is not handled in Logging.C. Please contact a VisIt developer.
# MAINTENANCE ISSUE: SetSuppressMessagesRPC is not handled in Logging.C. Please contact a VisIt developer.
SaveSession("/Users/Jamie/.visit/crash_recovery.4536.session")
# MAINTENANCE ISSUE: SetSuppressMessagesRPC is not handled in Logging.C. Please contact a VisIt developer.
# MAINTENANCE ISSUE: SetSuppressMessagesRPC is not handled in Logging.C. Please contact a VisIt developer.
SaveSession("/Users/Jamie/.visit/crash_recovery.4536.session")
# MAINTENANCE ISSUE: SetSuppressMessagesRPC is not handled in Logging.C. Please contact a VisIt developer.
# MAINTENANCE ISSUE: SetSuppressMessagesRPC is not handled in Logging.C. Please contact a VisIt developer.
SaveSession("/Users/Jamie/.visit/crash_recovery.4536.session")
# MAINTENANCE ISSUE: SetSuppressMessagesRPC is not handled in Logging.C. Please contact a VisIt developer.
# MAINTENANCE ISSUE: SetSuppressMessagesRPC is not handled in Logging.C. Please contact a VisIt developer.
SaveSession("/Users/Jamie/.visit/crash_recovery.4536.session")
# MAINTENANCE ISSUE: SetSuppressMessagesRPC is not handled in Logging.C. Please contact a VisIt developer.
# MAINTENANCE ISSUE: SetSuppressMessagesRPC is not handled in Logging.C. Please contact a VisIt developer.
SaveSession("/Users/Jamie/.visit/crash_recovery.4536.session")
# MAINTENANCE ISSUE: SetSuppressMessagesRPC is not handled in Logging.C. Please contact a VisIt developer.
# MAINTENANCE ISSUE: SetSuppressMessagesRPC is not handled in Logging.C. Please contact a VisIt developer.
SaveSession("/Users/Jamie/.visit/crash_recovery.4536.session")
# MAINTENANCE ISSUE: SetSuppressMessagesRPC is not handled in Logging.C. Please contact a VisIt developer.
# MAINTENANCE ISSUE: SetSuppressMessagesRPC is not handled in Logging.C. Please contact a VisIt developer.
SaveSession("/Users/Jamie/.visit/crash_recovery.4536.session")
# MAINTENANCE ISSUE: SetSuppressMessagesRPC is not handled in Logging.C. Please contact a VisIt developer.
# MAINTENANCE ISSUE: SetSuppressMessagesRPC is not handled in Logging.C. Please contact a VisIt developer.
SaveSession("/Users/Jamie/.visit/crash_recovery.4536.session")
# MAINTENANCE ISSUE: SetSuppressMessagesRPC is not handled in Logging.C. Please contact a VisIt developer.
# MAINTENANCE ISSUE: SetSuppressMessagesRPC is not handled in Logging.C. Please contact a VisIt developer.
SaveSession("/Users/Jamie/.visit/crash_recovery.4536.session")
# MAINTENANCE ISSUE: SetSuppressMessagesRPC is not handled in Logging.C. Please contact a VisIt developer.
# MAINTENANCE ISSUE: SetSuppressMessagesRPC is not handled in Logging.C. Please contact a VisIt developer.
SaveSession("/Users/Jamie/.visit/crash_recovery.4536.session")
# MAINTENANCE ISSUE: SetSuppressMessagesRPC is not handled in Logging.C. Please contact a VisIt developer.
# MAINTENANCE ISSUE: SetSuppressMessagesRPC is not handled in Logging.C. Please contact a VisIt developer.
SaveSession("/Users/Jamie/.visit/crash_recovery.4536.session")
# MAINTENANCE ISSUE: SetSuppressMessagesRPC is not handled in Logging.C. Please contact a VisIt developer.
# MAINTENANCE ISSUE: SetSuppressMessagesRPC is not handled in Logging.C. Please contact a VisIt developer.
SaveSession("/Users/Jamie/.visit/crash_recovery.4536.session")
# MAINTENANCE ISSUE: SetSuppressMessagesRPC is not handled in Logging.C. Please contact a VisIt developer.
# MAINTENANCE ISSUE: SetSuppressMessagesRPC is not handled in Logging.C. Please contact a VisIt developer.
SaveSession("/Users/Jamie/.visit/crash_recovery.4536.session")
# MAINTENANCE ISSUE: SetSuppressMessagesRPC is not handled in Logging.C. Please contact a VisIt developer.
# MAINTENANCE ISSUE: SetSuppressMessagesRPC is not handled in Logging.C. Please contact a VisIt developer.
SaveSession("/Users/Jamie/.visit/crash_recovery.4536.session")
# MAINTENANCE ISSUE: SetSuppressMessagesRPC is not handled in Logging.C. Please contact a VisIt developer.
# MAINTENANCE ISSUE: SetSuppressMessagesRPC is not handled in Logging.C. Please contact a VisIt developer.
SaveSession("/Users/Jamie/.visit/crash_recovery.4536.session")
# MAINTENANCE ISSUE: SetSuppressMessagesRPC is not handled in Logging.C. Please contact a VisIt developer.
# MAINTENANCE ISSUE: SetSuppressMessagesRPC is not handled in Logging.C. Please contact a VisIt developer.
SaveSession("/Users/Jamie/.visit/crash_recovery.4536.session")
# MAINTENANCE ISSUE: SetSuppressMessagesRPC is not handled in Logging.C. Please contact a VisIt developer.
# MAINTENANCE ISSUE: SetSuppressMessagesRPC is not handled in Logging.C. Please contact a VisIt developer.
SaveSession("/Users/Jamie/.visit/crash_recovery.4536.session")
# MAINTENANCE ISSUE: SetSuppressMessagesRPC is not handled in Logging.C. Please contact a VisIt developer.
# MAINTENANCE ISSUE: SetSuppressMessagesRPC is not handled in Logging.C. Please contact a VisIt developer.
SaveSession("/Users/Jamie/.visit/crash_recovery.4536.session")
# MAINTENANCE ISSUE: SetSuppressMessagesRPC is not handled in Logging.C. Please contact a VisIt developer.
# MAINTENANCE ISSUE: SetSuppressMessagesRPC is not handled in Logging.C. Please contact a VisIt developer.
SaveSession("/Users/Jamie/.visit/crash_recovery.4536.session")
# MAINTENANCE ISSUE: SetSuppressMessagesRPC is not handled in Logging.C. Please contact a VisIt developer.
# MAINTENANCE ISSUE: SetSuppressMessagesRPC is not handled in Logging.C. Please contact a VisIt developer.
SaveSession("/Users/Jamie/.visit/crash_recovery.4536.session")
# MAINTENANCE ISSUE: SetSuppressMessagesRPC is not handled in Logging.C. Please contact a VisIt developer.
# MAINTENANCE ISSUE: SetSuppressMessagesRPC is not handled in Logging.C. Please contact a VisIt developer.
SaveSession("/Users/Jamie/.visit/crash_recovery.4536.session")
# MAINTENANCE ISSUE: SetSuppressMessagesRPC is not handled in Logging.C. Please contact a VisIt developer.
# MAINTENANCE ISSUE: SetSuppressMessagesRPC is not handled in Logging.C. Please contact a VisIt developer.
SaveSession("/Users/Jamie/.visit/crash_recovery.4536.session")
# MAINTENANCE ISSUE: SetSuppressMessagesRPC is not handled in Logging.C. Please contact a VisIt developer.
# MAINTENANCE ISSUE: SetSuppressMessagesRPC is not handled in Logging.C. Please contact a VisIt developer.
SaveSession("/Users/Jamie/.visit/crash_recovery.4536.session")
# MAINTENANCE ISSUE: SetSuppressMessagesRPC is not handled in Logging.C. Please contact a VisIt developer.
# MAINTENANCE ISSUE: SetSuppressMessagesRPC is not handled in Logging.C. Please contact a VisIt developer.
SaveSession("/Users/Jamie/.visit/crash_recovery.4536.session")
# MAINTENANCE ISSUE: SetSuppressMessagesRPC is not handled in Logging.C. Please contact a VisIt developer.
# MAINTENANCE ISSUE: SetSuppressMessagesRPC is not handled in Logging.C. Please contact a VisIt developer.
SaveSession("/Users/Jamie/.visit/crash_recovery.4536.session")
# MAINTENANCE ISSUE: SetSuppressMessagesRPC is not handled in Logging.C. Please contact a VisIt developer.
# MAINTENANCE ISSUE: SetSuppressMessagesRPC is not handled in Logging.C. Please contact a VisIt developer.
SaveSession("/Users/Jamie/.visit/crash_recovery.4536.session")
# MAINTENANCE ISSUE: SetSuppressMessagesRPC is not handled in Logging.C. Please contact a VisIt developer.
# MAINTENANCE ISSUE: SetSuppressMessagesRPC is not handled in Logging.C. Please contact a VisIt developer.
SaveSession("/Users/Jamie/.visit/crash_recovery.4536.session")
# MAINTENANCE ISSUE: SetSuppressMessagesRPC is not handled in Logging.C. Please contact a VisIt developer.
# MAINTENANCE ISSUE: SetSuppressMessagesRPC is not handled in Logging.C. Please contact a VisIt developer.
SaveSession("/Users/Jamie/.visit/crash_recovery.4536.session")
# MAINTENANCE ISSUE: SetSuppressMessagesRPC is not handled in Logging.C. Please contact a VisIt developer.
# MAINTENANCE ISSUE: SetSuppressMessagesRPC is not handled in Logging.C. Please contact a VisIt developer.
SaveSession("/Users/Jamie/.visit/crash_recovery.4536.session")
# MAINTENANCE ISSUE: SetSuppressMessagesRPC is not handled in Logging.C. Please contact a VisIt developer.
# MAINTENANCE ISSUE: SetSuppressMessagesRPC is not handled in Logging.C. Please contact a VisIt developer.
SaveSession("/Users/Jamie/.visit/crash_recovery.4536.session")
# MAINTENANCE ISSUE: SetSuppressMessagesRPC is not handled in Logging.C. Please contact a VisIt developer.
# MAINTENANCE ISSUE: SetSuppressMessagesRPC is not handled in Logging.C. Please contact a VisIt developer.
SaveSession("/Users/Jamie/.visit/crash_recovery.4536.session")
# MAINTENANCE ISSUE: SetSuppressMessagesRPC is not handled in Logging.C. Please contact a VisIt developer.
# MAINTENANCE ISSUE: SetSuppressMessagesRPC is not handled in Logging.C. Please contact a VisIt developer.
SaveSession("/Users/Jamie/.visit/crash_recovery.4536.session")
# MAINTENANCE ISSUE: SetSuppressMessagesRPC is not handled in Logging.C. Please contact a VisIt developer.
# MAINTENANCE ISSUE: SetSuppressMessagesRPC is not handled in Logging.C. Please contact a VisIt developer.
SaveSession("/Users/Jamie/.visit/crash_recovery.4536.session")
# MAINTENANCE ISSUE: SetSuppressMessagesRPC is not handled in Logging.C. Please contact a VisIt developer.
# MAINTENANCE ISSUE: SetSuppressMessagesRPC is not handled in Logging.C. Please contact a VisIt developer.
SaveSession("/Users/Jamie/.visit/crash_recovery.4536.session")
# MAINTENANCE ISSUE: SetSuppressMessagesRPC is not handled in Logging.C. Please contact a VisIt developer.
# MAINTENANCE ISSUE: SetSuppressMessagesRPC is not handled in Logging.C. Please contact a VisIt developer.
SaveSession("/Users/Jamie/.visit/crash_recovery.4536.session")
# MAINTENANCE ISSUE: SetSuppressMessagesRPC is not handled in Logging.C. Please contact a VisIt developer.
# MAINTENANCE ISSUE: SetSuppressMessagesRPC is not handled in Logging.C. Please contact a VisIt developer.
SaveSession("/Users/Jamie/.visit/crash_recovery.4536.session")
# MAINTENANCE ISSUE: SetSuppressMessagesRPC is not handled in Logging.C. Please contact a VisIt developer.
# MAINTENANCE ISSUE: SetSuppressMessagesRPC is not handled in Logging.C. Please contact a VisIt developer.
SaveSession("/Users/Jamie/.visit/crash_recovery.4536.session")
# MAINTENANCE ISSUE: SetSuppressMessagesRPC is not handled in Logging.C. Please contact a VisIt developer.
# MAINTENANCE ISSUE: SetSuppressMessagesRPC is not handled in Logging.C. Please contact a VisIt developer.
SaveSession("/Users/Jamie/.visit/crash_recovery.4536.session")
# MAINTENANCE ISSUE: SetSuppressMessagesRPC is not handled in Logging.C. Please contact a VisIt developer.
# MAINTENANCE ISSUE: SetSuppressMessagesRPC is not handled in Logging.C. Please contact a VisIt developer.
SaveSession("/Users/Jamie/.visit/crash_recovery.4536.session")
# MAINTENANCE ISSUE: SetSuppressMessagesRPC is not handled in Logging.C. Please contact a VisIt developer.
# MAINTENANCE ISSUE: SetSuppressMessagesRPC is not handled in Logging.C. Please contact a VisIt developer.
SaveSession("/Users/Jamie/.visit/crash_recovery.4536.session")
# MAINTENANCE ISSUE: SetSuppressMessagesRPC is not handled in Logging.C. Please contact a VisIt developer.
# MAINTENANCE ISSUE: SetSuppressMessagesRPC is not handled in Logging.C. Please contact a VisIt developer.
SaveSession("/Users/Jamie/.visit/crash_recovery.4536.session")
# MAINTENANCE ISSUE: SetSuppressMessagesRPC is not handled in Logging.C. Please contact a VisIt developer.
# MAINTENANCE ISSUE: SetSuppressMessagesRPC is not handled in Logging.C. Please contact a VisIt developer.
SaveSession("/Users/Jamie/.visit/crash_recovery.4536.session")
# MAINTENANCE ISSUE: SetSuppressMessagesRPC is not handled in Logging.C. Please contact a VisIt developer.
# MAINTENANCE ISSUE: SetSuppressMessagesRPC is not handled in Logging.C. Please contact a VisIt developer.
SaveSession("/Users/Jamie/.visit/crash_recovery.4536.session")
# MAINTENANCE ISSUE: SetSuppressMessagesRPC is not handled in Logging.C. Please contact a VisIt developer.
# MAINTENANCE ISSUE: SetSuppressMessagesRPC is not handled in Logging.C. Please contact a VisIt developer.
SaveSession("/Users/Jamie/.visit/crash_recovery.4536.session")
# MAINTENANCE ISSUE: SetSuppressMessagesRPC is not handled in Logging.C. Please contact a VisIt developer.
# MAINTENANCE ISSUE: SetSuppressMessagesRPC is not handled in Logging.C. Please contact a VisIt developer.
SaveSession("/Users/Jamie/.visit/crash_recovery.4536.session")
# MAINTENANCE ISSUE: SetSuppressMessagesRPC is not handled in Logging.C. Please contact a VisIt developer.
# MAINTENANCE ISSUE: SetSuppressMessagesRPC is not handled in Logging.C. Please contact a VisIt developer.
SaveSession("/Users/Jamie/.visit/crash_recovery.4536.session")
# MAINTENANCE ISSUE: SetSuppressMessagesRPC is not handled in Logging.C. Please contact a VisIt developer.
# MAINTENANCE ISSUE: SetSuppressMessagesRPC is not handled in Logging.C. Please contact a VisIt developer.
SaveSession("/Users/Jamie/.visit/crash_recovery.4536.session")
# MAINTENANCE ISSUE: SetSuppressMessagesRPC is not handled in Logging.C. Please contact a VisIt developer.
# MAINTENANCE ISSUE: SetSuppressMessagesRPC is not handled in Logging.C. Please contact a VisIt developer.
SaveSession("/Users/Jamie/.visit/crash_recovery.4536.session")
# MAINTENANCE ISSUE: SetSuppressMessagesRPC is not handled in Logging.C. Please contact a VisIt developer.
# MAINTENANCE ISSUE: SetSuppressMessagesRPC is not handled in Logging.C. Please contact a VisIt developer.
SaveSession("/Users/Jamie/.visit/crash_recovery.4536.session")
# MAINTENANCE ISSUE: SetSuppressMessagesRPC is not handled in Logging.C. Please contact a VisIt developer.
# MAINTENANCE ISSUE: SetSuppressMessagesRPC is not handled in Logging.C. Please contact a VisIt developer.
SaveSession("/Users/Jamie/.visit/crash_recovery.4536.session")
# MAINTENANCE ISSUE: SetSuppressMessagesRPC is not handled in Logging.C. Please contact a VisIt developer.
# MAINTENANCE ISSUE: SetSuppressMessagesRPC is not handled in Logging.C. Please contact a VisIt developer.
SaveSession("/Users/Jamie/.visit/crash_recovery.4536.session")
# MAINTENANCE ISSUE: SetSuppressMessagesRPC is not handled in Logging.C. Please contact a VisIt developer.
# MAINTENANCE ISSUE: SetSuppressMessagesRPC is not handled in Logging.C. Please contact a VisIt developer.
SaveSession("/Users/Jamie/.visit/crash_recovery.4536.session")
# MAINTENANCE ISSUE: SetSuppressMessagesRPC is not handled in Logging.C. Please contact a VisIt developer.
# MAINTENANCE ISSUE: SetSuppressMessagesRPC is not handled in Logging.C. Please contact a VisIt developer.
SaveSession("/Users/Jamie/.visit/crash_recovery.4536.session")
# MAINTENANCE ISSUE: SetSuppressMessagesRPC is not handled in Logging.C. Please contact a VisIt developer.
# MAINTENANCE ISSUE: SetSuppressMessagesRPC is not handled in Logging.C. Please contact a VisIt developer.
SaveSession("/Users/Jamie/.visit/crash_recovery.4536.session")
# MAINTENANCE ISSUE: SetSuppressMessagesRPC is not handled in Logging.C. Please contact a VisIt developer.
# MAINTENANCE ISSUE: SetSuppressMessagesRPC is not handled in Logging.C. Please contact a VisIt developer.
SaveSession("/Users/Jamie/.visit/crash_recovery.4536.session")
# MAINTENANCE ISSUE: SetSuppressMessagesRPC is not handled in Logging.C. Please contact a VisIt developer.
# MAINTENANCE ISSUE: SetSuppressMessagesRPC is not handled in Logging.C. Please contact a VisIt developer.
SaveSession("/Users/Jamie/.visit/crash_recovery.4536.session")
# MAINTENANCE ISSUE: SetSuppressMessagesRPC is not handled in Logging.C. Please contact a VisIt developer.
# MAINTENANCE ISSUE: SetSuppressMessagesRPC is not handled in Logging.C. Please contact a VisIt developer.
SaveSession("/Users/Jamie/.visit/crash_recovery.4536.session")
# MAINTENANCE ISSUE: SetSuppressMessagesRPC is not handled in Logging.C. Please contact a VisIt developer.
# MAINTENANCE ISSUE: SetSuppressMessagesRPC is not handled in Logging.C. Please contact a VisIt developer.
SaveSession("/Users/Jamie/.visit/crash_recovery.4536.session")
# MAINTENANCE ISSUE: SetSuppressMessagesRPC is not handled in Logging.C. Please contact a VisIt developer.
# MAINTENANCE ISSUE: SetSuppressMessagesRPC is not handled in Logging.C. Please contact a VisIt developer.
SaveSession("/Users/Jamie/.visit/crash_recovery.4536.session")
# MAINTENANCE ISSUE: SetSuppressMessagesRPC is not handled in Logging.C. Please contact a VisIt developer.
# MAINTENANCE ISSUE: SetSuppressMessagesRPC is not handled in Logging.C. Please contact a VisIt developer.
SaveSession("/Users/Jamie/.visit/crash_recovery.4536.session")
# MAINTENANCE ISSUE: SetSuppressMessagesRPC is not handled in Logging.C. Please contact a VisIt developer.
# MAINTENANCE ISSUE: SetSuppressMessagesRPC is not handled in Logging.C. Please contact a VisIt developer.
SaveSession("/Users/Jamie/.visit/crash_recovery.4536.session")
# MAINTENANCE ISSUE: SetSuppressMessagesRPC is not handled in Logging.C. Please contact a VisIt developer.
# MAINTENANCE ISSUE: SetSuppressMessagesRPC is not handled in Logging.C. Please contact a VisIt developer.
SaveSession("/Users/Jamie/.visit/crash_recovery.4536.session")
# MAINTENANCE ISSUE: SetSuppressMessagesRPC is not handled in Logging.C. Please contact a VisIt developer.
# MAINTENANCE ISSUE: SetSuppressMessagesRPC is not handled in Logging.C. Please contact a VisIt developer.
SaveSession("/Users/Jamie/.visit/crash_recovery.4536.session")
# MAINTENANCE ISSUE: SetSuppressMessagesRPC is not handled in Logging.C. Please contact a VisIt developer.
# MAINTENANCE ISSUE: SetSuppressMessagesRPC is not handled in Logging.C. Please contact a VisIt developer.
SaveSession("/Users/Jamie/.visit/crash_recovery.4536.session")
# MAINTENANCE ISSUE: SetSuppressMessagesRPC is not handled in Logging.C. Please contact a VisIt developer.
# MAINTENANCE ISSUE: SetSuppressMessagesRPC is not handled in Logging.C. Please contact a VisIt developer.
SaveSession("/Users/Jamie/.visit/crash_recovery.4536.session")
# MAINTENANCE ISSUE: SetSuppressMessagesRPC is not handled in Logging.C. Please contact a VisIt developer.
# MAINTENANCE ISSUE: SetSuppressMessagesRPC is not handled in Logging.C. Please contact a VisIt developer.
SaveSession("/Users/Jamie/.visit/crash_recovery.4536.session")
# MAINTENANCE ISSUE: SetSuppressMessagesRPC is not handled in Logging.C. Please contact a VisIt developer.
# MAINTENANCE ISSUE: SetSuppressMessagesRPC is not handled in Logging.C. Please contact a VisIt developer.
SaveSession("/Users/Jamie/.visit/crash_recovery.4536.session")
# MAINTENANCE ISSUE: SetSuppressMessagesRPC is not handled in Logging.C. Please contact a VisIt developer.
# MAINTENANCE ISSUE: SetSuppressMessagesRPC is not handled in Logging.C. Please contact a VisIt developer.
SaveSession("/Users/Jamie/.visit/crash_recovery.4536.session")
# MAINTENANCE ISSUE: SetSuppressMessagesRPC is not handled in Logging.C. Please contact a VisIt developer.
# MAINTENANCE ISSUE: SetSuppressMessagesRPC is not handled in Logging.C. Please contact a VisIt developer.
SaveSession("/Users/Jamie/.visit/crash_recovery.4536.session")
# MAINTENANCE ISSUE: SetSuppressMessagesRPC is not handled in Logging.C. Please contact a VisIt developer.
# MAINTENANCE ISSUE: SetSuppressMessagesRPC is not handled in Logging.C. Please contact a VisIt developer.
SaveSession("/Users/Jamie/.visit/crash_recovery.4536.session")
# MAINTENANCE ISSUE: SetSuppressMessagesRPC is not handled in Logging.C. Please contact a VisIt developer.
# MAINTENANCE ISSUE: SetSuppressMessagesRPC is not handled in Logging.C. Please contact a VisIt developer.
SaveSession("/Users/Jamie/.visit/crash_recovery.4536.session")
# MAINTENANCE ISSUE: SetSuppressMessagesRPC is not handled in Logging.C. Please contact a VisIt developer.
# MAINTENANCE ISSUE: SetSuppressMessagesRPC is not handled in Logging.C. Please contact a VisIt developer.
SaveSession("/Users/Jamie/.visit/crash_recovery.4536.session")
# MAINTENANCE ISSUE: SetSuppressMessagesRPC is not handled in Logging.C. Please contact a VisIt developer.
# MAINTENANCE ISSUE: SetSuppressMessagesRPC is not handled in Logging.C. Please contact a VisIt developer.
SaveSession("/Users/Jamie/.visit/crash_recovery.4536.session")
# MAINTENANCE ISSUE: SetSuppressMessagesRPC is not handled in Logging.C. Please contact a VisIt developer.
# MAINTENANCE ISSUE: SetSuppressMessagesRPC is not handled in Logging.C. Please contact a VisIt developer.
SaveSession("/Users/Jamie/.visit/crash_recovery.4536.session")
# MAINTENANCE ISSUE: SetSuppressMessagesRPC is not handled in Logging.C. Please contact a VisIt developer.
# MAINTENANCE ISSUE: SetSuppressMessagesRPC is not handled in Logging.C. Please contact a VisIt developer.
SaveSession("/Users/Jamie/.visit/crash_recovery.4536.session")
# MAINTENANCE ISSUE: SetSuppressMessagesRPC is not handled in Logging.C. Please contact a VisIt developer.
# MAINTENANCE ISSUE: SetSuppressMessagesRPC is not handled in Logging.C. Please contact a VisIt developer.
SaveSession("/Users/Jamie/.visit/crash_recovery.4536.session")
# MAINTENANCE ISSUE: SetSuppressMessagesRPC is not handled in Logging.C. Please contact a VisIt developer.
# MAINTENANCE ISSUE: SetSuppressMessagesRPC is not handled in Logging.C. Please contact a VisIt developer.
SaveSession("/Users/Jamie/.visit/crash_recovery.4536.session")
# MAINTENANCE ISSUE: SetSuppressMessagesRPC is not handled in Logging.C. Please contact a VisIt developer.
# MAINTENANCE ISSUE: SetSuppressMessagesRPC is not handled in Logging.C. Please contact a VisIt developer.
SaveSession("/Users/Jamie/.visit/crash_recovery.4536.session")
# MAINTENANCE ISSUE: SetSuppressMessagesRPC is not handled in Logging.C. Please contact a VisIt developer.
# MAINTENANCE ISSUE: SetSuppressMessagesRPC is not handled in Logging.C. Please contact a VisIt developer.
SaveSession("/Users/Jamie/.visit/crash_recovery.4536.session")
# MAINTENANCE ISSUE: SetSuppressMessagesRPC is not handled in Logging.C. Please contact a VisIt developer.
# MAINTENANCE ISSUE: SetSuppressMessagesRPC is not handled in Logging.C. Please contact a VisIt developer.
SaveSession("/Users/Jamie/.visit/crash_recovery.4536.session")
# MAINTENANCE ISSUE: SetSuppressMessagesRPC is not handled in Logging.C. Please contact a VisIt developer.
# MAINTENANCE ISSUE: SetSuppressMessagesRPC is not handled in Logging.C. Please contact a VisIt developer.
SaveSession("/Users/Jamie/.visit/crash_recovery.4536.session")
# MAINTENANCE ISSUE: SetSuppressMessagesRPC is not handled in Logging.C. Please contact a VisIt developer.
# MAINTENANCE ISSUE: SetSuppressMessagesRPC is not handled in Logging.C. Please contact a VisIt developer.
SaveSession("/Users/Jamie/.visit/crash_recovery.4536.session")
# MAINTENANCE ISSUE: SetSuppressMessagesRPC is not handled in Logging.C. Please contact a VisIt developer.
# MAINTENANCE ISSUE: SetSuppressMessagesRPC is not handled in Logging.C. Please contact a VisIt developer.
SaveSession("/Users/Jamie/.visit/crash_recovery.4536.session")
# MAINTENANCE ISSUE: SetSuppressMessagesRPC is not handled in Logging.C. Please contact a VisIt developer.
# MAINTENANCE ISSUE: SetSuppressMessagesRPC is not handled in Logging.C. Please contact a VisIt developer.
SaveSession("/Users/Jamie/.visit/crash_recovery.4536.session")
# MAINTENANCE ISSUE: SetSuppressMessagesRPC is not handled in Logging.C. Please contact a VisIt developer.
# MAINTENANCE ISSUE: SetSuppressMessagesRPC is not handled in Logging.C. Please contact a VisIt developer.
SaveSession("/Users/Jamie/.visit/crash_recovery.4536.session")
# MAINTENANCE ISSUE: SetSuppressMessagesRPC is not handled in Logging.C. Please contact a VisIt developer.
# MAINTENANCE ISSUE: SetSuppressMessagesRPC is not handled in Logging.C. Please contact a VisIt developer.
SaveSession("/Users/Jamie/.visit/crash_recovery.4536.session")
# MAINTENANCE ISSUE: SetSuppressMessagesRPC is not handled in Logging.C. Please contact a VisIt developer.
# MAINTENANCE ISSUE: SetSuppressMessagesRPC is not handled in Logging.C. Please contact a VisIt developer.
SaveSession("/Users/Jamie/.visit/crash_recovery.4536.session")
# MAINTENANCE ISSUE: SetSuppressMessagesRPC is not handled in Logging.C. Please contact a VisIt developer.
# MAINTENANCE ISSUE: SetSuppressMessagesRPC is not handled in Logging.C. Please contact a VisIt developer.
SaveSession("/Users/Jamie/.visit/crash_recovery.4536.session")
# MAINTENANCE ISSUE: SetSuppressMessagesRPC is not handled in Logging.C. Please contact a VisIt developer.
# MAINTENANCE ISSUE: SetSuppressMessagesRPC is not handled in Logging.C. Please contact a VisIt developer.
SaveSession("/Users/Jamie/.visit/crash_recovery.4536.session")
# MAINTENANCE ISSUE: SetSuppressMessagesRPC is not handled in Logging.C. Please contact a VisIt developer.
# MAINTENANCE ISSUE: SetSuppressMessagesRPC is not handled in Logging.C. Please contact a VisIt developer.
SaveSession("/Users/Jamie/.visit/crash_recovery.4536.session")
# MAINTENANCE ISSUE: SetSuppressMessagesRPC is not handled in Logging.C. Please contact a VisIt developer.
# MAINTENANCE ISSUE: SetSuppressMessagesRPC is not handled in Logging.C. Please contact a VisIt developer.
SaveSession("/Users/Jamie/.visit/crash_recovery.4536.session")
# MAINTENANCE ISSUE: SetSuppressMessagesRPC is not handled in Logging.C. Please contact a VisIt developer.
# MAINTENANCE ISSUE: SetSuppressMessagesRPC is not handled in Logging.C. Please contact a VisIt developer.
SaveSession("/Users/Jamie/.visit/crash_recovery.4536.session")
# MAINTENANCE ISSUE: SetSuppressMessagesRPC is not handled in Logging.C. Please contact a VisIt developer.
# MAINTENANCE ISSUE: SetSuppressMessagesRPC is not handled in Logging.C. Please contact a VisIt developer.
SaveSession("/Users/Jamie/.visit/crash_recovery.4536.session")
# MAINTENANCE ISSUE: SetSuppressMessagesRPC is not handled in Logging.C. Please contact a VisIt developer.
# MAINTENANCE ISSUE: SetSuppressMessagesRPC is not handled in Logging.C. Please contact a VisIt developer.
SaveSession("/Users/Jamie/.visit/crash_recovery.4536.session")
# MAINTENANCE ISSUE: SetSuppressMessagesRPC is not handled in Logging.C. Please contact a VisIt developer.
# MAINTENANCE ISSUE: SetSuppressMessagesRPC is not handled in Logging.C. Please contact a VisIt developer.
SaveSession("/Users/Jamie/.visit/crash_recovery.4536.session")
# MAINTENANCE ISSUE: SetSuppressMessagesRPC is not handled in Logging.C. Please contact a VisIt developer.
# MAINTENANCE ISSUE: SetSuppressMessagesRPC is not handled in Logging.C. Please contact a VisIt developer.
SaveSession("/Users/Jamie/.visit/crash_recovery.4536.session")
# MAINTENANCE ISSUE: SetSuppressMessagesRPC is not handled in Logging.C. Please contact a VisIt developer.
# MAINTENANCE ISSUE: SetSuppressMessagesRPC is not handled in Logging.C. Please contact a VisIt developer.
SaveSession("/Users/Jamie/.visit/crash_recovery.4536.session")
# MAINTENANCE ISSUE: SetSuppressMessagesRPC is not handled in Logging.C. Please contact a VisIt developer.
# MAINTENANCE ISSUE: SetSuppressMessagesRPC is not handled in Logging.C. Please contact a VisIt developer.
SaveSession("/Users/Jamie/.visit/crash_recovery.4536.session")
# MAINTENANCE ISSUE: SetSuppressMessagesRPC is not handled in Logging.C. Please contact a VisIt developer.
# MAINTENANCE ISSUE: SetSuppressMessagesRPC is not handled in Logging.C. Please contact a VisIt developer.
SaveSession("/Users/Jamie/.visit/crash_recovery.4536.session")
# MAINTENANCE ISSUE: SetSuppressMessagesRPC is not handled in Logging.C. Please contact a VisIt developer.
# MAINTENANCE ISSUE: SetSuppressMessagesRPC is not handled in Logging.C. Please contact a VisIt developer.
SaveSession("/Users/Jamie/.visit/crash_recovery.4536.session")
# MAINTENANCE ISSUE: SetSuppressMessagesRPC is not handled in Logging.C. Please contact a VisIt developer.
# MAINTENANCE ISSUE: SetSuppressMessagesRPC is not handled in Logging.C. Please contact a VisIt developer.
SaveSession("/Users/Jamie/.visit/crash_recovery.4536.session")
# MAINTENANCE ISSUE: SetSuppressMessagesRPC is not handled in Logging.C. Please contact a VisIt developer.
# MAINTENANCE ISSUE: SetSuppressMessagesRPC is not handled in Logging.C. Please contact a VisIt developer.
SaveSession("/Users/Jamie/.visit/crash_recovery.4536.session")
# MAINTENANCE ISSUE: SetSuppressMessagesRPC is not handled in Logging.C. Please contact a VisIt developer.
# MAINTENANCE ISSUE: SetSuppressMessagesRPC is not handled in Logging.C. Please contact a VisIt developer.
SaveSession("/Users/Jamie/.visit/crash_recovery.4536.session")
# MAINTENANCE ISSUE: SetSuppressMessagesRPC is not handled in Logging.C. Please contact a VisIt developer.
# MAINTENANCE ISSUE: SetSuppressMessagesRPC is not handled in Logging.C. Please contact a VisIt developer.
SaveSession("/Users/Jamie/.visit/crash_recovery.4536.session")
# MAINTENANCE ISSUE: SetSuppressMessagesRPC is not handled in Logging.C. Please contact a VisIt developer.
# MAINTENANCE ISSUE: SetSuppressMessagesRPC is not handled in Logging.C. Please contact a VisIt developer.
SaveSession("/Users/Jamie/.visit/crash_recovery.4536.session")
# MAINTENANCE ISSUE: SetSuppressMessagesRPC is not handled in Logging.C. Please contact a VisIt developer.
# MAINTENANCE ISSUE: SetSuppressMessagesRPC is not handled in Logging.C. Please contact a VisIt developer.
SaveSession("/Users/Jamie/.visit/crash_recovery.4536.session")
# MAINTENANCE ISSUE: SetSuppressMessagesRPC is not handled in Logging.C. Please contact a VisIt developer.
# MAINTENANCE ISSUE: SetSuppressMessagesRPC is not handled in Logging.C. Please contact a VisIt developer.
SaveSession("/Users/Jamie/.visit/crash_recovery.4536.session")
# MAINTENANCE ISSUE: SetSuppressMessagesRPC is not handled in Logging.C. Please contact a VisIt developer.
# MAINTENANCE ISSUE: SetSuppressMessagesRPC is not handled in Logging.C. Please contact a VisIt developer.
SaveSession("/Users/Jamie/.visit/crash_recovery.4536.session")
# MAINTENANCE ISSUE: SetSuppressMessagesRPC is not handled in Logging.C. Please contact a VisIt developer.
# MAINTENANCE ISSUE: SetSuppressMessagesRPC is not handled in Logging.C. Please contact a VisIt developer.
SaveSession("/Users/Jamie/.visit/crash_recovery.4536.session")
# MAINTENANCE ISSUE: SetSuppressMessagesRPC is not handled in Logging.C. Please contact a VisIt developer.
# MAINTENANCE ISSUE: SetSuppressMessagesRPC is not handled in Logging.C. Please contact a VisIt developer.
SaveSession("/Users/Jamie/.visit/crash_recovery.4536.session")
# MAINTENANCE ISSUE: SetSuppressMessagesRPC is not handled in Logging.C. Please contact a VisIt developer.
# MAINTENANCE ISSUE: SetSuppressMessagesRPC is not handled in Logging.C. Please contact a VisIt developer.
SaveSession("/Users/Jamie/.visit/crash_recovery.4536.session")
# MAINTENANCE ISSUE: SetSuppressMessagesRPC is not handled in Logging.C. Please contact a VisIt developer.
# MAINTENANCE ISSUE: SetSuppressMessagesRPC is not handled in Logging.C. Please contact a VisIt developer.
SaveSession("/Users/Jamie/.visit/crash_recovery.4536.session")
# MAINTENANCE ISSUE: SetSuppressMessagesRPC is not handled in Logging.C. Please contact a VisIt developer.
# MAINTENANCE ISSUE: SetSuppressMessagesRPC is not handled in Logging.C. Please contact a VisIt developer.
SaveSession("/Users/Jamie/.visit/crash_recovery.4536.session")
# MAINTENANCE ISSUE: SetSuppressMessagesRPC is not handled in Logging.C. Please contact a VisIt developer.
# MAINTENANCE ISSUE: SetSuppressMessagesRPC is not handled in Logging.C. Please contact a VisIt developer.
SaveSession("/Users/Jamie/.visit/crash_recovery.4536.session")
# MAINTENANCE ISSUE: SetSuppressMessagesRPC is not handled in Logging.C. Please contact a VisIt developer.
# MAINTENANCE ISSUE: SetSuppressMessagesRPC is not handled in Logging.C. Please contact a VisIt developer.
SaveSession("/Users/Jamie/.visit/crash_recovery.4536.session")
# MAINTENANCE ISSUE: SetSuppressMessagesRPC is not handled in Logging.C. Please contact a VisIt developer.
# MAINTENANCE ISSUE: SetSuppressMessagesRPC is not handled in Logging.C. Please contact a VisIt developer.
SaveSession("/Users/Jamie/.visit/crash_recovery.4536.session")
# MAINTENANCE ISSUE: SetSuppressMessagesRPC is not handled in Logging.C. Please contact a VisIt developer.
# MAINTENANCE ISSUE: SetSuppressMessagesRPC is not handled in Logging.C. Please contact a VisIt developer.
SaveSession("/Users/Jamie/.visit/crash_recovery.4536.session")
# MAINTENANCE ISSUE: SetSuppressMessagesRPC is not handled in Logging.C. Please contact a VisIt developer.
# MAINTENANCE ISSUE: SetSuppressMessagesRPC is not handled in Logging.C. Please contact a VisIt developer.
SaveSession("/Users/Jamie/.visit/crash_recovery.4536.session")
# MAINTENANCE ISSUE: SetSuppressMessagesRPC is not handled in Logging.C. Please contact a VisIt developer.
# MAINTENANCE ISSUE: SetSuppressMessagesRPC is not handled in Logging.C. Please contact a VisIt developer.
SaveSession("/Users/Jamie/.visit/crash_recovery.4536.session")
# MAINTENANCE ISSUE: SetSuppressMessagesRPC is not handled in Logging.C. Please contact a VisIt developer.
# MAINTENANCE ISSUE: SetSuppressMessagesRPC is not handled in Logging.C. Please contact a VisIt developer.
SaveSession("/Users/Jamie/.visit/crash_recovery.4536.session")
# MAINTENANCE ISSUE: SetSuppressMessagesRPC is not handled in Logging.C. Please contact a VisIt developer.
# MAINTENANCE ISSUE: SetSuppressMessagesRPC is not handled in Logging.C. Please contact a VisIt developer.
SaveSession("/Users/Jamie/.visit/crash_recovery.4536.session")
# MAINTENANCE ISSUE: SetSuppressMessagesRPC is not handled in Logging.C. Please contact a VisIt developer.
# MAINTENANCE ISSUE: SetSuppressMessagesRPC is not handled in Logging.C. Please contact a VisIt developer.
SaveSession("/Users/Jamie/.visit/crash_recovery.4536.session")
# MAINTENANCE ISSUE: SetSuppressMessagesRPC is not handled in Logging.C. Please contact a VisIt developer.
# MAINTENANCE ISSUE: SetSuppressMessagesRPC is not handled in Logging.C. Please contact a VisIt developer.
SaveSession("/Users/Jamie/.visit/crash_recovery.4536.session")
# MAINTENANCE ISSUE: SetSuppressMessagesRPC is not handled in Logging.C. Please contact a VisIt developer.
# MAINTENANCE ISSUE: SetSuppressMessagesRPC is not handled in Logging.C. Please contact a VisIt developer.
SaveSession("/Users/Jamie/.visit/crash_recovery.4536.session")
# MAINTENANCE ISSUE: SetSuppressMessagesRPC is not handled in Logging.C. Please contact a VisIt developer.
# MAINTENANCE ISSUE: SetSuppressMessagesRPC is not handled in Logging.C. Please contact a VisIt developer.
SaveSession("/Users/Jamie/.visit/crash_recovery.4536.session")
# MAINTENANCE ISSUE: SetSuppressMessagesRPC is not handled in Logging.C. Please contact a VisIt developer.
# MAINTENANCE ISSUE: SetSuppressMessagesRPC is not handled in Logging.C. Please contact a VisIt developer.
SaveSession("/Users/Jamie/.visit/crash_recovery.4536.session")
# MAINTENANCE ISSUE: SetSuppressMessagesRPC is not handled in Logging.C. Please contact a VisIt developer.
# MAINTENANCE ISSUE: SetSuppressMessagesRPC is not handled in Logging.C. Please contact a VisIt developer.
SaveSession("/Users/Jamie/.visit/crash_recovery.4536.session")
# MAINTENANCE ISSUE: SetSuppressMessagesRPC is not handled in Logging.C. Please contact a VisIt developer.
# MAINTENANCE ISSUE: SetSuppressMessagesRPC is not handled in Logging.C. Please contact a VisIt developer.
SaveSession("/Users/Jamie/.visit/crash_recovery.4536.session")
# MAINTENANCE ISSUE: SetSuppressMessagesRPC is not handled in Logging.C. Please contact a VisIt developer.
# MAINTENANCE ISSUE: SetSuppressMessagesRPC is not handled in Logging.C. Please contact a VisIt developer.
SaveSession("/Users/Jamie/.visit/crash_recovery.4536.session")
# MAINTENANCE ISSUE: SetSuppressMessagesRPC is not handled in Logging.C. Please contact a VisIt developer.
# MAINTENANCE ISSUE: SetSuppressMessagesRPC is not handled in Logging.C. Please contact a VisIt developer.
SaveSession("/Users/Jamie/.visit/crash_recovery.4536.session")
# MAINTENANCE ISSUE: SetSuppressMessagesRPC is not handled in Logging.C. Please contact a VisIt developer.
# MAINTENANCE ISSUE: SetSuppressMessagesRPC is not handled in Logging.C. Please contact a VisIt developer.
SaveSession("/Users/Jamie/.visit/crash_recovery.4536.session")
# MAINTENANCE ISSUE: SetSuppressMessagesRPC is not handled in Logging.C. Please contact a VisIt developer.
# MAINTENANCE ISSUE: SetSuppressMessagesRPC is not handled in Logging.C. Please contact a VisIt developer.
SaveSession("/Users/Jamie/.visit/crash_recovery.4536.session")
# MAINTENANCE ISSUE: SetSuppressMessagesRPC is not handled in Logging.C. Please contact a VisIt developer.
# MAINTENANCE ISSUE: SetSuppressMessagesRPC is not handled in Logging.C. Please contact a VisIt developer.
SaveSession("/Users/Jamie/.visit/crash_recovery.4536.session")
# MAINTENANCE ISSUE: SetSuppressMessagesRPC is not handled in Logging.C. Please contact a VisIt developer.
# MAINTENANCE ISSUE: SetSuppressMessagesRPC is not handled in Logging.C. Please contact a VisIt developer.
SaveSession("/Users/Jamie/.visit/crash_recovery.4536.session")
# MAINTENANCE ISSUE: SetSuppressMessagesRPC is not handled in Logging.C. Please contact a VisIt developer.
# MAINTENANCE ISSUE: SetSuppressMessagesRPC is not handled in Logging.C. Please contact a VisIt developer.
SaveSession("/Users/Jamie/.visit/crash_recovery.4536.session")
# MAINTENANCE ISSUE: SetSuppressMessagesRPC is not handled in Logging.C. Please contact a VisIt developer.
# MAINTENANCE ISSUE: SetSuppressMessagesRPC is not handled in Logging.C. Please contact a VisIt developer.
SaveSession("/Users/Jamie/.visit/crash_recovery.4536.session")
# MAINTENANCE ISSUE: SetSuppressMessagesRPC is not handled in Logging.C. Please contact a VisIt developer.
# MAINTENANCE ISSUE: SetSuppressMessagesRPC is not handled in Logging.C. Please contact a VisIt developer.
SaveSession("/Users/Jamie/.visit/crash_recovery.4536.session")
# MAINTENANCE ISSUE: SetSuppressMessagesRPC is not handled in Logging.C. Please contact a VisIt developer.
# MAINTENANCE ISSUE: SetSuppressMessagesRPC is not handled in Logging.C. Please contact a VisIt developer.
SaveSession("/Users/Jamie/.visit/crash_recovery.4536.session")
# MAINTENANCE ISSUE: SetSuppressMessagesRPC is not handled in Logging.C. Please contact a VisIt developer.
# MAINTENANCE ISSUE: SetSuppressMessagesRPC is not handled in Logging.C. Please contact a VisIt developer.
SaveSession("/Users/Jamie/.visit/crash_recovery.4536.session")
# MAINTENANCE ISSUE: SetSuppressMessagesRPC is not handled in Logging.C. Please contact a VisIt developer.
# MAINTENANCE ISSUE: SetSuppressMessagesRPC is not handled in Logging.C. Please contact a VisIt developer.
SaveSession("/Users/Jamie/.visit/crash_recovery.4536.session")
# MAINTENANCE ISSUE: SetSuppressMessagesRPC is not handled in Logging.C. Please contact a VisIt developer.
# MAINTENANCE ISSUE: SetSuppressMessagesRPC is not handled in Logging.C. Please contact a VisIt developer.
SaveSession("/Users/Jamie/.visit/crash_recovery.4536.session")
# MAINTENANCE ISSUE: SetSuppressMessagesRPC is not handled in Logging.C. Please contact a VisIt developer.
# MAINTENANCE ISSUE: SetSuppressMessagesRPC is not handled in Logging.C. Please contact a VisIt developer.
SaveSession("/Users/Jamie/.visit/crash_recovery.4536.session")
# MAINTENANCE ISSUE: SetSuppressMessagesRPC is not handled in Logging.C. Please contact a VisIt developer.
# MAINTENANCE ISSUE: SetSuppressMessagesRPC is not handled in Logging.C. Please contact a VisIt developer.
SaveSession("/Users/Jamie/.visit/crash_recovery.4536.session")
# MAINTENANCE ISSUE: SetSuppressMessagesRPC is not handled in Logging.C. Please contact a VisIt developer.
# MAINTENANCE ISSUE: SetSuppressMessagesRPC is not handled in Logging.C. Please contact a VisIt developer.
SaveSession("/Users/Jamie/.visit/crash_recovery.4536.session")
# MAINTENANCE ISSUE: SetSuppressMessagesRPC is not handled in Logging.C. Please contact a VisIt developer.
# MAINTENANCE ISSUE: SetSuppressMessagesRPC is not handled in Logging.C. Please contact a VisIt developer.
SaveSession("/Users/Jamie/.visit/crash_recovery.4536.session")
# MAINTENANCE ISSUE: SetSuppressMessagesRPC is not handled in Logging.C. Please contact a VisIt developer.
# MAINTENANCE ISSUE: SetSuppressMessagesRPC is not handled in Logging.C. Please contact a VisIt developer.
SaveSession("/Users/Jamie/.visit/crash_recovery.4536.session")
# MAINTENANCE ISSUE: SetSuppressMessagesRPC is not handled in Logging.C. Please contact a VisIt developer.
# MAINTENANCE ISSUE: SetSuppressMessagesRPC is not handled in Logging.C. Please contact a VisIt developer.
SaveSession("/Users/Jamie/.visit/crash_recovery.4536.session")
# MAINTENANCE ISSUE: SetSuppressMessagesRPC is not handled in Logging.C. Please contact a VisIt developer.
# MAINTENANCE ISSUE: SetSuppressMessagesRPC is not handled in Logging.C. Please contact a VisIt developer.
SaveSession("/Users/Jamie/.visit/crash_recovery.4536.session")
# MAINTENANCE ISSUE: SetSuppressMessagesRPC is not handled in Logging.C. Please contact a VisIt developer.
# MAINTENANCE ISSUE: SetSuppressMessagesRPC is not handled in Logging.C. Please contact a VisIt developer.
SaveSession("/Users/Jamie/.visit/crash_recovery.4536.session")
# MAINTENANCE ISSUE: SetSuppressMessagesRPC is not handled in Logging.C. Please contact a VisIt developer.
# MAINTENANCE ISSUE: SetSuppressMessagesRPC is not handled in Logging.C. Please contact a VisIt developer.
SaveSession("/Users/Jamie/.visit/crash_recovery.4536.session")
# MAINTENANCE ISSUE: SetSuppressMessagesRPC is not handled in Logging.C. Please contact a VisIt developer.
# MAINTENANCE ISSUE: SetSuppressMessagesRPC is not handled in Logging.C. Please contact a VisIt developer.
SaveSession("/Users/Jamie/.visit/crash_recovery.4536.session")
# MAINTENANCE ISSUE: SetSuppressMessagesRPC is not handled in Logging.C. Please contact a VisIt developer.
# MAINTENANCE ISSUE: SetSuppressMessagesRPC is not handled in Logging.C. Please contact a VisIt developer.
SaveSession("/Users/Jamie/.visit/crash_recovery.4536.session")
# MAINTENANCE ISSUE: SetSuppressMessagesRPC is not handled in Logging.C. Please contact a VisIt developer.
# MAINTENANCE ISSUE: SetSuppressMessagesRPC is not handled in Logging.C. Please contact a VisIt developer.
SaveSession("/Users/Jamie/.visit/crash_recovery.4536.session")
# MAINTENANCE ISSUE: SetSuppressMessagesRPC is not handled in Logging.C. Please contact a VisIt developer.
# MAINTENANCE ISSUE: SetSuppressMessagesRPC is not handled in Logging.C. Please contact a VisIt developer.
SaveSession("/Users/Jamie/.visit/crash_recovery.4536.session")
# MAINTENANCE ISSUE: SetSuppressMessagesRPC is not handled in Logging.C. Please contact a VisIt developer.
# MAINTENANCE ISSUE: SetSuppressMessagesRPC is not handled in Logging.C. Please contact a VisIt developer.
SaveSession("/Users/Jamie/.visit/crash_recovery.4536.session")
# MAINTENANCE ISSUE: SetSuppressMessagesRPC is not handled in Logging.C. Please contact a VisIt developer.
# MAINTENANCE ISSUE: SetSuppressMessagesRPC is not handled in Logging.C. Please contact a VisIt developer.
SaveSession("/Users/Jamie/.visit/crash_recovery.4536.session")
# MAINTENANCE ISSUE: SetSuppressMessagesRPC is not handled in Logging.C. Please contact a VisIt developer.
# MAINTENANCE ISSUE: SetSuppressMessagesRPC is not handled in Logging.C. Please contact a VisIt developer.
SaveSession("/Users/Jamie/.visit/crash_recovery.4536.session")
# MAINTENANCE ISSUE: SetSuppressMessagesRPC is not handled in Logging.C. Please contact a VisIt developer.
# MAINTENANCE ISSUE: SetSuppressMessagesRPC is not handled in Logging.C. Please contact a VisIt developer.
SaveSession("/Users/Jamie/.visit/crash_recovery.4536.session")
# MAINTENANCE ISSUE: SetSuppressMessagesRPC is not handled in Logging.C. Please contact a VisIt developer.
# MAINTENANCE ISSUE: SetSuppressMessagesRPC is not handled in Logging.C. Please contact a VisIt developer.
SaveSession("/Users/Jamie/.visit/crash_recovery.4536.session")
# MAINTENANCE ISSUE: SetSuppressMessagesRPC is not handled in Logging.C. Please contact a VisIt developer.
# MAINTENANCE ISSUE: SetSuppressMessagesRPC is not handled in Logging.C. Please contact a VisIt developer.
SaveSession("/Users/Jamie/.visit/crash_recovery.4536.session")
# MAINTENANCE ISSUE: SetSuppressMessagesRPC is not handled in Logging.C. Please contact a VisIt developer.
# MAINTENANCE ISSUE: SetSuppressMessagesRPC is not handled in Logging.C. Please contact a VisIt developer.
SaveSession("/Users/Jamie/.visit/crash_recovery.4536.session")
# MAINTENANCE ISSUE: SetSuppressMessagesRPC is not handled in Logging.C. Please contact a VisIt developer.
# MAINTENANCE ISSUE: SetSuppressMessagesRPC is not handled in Logging.C. Please contact a VisIt developer.
SaveSession("/Users/Jamie/.visit/crash_recovery.4536.session")
# MAINTENANCE ISSUE: SetSuppressMessagesRPC is not handled in Logging.C. Please contact a VisIt developer.
# MAINTENANCE ISSUE: SetSuppressMessagesRPC is not handled in Logging.C. Please contact a VisIt developer.
SaveSession("/Users/Jamie/.visit/crash_recovery.4536.session")
# MAINTENANCE ISSUE: SetSuppressMessagesRPC is not handled in Logging.C. Please contact a VisIt developer.
# MAINTENANCE ISSUE: SetSuppressMessagesRPC is not handled in Logging.C. Please contact a VisIt developer.
SaveSession("/Users/Jamie/.visit/crash_recovery.4536.session")
# MAINTENANCE ISSUE: SetSuppressMessagesRPC is not handled in Logging.C. Please contact a VisIt developer.
# MAINTENANCE ISSUE: SetSuppressMessagesRPC is not handled in Logging.C. Please contact a VisIt developer.
SaveSession("/Users/Jamie/.visit/crash_recovery.4536.session")
# MAINTENANCE ISSUE: SetSuppressMessagesRPC is not handled in Logging.C. Please contact a VisIt developer.
# MAINTENANCE ISSUE: SetSuppressMessagesRPC is not handled in Logging.C. Please contact a VisIt developer.
SaveSession("/Users/Jamie/.visit/crash_recovery.4536.session")
# MAINTENANCE ISSUE: SetSuppressMessagesRPC is not handled in Logging.C. Please contact a VisIt developer.
# MAINTENANCE ISSUE: SetSuppressMessagesRPC is not handled in Logging.C. Please contact a VisIt developer.
SaveSession("/Users/Jamie/.visit/crash_recovery.4536.session")
# MAINTENANCE ISSUE: SetSuppressMessagesRPC is not handled in Logging.C. Please contact a VisIt developer.
# MAINTENANCE ISSUE: SetSuppressMessagesRPC is not handled in Logging.C. Please contact a VisIt developer.
SaveSession("/Users/Jamie/.visit/crash_recovery.4536.session")
# MAINTENANCE ISSUE: SetSuppressMessagesRPC is not handled in Logging.C. Please contact a VisIt developer.
# MAINTENANCE ISSUE: SetSuppressMessagesRPC is not handled in Logging.C. Please contact a VisIt developer.
SaveSession("/Users/Jamie/.visit/crash_recovery.4536.session")
# MAINTENANCE ISSUE: SetSuppressMessagesRPC is not handled in Logging.C. Please contact a VisIt developer.
# MAINTENANCE ISSUE: SetSuppressMessagesRPC is not handled in Logging.C. Please contact a VisIt developer.
SaveSession("/Users/Jamie/.visit/crash_recovery.4536.session")
# MAINTENANCE ISSUE: SetSuppressMessagesRPC is not handled in Logging.C. Please contact a VisIt developer.
# MAINTENANCE ISSUE: SetSuppressMessagesRPC is not handled in Logging.C. Please contact a VisIt developer.
SaveSession("/Users/Jamie/.visit/crash_recovery.4536.session")
# MAINTENANCE ISSUE: SetSuppressMessagesRPC is not handled in Logging.C. Please contact a VisIt developer.
# MAINTENANCE ISSUE: SetSuppressMessagesRPC is not handled in Logging.C. Please contact a VisIt developer.
SaveSession("/Users/Jamie/.visit/crash_recovery.4536.session")
# MAINTENANCE ISSUE: SetSuppressMessagesRPC is not handled in Logging.C. Please contact a VisIt developer.
# MAINTENANCE ISSUE: SetSuppressMessagesRPC is not handled in Logging.C. Please contact a VisIt developer.
SaveSession("/Users/Jamie/.visit/crash_recovery.4536.session")
# MAINTENANCE ISSUE: SetSuppressMessagesRPC is not handled in Logging.C. Please contact a VisIt developer.
# MAINTENANCE ISSUE: SetSuppressMessagesRPC is not handled in Logging.C. Please contact a VisIt developer.
SaveSession("/Users/Jamie/.visit/crash_recovery.4536.session")
# MAINTENANCE ISSUE: SetSuppressMessagesRPC is not handled in Logging.C. Please contact a VisIt developer.
# MAINTENANCE ISSUE: SetSuppressMessagesRPC is not handled in Logging.C. Please contact a VisIt developer.
SaveSession("/Users/Jamie/.visit/crash_recovery.4536.session")
# MAINTENANCE ISSUE: SetSuppressMessagesRPC is not handled in Logging.C. Please contact a VisIt developer.
# MAINTENANCE ISSUE: SetSuppressMessagesRPC is not handled in Logging.C. Please contact a VisIt developer.
SaveSession("/Users/Jamie/.visit/crash_recovery.4536.session")
# MAINTENANCE ISSUE: SetSuppressMessagesRPC is not handled in Logging.C. Please contact a VisIt developer.
# MAINTENANCE ISSUE: SetSuppressMessagesRPC is not handled in Logging.C. Please contact a VisIt developer.
SaveSession("/Users/Jamie/.visit/crash_recovery.4536.session")
# MAINTENANCE ISSUE: SetSuppressMessagesRPC is not handled in Logging.C. Please contact a VisIt developer.
# MAINTENANCE ISSUE: SetSuppressMessagesRPC is not handled in Logging.C. Please contact a VisIt developer.
SaveSession("/Users/Jamie/.visit/crash_recovery.4536.session")
# MAINTENANCE ISSUE: SetSuppressMessagesRPC is not handled in Logging.C. Please contact a VisIt developer.
# MAINTENANCE ISSUE: SetSuppressMessagesRPC is not handled in Logging.C. Please contact a VisIt developer.
SaveSession("/Users/Jamie/.visit/crash_recovery.4536.session")
# MAINTENANCE ISSUE: SetSuppressMessagesRPC is not handled in Logging.C. Please contact a VisIt developer.
# MAINTENANCE ISSUE: SetSuppressMessagesRPC is not handled in Logging.C. Please contact a VisIt developer.
SaveSession("/Users/Jamie/.visit/crash_recovery.4536.session")
# MAINTENANCE ISSUE: SetSuppressMessagesRPC is not handled in Logging.C. Please contact a VisIt developer.
# MAINTENANCE ISSUE: SetSuppressMessagesRPC is not handled in Logging.C. Please contact a VisIt developer.
SaveSession("/Users/Jamie/.visit/crash_recovery.4536.session")
# MAINTENANCE ISSUE: SetSuppressMessagesRPC is not handled in Logging.C. Please contact a VisIt developer.
# MAINTENANCE ISSUE: SetSuppressMessagesRPC is not handled in Logging.C. Please contact a VisIt developer.
SaveSession("/Users/Jamie/.visit/crash_recovery.4536.session")
# MAINTENANCE ISSUE: SetSuppressMessagesRPC is not handled in Logging.C. Please contact a VisIt developer.
# MAINTENANCE ISSUE: SetSuppressMessagesRPC is not handled in Logging.C. Please contact a VisIt developer.
SaveSession("/Users/Jamie/.visit/crash_recovery.4536.session")
# MAINTENANCE ISSUE: SetSuppressMessagesRPC is not handled in Logging.C. Please contact a VisIt developer.
# MAINTENANCE ISSUE: SetSuppressMessagesRPC is not handled in Logging.C. Please contact a VisIt developer.
SaveSession("/Users/Jamie/.visit/crash_recovery.4536.session")
# MAINTENANCE ISSUE: SetSuppressMessagesRPC is not handled in Logging.C. Please contact a VisIt developer.
# MAINTENANCE ISSUE: SetSuppressMessagesRPC is not handled in Logging.C. Please contact a VisIt developer.
SaveSession("/Users/Jamie/.visit/crash_recovery.4536.session")
# MAINTENANCE ISSUE: SetSuppressMessagesRPC is not handled in Logging.C. Please contact a VisIt developer.
# MAINTENANCE ISSUE: SetSuppressMessagesRPC is not handled in Logging.C. Please contact a VisIt developer.
SaveSession("/Users/Jamie/.visit/crash_recovery.4536.session")
# MAINTENANCE ISSUE: SetSuppressMessagesRPC is not handled in Logging.C. Please contact a VisIt developer.
# MAINTENANCE ISSUE: SetSuppressMessagesRPC is not handled in Logging.C. Please contact a VisIt developer.
SaveSession("/Users/Jamie/.visit/crash_recovery.4536.session")
# MAINTENANCE ISSUE: SetSuppressMessagesRPC is not handled in Logging.C. Please contact a VisIt developer.
# MAINTENANCE ISSUE: SetSuppressMessagesRPC is not handled in Logging.C. Please contact a VisIt developer.
SaveSession("/Users/Jamie/.visit/crash_recovery.4536.session")
# MAINTENANCE ISSUE: SetSuppressMessagesRPC is not handled in Logging.C. Please contact a VisIt developer.
# MAINTENANCE ISSUE: SetSuppressMessagesRPC is not handled in Logging.C. Please contact a VisIt developer.
SaveSession("/Users/Jamie/.visit/crash_recovery.4536.session")
# MAINTENANCE ISSUE: SetSuppressMessagesRPC is not handled in Logging.C. Please contact a VisIt developer.
# MAINTENANCE ISSUE: SetSuppressMessagesRPC is not handled in Logging.C. Please contact a VisIt developer.
SaveSession("/Users/Jamie/.visit/crash_recovery.4536.session")
# MAINTENANCE ISSUE: SetSuppressMessagesRPC is not handled in Logging.C. Please contact a VisIt developer.
# MAINTENANCE ISSUE: SetSuppressMessagesRPC is not handled in Logging.C. Please contact a VisIt developer.
SaveSession("/Users/Jamie/.visit/crash_recovery.4536.session")
# MAINTENANCE ISSUE: SetSuppressMessagesRPC is not handled in Logging.C. Please contact a VisIt developer.
# MAINTENANCE ISSUE: SetSuppressMessagesRPC is not handled in Logging.C. Please contact a VisIt developer.
SaveSession("/Users/Jamie/.visit/crash_recovery.4536.session")
# MAINTENANCE ISSUE: SetSuppressMessagesRPC is not handled in Logging.C. Please contact a VisIt developer.
# MAINTENANCE ISSUE: SetSuppressMessagesRPC is not handled in Logging.C. Please contact a VisIt developer.
SaveSession("/Users/Jamie/.visit/crash_recovery.4536.session")
# MAINTENANCE ISSUE: SetSuppressMessagesRPC is not handled in Logging.C. Please contact a VisIt developer.
# MAINTENANCE ISSUE: SetSuppressMessagesRPC is not handled in Logging.C. Please contact a VisIt developer.
SaveSession("/Users/Jamie/.visit/crash_recovery.4536.session")
# MAINTENANCE ISSUE: SetSuppressMessagesRPC is not handled in Logging.C. Please contact a VisIt developer.
# MAINTENANCE ISSUE: SetSuppressMessagesRPC is not handled in Logging.C. Please contact a VisIt developer.
SaveSession("/Users/Jamie/.visit/crash_recovery.4536.session")
# MAINTENANCE ISSUE: SetSuppressMessagesRPC is not handled in Logging.C. Please contact a VisIt developer.
# MAINTENANCE ISSUE: SetSuppressMessagesRPC is not handled in Logging.C. Please contact a VisIt developer.
SaveSession("/Users/Jamie/.visit/crash_recovery.4536.session")
# MAINTENANCE ISSUE: SetSuppressMessagesRPC is not handled in Logging.C. Please contact a VisIt developer.
# MAINTENANCE ISSUE: SetSuppressMessagesRPC is not handled in Logging.C. Please contact a VisIt developer.
SaveSession("/Users/Jamie/.visit/crash_recovery.4536.session")
# MAINTENANCE ISSUE: SetSuppressMessagesRPC is not handled in Logging.C. Please contact a VisIt developer.
# MAINTENANCE ISSUE: SetSuppressMessagesRPC is not handled in Logging.C. Please contact a VisIt developer.
SaveSession("/Users/Jamie/.visit/crash_recovery.4536.session")
# MAINTENANCE ISSUE: SetSuppressMessagesRPC is not handled in Logging.C. Please contact a VisIt developer.
# MAINTENANCE ISSUE: SetSuppressMessagesRPC is not handled in Logging.C. Please contact a VisIt developer.
SaveSession("/Users/Jamie/.visit/crash_recovery.4536.session")
# MAINTENANCE ISSUE: SetSuppressMessagesRPC is not handled in Logging.C. Please contact a VisIt developer.
# MAINTENANCE ISSUE: SetSuppressMessagesRPC is not handled in Logging.C. Please contact a VisIt developer.
SaveSession("/Users/Jamie/.visit/crash_recovery.4536.session")
# MAINTENANCE ISSUE: SetSuppressMessagesRPC is not handled in Logging.C. Please contact a VisIt developer.
# MAINTENANCE ISSUE: SetSuppressMessagesRPC is not handled in Logging.C. Please contact a VisIt developer.
SaveSession("/Users/Jamie/.visit/crash_recovery.4536.session")
# MAINTENANCE ISSUE: SetSuppressMessagesRPC is not handled in Logging.C. Please contact a VisIt developer.
# MAINTENANCE ISSUE: SetSuppressMessagesRPC is not handled in Logging.C. Please contact a VisIt developer.
SaveSession("/Users/Jamie/.visit/crash_recovery.4536.session")
# MAINTENANCE ISSUE: SetSuppressMessagesRPC is not handled in Logging.C. Please contact a VisIt developer.
# MAINTENANCE ISSUE: SetSuppressMessagesRPC is not handled in Logging.C. Please contact a VisIt developer.
SaveSession("/Users/Jamie/.visit/crash_recovery.4536.session")
# MAINTENANCE ISSUE: SetSuppressMessagesRPC is not handled in Logging.C. Please contact a VisIt developer.
# MAINTENANCE ISSUE: SetSuppressMessagesRPC is not handled in Logging.C. Please contact a VisIt developer.
SaveSession("/Users/Jamie/.visit/crash_recovery.4536.session")
# MAINTENANCE ISSUE: SetSuppressMessagesRPC is not handled in Logging.C. Please contact a VisIt developer.
# MAINTENANCE ISSUE: SetSuppressMessagesRPC is not handled in Logging.C. Please contact a VisIt developer.
SaveSession("/Users/Jamie/.visit/crash_recovery.4536.session")
# MAINTENANCE ISSUE: SetSuppressMessagesRPC is not handled in Logging.C. Please contact a VisIt developer.
# MAINTENANCE ISSUE: SetSuppressMessagesRPC is not handled in Logging.C. Please contact a VisIt developer.
SaveSession("/Users/Jamie/.visit/crash_recovery.4536.session")
# MAINTENANCE ISSUE: SetSuppressMessagesRPC is not handled in Logging.C. Please contact a VisIt developer.
# MAINTENANCE ISSUE: SetSuppressMessagesRPC is not handled in Logging.C. Please contact a VisIt developer.
SaveSession("/Users/Jamie/.visit/crash_recovery.4536.session")
# MAINTENANCE ISSUE: SetSuppressMessagesRPC is not handled in Logging.C. Please contact a VisIt developer.
# MAINTENANCE ISSUE: SetSuppressMessagesRPC is not handled in Logging.C. Please contact a VisIt developer.
SaveSession("/Users/Jamie/.visit/crash_recovery.4536.session")
# MAINTENANCE ISSUE: SetSuppressMessagesRPC is not handled in Logging.C. Please contact a VisIt developer.
# MAINTENANCE ISSUE: SetSuppressMessagesRPC is not handled in Logging.C. Please contact a VisIt developer.
SaveSession("/Users/Jamie/.visit/crash_recovery.4536.session")
# MAINTENANCE ISSUE: SetSuppressMessagesRPC is not handled in Logging.C. Please contact a VisIt developer.
# MAINTENANCE ISSUE: SetSuppressMessagesRPC is not handled in Logging.C. Please contact a VisIt developer.
SaveSession("/Users/Jamie/.visit/crash_recovery.4536.session")
# MAINTENANCE ISSUE: SetSuppressMessagesRPC is not handled in Logging.C. Please contact a VisIt developer.
# MAINTENANCE ISSUE: SetSuppressMessagesRPC is not handled in Logging.C. Please contact a VisIt developer.
SaveSession("/Users/Jamie/.visit/crash_recovery.4536.session")
# MAINTENANCE ISSUE: SetSuppressMessagesRPC is not handled in Logging.C. Please contact a VisIt developer.
# MAINTENANCE ISSUE: SetSuppressMessagesRPC is not handled in Logging.C. Please contact a VisIt developer.
SaveSession("/Users/Jamie/.visit/crash_recovery.4536.session")
# MAINTENANCE ISSUE: SetSuppressMessagesRPC is not handled in Logging.C. Please contact a VisIt developer.
# MAINTENANCE ISSUE: SetSuppressMessagesRPC is not handled in Logging.C. Please contact a VisIt developer.
SaveSession("/Users/Jamie/.visit/crash_recovery.4536.session")
# MAINTENANCE ISSUE: SetSuppressMessagesRPC is not handled in Logging.C. Please contact a VisIt developer.
# MAINTENANCE ISSUE: SetSuppressMessagesRPC is not handled in Logging.C. Please contact a VisIt developer.
SaveSession("/Users/Jamie/.visit/crash_recovery.4536.session")
# MAINTENANCE ISSUE: SetSuppressMessagesRPC is not handled in Logging.C. Please contact a VisIt developer.
# MAINTENANCE ISSUE: SetSuppressMessagesRPC is not handled in Logging.C. Please contact a VisIt developer.
SaveSession("/Users/Jamie/.visit/crash_recovery.4536.session")
# MAINTENANCE ISSUE: SetSuppressMessagesRPC is not handled in Logging.C. Please contact a VisIt developer.
# MAINTENANCE ISSUE: SetSuppressMessagesRPC is not handled in Logging.C. Please contact a VisIt developer.
SaveSession("/Users/Jamie/.visit/crash_recovery.4536.session")
# MAINTENANCE ISSUE: SetSuppressMessagesRPC is not handled in Logging.C. Please contact a VisIt developer.
# MAINTENANCE ISSUE: SetSuppressMessagesRPC is not handled in Logging.C. Please contact a VisIt developer.
SaveSession("/Users/Jamie/.visit/crash_recovery.4536.session")
# MAINTENANCE ISSUE: SetSuppressMessagesRPC is not handled in Logging.C. Please contact a VisIt developer.
# MAINTENANCE ISSUE: SetSuppressMessagesRPC is not handled in Logging.C. Please contact a VisIt developer.
SaveSession("/Users/Jamie/.visit/crash_recovery.4536.session")
# MAINTENANCE ISSUE: SetSuppressMessagesRPC is not handled in Logging.C. Please contact a VisIt developer.
# MAINTENANCE ISSUE: SetSuppressMessagesRPC is not handled in Logging.C. Please contact a VisIt developer.
SaveSession("/Users/Jamie/.visit/crash_recovery.4536.session")
# MAINTENANCE ISSUE: SetSuppressMessagesRPC is not handled in Logging.C. Please contact a VisIt developer.
# MAINTENANCE ISSUE: SetSuppressMessagesRPC is not handled in Logging.C. Please contact a VisIt developer.
SaveSession("/Users/Jamie/.visit/crash_recovery.4536.session")
# MAINTENANCE ISSUE: SetSuppressMessagesRPC is not handled in Logging.C. Please contact a VisIt developer.
# MAINTENANCE ISSUE: SetSuppressMessagesRPC is not handled in Logging.C. Please contact a VisIt developer.
SaveSession("/Users/Jamie/.visit/crash_recovery.4536.session")
# MAINTENANCE ISSUE: SetSuppressMessagesRPC is not handled in Logging.C. Please contact a VisIt developer.
# MAINTENANCE ISSUE: SetSuppressMessagesRPC is not handled in Logging.C. Please contact a VisIt developer.
SaveSession("/Users/Jamie/.visit/crash_recovery.4536.session")
# MAINTENANCE ISSUE: SetSuppressMessagesRPC is not handled in Logging.C. Please contact a VisIt developer.
# MAINTENANCE ISSUE: SetSuppressMessagesRPC is not handled in Logging.C. Please contact a VisIt developer.
SaveSession("/Users/Jamie/.visit/crash_recovery.4536.session")
# MAINTENANCE ISSUE: SetSuppressMessagesRPC is not handled in Logging.C. Please contact a VisIt developer.
# MAINTENANCE ISSUE: SetSuppressMessagesRPC is not handled in Logging.C. Please contact a VisIt developer.
SaveSession("/Users/Jamie/.visit/crash_recovery.4536.session")
# MAINTENANCE ISSUE: SetSuppressMessagesRPC is not handled in Logging.C. Please contact a VisIt developer.
# MAINTENANCE ISSUE: SetSuppressMessagesRPC is not handled in Logging.C. Please contact a VisIt developer.
SaveSession("/Users/Jamie/.visit/crash_recovery.4536.session")
# MAINTENANCE ISSUE: SetSuppressMessagesRPC is not handled in Logging.C. Please contact a VisIt developer.
# MAINTENANCE ISSUE: SetSuppressMessagesRPC is not handled in Logging.C. Please contact a VisIt developer.
SaveSession("/Users/Jamie/.visit/crash_recovery.4536.session")
# MAINTENANCE ISSUE: SetSuppressMessagesRPC is not handled in Logging.C. Please contact a VisIt developer.
# MAINTENANCE ISSUE: SetSuppressMessagesRPC is not handled in Logging.C. Please contact a VisIt developer.
SaveSession("/Users/Jamie/.visit/crash_recovery.4536.session")
# MAINTENANCE ISSUE: SetSuppressMessagesRPC is not handled in Logging.C. Please contact a VisIt developer.
# MAINTENANCE ISSUE: SetSuppressMessagesRPC is not handled in Logging.C. Please contact a VisIt developer.
SaveSession("/Users/Jamie/.visit/crash_recovery.4536.session")
# MAINTENANCE ISSUE: SetSuppressMessagesRPC is not handled in Logging.C. Please contact a VisIt developer.
# MAINTENANCE ISSUE: SetSuppressMessagesRPC is not handled in Logging.C. Please contact a VisIt developer.
SaveSession("/Users/Jamie/.visit/crash_recovery.4536.session")
# MAINTENANCE ISSUE: SetSuppressMessagesRPC is not handled in Logging.C. Please contact a VisIt developer.
# MAINTENANCE ISSUE: SetSuppressMessagesRPC is not handled in Logging.C. Please contact a VisIt developer.
SaveSession("/Users/Jamie/.visit/crash_recovery.4536.session")
# MAINTENANCE ISSUE: SetSuppressMessagesRPC is not handled in Logging.C. Please contact a VisIt developer.
# MAINTENANCE ISSUE: SetSuppressMessagesRPC is not handled in Logging.C. Please contact a VisIt developer.
SaveSession("/Users/Jamie/.visit/crash_recovery.4536.session")
# MAINTENANCE ISSUE: SetSuppressMessagesRPC is not handled in Logging.C. Please contact a VisIt developer.
# MAINTENANCE ISSUE: SetSuppressMessagesRPC is not handled in Logging.C. Please contact a VisIt developer.
SaveSession("/Users/Jamie/.visit/crash_recovery.4536.session")
# MAINTENANCE ISSUE: SetSuppressMessagesRPC is not handled in Logging.C. Please contact a VisIt developer.
# MAINTENANCE ISSUE: SetSuppressMessagesRPC is not handled in Logging.C. Please contact a VisIt developer.
SaveSession("/Users/Jamie/.visit/crash_recovery.4536.session")
# MAINTENANCE ISSUE: SetSuppressMessagesRPC is not handled in Logging.C. Please contact a VisIt developer.
# MAINTENANCE ISSUE: SetSuppressMessagesRPC is not handled in Logging.C. Please contact a VisIt developer.
SaveSession("/Users/Jamie/.visit/crash_recovery.4536.session")
# MAINTENANCE ISSUE: SetSuppressMessagesRPC is not handled in Logging.C. Please contact a VisIt developer.
# MAINTENANCE ISSUE: SetSuppressMessagesRPC is not handled in Logging.C. Please contact a VisIt developer.
SaveSession("/Users/Jamie/.visit/crash_recovery.4536.session")
# MAINTENANCE ISSUE: SetSuppressMessagesRPC is not handled in Logging.C. Please contact a VisIt developer.
# MAINTENANCE ISSUE: SetSuppressMessagesRPC is not handled in Logging.C. Please contact a VisIt developer.
SaveSession("/Users/Jamie/.visit/crash_recovery.4536.session")
# MAINTENANCE ISSUE: SetSuppressMessagesRPC is not handled in Logging.C. Please contact a VisIt developer.
# MAINTENANCE ISSUE: SetSuppressMessagesRPC is not handled in Logging.C. Please contact a VisIt developer.
SaveSession("/Users/Jamie/.visit/crash_recovery.4536.session")
# MAINTENANCE ISSUE: SetSuppressMessagesRPC is not handled in Logging.C. Please contact a VisIt developer.
# MAINTENANCE ISSUE: SetSuppressMessagesRPC is not handled in Logging.C. Please contact a VisIt developer.
SaveSession("/Users/Jamie/.visit/crash_recovery.4536.session")
# MAINTENANCE ISSUE: SetSuppressMessagesRPC is not handled in Logging.C. Please contact a VisIt developer.
# MAINTENANCE ISSUE: SetSuppressMessagesRPC is not handled in Logging.C. Please contact a VisIt developer.
SaveSession("/Users/Jamie/.visit/crash_recovery.4536.session")
# MAINTENANCE ISSUE: SetSuppressMessagesRPC is not handled in Logging.C. Please contact a VisIt developer.
# MAINTENANCE ISSUE: SetSuppressMessagesRPC is not handled in Logging.C. Please contact a VisIt developer.
SaveSession("/Users/Jamie/.visit/crash_recovery.4536.session")
# MAINTENANCE ISSUE: SetSuppressMessagesRPC is not handled in Logging.C. Please contact a VisIt developer.
# MAINTENANCE ISSUE: SetSuppressMessagesRPC is not handled in Logging.C. Please contact a VisIt developer.
SaveSession("/Users/Jamie/.visit/crash_recovery.4536.session")
# MAINTENANCE ISSUE: SetSuppressMessagesRPC is not handled in Logging.C. Please contact a VisIt developer.
# MAINTENANCE ISSUE: SetSuppressMessagesRPC is not handled in Logging.C. Please contact a VisIt developer.
SaveSession("/Users/Jamie/.visit/crash_recovery.4536.session")
# MAINTENANCE ISSUE: SetSuppressMessagesRPC is not handled in Logging.C. Please contact a VisIt developer.
# MAINTENANCE ISSUE: SetSuppressMessagesRPC is not handled in Logging.C. Please contact a VisIt developer.
SaveSession("/Users/Jamie/.visit/crash_recovery.4536.session")
# MAINTENANCE ISSUE: SetSuppressMessagesRPC is not handled in Logging.C. Please contact a VisIt developer.
# MAINTENANCE ISSUE: SetSuppressMessagesRPC is not handled in Logging.C. Please contact a VisIt developer.
SaveSession("/Users/Jamie/.visit/crash_recovery.4536.session")
# MAINTENANCE ISSUE: SetSuppressMessagesRPC is not handled in Logging.C. Please contact a VisIt developer.
# MAINTENANCE ISSUE: SetSuppressMessagesRPC is not handled in Logging.C. Please contact a VisIt developer.
SaveSession("/Users/Jamie/.visit/crash_recovery.4536.session")
# MAINTENANCE ISSUE: SetSuppressMessagesRPC is not handled in Logging.C. Please contact a VisIt developer.
# MAINTENANCE ISSUE: SetSuppressMessagesRPC is not handled in Logging.C. Please contact a VisIt developer.
SaveSession("/Users/Jamie/.visit/crash_recovery.4536.session")
# MAINTENANCE ISSUE: SetSuppressMessagesRPC is not handled in Logging.C. Please contact a VisIt developer.
# MAINTENANCE ISSUE: SetSuppressMessagesRPC is not handled in Logging.C. Please contact a VisIt developer.
SaveSession("/Users/Jamie/.visit/crash_recovery.4536.session")
# MAINTENANCE ISSUE: SetSuppressMessagesRPC is not handled in Logging.C. Please contact a VisIt developer.
# MAINTENANCE ISSUE: SetSuppressMessagesRPC is not handled in Logging.C. Please contact a VisIt developer.
SaveSession("/Users/Jamie/.visit/crash_recovery.4536.session")
# MAINTENANCE ISSUE: SetSuppressMessagesRPC is not handled in Logging.C. Please contact a VisIt developer.
# MAINTENANCE ISSUE: SetSuppressMessagesRPC is not handled in Logging.C. Please contact a VisIt developer.
SaveSession("/Users/Jamie/.visit/crash_recovery.4536.session")
# MAINTENANCE ISSUE: SetSuppressMessagesRPC is not handled in Logging.C. Please contact a VisIt developer.
# MAINTENANCE ISSUE: SetSuppressMessagesRPC is not handled in Logging.C. Please contact a VisIt developer.
SaveSession("/Users/Jamie/.visit/crash_recovery.4536.session")
# MAINTENANCE ISSUE: SetSuppressMessagesRPC is not handled in Logging.C. Please contact a VisIt developer.
# MAINTENANCE ISSUE: SetSuppressMessagesRPC is not handled in Logging.C. Please contact a VisIt developer.
SaveSession("/Users/Jamie/.visit/crash_recovery.4536.session")
# MAINTENANCE ISSUE: SetSuppressMessagesRPC is not handled in Logging.C. Please contact a VisIt developer.
# MAINTENANCE ISSUE: SetSuppressMessagesRPC is not handled in Logging.C. Please contact a VisIt developer.
SaveSession("/Users/Jamie/.visit/crash_recovery.4536.session")
# MAINTENANCE ISSUE: SetSuppressMessagesRPC is not handled in Logging.C. Please contact a VisIt developer.
# MAINTENANCE ISSUE: SetSuppressMessagesRPC is not handled in Logging.C. Please contact a VisIt developer.
SaveSession("/Users/Jamie/.visit/crash_recovery.4536.session")
# MAINTENANCE ISSUE: SetSuppressMessagesRPC is not handled in Logging.C. Please contact a VisIt developer.
# MAINTENANCE ISSUE: SetSuppressMessagesRPC is not handled in Logging.C. Please contact a VisIt developer.
SaveSession("/Users/Jamie/.visit/crash_recovery.4536.session")
# MAINTENANCE ISSUE: SetSuppressMessagesRPC is not handled in Logging.C. Please contact a VisIt developer.
# MAINTENANCE ISSUE: SetSuppressMessagesRPC is not handled in Logging.C. Please contact a VisIt developer.
SaveSession("/Users/Jamie/.visit/crash_recovery.4536.session")
# MAINTENANCE ISSUE: SetSuppressMessagesRPC is not handled in Logging.C. Please contact a VisIt developer.
# MAINTENANCE ISSUE: SetSuppressMessagesRPC is not handled in Logging.C. Please contact a VisIt developer.
SaveSession("/Users/Jamie/.visit/crash_recovery.4536.session")
# MAINTENANCE ISSUE: SetSuppressMessagesRPC is not handled in Logging.C. Please contact a VisIt developer.
# MAINTENANCE ISSUE: SetSuppressMessagesRPC is not handled in Logging.C. Please contact a VisIt developer.
SaveSession("/Users/Jamie/.visit/crash_recovery.4536.session")
# MAINTENANCE ISSUE: SetSuppressMessagesRPC is not handled in Logging.C. Please contact a VisIt developer.
# MAINTENANCE ISSUE: SetSuppressMessagesRPC is not handled in Logging.C. Please contact a VisIt developer.
SaveSession("/Users/Jamie/.visit/crash_recovery.4536.session")
# MAINTENANCE ISSUE: SetSuppressMessagesRPC is not handled in Logging.C. Please contact a VisIt developer.
# MAINTENANCE ISSUE: SetSuppressMessagesRPC is not handled in Logging.C. Please contact a VisIt developer.
SaveSession("/Users/Jamie/.visit/crash_recovery.4536.session")
# MAINTENANCE ISSUE: SetSuppressMessagesRPC is not handled in Logging.C. Please contact a VisIt developer.
# MAINTENANCE ISSUE: SetSuppressMessagesRPC is not handled in Logging.C. Please contact a VisIt developer.
SaveSession("/Users/Jamie/.visit/crash_recovery.4536.session")
# MAINTENANCE ISSUE: SetSuppressMessagesRPC is not handled in Logging.C. Please contact a VisIt developer.
# MAINTENANCE ISSUE: SetSuppressMessagesRPC is not handled in Logging.C. Please contact a VisIt developer.
SaveSession("/Users/Jamie/.visit/crash_recovery.4536.session")
# MAINTENANCE ISSUE: SetSuppressMessagesRPC is not handled in Logging.C. Please contact a VisIt developer.
# MAINTENANCE ISSUE: SetSuppressMessagesRPC is not handled in Logging.C. Please contact a VisIt developer.
SaveSession("/Users/Jamie/.visit/crash_recovery.4536.session")
# MAINTENANCE ISSUE: SetSuppressMessagesRPC is not handled in Logging.C. Please contact a VisIt developer.
# MAINTENANCE ISSUE: SetSuppressMessagesRPC is not handled in Logging.C. Please contact a VisIt developer.
SaveSession("/Users/Jamie/.visit/crash_recovery.4536.session")
# MAINTENANCE ISSUE: SetSuppressMessagesRPC is not handled in Logging.C. Please contact a VisIt developer.
# MAINTENANCE ISSUE: SetSuppressMessagesRPC is not handled in Logging.C. Please contact a VisIt developer.
SaveSession("/Users/Jamie/.visit/crash_recovery.4536.session")
# MAINTENANCE ISSUE: SetSuppressMessagesRPC is not handled in Logging.C. Please contact a VisIt developer.
# MAINTENANCE ISSUE: SetSuppressMessagesRPC is not handled in Logging.C. Please contact a VisIt developer.
SaveSession("/Users/Jamie/.visit/crash_recovery.4536.session")
# MAINTENANCE ISSUE: SetSuppressMessagesRPC is not handled in Logging.C. Please contact a VisIt developer.
# MAINTENANCE ISSUE: SetSuppressMessagesRPC is not handled in Logging.C. Please contact a VisIt developer.
SaveSession("/Users/Jamie/.visit/crash_recovery.4536.session")
# MAINTENANCE ISSUE: SetSuppressMessagesRPC is not handled in Logging.C. Please contact a VisIt developer.
# MAINTENANCE ISSUE: SetSuppressMessagesRPC is not handled in Logging.C. Please contact a VisIt developer.
SaveSession("/Users/Jamie/.visit/crash_recovery.4536.session")
# MAINTENANCE ISSUE: SetSuppressMessagesRPC is not handled in Logging.C. Please contact a VisIt developer.
# MAINTENANCE ISSUE: SetSuppressMessagesRPC is not handled in Logging.C. Please contact a VisIt developer.
SaveSession("/Users/Jamie/.visit/crash_recovery.4536.session")
# MAINTENANCE ISSUE: SetSuppressMessagesRPC is not handled in Logging.C. Please contact a VisIt developer.
# MAINTENANCE ISSUE: SetSuppressMessagesRPC is not handled in Logging.C. Please contact a VisIt developer.
SaveSession("/Users/Jamie/.visit/crash_recovery.4536.session")
# MAINTENANCE ISSUE: SetSuppressMessagesRPC is not handled in Logging.C. Please contact a VisIt developer.
# MAINTENANCE ISSUE: SetSuppressMessagesRPC is not handled in Logging.C. Please contact a VisIt developer.
SaveSession("/Users/Jamie/.visit/crash_recovery.4536.session")
# MAINTENANCE ISSUE: SetSuppressMessagesRPC is not handled in Logging.C. Please contact a VisIt developer.
# MAINTENANCE ISSUE: SetSuppressMessagesRPC is not handled in Logging.C. Please contact a VisIt developer.
SaveSession("/Users/Jamie/.visit/crash_recovery.4536.session")
# MAINTENANCE ISSUE: SetSuppressMessagesRPC is not handled in Logging.C. Please contact a VisIt developer.
# MAINTENANCE ISSUE: SetSuppressMessagesRPC is not handled in Logging.C. Please contact a VisIt developer.
SaveSession("/Users/Jamie/.visit/crash_recovery.4536.session")
# MAINTENANCE ISSUE: SetSuppressMessagesRPC is not handled in Logging.C. Please contact a VisIt developer.
# MAINTENANCE ISSUE: SetSuppressMessagesRPC is not handled in Logging.C. Please contact a VisIt developer.
SaveSession("/Users/Jamie/.visit/crash_recovery.4536.session")
# MAINTENANCE ISSUE: SetSuppressMessagesRPC is not handled in Logging.C. Please contact a VisIt developer.
# MAINTENANCE ISSUE: SetSuppressMessagesRPC is not handled in Logging.C. Please contact a VisIt developer.
SaveSession("/Users/Jamie/.visit/crash_recovery.4536.session")
# MAINTENANCE ISSUE: SetSuppressMessagesRPC is not handled in Logging.C. Please contact a VisIt developer.
# MAINTENANCE ISSUE: SetSuppressMessagesRPC is not handled in Logging.C. Please contact a VisIt developer.
SaveSession("/Users/Jamie/.visit/crash_recovery.4536.session")
# MAINTENANCE ISSUE: SetSuppressMessagesRPC is not handled in Logging.C. Please contact a VisIt developer.
# MAINTENANCE ISSUE: SetSuppressMessagesRPC is not handled in Logging.C. Please contact a VisIt developer.
SaveSession("/Users/Jamie/.visit/crash_recovery.4536.session")
# MAINTENANCE ISSUE: SetSuppressMessagesRPC is not handled in Logging.C. Please contact a VisIt developer.
# MAINTENANCE ISSUE: SetSuppressMessagesRPC is not handled in Logging.C. Please contact a VisIt developer.
SaveSession("/Users/Jamie/.visit/crash_recovery.4536.session")
# MAINTENANCE ISSUE: SetSuppressMessagesRPC is not handled in Logging.C. Please contact a VisIt developer.
# MAINTENANCE ISSUE: SetSuppressMessagesRPC is not handled in Logging.C. Please contact a VisIt developer.
SaveSession("/Users/Jamie/.visit/crash_recovery.4536.session")
# MAINTENANCE ISSUE: SetSuppressMessagesRPC is not handled in Logging.C. Please contact a VisIt developer.
# MAINTENANCE ISSUE: SetSuppressMessagesRPC is not handled in Logging.C. Please contact a VisIt developer.
SaveSession("/Users/Jamie/.visit/crash_recovery.4536.session")
# MAINTENANCE ISSUE: SetSuppressMessagesRPC is not handled in Logging.C. Please contact a VisIt developer.
# MAINTENANCE ISSUE: SetSuppressMessagesRPC is not handled in Logging.C. Please contact a VisIt developer.
SaveSession("/Users/Jamie/.visit/crash_recovery.4536.session")
# MAINTENANCE ISSUE: SetSuppressMessagesRPC is not handled in Logging.C. Please contact a VisIt developer.
# MAINTENANCE ISSUE: SetSuppressMessagesRPC is not handled in Logging.C. Please contact a VisIt developer.
SaveSession("/Users/Jamie/.visit/crash_recovery.4536.session")
# MAINTENANCE ISSUE: SetSuppressMessagesRPC is not handled in Logging.C. Please contact a VisIt developer.
# MAINTENANCE ISSUE: SetSuppressMessagesRPC is not handled in Logging.C. Please contact a VisIt developer.
SaveSession("/Users/Jamie/.visit/crash_recovery.4536.session")
# MAINTENANCE ISSUE: SetSuppressMessagesRPC is not handled in Logging.C. Please contact a VisIt developer.
# MAINTENANCE ISSUE: SetSuppressMessagesRPC is not handled in Logging.C. Please contact a VisIt developer.
SaveSession("/Users/Jamie/.visit/crash_recovery.4536.session")
# MAINTENANCE ISSUE: SetSuppressMessagesRPC is not handled in Logging.C. Please contact a VisIt developer.
# MAINTENANCE ISSUE: SetSuppressMessagesRPC is not handled in Logging.C. Please contact a VisIt developer.
SaveSession("/Users/Jamie/.visit/crash_recovery.4536.session")
# MAINTENANCE ISSUE: SetSuppressMessagesRPC is not handled in Logging.C. Please contact a VisIt developer.
# MAINTENANCE ISSUE: SetSuppressMessagesRPC is not handled in Logging.C. Please contact a VisIt developer.
SaveSession("/Users/Jamie/.visit/crash_recovery.4536.session")
# MAINTENANCE ISSUE: SetSuppressMessagesRPC is not handled in Logging.C. Please contact a VisIt developer.
# MAINTENANCE ISSUE: SetSuppressMessagesRPC is not handled in Logging.C. Please contact a VisIt developer.
SaveSession("/Users/Jamie/.visit/crash_recovery.4536.session")
# MAINTENANCE ISSUE: SetSuppressMessagesRPC is not handled in Logging.C. Please contact a VisIt developer.
# MAINTENANCE ISSUE: SetSuppressMessagesRPC is not handled in Logging.C. Please contact a VisIt developer.
SaveSession("/Users/Jamie/.visit/crash_recovery.4536.session")
# MAINTENANCE ISSUE: SetSuppressMessagesRPC is not handled in Logging.C. Please contact a VisIt developer.
# MAINTENANCE ISSUE: SetSuppressMessagesRPC is not handled in Logging.C. Please contact a VisIt developer.
SaveSession("/Users/Jamie/.visit/crash_recovery.4536.session")
# MAINTENANCE ISSUE: SetSuppressMessagesRPC is not handled in Logging.C. Please contact a VisIt developer.
# MAINTENANCE ISSUE: SetSuppressMessagesRPC is not handled in Logging.C. Please contact a VisIt developer.
SaveSession("/Users/Jamie/.visit/crash_recovery.4536.session")
# MAINTENANCE ISSUE: SetSuppressMessagesRPC is not handled in Logging.C. Please contact a VisIt developer.
# MAINTENANCE ISSUE: SetSuppressMessagesRPC is not handled in Logging.C. Please contact a VisIt developer.
SaveSession("/Users/Jamie/.visit/crash_recovery.4536.session")
# MAINTENANCE ISSUE: SetSuppressMessagesRPC is not handled in Logging.C. Please contact a VisIt developer.
# MAINTENANCE ISSUE: SetSuppressMessagesRPC is not handled in Logging.C. Please contact a VisIt developer.
SaveSession("/Users/Jamie/.visit/crash_recovery.4536.session")
# MAINTENANCE ISSUE: SetSuppressMessagesRPC is not handled in Logging.C. Please contact a VisIt developer.
# MAINTENANCE ISSUE: SetSuppressMessagesRPC is not handled in Logging.C. Please contact a VisIt developer.
SaveSession("/Users/Jamie/.visit/crash_recovery.4536.session")
# MAINTENANCE ISSUE: SetSuppressMessagesRPC is not handled in Logging.C. Please contact a VisIt developer.
# MAINTENANCE ISSUE: SetSuppressMessagesRPC is not handled in Logging.C. Please contact a VisIt developer.
SaveSession("/Users/Jamie/.visit/crash_recovery.4536.session")
# MAINTENANCE ISSUE: SetSuppressMessagesRPC is not handled in Logging.C. Please contact a VisIt developer.
# MAINTENANCE ISSUE: SetSuppressMessagesRPC is not handled in Logging.C. Please contact a VisIt developer.
SaveSession("/Users/Jamie/.visit/crash_recovery.4536.session")
# MAINTENANCE ISSUE: SetSuppressMessagesRPC is not handled in Logging.C. Please contact a VisIt developer.
# MAINTENANCE ISSUE: SetSuppressMessagesRPC is not handled in Logging.C. Please contact a VisIt developer.
SaveSession("/Users/Jamie/.visit/crash_recovery.4536.session")
# MAINTENANCE ISSUE: SetSuppressMessagesRPC is not handled in Logging.C. Please contact a VisIt developer.
# MAINTENANCE ISSUE: SetSuppressMessagesRPC is not handled in Logging.C. Please contact a VisIt developer.
SaveSession("/Users/Jamie/.visit/crash_recovery.4536.session")
# MAINTENANCE ISSUE: SetSuppressMessagesRPC is not handled in Logging.C. Please contact a VisIt developer.
# MAINTENANCE ISSUE: SetSuppressMessagesRPC is not handled in Logging.C. Please contact a VisIt developer.
SaveSession("/Users/Jamie/.visit/crash_recovery.4536.session")
# MAINTENANCE ISSUE: SetSuppressMessagesRPC is not handled in Logging.C. Please contact a VisIt developer.
# MAINTENANCE ISSUE: SetSuppressMessagesRPC is not handled in Logging.C. Please contact a VisIt developer.
SaveSession("/Users/Jamie/.visit/crash_recovery.4536.session")
# MAINTENANCE ISSUE: SetSuppressMessagesRPC is not handled in Logging.C. Please contact a VisIt developer.
# MAINTENANCE ISSUE: SetSuppressMessagesRPC is not handled in Logging.C. Please contact a VisIt developer.
SaveSession("/Users/Jamie/.visit/crash_recovery.4536.session")
# MAINTENANCE ISSUE: SetSuppressMessagesRPC is not handled in Logging.C. Please contact a VisIt developer.
# MAINTENANCE ISSUE: SetSuppressMessagesRPC is not handled in Logging.C. Please contact a VisIt developer.
SaveSession("/Users/Jamie/.visit/crash_recovery.4536.session")
# MAINTENANCE ISSUE: SetSuppressMessagesRPC is not handled in Logging.C. Please contact a VisIt developer.
# MAINTENANCE ISSUE: SetSuppressMessagesRPC is not handled in Logging.C. Please contact a VisIt developer.
SaveSession("/Users/Jamie/.visit/crash_recovery.4536.session")
# MAINTENANCE ISSUE: SetSuppressMessagesRPC is not handled in Logging.C. Please contact a VisIt developer.
# MAINTENANCE ISSUE: SetSuppressMessagesRPC is not handled in Logging.C. Please contact a VisIt developer.
SaveSession("/Users/Jamie/.visit/crash_recovery.4536.session")
# MAINTENANCE ISSUE: SetSuppressMessagesRPC is not handled in Logging.C. Please contact a VisIt developer.
# MAINTENANCE ISSUE: SetSuppressMessagesRPC is not handled in Logging.C. Please contact a VisIt developer.
SaveSession("/Users/Jamie/.visit/crash_recovery.4536.session")
# MAINTENANCE ISSUE: SetSuppressMessagesRPC is not handled in Logging.C. Please contact a VisIt developer.
# MAINTENANCE ISSUE: SetSuppressMessagesRPC is not handled in Logging.C. Please contact a VisIt developer.
SaveSession("/Users/Jamie/.visit/crash_recovery.4536.session")
# MAINTENANCE ISSUE: SetSuppressMessagesRPC is not handled in Logging.C. Please contact a VisIt developer.
# MAINTENANCE ISSUE: SetSuppressMessagesRPC is not handled in Logging.C. Please contact a VisIt developer.
SaveSession("/Users/Jamie/.visit/crash_recovery.4536.session")
# MAINTENANCE ISSUE: SetSuppressMessagesRPC is not handled in Logging.C. Please contact a VisIt developer.
# MAINTENANCE ISSUE: SetSuppressMessagesRPC is not handled in Logging.C. Please contact a VisIt developer.
SaveSession("/Users/Jamie/.visit/crash_recovery.4536.session")
# MAINTENANCE ISSUE: SetSuppressMessagesRPC is not handled in Logging.C. Please contact a VisIt developer.
# MAINTENANCE ISSUE: SetSuppressMessagesRPC is not handled in Logging.C. Please contact a VisIt developer.
SaveSession("/Users/Jamie/.visit/crash_recovery.4536.session")
# MAINTENANCE ISSUE: SetSuppressMessagesRPC is not handled in Logging.C. Please contact a VisIt developer.
# MAINTENANCE ISSUE: SetSuppressMessagesRPC is not handled in Logging.C. Please contact a VisIt developer.
SaveSession("/Users/Jamie/.visit/crash_recovery.4536.session")
# MAINTENANCE ISSUE: SetSuppressMessagesRPC is not handled in Logging.C. Please contact a VisIt developer.
# MAINTENANCE ISSUE: SetSuppressMessagesRPC is not handled in Logging.C. Please contact a VisIt developer.
SaveSession("/Users/Jamie/.visit/crash_recovery.4536.session")
# MAINTENANCE ISSUE: SetSuppressMessagesRPC is not handled in Logging.C. Please contact a VisIt developer.
# MAINTENANCE ISSUE: SetSuppressMessagesRPC is not handled in Logging.C. Please contact a VisIt developer.
SaveSession("/Users/Jamie/.visit/crash_recovery.4536.session")
# MAINTENANCE ISSUE: SetSuppressMessagesRPC is not handled in Logging.C. Please contact a VisIt developer.
# MAINTENANCE ISSUE: SetSuppressMessagesRPC is not handled in Logging.C. Please contact a VisIt developer.
SaveSession("/Users/Jamie/.visit/crash_recovery.4536.session")
# MAINTENANCE ISSUE: SetSuppressMessagesRPC is not handled in Logging.C. Please contact a VisIt developer.
# MAINTENANCE ISSUE: SetSuppressMessagesRPC is not handled in Logging.C. Please contact a VisIt developer.
SaveSession("/Users/Jamie/.visit/crash_recovery.4536.session")
# MAINTENANCE ISSUE: SetSuppressMessagesRPC is not handled in Logging.C. Please contact a VisIt developer.
# MAINTENANCE ISSUE: SetSuppressMessagesRPC is not handled in Logging.C. Please contact a VisIt developer.
SaveSession("/Users/Jamie/.visit/crash_recovery.4536.session")
# MAINTENANCE ISSUE: SetSuppressMessagesRPC is not handled in Logging.C. Please contact a VisIt developer.
# MAINTENANCE ISSUE: SetSuppressMessagesRPC is not handled in Logging.C. Please contact a VisIt developer.
SaveSession("/Users/Jamie/.visit/crash_recovery.4536.session")
# MAINTENANCE ISSUE: SetSuppressMessagesRPC is not handled in Logging.C. Please contact a VisIt developer.
# MAINTENANCE ISSUE: SetSuppressMessagesRPC is not handled in Logging.C. Please contact a VisIt developer.
SaveSession("/Users/Jamie/.visit/crash_recovery.4536.session")
# MAINTENANCE ISSUE: SetSuppressMessagesRPC is not handled in Logging.C. Please contact a VisIt developer.
# MAINTENANCE ISSUE: SetSuppressMessagesRPC is not handled in Logging.C. Please contact a VisIt developer.
SaveSession("/Users/Jamie/.visit/crash_recovery.4536.session")
# MAINTENANCE ISSUE: SetSuppressMessagesRPC is not handled in Logging.C. Please contact a VisIt developer.
# MAINTENANCE ISSUE: SetSuppressMessagesRPC is not handled in Logging.C. Please contact a VisIt developer.
SaveSession("/Users/Jamie/.visit/crash_recovery.4536.session")
# MAINTENANCE ISSUE: SetSuppressMessagesRPC is not handled in Logging.C. Please contact a VisIt developer.
# MAINTENANCE ISSUE: SetSuppressMessagesRPC is not handled in Logging.C. Please contact a VisIt developer.
SaveSession("/Users/Jamie/.visit/crash_recovery.4536.session")
# MAINTENANCE ISSUE: SetSuppressMessagesRPC is not handled in Logging.C. Please contact a VisIt developer.
# MAINTENANCE ISSUE: SetSuppressMessagesRPC is not handled in Logging.C. Please contact a VisIt developer.
SaveSession("/Users/Jamie/.visit/crash_recovery.4536.session")
# MAINTENANCE ISSUE: SetSuppressMessagesRPC is not handled in Logging.C. Please contact a VisIt developer.
# MAINTENANCE ISSUE: SetSuppressMessagesRPC is not handled in Logging.C. Please contact a VisIt developer.
SaveSession("/Users/Jamie/.visit/crash_recovery.4536.session")
# MAINTENANCE ISSUE: SetSuppressMessagesRPC is not handled in Logging.C. Please contact a VisIt developer.
# MAINTENANCE ISSUE: SetSuppressMessagesRPC is not handled in Logging.C. Please contact a VisIt developer.
SaveSession("/Users/Jamie/.visit/crash_recovery.4536.session")
# MAINTENANCE ISSUE: SetSuppressMessagesRPC is not handled in Logging.C. Please contact a VisIt developer.
# MAINTENANCE ISSUE: SetSuppressMessagesRPC is not handled in Logging.C. Please contact a VisIt developer.
SaveSession("/Users/Jamie/.visit/crash_recovery.4536.session")
# MAINTENANCE ISSUE: SetSuppressMessagesRPC is not handled in Logging.C. Please contact a VisIt developer.
# MAINTENANCE ISSUE: SetSuppressMessagesRPC is not handled in Logging.C. Please contact a VisIt developer.
SaveSession("/Users/Jamie/.visit/crash_recovery.4536.session")
# MAINTENANCE ISSUE: SetSuppressMessagesRPC is not handled in Logging.C. Please contact a VisIt developer.
# MAINTENANCE ISSUE: SetSuppressMessagesRPC is not handled in Logging.C. Please contact a VisIt developer.
SaveSession("/Users/Jamie/.visit/crash_recovery.4536.session")
# MAINTENANCE ISSUE: SetSuppressMessagesRPC is not handled in Logging.C. Please contact