import os.path
import re
import time

# Global state variable
automaticMappingEnabled = False
activePlotVar = ""

# Define macros 
def AddMappingDisplacementOperator():
    global automaticMappingEnabled
    if automaticMappingEnabled:
        # Check if  displacement expression exists
        if "_mapping_displacement" in [exp[0] for exp in Expressions()] and len(GetActivePlots()) == 1:
            # If yes, add operator ...
            dispIndex = len(GetPlotList().GetPlots(GetActivePlots()[0]).operators)
            AddOperator("Displace", 0)
            while dispIndex > 0:
                DemoteOperator(dispIndex, 0)
                dispIndex = dispIndex - 1
            # ... and set attributes
            DisplaceAtts = DisplaceAttributes()
            DisplaceAtts.factor = 1
            DisplaceAtts.variable = "_mapping_displacement"
            SetOperatorOptions(DisplaceAtts)

def onAddPlot(plotType, plotVar):
    global activePlotVar
    activePlotVar = plotVar
    # FIXME: Hack, wait for plot to appear in plot list
    time.sleep(0.1)
    # Get list of operators in active plot
    plotOperators = GetPlotList().GetPlots(GetPlotList().GetNumPlots()-1).operators
    # Add displacement operator if one does not alread exists
    # FIXME: It may be better to check whether the Displacement operator
    # is actually performing the mapping instead of just checking type
    if not "Displace" in [OperatorPlugins()[op] for op in plotOperators]:
        AddMappingDisplacementOperator()

RegisterCallback("AddPlotRPC", onAddPlot)

def onSetActivePlots(activePlotList, dummy):
    global activePlotVar
    activePlotVar = GetPlotList().GetPlots(activePlotList[0]).plotVar

RegisterCallback("SetActivePlotsRPC", onSetActivePlots)

def onChangeActivePlotsVar(newVar):
    global activePlotVar
    plotsToChange = ()
    for i in range(0, GetNumPlots()):
        plot = GetPlotList().GetPlots(i)
        if PlotPlugins()[plot.plotType] == "Spreadsheet" and plot.plotVar == activePlotVar:
            plotsToChange = plotsToChange + (i,)
    if len(plotsToChange) > 0:
        activePlotsSave = GetActivePlots()
        SetActivePlots(plotsToChange)
        RegisterCallback("ChangeActivePlotsVarRPC")
        ChangeActivePlotsVar(newVar)
        RegisterCallback("ChangeActivePlotsVarRPC", onChangeActivePlotsVar)
        SetActivePlots(activePlotsSave)
    activePlotVar = newVar

RegisterCallback("ChangeActivePlotsVarRPC", onChangeActivePlotsVar)

def SetupSlice():
    # Import global variable
    global automaticMappingEnabled
    global activePlotVar

    # Disable callback
    RegisterCallback("AddPlotRPC")

    # Get the name of the first variable in the file
    filename = GetWindowInformation().activeSource
    m = GetMetaData(filename)
    varname = m.GetScalars(0).name
    activePlotVar = varname
    meshname = m.GetMeshes(0).name

    if m.GetMeshes(0).topologicalDimension == 2:
        AddPlot("Mesh", meshname)
        AddMappingDisplacementOperator()
        HideActivePlots()
        AddPlot("Pseudocolor", varname)
        AddMappingDisplacementOperator()
    else:
        # Do a mesh plot. We do need a plot to perform a query
        AddPlot("Mesh", meshname)
        MeshAtts = MeshAttributes()
        MeshAtts.legendFlag = 0
        SetPlotOptions(MeshAtts)
        AddMappingDisplacementOperator()

        # Get the centroid
        if m.GetMeshes(0).hasSpatialExtents and not automaticMappingEnabled:
            centroid = (
                0.5 * (m.GetMeshes(0).minSpatialExtents[0] + m.GetMeshes(0).maxSpatialExtents[0]),
                0.5 * (m.GetMeshes(0).minSpatialExtents[1] + m.GetMeshes(0).maxSpatialExtents[1]),
                0.5 * (m.GetMeshes(0).minSpatialExtents[2] + m.GetMeshes(0).maxSpatialExtents[2])
            )
        else:
            DrawPlots()
            Query("Centroid", 0, 0, "default")
            centroid = GetQueryOutputValue()

        # Hide the mesh plot
        HideActivePlots()

        # Add a ThreeSlice through the centroid
        AddOperator("ThreeSlice")
        ThreeSliceAtts = ThreeSliceAttributes()
        ThreeSliceAtts.x = centroid[0]
        ThreeSliceAtts.y = centroid[1]
        ThreeSliceAtts.z = centroid[2]
        SetOperatorOptions(ThreeSliceAtts)

        # Add a Pseudocolor plot and the same ThreeSlice
        AddPlot("Pseudocolor", varname)
        AddMappingDisplacementOperator()
        AddOperator("ThreeSlice")
        SetOperatorOptions(ThreeSliceAtts)

    # Re-enable callback if necessary
    if automaticMappingEnabled:
        RegisterCallback("AddPlotRPC", onAddPlot)

def onOpenDatabase(database, timestate, addDefaultPlots, forcedFileType):
    # Wait until open complete and database is the active source
    filename = GetWindowInformation().activeSource
    while filename != database:
        time.sleep(0.1) 
        filename = GetWindowInformation().activeSource

    if "4d" in filename and "dfn" in filename:
        # <HACK>
        # TEMPORARY HACK: Define expressions for 4D vis
        # ... hardcoded mass
        if not 'm' in [ e[0] for e in Expressions() ]:
            DefineScalarExpression("m", "cell_constant(Mesh, 2)")
        # ... import B and Bstar
        dirname = os.path.dirname(':'.join(filename.split(":")[1:]))
        DefineArrayExpression("Bstar", "conn_cmfe(<"+dirname+"/plt.Bstar_par0000.1.hydrogen.4d.hdf5:component_0>, <Mesh>)")
        DefineScalarExpression("B", "conn_cmfe(<"+dirname+"/BFieldMag2d.hdf5:component_0>, <Mesh>)")
        # ... Expressions to compute derived quantities
        DefineArrayExpression("f_times_Bstar", "array_componentwise_product(component_0, Bstar)")
        DefineScalarExpression("n", "(_dv_par*_dmu)/m*array_sum(f_times_Bstar)")
        DefineScalarExpression("Vpar", "(_dv_par*_dmu)/m*array_sum(array_componentwise_product(f_times_Bstar, _vpar))/n")
        DefineArrayExpression("vpardiff", "_vpar-Vpar")
        DefineScalarExpression("T", "(_dv_par*_dmu)/m*array_sum(array_componentwise_product(f_times_Bstar, m*array_componentwise_product(vpardiff,vpardiff)+_mu*B))/(3*n)")
        densfilename = ':'.join(filename.split(":")[1:]).replace('dfn','density').replace('4d','2d')
        DefineScalarExpression("n_diff", "conn_cmfe(<"+densfilename+":component_0>, <Mesh>) - n")
        DefineScalarExpression("n_reldiff", "n_diff / n")
        temperaturefilename = densfilename.replace('density','temperature')
        DefineScalarExpression("T_diff", "conn_cmfe(<"+temperaturefilename+":component_0>, <Mesh>) - T")
        DefineScalarExpression("T_reldiff", "T_diff / T")
        DefineArrayExpression("FM", "1/((2*T/m)^1.5*1.772453850905516)*n*exp(-(m*sqr(_vpar-Vpar) + _mu*B)/(2*T))")
        #DefineArrayExpression("deltaF", "component_0 - FM")
        DefineArrayExpression("deltaF", "array_componentwise_product(Bstar, component_0 - FM)")
        deltaF_filename = ':'.join(filename.split(":")[1:]).replace('dfn','deltaF')
        DefineArrayExpression("deltaF_COGENT", "conn_cmfe(<"+deltaF_filename+":component_0>, <Mesh>)")
        DefineArrayExpression("deltaF_diff", "deltaF - deltaF_COGENT")
        # </HACK>

    # Check if there is already a plot for opened database. If there is,
    # we do not add further plots. If there are not any plots, we
    # automatically create a slice
    plotExists = False
    for plotNo in range(0, GetNumPlots()):
        if GetPlotList().GetPlots(plotNo).databaseName == filename:
            plotExists = True
            break
    if not plotExists:
        SetupSlice()
        DrawPlots()

RegisterCallback("OpenDatabaseRPC", onOpenDatabase)

def SetupIsosurf():
    global activePlotVar
    # Get the name of the first variable in the file
    filename = GetWindowInformation().activeSource
    m = GetMetaData(filename)
    varname = m.GetScalars(0).name
    activePlotVar = varname

    if m.GetMeshes(0).topologicalDimension == 2:
        # In two dimensions add a simple contour plot ...
        AddPlot("Contour", varname)
        # ... with 10 black contour lines evenly spaced within the fuctnion range
        ContourAtts = ContourAttributes()
        ContourAtts.colorType = ContourAtts.ColorBySingleColor
        ContourAtts.singleColor = (0, 0, 0, 255)
        ContourAtts.contourNLevels = 10
        ContourAtts.legendFlag = 0
        SetPlotOptions(ContourAtts)
    else:
        # Disable callback
        RegisterCallback("AddPlotRPC")
        # In three diemensions add a pseudocolor plot ...
        AddPlot("Pseudocolor", varname)
        AddMappingDisplacementOperator()
        # ... and an isosurface operator ...
        AddOperator("Isosurface")
        # ... with one level at the center of the function range
        IsosurfaceAtts = IsosurfaceAttributes()
        IsosurfaceAtts.contourNLevels = 1
        IsosurfaceAtts.contourMethod = IsosurfaceAtts.Level
        IsosurfaceAtts.scaling = IsosurfaceAtts.Linear
        #IsosurfaceAtts.variable = varname
        SetOperatorOptions(IsosurfaceAtts)
        # Re-enable callback if necessary
        global automaticMappingEnabled
        if automaticMappingEnabled:
            RegisterCallback("AddPlotRPC", onAddPlot)

def SetupBoundingBox():
    filename = GetWindowInformation().activeSource
    m = GetMetaData(filename)
    if len(m.GetMeshes(0).blockNames) == 1:
        AddPlot("Subset", m.GetMeshes(0).name)
    else:
        AddPlot("Subset", m.GetMeshes(0).blockTitle)
    SubsetAtts = SubsetAttributes()
    SubsetAtts.colorType = SubsetAtts.ColorBySingleColor  # ColorBySingleColor, ColorByMultipleColors, ColorByColorTable
    SubsetAtts.legendFlag = 0
    SubsetAtts.lineStyle = SubsetAtts.SOLID  # SOLID, DASH, DOT, DOTDASH
    SubsetAtts.lineWidth = 1
    SubsetAtts.wireframe = 1
    SetPlotOptions(SubsetAtts)

def SetupMesh():
    # Get the name of the first mesh in the file
    filename = GetWindowInformation().activeSource
    m = GetMetaData(filename)
    meshname = m.GetMeshes(0).name
    AddPlot("Mesh", meshname)
    MeshAtts = MeshAttributes()
    MeshAtts.legendFlag = 0
    SetPlotOptions(MeshAtts)

def SetupBoundary():
    # Get the name of the first variable in the file
    filename = GetWindowInformation().activeSource
    m = GetMetaData(filename)
    if m.GetNumMaterials() > 0:
        materialsname = m.GetMaterials(0).name
        if m.GetMeshes(0).topologicalDimension == 2:
            AddPlot("FilledBoundary", materialsname)
            FilledBoundaryAtts = FilledBoundaryAttributes()
            FilledBoundaryAtts.colorType = FilledBoundaryAtts.ColorBySingleColor  # ColorBySingleColor, ColorByMultipleColors, ColorByColorTable
            FilledBoundaryAtts.legendFlag = 0
            FilledBoundaryAtts.lineStyle = FilledBoundaryAtts.SOLID  # SOLID, DASH, DOT, DOTDASH
            FilledBoundaryAtts.lineWidth = 1
            FilledBoundaryAtts.singleColor = (0, 0, 0, 255)
            FilledBoundaryAtts.boundaryType = FilledBoundaryAtts.Material  # Domain, Group, Material, Unknown
            FilledBoundaryAtts.wireframe = 1
            SetPlotOptions(FilledBoundaryAtts)
        else:
            AddPlot("Boundary", materialsname)
            BoundaryAtts = BoundaryAttributes()
            BoundaryAtts.colorType = BoundaryAtts.ColorBySingleColor  # ColorBySingleColor, ColorByMultipleColors, ColorByColorTable
            BoundaryAtts.legendFlag = 0
            BoundaryAtts.singleColor = (255, 255, 255, 255)
            BoundaryAtts.boundaryType = BoundaryAtts.Material  # Domain, Group, Material, Unknown
            SetPlotOptions(BoundaryAtts)
    else:
        print "Error: File contains no EB information."

def GetActivePlots():
    apl = []
    for plotNo in range(0, GetNumPlots()):
        if GetPlotList().GetPlots(plotNo).activeFlag:
            apl.append(plotNo)
    return tuple(apl)

def AddMappingToAllPlots():
    # Remeber plots that were active
    apl_save = GetActivePlots()
    for plotNo in range(0, GetNumPlots()):
        SetActivePlots(plotNo)
        plotHidden = GetPlotList().GetPlots(plotNo).hiddenFlag
        # Check if  displacement expression exists
        plotOperators = GetPlotList().GetPlots(plotNo).operators
        if "_mapping_displacement" in [exp[0] for exp in Expressions()] and not "Displace" in [OperatorPlugins()[op] for op in plotOperators]:
            if not plotHidden:
                HideActivePlots() # Hide plot so that adding operator does not cause error
            # If yes, add operator ...
            dispIndex = len(plotOperators)
            AddOperator("Displace")
            while dispIndex > 0:
                DemoteOperator(dispIndex)
                dispIndex = dispIndex - 1
            # ... and set attributes
            DisplaceAtts = DisplaceAttributes()
            DisplaceAtts.factor = 1
            DisplaceAtts.variable = "_mapping_displacement"
            SetOperatorOptions(DisplaceAtts)

            if not plotHidden:
                HideActivePlots() # If plot was not hidden, show it again
    DrawPlots()
    # Restore active plots
    SetActivePlots(apl_save)

def RemoveMappingFromAllPlots():
    # Remeber plots that were active
    apl_save = GetActivePlots()
    for plotNo in range(0, GetNumPlots()):
        plotOperators = GetPlotList().GetPlots(plotNo).operators
        SetActivePlots(plotNo)
        for opNo in range(0, len(plotOperators)):
            if OperatorPlugins()[plotOperators[opNo]] == 'Displace' and GetOperatorOptions(opNo).variable == "_mapping_displacement":
                RemoveOperator(opNo)
    DrawPlots()
    # Restore active plots
    SetActivePlots(apl_save)

def EnableAutomaticMapping():
    global automaticMappingEnabled
    automaticMappingEnabled = True
    AddMappingToAllPlots()
    RegisterCallback("AddPlotRPC", onAddPlot)

def DisableAutomaticMapping():
    global automaticMappingEnabled
    automaticMappingEnabled = False
    RemoveMappingFromAllPlots()
    RegisterCallback("AddPlotRPC")

#pick4d_distributions = [ "component_0", "FM", "deltaF" ]
pick4d_distributions = [ "component_0" ]

def PerformPick4D(pa):
    global lastPickOutput
    if lastPickOutput != GetPickOutput():
        lastPickOutput = GetPickOutput()
        pattern = re.compile('level <([^>]*)>')
        match = pattern.search(lastPickOutput)
        if match != None:
            try:
                (i, j) = match.group(1).split(",")
                i = int(i)
                j = int(j)
                RegisterCallback("SetActivePlotsRPC")
                for window, distribution in enumerate(pick4d_distributions, 2):
                    SetActiveWindow(window)
                    DeleteAllPlots()
                    AddPlot("Pseudocolor", "operators/ExtractPointFunction2D/%s" % distribution)
                    ExtractPointFunction2DAtts = ExtractPointFunction2DAttributes()
                    ExtractPointFunction2DAtts.I = i
                    ExtractPointFunction2DAtts.J = j
                    SetOperatorOptions(ExtractPointFunction2DAtts)
                    DrawPlots()

                RegisterCallback("SetActivePlotsRPC", onSetActivePlots)
                SetActiveWindow(1)
            except:
                pass

def StartPick4D():
    global lastPickOutput
    lastPickOutput = GetPickOutput()
    pickAtts = GetPickAttributes()
    pickAtts.variables = ("default")
    pickAtts.showIncidentElements = 0
    pickAtts.showNodeId = 0
    pickAtts.showNodeDomainLogicalCoords = 0
    pickAtts.showNodeBlockLogicalCoords = 0
    pickAtts.showNodePhysicalCoords = 0
    pickAtts.showZoneId = 0
    pickAtts.showZoneDomainLogicalCoords = 0
    pickAtts.showZoneBlockLogicalCoords = 1
    pickAtts.doTimeCurve = 0
    pickAtts.conciseOutput = 0
    pickAtts.showTimeStep = 0
    pickAtts.showMeshName = 0
    pickAtts.showGlobalIds = 0
    pickAtts.showPickLetter = 0
    pickAtts.reusePickLetter = 1
    pickAtts.createSpreadsheet = 0
    pickAtts.floatFormat = "%g"
    SetPickAttributes(pickAtts)
    RegisterCallback("PickAttributes", PerformPick4D)
    SetWindowMode("zone pick")
    if len(pick4d_distributions) == 1:
        SetWindowLayout(2)
    else:
        SetWindowLayout(4)
    SetActiveWindow(1)

def EndPick4D():
    SetWindowLayout(1)
    SetWindowMode("navigate")
    RegisterCallback("PickAttributes")

RegisterMacro("Slice", SetupSlice)
RegisterMacro("Contours", SetupIsosurf)
RegisterMacro("Boxes", SetupBoundingBox)
RegisterMacro("Mesh", SetupMesh)
RegisterMacro("EB", SetupBoundary)
RegisterMacro("Mapping on", EnableAutomaticMapping)
RegisterMacro("Mapping off", DisableAutomaticMapping)
RegisterMacro("Start 4D Pick", StartPick4D)
RegisterMacro("End 4D Pick", EndPick4D)
def user_macro_Basic_view_settings():
    AddPlot("Pseudocolor", "phi", 1, 1)
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
    SetActivePlots(1)
    SetActivePlots(1)
    PseudocolorAtts = PseudocolorAttributes()
    PseudocolorAtts.scaling = PseudocolorAtts.Linear  # Linear, Log, Skew
    PseudocolorAtts.skewFactor = 1
    PseudocolorAtts.limitsMode = PseudocolorAtts.OriginalData  # OriginalData, CurrentPlot
    PseudocolorAtts.minFlag = 0
    PseudocolorAtts.min = 0
    PseudocolorAtts.maxFlag = 0
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
    DrawPlots()
    SetActivePlots((0, 1))
    SetActivePlots(0)
    silr = SILRestriction()
    silr.TurnOnAll()
    SetPlotSILRestriction(silr ,1)
    DrawPlots()
    
    # Set viewing attributes
    
    ViewCurveAtts = ViewCurveAttributes()
    ViewCurveAtts.domainCoords = (0, 1)
    ViewCurveAtts.rangeCoords = (0, 1)
    ViewCurveAtts.viewportCoords = (0.2, 0.95, 0.15, 0.95)
    ViewCurveAtts.domainScale = ViewCurveAtts.LINEAR  # LINEAR, LOG
    ViewCurveAtts.rangeScale = ViewCurveAtts.LINEAR  # LINEAR, LOG
    SetViewCurve(ViewCurveAtts)
    View2DAtts = View2DAttributes()
    View2DAtts.windowCoords = (312, 702, 312, 702)
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
    
RegisterMacro("Basic_view_settings", user_macro_Basic_view_settings)

