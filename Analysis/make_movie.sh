#!/bin/bash

#module load ffmpeg-4.1-gcc-5.4.0-cbapykp

variable=rho
subdir=run0005
name=BBH_${subdir}_${variable}
#analysis_dir=/home/dc-bamb1/GRChombo/Analysis
analysis_dir=~/GRChombo/Analysis

cd plots/Binary_BH/BBH_${subdir}/BBH_${subdir}_${variable}_movie
echo "making ${name}_movie"

#ffmpeg -framerate 3 -i frame_%06d.png -c:v mpeg4 -vb 5000k ${analysis_dir}/movies/${name}_movie.mp4
output_path=${analysis_dir}/movies/${name}_movie.mp4
ffmpeg -f image2 -framerate 12 -i BBH_movie_%06d.png -c:v libx264 -crf 22 -pix_fmt yuv420p ${output_path}

cd ${analysis_dir}
echo "movie saved as ${output_path}"
