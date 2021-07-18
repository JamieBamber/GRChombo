#!/bin/bash
#
# this copy is for cosma7

work_dir=/cosma/home/dp174/dc-bamb1/GRChombo/Analysis/ReprocessingTools/SphericalExtraction_v2

start_number=0
end_number=200000
resume=0 # resume previous extraction?

nphi=64
ntheta=32
# extraction_radius=50
N1=256
L=1024
box_size=32
plot_interval=5

data_directory=/cosma6/data/dp174/dc-bamb1/GRChombo_data/NewtonianBinaryBHScalar

# specify the input params for each run I want to submit
# list for each is: M, d, mu, dt 

# original values were
# note: M = 0.4885, d = 6.1, omega_binary = 0.06560735
# period = 95.7695
# dt = 2 * dt_multiplier

run0020=(0.2 10 0.5 0.0625 0 0 0)

params_file=params.txt

run_list=(
	run0020
)

for run in "${run_list[@]}"
do
  	cd $work_dir
        # extract parameters
	val="$run[0]"; M="${!val}"
	echo "M="$M
        val="$run[1]"; d="${!val}"
        val="$run[2]"; mu="${!val}"
        val="$run[3]"; dt_mult="${!val}"
        val="$run[4]"; l="${!val}"
        val="$run[5]"; m="${!val}"
        val="$run[6]"; Al="${!val}"
        
       	##omega_BH=$(awk "BEGIN {printf \"%.7f\n\", sqrt(2*${M}/(${d}*${d}*${d}))}")
        ##omega_BH=$(bc <<< "scale=6; sqrt(2*${M}/(${d}*${d}*${d}))")
        ##echo "omega_BH = ${omega_BH}"

        # text_number=$(printf "%04d" ${run_number})
        subdir=${run}_M${M}_d${d}_mu${mu}_dt_mult${dt_mult}_l${l}_m${m}_Al${Al}_L${L}_N${N1}

	# suffix=_r_${extraction_radius}

	name=${subdir}_phi_integrals
	echo ${name} "phi integrals"
	new_dir_path=outputs/${name}
	#
	mkdir -p ${new_dir_path}
	
	cp slurm_submit_cosma7 ${new_dir_path}/slurm_submit
	cp params.txt ${new_dir_path}
	
	cd ${new_dir_path}
	# add the location of the new directory to the params file
	sed -i "s|JOBNAME|${run}PI|" slurm_submit
	sed -i "s|DTMULT|${dt_mult}|" params.txt
	sed -i "s|RESUMEYN|${resume}|" params.txt
	sed -i "s|SUBDIR|${subdir}|" params.txt
	sed -i "s|LSPACE|${L}|" params.txt
	sed -i "s|NBASIC|${N1}|" params.txt
	sed -i "s|NSPACE3|$(($N1/2))|" params.txt
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
