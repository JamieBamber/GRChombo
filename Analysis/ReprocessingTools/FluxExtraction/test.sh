#!/bin/bash

string=run101_a0.7_Al0_end

bh_spin=$(echo $string | sed -e 's/.*_a\(.*\)_Al.*/\1/')
echo $string
min_radius=$(echo "scale=5; 1.00 + sqrt(1 - ${bh_spin} * ${bh_spin})" | bc)
echo "min_radius = " ${min_radius}


