#!/bin/bash
rsync -avh supermuc:~/GRChombo/GRChombo/ ~/GRChombo_supermuc --exclude={'.git'} --exclude-from='/Users/Jamie/GRChombo_supermuc/.gitignore' 
