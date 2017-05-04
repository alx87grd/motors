
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

a1 = 'tor'
a2 = 'mas'

A.two_axis_regression( a1 , a2 )

a1 = 'tor'
a2 = 'pri'
  
A.two_axis_regression( a1 , a2 )
  
a1 = 'tor'
a2 = 'ine'
  
A.two_axis_regression( a1 , a2 )
 
a1 = 'tor'
a2 = 'vol'
  
A.two_axis_regression( a1 , a2 )
 
a1 = 'tor'
a2 = 'kin'
  
A.two_axis_regression( a1 , a2 )

plt.show()

