'''generating the final graphs which should summarize all data'''
import numpy as np
from matplotlib import pyplot as plt

# Experiment parameters
experiment_params = np.array([[1300, 100],[1300, 500],[1300, 1000],\
                              [1500, 100],[1500, 500],[1500, 1000],\
                              [1750, 100],[1750, 500],[1750, 1000]])

# Function to make graphs
def final_graph(cooling_rate, n_exp):
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
    # Sample cooling rate
    cooling_rate = np.array([[0.66734257, 0.69078883, 0.77631882, 0.63813754],
       [0.39912428, 0.45883439, 0.49331085, 0.39826872],
       [0.73990755, 0.8245401 , 0.82595915, 0.70234445],
       [0.6686941 , 0.77086088, 0.74432964, 0.64881394],
       [0.71908277, 0.83954894, 0.8427713 , 0.71143514],
       [0.75150193, 0.85826932, 0.83488946, 0.71027249],
       [0.66258022, 0.76044122, 0.75452233, 0.63714172],
       [0.71199218, 0.82476226, 0.81331313, 0.70321665],
       [0.72214175, 0.79171589, 0.79241718, 0.67660492]])
    
    print(experiment_params)
    graph_data = final_graph(cooling_rate, 0)
    print(graph_data)
