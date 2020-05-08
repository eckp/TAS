'''generating the final graphs which should summarize all data'''
import numpy as np
from matplotlib import pyplot as plt
from data import *
from experiment_read import *
from regression import get_cooling_rate
from temperature_history import get_temp_history

def final_graph(cooling_rate, n_exp):
    '''Accepts cooling rate and tow number (0-3) to generate a graph
    with compaction force, laser power and cooling rate combined.
    Returns the matrix with graph data, where the compaction force is
    held constant throughout the columns and laser power throughout rows.'''
    
    graph_data = np.empty((3,3))
    n_points = len(experiment_params[:,0])
    xgraph = []
    comp_force = []

    # Generate usable matrix for graphs
    for i in range(int(n_points/3)):
        xgraph.append(experiment_params[i*3,0])
        comp_force.append(experiment_params[i,1])
        for j in range(int(n_points/3)):
            counter = i * 3 + j
            #columns -> constant comp. force
            #rows -> constant laser power
            graph_data[i,j] = cooling_rate[counter,n_exp]

    # Plot graphs
    for k in range(int(n_points/3)):
        ygraph = graph_data[:,k]
        plt.plot(xgraph, ygraph, label=comp_force[k])

    plt.legend()
    plt.show()
    return graph_data
        
        

if __name__ == "__main__":
    back = {f'Exp{i + 1}' : [generate_back(i), experiment_params[i]] for i in range(numExp)} #rear camera data

    for exp in back.values():
        for itow in range(0,8,2):  # odd tows 1 through 7
            print(f'experiment {exp[1]}, tow nr. {itow+1}')
            time = exp[0].time  # get the time list of this tow
            tow_temp = exp[0].tows[itow]  # get the temperature data of this tow
            # sample the temp history along the entire length of the tow
            tow_time_temps = np.array([get_temp_history(tow_temp, time, sample_idx=sample_idx) for sample_idx in range(len(time))])
            plt.pcolor(tow_time_temps[:,1,:].T, cmap='inferno')
            plt.show()
            
            sample_range = list(range(70, 740))  # range of indices to sample (cooling rate calculations require smooth enough curves)
            tow_cooling_rates = [get_cooling_rate(temp_hist, time_map) for time_map, temp_hist  in tow_time_temps[min(sample_range):max(sample_range)+1]]
            plt.plot(sample_range, tow_cooling_rates)
            plt.show()
    
#    print(experiment_params)
#    graph_data = final_graph(cooling_rate, 0)
#    print(graph_data)
