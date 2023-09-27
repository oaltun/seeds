# mkdir -p ~/opt/miniconda3
# wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh -O ~/opt/miniconda3/miniconda.sh
# bash ~/opt/miniconda3/miniconda.sh -b -u -p ~/opt/miniconda3
# rm -rf ~/opt/miniconda3/miniconda.sh

conda env create -f conda_environment.yml -p ./.condaenv
