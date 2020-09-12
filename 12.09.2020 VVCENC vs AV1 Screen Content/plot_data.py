 #!/usr/bin/env python3

import matplotlib.pyplot as plt
from matplotlib.cm import get_cmap
import matplotlib
import statistics
import sys
from ast import literal_eval
from scipy import interpolate
import numpy as np

def plot_range(data, color, encoder, m_place):
    cpus = set([x[2] for x in data])
    cmap = plt.get_cmap(color)
    colors = list(cmap(np.linspace(0.3, 0.9, len(set([x[2] for x in data])))))
    for cpu in cpus:
        dt = [x for x in data if x[2] == cpu]
        x = sorted([round(x[4])for x in dt])
        y = sorted([x[m_place] for x in dt])
        time = sum([x[1] for x in dt])/len(dt)
        f = interpolate.interp1d(x, y, kind='quadratic')
        xnew = np.linspace(min(x), max(x), max(x) - min(x) )
        plt.plot(xnew, f(xnew), label=f'{encoder} {cpu}, Average Time: {round(time)}', linewidth=3, c=colors.pop())

if __name__ == "__main__":

    files = sys.argv[1:]
    print(files)

    data = []

    for file in files:
        with open(file) as f:
            print(file)
            dt = literal_eval(f.readline())

            data.extend(dt)

    aom_data = [x for x in data if x[0] == 'aom']
    vvc_data = [x for x in data if x[0] == 'vvc']

    codecs = sorted(list(set([x[0] for x in data])))
    codecs = [x.upper() for x in codecs]
    print(codecs)
    for metric, place in [('VMAF', 5), ('PSNR', 6), ('SSIM', 7), ('MS-SSIM', 8)]:

        plt.plot([], [], ' ', label='Xiph 1080p 50fps Camera Footage "park_joy"')
        plot_range(aom_data, 'Blues', 'Aomenc', place)
        plot_range(vvc_data, 'Reds', 'VVC', place)
        # Plot

        plt.xticks([x for x in range(0, 40000, 1000)], [int(x) for x in range(0, 40) ],fontsize=26)

        if metric in ('VMAF', 'PSNR'):
            plt.yticks([x for x in range(0, 101, 1)], fontsize =28)
            [plt.axhline(i, color='grey', linewidth=0.5) for i in range(1, 100, 2)]
            [plt.axhline(i, color='black', linewidth=1) for i in range(0, 100, 2)]
        else:
            [plt.axhline(i/100, color='grey', linewidth=0.5) for i in range(61, 1000, 2)]
            [plt.axhline(i/100, color='black', linewidth=1) for i in range(62, 1000, 2)]
            plt.yticks([x/100 for x in range(0, 1000, 1)], fontsize =28)

        plt.subplots_adjust(left=0.05, right=0.9, top=0.9, bottom=0.1)

        [plt.axvline(i, color='grey', linewidth=0.3) for i in range(0, 40000, 500)]
        plt.ylabel(metric.capitalize(), size=32)
        plt.xlabel('Bit rate', size=24)
        plt.title(f"{' vs '.join(codecs)}, latest git 10.09.2020 {metric}", size=28)
        plt.legend(prop={'size': 19}, loc="lower right")

        # low_xlim = min([x[4] for x in data])
        low_ylim = min([x[place] for x in data])
        plt.xlim(3000,30000)

        if metric == 'VMAF':
            high_ylim = 100
        else:
            high_ylim = max([x[place] for x in data])

        plt.ylim((low_ylim, high_ylim))
        plt.margins(0)
        plt.subplots_adjust(left=0.060, right=0.995, top=0.965, bottom=0.065)
        plt.show()
