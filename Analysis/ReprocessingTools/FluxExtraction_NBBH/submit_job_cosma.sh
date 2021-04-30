#!/bin/bash
#
# this copy is for the Skylake nodes

work_dir=/cosma/home/dp174/dc-bamb1/GRChombo/Analysis/ReprocessingTools/FluxExtraction_NBBH

start_number=0
end_number=200000
resume=0 # resume previous extraction?

nphi=36
ntheta=24
extraction_radius=50
N1=128
L=256
box_size=16
plot_interval=50

data_directory=/cosma6/data/dp174/dc-bamb1/GRChombo_data/NewtonianBinaryBHScalar

# specify the input params for each run I want to submit
# list for each is: M, d, mu, dt 

# original values were
# note: M = 0.4885, d = 6.1, omega_binary = 0.06560735
# period = 95.7695
# dt = 2 * dt_multiplier

run0001=(0.1 10 0.014142136 0.25)
run0002=(0.1 10 0.005 0.25)
run0003=(0.1 10 0.02 0.25)
run0004=(0.1 10 0.1 0.25)

run0007=(0.2 10 0.02 0.5)
run0008=(0.2 10 0.025 0.5)
run0009=(0.2 10 0.015 0.5)
run0010=(0.2 10 0.01 0.5)
run0011=(0.2 10 0.03 0.5)

params_file=params.txt

run_list=(
	run0007
	run0008
	run0009
	run0010
	run0011
)

for run in "${run_list[@]}"
do
  	cd $work_dir
        # extract parameters    
        val="$run[0]"; M="${!val}"
        val="$run[1]"; d="${!val}"
        val="$run[2]"; mu="${!val}"
        val="$run[3]"; dt_mult="${!val}"
        
       	omega_BH=$(awk "BEGIN {printf \"%.7f\n\", sqrt(2*${M}/(${d}*${d}*${d}))}")
        #omega_BH=$(bc <<< "scale=6; sqrt(2*${M}/(${d}*${d}*${d}))")
        echo "omega_BH = ${omega_BH}"

        # text_number=$(printf "%04d" ${run_number})
        subdir=${run}_M${M}_d${d}_mu${mu}_dt_mult${dt_mult}

	suffix=_r_${extraction_radius}

	name=${subdir}_flux${suffix}
	echo ${name} "flux extraction"
	new_dir_path=outputs/${name}
	#
	mkdir -p ${new_dir_path}
	
	cp slurm_submit_cosma ${new_dir_path}/slurm_submit
	cp params.txt ${new_dir_path}
	
	cd ${new_dir_path}
	# add the location of the new directory to the params file
	sed -i "s|JOBNAME|${run}FE|" slurm_submit
	sed -i "s|DTMULT|${dt_mult}|" params.txt
	sed -i "s|RESUMEYN|${resume}|" params.txt
	sed -i "s|SUBDIR|${subdir}|" params.txt
	sed -i "s|LSPACE|${L}|" params.txt
	sed -i "s|NBASIC|${N1}|" params.txt
	sed -i "s|BOXSIZE|${box_size}|" params.txt
	sed -i "s|CENTERX|$(($L/2))|" params.txt
	sed -i "s|CENTERY|$(($L/2))|" params.txt
	sed -i "s|CENTERZ|0|" params.txt
	sed -i "s|SNUMBER|${start_number}|" params.txt
	sed -i "s|ENUMBER|${end_number}|" params.txt
	sed -i "s|PLOTINTERVAL|${plot_interval}|" params.txt
	sed -i "s|REXTRACT|${extraction_radius}|" params.txt
	sed -i "s|NPHI|${nphi}|" params.txt
	sed -i "s|NTHETA|${ntheta}|" params.txt
	sed -i "s|SUFFIX|${suffix}|" params.txt

	sbatch slurm_submit
	#
	cd ${work_dir}
done	
