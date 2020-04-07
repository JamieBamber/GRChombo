#!/bin/bash

module load ffmpeg-4.1-gcc-5.4.0-cbapykp

name=phi_a\=l\=0_IsoKerr_vs_KerrSchild
analysis_dir=/home/dc-bamb1/GRChombo/Analysis

cd plots/${name}_movie

ffmpeg -framerate 3 -i frame_%06d.png -c:v mpeg4 -vb 5000k ${analysis_dir}/movies/${name}_movie.mp4

cd ${analysis_dir}
