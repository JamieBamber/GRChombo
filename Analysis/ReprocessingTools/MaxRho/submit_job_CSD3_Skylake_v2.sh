#!/bin/bash
#
# this copy is for the Skylake nodes

work_dir=/home/dc-bamb1/GRChombo/Analysis/ReprocessingTools/MaxRho

start_number=0
end_number=20000
lin_or_log=1 # note 0 = log, 1 = linear
max_radius=300
N1=128
Nhalf=$(($N1 / 2))

# specify the input params for each run I want to submit
# list for each is: l, m, a, Al, mu, dt
# test adding spin
run0001=(0 0 0.0 0 0.4 0.0625)
run0002=(0 0 0.7 0 0.4 0.0625)
run0003=(0 0 0.99 0 0.4 0.0625)
# same for l=m=1
run0004=(1 1 0.0 0 0.4 0.0625)
run0005=(1 1 0.7 0 0.4 0.0625)
run0006=(1 1 0.99 0 0.4 0.0625)
# test lm
run0007=(2 2 0.7 0 0.4 0.0625)
run0008=(4 4 0.7 0 0.4 0.0625)
run0009=(1 -1 0.7 0 0.4 0.0625)
run0010=(8 8 0.7 0 0.4 0.0625)
# test effect of mu
# run0111=(0 0 0.0 0 0.05 0.4)
run0011=(1 1 0.7 0 2.0 0.015625)
run0012=(1 1 0.7 0 0.01 0.0625)
# test effect of m / mu ratio
run0013=(2 2 0.7 0 0.8 0.03125)
run0014=(8 8 0.7 0 3.2 0.0078125)
# test effect of alignment
run0015=(1 1 0.7 0.5 0.4 0.0625)
run0016=(1 -1 0.99 0 0.4 0.0625)
run0017=(1 1 0.99 0.5 0.4 0.0625)
run0018=(1 1 0.99 0.25 0.4 0.0625)
run0019=(1 1 0.7 0 0.01 2.5)

plot_interval=10
#var_index=6

# specify runs to submit
run_list=(
	run0007
)

## loop over subdirs
for run in "${run_list[@]}"
do
  	cd $work_dir

        # extract parameters    
        val="$run[0]"; l="${!val}"
        val="$run[1]"; m="${!val}"
        val="$run[2]"; a="${!val}"
        val="$run[3]"; Al="${!val}"
        M=1
	val="$run[4]"; mu="${!val}"
        val="$run[5]"; dt_mult="${!val}"

        # text_number=$(printf "%04d" ${run_number})
        subdir=${run}_l${l}_m${m}_a${a}_Al${Al}_mu${mu}_M${M}_IsoKerr
	#_N$N1

	# note vars = {phi Pi chi rho rho_azimuth J_rKS J_azimuth_rKS J_R J_azimuth_R}
	min_radius=$(echo "scale=5; ${M}*(1.00 + sqrt(1 - ${a} * ${a}))" | bc)
	#min_radius=5
	echo "mu = " ${mu}
	echo "min_radius = " ${min_radius}

	suffix=full_region

        #dt_mult=$(echo "scale=5; 0.025 / ${mu}" | bc | sed 's/^\./0./')
        echo "dt_multiplier = " ${dt_mult}

        name=${subdir}_max_rho_and_rho_azimuth
	
	echo ${name} "flux extraction"
	new_dir_path=outputs/${name}
	#
	mkdir -p ${new_dir_path}
	
	cp slurm_submit_Skylake ${new_dir_path}/slurm_submit
	cp params.txt ${new_dir_path}
	
	cd ${new_dir_path}
	# add the location of the new directory to the params file
	sed -i "s|JOBNAME|${run}MR|" slurm_submit
	sed -i "s|DTMULT|${dt_mult}|" params.txt
	sed -i "s|NBASIC|${N1}|" params.txt
	sed -i "s|SUBDIR|${subdir}|" params.txt
	sed -i "s|BHSPIN|${a}|" params.txt
	sed -i "s|BHMASS|${M}|" params.txt
	sed -i "s|SNUMBER|${start_number}|" params.txt
	sed -i "s|ENUMBER|${end_number}|" params.txt
	sed -i "s|VARINDEX|${var_index}|" params.txt
	sed -i "s|PLOTINTERVAL|${plot_interval}|" params.txt
	sed -i "s|MINRADIUS|${min_radius}|" params.txt
	sed -i "s|MAXRADIUS|${max_radius}|" params.txt
	sed -i "s|SFIX|${suffix}|" params.txt

	# half box or full box?
        if (( $(echo "$Al > 0.0" |bc -l) )); then
                echo "Al = $Al so full box"
                sed -i "s|NSPACE3|${N1}|" params.txt
                sed -i "s|CENTERZ|512.0|" params.txt
                sed -i "s|ZBOUND|3|" params.txt
		sed -i "s|HALFBOX|0|" params.txt
        else
            	echo "Al = $Al so half box"
                sed -i "s|NSPACE3|${Nhalf}|" params.txt
                sed -i "s|CENTERZ|0.0|" params.txt
                sed -i "s|ZBOUND|2|" params.txt
		sed -i "s|HALFBOX|1|" params.txt
        fi
	sbatch slurm_submit
	#
	cd ${work_dir}
done	
