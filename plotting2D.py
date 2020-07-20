from bokeh.plotting import figure, output_file, show 

# instantiating the figure object  
graph = figure(title = "Bokeh Rectangle Graph")  

# name of the x-axis  
graph.xaxis.axis_label = "x-axis"

# name of the y-axis  
graph.yaxis.axis_label = "y-axis"

# points to be plotted 
x = [] 
y = [] 
w= [] 
h = [] 
color = []
fill_alpha = []
for i in a.items:
    w_ = i.dimension[0]
    h_ = i.dimension[1]
    x_ = i.position[0]+ w_/2
    y_ = -i.position[1] - h_/2
    w.append(w_)
    h.append(h_)
    x.append(x_)
    y.append(y_)
    color.append("yellow")
    fill_alpha.append(i.dimension[2]/a.depth)


# plotting the graph  
graph.rect(x, 
           y, 
           w, 
           h, 
           color = color, 
           fill_alpha = fill_alpha)  

# displaying the model  
show(graph)
