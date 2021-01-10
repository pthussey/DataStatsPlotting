import numpy as np
import pandas as pd

import matplotlib
import matplotlib.pyplot as plt
import seaborn as sns


# Sets the default rc parameters for plotting
def SetParams(font='Malgun Gothic', basesize=12, basecolor='0.4'):
    plt.rcParams["font.family"] = font
    plt.rcParams["font.size"] = basesize
    plt.rcParams["xtick.labelsize"] = basesize
    plt.rcParams["ytick.labelsize"] = basesize
    plt.rcParams["legend.fontsize"] = basesize
    plt.rcParams["axes.titlesize"] = basesize+2
    plt.rcParams["axes.titleweight"] = 'bold'
    plt.rcParams["axes.labelsize"] = basesize+1
    plt.rcParams["text.color"] = basecolor
    plt.rcParams["axes.labelcolor"] = basecolor
    plt.rcParams["axes.edgecolor"] = basecolor
    plt.rcParams["xtick.color"] = basecolor
    plt.rcParams["ytick.color"] = basecolor
    plt.rcParams["ytick.left"]: True
    plt.rcParams["xtick.bottom"]: True
    plt.rcParams["axes.labelpad"] = basesize


def Despine(ax, spines='topright'):
    if spines == 'all':
        ax.spines['right'].set_visible(False)
        ax.spines['top'].set_visible(False)
        ax.spines['left'].set_visible(False)
        ax.spines['bottom'].set_visible(False)
        ax.tick_params(axis='both', length=0.0)
    elif spines == 'toprightleft':
        ax.spines['right'].set_visible(False)
        ax.spines['top'].set_visible(False)
        ax.spines['left'].set_visible(False)
        ax.tick_params(axis='y', length=0.0)
    else:
        ax.spines['right'].set_visible(False)
        ax.spines['top'].set_visible(False)


def AnnotateBars(rects, color='0.4', orient='v', offset=3, weight='normal', digits=0, percent=False):
    """Attaches a text label for each bar in a bar plot. 
    If using seaborn, must save plot to a variable 
    and pass the patches (ex. g.patches) for the rects parameter."""
    if orient == 'h':
        for rect in rects:
            width = rect.get_width()
            if percent == True:
                form='{:.'+str(digits)+'f'+'}%'
            else:
                form='{:.'+str(digits)+'f'+'}'
            plt.annotate(form.format(width),
                    xy=(width, rect.get_y() + rect.get_height() / 2),
                    xytext=(offset, 0),
                    textcoords="offset points",
                    ha='left', va='center',
                    weight=weight, color=color)
    else:
        for rect in rects:
            height = rect.get_height()
            if percent == True:
                form='{:.'+str(digits)+'f'+'}%'
            else:
                form='{:.'+str(digits)+'f'+'}'
            plt.annotate(form.format(height),
                        xy=(rect.get_x() + rect.get_width() / 2, height),
                        xytext=(0, offset),
                        textcoords="offset points",
                        ha='center', va='bottom',
                        weight=weight, color=color)


def AnnotatePointAbove(coord, color='0.4', weight='normal', fontsize=12, ha='center', offset=10, decpoints=1):
    form = '{:.' + str(decpoints) + 'f}'
    plt.annotate(form.format(coord[1]),
                 xy=(coord), xytext=(0, offset),
                 textcoords="offset points",
                 ha=ha, va='bottom',
                 fontsize=fontsize,
                 weight=weight, color=color)


def AnnotatePointBelow(coord, color='0.4', weight='normal', fontsize=12, ha='center', offset=10, decpoints=1):
    form = '{:.' + str(decpoints) + 'f}'
    plt.annotate(form.format(coord[1]),
                 xy=(coord), xytext=(0, -offset),
                 textcoords="offset points",
                 ha=ha, va='top',
                 fontsize=fontsize,
                 weight=weight, color=color)


def AnnotatePointLeft(coord, color='0.4', weight='normal', fontsize=12, va='center', offset=10, decpoints=1):
    form = '{:.' + str(decpoints) + 'f}'
    plt.annotate(form.format(coord[1]),
                 xy=(coord), xytext=(-offset, 0),
                 textcoords="offset points",
                 ha='right', va=va,
                 fontsize=fontsize,
                 weight=weight, color=color)


def AnnotatePointRight(coord, color='0.4', weight='normal', fontsize=12, va='center', offset=10, decpoints=1):
    form = '{:.' + str(decpoints) + 'f}'
    plt.annotate(form.format(coord[1]),
                 xy=(coord), xytext=(offset, 0),
                 textcoords="offset points",
                 ha='left', va=va,
                 fontsize=fontsize,
                 weight=weight, color=color)


def AnnotateLine(xs, ys, color='0.4', weight='normal', fontsize=12, offset=10, decpoints=1):
    d = dict(zip(range(len(xs)), list(zip(xs,ys)))) # Dict of coordinates
    
    for k, coord in d.items():
        if k == 0: # Annotate first point in the line
            if d[k+1][1] > d[k][1]:
                AnnotatePointBelow(coord, color=color,
                                   weight=weight,fontsize=fontsize,
                                   offset=offset, decpoints=decpoints)
            else:
                AnnotatePointAbove(coord, color=color,
                                   weight=weight, fontsize=fontsize,
                                   offset=offset, decpoints=decpoints)
                
        elif k == len(xs)-1: # Annotate final point in the line
            if d[k-1][1] > d[k][1]:
                AnnotatePointBelow(coord, color=color,
                                   weight=weight, fontsize=fontsize,
                                   offset=offset, decpoints=decpoints)
            else:
                AnnotatePointAbove(coord, color=color,
                                   weight=weight, fontsize=fontsize,
                                   offset=offset, decpoints=decpoints)
                
        else: # Annotate all other points
            if (d[k-1][1] <= d[k][1]) & (d[k+1][1] <= d[k][1]): # Lines form a peak at the point
                AnnotatePointAbove(coord, color=color,
                                   weight=weight, fontsize=fontsize,
                                   offset=offset, decpoints=decpoints)
                
            elif (d[k-1][1] > d[k][1]) & (d[k+1][1] > d[k][1]): # Lines form a trough at the point
                AnnotatePointBelow(coord, color=color,
                                   weight=weight, fontsize=fontsize,
                                   offset=offset, decpoints=decpoints)
                
            else:
                # Vectors to use to determine where the annotation needs to go in edge cases
                v0 = np.array(d[k-1]) - np.array(d[k]) # Incoming line vector
                v1 = np.array(d[k+1]) - np.array(d[k]) # Outgoing line vector
                v2 = np.array((d[k-1][0], d[k][1])) - np.array(d[k]) # Incoming horizontal vector
                v3 = np.array((d[k+1][0], d[k][1])) - np.array(d[k]) # Outgoing horizontal vector
                
                # Angles to use to determine where the annotation needs to go in edge cases
                int_angle = np.math.atan2(np.linalg.det([v0,v1]), np.dot(v0,v1)) # The signed interior angle between v0 and v1
                in_hangle = np.math.atan2(np.linalg.det([v0,v2]), np.dot(v0,v2)) # The signed angle between v0 and v2
                out_hangle = np.math.atan2(np.linalg.det([v1,v3]), np.dot(v1,v3)) # The signed angle between v1 and v3
                
                if (d[k-1][1] <= d[k][1]) & (int_angle >= 0): # Incoming line slopes up and interior angle is positive
                    if abs(np.degrees(in_hangle)) < 26: # Angle between incoming line and horizontal is small
                        print(1, k, np.degrees(in_hangle))
                        AnnotatePointAbove(coord, color=color, ha='right',
                                           weight=weight, fontsize=fontsize,
                                           offset=offset, decpoints=decpoints)
                    else:
                        AnnotatePointLeft(coord, color=color,
                                          weight=weight, fontsize=fontsize,
                                          offset=offset, decpoints=decpoints)
                
                elif (d[k-1][1] <= d[k][1]) & (int_angle < 0): # Incoming line slopes up and interior angle is negative
                    if abs(np.degrees(out_hangle)) < 26: # Angle between outgoing line and horizontal is small
                        print(2, k, np.degrees(out_hangle))
                        AnnotatePointBelow(coord, color=color, ha='left',
                                           weight=weight, fontsize=fontsize,
                                           offset=offset, decpoints=decpoints)
                    else:
                        AnnotatePointRight(coord, color=color,
                                           weight=weight, fontsize=fontsize,
                                           offset=offset, decpoints=decpoints)
                        
                elif (d[k-1][1] >= d[k][1]) & (int_angle >= 0): # Incoming line slopes down and interior angle is positive
                    if abs(np.degrees(out_hangle)) < 26: # Angle between outgoing line and horizontal is small
                        print(3, k, np.degrees(out_hangle))
                        AnnotatePointAbove(coord, color=color, ha='left',
                                           weight=weight, fontsize=fontsize,
                                           offset=offset, decpoints=decpoints)
                    else:
                        AnnotatePointRight(coord, color=color,
                                           weight=weight, fontsize=fontsize,
                                           offset=offset, decpoints=decpoints)


def main():
    pass

if __name__ == '__main__':
    main()