#!/bin/bash

module load ffmpeg-4.1-gcc-5.4.0-cbapykp

name=l0_m0_mu1_compare_a_r_star_phi_profile
analysis_dir=/home/dc-bamb1/GRChombo/Analysis

cd plots/${name}_movie

ffmpeg -framerate 12 -i frame_%06d.png -c:v mpeg4 -vb 8000k ${analysis_dir}/movies/${name}_movie.mp4

cd ${analysis_dir}
