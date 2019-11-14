#Written By: Michael Wright
#Date: November 12, 2019


#--------------------------------------------------
# model for charting relative strength of a pokemon
#--------------------------------------------------

#goal:	to find and plot the ammount of time/levels a high CP, low IV pokemon will be better than a high IV, low CP pomemon
#		aditionally, find the ammount of stardust it would take either one to hit lvl 30 (90% potential) and output the difference

import matplotlib.pyplot as plt
import PySimpleGUI as sg
import pypokedex
import numpy as np
from math import sqrt


atk_ = 0
def_ = 0
hp_ = 0
i = 0
j = 0
lvl_dif = 0

cp_multiplier = [0.094, 0.1351374318, 0.16639787, 0.192650919, 0.21573247,
		0.2365726613, 0.25572005, 0.2735303812, 0.29024988, 0.3060573775,
        0.3210876 , 0.3354450362, 0.34921268, 0.3624577511, 0.37523559,
        0.3875924064, 0.39956728, 0.4111935514, 0.42250001, 0.4335116883,
        0.44310755, 0.4530599591, 0.46279839, 0.4723360832, 0.48168495, 
        0.4908558003, 0.49985844, 0.508701765, 0.51739395, 0.5259425113, #15.5
        0.53435433, 0.542635767, 0.55079269, 0.5588305763, 0.56675452,
        0.574569153, 0.58227891, 0.5898879171, 0.59740001, 0.6048188139,
        0.61215729, 0.6194041117, 0.62656713, 0.6336491729, 0.64065295,
        0.6475809666, 0.65443563, 0.6612192524, 0.667934, 0.6745818959, #25.5
        0.68116492, 0.6876849236, 0.69414365, 0.70054287, 0.70688421,
        0.713169119, 0.71939909, 0.7255756036, 0.7317, 0.7347410093,
        0.73776948, 0.7407855938, 0.74378943, 0.7467812109, 0.74976104,
        0.7527290867, 0.75568551, 0.7586303683, 0.76156384, 0.7644860647,
        0.76739717, 0.7702972656, 0.7731865, 0.7760649616, 0.77893275, 
        0.7817900548, 0.78463697, 0.7874736075, 0.79030001]

Total_stardust = [0, 200, 400, 600, 800, 1200, 1600, 2000, 2400, 3000, 3600, 4200,
		4800, 5600, 6400, 7200, 8000, 9000, 10000, 11000, 12000, 13300, 14600,
		15900, 17200, 18800, 20400, 22000, 23600, 25500, 27400, 29300, 31200,
		33400, 35600, 37800, 40000, 42500, 45000, 47500, 50000, 53000, 56000,
		59000, 62000, 65500, 69000, 72500, 76000, 80000, 84000, 88000, 92000,
		96500, 101000, 105500, 110000, 115000, 120000, 125000, 130000, 136000,
		142000, 148000, 154000, 161000, 168000, 175000, 182000, 190000, 198000,
		206000, 214000, 223000, 232000, 241000, 250000, 260000, 270000]

def stat_calculations(p):
	#---------------------------------------------------------------------
	# this function calculates ingame stats using the pypokedex library
	#---------------------------------------------------------------------

	global atk_
	global def_
	global hp_

	base_speed = 1 + (p.base_stats.speed - 75) / 500
	base_stamina = (1.75 * p.base_stats.hp) + 50

	if p.base_stats.attack >= p.base_stats.sp_atk:
		higher = p.base_stats.attack
		lower = p.base_stats.sp_atk
	else:
		higher = p.base_stats.sp_atk
		lower = p.base_stats.attack

	scaled_atk = round(2 *((7/8)*higher + (1/8)*lower))

	base_atk = round(scaled_atk * base_speed)

	if p.base_stats.defense >= p.base_stats.sp_def:
		higher = p.base_stats.defense
		lower = p.base_stats.sp_def
	else:
		higher = p.base_stats.sp_def
		lower = p.base_stats.defense

	scaled_def = round(2 *((5/8)*higher + (3/8)*lower))

	base_def = round(scaled_def * base_speed)

	atk_ = base_atk
	def_ = base_def
	hp_ = base_stamina

	return

def compute_cp(iv_HP,iv_A,iv_D):
	#---------------------------------------------------------------------
	# this function computes the CP of a pokemon at all
	# levels given its base stats and IVs
	#---------------------------------------------------------------------

	global atk_
	global def_
	global hp_

	out = {}

	for lvl in range(1, 80):
		mul = cp_multiplier[lvl - 1]
		cp = ((atk_ + iv_A) * sqrt(def_ + iv_D) * sqrt(hp_ + iv_HP) * mul**2) / 10 
		out[float(lvl/2) + 0.5] = round(cp - 1)	
	return out

#------------------------------------------------------------------------------------
#			main program compares the values of the chosen pokemon and returns total 
#			cp and stardust differnece between the two
#------------------------------------------------------------------------------------
sg.change_look_and_feel('DarkAmber')

layout = [  [sg.Text("Stardust Power-Up Calcuator")],
			[sg.Text("Please input the name of the Pokemon you're comparing:"), sg.InputText(size = (10,1))],
			[sg.Text("Enter the current CP of the High CP/Low IV Pokemon:"), sg.InputText(size = (8,1))],
			[sg.Text("Enter the IVs of your Pokemon in order:")],
			[sg.Text("Stamina:"),sg.InputText(size = (4,1)), sg.Text("Attack:"), sg.InputText(size = (4,1)), sg.Text("Defense:"), sg.InputText(size = (4,1))],
			[sg.Text("Enter the current CP of the Low CP/High IV Pokemon"), sg.InputText(size = (8,1))],
			[sg.Text("Enter the IVs of your Pokemon in order:")],
			[sg.Text("Stamina:"),sg.InputText(size = (4,1)), sg.Text("Attack:"), sg.InputText(size = (4,1)), sg.Text("Defense:"), sg.InputText(size = (4,1))],
			[sg.Text("The total stardust it will cost you to get your high IV pokemon in fighting shape is:___", key = 'stardust')],
			[sg.Button('Ok'), sg.Button('Cancel')] ]

window = sg.Window('Pokemon Star-Dust Calculator', layout)

# Event Loop to process "events" and get the "values" of the inputs
while True:

	event, values = window.read()
	if event in (None, 'Cancel'):   # if user closes window or clicks cancel
		break
	#print('You entered ', values[0])

	#print("Please input the name of the Pokemon you're comparing:")
	x = values[0]
	p = pypokedex.get(name = str(x))
	stat_calculations(p)
	#print('Enter the current CP of the High CP/Low IV Pokemon')
	high_cp = int(values[1])

	#print('Now enter the IVs of your Pokemon in the order: |Stamina| |Attack| |Defense| ')
	CP_high_list = list(compute_cp(int(values[2]),int(values[3]),int(values[4])).values())

	#print('Please enter the current CP of the Low CP/High IV Pokemon: ')
	low_cp = int(values[5])

	#print('Now enter the IVs of that Pokemon in the order: |Stamina| |Attack| |Defense| ')
	CP_low_list = list(compute_cp(int(values[6]),int(values[7]),int(values[8])).values())

	while 1:
		if CP_low_list[i] >= low_cp:
			break
		i = i + 1

	while 1:
		if CP_high_list[j] >= high_cp:
			break
		j = j + 1

	while CP_low_list[i] <= CP_high_list[j]:
		lvl_dif = lvl_dif + 1
		i = i + 1

	#print('The total stardust it will cost you to get your high IV pokemon in fighting shape is: {0}'.format(Total_stardust[j] - Total_stardust[j - lvl_dif]))

	PkmLvl = [0]

	for num in range(1,79):
		PkmLvl.append(num / 2)

	fixed_SD = [i / 100 for i in Total_stardust]

	plt.plot(PkmLvl, CP_high_list ,PkmLvl, CP_low_list, PkmLvl, fixed_SD,)

	plt.axhline(y = CP_low_list[i - lvl_dif], xmax = (i - lvl_dif)/80, dashes = [6,2])
	plt.axhline(y = CP_high_list[j], xmax = j / 80, dashes = [6,2])

	plt.axvline(x = PkmLvl[i], ymax = (Total_stardust[i] / 400000), dashes = [6,2])
	plt.axvline(x = PkmLvl[i - lvl_dif], ymax = (Total_stardust[i - lvl_dif] / 400000), dashes = [6,2])

	plt.xlim(0,40)
	plt.ylim(0, 4000)
	plt.xlabel('Pokemon Level')
	plt.ylabel('Bad IV (Blue), Good IV (Orange), Stardust/100 (Green)')
	plt.title('Leveling guide for {0}'.format(p.name))

	window.Element('stardust').Update('total stardust to needed to Match CP: {0}'.format(Total_stardust[j] - Total_stardust[j - lvl_dif]))
	
	plt.show()


window.close()


"""
#print("Please input the name of the Pokemon you're comparing:")
x = values[0]
p = pypokedex.get(name = str(x))
stat_calculations(p)
#print('Enter the current CP of the High CP/Low IV Pokemon')
high_cp = int(values[1])

#print('Now enter the IVs of your Pokemon in the order: |Stamina| |Attack| |Defense| ')
CP_high_list = list(compute_cp(int(values[2]),int(values[3]),int(values[4])).values())

#print('Please enter the current CP of the Low CP/High IV Pokemon: ')
low_cp = int(values[5])

#print('Now enter the IVs of that Pokemon in the order: |Stamina| |Attack| |Defense| ')
CP_low_list = list(compute_cp(int(values[6]),int(values[7]),int(values[8])).values())

while 1:
	if CP_low_list[i] >= low_cp:
		break
	i = i + 1

while 1:
	if CP_high_list[j] >= high_cp:
		break
	j = j + 1

while CP_low_list[i] <= CP_high_list[j]:
	lvl_dif = lvl_dif + 1
	i = i + 1

print('The total stardust it will cost you to get your high IV pokemon in fighting shape is: {0}'.format(Total_stardust[j] - Total_stardust[j - lvl_dif]))


PkmLvl = [0]
for num in range(1,79):
	PkmLvl.append(num / 2)

fixed_SD = [i / 100 for i in Total_stardust]

plt.plot(PkmLvl, CP_high_list ,PkmLvl, CP_low_list, PkmLvl, fixed_SD,)

plt.axhline(y = CP_low_list[j - lvl_dif], xmax = (j - lvl_dif)/80, dashes = [6,2])
plt.axhline(y = CP_high_list[j], xmax = j / 80, dashes = [6,2])

plt.axvline(x = PkmLvl[j], ymax = (Total_stardust[j] / 400000), dashes = [6,2])
plt.axvline(x = PkmLvl[j - lvl_dif], ymax = (Total_stardust[j - lvl_dif] / 400000), dashes = [6,2])

plt.xlim(0,40)
plt.ylim(0, 4000)
plt.xlabel('Pokemon Level')
plt.ylabel('Total CP (Blue) and Relative Stardust Cost (Orange)')
plt.title('Leveling guide for {0}'.format(p.name))

plt.show()

"""
