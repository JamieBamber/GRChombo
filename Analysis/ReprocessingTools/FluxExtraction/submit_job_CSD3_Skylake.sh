#!/bin/bash
#
# this copy is for the Skylake nodes

work_dir=/home/dc-bamb1/GRChombo/Analysis/ReprocessingTools/FluxExtraction

start_number=0
end_number=2000
lin_or_log=1 # note 0 = log, 1 = linear

nphi=32
ntheta=32
theta_max=0.98
max_radius=500

subdirs=(
	run0001_l1_m1_a0.7_Al0_mu0.4_M1_IsoKerr
)

# run0001_l1_m1_a0.7_Al0_mu0.4_M1_IsoKerr
# run0002_l2_m2_a0.7_Al0_mu0.4_M1_IsoKerr
# run0003_l0_m0_a0.7_Al0_mu0.4_M1_IsoKerr
# run0004_l4_m4_a0.7_Al0_mu0.4_M1_IsoKerr
# run0005_l1_m-1_a0.7_Al0_mu0.4_M1_IsoKerr

## loop over subdirs
for subdir in "${subdirs[@]}"; do
	bh_spin=$(echo $subdir | sed -e 's/.*_a\(.*\)_Al.*/\1/')
	bh_mass=$(echo $subdir | sed -e 's/.*_M\(.*\)_Kerr.*/\1/')
	mu=$(echo $subdir | sed -e 's/.*_mu\(.*\)_M.*/\1/')

	# note vars = {phi Pi chi rho rho_azimuth J_rKS J_azimuth_rKS J_R J_azimuth_R}
	#min_radius=$(echo "scale=5; 1.00 + sqrt(1 - ${bh_spin} * ${bh_spin})" | bc)
	min_radius=5
	echo "mu = " ${mu}
	echo "min_radius = " ${min_radius}
	
	suffix=min_R${min_radius}_max_R${max_radius}_nphi${nphi}_ntheta${ntheta}_theta_max${theta_max}

	dt_mult=$(echo "scale=5; 0.025 / ${mu}" | bc | sed 's/^\./0./')
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
	sed -i "s|DTMULT|${dt_mult}|" params.txt
	sed -i "s|SUBDIR|${subdir}|" params.txt
	sed -i "s|BHSPIN|${bh_spin}|" params.txt
	sed -i "s|BHMASS|${bh_mass}|" params.txt
	sed -i "s|SNUMBER|${start_number}|" params.txt
	sed -i "s|ENUMBER|${end_number}|" params.txt
	sed -i "s|VARINDEX|${var_index}|" params.txt
	sed -i "s|LINLOG|${lin_or_log}|" params.txt
	sed -i "s|MINRADIUS|${min_radius}|" params.txt
	sed -i "s|MAXRADIUS|${max_radius}|" params.txt
	sed -i "s|NPHI|${nphi}|" params.txt
	sed -i "s|NTHETA|${ntheta}|" params.txt
	sed -i "s|SUFFIX|${suffix}|" params.txt
	sed -i "s|THETAMAX|${theta_max}|" params.txt
	sbatch slurm_submit
	#
	cd ${work_dir}
done	
