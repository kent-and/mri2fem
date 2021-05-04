

# 1800 s   = 30 min
# 32400 s  = 9 hours 

python3 analytical_1D.py


python3 diffusion_1D.py  --L_max 50  --Ns 10 20 40 80 --dt 300 --final_time 1800 --lumped not --check_point 0.1
python3 diffusion_1D.py  --L_max 50  --Ns 10 20 40 80 --dt 300 --final_time 1800 --lumped lumped --check_point 0.1
python3 diffusion_1D.py  --L_max 50  --Ns 10 20 40 80 --dt 300 --final_time 32400 --lumped not --check_point 0.1
python3 diffusion_1D.py  --L_max 50  --Ns 10 20 40 80 --dt 300 --final_time 32400 --lumped lumped --check_point 0.1


