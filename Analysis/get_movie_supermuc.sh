#!/bin/bash
variable=rho
name=l0_m0_mu1_compare_a_r_star_phi_profile_movie.mp4
echo "start scp"
# scp di76bej@skx.supermuc.lrz.de:
scp supermuc:~/GRChombo/GRChombo/Analysis/visit/${name} ~/GRChombo/Analysis/movies/${name}
