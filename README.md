# opynions
### Developed for the Echo Chambers project - A package for exploring the parameter space of the Rewiring Unbounded Confidence Model (RUCM) ###

### Our goal ###
This project builds on the findings of Del Vicario et al. (2017). The goal of the project was to implement the Rewirining Unbounded Confidence Model (RUCM) on a Network and study the final distributions of opinions. The study was particularly focused on studying the phase lines between unimodal, bimodal, and multimodal distributions of opinions using four metrics: variance, number of disconnected nodes, opinion similarity, and modularity. The hypothesis of the project was that similar phase lines would be observed when using other metrics. 

### Technical details ####
The parameters for all experiments have been 2000 nodes over 100 timesteps (each timestep every node is updated in random order). We studied parameter space for mu and epsilon in [0,0.5]. Results were averaged over 5 runs. Pytest for this project is implemented and it is working. There are assert lines implemented in the code (excluding deprecated folder). The repository is structured as a module with a setup.py file. 

### References: ###
[1] Del Vicario, M., Scala, A., Caldarelli, G., Stanley, H. E., & Quattrociocchi, W. (2017). Modeling confirmation bias and polarization. Scientific Reports, 7(1), 40391. https://doi.org/10.1038/srep40391
[2] Github repo for a BCM implementiation in python: https://github.com/Gunner62/PolarizationModel
[3] Kan, U., Feng, M., & Porter, M. A. (2022). An adaptive bounded-confidence model of opinion dynamics on networks. arXiv. https://arxiv.org/abs/2112.05856
