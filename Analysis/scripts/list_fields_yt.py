import yt

data_dir="/p/project/pra116/bamber1/BinaryBHScalarField/"
#data_dir="/p/scratch/pra116/bamber1/NewtonianBinaryScalar/"
#subdir="run0023v2_mu0.5_delay0_G0.0000000001_ratio1"
#run0023ICS_mu0.5_delay0_G0.00000001_ratio1_l0_m0_Al0"
#subdir="run0020_M0.2_d10_mu0.5_dt_mult0.0625_l0_m0_Al0_L1024_N256"
number=0

"BinaryBHSFChk_000000.3d.hdf5"

def print_fields(subdir):
  filename=data_dir+subdir+"/BinaryBHSFChk_{:06d}.3d.hdf5".format(number)
  #filename=data_dir+subdir+"/BinaryBHSFPlot_{:06d}.3d.hdf5".format(number)
  #filename=data_dir+subdir+"/Newton_plt{:06d}.3d.hdf5".format(number)     

  ds = yt.load(filename)

  print("loaded ", filename)

  print("fields = ")
  for i in sorted(ds.field_list):
    print(i)

print_fields("run0023_mu0.5_delay0_G0.0000000001_ratio1")
print_fields("run0023ICS_mu0.5_delay0_G0.0000000001_ratio1")
