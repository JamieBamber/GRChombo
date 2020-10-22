#!/bin/bash
#
# this copy is for the Skylake nodes

work_dir=/home/dc-bamb1/GRChombo/Analysis/ReprocessingTools/Y00Integration_KerrSchild

subdir=run0071_KNL_l1_m1_a0.99_Al0_mu0.4_M1_KerrSchild
start_number=0
end_number=1250
lin_or_log=1 # note 0 = log, 1 = linear
bh_spin=0.99
bh_mass=1
var_index=5
# note vars = {c_phi, c_Pi, c_chi, c_rho, c_J_azimuth, c_J_r}
min_radius=$(echo "scale=5; 1.001 + sqrt(1 - ${bh_spin} * ${bh_spin})" | bc)
echo "min_radius = " ${min_radius}

# extract parameters from params.txt
name=${subdir}_var${var_index}_linlog${lin_or_log}_start_number_${start_number}_KS
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
sbatch slurm_submit
#
cd ${work_dir}

