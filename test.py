
import motors as m
import matplotlib.pyplot as plt

A = m.MotorAnalyzer('../data/all_data_test.csv')


a1 = 'tor'
a2 = 'vel'

A.two_axis_regression( a1 , a2 )

plt.show()
