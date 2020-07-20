from .constants import RotationType, Axis
from .auxiliary_methods import intersect, set_to_decimal

DEFAULT_NUMBER_OF_DECIMALS = 3
START_POSITION = [0, 0, 0]


class Item:
    def __init__(self, name, width, height, depth, weight):
        self.name = name
        self.width = width
        self.height = height
        self.depth = depth
        self.weight = weight
        self.rotation_type = 0
        self.position = START_POSITION
        self.number_of_decimals = DEFAULT_NUMBER_OF_DECIMALS
        self.dimension = [0,0,0]
        self.position_elevated = [0,0,0] #Depth(Actually height but in this coding, W*L*H convention is Width*Height*Depth) value in terms of total elevation from z=0
  
    def format_numbers(self, number_of_decimals):
        self.width = set_to_decimal(self.width, number_of_decimals)
        self.height = set_to_decimal(self.height, number_of_decimals)
        self.depth = set_to_decimal(self.depth, number_of_decimals)
        self.weight = set_to_decimal(self.weight, number_of_decimals)
        self.number_of_decimals = number_of_decimals

    def string(self):
        return "%s(%sx%sx%s, weight: %s) pos(%s)- dim(%s) rt(%s) vol(%s)" % (
            self.name, self.width, self.height, self.depth, self.weight,
            self.position, self.dimension, self.rotation_type, self.get_volume()
        )

    def get_volume(self):
        return set_to_decimal(
            self.width * self.height * self.depth, self.number_of_decimals
        )

    def get_dimension(self):
        if self.rotation_type == RotationType.RT_WHD:
            dimension = [self.width, self.height, self.depth]
            self.dimension = dimension
            self.position_elevated = [self.position[0],self.position[1],self.position[2]+dimension[2]]
        elif self.rotation_type == RotationType.RT_HWD:
            dimension = [self.height, self.width, self.depth]
            self.dimension = dimension
            self.position_elevated = [self.position[0],self.position[1],self.position[2]+dimension[2]]
        elif self.rotation_type == RotationType.RT_HDW:
            dimension = [self.height, self.depth, self.width]
            self.dimension = dimension
            self.position_elevated = [self.position[0],self.position[1],self.position[2]+dimension[2]]
        elif self.rotation_type == RotationType.RT_DHW:
            dimension = [self.depth, self.height, self.width]
            self.dimension = dimension
            self.position_elevated = [self.position[0],self.position[1],self.position[2]+dimension[2]]
        elif self.rotation_type == RotationType.RT_DWH:
            dimension = [self.depth, self.width, self.height]
            self.dimension = dimension
            self.position_elevated = [self.position[0],self.position[1],self.position[2]+dimension[2]]
        elif self.rotation_type == RotationType.RT_WDH:
            dimension = [self.width, self.depth, self.height]
            self.position_elevated = [self.position[0],self.position[1],self.position[2]+dimension[2]]
            self.dimension = dimension
        else:
            dimension = [0,0,0]
            self.dimension = dimension
            self.position_elevated = [0,0,0]

        return dimension


class Bin:
    def __init__(self, name, width, height, depth, max_weight):
        self.name = name
        self.width = width
        self.height = height
        self.depth = depth
        self.max_weight = max_weight
        self.items = []
        self.unfitted_items = []
        self.number_of_decimals = DEFAULT_NUMBER_OF_DECIMALS
        
        #For layers at z>0 calculations - These are temporary values
        self.item_depths = []
        self.apparent_items = []

    def format_numbers(self, number_of_decimals):
        self.width = set_to_decimal(self.width, number_of_decimals)
        self.height = set_to_decimal(self.height, number_of_decimals)
        self.depth = set_to_decimal(self.depth, number_of_decimals)
        self.max_weight = set_to_decimal(self.max_weight, number_of_decimals)
        self.number_of_decimals = number_of_decimals

    def string(self):
        return "%s(%sx%sx%s, max_weight:%s) vol(%s)" % (
            self.name, self.width, self.height, self.depth, self.max_weight,
            self.get_volume()
        )

    def get_volume(self):
        return set_to_decimal(
            self.width * self.height * self.depth, self.number_of_decimals
        )

    def get_total_weight(self):
        total_weight = 0

        for item in self.items:
            total_weight += item.weight

        return set_to_decimal(total_weight, self.number_of_decimals)

    def put_item(self, item, pivot, axis, w):
        fit = False
        valid_item_position = item.position
        item.position = pivot

        for i in range(0, len(RotationType.ALL)):
            if pivot[2]>0:
                break
            item.rotation_type = i
            dimension = item.get_dimension()
            if axis == 1:
                #Height(L), Height(R) Check - when height_l is false, check height_r validity
                
                if (
                    self.width < pivot[0] + dimension[0] or
                    self.height < pivot[1] + dimension[1] or
                    self.depth < pivot[2] + dimension[2]
                    ):
                    height_l = False
                    
                    if (
                        pivot[0]+w-dimension[0] < 0 or
                        self.height < pivot[1] + dimension[1] or
                        self.depth < pivot[2] + dimension[2]
                        ):
                        height_r1 = False
                        
                        if (
                            self.width < pivot[0]+w+dimension[0] or
                            pivot[1] - dimension[1] < 0 or
                            self.depth < pivot[2] + dimension[2]
                            ):
                            height_r2 = False
                        else:
                            height_r2 = True
                            item.position = [pivot[0]+w,pivot[1]-dimension[1],pivot[2]]
                            
                    else:
                        height_r1 = True
                        item.position = [pivot[0]+w-dimension[0],pivot[1],pivot[2]]
                        
                else:
                    height_l = True
                    
                    

                if height_l == False and height_r1 == False and height_r2 == False:
                    item.position = pivot
                    continue
                
            else:
                if (
                    self.width < pivot[0] + dimension[0] or
                    self.height < pivot[1] + dimension[1] or
                    self.depth < pivot[2] + dimension[2]
                    ):
                    continue
    
            fit = True
            
            
            for current_item_in_bin in self.apparent_items:
                if current_item_in_bin.position[2]==0:
                    if intersect(current_item_in_bin, item):
                        fit = False
                        break
            if not fit:
                item.position = pivot
                continue
            

            for current_item_in_bin in self.items:
                if intersect(current_item_in_bin, item):
                    fit = False
                    break
            if not fit:
                item.position = pivot
                continue
            
            
            

            if fit:
                if self.get_total_weight() + item.weight > self.max_weight:
                    fit = False
                    return fit
                

                self.items.append(item)
                self.item_depths.append(item.position_elevated[2])

            if not fit:
                item.position = valid_item_position

            return fit

        if not fit:
            item.position = valid_item_position

        return fit
    
    def put_apparent_item(self,apparent_item):
        self.apparent_items.append(apparent_item)
        
    def put_item_subsequent_layers(self, item, pivot, axis, w, base_z, z_layers):
        fit = False
        valid_item_position = item.position
        item.position = pivot

        for i in range(0, len(RotationType.ALL)):
            if pivot[2]>base_z:
                break
            item.rotation_type = i
            dimension = item.get_dimension()
            if axis == 1:
                #Height(L), Height(R) Check - when height_l is false, check height_r validity
                
                
                if (
                    self.width < pivot[0] + dimension[0] or
                    self.height < pivot[1] + dimension[1] or
                    self.depth < pivot[2] + dimension[2]
                    ):
                    height_l = False
                    
                    if (
                        pivot[0]+w-dimension[0] < 0 or
                        self.height < pivot[1] + dimension[1] or
                        self.depth < pivot[2] + dimension[2]
                        ):
                        height_r1 = False
                        
                        if (
                            self.width < pivot[0]+w+dimension[0] or
                            pivot[1] - dimension[1] < 0 or
                            self.depth < pivot[2] + dimension[2]
                            ):
                            height_r2 = False
                        else:
                            height_r2 = True
                            item.position = [pivot[0]+w,pivot[1]-dimension[1],pivot[2]]
                            
                    else:
                        height_r1 = True
                        item.position = [pivot[0]+w-dimension[0],pivot[1],pivot[2]]
                else:
                    height_l = True

                if height_l == False and height_r1 == False and height_r2 == False:
                    item.position = pivot
                    continue
                
            else:
                if (
                    self.width < pivot[0] + dimension[0] or
                    self.height < pivot[1] + dimension[1] or
                    self.depth < pivot[2] + dimension[2]
                    ):
                    continue

            fit = True
            #if(item.name=='15' and float(base_z)==3.969):
            #    print(item.position,item.dimension,axis)

            for current_item_in_bin in self.apparent_items:
                if intersect(current_item_in_bin, item):
                    fit = False
                    break
            if not fit:
                item.position = pivot
                continue
            

            if fit:
                if self.get_total_weight() + item.weight > self.max_weight:
                    fit = False
                    return fit
                

                self.items.append(item)
                self.item_depths.append(item.position_elevated[2])

            if not fit:
                item.position = valid_item_position

            return fit

        if not fit:
            item.position = valid_item_position

        return fit
    


class Packer:
    def __init__(self):
        self.bins = []
        self.items = []
        self.unfit_items = []
        self.total_items = 0

    def add_bin(self, bin):
        return self.bins.append(bin)

    def add_item(self, item):
        self.total_items = len(self.items) + 1

        return self.items.append(item)

    def pack_to_bin(self, bin, item):
        fitted = False

        if not bin.items:
            response = bin.put_item(item, START_POSITION,0,0)

            if not response:
                bin.unfitted_items.append(item)

            return

        for axis in range(0, 3):
            items_in_bin = bin.items

            for ib in items_in_bin:
                pivot = [0, 0, 0]
                w, h, d = ib.get_dimension()
                if axis == Axis.WIDTH:
                    pivot = [
                        ib.position[0] + w,
                        ib.position[1],
                        ib.position[2]
                    ]
                elif axis == Axis.HEIGHT:
                    pivot = [
                        ib.position[0],
                        ib.position[1] + h,
                        ib.position[2],                        
                    ]

                elif axis == Axis.DEPTH:
                    pivot = [
                        ib.position[0],
                        ib.position[1],
                        ib.position[2] + d
                    ]

                if bin.put_item(item, pivot, axis, w):
                    
                    fitted = True
                    break
            if fitted:
                break

        if not fitted:
            #first try fitting in the next layer
            z_layers = [0]
            k=0
            while True:
                base_z = min(num for num in bin.item_depths if num>k)
                print(base_z)
                z_layers.append(base_z)
            
                #Making apparent items for base_z
                    
                offset_depths = [x-base_z for x in bin.item_depths]
                if base_z==max(bin.item_depths):
                    pivs=[]
                    count_A=0
                    count_B=0
                    for d in offset_depths:
                        if d==0:
                            try:
                                piv = bin.apparent_items[count_A].position
                                piv[2] = base_z
                                pivs.append(piv)
                                count_A+=1
                            except:
                                piv = bin.items[count_B].position
                                piv[2] = base_z
                                pivs.append(piv)
                                count_B+=1
                
                bin.apparent_items = []
                for key,d in enumerate(offset_depths):
                    if d>0:
                        #This xy-plane is occupied
                        #apparent_item instance has to be defined to mask this area on xy-plane
                        apparent_item = Item("apparent_"+bin.items[key].name,bin.items[key].dimension[0],bin.items[key].dimension[1],d,0)
                        apparent_item.position = [bin.items[key].position[0],bin.items[key].position[1],base_z]
                        apparent_item.dimension = [bin.items[key].dimension[0],bin.items[key].dimension[1],d]
                        apparent_item.position_elevated = [bin.items[key].position[0],bin.items[key].position[1],d+base_z]
                        #This apprent_item has to be put in the bin to mask the area already occupied by the actual item
                        bin.put_apparent_item(apparent_item)
                    
            
 
                #Now, put the actual item at the base_z layer
                if not bin.apparent_items:
                    responses=[]
                    for piv in pivs:
                        response = bin.put_item_subsequent_layers(item, piv, 0, 0, base_z, z_layers)
                        responses.append(response)
                    fit_test=0
                    for response in responses:
                        fit_test+=response
                    if fit_test==0:
                        bin.unfitted_items.append(item)
                    return

     
                        
                for axis in range(0, 3):
                    items_in_bin = bin.apparent_items
                

                    for ib in items_in_bin:
                        pivot = [0, 0, 0]
                        [w, h, d] = ib.dimension
                        if axis == Axis.WIDTH:
                            pivot = [
                                ib.position[0] + w,     #ib.position[2]=base_z
                                ib.position[1],
                                ib.position[2]
                                ]   
                        elif axis == Axis.HEIGHT: 
                            pivot = [
                                ib.position[0],
                                ib.position[1] + h,
                                ib.position[2]
                                ]
                        elif axis == Axis.DEPTH:
                            pivot = [
                                ib.position[0],
                                ib.position[1],
                                ib.position[2] + d
                                ]

                        if bin.put_item_subsequent_layers(item, pivot, axis, w, base_z, z_layers):
                            fitted = True
                            #Making apparent items at z<base_z among z_layers values when the item is stacked
                            for l,ly in enumerate(z_layers):
                                assert(ly<=base_z)
                                for ap_i in bin.apparent_items:
                                    if ap_i.name.startswith("apparent_") and ly<base_z:
                                        apparent_item = Item("lower_projection_"+ap_i.name,ap_i.dimension[0],ap_i.dimension[1],base_z-ly,0)
                                        apparent_item.position = [ap_i.position[0],ap_i.position[1],ly]
                                        apparent_item.dimension = [ap_i.dimension[0],ap_i.dimension[1],base_z-ly]
                                        apparent_item.position_elevated = [ap_i.position[0],ap_i.position[1],base_z]
                                        bin.put_apparent_item(apparent_item)
                                for item in bin.items:
                                    if item.position[2]==base_z and ly<base_z:
                                        apparent_item = Item("lower_projection_"+item.name,item.dimension[0],item.dimension[1],base_z-ly,0)
                                        apparent_item.position = [item.position[0],item.position[1],ly]
                                        apparent_item.dimension = [item.dimension[0],item.dimension[1],base_z-ly]
                                        apparent_item.position_elevated = [item.position[0],item.position[1],base_z]
                                        bin.put_apparent_item(apparent_item)
                                        
                            break
                    if fitted:
                        return
                    else:
                        if axis==2:
                            break
                    if axis==2:
                        break
                k=base_z
                if k==max(bin.item_depths):
                    break
            
            print(z_layers)
            bin.unfitted_items.append(item)

    def pack(
        self, bigger_first=False, distribute_items=False,
        number_of_decimals=DEFAULT_NUMBER_OF_DECIMALS
    ):
        for bin in self.bins:
            bin.format_numbers(number_of_decimals)

        for item in self.items:
            item.format_numbers(number_of_decimals)

        #self.bins.sort(
        #    key=lambda bin: bin.get_volume(), reverse=bigger_first
        #)
        #self.items.sort(
        #    key=lambda item: item.get_volume(), reverse=bigger_first
        #)

        #for bin in self.bins:
            #for item in self.items:
        self.pack_to_bin(bin, item)

        if distribute_items:
            for item in bin.items:
                self.items.remove(item)


                
