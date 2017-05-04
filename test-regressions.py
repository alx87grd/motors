
import motors as m
import matplotlib.pyplot as plt

A = m.MotorAnalyzer('../data/all_data_test.csv')

#     'typ':     'Type'      
#     'dia':     'Diameter'             
#     'pow':     'Power'                
#     'sup':     'Supply tension'       
#     'vel':     'No load velocity'      
#     'tor':     'Max. continuous torque'
#     'pri':     'Price'                
#     'len':     'Length'               
#     'ine':     'Rotor inertia'       
#     'mas':     'Mass'                 
#     'vol':     'Volume'         

""" Select Axis """

a1 = 'tor'
# a1 = 'pow'

a2 = 'mas'
# a2 = 'pri'
# a2 = 'ine'
# a2 = 'vol'
# a2 = 'kin'

""" Domain """
# A.active_range[0] = [5,80]
# A.active_type = 'RE'

""" Analysis """
A.two_axis_regression( a1 , a2 )
plt.show()


