from experiment_read import *
from matplotlib import pyplot as plt

"""
    Script to work with the temperature history of the nip point

    Format:
        Each experiment (certain laser power and compaction force) is
        stored as 'front_exp_i' where i is the index of the experiment.
        
        In order to obtain the data for each time step and tow:
            time = front_exp_i.time
            tow j = front_exp_i.tow{j} with ( 1 <= j (tow number) <= 8 )

    Version date: 24.03.2020
"""

"""
    Here goes a list with the graphs we will need:

        1.- Generate the temperature history for each experiment including all tows:
            This will make sure we see the difference in between tows.

        2.- For each tow plot all experiments.

        3.- For a certain power setting plot the temperature history of the tows in different plots.

        4.- For a certain compaction Force plot the temperature history of the tows in different plots.

        5.- We do the same things as before, but with averaged temperatures of the four tows.
"""

"""
    Nice features for the plots:

        plt.xlabel(r"time [s]", size = 15)
        plt.ylabel(r"Temperature [$^\circ C$]", size = 15)
        plt.axis('equal')
        plt.box()
        plt.xlim(x_min, x_max)
        plt.ylim(y_min, y_max)
        plt.xticks(np.arange(x_min, y_min, spacing))
        plt.legend(loc="best",fancybox=True, shadow=True)
        plt.axhline(y=0, color='k', linewidth=0.75)
        plt.axvline(x=0, color='k', linewidth=0.75)
        plt.minorticks_on()
        plt.grid(b=True, which='major', color='#bebebe', linestyle='-')
        plt.grid(b=True, which='minor', color='#e9e9e9', linestyle='-', linewidth=0.5)
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

# Plotting Styles:

linestyle_tow_1 = 'solid'
linestyle_tow_3 = 'dashed'
linestyle_tow_5 = 'dotted'
linestyle_tow_7 = 'dashdot'

# 0.- Plot it all:

for i in range(4):
    for j in range(1,4):
        plt.subplot(221+i)
        plt.plot(eval(f"front_exp_{j}.time"), eval(f"front_exp_{j}.tow{2 * i + 1}"), label = (f"Experiment {j}, Tow {2 * i + 1}"), linestyle = eval(f"linestyle_tow_{2 * i + 1}"))


        plt.title("Same power setting 1300W")        
        plt.xlabel(r"time [s]", size = 15)
        plt.ylabel(r"Temperature [$^\circ C$]", size = 15)
        plt.box()
        plt.legend(loc="best", fancybox = True, shadow = True)
        plt.axhline(y=0, color='k', linewidth=0.75)
        plt.axvline(x=0, color='k', linewidth=0.75)
        plt.minorticks_on()
        plt.grid(b=True, which='major', color='#bebebe', linestyle='-')
        plt.grid(b=True, which='minor', color='#e9e9e9', linestyle='-', linewidth=0.5)
plt.show()




for i in range(4):
    for j in range(4,7):
        plt.subplot(221+i)
        plt.plot(eval(f"front_exp_{j}.time"), eval(f"front_exp_{j}.tow{2 * i + 1}"), label = (f"Experiment {j}, Tow {2 * i + 1}"), linestyle = eval(f"linestyle_tow_{2 * i + 1}"))


        plt.title("Same power setting 1500 W")        
        plt.xlabel(r"time [s]", size = 15)
        plt.ylabel(r"Temperature [$^\circ C$]", size = 15)
        plt.box()
        plt.legend(loc="best", fancybox = True, shadow = True)
        plt.axhline(y=0, color='k', linewidth=0.75)
        plt.axvline(x=0, color='k', linewidth=0.75)
        plt.minorticks_on()
        plt.grid(b=True, which='major', color='#bebebe', linestyle='-')
        plt.grid(b=True, which='minor', color='#e9e9e9', linestyle='-', linewidth=0.5)

plt.show()



for i in range(4):
    for j in range(4):
        plt.subplot(221+i)
        plt.plot(eval(f"front_exp_{3*j}.time"), eval(f"front_exp_{j}.tow{2 * i + 1}"), label = (f"Experiment {j}, Tow {2 * i + 1}"), linestyle = eval(f"linestyle_tow_{2 * i + 1}"))


        plt.title("Same power setting 1750 W")        
        plt.xlabel(r"time [s]", size = 15)
        plt.ylabel(r"Temperature [$^\circ C$]", size = 15)
        plt.box()
        plt.legend(loc="best", fancybox = True, shadow = True)
        plt.axhline(y=0, color='k', linewidth=0.75)
        plt.axvline(x=0, color='k', linewidth=0.75)
        plt.minorticks_on()
        plt.grid(b=True, which='major', color='#bebebe', linestyle='-')
        plt.grid(b=True, which='minor', color='#e9e9e9', linestyle='-', linewidth=0.5)

plt.show()


for i in range(4):
    for j in range(3):
        plt.subplot(221+i)
        plt.plot(eval(f"front_exp_{3*j+1}.time"), eval(f"front_exp_{j}.tow{2 * i + 1}"), label = (f"Experiment {3*j+1}, Tow {2 * i + 1}"), linestyle = eval(f"linestyle_tow_{2 * i + 1}"))


        plt.title("Same force setting 100 N")        
        plt.xlabel(r"time [s]", size = 15)
        plt.ylabel(r"Temperature [$^\circ C$]", size = 15)
        plt.box()
        plt.legend(loc="best", fancybox = True, shadow = True)
        plt.axhline(y=0, color='k', linewidth=0.75)
        plt.axvline(x=0, color='k', linewidth=0.75)
        plt.minorticks_on()
        plt.grid(b=True, which='major', color='#bebebe', linestyle='-')
        plt.grid(b=True, which='minor', color='#e9e9e9', linestyle='-', linewidth=0.5)

plt.show()


for i in range(4):
    for j in range(3):
        plt.subplot(221+i)
        plt.plot(eval(f"front_exp_{3*j+2}.time"), eval(f"front_exp_{j}.tow{2 * i + 1}"), label = (f"Experiment {3*j+2}, Tow {2 * i + 1}"), linestyle = eval(f"linestyle_tow_{2 * i + 1}"))


        plt.title("Same force setting 500 N")        
        plt.xlabel(r"time [s]", size = 15)
        plt.ylabel(r"Temperature [$^\circ C$]", size = 15)
        plt.box()
        plt.legend(loc="best", fancybox = True, shadow = True)
        plt.axhline(y=0, color='k', linewidth=0.75)
        plt.axvline(x=0, color='k', linewidth=0.75)
        plt.minorticks_on()
        plt.grid(b=True, which='major', color='#bebebe', linestyle='-')
        plt.grid(b=True, which='minor', color='#e9e9e9', linestyle='-', linewidth=0.5)

plt.show()



for i in range(4):
    for j in range(1,4):
        plt.subplot(221+i)
        plt.plot(eval(f"front_exp_{3*j}.time"), eval(f"front_exp_{j}.tow{2 * i + 1}"), label = (f"Experiment {3*j}, Tow {2 * i + 1}"), linestyle = eval(f"linestyle_tow_{2 * i + 1}"))


        plt.title("Same force setting 1000 N")        
        plt.xlabel(r"time [s]", size = 15)
        plt.ylabel(r"Temperature [$^\circ C$]", size = 15)
        plt.box()
        plt.legend(loc="best", fancybox = True, shadow = True)
        plt.axhline(y=0, color='k', linewidth=0.75)
        plt.axvline(x=0, color='k', linewidth=0.75)
        plt.minorticks_on()
        plt.grid(b=True, which='major', color='#bebebe', linestyle='-')
        plt.grid(b=True, which='minor', color='#e9e9e9', linestyle='-', linewidth=0.5)

plt.show()

# 1.- Generate the temperature history for each experiment including all tows:


# 2.- For each tow plot all experiments.


# 3.- For a certain power setting plot the temperature history of the tows in different plots.


# 4.- For a certain compaction Force plot the temperature history of the tows in different plots.


# 5.- We do the same things as before, but with averaged temperatures of the four tows.
    


