#!/bin/bash
#
# this copy is for the Skylake nodes

work_dir=/home/dc-bamb1/GRChombo/Analysis/ReprocessingTools/VolumeIntegral_KerrSchild

start_number=0
end_number=2000
lin_or_log=1 # note 0 = log, 1 = linear
plot_interval=10
max_radius=450

subdirs=(
	run0101_l1_m1_a0.7_Al0_mu0.4_M1_KerrSchild
	run0102_l2_m2_a0.7_Al0_mu0.4_M1_KerrSchild
	run0103_l0_m0_a0.7_Al0_mu0.4_M1_KerrSchild
	run0105_l1_m-1_a0.7_Al0_mu0.4_M1_KerrSchild
	run0109_l2_m2_a0.7_Al0_mu0.8_M1_KerrSchild
)

#	run0102_l2_m2_a0.7_Al0_mu0.4_M1_KerrSchild
#	run0103_l0_m0_a0.7_Al0_mu0.4_M1_KerrSchild
#	run0104_l4_m4_a0.7_Al0_mu0.4_M1_KerrSchild
#	run0105_l1_m-1_a0.7_Al0_mu0.4_M1_KerrSchild
#	run0106_l8_m8_a0.7_Al0_mu0.4_M1_KerrSchild
#	run0107_l1_m1_a0.99_Al0_mu0.4_M1_KerrSchild
#	run0108_l1_m1_a0_Al0_mu0.4_M1_KerrSchild
#	run0109_l2_m2_a0.7_Al0_mu0.8_M1_KerrSchild

## loop over subdirs
for subdir in "${subdirs[@]}"; do
	bh_spin=$(echo $subdir | sed -e 's/.*_a\(.*\)_Al.*/\1/')
	bh_mass=$(echo $subdir | sed -e 's/.*_M\(.*\)_Kerr.*/\1/')
	#var_index=5
	# note vars = {chi phi Pi rho rho_azimuth J_rKS J_azimuth_rKS J_R J_azimuth_R}
	min_radius=$(echo "scale=5; 1.00 + sqrt(1 - ${bh_spin} * ${bh_spin})" | bc)
	#min_radius=2.1
	echo "min_radius = " ${min_radius}

	# suffix
	suffix=_in_r_plus_to_${max_radius}
	#_in_r${min_radius}_to_${max_radius}

	# extract parameters from params.txt
	name=${subdir}_mass_ang_mom_integral_r_between_${min_radius}_${max_radius}
	echo ${name} "volume integral"
	new_dir_path=outputs/${name}
	#
	mkdir -p ${new_dir_path}
	
	cp slurm_submit_Skylake ${new_dir_path}/slurm_submit
	cp params.txt ${new_dir_path}/params.txt
	
	cd ${new_dir_path}
	# add the location of the new directory to the params file
	sed -i "s|SUBDIR|${subdir}|" params.txt
	sed -i "s|BHSPIN|${bh_spin}|" params.txt
	sed -i "s|BHMASS|${bh_mass}|" params.txt
	sed -i "s|SNUMBER|${start_number}|" params.txt
	sed -i "s|ENUMBER|${end_number}|" params.txt
	sed -i "s|MINRADIUS|${min_radius}|" params.txt
	sed -i "s|MAXRADIUS|${max_radius}|" params.txt
	sed -i "s|PLOTINTERVAL|${plot_interval}|" params.txt
	sed -i "s|SFIX|${suffix}|" params.txt
	sbatch slurm_submit
	#
	cd ${work_dir}
done	
