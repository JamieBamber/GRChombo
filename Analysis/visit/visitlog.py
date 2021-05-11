# Visit 2.13.3 log file
ScriptVersion = "2.13.3"
if ScriptVersion != Version():
    print "This script is for VisIt %s. It may not work with version %s" % (ScriptVersion, Version())
ShowAllWindows()
SetActivePlots()
DeleteActivePlots()
OpenDatabase("/cosma6/data/dp174/dc-bamb1/GRChombo_data/BinaryBHSF/run0023ICS_mu0.5_delay0_G0.0000000001_ratio1/BinaryBHSFChk_000000.3d.hdf5", 0)
