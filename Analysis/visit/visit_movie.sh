#!/bin/bash
module load visit
visit -movie -format mpeg -fps 12 -start 0 -end 597 -geometry 800x800 -scriptfile rho_movie_plot_script.py -framestep 1 -output run0001_rho_movie.mpg 

