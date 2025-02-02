from opynions.plotting import create_heatmap_from_csv, plot_heatmap
import csv
import os

#create_heatmap_from_csv('raw_data/formod_comm_heatmaps.csv','avg_modularity','mu','epsilon','Modularity large groups')
plot_heatmap('raw_data/modularity_matrix.csv','Modularity small groups')
#create_heatmap_from_csv('raw_data/variance_heatmap_data_converted.csv','Value','mu','epsilon',
                        #'Deprecated_Modularity','Modularity')
                        
