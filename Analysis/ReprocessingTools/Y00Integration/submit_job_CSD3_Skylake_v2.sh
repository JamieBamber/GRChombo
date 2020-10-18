#!/bin/bash
#
# this copy is for the Skylake nodes

work_dir=/home/dc-bamb1/GRChombo/Analysis/ReprocessingTools/Y00Integration

start_number=0
end_number=20000
lin_or_log=0 # note 0 = log, 1 = linear
resume=0 # resume previous integration?

nphi=64
ntheta=18
theta_max=1.0
max_radius=500

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
run0021=(0 0 0.7 0 2.0 0.015625)
run0020=(1 1 0.7 0 0.1 0.25)
run0022=(8 8 0.99 0 2.0 0.015625)
run0023=(1 1 0.7 0 0.2 0.125)
run0024=(1 1 0.7 0 0.125 0.2)

plot_interval=10
# vars = phi Pi chi rho rho_azimuth J_R J_azimuth_R
var_index=5

# specify runs to submit
run_list=(
	run0006
	run0008
	run0010
	run0011
	run0016
)

run_list2=(
	run0017
	run0018
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

	# note vars = {phi Pi chi rho rho_azimuth J_rKS J_azimuth_rKS J_R J_azimuth_R}
	min_radius=$(echo "scale=5; ${M}*(1.00 + sqrt(1 - ${a} * ${a}))" | bc)
	nradii=513
	#min_radius=5
	echo "min_radius = " ${min_radius}
	
	suffix=_r_plus_to_${max_radius}_nphi${nphi}_ntheta${ntheta}_theta_max${theta_max}
	#suffix=_${min_radius}_to_${max_radius}_nphi${nphi}_ntheta${ntheta}_theta_max${theta_max}

	#dt_mult=$(echo "scale=5; 0.025 / ${mu}" | bc | sed 's/^\./0./')
	echo "dt_multiplier = " ${dt_mult}

	name=${subdir}_var${var_index}_Ylm_integration_n${start_number}_linlog${lin_or_log}${suffix}
	echo ${name} "Ylm integration"
	new_dir_path=outputs/${name}
	#
	mkdir -p ${new_dir_path}
	
	cp slurm_submit_Skylake_short ${new_dir_path}/slurm_submit
	cp params.txt ${new_dir_path}
	
	cd ${new_dir_path}
	# add the location of the new directory to the params file
	sed -i "s|JOBNAME|${run}YlmI|" slurm_submit
	sed -i "s|DTMULT|${dt_mult}|" params.txt
	sed -i "s|SUBDIR|${subdir}|" params.txt
	sed -i "s|BHSPIN|${a}|" params.txt
	sed -i "s|VARINDEX|${var_index}|" params.txt
	sed -i "s|RESUMEYN|${resume}|" params.txt
	sed -i "s|BHMASS|${M}|" params.txt
	sed -i "s|SNUMBER|${start_number}|" params.txt
	sed -i "s|ENUMBER|${end_number}|" params.txt
	sed -i "s|VARINDEX|${var_index}|" params.txt
	sed -i "s|LINLOG|${lin_or_log}|" params.txt
	sed -i "s|PLOTINTERVAL|${plot_interval}|" params.txt
	sed -i "s|MINRADIUS|${min_radius}|" params.txt
	sed -i "s|MAXRADIUS|${max_radius}|" params.txt
	sed -i "s|NRADII|${nradii}|" params.txt
	sed -i "s|NPHI|${nphi}|" params.txt
	sed -i "s|NTHETA|${ntheta}|" params.txt
	sed -i "s|SUFFIX|${suffix}|" params.txt

	# half box or full box?
        if (( $(echo "$Al > 0.0" |bc -l) )); then
                echo "Al = $Al so full box"
                sed -i "s|NSPACE3|128|" params.txt
                sed -i "s|CENTERZ|512.0|" params.txt
                sed -i "s|ZBOUND|3|" params.txt
		sed -i "s|THETAMAX|2.0|" params.txt
        else
            	echo "Al = $Al so half box"
                sed -i "s|NSPACE3|64|" params.txt
                sed -i "s|CENTERZ|0.0|" params.txt
                sed -i "s|ZBOUND|2|" params.txt
		sed -i "s|THETAMAX|${theta_max}|" params.txt
        fi
	sbatch slurm_submit
	#
	cd ${work_dir}
done	
