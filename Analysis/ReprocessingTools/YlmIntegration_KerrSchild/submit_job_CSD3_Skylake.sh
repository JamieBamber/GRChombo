#!/bin/bash
#
# this copy is for the KNL nodes

work_dir=/home/dc-bamb1/GRChombo/Analysis/ReprocessingTools/YlmIntegration_KerrSchild

# new vars = chi phi Pi rho rho_azimuth J_rKS J_azimuth_rKS J_R J_azimuth_R
# old vars = phi Pi chi rho J_azimuth J_r	or possibly 	phi Pi chi rho J_azimuth J_r J_azimuth_r
var_index=0
start_number=1085
end_number=1085
lin_or_log=1 # note 0 = log, 1 = linear
max_radius=200

subdirs=(
	run0080_KNL_l1_m1_a0_Al0_mu0.4_M1_KerrSchild
)

#	run0071_KNL_l1_m1_a0.99_Al0_mu0.4_M1_KerrSchild
#	 run0079_KNL_l0_m0_a0.7_Al0_mu1_M1_KerrSchild



## loop over subdirs
for subdir in "${subdirs[@]}"; do
	bh_spin=$(echo $subdir | sed -e 's/.*_a\(.*\)_Al.*/\1/')
	bh_mass=$(echo $subdir | sed -e 's/.*_M\(.*\)_Kerr.*/\1/')
	#var_index=5
	# note vars = {chi phi Pi rho rho_azimuth J_rKS J_azimuth_rKS J_R J_azimuth_R}
	min_radius=$(echo "scale=5; 1.00 + sqrt(1 - ${bh_spin} * ${bh_spin})" | bc)
	echo "min_radius = " ${min_radius}
	
	# extract parameters from params.txt
	name=${subdir}_linlog${lin_or_log}_var${var_index}_n${start_number}
	echo ${name} "Y00 Integration"
	new_dir_path=outputs/${name}
	#
	mkdir -p ${new_dir_path}
	
	cp slurm_submit_Skylake ${new_dir_path}/slurm_submit
	cp params.txt ${new_dir_path}
	
	cd ${new_dir_path}
	# add the location of the new directory to the params file
	sed -i "s|SUBDIR|${subdir}|" params.txt
	sed -i "s|BHSPIN|${bh_spin}|" params.txt
	sed -i "s|BHMASS|${bh_mass}|" params.txt
	sed -i "s|SNUMBER|${start_number}|" params.txt
	sed -i "s|ENUMBER|${end_number}|" params.txt
	sed -i "s|VARINDEX|${var_index}|" params.txt
	sed -i "s|LINLOG|${lin_or_log}|" params.txt
	sed -i "s|MINRADIUS|${min_radius}|" params.txt
	sed -i "s|MAXRADIUS|${max_radius}|" params.txt
	sbatch slurm_submit
	#
	cd ${work_dir}
done	
