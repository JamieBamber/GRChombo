#!/bin/bash
#
# this copy is for the Skylake nodes

work_dir=/home/dc-bamb1/GRChombo/Analysis/ReprocessingTools/FluxExtraction_KerrSchild

subdir=run0101_KNL_l1_m1_a0.7_Al0_mu0.4_M1_KerrSchild
start_number=0
end_number=1005
bh_spin=0.7
bh_mass=1

# extract parameters from params.txt
name=${subdir}_start_number${start_number}
echo ${name} "flux extraction"
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
sbatch slurm_submit
#
cd ${work_dir}

