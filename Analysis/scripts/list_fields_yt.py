import yt

data_dir="/p/project/pra116/bamber1/BinaryBHScalarField/"
subdir="run0025_mu0.5_delay0_G0_ratio1_l1_m1_Al0"
#subdir="run0018_mu0.5_delay0_G0.000001_ratio1"
number=0

"BinaryBHSFChk_000000.3d.hdf5"

#filename=data_dir+subdir+"/BinaryBHSFChk_{:06d}.3d.hdf5".format(number)
filename=data_dir+subdir+"/BinaryBHSFPlot_{:06d}.3d.hdf5".format(number)

ds = yt.load(filename)

print("loaded ", filename)

print("fields = ")
for i in sorted(ds.field_list):
  print(i)

