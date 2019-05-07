# Automated GNU plots of NuLAB nutrient data
# Vince Kelly, Green Eyes LLC, vince@gescience.com
# April 2016

#move to data dir
	cd '/home/pi/ComScriptPi/profiles/NuLAB_Logging/'

#prep for png output
	set terminal png font "DejaVu Sans" enhanced

#add a grid
	set grid
	
#set legend outside
       set key outside
       set datafile separator ","

#Plot NH4 OBS
	set output '/home/pi/ComScriptPi/profiles/NuLAB_Logging/NH4obs.png'
	set term png size 1500,600
	set style data lines
	set autoscale xy
	set yrange [0 :0.1]
	set xlabel "Month/Day"
	set ylabel "Absorbance"
	set xdata time
	set timefmt "%m/%d/%Y %H:%M:%S"
	set format x "%m/%d"
	set xtics 691200
	set mxtics 4
	set title "{/*1.4 NuLAB Plus}\n\n{/*1.1On-board Standard Absorbance - Ammonium}"
	set pointsize 0.75
	set size 1.0,0.75
	plot 'Ammonium_Data-L.txt' using 1:14 notitle with points pt 1 ps 1.5 lc rgb "#8B008B"

#Plot NH4 Conc
	set output '/home/pi/ComScriptPi/profiles/NuLAB_Logging/NH4conc.png'
	set term png size 1500,600
	set style data lines
	set autoscale xy
	set yrange [0: ]
	set xlabel "Month/Day"
	set ylabel "Concentration"
	set xdata time
	set timefmt "%m/%d/%Y %H:%M:%S"
	set format x "%m/%d"
	set xtics 691200
	set mxtics 4
	set title "{/*1.4 NuLAB Plus}\n\n{/*1.1Sample Concentration - Ammonium}"
	set pointsize 0.75
	set size 1.0,0.75
	plot 'Ammonium_Data-L.txt' using 1:20 notitle with points pt 2 ps 1.5 lc rgb "#8B008B"

#Plot PO4 OBS
	set output '/home/pi/ComScriptPi/profiles/NuLAB_Logging/PO4obs.png'
	set term png size 1500,600
	set style data lines
	set autoscale xy
	set yrange [0 :0.1]
	set xlabel "Month/Day"
	set ylabel "Absorbance"
	set xdata time
	set timefmt "%m/%d/%Y %H:%M:%S"
	set format x "%m/%d"
	set xtics 691200
	set mxtics 4
	set title "{/*1.4 NuLAB Plus}\n\n{/*1.1On-board Standard Absorbance - Phosphate}"
	set pointsize 0.75
	set size 1.0,0.75
	plot 'Phosphate_Data-L.txt' using 1:14 notitle with points pt 1 ps 1.5 lc rgb "#DC143C"

#Plot PO4 Conc
	set output '/home/pi/ComScriptPi/profiles/NuLAB_Logging/PO4conc.png'
	set term png size 1500,600
	set style data lines
	set autoscale xy
	set yrange [0: ]
	set xlabel "Month/Day"
	set ylabel "Concentration"
	set xdata time
	set timefmt "%m/%d/%Y %H:%M:%S"
	set format x "%m/%d"
	set xtics 691200
	set mxtics 4
	set title "{/*1.4 NuLAB Plus}\n\n{/*1.1Sample Concentration - Phosphate}"
	set pointsize 0.75
	set size 1.0,0.75
	plot 'Phosphate_Data-L.txt' using 1:20 notitle with points pt 2 ps 1.5 lc rgb "#DC143C"

#Plot N+N OBS
	set output '/home/pi/ComScriptPi/profiles/NuLAB_Logging/N+Nobs.png'
	set term png size 1500,600
	set style data lines
	set autoscale xy
	set yrange [0 :0.1 ]
	set xlabel "Month/Day"
	set ylabel "Absorbance"
	set xdata time
	set timefmt "%m/%d/%Y %H:%M:%S"
	set format x "%m/%d"
	set xtics 691200
	set mxtics 4
	set title "{/*1.4 NuLAB Plus}\n\n{/*1.1On-board Standard Absorbance - N+N}"
	set pointsize 0.75
	set size 1.0,0.75
	plot 'N+N_Data-L.txt' using 1:14 notitle with points pt 1 ps 1.5 lc rgb "#006400"

#Plot N+N Conc
	set output '/home/pi/ComScriptPi/profiles/NuLAB_Logging/N+Nconc.png'
	set term png size 1500,600
	set style data lines
	set autoscale xy
	set yrange [0: ]
	set xlabel "Month/Day"
	set ylabel "Concentration"
	set xdata time
	set timefmt "%m/%d/%Y %H:%M:%S"
	set format x "%m/%d"
	set xtics 691200
	set mxtics 4
	set title "{/*1.4 NuLAB Plus}\n\n{/*1.1Sample Concentration - N+N}"
	set pointsize 0.75
	set size 1.0,0.75
	plot 'N+N_Data-L.txt' using 1:20 notitle with points pt 2 ps 1.5 lc rgb "#006400"



#Plot NO2 OBS
	set output '/home/pi/ComScriptPi/profiles/NuLAB_Logging/NO2obs.png'
	set term png size 1500,600
	set style data lines
	set autoscale xy
	set yrange [0 :0.1 ]
	set xlabel "Month/Day"
	set ylabel "Absorbance"
	set xdata time
	set timefmt "%m/%d/%Y %H:%M:%S"
	set format x "%m/%d"
	set xtics 691200
	set mxtics 4
	set title "{/*1.4 NuLAB Plus}\n\n{/*1.1On-board Standard Absorbance - Nitrite}"
	set pointsize 0.75
	set size 1.0,0.75
	plot 'Nitrite_Data-L.txt' using 1:14 notitle with points pt 1 ps 1.5 lc rgb "#0000FF"

#Plot NO2 Conc
	set output '/home/pi/ComScriptPi/profiles/NuLAB_Logging/NO2conc.png'
	set term png size 1500,600
	set style data lines
	set autoscale xy
	set yrange [0: ]
	set xlabel "Month/Day"
	set ylabel "Concentration"
	set xdata time
	set timefmt "%m/%d/%Y %H:%M:%S"
	set format x "%m/%d"
	set xtics 691200
	set mxtics 4
	set title "{/*1.4 NuLAB Plus}\n\n{/*1.1Sample Concentration - Nitrite}"
	set pointsize 0.75
	set size 1.0,0.75
	plot 'Nitrite_Data-L.txt' using 1:20 notitle with points pt 2 ps 1.5 lc rgb "#0000FF"

#Plot NO3 Conc
	set output '/home/pi/ComScriptPi/profiles/NuLAB_Logging/NO3conc.png'
	set term png size 1500,600
	set style data lines
	set autoscale xy
	set yrange [0: ]
	set xlabel "Month/Day"
	set ylabel "Concentration"
	set xdata time
	set timefmt "%m/%d/%Y %H:%M:%S"
	set format x "%m/%d"
	set xtics 691200
	set mxtics 4
	set title "{/*1.4 NuLAB Plus}\n\n{/*1.1Sample Concentration - Nitrate}"
	set pointsize 0.75
	set size 1.0,0.75
	plot 'Nitrate_Data-L.txt' using 1:6 notitle with points pt 2 ps 1.5 lc rgb "#2F4F4F"

