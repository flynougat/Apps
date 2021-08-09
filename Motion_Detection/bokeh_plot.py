from bokeh.models.sources import ColumnDataSource
from bokeh.models.tools import HoverTool
from video_capture import df
from bokeh.plotting import figure, show, output_file

#use Hover to add tag
#Hover can only display string, need convert datetime to string
df["Start_str"]=df["Start"].dt.strftime("%Y-%m-%d, %H:%M:%S")
df["End_str"]=df["End"].dt.strftime("%Y-%m-%d, %H:%M:%S")
print(df)

top=[]
bottom=[]
i = 0
while i < len(df["Start"]):
    top.append(1)
    bottom.append(0)
    i=i+1

cds = ColumnDataSource(dict(
    left=df["Start"],
    right=df["End"],
    Start_str = df["Start_str"],
    End_str = df["End_str"],
    top = top,
    bottom = bottom,
))

p=figure(x_axis_type='datetime', height = 100, width = 500, sizing_mode='scale_both', title = "Time Motion is Detected")
p.yaxis.minor_tick_line_color=None
#p.ygrid[0].ticker.desired_num_ticks=1   try to remove grid line

hover = HoverTool(tooltips=[("Start","@Start_str"), ("End", "@End_str")])

q=p.quad(left="left", right="right", top="top", bottom="bottom", color="orange", source = cds)
p.add_tools(hover)

output_file("motion_graph.html")
show(p)