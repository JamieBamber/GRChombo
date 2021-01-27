#!/bin/bash
#
# this copy is for the Skylake nodes

work_dir=/p/home/jusers/bamber1/juwels/GRChombo/Analysis/ReprocessingTools/FluxExtraction_GR_BBH

start_number=0
end_number=10000
resume=0 # resume previous extraction?

nphi=36
ntheta=24
extraction_radius=50
L=512
N1=64
box_size=16
plot_interval=10

data_directory=/p/project/pra116/bamber1/BinaryBHScalarField

# specify the input params for each run I want to submit
# list for each is: mu, delay, dt, G, BH mass ratio

# list for each is: mu, delay, dt, G, BH mass ratio                                                                                                                                                

run0011=(1 0 0.0625 0 1)
run0012=(1 10000 0.0625 0 1)
run0013=(0.08187607564 0 0.25 0 1)
run0014=(1 0 0.0625 0 2)
run0015=(1 10000 0.0625 0 2)
run0016=(0.5 0 0.25 0 1)
run0017=(0.5 10000 0.25 0 1)
run0018=(0.5 0 0.25 0.000001 1)

params_file=params.txt

run_list=(
    run0011
#    run0012
#    run0013
#    run0014
#    run0015
#    run0016
#    run0017
#    run0018
)

#subdir_list=(
#run0011_mu1_delay0_G0_ratio1
#run0012_mu1_delay10000_G0_ratio1
#run0013_mu0.08187607564_delay0_G0_ratio1
#run0014_mu1_delay0_G0_ratio2
#run0015_mu1_delay10000_G0_ratio2
#run0016_mu0.5_delay0_G0_ratio1
#run0017_mu0.5_delay10000_G0_ratio1
#run0018_mu0.5_delay0_G0.000001_ratio1
#)

for run in "${run_list[@]}"
do
  	cd $work_dir
	# extract parameters                                                                                                                                                                      
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
        new_dir_path=/p/scratch/pra116/bamber1/ReprocessingTools_outputs/FluxExtraction_GR_BBH/${name}
        #
	mkdir -p ${new_dir_path}
        
       	cp slurm_submit_juwels ${new_dir_path}/slurm_submit
        cp params.txt ${new_dir_path}
        
       	cd ${new_dir_path}
        # add the location of the new directory to the params file
        sed -i "s|JOBNAME|${run}FE|" slurm_submit
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

