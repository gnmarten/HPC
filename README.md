# HPC for Dummies

Welcome to **HPC for Dummies**. This guide will walk you through accessing and using the HPC cluster efficiently. This repository is intended for people without a background in programming. In fact, there is a technical manual, but it may be bewildering for humanities people. 

## Table of Contents
1. [Introduction](#introduction)
2. [Getting Started](#getting-started)
3. [Accessing the HPC](#accessing-the-hpc)
4. [Basic HPC Commands](#basic-hpc-commands)
5. [Submitting Jobs](#submitting-jobs)
6. [Monitoring Jobs](#monitoring-jobs)
7. [Best Practices](#best-practices)
8. [Troubleshooting](#troubleshooting)
9. [Additional Resources](#additional-resources)
10. [Understanding the toolchains (it's complicated)](#toolchains)
---

## Introduction
High-Performance Computing (HPC) enables you to solve complex computational problems by using large clusters of processors and a GPU cluster. This manual serves as a guide to make the most out of your HPC experience at [HPC Ghent](https://login.hpc.ugent.be/).

## Getting Started
[HPC Ghent interactive sessions](https://login.hpc.ugent.be/pun/sys/dashboard/batch_connect/sessions) --> Access via a WebGUI. You can launch Jupyter Notebooks from here (restricted to 1 hour).  
Large jobs need to be committed via a script in SLURM format. All scripts are liable to change due to system changes/updates. 

## Basic hpc(-related) tools and commands
How to transfer files: you need to tunnel to the HPC via [WinSCP]() for Windows people. FileZilla is another option. In fact, SCP is built into macOS. 

## Navigating Disk Spaces

Using tunnel access, there are three main disk spaces that you need to navigate. Swap "vsc42730" for your own account.

- **`/kyukon/home/gent/427/vsc42730/`:**
  - Limited disk size.
  - Job reports will appear here, allowing you to troubleshoot your scripts.
  - Unless using my specific scripts, all files and modules loaded will be written to this drive, which can cause it to overflow rapidly.

- **`/kyukon/data/gent/427/vsc42730/`:**
  - Used for storage of clean data to be processed. This is not a backup server!

- **`/kyukon/scratch/gent/427/vsc42730/`:**
  - Used as a kind of "scratch memory" for temporary files. You can use WinSCP to "find" large cache memory files and delete them if needed.
 
## Understanding the toolchains (it's complicated)
```bash 
Lmod has detected the following error: A different version of the 'GCCcore'
module is already loaded (see output of 'ml').
You should load another 'GCC' module for that is compatible with the currently
loaded version of 'GCCcore'.
Use 'ml spider GCC' to get an overview of the available versions
```
This is a typical error that will pop up if you attempt to load incompatible modules. You can see in the following table the compatible toolchains (if they are in the same row, then they are compatible):
```bash
GCCcore-13.2.0  GCC-13.2.0                  gfbf-2023b/gompi-2023b   foss-2023b
GCCcore-13.2.0  intel-compilers-2023.2.1    iimkl-2023b/iimpi-2023b  intel-2023b
GCCcore-12.3.0  GCC-12.3.0                  gfbf-2023a/gompi-2023a   foss-2023a
GCCcore-12.3.0  intel-compilers-2023.1.0    iimkl-2023a/iimpi-2023a  intel-2023a
GCCcore-12.2.0  GCC-12.2.0                  gfbf-2022b/gompi-2022b   foss-2022b
GCCcore-12.2.0  intel-compilers-2022.2.1    iimkl-2022b/iimpi-2022b  intel-2022b
GCCcore-11.3.0  GCC-11.3.0                  gfbf-2022a/gompi-2022a   foss-2022a
GCCcore-11.3.0  intel-compilers-2022.1.0    iimkl-2022a/iimpi-2022a  intel-2022a
GCCcore-11.2.0  GCC-11.2.0                  gfbf-2021b/gompi-2021b   foss-2021b
GCCcore-11.2.0  intel-compilers-2021.4.0    iimkl-2021b/iimpi-2021b  intel-2021b
GCCcore-10.3.0  GCC-10.3.0                  gfbf-2021a/gompi-2021a   foss-2021a
GCCcore-10.3.0  intel-compilers-2021.2.0    iimkl-2021a/iimpi-2021a  intel-2021a
GCCcore-10.2.0  GCC-10.2.0                  gfbf-2020b/gompi-2020b   foss-2020b
GCCcore-10.2.0  iccifort-2020.4.304         iimkl-2020b/iimpi-2020b  intel-2020b
```
So if you want to use 
```bash
module load PyTorch-Lightning/1.8.4-foss-2022a-CUDA-11.7.0 
module load PyTorch/1.12.0-foss-2022a-CUDA-11.7.0
```
then you need to select "Jupyter Notebook 6.4.0 GCCcore 11.3.0 IPython 8.5.0" in het WebGui, because "GCCcore-11.3.0" corresponds to "foss-2022a". Your options are determined by the cluster that you want to use. 
In order to find out what modules are available on what cluster, you need to access the command line (either in the WebGUI or via SSH) and look up as the error message indicates:
```bash
module spider PyTorch/
```
This will then show sth like
```bash
PyTorch/1.7.1-fosscuda-2020b
PyTorch/1.10.0-foss-2021a-CUDA-11.3.1
PyTorch/1.11.0-foss-2021a-CUDA-11.3.1
PyTorch/1.12.0-foss-2022a-CUDA-11.7.0
PyTorch/1.12.1-foss-2022a-CUDA-11.7.0
PyTorch/1.13.1-foss-2022a-CUDA-11.7.0
PyTorch/2.1.2-foss-2023a-CUDA-12.1.1
```
While the difference between torch 1 and 2 is huge (and mandated by the requirements of the script you need to run), it is not always necessary to look for exact correspondence in numbers. Higher numbers (eg CUDA 12.5) might be backwards compatible with CUDA 12.1.1. If the toolchain does not offer what you need, you can request it.

## Understanding the job file in .sh format

```bash
#!/bin/bash
#PBS -N x_jobname
#PBS -m ae
#PBS -l walltime=2:59:00
#PBS -l nodes=1:ppn=12:gpus=1
#PBS -l mem=50gb
```
This part sits on top. Despite it having been commented out, it is being read when committed via the CLI. The time it takes for your "job" to execute depends  on the values you enter here, e.g. walltime=2:59:00 is shorter than the default 7.59.00. The standard values are like this, but then it might takes days for your job to execute. 
```bash
#!/bin/bash
#PBS -N x_jobname
#PBS -m ae
#PBS -l walltime=7:59:00
#PBS -l nodes=1:ppn=32:gpus=1
#PBS -l mem=250gb
```
Continue as follows. Note that I created a directory python_packages on scratch in order to store user-specific packages. Generally, the HPC will know it's way around, but some locations need to be declared explicityly via "export". Remember to replace all mentions of "vsc42730" with your own login.
```bash
# Load required modules

module load foss/2023a
module load CUDA/12.1.1
module load cuDNN/8.9.2.26-CUDA-12.1.1
module load Python/3.11.3-GCCcore-12.3.0
module load PyTorch/2.1.2-foss-2023a
module load PyTorch-Lightning/2.1.3-foss-2023a
module load Transformers/4.39.3-gfbf-2023a

# Setup cache and install directories on scratch (keep your home drive from overflowing)
export XDG_CACHE_HOME=/kyukon/scratch/gent/427/vsc42730/cache
export PIP_CACHE_DIR=/kyukon/scratch/gent/427/vsc42730/pip_cache
export PYTHONUSERBASE=/kyukon/scratch/gent/427/vsc42730/python_packages
export PATH=$PYTHONUSERBASE/bin:$PATH
# Add the path to your local PyTorch CUDA libraries
export LD_LIBRARY_PATH=/kyukon/scratch/gent/427/vsc42730/python_packages/lib/python3.11/site-packages/torch/lib:$LD_LIBRARY_PATH

# Also add the CUDA libraries from the module
export LD_LIBRARY_PATH=/apps/gent/RHEL8/zen3-ampere-ib/software/CUDA/12.1.1/lib64:$LD_LIBRARY_PATH
export PYTHONPATH=/kyukon/scratch/gent/427/vsc42730/python_packages/lib/python3.11/site-packages:$PYTHONPATH

# Upgrade pip and resolve dependency issues
pip install --user --upgrade pip
pip install --user mlxtend numba whisperx 
pip install --user pyannote.audio --extra-index-url https://download.pytorch.org/whl/cu121 #very particular to the task I was implementing, you might not need this
#pip uninstall -y safetensors
#pip install --user safetensors #problem arises because of loading the transformers' specific version. Might be solved by loading another version.
#module list | grep cuda
#module show CUDA/12.1.1 #loading CUDA is tricky, use this for troubleshooting, it will show the location and availability

# Run the script
cd $VSC_HOME
python x.py

exit 0
```
The setup above is needed to run the Whisper transcription large model (3Gb) on large audio files. In other words, this setup is only needed if you need the equivalnet of a monster gaming PC with lots of CPU and GPU power. You only need this if you need to do the heavy lifting that your laptop or desktop does not allow for. Out of memory errors are due to the lack of RAM memory and GPU power (laptops only have 4GB or none).
