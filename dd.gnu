#!/usr/local/bin/gnuplot -persist
#set terminal pngcairo transparent enhanced font "arial,10" fontscale 1.0 size 800, 600
#set output 'histograms.3.png'
set terminal postscript eps enhanced color solid
set output "result.ps"
set boxwidth 0.9 absolute
red = "#FF0000"; green = "#00FF00"; blue = "#0000FF"; skyblue = "#87CEEB";
set style data histogram
set style fill   solid 1.00 border lt -1
set ylabel "Write time, s"
set xlabel "bs"
set grid
plot "log.txt" u 2:xtic(1) title "Average" linecolor rgb red, "log.txt" u 3 title "Median" linecolor rgb blue


