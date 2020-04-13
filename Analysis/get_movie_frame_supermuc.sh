#!/bin/bash

frame_dir=BBH_SF_rho_movie_run0004
frame_num=60
echo "start scp"
# scp di76bej@skx.supermuc.lrz.de:
scp supermuc:~/GRChombo/GRChombo/Analysis/visit/${frame_dir}/BBH_SF_movie_$(printf "%06d" ${frame_num}).png ${frame_dir}_$(printf "%06d" ${frame_num}).png
