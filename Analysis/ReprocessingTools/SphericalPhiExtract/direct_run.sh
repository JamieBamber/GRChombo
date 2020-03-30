#!/bin/bash
work_dir=/home/dc-bamb1/GRChombo/Analysis/ReprocessingTools/SphericalPhiExtract
cd ${work_dir}/outputs/
mpirun -np 8 ${work_dir}/ReprocessingTool3d.Linux.64.mpicxx.ifort.OPTHIGH.MPI.OPENMPCC.ex ${work_dir}/params.txt
cd ${work_dir}
