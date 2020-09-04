#!/bin/bash
#
# this copy is for the Skylake nodes

work_dir=/home/dc-bamb1/GRChombo/Analysis/ReprocessingTools/FluxExtraction_KerrSchild

start_number=0
end_number=20000
lin_or_log=1 # note 0 = log, 1 = linear

nphi=64
ntheta=64
theta_max=0.99
max_radius=500

# specify the input params for each run I want to submit
# list for each is: l, m, a, Al, mu, dt
# test adding spin
run0101=(0 0 0.0 0 0.4 0.0625)
run0102=(0 0 0.7 0 0.4 0.0625)
run0103=(0 0 0.99 0 0.4 0.0625)
# same for l=m=1
run0104=(1 1 0.0 0 0.4 0.0625)
run0105=(1 1 0.7 0 0.4 0.0625)
run0106=(1 1 0.99 0 0.4 0.0625)
# test lm
run0107=(2 2 0.7 0 0.4 0.0625)
run0108=(4 4 0.7 0 0.4 0.0625)
run0109=(1 -1 0.7 0 0.4 0.0625)
run0110=(8 8 0.7 0 0.4 0.0625)
# test effect of mu
# run0111=(0 0 0.0 0 0.05 0.4)
run0112=(1 1 0.7 0 0.2 0.0625)
run0113=(1 1 0.7 0 0.8 0.03125)
run0114=(1 1 0.7 0 0.1 0.0625)
# test effect of m / mu ratio
run0119=(2 2 0.7 0 0.8 0.03125)
run0115=(8 8 0.7 0 3.2 0.0078125)
# test effect of alignment
run0116=(1 1 0.7 0.5 0.4 0.0625)
run0117=(1 -1 0.99 0 0.4 0.0625)
run0118=(1 1 0.99 0.5 0.4 0.0625)

plot_interval=5
#var_index=6

# specify runs to submit
run_list=(
       run0105
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
        subdir=${run}_l${l}_m${m}_a${a}_Al${Al}_mu${mu}_M${M}_KerrSchild_N256

	# note vars = {phi Pi chi rho rho_azimuth J_rKS J_azimuth_rKS J_R J_azimuth_R}
	min_radius=$(echo "scale=5; ${M}*(1.00 + sqrt(1 - ${a} * ${a}))" | bc)
	#min_radius=5
	echo "mu = " ${mu}
	echo "min_radius = " ${min_radius}
	
	suffix=_r_plus_to_${max_radius}_nphi${nphi}_ntheta${ntheta}_theta_max${theta_max}
	#suffix=_${min_radius}_to_${max_radius}_nphi${nphi}_ntheta${ntheta}_theta_max${theta_max}

	#dt_mult=$(echo "scale=5; 0.025 / ${mu}" | bc | sed 's/^\./0./')
	echo "dt_multiplier = " ${dt_mult}

	name=${subdir}_var${var_index}_flux${suffix}
	echo ${name} "flux extraction"
	new_dir_path=outputs/${name}
	#
	mkdir -p ${new_dir_path}
	
	cp slurm_submit_Skylake ${new_dir_path}/slurm_submit
	cp params.txt ${new_dir_path}
	
	cd ${new_dir_path}
	# add the location of the new directory to the params file
	sed -i "s|JOBNAME|${run}FE|" slurm_submit
	sed -i "s|DTMULT|${dt_mult}|" params.txt
	sed -i "s|SUBDIR|${subdir}|" params.txt
	sed -i "s|BHSPIN|${a}|" params.txt
	sed -i "s|BHMASS|${M}|" params.txt
	sed -i "s|SNUMBER|${start_number}|" params.txt
	sed -i "s|ENUMBER|${end_number}|" params.txt
	sed -i "s|VARINDEX|${var_index}|" params.txt
	sed -i "s|LINLOG|${lin_or_log}|" params.txt
	sed -i "s|PLOTINTERVAL|${plot_interval}|" params.txt
	sed -i "s|MINRADIUS|${min_radius}|" params.txt
	sed -i "s|MAXRADIUS|${max_radius}|" params.txt
	sed -i "s|NPHI|${nphi}|" params.txt
	sed -i "s|NTHETA|${ntheta}|" params.txt
	sed -i "s|SUFFIX|${suffix}|" params.txt

	# half box or full box?
        if (( $(echo "$Al > 0.0" |bc -l) )); then
                echo "Al = $Al so full box"
                sed -i "s|NSPACE3|256|" params.txt
                sed -i "s|CENTERZ|512.0|" params.txt
                sed -i "s|ZBOUND|3|" params.txt
		sed -i "s|THETAMAX|2.0|" params.txt
        else
            	echo "Al = $Al so half box"
                sed -i "s|NSPACE3|128|" params.txt
                sed -i "s|CENTERZ|0.0|" params.txt
                sed -i "s|ZBOUND|2|" params.txt
		sed -i "s|THETAMAX|${theta_max}|" params.txt
        fi
	sbatch slurm_submit
	#
	cd ${work_dir}
done	
