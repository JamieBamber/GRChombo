#!/bin/bash

python_script=rho_movie_plot_script.py

work_dir=$(pwd)

cp slurm_submit_visit_supermuc outputs/slurm_submit
cp ${python_script} outputs/python_script.py

cd outputs
sbatch slurm_submit

echo "running ${python_script} in batch mode"

cd ${work_dir}



