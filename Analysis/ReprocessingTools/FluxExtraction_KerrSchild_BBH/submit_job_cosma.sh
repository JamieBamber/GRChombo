#!/bin/bash
#
# this copy is for the Skylake nodes

work_dir=/cosma/home/dp174/dc-bamb1/GRChombo/Analysis/ReprocessingTools/FluxExtraction_KerrSchild_BBH

start_number=0
end_number=200000
resume=0 # resume previous extraction?

nphi=36
ntheta=24
extraction_radius=100
N1=64
L=512
box_size=16
plot_interval=50

data_directory=/cosma6/data/dp174/dc-bamb1/GRChombo_data/BinaryBHSF

# specify the input params for each run I want to submit
# list for each is: M, d, mu, dt 

# original values were
# note: M = 0.4885, d = 6.1, omega_binary = 0.06560735
# period = 95.7695
# dt = 2 * dt_multiplier

run0011=(1 0 0.0625 0 1)
run0012=(1 10000 0.0625 0 1)
run0003=(0.08187607564 0 0.25 0 1)
run0014=(1 0 0.0625 0 2)
run0015=(1 10000 0.0625 0 2)
run0016=(0.5 0 0.25 0 1)
run0017=(0.5 10000 0.25 0 1)
run0018=(0.5 0 0.25 0.000001 1)

params_file=params.txt

# specify runs to submit
run_list=(
	run0011
)

for run in "${run_list[@]}"
do
  	cd $work_dir
	#
        val="$run[0]"; mu="${!val}"
        val="$run[1]"; delay="${!val}"
        val="$run[2]"; dt_mult="${!val}"
        val="$run[3]"; G="${!val}"
        val="$run[4]"; ratio="${!val}"

        # text_number=$(printf "%04d" ${run_number})
        subdir=${run}_mu${mu}_delay${delay}_G${G}_ratio${ratio}

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
