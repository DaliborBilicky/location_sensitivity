# Testing location optimal solution sensitivity

## Table of Contents

- [Description](#description)
  - [Goals of the project](#goals-of-the-project)
- [Download and install](#download-and-install)
  - [Python interpreter](#python-interpreter)
  - [Cloning the repo](#cloning-the-repo)
  - [Installing libraries](#installing-libraries)
- [Usage](#usage)
  - [Arguments](#arguments)
  - [Example](#example)
- [Output](#output)
  - [Example snippet](#example-snippet)

## Description

The **weighted p-median** and **weighted p-center** are facility location 
problems with significant applications in operations research. They are 
commonly used for placing facilities such as ambulance stations, hospitals, 
fire stations, or warehouses within a given region.

The main objective of this project is to **analyze the sensitivity** of the 
optimal solutions of the weighted p-median and weighted p-center problems when 
certain **input parameters of the transportation network (graph)** are modified.

### Goals of the project:

1. **Implement an appropriate algorithm** capable of finding an optimal 
solution for the weighted p-median or weighted p-center problem.
2. **Program mathematical expressions** modeling changes in the input 
parameters of the given graph.
3. **Test and evaluate** these models on small and medium-sized graphs.

## Download and install

### Python interpreter

Need to have installed python. Newest version is the best choice. I was working
on 3.13.2.

### Cloning the repo

```bash
git clone https://github.com/DaliborBilicky/location_sensitivity.git
```

### Installing libraries

**Note:** I recommend creating a virtual environment and than installing the 
libraries

[Tutorial how to make virtual environment](https://docs.python.org/3/tutorial/venv.html)

```bash
pip install -r requirements.txt
```

### Usage

To start the application, open your terminal and run the following command:

```bash
python src/main.py <option> <region acronym> <P>
```

#### Arguments

- `<option>`  
  Type of experiment to run:
  - `A` – Tests how the optimal solution changes as the sensitivity parameter `k` increases.
  - `F` – Finds the first value of `k` where the optimal solution changes.

- `<region acronym>`  
  Region to run the experiment on. Choose one of the following Slovak region acronyms:
  - `BA` – Bratislava  
  - `TT` – Trnava  
  - `NR` – Nitra  
  - `TN` – Trenčín  
  - `ZA` – Žilina  
  - `BB` – Banská Bystrica  
  - `PO` – Prešov  
  - `KE` – Košice

- `<P>`  
  The number of facilities to locate (e.g., ambulance or fire stations).

---

#### Example

```bash
python src/main.py A ZA 12
```

### Output

All result files are saved in the `./results/` directory.
The output is stored in files with the following names:

- `<region acronym>-<P>-calculate-all-ks.txt`
- `<region acronym>-<P>-calculate-first-k.txt`

Each file contains comprehensive statistics for a given region and sensitivity 
parameter `k`. The output includes:

- **Sensitivity parameter `k`** and its **upper limit**
- **Selected p-medians** (indices of optimal facility locations)
- **Speed statistics**:
  - Speed of ambulance
  - Minimum / Maximum / Average / Most frequent speed decline (km/h)
- **Top 10 smallest and largest speed declines** with details on:
  - Edge (node-node pair)
  - Original and elongated edge cost
- **Edges connected to selected p-medians** with their respective speed declines

#### Example snippet:

```text
k: 6.9357, upper limit: 44.3887
Weighted p-medians:
[6, 15, 18, 33, 44, 49, 50, 51, 77, 78, 82, 83, 84, 85, 113]
Speed of ambulance: 110
Min speed decline: 0.8961
Max speed decline: 17.2290
Average speed decline: 3.4149
Most often speed decline: 2.5460
```

Each run produces similar structured statistics, either:
- For a **single** value of `k`, or
- For **multiple values** in a loop (e.g. all `k` from 0 to the upper bound)

This makes the results easily traceable, comparable, and ready for further 
analysis or visualization.
