# BL7011
Analysis scripts for the beam line endstation 7.0.1.1 at the Advanced Light Source

## Installation 

Follow the steps below to set up the environment and install the necessary packages.

### Step 1: Install Anaconda/Miniconda

If you don't already have Anaconda or Miniconda installed, you can download and install them from the following links:

- [Anaconda](https://www.anaconda.com/products/individual)
- [Miniconda](https://docs.conda.io/en/latest/miniconda.html)

### Step 2: Create and Activate Conda Environment

Open a terminal or command prompt and create a new conda environment with the desired name (e.g., `BL7011`):

```sh
conda create -n BL7011 python=3.12
conda activate BL7011
```

### Step 3: Install Dependencies

Install the required dependencies using the requirements.txt file:

```sh
conda install --file requirements.txt -c conda-forge
```

### Step 4: Install the Main `BL7011` Package

You can install the main `BL7011` package using `pip` by first navigating into the folder with the `setup.py` file. There are two modes of installation:

#### Regular Installation

For a regular installation, use the following command:

```sh
pip install . --no-deps
```

#### Developer Mode

If you are planning to develop or modify the package, install it in developer mode:

```sh
pip install -e . --no-deps
```

See `environment_example.yml` for reference.


# Copyright Notice

BL7011 Copyright (c) 2026, The Regents of the University of California, through Lawrence Berkeley National Laboratory (subject to receipt of any required approvals from the U.S. Dept. of Energy) and Massachusetts Institute of Technology. All rights reserved.

If you have questions about your rights to use or distribute this software, please contact Berkeley Lab's Intellectual Property Office at IPO@lbl.gov.

NOTICE.  This Software was developed under funding from the U.S. Department of Energy and the U.S. Government consequently retains certain rights.  As such, the U.S. Government has been granted for itself and others acting on its behalf a paid-up, nonexclusive, irrevocable, worldwide license in the Software to reproduce, distribute copies to the public, prepare derivative  works, and perform publicly and display publicly, and to permit others to do so.

