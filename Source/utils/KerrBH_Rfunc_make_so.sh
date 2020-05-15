#!/bin/bash
current_dir=$(pwd)
utils_dir=/home/dc-bamb1/GRChombo/Source/utils
cd ${utils_dir}
rm KerrBH_Rfunc_lib.so KerrBH_Rfunc.o 
mv KerrBH_Rfunc.cpp.txt KerrBH_Rfunc.cpp
make KerrBH_Rfunc
icpc -shared -o KerrBH_Rfunc_lib.so KerrBH_Rfunc.o 
mv KerrBH_Rfunc.cpp KerrBH_Rfunc.cpp.txt
cd ${current_dir}
