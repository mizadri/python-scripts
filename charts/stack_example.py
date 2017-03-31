"""
Bar chart demo with pairs of bars grouped for easy comparison.
"""
import numpy as np
import matplotlib.pyplot as plt


n_groups = 3

means_e1 = (20, 35, 30)
std_e1 = (2, 3, 4)

means_e2 = (25, 32, 34)
std_e2 = (3, 5, 2)

means_e3 = (5, 2, 4)
std_e3 = (0.3, 0.5, 0.2)

fig, ax = plt.subplots()

index = np.arange(n_groups)
bar_width = 0.35

opacity = 0.4
error_config = {'ecolor': '0.3'}

rects1 = plt.bar(index , means_e1, bar_width,
                 alpha=opacity,
                 color='b',
                 yerr=std_e1,
                 error_kw=error_config,
                 label='Main')

rects2 = plt.bar(index + bar_width + 0.1, means_e2, bar_width,
                 alpha=opacity,
                 color='r',
                 yerr=std_e2,
                 error_kw=error_config,
                 label='e2')

rects3 = plt.bar(index + bar_width + bar_width + 0.2, means_e3, bar_width,
                 alpha=opacity,
                 color='g',
                 yerr=std_e3,
                 error_kw=error_config,
                 label='e3')

plt.xlabel('Dataset type used')
plt.ylabel('Percentage of reads joined after normalisation to 1 million reads')
plt.title('Application of Thimble on datasets, showing the ability of each stitcher option.')
plt.xticks(index + bar_width + bar_width, ('1', '2', '3'))
plt.legend()

plt.tight_layout()
plt.show()