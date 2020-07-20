# 3dBinPacking
3d Bin Packing - Currently focusing primarily on 3D-Knapsack problem in packing

Primary architecture developed at https://github.com/enzoruiz/3dbinpacking
- I am using the main architectural style proposed here, but I've made quite a few significant changes in that the main source code is not accurate when items get stacked in z-dimensions.

List of changes implemented:
1. In xy-plane, items were stacked if they could fit in Width-dimension (x) and Height-Dimension (y) by rotating them in 6 all possible orientations. However, xy-plane stackabilities were calculated from an already-stacked item's top-left corner point (min(x),min(y) of the already stacked item - I used unsigned 4th quadrant for xy-plane) with either width or height value of the already-stacked item at a time. This made items (if they could fit in the bin) to be stacked only from two possible points (top right and bottom left point of the already-stacked item)
-> This was changed to allow items to be stacked in bottom right corner of the already-stacked item as well (both in -x direction and -y direction from there), which led to far better space efficiency

2. Once the base-layer(z=0) is filled, items with equal z-values (Not necessarily item's original depth value since it could've been reoriented) were identified. This made it possible to identify the min(z) value, on which items that can't fit at z=0 can be stacked if the next layer provides more space.
-> For instance, if items stacked at z=0 has z=1, z=2, z=3 values respectively and a new item to be stacked cannot fit at z=0, it checks whether it can be stacked at z=1. If it can't, it checks for its stackability at z=2, then z=3, etc. This is done while comparing the new item's z-value from the layer it is stacked on and the total depth of the bin.

3. Created an area mask
-> If a bigger object is stacked at for example z=1 while there is still some space beneath it at z=0, and a new item to be stacked can fit at z=0 under that big object, then the new item does not go under that spot at z=0 (for realisitic palletizing/bin packing). Instead it looks for possible space at z=0 which isn't masked by other objects on top, or simply get stacked at another layer which isn't masked.

4. Center of Gravity [Rather, percentage of rectanglular portion that is stacked on top of other items] calculation for its stackability at another layer
-> sometimes, for instance, if z=0 is filled by one tiny object and a new item to be stacked has identical x,y dimensions as xy-plane of the bin (provided it cannot be reoriented due to its depth as well), this item gets stacked on that tiny object; The big object should be stacked only when certain % of its area is directly on top of other objects (perhaps <50% in ideal case, but I set the threshhold to 60% for more realistic cases)

5. 2D and 3D visulization
-> 2D for xy-plane visualization (Accurate)
-> 3D for overall visualization (The library used seems to render graphics erroneously in some cases, but in terms of understanding how items are stacked it works just as well!


TODO list:
Stacking items are current done by referencing other stacked objects' vertices.
This works well for most cases; but in a rare case where referencing a stacked object's (e.g., at layer z=1) vertix makes the item float and thus puts it in a situation where the shared area with other stacked objects underneath (e.g., at z=0) is <60% (From 4.) -> In this case, the item is not stacked even though there is enough space and utilizing this space could give the shared area >60%.
