#!/bin/bash
#
# This script should make a new directory in GRChombo_data for the data, and copy the slurm_submit file, params.txt file and output files to
# that directory, submit the job, then change back to the working directory

# this copy is for COSMA6

work_dir=/p/home/jusers/bamber1/juwels/GRChombo/Examples/NewtonianScalar
cd $work_dir
data_directory=/p/scratch/pra116/bamber1/NewtonianBinaryScalar
#data_directory=/p/project/pra116/bamber1/NewtonianBinaryBHScalar

# specify the input params for each run I want to submit
# list for each is: M1, M2, d, mu, dt, l, m, Al, disp_ratio 

# original values were
# note: M = 0.4885, d = 6.1, omega_binary = 0.06560735
# period = 95.7695
# dt = 2 * dt_multiplier

# M = 0.2, d = 10 gives omega_binary = 0.02
# omega = sqrt{2 M / d^3}

run0001=(0.1 0.1 20 0.014142136 0.25 0 0 0)
run0002=(0.1 0.1 20 0.005 0.25 0 0 0)
run0003=(0.1 0.1 20 0.02 0.25 0 0 0)
run0004=(0.1 0.1 20 0.1 0.25 0 0 0)
run0005=(0.1 0.1 20 0.01 0.25 0 0 0)
run0006=(0.1 0.1 20 0.5 0.0625 0 0 0)

#
run0005=(0.2 0.2 10 0.002 0.5 0 0 0)
run0006=(0.2 0.2 10 0.005 0.5 0 0 0)
run0007=(0.2 0.2 10 0.02 0.5 0 0 0)
run0008=(0.2 0.2 10 0.025 0.5 0 0 0)
run0009=(0.2 0.2 10 0.015 0.5 0 0 0)
run0010=(0.2 0.2 10 0.01 0.5 0 0 0)
run0011=(0.2 0.2 10 0.03 0.5 0 0 0)
#
#run0012=(0.2 10 0.02 0.5 1 -1 0)
#run0013=(0.2 10 0.02 0.5 1 1 0)
run0115=(0.5 0.5 12 1 0.03125 0 0 0 1.0)
run0015=(0.48847892320123 0.48847892320123 12.21358 1 0.03125 0 0 0)
run0215=(0.3194742895317072 0.654181589210298 10.0 1 0.03125 0 0 0 2.0)
run0016=(0.48847892320123 0.48847892320123 12.21358 1 0.03125 1 -1 0)
run0017=(0.48847892320123 0.48847892320123 12.21358 1 0.03125 1 1 0)
run0018=(0.2 0.2 10 1 0.03125 0 0 0)
run0019=(0.2 0.2 10 0.1 0.125 0 0 0)
run0020=(0.2 0.2 10 0.5 0.0625 0 0 0)
run0021=(0.2 0.2 10 0.05 0.25 0 0 0)
run0022=(0.2 0.2 10 0.2 0.0625 0 0 0)
run0023=(0.2 0.2 10 0.3 0.0625 0 0 0)
run0024=(0.2 0.2 10 0.15 0.0625 0 0 0)
run0025=(0.2 0.2 10 0.25 0.0625 0 0 0)
run0026=(0.2 0.2 10 2 0.03125 0 0 0)
run0027=(0.2 0.2 10 5 0.015625 0 0 0)

params_file=params.txt

run_list=(
#    run0005
#    run0006
#   run0007
#    run0008
#    run0009
#    run0010
#    run0011
run0115
#run0016
#run0017
#run0018
#run0019
#run0026
#run0021
#run0022
#run0023
#run0024
#run0025
#    run0026
#    run0027
)

# dt_raw = 2
# dt = 1
# period ~ 315

plot_interval=1
L=1024
N1=256
box_size=32

restart_hash="#"
restart_num="000000"

for run in "${run_list[@]}"
do
  	cd $work_dir
        # extract parameters    
        val="$run[0]"; M1="${!val}"
	val="$run[1]"; M2="${!val}"
        val="$run[2]"; d="${!val}"
        val="$run[3]"; mu="${!val}"
        val="$run[4]"; dt_mult="${!val}"
        val="$run[5]"; l="${!val}"
        val="$run[6]"; m="${!val}"
        val="$run[7]"; Al="${!val}"
	val="$run[8]"; disp_ratio="${!val}"
	
	omega_BH=$(awk "BEGIN {printf \"%.7f\n\", sqrt((${M1}+${M2})/(${d}*${d}*${d}))}")
	#omega_BH=$(bc <<< "scale=6; sqrt(2*${M}/(${d}*${d}*${d}))")
	echo "omega_BH = ${omega_BH}"

        # text_number=$(printf "%04d" ${run_number})
	if [[ $M1 == $M2 ]]
	then
	   new_dir=${run}_M${M1}_d${d}_mu${mu}_dt_mult${dt_mult}_l${l}_m${m}_Al${Al}_L${L}_N${N1}
	else
           new_dir=${run}_M1${M1}_M2${M2}_d${d}_mu${mu}_dt_mult${dt_mult}_l${l}_m${m}_Al${Al}_L${L}_N${N1}
	fi
        echo ${new_dir}
        new_dir_path=${data_directory}/${new_dir}
        #
	mkdir -p ${new_dir_path}
	cp ScalarFieldLevel.cpp ${new_dir_path}/ScalarFieldLevel.cpp.txt
        cp slurm_submit_juwels_test ${new_dir_path}/slurm_submit
	params_file=params.txt
        cp ${params_file} ${new_dir_path}/params.txt

	cd ${new_dir_path}
        chk_file=Newton_chk${restart_num}.3d.hdf5
        for chk in Newton_chk*.hdf5
        do
            chk_file=$chk
        done
        echo $chk_file
        #                                                                                                # add the input params to the input files
        sed -i "s|DATADIR|${new_dir_path}|" ${new_dir_path}/params.txt
        sed -i "s|DATASUBDIR|${new_dir}|" ${new_dir_path}/params.txt
        sed -i "s|DTMULT|${dt_mult}|" ${new_dir_path}/params.txt
        sed -i "s|JOBNAME|${run}NS|" ${new_dir_path}/slurm_submit
        sed -i "s|BOXLENGTH|${L}|" ${new_dir_path}/params.txt
        sed -i "s|BOXSIZE|${box_size}|" ${new_dir_path}/params.txt
        sed -i "s|CENTERX|$(($L/2))|" ${new_dir_path}/params.txt
        sed -i "s|CENTERY|$(($L/2))|" ${new_dir_path}/params.txt
        sed -i "s|BHMASS1|${M1}|" ${new_dir_path}/params.txt
	sed -i "s|BHMASS2|${M2}|" ${new_dir_path}/params.txt
	sed -i "s|DISPRATIO|${disp_ratio}|" ${new_dir_path}/params.txt
	sed -i "s|BHSEP|${d}|" ${new_dir_path}/params.txt
        sed -i "s|MUVAL|${mu}|" ${new_dir_path}/params.txt
        sed -i "s|SCALARL|${l}|" ${new_dir_path}/params.txt
        sed -i "s|SCALARM|${m}|" ${new_dir_path}/params.txt
	sed -i "s|RESTARTHASH|${restart_hash}|" ${new_dir_path}/params.txt
        #sed -i "s|RESTARTNUM|${restart_num}|" ${new_dir_path}/params.txt
	sed -i "s|CHKFILE|${chk_file}|" ${new_dir_path}/params.txt
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
