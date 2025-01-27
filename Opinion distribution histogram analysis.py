import utils
import UCM
import simulation
import distribution
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy.signal import find_peaks

# all_opinions, avg_histogram = utils.get_opinion_hist(5, 2000, 10, 0.4, 0.25)

# plt.figure(figsize=(10, 6))
# plt.bar(np.linspace(0, 1, len(avg_histogram)), avg_histogram, width=0.01, align='center')
# plt.xlabel('Opinion')
# plt.ylabel('Frequency')
# plt.grid()
# plt.show()

#print(all_opinions[1][1:10])
#print(type(all_opinions))

######## EXPERIMENT 1 ########
# set the parameter miu to 0.1. Calculate and generate the histogram for set values for both parameters.

# all_opinions, avg_histogram = utils.get_opinion_hist(5, 2000, 50, 0.2, 0.1)

# plt.figure(figsize=(10, 6))
# plt.bar(np.linspace(0, 1, len(avg_histogram)), avg_histogram, width=0.01, align='center')
# plt.xlabel('Opinion')
# plt.ylabel('Frequency')
# plt.grid()
# plt.show()

# all_opinions, avg_histogram = utils.get_opinion_hist(5, 2000, 50, 0.4, 0.1)

# plt.figure(figsize=(10, 6))
# plt.bar(np.linspace(0, 1, len(avg_histogram)), avg_histogram, width=0.01, align='center')
# plt.xlabel('Opinion')
# plt.ylabel('Frequency')
# plt.grid()
# plt.show()

####### EXPERIMENT 2 #########
# analise the histogram by calculating variance for the distribution. 
# Parameters: miu = 0.1, epsilon goes from 0 to 0.5 with 0.01 time-steps.

# variance_values = []
# epsilon_values = np.linspace(0,0.5,51)

# for i in epsilon_values:
#     var = distribution.opinions_variance(5,2000,10,i,0.3)
#     variance_values.append(var)


# plt.figure(figsize=(10, 6))
# plt.plot(epsilon_values, variance_values, color = "blue")
# plt.xlabel('Epsilon value')
# plt.ylabel('Variance of the distribution')
# plt.title('Variance for constant miu = 0.3 and changing epsilon value')
# plt.grid()
# plt.savefig("Variance for constant miu = 03 and changing epsilon value.jpeg")

####### EXPERIMENT 3 #########
#varing both parameters - heatmap of the variance

# variance_matrix = []

# epsilon_values = np.linspace(0,0.5,51)
# miu_values = np.linspace(0,0.5,51)

# for j in miu_values:
#     variance_values = []
#     for i in epsilon_values:
#         var = distribution.opinions_variance(5,2000,10,i,j)
#         variance_values.append(var)
#     variance_matrix.append(variance_values)

# variance_matrix = np.array(variance_matrix)

# plt.figure(figsize=(10, 8))
# plt.imshow(variance_matrix, extent=[0, 0.5, 0.5, 0], aspect='auto', cmap='viridis')
# plt.colorbar(label='Opinion Variance')
# plt.xlabel('Epsilon')
# plt.ylabel('Miu')
# plt.title('Heatmap of Opinion Variance')
# plt.show()


####### EXPERIMENT 4 #########
#counting peaks in the histogram 

# epsilon_values = np.linspace(0,0.5,51)
# number_peaks = []
# for i in epsilon_values:
#     all_opinions, avg_histogram = utils.get_opinion_hist(5, 2000, 50, i, 0.45)
#     peaks = distribution.count_peaks_in_histogram(avg_histogram, 30, 10)
#     number_peaks.append(peaks)

# plt.figure(figsize=(10, 6))
# plt.plot(epsilon_values, number_peaks, marker='o', color = "blue")
# plt.xlabel('Epsilon values')
# plt.ylabel('Number of peaks')
# plt.grid()
# plt.show()

####### EXPERIMENT 5 #########

# miu_values = np.linspace(0,0.5,51)
# number_excluded = []

# for i in miu_values:
#     all_opinions, avg_histogram, isolated = utils.get_opinion_hist(5, 2000, 50, 0.45, i)
#     number_excluded.append(isolated)

# plt.figure(figsize=(10, 6))
# plt.plot(miu_values, number_excluded, marker='o', color = "blue")
# plt.xlabel('Miu values')
# plt.ylabel('Number of isolated nodes')
# plt.grid()
# plt.show()

######## EXPERIMENT 6 #########
#generating data to heatmap - variance 

variance_matrix = [] 

epsilon_values = np.linspace(0, 0.5, 51)
miu_values = np.linspace(0, 0.5, 51)

for j in epsilon_values:
    variance_values = []
    for i in miu_values:
        var = distribution.opinions_variance(5, 2000, 10, j, i) 
        variance_values.append(var)
    variance_matrix.append(variance_values)

variance_matrix = np.array(variance_matrix)

#Saving to Data Frame 
df = pd.DataFrame(
    variance_matrix,
    index=[f"{epsilon:.2f}" for epsilon in epsilon_values],  # Rows - epsilon values
    columns=[f"{miu:.2f}" for miu in miu_values]  # Columns - miu values
)
df.index.name = "epsilon/mu"

# Saving to CSV
filename = "variance_heatmap_data.csv"
df.to_csv(filename)

print(f"Data saved to {filename}")