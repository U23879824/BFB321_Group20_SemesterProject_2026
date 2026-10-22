#To calculate how much stock is avialable for customer orders:
def calculate_atp(on_hand, reserved):
    return max(0, on_hand - reserved)
 
#Identifying differences between inventory systen and actual physical stock present in store:
def inventory_discrepancy(system_stock, physical_stock):
    return system_stock - physical_stock 

#Determining whether a store has enough available stock to fulfil an order:
def sufficient_stock(atp, requested):
    return atp >= requested

