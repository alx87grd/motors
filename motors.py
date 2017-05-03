# Libs

import numpy as np
import csv
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.lines  as mlines


'''
################################################################################
'''


class ElectricMotor:
    """ 
    Mother class for storing electric motor info and data
    ----------------------------------------------
    """
    
    ############################
    def __init__(self):
        """ """

        self.specs = {}
        
        self.specs['typ'] = [ 'empty',   'Type'                  ,  ''       ]
        self.specs['dia'] = [       0,   'Diameter'              ,  '[mm]'   ]
        self.specs['pow'] = [       0,   'Power'                 ,  '[watts]']
        self.specs['sup'] = [       0,   'Supply tension'        ,  '[volts]']
        self.specs['vel'] = [       0,   'No load velocity'      ,  '[RPM]'  ]
        self.specs['tor'] = [       0,   'Max continuous torque' ,  '[mNm]'  ]
        self.specs['pri'] = [       0,   'Price'                 ,  '[$USD]' ]
        self.specs['len'] = [       0,   'Length'                ,  '[mm]'   ]
        self.specs['ine'] = [       0,   'Rotor inertia'         ,  '[gcm2]' ]
        self.specs['mas'] = [       0,   'Mass'                  ,  '[g]'    ]
        self.specs['vol'] = [       0,   'Volume'                ,  '[L]'    ]
        self.specs['kin'] = [       0,   'Max kinetic energy'    ,  '[J]'    ]

        
    #############################
    def process_data(self):
        """ 
        Compute secondary values
        --------------------------------------        
        """
        
        ###################
        # Motor volume
        ###################
        
        d = self.specs['dia'][0]
        l = self.specs['len'][0]
        v = np.pi * 0.25 * d**2 * l * 1e-06 # volume in liter
        
        self.specs['vol'][0] = v
        
        ###################
        # Max kinetic energy
        ###################
        
        I = self.specs['ine'][0]
        w = self.specs['vel'][0]
        
        # RPM to rad/sec
        
        w_rad_sec = w * 2 * np.pi * (1./60)
        I_kgm2    = I * 1e-7
        
        T = 0.5 * I_kgm2 * w_rad_sec**2
        
        self.specs['kin'][0] = T
        


'''
################################################################################
'''


class MotorAnalyzer:
    """ 
    Class for processing motor data
    ----------------------------------------------
     - converting csv to a list of motors
    """
    
    ############################
    def __init__( self , filename = 'data.csv' ):
        """ """
        
        nm = ElectricMotor()
        
        # Copy specs
        self.specs = nm.specs
        
        # Load values from files
        self.load_motors_data(filename)
        
        # Params
        self.save        = True
        self.output_path = '../output/'
        
    
    ############################
    def process_motor_data(self, row ):
        """ from a list of info, create motor class """
        
        nm = ElectricMotor()
        
        nm.specs['typ'][0] = row[0]
        nm.specs['dia'][0] = float( row[1] )
        nm.specs['pow'][0] = float( row[2] )
        nm.specs['sup'][0] = float( row[3] )
        nm.specs['vel'][0] = float( row[4] )
        nm.specs['tor'][0] = float( row[5] )
        nm.specs['pri'][0] = float( row[6] )
        nm.specs['len'][0] = float( row[7] )
        nm.specs['ine'][0] = float( row[8] )
        nm.specs['mas'][0] = float( row[9] )
        
        nm.process_data()
        
        return nm
    
    
    ############################
    def load_motors_data(self, filename = 'data.csv'  ):
        """ create a list of motors from data"""
        
        self.n  = 0
        self.ml = []
        
        with open( filename , newline='') as f:
            reader = csv.reader(f)
            for row in reader:
                print( 'Loading: ' , row )
                self.ml.append( self.process_motor_data( row ) )
                self.n = self.n + 1
        
        print('Loaded ',self.n,' motors')
        return self.ml
    
    
    
    ############################
    def two_axis_analysis(self, param1 = 'dia' , param2 = 'pow' , type2plot = 'All'  ):
        """ create two array of data to compare """
        
        # Init list
        x = []
        y = []
        
        for motor in self.ml:
            
            if type2plot == 'All':
                
                x.append( motor.specs[param1][0] )
                y.append( motor.specs[param2][0] )
                
            else:
                #TODO
                pass
    
    
        return x,y
    
    
    ############################
    def two_axis_plot( self,  param1 = 'dia' , param2 = 'pow' , type2plot = 'All'  ):
        """ create two array of data to compare """
        
        # Create figure
        fig , plot = plt.subplots(1, sharex=True,figsize=(4, 3),dpi=300, frameon=True)
        
        # Save plot access
        self.fig  = fig
        self.plot = plot
        
        # For all motors
        for motor in self.ml:
            
            if type2plot == 'All':
                
                x =  motor.specs[param1][0]
                y =  motor.specs[param2][0]
                
                marker_type, color_type = self.motortype2marker( motor.specs['typ'][0] )
                
                plot.plot([x], [y], marker=marker_type, markersize=3, color=color_type)
                
            else:
                #TODO
                pass
            
        # Figure params
        plot.grid(True)
        plot.set_xlabel( self.specs[param1][1] + '\n' + self.specs[param1][2], fontsize=7 )
        plot.set_ylabel( self.specs[param2][1] + '\n' + self.specs[param2][2], fontsize=7 )
#         plot.set_xlim(0,50)
        plot.tick_params(axis='both', which='major', labelsize=7)
        plot.tick_params(axis='both', which='minor', labelsize=6)
        
        self.addmotortypelegend()
        plt.draw()
        fig.tight_layout()
        
        fig_name = 'Motor analysis of ' + self.specs[param1][1] + ' vs. ' + self.specs[param2][1]
        fig.canvas.set_window_title( fig_name )        
        
        if self.save:
            file_name = self.output_path + fig_name.replace(" ", "_")
            print(file_name)
            fig.savefig( file_name + '.png' , format='png', bbox_inches='tight', pad_inches=0.05) 
            fig.savefig( file_name + '.pdf' , format='pdf', bbox_inches='tight', pad_inches=0.05) 
            print('Figure {' + fig_name + '} saved')
        
        
    ############################
    def motortype2marker(self, motor_type  ):
        """ maps type to marker """
        
        if motor_type == 'RE':
            marker='o'
            color='b'
        elif motor_type == 'EC':
            marker='x'
            color='g'
        elif motor_type == 'EC-max':
            marker='^'
            color='r'
        elif motor_type == 'EC Flat':
            marker='v'
            color='c'
        else:
            marker = '.'
            color='k'
            
        return marker, color
    
    ############################
    def addmotortypelegend(self):
        """ create motor type legend """
        
        re     = mlines.Line2D([],[], marker='o', color='b', label='RE' , linestyle='')
        ec     = mlines.Line2D([],[], marker='x', color='g', label='EC', linestyle='')
        ecmax  = mlines.Line2D([],[], marker='^', color='r', label='EC-max', linestyle='')
        ecflat = mlines.Line2D([],[], marker='v', color='c', label='EC Flat', linestyle='')
        other  = mlines.Line2D([],[], marker='.', color='k', label='others', linestyle='')
        
        self.plot.legend( handles=[re,ec,ecmax,ecflat,other], fontsize=7)
    
'''
################################################################################
'''

        

'''
#################################################################
##################          Main                         ########
#################################################################
'''


if __name__ == "__main__":     
    """ MAIN TEST """
    
    
    A = MotorAnalyzer('../data/all_data_test.csv')
    
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
    
    A.two_axis_plot( a1 , a2 )
    
    a1 = 'tor'
    a2 = 'pri'
      
    A.two_axis_plot( a1 , a2 )
      
    a1 = 'tor'
    a2 = 'ine'
      
    A.two_axis_plot( a1 , a2 )
     
    a1 = 'tor'
    a2 = 'vol'
      
    A.two_axis_plot( a1 , a2 )
     
    a1 = 'tor'
    a2 = 'kin'
      
    A.two_axis_plot( a1 , a2 )
    
    plt.show()