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

---

## Introduction
High-Performance Computing (HPC) enables you to solve complex computational problems by using large clusters of processors and a GPU cluster. This manual serves as a guide to make the most out of your HPC experience at [HPC Ghent](https://login.hpc.ugent.be/).

## Getting Started
[HPC Ghent interactive sessions](https://login.hpc.ugent.be/pun/sys/dashboard/batch_connect/sessions) --> Jupyter Notebook. 
All scripts are liable to change due to system changes/updates. 

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
