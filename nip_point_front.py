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

    Version date: 26.03.2020
"""

"""
    In case we would like to work with the data from the back camara, use the following procedure:

        Generate data from experiment 'i':
            Use the name 'back_exp_i', where i indicates the number of the experiment.
            back_exp_i = generate_back(i-1)

        Format:
            Each experiment (certain laser power and compaction force) is
            stored as 'back_exp_i' where i is the index of the experiment.
        
            In order to obtain the data for each time step, tow and line:
                time = back_exp_i.time
                tow j - line k = back_exp_i.tow{j}[k - 1] with ( 1 <= j (tow number) <= 8 ) and ( 1 <= k (line number) <= 10 )

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

        plt.rcParams.update({'font.size': 15})
        plt.title()
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

color_1 = "#f87e05"
color_2 = "#002eea"
color_3 = "#f00000"
color_4 = "#0aa600"

color_darker_1 = "#b06903"
color_darker_2 = "#1c1f71"
color_darker_3 = "#761515"
color_darker_4 = "#0b7604"

linestyle_1 = 'solid'
linestyle_2 = 'dashed'
linestyle_3 = 'dashdot'
linestyle_4 = (0, (3, 1, 1, 1, 1, 1))

experiment_style_1 = 'solid'
experiment_style_2 = (0, (1, 1))
experiment_style_3 = (0, (1, 1))
experiment_style_4 = (0, (5, 10))
experiment_style_5 = (0, (5, 5))
experiment_style_6 = (0, (5, 1))
experiment_style_7 = 'dashed'
experiment_style_8 = (0, (3, 5, 1, 5, 1, 5))
experiment_style_9 = (0, (3, 1, 1, 1, 1, 1))

title_1 = "Laser Power = 1300 W, Compaction Force = 100 N"
title_2 = "Laser Power = 1300 W, Compaction Force = 500 N"
title_3 = "Laser Power = 1300 W, Compaction Force = 1000 N"
title_4 = "Laser Power = 1500 W, Compaction Force = 100 N"
title_5 = "Laser Power = 1500 W, Compaction Force = 500 N"
title_6 = "Laser Power = 1500 W, Compaction Force = 1000 N"
title_7 = "Laser Power = 1750 W, Compaction Force = 100 N"
title_8 = "Laser Power = 1750 W, Compaction Force = 500 N"
title_9 = "Laser Power = 1750 W, Compaction Force = 1000 N"

power_title_1 = "Laser Power = 1300 W"
power_title_2 = "Laser Power = 1500 W"
power_title_3 = "Laser Power = 1750 W"

compaction_title_1 = "Compaction Force = 100 N"
compaction_title_2 = "Compaction Force = 500 N"
compaction_title_3 = "Compaction Force = 1000 N"

# 0.- Plot it all:

def plot_all():
    for i in range(1,10):

        plt.rc('xtick', labelsize=20)
        plt.rc('ytick', labelsize=20)
        plt.rc('legend', fontsize=13)
        
        for j in range(4):
            plt.plot(eval(f"front_exp_{i}.time"), eval(f"front_exp_{i}.tow{2 * j + 1}"), label = (f"Experiment {i}, Tow {2 * j + 1}"), linestyle = eval(f"linestyle_{j + 1}"))
            
    plt.xlabel(r"time [s]", size = 15)
    plt.ylabel(r"Temperature [$^\circ C$]", size = 15)
    plt.box()
    plt.xlim(-0.5,15.1)
    plt.legend(loc="best", fancybox = True, shadow = True)
    plt.axhline(y=0, color='k', linewidth=0.75)
    plt.axvline(x=0, color='k', linewidth=0.75)
    plt.minorticks_on()
    plt.grid(b=True, which='major', color='#bebebe', linestyle='-')
    plt.grid(b=True, which='minor', color='#e9e9e9', linestyle='-', linewidth=0.5)
    figure = plt.gcf()
    figure.set_size_inches(12,6)
    plt.savefig(f"figures/all.png", dpi=300, bbox_inches = "tight")
    #plt.show()
    plt.close()

# 1.- Generate the temperature history for each experiment including all tows:

def plot_each_experiment_sep():
    for i in range(1,10):
        
        plt.rc('xtick', labelsize=20)
        plt.rc('ytick', labelsize=20)
        plt.rc('legend', fontsize=13)
        
        for j in range(4):
            plt.plot(eval(f"front_exp_{i}.time"), eval(f"front_exp_{i}.tow{2 * j + 1}"), label = (f"Tow {2 * j + 1}"), linestyle = eval(f"linestyle_{j + 1}"), color =  eval(f"color_darker_{j + 1}"), linewidth = 0.85)
            
        plt.title(eval(f"title_{i}"), size = 15)
        plt.xlabel(r"time [s]", size = 15)
        plt.ylabel(r"Temperature [$^\circ C$]", size = 15)
        plt.box()
        plt.xlim(-0.5,15.1)
        plt.legend(loc="best", fancybox = True, shadow = True)
        plt.axhline(y=0, color='k', linewidth=0.75)
        plt.axvline(x=0, color='k', linewidth=0.75)
        plt.minorticks_on()
        plt.grid(b=True, which='major', color='#bebebe', linestyle='-')
        plt.grid(b=True, which='minor', color='#e9e9e9', linestyle='-', linewidth=0.5)
        figure = plt.gcf()
        figure.set_size_inches(12,6)
        plt.savefig(f"figures/exp_{i}.png", dpi=300, bbox_inches = "tight")
        #plt.show()
        plt.close()

# 2.- For each tow plot all experiments.

def plot_each_tow_sep():
    for j in range(4):
        
        plt.rc('xtick', labelsize=20)
        plt.rc('ytick', labelsize=20)
        plt.rc('legend', fontsize=13)
        plt.subplot(221 + j)
        
        for i in range(1,10):
            plt.plot(eval(f"front_exp_{i}.time"), eval(f"front_exp_{i}.tow{2 * j + 1}"), label = (f"Experiment {i}"), linestyle = eval(f"experiment_style_{i}"))

        plt.title(f"Tow {2 * j + 1}", size = 15) 
        plt.xlabel(r"time [s]", size = 15)
        plt.ylabel(r"Temperature [$^\circ C$]", size = 15)
        plt.box()
        plt.xlim(-0.5,15.1)
        plt.legend(loc="best", fancybox = True, shadow = True)
        plt.axhline(y=0, color='k', linewidth=0.75)
        plt.axvline(x=0, color='k', linewidth=0.75)
        plt.minorticks_on()
        plt.grid(b=True, which='major', color='#bebebe', linestyle='-')
        plt.grid(b=True, which='minor', color='#e9e9e9', linestyle='-', linewidth=0.5)
        
    figure = plt.gcf()
    figure.set_size_inches(12,6)
    plt.savefig(f"figures/tow_{2 * j + 1}.png", dpi=300, bbox_inches = "tight")
    #plt.show()
    plt.close()

# 3.- For a certain power setting plot the temperature history of the tows in different plots.

def plot_each_power_w_all_tows():
    for k in range(1, 4):

        plt.rc('xtick', labelsize=20)
        plt.rc('ytick', labelsize=20)
        plt.rc('legend', fontsize=13)
        
        for i in range(4):
            for j in range(3 * k - 2, 3 * k + 1):
                plt.subplot(221+i)
                
                plt.plot(eval(f"front_exp_{j}.time"), eval(f"front_exp_{j}.tow{2 * i + 1}"), label = (eval(f"compaction_title_{j - 3 * ( k - 1 )}")), linestyle = eval(f"linestyle_{j - 3 * ( k - 1 )}"))
                
            plt.title(f"Tow {2 * i + 1}", size = 15)
            plt.xlabel(r"time [s]", size = 15)
            plt.ylabel(r"Temperature [$^\circ C$]", size = 15)
            plt.box()
            plt.xlim(-0.5,15.1)
            plt.legend(loc="best", fancybox = True, shadow = True)
            plt.axhline(y=0, color='k', linewidth=0.75)
            plt.axvline(x=0, color='k', linewidth=0.75)
            plt.minorticks_on()
            plt.grid(b=True, which='major', color='#bebebe', linestyle='-')
            plt.grid(b=True, which='minor', color='#e9e9e9', linestyle='-', linewidth=0.5)

        plt.suptitle(eval(f"power_title_{k}"), size = 17.5)
        plt.subplots_adjust(wspace=0.3, hspace=0.35)
        figure = plt.gcf()
        figure.set_size_inches(18,10)
        plt.savefig(f"figures/power_{k}.png", dpi=300, bbox_inches = "tight")
        #plt.show()
        plt.close()    

# 4.- For a certain compaction Force plot the temperature history of the tows in different plots.

def plot_each_force_w_all_tows():
    for k in range(1, 4):

        plt.rc('xtick', labelsize=20)
        plt.rc('ytick', labelsize=20)
        plt.rc('legend', fontsize=13)
        
        for i in range(4):
            for j in range(k, k + 7, 3):
                plt.subplot(221+i)
                
                plt.plot(eval(f"front_exp_{j}.time"), eval(f"front_exp_{j}.tow{2 * i + 1}"), label = (eval(f"power_title_{int((j - k) / 3 + 1)}")), linestyle = eval(f"linestyle_{int((j - k) / 3 + 1)}"))
                
            plt.title(f"Tow {2 * i + 1}", size = 15)
            plt.xlabel(r"time [s]", size = 15)
            plt.ylabel(r"Temperature [$^\circ C$]", size = 15)
            plt.box()
            plt.xlim(-0.5,15.1)
            plt.legend(loc="best", fancybox = True, shadow = True)
            plt.axhline(y=0, color='k', linewidth=0.75)
            plt.axvline(x=0, color='k', linewidth=0.75)
            plt.minorticks_on()
            plt.grid(b=True, which='major', color='#bebebe', linestyle='-')
            plt.grid(b=True, which='minor', color='#e9e9e9', linestyle='-', linewidth=0.5)

        plt.suptitle(eval(f"compaction_title_{k}"), size = 17.5)
        plt.subplots_adjust(wspace=0.3, hspace=0.35)
        figure = plt.gcf()
        figure.set_size_inches(18,10)
        plt.savefig(f"figures/force_{k}.png", dpi=300, bbox_inches = "tight")
        #plt.show()
        plt.close()


# 5.- We do the same things as before, but with averaged temperatures of the four tows.

# 5.1.- Averaged tows for certain laser power setting.

def plot_each_power_w_avg_tow():
    for i in range(3):

        plt.rc('xtick', labelsize=20)
        plt.rc('ytick', labelsize=20)
        plt.rc('legend', fontsize=13)
        
        for j in range(1, 4):
            if 3 * i + j == 1:
                average_temp = 1 / 3 * ( eval(f"front_exp_{3 * i + j}.tow1") + eval(f"front_exp_{3 * i + j}.tow5") + eval(f"front_exp_{3 * i + j}.tow7") )
            else:
                average_temp = 0.25 * ( eval(f"front_exp_{3 * i + j}.tow1") + eval(f"front_exp_{3 * i + j}.tow3") + eval(f"front_exp_{3 * i + j}.tow5") + eval(f"front_exp_{3 * i + j}.tow7") )

            #plt.subplot(311+i)
            
            plt.plot(eval(f"front_exp_{3 * i + j}.time"), average_temp, label = eval(f"compaction_title_{j}"), linestyle = eval(f"linestyle_{j}") )

        plt.title(eval(f"power_title_{i + 1}"), size = 15)
        plt.xlabel(r"time [s]", size = 15)
        plt.ylabel(r"Temperature [$^\circ C$]", size = 15)
        plt.box()
        plt.xlim(-0.5,15.1)
        plt.legend(loc="best", fancybox = True, shadow = True)
        plt.axhline(y=0, color='k', linewidth=0.75)
        plt.axvline(x=0, color='k', linewidth=0.75)
        plt.minorticks_on()
        plt.grid(b=True, which='major', color='#bebebe', linestyle='-')
        plt.grid(b=True, which='minor', color='#e9e9e9', linestyle='-', linewidth=0.5)
        figure = plt.gcf()
        figure.set_size_inches(12,6)
        plt.savefig(f"figures/avg_tow_power_{i}.png", dpi=300, bbox_inches = "tight")
        #plt.show()
        plt.close()

# 5.2.- Averaged tows for certain compaction force setting.

def plot_each_force_w_avg_tow():
    for i in range(1, 4):

        plt.rc('xtick', labelsize=20)
        plt.rc('ytick', labelsize=20)
        plt.rc('legend', fontsize=13)
        
        for j in range(3):
            
            if  i + 3 * j == 1:
                average_temp = 1 / 3 * ( eval(f"front_exp_{i + 3 * j}.tow1") + eval(f"front_exp_{i + 3 * j}.tow5") + eval(f"front_exp_{i + 3 * j}.tow7") )
            else:
                average_temp = 0.25 * ( eval(f"front_exp_{i + 3 * j}.tow1") + eval(f"front_exp_{i + 3 * j}.tow3") + eval(f"front_exp_{i + 3 * j}.tow5") + eval(f"front_exp_{i + 3 * j}.tow7") )
                
            #plt.subplot(310+i)
            
            plt.plot(eval(f"front_exp_{i + 3 * j}.time"), average_temp, label = eval(f"power_title_{j + 1}"), linestyle = eval(f"linestyle_{j + 1}") )

        plt.title(eval(f"compaction_title_{i}"), size = 15)
        plt.xlabel(r"time [s]", size = 15)
        plt.ylabel(r"Temperature [$^\circ C$]", size = 15)
        plt.box()
        plt.xlim(-0.5,15.1)
        plt.legend(loc="best", fancybox = True, shadow = True)
        plt.axhline(y=0, color='k', linewidth=0.75)
        plt.axvline(x=0, color='k', linewidth=0.75)
        plt.minorticks_on()
        plt.grid(b=True, which='major', color='#bebebe', linestyle='-')
        plt.grid(b=True, which='minor', color='#e9e9e9', linestyle='-', linewidth=0.5)
        figure = plt.gcf()
        figure.set_size_inches(12,6)
        plt.savefig(f"figures/avg_tow_force_{i}.png", dpi=300, bbox_inches = "tight")
        #plt.show()
        plt.close()

# 6.- Find the total temperature such that we find a single value.

# 6.1.- Find average temperature for each single tow.

def total_avg_temp_per_exp_tow():
    for i in range(1,10):

        plt.rc('xtick', labelsize=20)
        plt.rc('ytick', labelsize=20)
        plt.rc('legend', fontsize=13)
        
        for j in range(4):
            
            time_interval = eval(f"front_exp_{i}.time[ np.all([front_exp_{i}.time >= 4.0 , front_exp_{i}.time <= 11.0], axis = 0) ]")
            
            start = np.where(eval(f"front_exp_{i}.time") == time_interval[0])[0][0]
            
            end = np.where(eval(f"front_exp_{i}.time") == time_interval[-1])[0][0]

            tow_temp_interval = eval(f"front_exp_{i}.tow{2 * j + 1}[ start : end ]")
            
            average_temp_tot = np.sum(tow_temp_interval) / time_interval.size * np.ones(time_interval.size)
            
##            print(f"For experiment #{i} and tow #{2 * j + 1}, the average temperature is of ", average_temp_tot[0], " [deg C]")
            
            plt.plot(eval(f"front_exp_{i}.time"), eval(f"front_exp_{i}.tow{2 * j + 1}"), linewidth = 0.85, linestyle = eval(f"linestyle_{j + 1}"), color =  eval(f"color_darker_{j + 1}"))
            
            plt.plot(time_interval, average_temp_tot, label = (f"Tow {2 * j + 1}"), linestyle = eval(f"linestyle_{j + 1}"), linewidth = 1.75, color =  eval(f"color_{j + 1}"))

        plt.title(eval(f"title_{i}"), size = 15)
        plt.xlabel(r"time [s]", size = 15)
        plt.ylabel(r"Temperature [$^\circ C$]", size = 15)
        plt.box()
        plt.xlim(3.5, 12.1)
        plt.ylim(250, 525)
        plt.legend(loc="best", fancybox = True, shadow = True)
        plt.axhline(y=0, color='k', linewidth=0.75)
        plt.axvline(x=0, color='k', linewidth=0.75)
        plt.minorticks_on()
        plt.grid(b=True, which='major', color='#bebebe', linestyle='-')
        plt.grid(b=True, which='minor', color='#e9e9e9', linestyle='-', linewidth=0.5)
        figure = plt.gcf()
        figure.set_size_inches(12,6)
        plt.savefig(f"figures/tot_avg_exp_{i}_sectioned.png", dpi = 300, bbox_inches = "tight")
        plt.show()
        plt.close()

##        print()
##        print()

# 6.2.- Find average temperature for certain laser power setting

def total_avg_temp_each_power():
    for i in range(3):

        plt.rc('xtick', labelsize=20)
        plt.rc('ytick', labelsize=20)
        plt.rc('legend', fontsize=13)
            
        for j in range(1,4):

            time_interval = eval(f"front_exp_{3 * i + j}.time[ np.all([front_exp_{3 * i + j}.time >= 4.0 , front_exp_{3 * i + j}.time <= 11.0], axis = 0) ]")
            
            start = np.where(eval(f"front_exp_{3 * i + j}.time") == time_interval[0])[0][0]
            
            end = np.where(eval(f"front_exp_{3 * i + j}.time") == time_interval[-1])[0][0]

            average_temp_tot = np.zeros(time_interval.size)

            tow_1_temp_interval = eval(f"front_exp_{3 * i + j}.tow{1}[ start : end ]")
            tow_3_temp_interval = eval(f"front_exp_{3 * i + j}.tow{3}[ start : end ]")
            tow_5_temp_interval = eval(f"front_exp_{3 * i + j}.tow{5}[ start : end ]")
            tow_7_temp_interval = eval(f"front_exp_{3 * i + j}.tow{7}[ start : end ]")
            
            if 3 * i + j == 1:
                average_temp_tot = 1 /3 * ( np.sum(tow_1_temp_interval + tow_5_temp_interval + tow_7_temp_interval) ) /  time_interval.size * np.ones(time_interval.size)
                average_temp = 1 / 3 * ( eval(f"front_exp_{3 * i + j}.tow1") + eval(f"front_exp_{3 * i + j}.tow5") + eval(f"front_exp_{3 * i + j}.tow7") )
            else:
                average_temp_tot = 1 / 4 * ( np.sum(tow_1_temp_interval + tow_3_temp_interval + tow_5_temp_interval + tow_7_temp_interval) ) /  time_interval.size * np.ones(time_interval.size)
                average_temp = 0.25 * ( eval(f"front_exp_{3 * i + j}.tow1") + eval(f"front_exp_{3 * i + j}.tow3") + eval(f"front_exp_{3 * i + j}.tow5") + eval(f"front_exp_{3 * i + j}.tow7") )
                    
            plt.plot(eval(f"front_exp_{3 * i + j}.time"), average_temp, label = eval(f"compaction_title_{j}"), linestyle = eval(f"linestyle_{j}"), linewidth = 1.2, color =  eval(f"color_darker_{j}") )
            plt.plot(time_interval, average_temp_tot, label = (eval(f"compaction_title_{j}") + " - Averaged Line"), linestyle = eval(f"linestyle_{j}"), linewidth = 1.75, color =  eval(f"color_{j}") )

        plt.title(eval(f"power_title_{i + 1}"), size = 15)
        plt.xlabel(r"time [s]", size = 15)
        plt.ylabel(r"Temperature [$^\circ C$]", size = 15)
        plt.box()
        plt.xlim(-0.5,15.1)
        plt.legend(loc="best", fancybox = True, shadow = True)
        plt.axhline(y=0, color='k', linewidth=0.75)
        plt.axvline(x=0, color='k', linewidth=0.75)
        plt.minorticks_on()
        plt.grid(b=True, which='major', color='#bebebe', linestyle='-')
        plt.grid(b=True, which='minor', color='#e9e9e9', linestyle='-', linewidth=0.5)
        figure = plt.gcf()
        figure.set_size_inches(12,6)
        plt.savefig(f"figures/tot_avg_power_{i}.png", dpi=300, bbox_inches = "tight")
        #plt.show()
        plt.close()

# 6.3.- Find average temperature for certain compaction force setting

def total_avg_temp_each_force():
    for i in range(1,4):

        plt.rc('xtick', labelsize=20)
        plt.rc('ytick', labelsize=20)
        plt.rc('legend', fontsize=13)
        
        for j in range(3):

            time_interval = eval(f"front_exp_{i + 3 * j}.time[ np.all([front_exp_{i + 3 * j}.time >= 4.0 , front_exp_{i + 3 * j}.time <= 11.0], axis = 0) ]")
            
            start = np.where(eval(f"front_exp_{i + 3 * j}.time") == time_interval[0])[0][0]
            
            end = np.where(eval(f"front_exp_{i + 3 * j}.time") == time_interval[-1])[0][0]

            average_temp_tot = np.zeros(time_interval.size)

            tow_1_temp_interval = eval(f"front_exp_{i + 3 * j}.tow{1}[ start : end ]")
            tow_3_temp_interval = eval(f"front_exp_{i + 3 * j}.tow{3}[ start : end ]")
            tow_5_temp_interval = eval(f"front_exp_{i + 3 * j}.tow{5}[ start : end ]")
            tow_7_temp_interval = eval(f"front_exp_{i + 3 * j}.tow{7}[ start : end ]")
            
            if i + 3 * j == 1:
                average_temp_tot = 1 /3 * ( np.sum(tow_1_temp_interval + tow_5_temp_interval + tow_7_temp_interval) ) /  time_interval.size * np.ones(time_interval.size)
                average_temp = 1 / 3 * ( eval(f"front_exp_{i + 3 * j}.tow1") + eval(f"front_exp_{i + 3 * j}.tow5") + eval(f"front_exp_{i + 3 * j}.tow7") )
            else:
                average_temp_tot = 1 / 4 * ( np.sum(tow_1_temp_interval + tow_3_temp_interval + tow_5_temp_interval + tow_7_temp_interval) ) /  time_interval.size * np.ones(time_interval.size)
                average_temp = 0.25 * ( eval(f"front_exp_{i + 3 * j}.tow1") + eval(f"front_exp_{i + 3 * j}.tow3") + eval(f"front_exp_{i + 3 * j}.tow5") + eval(f"front_exp_{i + 3 * j}.tow7") )
                
            plt.plot(eval(f"front_exp_{i + 3 * j}.time"), average_temp, label = eval(f"power_title_{j + 1}"), linestyle = eval(f"linestyle_{j + 1}"), linewidth = 1.2, color =  eval(f"color_darker_{j + 1}") )
            plt.plot(time_interval, average_temp_tot, label = (eval(f"power_title_{j + 1}") + " - Averaged Line"), linestyle = eval(f"linestyle_{j + 1}"), linewidth = 1.75, color =  eval(f"color_{j + 1}") )

        plt.title(eval(f"compaction_title_{i}"), size = 15)
        plt.xlabel(r"time [s]", size = 15)
        plt.ylabel(r"Temperature [$^\circ C$]", size = 15)
        plt.box()
        plt.xlim(-0.5,15.1)
        plt.legend(loc="best", fancybox = True, shadow = True)
        plt.axhline(y=0, color='k', linewidth=0.75)
        plt.axvline(x=0, color='k', linewidth=0.75)
        plt.minorticks_on()
        plt.grid(b=True, which='major', color='#bebebe', linestyle='-')
        plt.grid(b=True, which='minor', color='#e9e9e9', linestyle='-', linewidth=0.5)
        figure = plt.gcf()
        figure.set_size_inches(12,6)
        plt.savefig(f"figures/tot_avg_force_{i}.png", dpi=300, bbox_inches = "tight")
        #plt.show()
        plt.close()
            

# Run functions:

##plot_all()
plot_each_experiment_sep()
##plot_each_tow_sep()
##plot_each_power_w_all_tows()
##plot_each_force_w_all_tows()
##plot_each_power_w_avg_tow()
##plot_each_force_w_avg_tow()
##total_avg_temp_per_exp_tow()
##total_avg_temp_each_power()
##total_avg_temp_each_force()
