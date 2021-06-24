#!/bin/bash
load $WORK_DIR/Cosma-Durham.modules.sh
current_dir=$(pwd)
utils_dir=/cosma/home/dp174/dc-bamb1/GRChombo/Source/utils
cd ${utils_dir}
name=KerrBH_Rfunc_general_s
rm ${name}_lib.so ${name}.o 
mv ${name}.cpp.txt ${name}.cpp
make ${name}
icpc -shared -o ${name}.so ${name}.o 
mv ${name}.cpp ${name}.cpp.txt
cd ${current_dir}
