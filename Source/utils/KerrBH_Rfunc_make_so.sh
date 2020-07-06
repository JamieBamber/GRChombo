#!/bin/bash
load $WORK_DIR/SupermucNG_modules.sh
current_dir=$(pwd)
utils_dir=/dss/dsshome1/04/di76bej/GRChombo/GRChombo/Source/utils
cd ${utils_dir}
rm KerrBH_Rfunc_lib.so KerrBH_Rfunc.o 
mv KerrBH_Rfunc.cpp.txt KerrBH_Rfunc.cpp
make KerrBH_Rfunc
icpc -shared -o KerrBH_Rfunc_lib.so KerrBH_Rfunc.o 
mv KerrBH_Rfunc.cpp KerrBH_Rfunc.cpp.txt
cd ${current_dir}
