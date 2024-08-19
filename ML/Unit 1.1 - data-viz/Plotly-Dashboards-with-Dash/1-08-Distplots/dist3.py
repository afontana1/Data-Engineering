#######
# This distplot looks back at the Mark Twain/
# Quintus Curtius Snodgrass data and tries
# to compare them.
######
import plotly.offline as pyo
import plotly.figure_factory as ff

snodgrass = [0.209, 0.205, 0.196, 0.210, 0.202, 0.207, 0.224, 0.223, 0.220, 0.201]
twain = [0.225, 0.262, 0.217, 0.240, 0.230, 0.229, 0.235, 0.217]

hist_data = [snodgrass, twain]
group_labels = ["Snodgrass", "Twain"]

fig = ff.create_distplot(hist_data, group_labels, bin_size=[0.005, 0.005])
pyo.plot(fig, filename="SnodgrassTwainDistplot.html")
