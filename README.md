# opynions
### Echo Chambers project - A package for exploring the parameter space of the Rewiring Unbounded Confidence Model (RUCM) ###

### Our goal ###
This project builds on the findings of Del Vicario et al. (2017). The goal of the project was to implement the Rewiring Unbounded Confidence Model (RUCM) on a Network and study the final distributions of opinions. The study was particularly focused on studying the phase lines between unimodal, bimodal, and multimodal distributions of opinions using four metrics: variance, number of disconnected nodes, opinion similarity, and modularity. The hypothesis of the project was that similar phase lines would be observed when using other metrics. 

<div align="center">
  <img src="https://github.com/user-attachments/assets/3d59234e-90a0-4e84-91c5-c6c25530c4e2" alt="FIRST_g_e12_m3" width="400">
</div>

### Authors ###
- Sanda Mura
- Matijs Verloo
- Karolina Chlopicka
- Rory Guliker

### Project structure ###
- `data/.`: Directory containing data generated for heatmaps visualisation.
- `slide/echo_chambers_presentation.pdf`: Presentation slides.
- `opynions/code`
  - `simulation.py`: Contains functions to run a simulation.
  - `utils.py`: Functions for accessing simulation results, plotting the network and distribution of final opinions.
- `opynions/analysis`
  - `utils.py`: Utility functions for data handling and plotting.
  - `similarity.py`: Functions for analyzing the similarity of opinions between neighbors in a graph.
  - `multiprocessing.py`: Multiprocessing functions for generating dicts with data. 
  - `modularity.py`: Functions for analyzing the number of communities and modularity of graphs.
  - `isolation.py`: Functions for analysis of disconnected nodes in the network.
  - `distribution.py`: Functions for analysis of opinion distribution in the network.
  - `combined.py`: All-in-one analysis function derived from the other analysis functions.
- `opynions/demo.py`: Functions for demonstrating the package.
- `opynions/settings.py`: The constants used when creating results shown in the presentation.
- `results/figures/.`: Results of the experiments - figures.
- `test/.`: Unit tests for implemented functions.
- `docs/.`: All auto-generated documentation for the functions and description of model design. 
- `depreciated/.`: All depreciated files.

### Bonuses for grading ###
- Pytest for this project is implemented and it is working. (Github workflow auto-testing as well).
- There are assert lines implemented in the code (excluding deprecated folder).
- The project is structured as a module and `pip install` works.
- Auto-generated docs are available in the docs folder, `run/host index.html` to see them.

### References: ###
[1] Del Vicario, M., Scala, A., Caldarelli, G., Stanley, H. E., & Quattrociocchi, W. (2017). Modeling confirmation bias and polarization. Scientific Reports, 7(1), 40391. https://doi.org/10.1038/srep40391 <br />
[2] Github repo for a BCM implementiation in python: https://github.com/Gunner62/PolarizationModel <br />
[3] Kan, U., Feng, M., & Porter, M. A. (2022). An adaptive bounded-confidence model of opinion dynamics on networks. arXiv. https://arxiv.org/abs/2112.05856 <br />

### License ###
This project is licensed under the MIT License - see the LICENSE.md file for details.
