from experiment_read import *
from matplotlib import pyplot as plt

"""
    Script to work with the temperature history of the nip point

    Format:
        Each experiment (certain laser power and compaction force) is
        stored as 'front_exp_i' where i is the index of the experiment.
        
        In order to obtain the data for each time step and tow:
            time = front_exp_i[0]
            tow j = front_exp_i[j] with ( 1 <= j (tow number) <= 8 )

    Version date: 10.03.2020
"""

# Experiment                     |  Laser Power | Compaction Force

front_exp_1 = generate_front(0) #       1300 W  |       100  N
front_exp_2 = generate_front(1) #       1300 W  |       500  N 
front_exp_3 = generate_front(2) #       1300 W  |       1000 N 
front_exp_4 = generate_front(3) #       1500 W  |       100  N 
front_exp_5 = generate_front(4) #       1500 W  |       500  N 
front_exp_6 = generate_front(5) #       1500 W  |       1000 N 
front_exp_7 = generate_front(6) #       1750 W  |       100  N 
front_exp_8 = generate_front(7) #       1750 W  |       500  N 
front_exp_9 = generate_front(8) #       1750 W  |       1000 N

for i in range(1,10):
    for j in range(4):
        plt.plot(eval(f"front_exp_{i}.time"), eval(f"front_exp_{i}.tow{2 * j + 1}"),
                 label = (f"Experiment {i}, Tow {2 * j + 1}"))
        
plt.xlabel(r"time [s]", size = 15)
plt.ylabel(r"Temperature [$^\circ C$]", size = 15)

#plt.axis('equal')
plt.box()
#plt.xlim(40,200)
#plt.ylim(-0.35,0.5)

#plt.xticks(np.arange(40.0,200.1, 20))

plt.legend(loc="best",fancybox=True, shadow=True)


plt.axhline(y=0, color='k', linewidth=0.75)
plt.axvline(x=0, color='k', linewidth=0.75)
plt.minorticks_on()
plt.grid(b=True, which='major', color='#bebebe', linestyle='-')
plt.grid(b=True, which='minor', color='#e9e9e9', linestyle='-', linewidth=0.5)

plt.show()

    


