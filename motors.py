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
        
        # Copy specs dictionnary
        self.specs = nm.specs
        
        # Load values from files
        self.load_motors_data( filename )
        
        # I/O Params
        self.save          = True
        self.output_path   = '../output/'
        self.analysis_name = 'Motor analysis of '
        
        # Analysis Params
        self.active_type  = 'All'
        self.active_range = [[-1,100000000],[-1,1000000000]]
        
        # Regression Params
        self.reg_type = 'lin'
        
    
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
        
        self.n          = 0
        self.motor_list = []
        
        with open( filename , newline='') as f:
            reader = csv.reader(f)
            for row in reader:
                print( 'Loading: ' , row )
                self.motor_list.append( self.process_motor_data( row ) )
                self.n = self.n + 1
        
        print('Loaded ',self.n,' motors')
        return self.motor_list
    
    
    ############################
    def two_axis_plot( self,  param1 = 'dia' , param2 = 'pow'):
    
        self.two_axis_analysis( param1, param2, plot = True, reg = False)
        
    ############################
    def two_axis_regression( self,  param1 = 'dia' , param2 = 'pow'):
    
        self.two_axis_analysis( param1, param2, plot = True, reg = True)
    
    
    ############################
    def two_axis_analysis( self,  param1 = 'dia' , param2 = 'pow' , plot = False , reg = False ):
        """ analyze relationships between two params """
        
        # Init lists
        self.x = []
        self.y = []
        
        if plot:
            # Create figure
            fig , plot = plt.subplots(1, sharex=True,figsize=(4, 3),dpi=300, frameon=True)
            self.fig  = fig
            self.plot = plot
        
        # For all motors
        for motor in self.motor_list:
            
            if self.motor_meet_criteria( motor, param1, param2):
                # Include this motor in the analysis
                
                x =  motor.specs[param1][0]
                y =  motor.specs[param2][0]
                
                self.x.append(x)
                self.y.append(y)
                
                if plot:
                    marker_type, color_type = self.motortype2marker( motor.specs['typ'][0] )
                    plot.plot([x], [y], marker=marker_type, markersize=3, color=color_type)
                
            else:
                # Skip this motor
                pass
            
        print('Number of motor in analysis domain: ', self.x.__len__( ) )
        
                
        if reg:
            # Conduct regression
            
            n = len(self.x)
            
            # Regressor
            X = np.array(self.x)
            Y = np.array(self.y)
            
            if self.reg_type == 'lin':
                
                X_0 = np.ones( n ) # constant offset
                
                Phi = np.array([ X, X_0])
                
                P = np.linalg.inv( np.dot( Phi , Phi.T ) ) 
                M = np.dot( P , Phi )
                
                self.theta = np.dot( M , Y )
                
                print('Reg. results: slope=', self.theta[0], ' offset=', self.theta[1])
                
                
        if plot:
            
            if reg:
                # Plot regression
                n = 10
                x = np.linspace( X.min() , X.max(), num=n)
                y = self.reg_map(x)
                
                plot.plot( x, y, linestyle = '-.', color = 'gray' )
                
            # Figure params
            plot.grid(True)
            plot.set_xlabel( self.specs[param1][1] + '\n' + self.specs[param1][2], fontsize=7 )
            plot.set_ylabel( self.specs[param2][1] + '\n' + self.specs[param2][2], fontsize=7 )
            plot.tick_params(axis='both', which='major', labelsize=7)
            plot.tick_params(axis='both', which='minor', labelsize=6)
            
            self.addmotortypelegend()
            plt.draw()
            fig.tight_layout()
            
            fig_name = self.analysis_name + self.specs[param1][1] + ' vs. ' + self.specs[param2][1]
            fig.canvas.set_window_title( fig_name )        
            
            if self.save:
                file_name = self.output_path + fig_name.replace(" ", "_")
                fig.savefig( file_name + '.png' , format='png', bbox_inches='tight', pad_inches=0.05) 
                fig.savefig( file_name + '.pdf' , format='pdf', bbox_inches='tight', pad_inches=0.05) 
                print('Figure {' + fig_name + '} saved')
                
                
    ############################
    def reg_map(self, x):  
        """ Foward computation using regression """
        
        if self.reg_type == 'lin':
            
            y = self.theta[0] * x + self.theta[1]
            
        return y
        
    ############################
    def motor_meet_criteria(self, motor , param1, param2):
        """ check if motor meet analysis criteria """   
        
        motor_type_ok = False
        
        # Domain in terms of motor type
        
        if ( self.active_type == 'All' or self.active_type == motor.specs['typ'][0] ):
            # Motor type is ok
            motor_type_ok = True
            
            
        # Domain in terms of param1 and param2 range
        
        motor_range_ok = True
        
        x =  motor.specs[param1][0]
        y =  motor.specs[param2][0]
        
        if ( x < self.active_range[0][0] or x > self.active_range[0][1] ):
            # Param 1 is out of range
            motor_range_ok = False
            
        if ( y < self.active_range[1][0] or y > self.active_range[1][1] ):
            # Param 2 is out of range
            motor_range_ok = False
        
        
        # Combination
        
        motor_meet_criteria = motor_type_ok and motor_range_ok
        
        return motor_meet_criteria
        
        
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