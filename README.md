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
