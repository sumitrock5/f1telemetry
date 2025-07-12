from matplotlib import pyplot as plt
import fastf1
import fastf1.plotting

fastf1.plotting.setup_mpl(mpl_timedelta_support=True, misc_mpl_mods=False,
                          color_scheme='fastf1')

session = fastf1.get_session(2025, 'China', 'SQ')

session.load()
fast_leclerc = session.laps.pick_driver('LEC').pick_fastest()
lec_car_data = fast_leclerc.get_car_data()
t_lec = lec_car_data['Time']
vCar_lec = lec_car_data['Speed']

fast_hamilton = session.laps.pick_driver('HAM').pick_fastest()
ham_car_data = fast_hamilton.get_car_data()
t_ham = ham_car_data['Time']
vCar_ham = ham_car_data['Speed']

lec_tel = fast_leclerc.get_car_data().add_distance()
ham_tel = fast_hamilton.get_car_data().add_distance()

circuit_info = session.get_circuit_info()
x=circuit_info.corners['Distance']
num=circuit_info.corners['Number']


# saving data in csv
import csv
Data_lec = [vCar_lec,
        t_lec, lec_tel['Distance']]
with open("Data_lec.csv", "w", newline="") as file:
    writer = csv.writer(file)
    writer.writerows(Data_lec)

Data_ham = [vCar_ham,
        t_ham, ham_tel['Distance']]
with open("Data_ham.csv", "w", newline="") as file:
    writer = csv.writer(file)
    writer.writerows(Data_ham)


Data_Circuit = [x,
                num]
with open("Data_Circuit.csv", "w", newline="") as file:
    writer = csv.writer(file)
    writer.writerows(Data_Circuit)


# The rest is just plotting

fig, ax = plt.subplots()
ax.plot(lec_tel['Distance'], vCar_lec, color='white', label='LEC')
ax.plot(ham_tel['Distance'], vCar_ham, color='red', label='HAM')

ax.set_xlabel('Distance in m')
ax.set_ylabel('Speed in km/h')

ax.legend()
plt.suptitle(f"Fastest Lap Comparison \n "
             f"{session.event['EventName']} {session.event.year} Qualifying")

plt.show()