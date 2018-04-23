#!/bin/bash

#python three_lepton.py
#python four_lepton.py
#python two_lepton.py
#python emu.py
#python mass_shape_plots.py
#python reso_plot.py
#python limits.py
#python grav.py
#python h4l_int.py
#python two_hdm.py
#python p0_plot.py
#python offshell_4l.py
python offshell_2l2v.py

#for ith_file in `ls | grep ".eps"`
#do
#  epstopdf $ith_file
#done

mv *.png *.pdf *.eps plots 
