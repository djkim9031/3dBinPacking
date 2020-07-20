from py3dbp import Packer, Bin, Item

packer = Packer()

a= Bin('large-3-box', 23.6875, 11.2, 35.0, 1000.0)
#packer.add_bin(Bin('small-envelope', 11.5, 6.125, 0.25, 10))
#packer.add_bin(Bin('large-envelope', 15.0, 12.0, 0.75, 15))
#packer.add_bin(Bin('small-box', 8.625, 5.375, 1.625, 70.0))
#packer.add_bin(Bin('medium-box', 11.0, 8.5, 5.5, 70.0))
#packer.add_bin(Bin('medium-2-box', 13.625, 11.875, 3.375, 70.0))
#packer.add_bin(Bin('large-box', 12.0, 12.0, 5.5, 70.0))
#packer.add_bin(Bin('large-2-box', 23.6875, 11.75, 3.0, 70.0))
packer.add_bin(a)

packer.add_item(Item('1', 3.9370, 1.9685, 11.9685, 1))
packer.pack()
#packer.add_item(Item('2', 23.6875, 11.2, 30, 10))
#packer.pack()
packer.add_item(Item('2', 3.9370, 1.9685, 1.9685, 2))
packer.pack()
packer.add_item(Item('3', 3.9370, 1.9685, 1.9685, 3))
packer.pack()
packer.add_item(Item('4', 7.8740, 3.9370, 1.9685, 4))
packer.pack()
packer.add_item(Item('5', 7.8740, 3.9370, 1.9685, 5))
packer.pack()
packer.add_item(Item('6', 7.8740, 3.9370, 1.9685, 6))
packer.pack()
packer.add_item(Item('7', 15.5, 6, 20, 6))
packer.pack()
packer.add_item(Item('8', 7.8740, 3.9370, 1.9685, 7))
packer.pack()
packer.add_item(Item('9', 7.8740, 3.9370, 1.9685, 8))
packer.pack()
packer.add_item(Item('10', 7.8740, 3.9370, 1.9685, 9))
packer.pack()
packer.add_item(Item('11', 7.8740, 3.9370, 1.9685, 10))
packer.pack()
packer.add_item(Item('12', 7.8740, 3.9370, 1.9685, 11))
packer.pack()
packer.add_item(Item('250g [powder 11]', 7, 3.770, 3.9685, 11))
packer.pack()
packer.add_item(Item('7', 15.5, 6, 10, 6))
packer.pack()



#packer.add_item(Item('250g [powder 12]', 7.8740, 3.9370, 1.9685, 6))
#packer.pack()
#packer.add_item(Item('250g [powder 7]', 7.8740, 3.9370, 1.9685, 7))
#packer.pack()
#packer.add_item(Item('250g [powder 8]', 7.8740, 3.9370, 1.9685, 8))
#packer.pack()



#packer.add_item(Item('250g [powder 9]', 7.8740, 3.9370, 1.9685, 9))
#packer.add_item(Item('250g [powder 4]', 7.8740, 3.9370, 1.9685, 4))
#packer.add_item(Item('250g [powder 5]', 7.8740, 3.9370, 1.9685, 5))
#packer.add_item(Item('250g [powder 6]', 7.8740, 3.9370, 1.9685, 6))
#packer.add_item(Item('250g [powder 7]', 7.8740, 3.9370, 1.9685, 7))
#packer.add_item(Item('250g [powder 8]', 7.8740, 3.9370, 1.9685, 8))
#packer.add_item(Item('250g [powder 9]', 7.8740, 3.9370, 1.9685, 9))

#packer.pack()

for b in packer.bins:
    print(":::::::::::", b.string())

    print("FITTED ITEMS:")
    for item in b.items:
        print("====> ", item.string())

    print("UNFITTED ITEMS:")
    for item in b.unfitted_items:
        print("====> ", item.string())

    print("***************************************************")
    print("***************************************************")
    
    
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
