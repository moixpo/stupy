# -*- coding: utf-8 -*-
"""
#  Version  2.4  nov 2020
#  Moix P-O
#  Albedo-Engineering WWW.ALBEDO-ENGINEERING.COM
#  WWW.OFFGRID.CH

@author: moix_
@modified by: brycepg

xt_graph_plotter_pandas.py
"""


import matplotlib.pyplot as plt
import matplotlib.sankey as sk

import pandas as pd
import numpy as np

from PIL import Image

import xt_all_csv_pandas_import


#colorset
PINK_COLOR='#FFB2C7'
RED_COLOR='#CC0000'
WHITE_COLOR='#FFFFFF'

#albedo
A_RED_COLOR="#9A031E"
A_YELLOW_COLOR="#F7B53B"
A_BLUE_COLOR="#2E5266"
A_RAISINBLACK_COLOR="#272838"
A_BLUEGREY_COLOR="#7E7F9A"
A_GREY_COLOR_SLATE="#6E8898"
A_GREY_COLOR2_BLUED="#9FB1BC"
A_GREY_COLOR3_LIGHT="#F9F8F8"


#Studer
NX_LIGHT_BLUE="#F0F6F8"
NX_BLUE="#6BA3B8"
NX_BROWN="#A2A569"
NX_LIGHT_BROWN="#E3E4D2"
NX_PINK="#B06B96"
NX_GREEN="#78BE20"



#CHOICES:
FIGURE_FACECOLOR=WHITE_COLOR #NX_LIGHT_BROWN
AXE_FACECOLOR=WHITE_COLOR
SOLAR_COLOR=A_YELLOW_COLOR
LOAD_COLOR=A_RED_COLOR
GENSET_COLOR=A_BLUE_COLOR



#figsize=(FIGSIZE_WIDTH, FIGSIZE_HEIGHT)
FIGSIZE_WIDTH=14
FIGSIZE_HEIGHT=6
#figsize=(FIGSIZE_WIDTH, FIGSIZE_HEIGHT)

WATERMARK_PICTURE='logo.png'

#addition of a watermark on the figure
im = Image.open(WATERMARK_PICTURE)   




def build_sys_power_figure(total_datalog_df, quarters_mean_df):
    
    all_channels_labels = list(total_datalog_df.columns)

    
    #####################################
    #plot all the channels with SYSTEM Power 
    
    channels_number_PsolarTot = [i for i, elem in enumerate(all_channels_labels) if 'Solar power (ALL) [kW]' in elem]
    channel_number_Pin_actif_Tot = [i for i, elem in enumerate(all_channels_labels) if "Pin power (ALL)" in elem]
    channel_number_Pout_actif_Tot = [i for i, elem in enumerate(all_channels_labels) if "Pout power (ALL)" in elem]
    
    
     
    #utilisation directe du label plutot que les indexs des columns: 
    chanel_label_Pout_actif_tot=all_channels_labels[channel_number_Pout_actif_Tot[0]]
    chanel_label_Pin_actif_tot=all_channels_labels[channel_number_Pin_actif_Tot[0]]
    chanel_label_Psolar_tot=all_channels_labels[channels_number_PsolarTot[0]]
    
    
    #create object figure
    #fig_pow, axes_pow = plt.subplots(nrows=1, ncols=1)
    fig_pow, axes_pow = plt.subplots()
    fig_pow.set_facecolor(FIGURE_FACECOLOR)
    
    #total_datalog_df.plot(y=total_datalog_df.columns[channels_number_Pactif],
    #                      figsize=(12,6),
    #                      ax=axes_pow[0])
    
    total_datalog_df.plot(y=chanel_label_Psolar_tot,
                          figsize=(FIGSIZE_WIDTH, FIGSIZE_HEIGHT),
                          ax=axes_pow,
                          color=SOLAR_COLOR,
                          legend="Solar")
    
    total_datalog_df.plot(y=chanel_label_Pin_actif_tot,
                          figsize=(FIGSIZE_WIDTH, FIGSIZE_HEIGHT),
                          ax=axes_pow,
                          color=GENSET_COLOR,
                          legend="Grid/Genset")
    
    total_datalog_df.plot(y=chanel_label_Pout_actif_tot,
                          figsize=(FIGSIZE_WIDTH, FIGSIZE_HEIGHT),
                          ax=axes_pow,
                          color=LOAD_COLOR,
                          legend="Loads")
    
    
    axes_pow.set_ylabel('Power activ [kW]', fontsize=12)
    axes_pow.set_title('System Powers', fontsize=12, weight="bold")
    axes_pow.grid(True)
    #axes_pow.set_facecolor(AXE_FACECOLOR)
        
    fig_pow.figimage(im, 10, 10, zorder=3, alpha=.2)
    fig_pow.savefig("FigureExport/sys_power_figure.png")

    return fig_pow



def build_operating_mode_pies(total_datalog_df):

##############################
#OPERATING MODE:
####
    fig_mode, ax_mode =plt.subplots(nrows=1, ncols=2,figsize=(FIGSIZE_WIDTH, FIGSIZE_HEIGHT))
    fig_mode.suptitle('Operating state, master', fontweight = 'bold', fontsize = 12) 

    all_channels_labels = list(total_datalog_df.columns)
    
    channel_number = [i for i, elem in enumerate(all_channels_labels) if 'XT-Mode [] I3028 L1' in elem]  
    if channel_number:    
        channel_label=all_channels_labels[channel_number[0]]
    
        
        
        operating_time_in_mode=total_datalog_df[channel_label].value_counts().values/60/24
        op_labels=total_datalog_df[channel_label].value_counts().index
        
        ax_mode[0].pie(operating_time_in_mode, 
               labels=op_labels,
               shadow=True, 
               startangle=90,
               autopct='%1.1f%%',
               wedgeprops=dict(width=0.2)
               )
        ax_mode[0].set_title("Operating mode Inverter")
    
    
    
    channel_number = [i for i, elem in enumerate(all_channels_labels) if 'VT-Mode [] I11016 1' in elem]
    if channel_number:   
        channel_label=all_channels_labels[channel_number[0]]
        
        counts=total_datalog_df[channel_label].value_counts()
        operating_time_in_mode=counts.values/60/24
        op_labels=counts.index
        
        ax_mode[1].pie(operating_time_in_mode, 
               labels=op_labels,
               shadow=True, 
               startangle=90,
               autopct='%1.1f%%',
               wedgeprops=dict(width=0.2)
               )
        ax_mode[1].set_title("Operating mode VT")
    
    #'VS-Mod1 [] I15014 1'
    channel_number = [i for i, elem in enumerate(all_channels_labels) if 'VS-Mod' in elem]
    if channel_number:   
        channel_label=all_channels_labels[channel_number[0]]
        
        counts=total_datalog_df[channel_label].value_counts()
        operating_time_in_mode=counts.values/60/24
        op_labels=counts.index
        
        ax_mode[1].pie(operating_time_in_mode, 
               labels=op_labels,
               shadow=True, 
               startangle=90,
               autopct='%1.1f%%',
               wedgeprops=dict(width=0.2)
               )
        ax_mode[1].set_title("Operating mode VS")
        

    fig_mode.figimage(im, 10, 10, zorder=3, alpha=.2)
    fig_mode.savefig("FigureExport/operating_modes.png")
    
    return fig_mode


def build_consumption_profile(total_datalog_df):

    all_channels_labels = list(total_datalog_df.columns)

    channel_number = [i for i, elem in enumerate(all_channels_labels) if 'Pout Consumption power (ALL)' in elem]
   
    #channel_number=channel_number_Pout_conso_Tot
    
    time_of_day_in_hours=list(total_datalog_df.index.hour+total_datalog_df.index.minute/60)
    time_of_day_in_minutes=list(total_datalog_df.index.hour*60+total_datalog_df.index.minute)
    
    #add a channels to the dataframe with minutes of the day to be able to sort data on it:
    
    #Create a new entry:
    total_datalog_df['Time of day in minutes']=time_of_day_in_minutes
        
        
    fig_pow_by_min_of_day, axes_pow_by_min_of_day = plt.subplots(nrows=1, ncols=1, figsize=(FIGSIZE_WIDTH, FIGSIZE_HEIGHT))
    
    
    #maybe it is empty if there is no inverter:
    if channel_number:
        
        channel_label=all_channels_labels[channel_number[0]]
        
        axes_pow_by_min_of_day.plot(time_of_day_in_hours,
                          total_datalog_df[channel_label].values, 
                          marker='+',
                          alpha=0.25,
                          color='b',
                          linestyle='None')
       
        
    
        #faire la moyenne de tous les points qui sont à la même minute du jour:
        mean_by_minute=np.zeros(1440)
        x1=np.array(range(0,1440))
        for k in x1:
            tem_min_pow1=total_datalog_df[total_datalog_df['Time of day in minutes'].values == k]
            mean_by_minute[k]=np.nanmean(tem_min_pow1[channel_label].values)
            
    
        axes_pow_by_min_of_day.plot(x1/60, mean_by_minute,
                          color='g',
                          linestyle ='-',
                          linewidth=2)
    
        #faire la moyenne de tous les points qui sont à la même heure:
        mean_by_hour=np.zeros(24)
        x2=np.array(range(0,24))
        for k in x2:
            tem_min_pow2=total_datalog_df[total_datalog_df.index.hour == k]
            mean_by_hour[k]=np.nanmean(tem_min_pow2[channel_label].values)
            
    
        axes_pow_by_min_of_day.plot(x2, mean_by_hour,
                          color='r',
                          linestyle ='-',
                          linewidth=2,
                          drawstyle='steps-post')
        
        #mean power:
        #axes_pow_by_min_of_day.axhline(np.nanmean(total_datalog_df[channel_label].values), color='k', linestyle='dashed', linewidth=2)
        axes_pow_by_min_of_day.axhline(mean_by_minute.mean(), color='k', linestyle='dashed', linewidth=2)
        text_to_disp='Mean power= ' + str(round(mean_by_minute.mean(), 2)) + ' kW'
        axes_pow_by_min_of_day.text(0.1,mean_by_minute.mean()+0.1,  text_to_disp, horizontalalignment='left',verticalalignment='bottom')
        axes_pow_by_min_of_day.legend(["All points", "min mean profile" ,"hour mean profile"])
        axes_pow_by_min_of_day.set_ylabel("Power [kW]", fontsize=12)
        axes_pow_by_min_of_day.set_xlabel("Time [h]", fontsize=12)
        axes_pow_by_min_of_day.set_xlim(0,24)
        axes_pow_by_min_of_day.set_title("Consumption profile by hour of the day", fontsize=12, weight="bold")
        axes_pow_by_min_of_day.grid(True)
        
    
    else:
        #axes_pow_by_min_of_day.text(0.0, 0.0, "There is no Studer inverter!", horizontalalignment='left',verticalalignment='bottom')
        axes_pow_by_min_of_day.set_title("There is no Studer inverter!", fontsize=12, weight="bold")
        
    
    fig_pow_by_min_of_day.figimage(im, 10, 10, zorder=3, alpha=.2)
    fig_pow_by_min_of_day.savefig("FigureExport/typical_power_profile_figure.png")

    return fig_pow_by_min_of_day





def build_power_histogram_figure(total_datalog_df, quarters_mean_df):
    all_channels_labels = list(total_datalog_df.columns)
    quarters_channels_labels=list(quarters_mean_df.columns)
    channels_number_Pin_actif = [i for i, elem in enumerate(all_channels_labels) if "Pin power (ALL)" in elem]
    channels_number_Pout_actif = [i for i, elem in enumerate(all_channels_labels) if "Pout power (ALL)" in elem]


    #take out the 0kW power (when genset/grid is not connected):    
    #chanel_number=channels_number_Pin_actif[0]


    channel_number=channels_number_Pin_actif[0]
    values_for_hist=quarters_mean_df.iloc[:,channel_number]
    values_for_hist2=values_for_hist[values_for_hist > 0.1]
    
    temp=quarters_mean_df.iloc[:,channel_number]
    #values_for_hist[values_for_hist > 0.1]
    values_for_Pin_hist=temp[temp > 0.1]

    
    channel_number=channels_number_Pout_actif[0]
    values_for_Pout_hist=quarters_mean_df.iloc[:,channel_number]

    fig_hist, axes_hist = plt.subplots(figsize=(FIGSIZE_WIDTH, FIGSIZE_HEIGHT))
    
    values_for_Pout_hist.hist( bins=50, alpha=0.5, label="Pout",density=True)
    values_for_Pin_hist.hist( bins=50, alpha=0.5, label="Pin", density=True)
    plt.axvline(quarters_mean_df[quarters_channels_labels[channel_number]].mean(), color='k', linestyle='dashed', linewidth=2)

    axes_hist.set_title("Histogram of Powers (without 0 kW for Pin)", fontsize=12, weight="bold")
    axes_hist.set_xlabel("Power [kW]", fontsize=12)
    axes_hist.set_ylabel("Frequency density", fontsize=12)
    axes_hist.legend(loc='upper right')


    axes_hist.grid(True)
    
    fig_hist.figimage(im, 10, 10, zorder=3, alpha=.2)
    fig_hist.savefig("FigureExport/histogramm_power_figure.png")

    return fig_hist





def build_bsp_voltage_current_figure(total_datalog_df):
    all_channels_labels = list(total_datalog_df.columns)
    channel_number_ubat_ref=[i for i, elem in enumerate(all_channels_labels) if 'System Ubat ref [Vdc]' in elem]

    #channel_number_ubatbsp = [i for i, elem in enumerate(all_channels_labels) if 'BSP-Ubat' in elem]
    channels_number_ibatbsp = [i for i, elem in enumerate(all_channels_labels) if 'BSP-Ibat' in elem]


   
    ################################
    #bsp battery voltage and current on the same graph:
    fig_bsp_mes, ax1_bsp_mes = plt.subplots(figsize=(FIGSIZE_WIDTH, FIGSIZE_HEIGHT))
    ax2_bsp_mes = ax1_bsp_mes.twinx()
    y1=total_datalog_df[total_datalog_df.columns[channel_number_ubat_ref]]
    y2=total_datalog_df[total_datalog_df.columns[channels_number_ibatbsp]]
    xtime=total_datalog_df.index
    ax1_bsp_mes.plot(xtime, y1, 'b-')
    ax2_bsp_mes.plot(xtime, y2, 'r-')
    
    ax1_bsp_mes.set_ylabel('Voltage [V]', fontsize=12, color='b')
    ax2_bsp_mes.set_ylabel('Amperes [A]', fontsize=12, color='r')
    ax1_bsp_mes.set_title("Battery voltage and current (only with BSP)", fontsize=12, weight="bold")
    
    ax1_bsp_mes.grid(True)

    fig_bsp_mes.figimage(im, 10, 10, zorder=3, alpha=.2)
    fig_bsp_mes.savefig("FigureExport/bsp_mes_figure.png")

    return fig_bsp_mes


    
def build_total_battery_voltages_currents_figure(total_datalog_df):
    all_channels_labels = list(total_datalog_df.columns)

    ################################
    # plot all the channels with battery voltage and current:
    channels_number_ubat = [i for i, elem in enumerate(all_channels_labels) if "Ubat" in elem]
    channels_number_ibat = [i for i, elem in enumerate(all_channels_labels) if "Ibat" in elem]

    # fig_bat=plt.figure()
    fig_batt, (axes_bat_u, axes_bat_i) = plt.subplots(nrows=2, ncols=1)

    total_datalog_df.plot(
        y=total_datalog_df.columns[channels_number_ubat],
        grid=True,
        figsize=(FIGSIZE_WIDTH, FIGSIZE_HEIGHT),
        sharex=True,
        ax=axes_bat_u,
    )

    axes_bat_u.set_ylabel("Voltage [V]", fontsize=12)
    axes_bat_u.set_title("All Battery Voltages", fontsize=12, weight="bold")
    axes_bat_u.grid(True)

    total_datalog_df.plot(
        y=total_datalog_df.columns[channels_number_ibat],
        figsize=(FIGSIZE_WIDTH, FIGSIZE_HEIGHT),
        grid=True,
        sharex=axes_bat_u,
        ax=axes_bat_i,
    )

    axes_bat_i.set_ylabel("Amperes [A]", fontsize=12)
    axes_bat_i.set_title("All Battery Currents", fontsize=12, weight="bold")
    axes_bat_i.grid(True)
    
    fig_batt.figimage(im, 10, 10, zorder=3, alpha=.2)
    fig_batt.savefig("FigureExport/all_bat_channels.png")

    return fig_batt



def build_battery_voltage_histogram_figure(total_datalog_df, quarters_mean_df):
    all_channels_labels = list(total_datalog_df.columns)
    quarters_channels_labels=list(quarters_mean_df.columns)
    channels_number_ubat = [i for i, elem in enumerate(all_channels_labels) if "System Ubat ref [Vdc]" in elem]
    chanel_number=channels_number_ubat[0]
    
    fig_batt_hist, axes_bat_u_hist = plt.subplots(nrows=1, ncols=1, figsize=(FIGSIZE_WIDTH, FIGSIZE_HEIGHT))

    quarters_mean_df.plot(
        y=quarters_mean_df.columns[chanel_number],
        kind="hist",
        bins=80,
        ax=axes_bat_u_hist,
    )
    all_channels_labels
    #print(all_channels_labels[channels_number_ubat[1]])
    
    plt.axvline(quarters_mean_df[quarters_channels_labels[chanel_number]].mean(), color='k', linestyle='dashed', linewidth=2)

    axes_bat_u_hist.set_xlabel("Voltage [V]", fontsize=12)
    axes_bat_u_hist.set_ylabel("occurence", fontsize=12)
    axes_bat_u_hist.set_title("Battery Voltage Histogram", fontsize=12, weight="bold")
    axes_bat_u_hist.grid(True)
    
    fig_batt_hist.figimage(im, 10, 10, zorder=3, alpha=.2)
    fig_batt_hist.savefig("FigureExport/bat_voltage_histogramm_figure.png")

    return fig_batt_hist



def build_battery_chargedischarge_histogram_figure(total_datalog_df, quarters_mean_df):
    
    all_channels_labels = list(total_datalog_df.columns)
    channel_number_ubat_ref = [i for i, elem in enumerate(all_channels_labels) if 'System Ubat ref [Vdc]' in elem]
    channels_number_ibatbsp = [i for i, elem in enumerate(all_channels_labels) if 'BSP-Ibat' in elem]
    
    # Set up the axes with gridspec
    fig_scat2hist = plt.figure(figsize=(FIGSIZE_WIDTH, FIGSIZE_HEIGHT))
    grid = plt.GridSpec(4, 4, hspace=0.2, wspace=0.2)
    main_ax = fig_scat2hist.add_subplot(grid[:-1, 0:])



    #check if there is an BSP or not, if not we display an empty graph 
        
    if total_datalog_df[all_channels_labels[channels_number_ibatbsp[0]]].sum()==0:
        main_ax.set_title('There is no BSP', fontsize=12, weight="bold")
    else: 

    
    #battery_power=total_datalog_df.values[:,channel_number_ubat_ref]*total_datalog_df.values[:,channels_number_ibatbsp]/1000
    
    #battery_power_df=pd.DataFrame({"Battery Power [kW]": battery_power,
    #                               "Battery Charge Power [kW]": battery_power,
    #                               "Battery Discharge Power [kW]": battery_power},
    #                                index=total_datalog_df.index)
                   
        
        
        #take out the points with negative current only:
        channel_number=channels_number_ibatbsp[0]
        
        #copy only voltage and current
        voltage_current_only_df=total_datalog_df[[all_channels_labels[channel_number_ubat_ref[0]],
                                                 all_channels_labels[channels_number_ibatbsp[0]]]]
        
        #keep rows with negativ current:
        voltage_neg_current_only_df=voltage_current_only_df[voltage_current_only_df[all_channels_labels[channels_number_ibatbsp[0]]]<0.0]
        
        #keep rows with positiv current:
        voltage_pos_current_only_df=voltage_current_only_df[voltage_current_only_df[all_channels_labels[channels_number_ibatbsp[0]]]>=0.0]
        
    
        #############
        #The graphs together:
        
        x=voltage_neg_current_only_df.values[:,0]
        y=voltage_neg_current_only_df.values[:,1]
        x2=voltage_pos_current_only_df.values[:,0]
        y2=voltage_pos_current_only_df.values[:,1]
        
        
        #main_ax.scatter(voltage_neg_current_only_df.values[:,0],
        #                  voltage_neg_current_only_df.values[:,1], 
        #                  alpha=0.25)
        #
        #
        #main_ax.scatter(voltage_pos_current_only_df.values[:,0],
        #                  voltage_pos_current_only_df.values[:,1], 
        #                  alpha=0.25)
        
        
        
        # scatter points on the main axes
        main_ax.plot(x, y, 'o', markersize=3, alpha=0.2)
        main_ax.plot(x2, y2, 'o', markersize=3, alpha=0.2)
        plt.axvline(x.mean(), color='k', linestyle='dashed', linewidth=2)
        text_to_disp='Mean volt in discharge= ' + str(round(x.mean(), 2)) + ' Vdc'
        main_ax.text(x.mean()+0.2, y.mean(), text_to_disp, horizontalalignment='left',verticalalignment='bottom')
        
        main_ax.grid(True) 
        
        # histogram on the attached axes
        x_hist = fig_scat2hist.add_subplot(grid[-1, 0:], yticklabels=[], sharex=main_ax)
        
        x_hist.hist(x, bins=50,
                    histtype='stepfilled',
                    orientation='vertical',
                    alpha=0.5, 
                    label='Discharge', 
                    density=0)
        
        plt.axvline(x.mean(), color='k', linestyle='dashed', linewidth=2)
        text_to_disp='Mean volt in discharge= ' + str(round(x.mean(), 2)) + ' Vdc'
        #x_hist.text(x.mean()+0.2, 0.0, text_to_disp, horizontalalignment='left',verticalalignment='bottom')
        
        
        x_hist.hist(x2, bins=50,
                    histtype='stepfilled',
                    orientation='vertical',
                    alpha=0.5, 
                    label='Charge', 
                    density=0)
        
        
        x_hist.grid(True) 
        
        #x_hist.invert_yaxis()
        
        main_ax.set_title('Battery voltage versus currents and charge/discharge histogramms', fontsize=12, weight="bold")
        main_ax.set_ylabel('Amperes [A]', fontsize=12)
        #x_hist.set_title(text_to_disp, fontsize=12, weight="bold")
        
        x_hist.set_xlabel('Voltage [V]', fontsize=12)
        x_hist.set_ylabel('Frequency density', fontsize=12)
        x_hist.set_ylabel('Counts', fontsize=12)
        x_hist.legend(loc='upper right')
    
    fig_scat2hist.figimage(im, 10, 10, zorder=3, alpha=.2)
    fig_scat2hist.savefig("FigureExport/bsp_chargedischarge_hist_figure.png")

    return fig_scat2hist



def build_ac_power_figure(total_datalog_df, quarters_mean_df):
    all_channels_labels = list(total_datalog_df.columns)
    channels_number_Papparent = [i for i, elem in enumerate(all_channels_labels) if ("I3098" in elem)  ]
    channels_number_PapparentMax=[i for i, elem in enumerate(all_channels_labels) if ("I3097" in elem)  ]
    fig_pow, axes_pow = plt.subplots(nrows=1, ncols=1, figsize=(FIGSIZE_WIDTH, FIGSIZE_HEIGHT))

   
    if channels_number_Papparent:
    
        total_datalog_df.plot(
            y=total_datalog_df.columns[channels_number_PapparentMax],
            marker="+",
            ax=axes_pow,
        )
        total_datalog_df.plot(
            y=total_datalog_df.columns[channels_number_Papparent],
            marker="+",
            ax=axes_pow,
        )
        #quarters_mean_df.plot( y=quarters_mean_df.columns[channels_number_Papparent], marker="o", ax=axes_pow  )
        
        axes_pow.set_ylabel("Apparent power S [kVA]", fontsize=12)
        axes_pow.set_title("1min and peak AC-apparent power S", fontsize=12, weight="bold")
        axes_pow.grid(True)
    else:
        axes_pow.set_title("No inverter in the system", fontsize=12, weight="bold")
        
        #channels_number_Pactif = [i for i, elem in enumerate(all_channels_labels) if "[kW]" in elem]

    #    fig_pow, axes_pow = plt.subplots(nrows=1, ncols=2, figsize=(FIGSIZE_WIDTH, FIGSIZE_HEIGHT))
    #
    #    total_datalog_df.plot(
    #        y=total_datalog_df.columns[channels_number_Pactif],
    #        ax=axes_pow[0],
    #    )
    #
    #    axes_pow[0].set_ylabel("Power activ/reactiv [kW/kVA]", fontsize=12)
    #    axes_pow[0].set_title("All AC-out Powers", fontsize=12, weight="bold")
    #    axes_pow[0].grid(True)
    #
    #    if channels_number_Papparent:
    #    
    #        total_datalog_df.plot(
    #            y=total_datalog_df.columns[channels_number_Papparent],
    #            marker="+",
    #            ax=axes_pow[1],
    #        )
    #        quarters_mean_df.plot(
    #            y=quarters_mean_df.columns[channels_number_Papparent], marker="o", ax=axes_pow[1]
    #        )
    #        axes_pow[1].set_ylabel("Power apparent [kVA]", fontsize=12)
    #        axes_pow[1].set_title("1min and 15min AC-out Power", fontsize=12, weight="bold")
    #        axes_pow[1].grid(True)
    #    else:
    #        axes_pow[1].set_title("No inverter in the system", fontsize=12, weight="bold")

    fig_pow.figimage(im, 10, 10, zorder=3, alpha=.2)
    fig_pow.savefig("FigureExport/apparent_power_figure.png")

    return fig_pow



#
#
#def build_voltage_versus_current_figure(total_datalog_df):
#    all_channels_labels = list(total_datalog_df.columns)
#    channels_number_ubatbsp = [i for i, elem in enumerate(all_channels_labels) if "BSP-Ubat" in elem]
#    channels_number_ibatbsp = [i for i, elem in enumerate(all_channels_labels) if "BSP-Ibat" in elem]
#    
#
#    #take out the points with negative current only:
#    channel_number=channels_number_ibatbsp[0]
#    
#    #copy only voltage and current
#    voltage_current_only_df=total_datalog_df[[all_channels_labels[channels_number_ubatbsp[0]],
#                                             all_channels_labels[channels_number_ibatbsp[0]]]]
#    
#    #keep rows with negativ current:
#    voltage_neg_current_only_df=voltage_current_only_df[voltage_current_only_df[all_channels_labels[channels_number_ibatbsp[0]]]<0.0]
#    
#    #keep rows with positiv current:
#    voltage_pos_current_only_df=voltage_current_only_df[voltage_current_only_df[all_channels_labels[channels_number_ibatbsp[0]]]>=0.0]
#
#
#    fig_batt, axes_batt = plt.subplots(nrows=1, ncols=1,figsize=(FIGSIZE_WIDTH, FIGSIZE_HEIGHT))
#    
#    #    axes_batt.scatter(
#    #        total_datalog_df.values[:, channels_number_ubatbsp],
#    #        total_datalog_df.values[:, channels_number_ibatbsp],
#    #        alpha=0.25
#    #    )
#    axes_batt.scatter(voltage_neg_current_only_df.values[:,0],
#                      voltage_neg_current_only_df.values[:,1], 
#                      alpha=0.25)
#    
#    
#    axes_batt.scatter(voltage_pos_current_only_df.values[:,0],
#                      voltage_pos_current_only_df.values[:,1], 
#                      alpha=0.25)
#
#    axes_batt.set_ylabel("Amperes [A]", fontsize=12)
#    axes_batt.set_xlabel("Voltage [V]", fontsize=12)
#    axes_batt.set_title("Voltage VS Currents measured by BSP", fontsize=12, weight="bold")
#    axes_batt.grid(True)
#
#
#    return fig_batt


def build_solar_production_figure(total_datalog_df):
    all_channels_labels = list(total_datalog_df.columns)
    chanel_number_for_solar = [
        i for i, elem in enumerate(all_channels_labels) if "Solar power (ALL) [kW]" in elem
    ]

    fig_solar, axes_solar = plt.subplots(nrows=1, ncols=1, figsize=(FIGSIZE_WIDTH, FIGSIZE_HEIGHT))

    total_datalog_df.plot(
        y=total_datalog_df.columns[chanel_number_for_solar],
        ax=axes_solar,
        color=SOLAR_COLOR
    )
    
    axes_solar.set_ylabel("Power [kW]", fontsize=12)
    axes_solar.set_title("Solar Production", fontsize=12, weight="bold")
    axes_solar.grid(True)
    
    fig_solar.figimage(im, 10, 10, zorder=3, alpha=.2)
    fig_solar.savefig("FigureExport/solar_power_profile_figure.png")

    return fig_solar



def build_solar_pv_voltage_figure(total_datalog_df):
    
    all_channels_labels = list(total_datalog_df.columns)
    chanel_number_for_solar_upv = [
        i for i, elem in enumerate(all_channels_labels) if ("Upv" in elem) or ("I15060" in elem) or ("I15059" in elem) or ("I11041" in elem)
    ]
    
    fig_solar_upv, axes_solar_upv = plt.subplots(nrows=1, ncols=1, figsize=(FIGSIZE_WIDTH, FIGSIZE_HEIGHT))

    #maybe it is empty if there is no solar charger:
    if chanel_number_for_solar_upv:
        
        total_datalog_df.plot(
            y=total_datalog_df.columns[chanel_number_for_solar_upv],
            ax=axes_solar_upv,
        )
        axes_solar_upv.set_ylabel("Voltage [Vdc]", fontsize=12)
        axes_solar_upv.set_title("PV input voltage", fontsize=12, weight="bold")
        axes_solar_upv.grid(True)
    else:
        axes_solar_upv.text(0.0, 0.0, "There is no Studer solar charger!", horizontalalignment='left',verticalalignment='bottom')
        axes_solar_upv.set_title("There is no Studer solar charger!", fontsize=12, weight="bold")

    
    fig_solar_upv.figimage(im, 10, 10, zorder=3, alpha=.2)
    fig_solar_upv.savefig("FigureExport/solar_pv_voltages_figure.png")
    
    return fig_solar_upv


def build_solar_energy_prod_figure(total_datalog_df):

    all_channels_labels = list(total_datalog_df.columns)
    chanel_number_for_solar = [i for i, elem in enumerate(all_channels_labels) if "Solar power (ALL) [kW]" in elem]
    day_kwh_df = total_datalog_df.resample("1d").sum() / 60
    month_kwh_df = total_datalog_df.resample("1M").sum() / 60
    
    
    fig_solar, axes_solar = plt.subplots(nrows=2, ncols=1, figsize=(FIGSIZE_WIDTH, FIGSIZE_HEIGHT))
    
    day_kwh_df[day_kwh_df.columns[chanel_number_for_solar]].plot(ax=axes_solar[0],
              kind='line',
              marker='o',
              color=SOLAR_COLOR)
    
    axes_solar[0].set_ylabel("Energy [kWh/day]", fontsize=12)
    axes_solar[0].set_title("PV production per day and per month", fontsize=12, weight="bold")
    axes_solar[0].legend(["Day production"])
    axes_solar[0].grid(True)
    
    
    
    month_kwh_df[month_kwh_df.columns[chanel_number_for_solar]].plot.bar(ax=axes_solar[1],
                          use_index=True)
    
    axes_solar[1].set_ylabel("Energy [kWh/month]", fontsize=12)
    #axes_solar[1].set_title("PV production per month", fontsize=12, weight="bold")
    axes_solar[1].legend(["Month production"])
    axes_solar[1].grid(True)
    
    #replace labels with the month name:
    loc, label= plt.xticks()
    plt.xticks(loc,labels=list(month_kwh_df.index.month_name()), rotation=45, ha = 'right' )

    fig_solar.figimage(im, 10, 10, zorder=3, alpha=.2)
    fig_solar.savefig("FigureExport/solar_daily_monthly_production_figure.png")

    return fig_solar




def build_genset_time_figure(total_datalog_df):
    all_channels_labels = list(total_datalog_df.columns)
    
    fig_transfer = plt.figure()
    ax_transfer = fig_transfer.add_subplot(111)

    #We'll check the transfer of phase 1 only (master)
    chanel_number_for_transfer = [ i for i, elem in enumerate(all_channels_labels) if "I3020 L1" in elem   ]
    if chanel_number_for_transfer: 
        minutes_without_transfer = np.count_nonzero(
            total_datalog_df.values[:, chanel_number_for_transfer] == 0.0
        )
        minutes_with_transfer = np.count_nonzero(
            total_datalog_df.values[:, chanel_number_for_transfer] == 1.0
        )
    
        len(total_datalog_df.values[:, chanel_number_for_transfer])
    
        labels = [
            "On grid/genset: " + str(round(minutes_with_transfer / 60, 1)) + " hours",
            "On inverter: " + str(round(minutes_without_transfer / 60, 1)) + " hours",
        ]
        ax_transfer.pie(
            [minutes_with_transfer, minutes_without_transfer],
            labels=labels,
            shadow=True,
            startangle=90,
            autopct="%1.1f%%",
            colors=[NX_PINK,NX_BLUE],
            wedgeprops=dict(width=0.5),
            explode=(0.1,0.1)
        )
        

#        plt.pie([minutes_with_transfer,minutes_without_transfer],
#                labels=labels,
#                shadow=True, 
#                startangle=90,
#                autopct='%1.1f%%',
#                wedgeprops=dict(width=0.5),
#                colors=[GENSET_COLOR,NX_LIGHT_BROWN])

        ax_transfer.set_title("Connection of the system to the grid/genset", fontsize=12, weight="bold")

    else:
        ax_transfer.set_title("No inverter and no grid/genset in the system", fontsize=12, weight="bold")

    fig_transfer.figimage(im, 10, 10, zorder=3, alpha=.2)
    fig_transfer.savefig("FigureExport/genset_use_figure.png")

    return fig_transfer




def build_genset_VF_behaviour(total_datalog_df):
    all_channels_labels = list(total_datalog_df.columns)
    channel_number_Pin_actif_Tot = [i for i, elem in enumerate(all_channels_labels) if "Pin power (ALL)" in elem]
    channel_number_input_frequency= [i for i, elem in enumerate(all_channels_labels) if "XT-Fin [Hz] I3122 L1" in elem]
    #channel_label_input_frequency=all_channels_labels[channel_number_input_frequency]
    
    #################################
    # frequency of genset in function of power:
    fig_genfreq, axes_genfreq = plt.subplots(nrows=1, ncols=2, figsize=(FIGSIZE_WIDTH, FIGSIZE_HEIGHT))

    #Check it is not empty to be sure there is an XT: for the case with solar chargers only:
    if channel_number_input_frequency:
        
        #total_datalog_df.columns[channels_number_Pin_actif]
        #['XT-Fin [Hz] I3122 L1']
        
            
        axes_genfreq[0].scatter(total_datalog_df[total_datalog_df.columns[channel_number_Pin_actif_Tot]].values,
                          total_datalog_df['XT-Fin [Hz] I3122 L1'].values, 
                          alpha=0.25,
                          color='b')
        
        #axes_genfreq[0].set_ylabel('Frequency [Hz]', fontsize=12)
        #axes_genfreq[0].set_xlabel('Power AC-input [kW]', fontsize=12)
        axes_genfreq[0].set_title('Genset frequency VS power', fontsize=12, weight="bold")
        axes_genfreq[0].grid(True) 
        axes_genfreq[0].set_ylim(45,55)
        
        
        axes_genfreq[1].scatter(total_datalog_df[total_datalog_df.columns[channel_number_Pin_actif_Tot]].values,
                          total_datalog_df['XT-Uin [Vac] I3113 L1'].values, 
                          alpha=0.25,
                          color='r')
        #axes_genfreq[1].set_ylabel('Voltage [Hz]', fontsize=12)
        #axes_genfreq[1].set_xlabel('Power AC-input [kW]', fontsize=12)
        axes_genfreq[1].set_title('Genset voltage VS power', fontsize=12, weight="bold")
        axes_genfreq[1].grid(True) 
        axes_genfreq[1].set_ylim(180,250)
        
    else:
        axes_genfreq[0].set_title('No inverter and no genset in the system', fontsize=12, weight="bold")
        axes_genfreq[1].set_title('No inverter and no genset in the system', fontsize=12, weight="bold")

    axes_genfreq[0].set_ylabel('Frequency [Hz]', fontsize=12)
    axes_genfreq[0].set_xlabel('Power AC-input [kW]', fontsize=12)
    
    axes_genfreq[1].set_ylabel('Voltage [Hz]', fontsize=12)
    axes_genfreq[1].set_xlabel('Power AC-input [kW]', fontsize=12)
    
    #plt.show
    
    fig_genfreq.figimage(im, 10, 10, zorder=3, alpha=.2)
    fig_genfreq.savefig("FigureExport/genset_droops_figure.png")

    return fig_genfreq

    
    
def build_all_battery_voltages_figure(total_datalog_df, month_mean_df):
    all_channels_labels = list(total_datalog_df.columns)
    channels_number_ubat = [i for i, elem in enumerate(all_channels_labels) if "Ubat" in elem]
    fig_batt_anlys, axes_batt_anlys = plt.subplots(nrows=1, ncols=1, figsize=(FIGSIZE_WIDTH, FIGSIZE_HEIGHT))
    # axes4_2 = axes4.twinx()

    total_datalog_df.plot(
        y=total_datalog_df.columns[channels_number_ubat],
        grid=True,
        title="All Battery Voltages",
        ax=axes_batt_anlys,
    )

    month_mean_df.plot(
        y=month_mean_df.columns[channels_number_ubat[1]], color="r", ax=axes_batt_anlys
    )

    axes_batt_anlys.set_ylabel("Voltage [V]", fontsize=12)
    axes_batt_anlys.set_title("All Battery Voltages", fontsize=12, weight="bold")
    axes_batt_anlys.grid(True)
    
    fig_batt_anlys.figimage(im, 10, 10, zorder=3, alpha=.2)
    fig_batt_anlys.savefig("FigureExport/all_batt_voltages_figure.png")

    return fig_batt_anlys


def build_mean_battery_voltage_figure(total_datalog_df, month_mean_df,day_mean_df):
    all_channels_labels = list(month_mean_df.columns)
    channels_number_ubatbsp = [i for i, elem in enumerate(all_channels_labels) if "System Ubat ref [Vdc]" in elem]
    
    #TODO: case sans BSP
    channel_number_ubat_ref= channels_number_ubatbsp[0]
    
    fig_battmeans, axes_battmeans = plt.subplots(nrows=1, ncols=1,figsize=(FIGSIZE_WIDTH, FIGSIZE_HEIGHT))   

    
    day_max_df=total_datalog_df.resample("1d").max()
    day_min_df=total_datalog_df.resample("1d").min()
    
    yminlist=day_min_df[day_min_df.columns[channel_number_ubat_ref]].values.tolist()
    ymaxlist=day_max_df[day_max_df.columns[channel_number_ubat_ref]].values.tolist()
    
    #ymin=np.hstack(yminlist)
    #ymax=np.hstack(ymaxlist)
    #
    #xtime=day_max_df.index
    #
    #
    ##axes_battmeans.fill_between(x, ymin, ymax, alpha=0.4)
    #axes_battmeans.plot(xtime, ymin, color='g', alpha=0.4)
    #
    #axes_battmeans.plot(xtime, ymax, color='r', alpha=0.4)
    


    day_mean_df.plot(y=day_mean_df.columns[channel_number_ubat_ref], 
                     color='r',
                     marker='o',
                     linestyle ='None',
                     grid=True,
                     ax=axes_battmeans,
                     alpha=0.25)
    
    month_mean_df.plot(y=month_mean_df.columns[channel_number_ubat_ref],
                          color='b',
                          marker='x',
                          linestyle ='-',
                          ax=axes_battmeans,
                          drawstyle='steps-post')
    
    
    day_max_df.plot(y=day_max_df.columns[channel_number_ubat_ref],
                          color='y',
                          marker='.',
                          linestyle ='None',
                          alpha=0.2,
                          ax=axes_battmeans)
    day_min_df.plot(y=day_min_df.columns[channel_number_ubat_ref],
                          color='g',
                          marker='.',
                          linestyle ='None',
                          alpha=0.2,
                          ax=axes_battmeans)
    
    axes_battmeans.set_ylabel('Voltage [V]', fontsize=12)
    axes_battmeans.set_title('Monthly and daily mean battery voltages', fontsize=12, weight="bold")
    #axes_battmeans.legend(["Day Mean", "Month Mean"]) 
    axes_battmeans.legend(["Day Mean", "Month Mean","day max", "day min", ])

    axes_battmeans.grid(True) 
    
    fig_battmeans.figimage(im, 10, 10, zorder=3, alpha=.2)
    fig_battmeans.savefig("FigureExport/battmeans_figure.png")

    
    return fig_battmeans


def build_battery_temperature_figure(quarters_mean_df):
    #all_channels_labels = list(total_datalog_df.columns)
    quarters_channels_labels=list(quarters_mean_df.columns)
    
    ####
    # Temperature recorded:
    channels_number_bat_temperature = [i for i, elem in enumerate(quarters_channels_labels) if ('Tbat' in elem)]
    
    fig_batt_temperature, axes_batt_temperature = plt.subplots(nrows=1, 
                               ncols=1,
                               figsize=(FIGSIZE_WIDTH, FIGSIZE_HEIGHT))
    #axes4_2 = axes4.twinx()
    
    quarters_mean_df.plot(y=quarters_mean_df.columns[channels_number_bat_temperature],
                          grid=True,
                          title='Battery Temperature',
                          ax=axes_batt_temperature)
    
    
    axes_batt_temperature.set_ylabel('Temperature [°C]', fontsize=12)
    #axes_batt_temperature.set_title('Batt Temperature', fontsize=12, weight="bold")
    axes_batt_temperature.grid(True) 
    axes_batt_temperature.set_title('Battery Temperature', fontsize=12, weight="bold")
    axes_batt_temperature.grid(True)
   
    fig_batt_temperature.figimage(im, 10, 10, zorder=3, alpha=.2)
    fig_batt_temperature.savefig("FigureExport/bat_temperature.png")

    return fig_batt_temperature








def build_bat_inout_figure(day_kwh_df, month_kwh_df):


    ##############################
    #CHARGE/DISCHARGE ENERGY OF THE BATTERY AND TRHOUGHPUT
    ################
    
    fig_bat_inout, axes_bat_inout = plt.subplots(nrows=2, ncols=1,figsize=(FIGSIZE_WIDTH, FIGSIZE_HEIGHT))
    
    
    
    #Daily:
    #to see both positive on the graph for better comparison:
    
    dischargeEd=-day_kwh_df['System Batt Discharge Power Pbatt [kW]']
    #chargeEd=day_kwh_df['System Batt Charge Power Pbatt [kW]']
    #Create a new entry called System Pin Power [kW]
    day_kwh_df['Abs Discharge']=dischargeEd
    
    
    
    day_kwh_df[['System Batt Charge Power Pbatt [kW]','Abs Discharge']].plot(ax=axes_bat_inout[0],
                          kind='line',
                          marker='o',
                          color=['g', 'r'])
    
    axes_bat_inout[0].legend(["CHARGE", "DISCHARGE"])
    axes_bat_inout[0].grid(True)
    #plt.xticks(np.arange(len(list(day_kwh_df.index))), labels=list(day_kwh_df.index.date), rotation=30, ha = 'center')        
    axes_bat_inout[0].set_ylabel("Energy per day [kWh]", fontsize=12)
    axes_bat_inout[0].set_title("How is the battery used? Daily and monthly cycling (correct only with BSP)", fontsize=12, weight="bold")
    
    
    
    #to see both positive on the graph for better comparison:
    dischargeEm=-month_kwh_df['System Batt Discharge Power Pbatt [kW]']
    chargeEm=month_kwh_df['System Batt Charge Power Pbatt [kW]']
    ind = np.arange(len(list(month_kwh_df.index.month_name())))
    
    
    width = 0.35  # the width of the bars
    b1=axes_bat_inout[1].bar(ind- width/2, chargeEm.values, width, color='g', label='CHARGE')
    b2=axes_bat_inout[1].bar(ind+ width/2, dischargeEm.values, width, color='r', label='DISCHARGE')
    
    
    
    axes_bat_inout[1].set_ylabel("Energy per month [kWh]", fontsize=12)
    #axes_bat_inout.legend(["CHARGE", "DISCHARGE"])
    axes_bat_inout[1].legend()
    axes_bat_inout[1].grid(True)
    plt.xticks(ind, labels=list(month_kwh_df.index.month_name()), rotation=30, ha = 'right')        
  
    fig_bat_inout.figimage(im, 10, 10, zorder=3, alpha=.2)
    fig_bat_inout.savefig("FigureExport/bat_inout.png")

    return fig_bat_inout







#def build_monthly_energies_figure(month_kwh_df):
#    #month_kwh_df = total_datalog_df.resample("1M").sum() / 60
#    fig_ener, axes_ener = plt.subplots(nrows=1, ncols=1, figsize=(FIGSIZE_WIDTH, FIGSIZE_HEIGHT))
#
#    # month_kwh_df['XT-Pout a [kW] I3101 L1-1'].plot(grid=True,
#    #                      kind='line',
#    #                      marker='o',
#    #                      color='red',
#    #                      ax=axes_ener)
#    
#    #normalized energy production
#    normed_solar=month_kwh_df["Solar power (ALL) [kW] I17999 ALL"]/(month_kwh_df["Solar power (ALL) [kW] I17999 ALL"]+month_kwh_df["XT-Pin a [kW] I3119 L1-1"])*100
#    normed_grid=month_kwh_df["XT-Pin a [kW] I3119 L1-1"]/(month_kwh_df["Solar power (ALL) [kW] I17999 ALL"]+month_kwh_df["XT-Pin a [kW] I3119 L1-1"])*100
#    
#    #axes_ener.plot.bar
#    #plt.bar(normed_solar, color='#b5ffb9', edgecolor='white', width=barWidth, label="group A")
#    #plt.bar(normed_grid, bottom=greenBars, color='#f9bc86', edgecolor='white', width=barWidth)
#    
#    normed_solar.plot.bar(grid=True, stacked=True, ax=axes_ener, color=[SOLAR_COLOR, GENSET_COLOR, LOAD_COLOR])
#    normed_grid.plot.bar(grid=True, stacked=True, ax=axes_ener, color=[SOLAR_COLOR, GENSET_COLOR, LOAD_COLOR])
#
##    month_kwh_df[
##        [
##            "Solar power (ALL) [kW] I17999 ALL",
##            "XT-Pin a [kW] I3119 L1-1"
##        ]
##    ].plot.bar(grid=True, stacked=False, ax=axes_ener, color=[SOLAR_COLOR, GENSET_COLOR, LOAD_COLOR])
##        
#    # replace labels with the month name:
#    loc, label = plt.xticks()
#    plt.xticks(loc, labels=list(month_kwh_df.index.month_name()))        
#
#    axes_ener.set_ylabel("Energy fraction [%]", fontsize=12)
#    axes_ener.set_title("Monthly Energy sources shares", fontsize=12, weight="bold")
#    axes_ener.legend(["Solar", "Grid/Genset"]);
#    axes_ener.grid(True)
#    return fig_ener



def build_monthly_energy_sources_fraction_figure(month_kwh_df):

    ############################
    #Montly Energies Fractions:
    #############
    
    all_channels_labels=list(month_kwh_df.columns)
    #quarters_channels_labels=list(quarters_mean_df.columns)
    
    #####################################
    #plot all the channels with SYSTEM Power 
    
    channels_number_PsolarTot = [i for i, elem in enumerate(all_channels_labels) if 'Solar power (ALL) [kW]' in elem]
    channel_number_Pin_actif_Tot = [i for i, elem in enumerate(all_channels_labels) if "Pin power (ALL)" in elem]
    #channel_number_Pout_actif_Tot = [i for i, elem in enumerate(all_channels_labels) if "Pout power (ALL)" in elem]
    
    
     
    #utilisation directe du label plutot que les indexs des columns: 
    #chanel_label_Pout_actif_tot=all_channels_labels[channel_number_Pout_actif_Tot[0]]
    chanel_label_Pin_actif_tot=all_channels_labels[channel_number_Pin_actif_Tot[0]]
    chanel_label_Psolar_tot=all_channels_labels[channels_number_PsolarTot[0]]


    fig_ener, axes_ener = plt.subplots(nrows=1, ncols=1, figsize=(FIGSIZE_WIDTH, FIGSIZE_HEIGHT))
    
    # month_kwh_df['XT-Pout a [kW] I3101 L1-1'].plot(grid=True,
    #                      kind='line',
    #                      marker='o',
    #                      color='red',
    #                      ax=axes_ener)
    
    
    #normalized energy production
    normed_solar=month_kwh_df[chanel_label_Psolar_tot]/(month_kwh_df[chanel_label_Psolar_tot]+abs(month_kwh_df[chanel_label_Pin_actif_tot])+1e-9)*100
    normed_grid=abs(month_kwh_df[chanel_label_Pin_actif_tot])/(month_kwh_df[chanel_label_Psolar_tot]+abs(month_kwh_df[chanel_label_Pin_actif_tot])+1e-9)*100
    
    
    ind = np.arange(len(list(month_kwh_df.index.month_name())))
    p1=axes_ener.bar(ind, normed_solar.values, color=SOLAR_COLOR)
    p2=axes_ener.bar(ind, normed_grid.values, bottom=normed_solar.values, color=GENSET_COLOR)
    
    plt.xticks(ind, labels=list(month_kwh_df.index.month_name()), rotation=30, ha = 'right')        
    
    axes_ener.set_ylabel("Energy fraction [%]", fontsize=12)
    axes_ener.set_title("Where comes energy from? monthly means", fontsize=12, weight="bold")
    axes_ener.legend(["Solar", "Grid/Genset"]);
    axes_ener.grid(True)
    
    fig_ener.figimage(im, 10, 10, zorder=3, alpha=.2)
    fig_ener.savefig("FigureExport/energy_origin.png")

    return fig_ener


def build_sankey_figure(month_kwh_df,year_kwh_df):
    
    
    ################
    #Energy flux
    #https://flothesof.github.io/sankey-tutorial-matplotlib.html
    
    fig_sankey, ax_sankey =plt.subplots(nrows=1, ncols=1,figsize=(FIGSIZE_WIDTH, FIGSIZE_HEIGHT))
    all_channels_labels=month_kwh_df.columns

    channels_number_PsolarTot       = [i for i, elem in enumerate(all_channels_labels) if 'Solar power (ALL) [kW]' in elem]
    channel_number_Pin_actif_Tot    = [i for i, elem in enumerate(all_channels_labels) if "Pin power (ALL)" in elem]
    
    channel_number_Pout_actif_Tot   = [i for i, elem in enumerate(all_channels_labels) if "Pout power (ALL)" in elem]
    channel_number_Pout_conso_Tot   = [i for i, elem in enumerate(all_channels_labels) if "Pout Consumption power (ALL)" in elem]
    channel_number_Pout_ACback_Tot  = [i for i, elem in enumerate(all_channels_labels) if "Pout AC-coupling back (ALL)" in elem]
    
    
    channels_number_Pchargebatt= [i for i, elem in enumerate(all_channels_labels) if "System Batt Charge Power Pbatt" in elem]
    channels_number_Pdischargebatt= [i for i, elem in enumerate(all_channels_labels) if "System Batt Discharge Power Pbatt" in elem]

   
    
    
    last_month_solar=       month_kwh_df[month_kwh_df.columns[channels_number_PsolarTot]].values[-1]
    last_month_grid=        month_kwh_df[month_kwh_df.columns[channel_number_Pin_actif_Tot]].values[-1]
    last_month_chargebatt=  month_kwh_df[month_kwh_df.columns[channels_number_Pchargebatt]].values[-1]
    last_month_dischargebatt=month_kwh_df[month_kwh_df.columns[channels_number_Pdischargebatt]].values[-1]
    last_month_loads=       month_kwh_df[month_kwh_df.columns[channel_number_Pout_conso_Tot]].values[-1]
    
    last_year_solar=        year_kwh_df[year_kwh_df.columns[channels_number_PsolarTot]].values[-1]
    last_year_grid=         year_kwh_df[year_kwh_df.columns[channel_number_Pin_actif_Tot]].values[-1]
    last_year_chargebatt=   year_kwh_df[year_kwh_df.columns[channels_number_Pchargebatt]].values[-1]
    last_year_dischargebatt=year_kwh_df[year_kwh_df.columns[channels_number_Pdischargebatt]].values[-1]
    last_year_loads=        year_kwh_df[year_kwh_df.columns[channel_number_Pout_conso_Tot]].values[-1]
    #channel_number_Pout_conso_Tot
    #channel_number_Pout_actif_Tot
    
    # first diagram
    if False: #True:
        solar_in=abs(last_month_solar)+1e-6
        genset_in=last_month_grid
        tot_chargebatt_out=last_month_chargebatt
        tot_dischargebatt_in=-last_month_dischargebatt
        
        loads_out=last_month_loads
    else:
        solar_in=abs(last_year_solar)+1e-6
        genset_in=last_year_grid
        tot_chargebatt_out=last_year_chargebatt
        tot_dischargebatt_in=-last_year_dischargebatt
        
        loads_out=last_year_loads
    
    #fluxes: 
    tot_prod_in=solar_in+genset_in
    direct_to_loads=loads_out-tot_dischargebatt_in
    losses=tot_prod_in-tot_chargebatt_out-direct_to_loads
    
    
    
    scalesankey=1/(solar_in+genset_in)
    
    sankey = sk.Sankey(ax=ax_sankey, 
                       unit="kWh", 
                       scale=scalesankey,
                       format='%.1f')
    
    sankey.add(flows=[solar_in, genset_in, -tot_prod_in],
               orientations=[1, 0, 0],
               labels=['Solar', 'GENSET', 'TOTAL'],
               pathlengths=[0.3, 0.3, 0.3],
               trunklength=1.0,
               patchlabel="Energy \n production",
               facecolor=NX_BROWN)
    
    sankey.add(flows=[tot_prod_in, -direct_to_loads, -tot_chargebatt_out, -losses ],
               labels=[None, 'direct to loads', 'to battery', "system losses/unmeasured"],
               orientations=[0, 0, -1, 1],
               trunklength=1.0,
               pathlengths=[0.3 ,0.4, 0.3, 0.3],
               prior=0,
               connect=(2, 0),
               facecolor=A_GREY_COLOR3_LIGHT)
    
    sankey.add(flows=[direct_to_loads, tot_dischargebatt_in, -loads_out],
               labels=[None, 'from battery', ' '],
               orientations=[0, -1, 0],
               pathlengths=[0.1 ,0.4, 0.3],
               trunklength=1.0,
               patchlabel="Energy \n consumption",
               prior=1,
               connect=(1, 0),
               facecolor=LOAD_COLOR)
    sankey.finish()
    
    ax_sankey.get_xaxis().set_visible(False)
    ax_sankey.get_yaxis().set_visible(False)
    ax_sankey.spines['bottom'].set_color('white')
    ax_sankey.spines['top'].set_color('white') 
    ax_sankey.spines['right'].set_color('white')
    ax_sankey.spines['left'].set_color('white')
    # basic sankey chart
    #matplotlib.sankey.Sankey(ax=None, scale=1.0, unit='', format='%G', gap=0.25, radius=0.1, shoulder=0.03, offset=0.15, head_angle=100, margin=0.4, tolerance=1e-06, **kwargs)[source]
    
    #sk.Sankey(ax=ax_sankey, flows=[minutes_with_transfer, minutes_without_transfer, -(minutes_with_transfer+minutes_without_transfer)], labels=['First', 'Second', 'Third'], orientations=[ 0, 0, -1]).finish()
    last_year=year_kwh_df.index.year[-1]
    plt.title("Sankey energy flow diagram of system in the recorded data of : " +  str(last_year) + " (available files of this year)" )
    plt.axis('tight')
    plt.axis('equal')

    fig_sankey.figimage(im, 10, 10, zorder=3, alpha=.2)
    fig_sankey.savefig("FigureExport/sankey_figure.png")

    return fig_sankey


def build_daily_energies_figure(day_kwh_df):
    fig_ener, axes_ener = plt.subplots(nrows=1, ncols=1, figsize=(FIGSIZE_WIDTH, FIGSIZE_HEIGHT))

    # month_kwh_df['XT-Pout a [kW] I3101 L1-1'].plot(grid=True,
    #                      kind='line',
    #                      marker='o',
    #                      color='red',
    #                      ax=axes_ener)

    day_kwh_df[
        [
            "Solar power (ALL) [kW] I17999 ALL",
            "System Pin power (ALL) [kW]",
            "System Pout power (ALL) [kW]",
        ]
    ].plot( grid=True, 
                stacked=False, 
                ax=axes_ener, 
                color=[SOLAR_COLOR, GENSET_COLOR, LOAD_COLOR],
                marker="o",
                linestyle="-" #"None"
                )
        
      

    axes_ener.set_ylabel("Energy [kWh]", fontsize=12)
    axes_ener.set_title("Daily Energies", fontsize=12, weight="bold")
    axes_ener.legend(["Solar", "Grid/Genset","Loads"]);
    axes_ener.grid(True)
    
    fig_ener.figimage(im, 10, 10, zorder=3, alpha=.2)
    fig_ener.savefig("FigureExport/daily_energies_figure.png")

    return fig_ener




def build_daily_energies_heatmap_figure(day_kwh_df):
    
    all_channels_labels = list(day_kwh_df.columns)

    channel_number_Pout_actif_Tot = [i for i, elem in enumerate(all_channels_labels) if "System Pout Consumption power (ALL) [kW]" in elem]
    
    
    

    ###############################
    #HEAT MAP OF THE DAY ENERGY
    ###############################
    
    #help and inspiration:
    #https://scipython.com/book/chapter-7-matplotlib/examples/a-heatmap-of-boston-temperatures/
    #https://vietle.info/post/calendarheatmap-python/
    
    
    #select last year of data:
    last_year=day_kwh_df.index.year[-1]
    temp1=day_kwh_df[day_kwh_df.index.year == last_year]
    energies_of_the_year=temp1[day_kwh_df.columns[channel_number_Pout_actif_Tot]]
    #TODO: put NaN in missing days...
    
    #select the year before
    year_before=last_year-1
    temp2=day_kwh_df[day_kwh_df.index.year == year_before]
    energies_of_the_yearbefore=temp2[day_kwh_df.columns[channel_number_Pout_actif_Tot]]
    
    
    # Define Ticks
    DAYS = ['Sun', 'Mon', 'Tues', 'Wed', 'Thurs', 'Fri', 'Sat']
    MONTHS = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'June', 'July', 'Aug', 'Sept', 'Oct', 'Nov', 'Dec']
    
    
    if energies_of_the_yearbefore.empty:    
        #then we have only one year of data :
        number_of_graph=1
        cal={str(last_year): energies_of_the_year}
        fig, ax = plt.subplots(number_of_graph, 1, figsize = (15,6))
        fig.suptitle('Energy consumption in kWh/day in the last year', fontweight = 'bold', fontsize = 12) 
        
        val=str(last_year)
        
        start = cal.get(val).index.min()
        end = cal.get(val).index.max()
        start_sun = start - np.timedelta64((start.dayofweek + 1) % 7, 'D')
        end_sun =  end + np.timedelta64(7 - end.dayofweek -1, 'D')
    
        num_weeks = (end_sun - start_sun).days // 7
        heatmap = np.full([7, num_weeks], np.nan)    
        ticks = {}
        y = np.arange(8) - 0.5
        x = np.arange(num_weeks + 1) - 0.5
        for week in range(num_weeks):
            for day in range(7):
                date = start_sun + np.timedelta64(7 * week + day, 'D')
                if date.day == 1:
                    ticks[week] = MONTHS[date.month - 1]
                if date.dayofyear == 1:
                    ticks[week] += f'\n{date.year}'
                if start <= date < end:
                    heatmap[day, week] = cal.get(val).loc[date, energies_of_the_year.columns[0]]
        mesh = ax.pcolormesh(x, y, heatmap, cmap = 'jet', edgecolors = 'grey')  #cmap = 'jet' cmap = 'inferno'  cmap = 'magma'
    
        ax.invert_yaxis()
    
        # Set the ticks.
        ax.set_xticks(list(ticks.keys()))
        ax.set_xticklabels(list(ticks.values()))
        ax.set_yticks(np.arange(7))
        ax.set_yticklabels(DAYS)
        ax.set_ylim(6.5,-0.5)
        ax.set_aspect('equal')
        ax.set_title(val, fontsize = 15)
    
        # Hatch for out of bound values in a year
        ax.patch.set(hatch='xx', edgecolor='black')
        fig.colorbar(mesh, ax=ax)
        
    
    else:
        #then we have two years of data and we can plot two graphs:
        number_of_graph=2
        cal={str(year_before): energies_of_the_yearbefore, str(last_year): energies_of_the_year}
        fig, ax = plt.subplots(number_of_graph, 1, figsize = (15,6))
        fig.suptitle('Energy consumption in kWh/day in the last 2 years', fontweight = 'bold', fontsize = 12)
      
        
        #for i, val in enumerate(['2018', '2019']):
        for i, val in enumerate(list(cal.keys())):
            
            start = cal.get(val).index.min()
            end = cal.get(val).index.max()
            start_sun = start - np.timedelta64((start.dayofweek + 1) % 7, 'D')
            end_sun =  end + np.timedelta64(7 - end.dayofweek -1, 'D')
        
            num_weeks = (end_sun - start_sun).days // 7
            heatmap = np.full([7, num_weeks], np.nan)    
            ticks = {}
            y = np.arange(8) - 0.5
            x = np.arange(num_weeks + 1) - 0.5
            for week in range(num_weeks):
                for day in range(7):
                    date = start_sun + np.timedelta64(7 * week + day, 'D')
                    if date.day == 1:
                        ticks[week] = MONTHS[date.month - 1]
                    if date.dayofyear == 1:
                        ticks[week] += f'\n{date.year}'
                    if start <= date <= end:
                        heatmap[day, week] = cal.get(val).loc[date, energies_of_the_year.columns[0]]
            mesh = ax[i].pcolormesh(x, y, heatmap, cmap = 'jet', edgecolors = 'grey')  #cmap = 'jet' cmap = 'inferno'  cmap = 'magma'
        
            ax[i].invert_yaxis()
        
            # Set the ticks.
            ax[i].set_xticks(list(ticks.keys()))
            ax[i].set_xticklabels(list(ticks.values()))
            ax[i].set_yticks(np.arange(7))
            ax[i].set_yticklabels(DAYS)
            ax[i].set_ylim(6.5,-0.5)
            ax[i].set_aspect('equal')
            ax[i].set_title(val, fontsize = 15)
        
            # Hatch for out of bound values in a year
            ax[i].patch.set(hatch='xx', edgecolor='black')
            fig.colorbar(mesh, ax=ax[i])
        
        
        # Add color bar at the bottom
        #cbar_ax = fig.add_axes([0.25, 0.10, 0.5, 0.05])
        #fig.colorbar(mesh, orientation="vertical", pad=0.2, cax = cbar_ax)
        #fig.colorbar(mesh, orientation="horizontal", pad=0.2, cax = ax)
        
        
        #colorbar = ax[0].collections[0].colorbar
        #r = colorbar.vmax - colorbar.vmin
        
        fig.subplots_adjust(hspace = 0.5)
    
    
    
    
    
    plt.xlabel('Map of energy consumption in kWh/day', fontsize=12)
    


    fig.figimage(im, 10, 10, zorder=3, alpha=.2)
    fig.savefig("FigureExport/energy_heatmap_figure.png")

    
    return fig



def build_monthly_energies_figure2(month_kwh_df):
    #month_kwh_df = total_datalog_df.resample("1M").sum() / 60
    fig_ener2, axes_ener2 = plt.subplots(nrows=1, ncols=1, figsize=(FIGSIZE_WIDTH, FIGSIZE_HEIGHT))
    
    month_kwh_df[["Solar power (ALL) [kW] I17999 ALL", "System Pin power (ALL) [kW]"]].plot.bar(
        stacked=True, 
        ax=axes_ener2, 
        use_index=False, 
        align="edge", 
        width=0.5,
        color=[SOLAR_COLOR, GENSET_COLOR],
    )



    month_kwh_df["System Pout power (ALL) [kW]"].plot(
        kind="bar",
        align="center",
        width=0.5,
        ax=axes_ener2,
        use_index=False,
        color=LOAD_COLOR,
        alpha=0.5,
    )

    month_kwh_df["System Pout power (ALL) [kW]"].plot(
        kind="line", 
        marker="o", 
        color="red", 
        ax=axes_ener2, 
        use_index=False
    )

    axes_ener2.set_ylabel("Energy [kWh]", fontsize=12)

    # replace labels with the month name:
    loc, label = plt.xticks()
    plt.xticks(loc, labels=list(month_kwh_df.index.month_name()))

    axes_ener2.set_title("Monthly Energies", fontsize=12, weight="bold")
    axes_ener2.legend(["Loads", "Solar", "Grid/Genset"]);
    axes_ener2.grid(True)
    
    fig_ener2.figimage(im, 10, 10, zorder=3, alpha=.2)
    fig_ener2.savefig("FigureExport/monthly_energy_figure.png")
    
    return fig_ener2


#
#def build_monthly_energies_polar_figure(total_datalog_df,month_kwh_df):
#    #month_kwh_df = total_datalog_df.resample("1M").sum() / 60
#    fig_ener2, axes_ener2 = plt.subplots(nrows=1, ncols=1, figsize=(FIGSIZE_WIDTH, FIGSIZE_HEIGHT))
#    
#    month_kwh_df[["Solar power (ALL) [kW] I17999 ALL", "XT-Pin a [kW] I3119 L1-1"]].plot.polar(
#        stacked=True, 
#        ax=axes_ener2, 
#        use_index=False, 
#        align="edge", 
#        width=0.5,
#        color=[SOLAR_COLOR, GENSET_COLOR],
#        legend=['Solar', 'Grid/Genset']
#    )
#
#
#
#    axes_ener2.set_ylabel("Energy [kWh]", fontsize=12)
#
#    # replace labels with the month name:
#    loc, label = plt.xticks()
#    plt.xticks(loc, labels=list(month_kwh_df.index.month_name()))
#
#    axes_ener2.set_title("Monthly Energies", fontsize=12, weight="bold")
#    axes_ener2.legend()
#    axes_ener2.grid(True)
#    return fig_ener2



def main():
    total_datalog_df = pd.read_pickle(xt_all_csv_pandas_import.MIN_DATAFRAME_NAME)
    quarters_mean_df = pd.read_pickle(xt_all_csv_pandas_import.QUARTERS_DATAFRAME_NAME)
    day_mean_df = pd.read_pickle(xt_all_csv_pandas_import.DAY_DATAFRAME_NAME)
    month_mean_df = pd.read_pickle(xt_all_csv_pandas_import.MONTH_DATAFRAME_NAME)
    year_mean_df = pd.read_pickle(xt_all_csv_pandas_import.YEAR_DATAFRAME_NAME)

    #%***************************************
    #% task: compute kWh
    # WARNING: it make sense only for P in KW
    # TODO: make a dataframe for energies
    #%****************************************

    # min to day: *60*24/1000
    # day to month: *60*24/1000

    day_kwh_df = total_datalog_df.resample("1d").sum() / 60
    month_kwh_df = total_datalog_df.resample("1M").sum() / 60
    year_kwh_df = total_datalog_df.resample("1Y").sum() / 60

    # close all existing figures at start
    plt.close("all")

    print(" ")
    print(" __________ GRAPH DISPLAY  _______________ ")
    print(" \n \n \n ")

    all_channels_labels = list(total_datalog_df.columns)
    channels_number_ubat = [i for i, elem in enumerate(all_channels_labels) if "Ubat" in elem]


    ######################################
    # System Power
    ###########################
    # fig100=plt.figure(100)
    build_sys_power_figure(total_datalog_df,quarters_mean_df)
    build_power_histogram_figure(total_datalog_df,quarters_mean_df)
    build_operating_mode_pies(total_datalog_df)

    ######################################
    # AC-details
    ###########################
    build_ac_power_figure(total_datalog_df, quarters_mean_df)
    build_consumption_profile(total_datalog_df)

    ######################
    # Battery analysis
    ######
    build_bsp_voltage_current_figure(total_datalog_df)
    build_total_battery_voltages_currents_figure(total_datalog_df)
    build_battery_voltage_histogram_figure(total_datalog_df, quarters_mean_df)
    build_battery_chargedischarge_histogram_figure(total_datalog_df, quarters_mean_df)
    build_battery_temperature_figure(quarters_mean_df)
                                     
    #build_voltage_versus_current_figure(total_datalog_df)
    build_mean_battery_voltage_figure(total_datalog_df, month_mean_df, day_mean_df)
    build_all_battery_voltages_figure(total_datalog_df, month_mean_df)
    build_bat_inout_figure(day_kwh_df, month_kwh_df)


    #######
    ## Charge /discharge power
    ########
    #    channels_number_ubatbsp = [i for i, elem in enumerate(all_channels_labels) if "BSP-Ubat" in elem]
    #    channels_number_ibatbsp = [i for i, elem in enumerate(all_channels_labels) if "BSP-Ibat" in elem]
    #    battery_power = (
    #        total_datalog_df.values[:, channels_number_ubatbsp]
    #        * total_datalog_df.values[:, channels_number_ibatbsp]
    #        / 1000
    #    )

    # battery_power_df=pd.DataFrame({"Battery Power [kW]": battery_power,
    #                               "Battery Charge Power [kW]": battery_power,
    #                               "Battery Discharge Power [kW]": battery_power},
    #                                index=total_datalog_df.index)
    #
    #

    # plt.show
    
    

    ##########
    # Solar Power:
    ############
    build_solar_production_figure(total_datalog_df)
    build_solar_pv_voltage_figure(total_datalog_df)
    build_solar_energy_prod_figure(total_datalog_df)
    ##########
    # Time on the genset:
    ############
    build_genset_time_figure(total_datalog_df)
    build_genset_VF_behaviour(total_datalog_df)
    # plt.show()

    # Analyse Batterie

    # axes4.bar(x=month_mean_df.index,
    #        y=total_datalog_df.columns[channels_number_ubat],
    #        color='r',
    #        ax=axes4_2)
    #
    # axes4.plot(x=total_datalog_df.index,
    #         y=total_datalog_df.columns[channels_number_ubat],
    #         grid=True,
    #         title='All Battery Voltages',
    #         ax=axes4)
    
    
    ############
    # Bar Monthly and Daily Energies:
    #################3
    
    # month_kwh_df['XT-Pout a [kW] I3101 L1-1']
    #build_monthly_energies_figure(month_kwh_df)
    build_monthly_energies_figure2(month_kwh_df)
    build_monthly_energy_sources_fraction_figure(month_kwh_df)
    
    build_daily_energies_figure(day_kwh_df)
    build_daily_energies_heatmap_figure(day_kwh_df)
    build_sankey_figure(month_kwh_df,year_kwh_df)

    #build_monthly_energies_polar_figure(total_datalog_df,month_kwh_df)
    
    plt.show()


#######
## HEAT MAPS:  TODO  for the daily consumption
########
# https://scipython.com/book/chapter-7-matplotlib/examples/a-heatmap-of-boston-temperatures/
# https://vietle.info/post/calendarheatmap-python/


##minimal battery voltage
# chanel_number=single_days['channels_label'].index('XT-Ubat- (MIN) [Vdc]')
# XT_batt_valmin=total_datalog_value[:,chanel_number]
#
##battery voltage
# chanel_number=single_days['channels_label'].index('XT-Ubat [Vdc]')
# XT_batt_val=total_datalog_value[:,chanel_number]
#
#
# chanel_number=single_days['channels_label'].index('BSP-Ubat [Vdc]')
# BSP_batt_val=total_datalog_value[:,chanel_number]
#
# chanel_number=single_days['channels_label'].index('BSP-Ibat [Adc]')
# BSP_I_batt_val=total_datalog_value[:,chanel_number]
#
##'BSP-Ubat [Vdc]',
## 'BSP-Ibat [Adc]',
## 'BSP-SOC [%]',
## 'BSP-Tbat [°C]',
#
#
#
# chanel_number=single_days['channels_label'].index('XT-Pin a [kW]')
# grid_power=total_datalog_value[:,chanel_number]
#
#
# print(" ************* ")
# print("BEWARE: for 3-phased systems, the sum of the three inverters")
# grid_power=total_datalog_value[:,chanel_number]+total_datalog_value[:,chanel_number+1]+total_datalog_value[:,chanel_number+2]
# print(" comment this line if not the case ")
# print(" ************* ")
# print("  ")
# minutes_of_the_day=total_time_vectors
#
#
#
#
# fig1=plt.figure(1)
# plt.clf()
# plt.plot(minutes_of_the_day/60/24, XT_batt_val, 'b')
# plt.plot(minutes_of_the_day/60/24, BSP_batt_val, 'g')
# plt.plot(minutes_of_the_day/60/24, XT_batt_valmin,'y+-')
#
# plt.xlabel('Time (days)', fontsize=12)
# plt.ylabel('Voltage [V]', fontsize=12)
# plt.title('Battery Voltage', fontsize=18, weight="bold")
#
# plt.ax = fig1.gca()
# plt.ax.grid(True)
#
# plt.show()
# fig1.legend(['mesure XT', 'mesure BSP', 'xt min'])
#
#
# fig2=plt.figure(2)
# plt.clf()
# plt.hist(BSP_batt_val, 25, facecolor='r', alpha=0.75)
#
# plt.xlabel('Voltage [V]')
# plt.ylabel('Occurence')
# plt.title('Histogram of Battery Voltage')
#
##plt.text(52, 25, r'$\mu=100,\ \sigma=15$')
##plt.axis([40, 60, 0, 0.03])
# plt.grid(True)
# plt.show()
#
# plt.ax = fig2.gca()
# plt.ax.grid(True)
#
#
#


if __name__ == "__main__":
    main()
