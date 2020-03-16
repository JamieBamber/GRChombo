# Visit 3.0.0 log file
ScriptVersion = "3.0.0"
if ScriptVersion != Version():
    print "This script is for VisIt %s. It may not work with version %s" % (ScriptVersion, Version())
ShowAllWindows()
Source("/dss/dsshome1/lrz/noarch/src/graphics/visit/install/3.0.0/linux-x86_64/bin/makemovie.py")
Source("phi_movie_plot_script.py.mangled")
# Visit 3.0.0 log file
ScriptVersion = "3.0.0"
if ScriptVersion != Version():
    print "This script is for VisIt %s. It may not work with version %s" % (ScriptVersion, Version())
ShowAllWindows()
Source("/dss/dsshome1/lrz/noarch/src/graphics/visit/install/3.0.0/linux-x86_64/bin/makemovie.py")
Source("phi_movie_plot_script.py.mangled")
