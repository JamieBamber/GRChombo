#!/bin/bash
variable=rho
name=run0001_rho_movie.mpg
echo "start scp"
# scp di76bej@skx.supermuc.lrz.de:
scp supermuc:~/GRChombo/GRChombo/Analysis/visit/${name} ~/GRChombo/Analysis/movies/${name}
