from mpl_toolkits.mplot3d import Axes3D
import numpy as np
import matplotlib.pyplot as plt

def cuboid_data(o, size=(1,1,1)):
    # suppose axis direction: x: to left; y: to inside; z: to upper
    # get the length, width, and height
    l, w, h = size
    x = [[o[0], o[0] + l, o[0] + l, o[0], o[0]],  
         [o[0], o[0] + l, o[0] + l, o[0], o[0]],  
         [o[0], o[0] + l, o[0] + l, o[0], o[0]],  
         [o[0], o[0] + l, o[0] + l, o[0], o[0]]]  
    y = [[-o[1], -o[1], -o[1] - w, -o[1] - w, -o[1]],  
         [-o[1], -o[1], -o[1] - w, -o[1] - w, -o[1]],  
         [-o[1], -o[1], -o[1], -o[1], -o[1]],          
         [-o[1] - w, -o[1] - w, -o[1] - w, -o[1] - w, -o[1] - w]]   
    z = [[o[2], o[2], o[2], o[2], o[2]],                       
         [o[2] + h, o[2] + h, o[2] + h, o[2] + h, o[2] + h],   
         [o[2], o[2], o[2] + h, o[2] + h, o[2]],               
         [o[2], o[2], o[2] + h, o[2] + h, o[2]]]               
    return np.array(x), np.array(y), np.array(z)

def plotCubeAt(pos=(0,0,0), size=(1,1,1), ax=None,**kwargs):
    # Plotting a cube element at position pos
    if ax !=None:
        X, Y, Z = cuboid_data( pos, size )
        ax.plot_surface(X, Y, Z, rstride=1, cstride=1, **kwargs)
        
positions=[]
sizes=[]
colors=[]
for key,item in enumerate(a.items):
    (x,y,z)=item.position
    (w,h,d)=item.dimension
    position=(float(x),float(y),float(z))
    size=(float(w),float(h),float(d))
    color=(1/(key+1),1,0.02*key)
    positions.append(position)
    sizes.append(size)
    colors.append(color)


fig = plt.figure()
ax = fig.gca(projection='3d')
#ax.set_aspect('equal')

for p,s,c in zip(positions,sizes,colors):
    plotCubeAt(pos=p, size=s, ax=ax, color=c)

plt.show()
