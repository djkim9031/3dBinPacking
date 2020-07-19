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
