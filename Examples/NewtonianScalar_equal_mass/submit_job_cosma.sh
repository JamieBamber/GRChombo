#!/bin/bash
#
# This script should make a new directory in GRChombo_data for the data, and copy the slurm_submit file, params.txt file and output files to
# that directory, submit the job, then change back to the working directory

# this copy is for COSMA6

work_dir=/cosma/home/dp174/dc-bamb1/GRChombo/Examples/NewtonianScalar_equal_mass
cd $work_dir
data_directory=/cosma6/data/dp174/dc-bamb1/GRChombo_data/NewtonianBinaryBHScalar

# specify the input params for each run I want to submit
# list for each is: M, d, mu, dt, l, m, Al 

# original values were
# note: M = 0.4885, d = 6.1, omega_binary = 0.06560735
# period = 95.7695
# dt = 2 * dt_multiplier

# M = 0.1, d = 20 gives omega_binary = 0.005

run0001=(0.1 20 0.014142136 0.25 0 0 0)
run0002=(0.1 20 0.005 0.25 0 0 0)
run0003=(0.1 20 0.02 0.25 0 0 0)
run0004=(0.1 20 0.1 0.25 0 0 0)
run0005=(0.1 20 0.01 0.25 0 0 0)
run0006=(0.1 20 0.5 0.0625 0 0 0)
#
run0007=(0.2 10 0.02 0.5 0 0 0)
run0008=(0.2 10 0.025 0.5 0 0 0)
run0009=(0.2 10 0.015 0.5 0 0 0)
run0010=(0.2 10 0.01 0.5 0 0 0)
run0011=(0.2 10 0.03 0.5 0 0 0)
#
run0012=(0.2 10 0.02 0.5 1 1 0)
run0012=(0.2 10 0.02 0.5 1 -1 0)
run0015=(0.48847892320123 12.21358 1 0.0625 0 0 0)
run0020=(0.2 10 0.5 0.0625 0 0 0)

params_file=params.txt

run_list=(
	run0020
)

plot_interval=5
L=1024
N1=256
box_size=32

for run in "${run_list[@]}"
do
  	cd $work_dir
        # extract parameters    
        val="$run[0]"; M="${!val}"
        val="$run[1]"; d="${!val}"
        val="$run[2]"; mu="${!val}"
        val="$run[3]"; dt_mult="${!val}"
        val="$run[4]"; l="${!val}"
        val="$run[5]"; m="${!val}"
        val="$run[6]"; Al="${!val}"
        
       	omega_BH=$(awk "BEGIN {printf \"%.7f\n\", sqrt(2*${M}/(${d}*${d}*${d}))}")
        #omega_BH=$(bc <<< "scale=6; sqrt(2*${M}/(${d}*${d}*${d}))")
        echo "omega_BH = ${omega_BH}"

        # text_number=$(printf "%04d" ${run_number})
        new_dir=${run}_M${M}_d${d}_mu${mu}_dt_mult${dt_mult}_l${l}_m${m}_Al${Al}_L${L}_N${N1}

        echo ${new_dir}
        new_dir_path=${data_directory}/${new_dir}
        #
	mkdir -p ${new_dir_path}
        cp slurm_submit_cosma ${new_dir_path}/slurm_submit
        params_file=params.txt
        cp ${params_file} ${new_dir_path}/params.txt

        cd ${new_dir_path}
        # add the input params to the input files
        sed -i "s|DATADIR|${new_dir_path}|" ${new_dir_path}/params.txt
        sed -i "s|DATASUBDIR|${new_dir}|" ${new_dir_path}/params.txt
        sed -i "s|DTMULT|${dt_mult}|" ${new_dir_path}/params.txt
        sed -i "s|JOBNAME|${run}NS|" ${new_dir_path}/slurm_submit
        sed -i "s|BOXLENGTH|${L}|" ${new_dir_path}/params.txt
        sed -i "s|BOXSIZE|${box_size}|" ${new_dir_path}/params.txt
        sed -i "s|CENTERX|$(($L/2))|" ${new_dir_path}/params.txt
        sed -i "s|CENTERY|$(($L/2))|" ${new_dir_path}/params.txt
        sed -i "s|BHMASS|${M}|" ${new_dir_path}/params.txt
        sed -i "s|BHSEP|${d}|" ${new_dir_path}/params.txt
        sed -i "s|MUVAL|${mu}|" ${new_dir_path}/params.txt
        sed -i "s|SCALARL|${l}|" ${new_dir_path}/params.txt
        sed -i "s|SCALARM|${m}|" ${new_dir_path}/params.txt
        sed -i "s|ALANGLE|${Al}|" ${new_dir_path}/params.txt
        sed -i "s|OMEGABH|${omega_BH}|" ${new_dir_path}/params.txt
        sed -i "s|NBASIC|${N1}|" ${new_dir_path}/params.txt
        sed -i "s|NSPACE3|$(($N1/2))|" ${new_dir_path}/params.txt
        sed -i "s|PLOTINTERVAL|${plot_interval}|" ${new_dir_path}/params.txt
	#
	mkdir -p outputs
        cd outputs
        sbatch ../slurm_submit
        #
	cd ${work_dir}
done
