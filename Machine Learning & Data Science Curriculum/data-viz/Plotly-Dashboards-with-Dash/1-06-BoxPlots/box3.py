#######
# This plot compares sample distributions
# of three-letter-words in the works of
# Quintus Curtius Snodgrass and Mark Twain
######
import plotly.offline as pyo
import plotly.graph_objs as go

snodgrass = [0.209, 0.205, 0.196, 0.210, 0.202, 0.207, 0.224, 0.223, 0.220, 0.201]
twain = [0.225, 0.262, 0.217, 0.240, 0.230, 0.229, 0.235, 0.217]

data = [go.Box(y=snodgrass, name="QCS"), go.Box(y=twain, name="MT")]
layout = go.Layout(
    title="Comparison of three-letter-word frequencies<br>\
    between Quintus Curtius Snodgrass and Mark Twain"
)
fig = go.Figure(data=data, layout=layout)
pyo.plot(fig, filename="box3.html")
