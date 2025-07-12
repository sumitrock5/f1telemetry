from matplotlib import pyplot as plt
import fastf1
import fastf1.plotting

fastf1.plotting.setup_mpl(mpl_timedelta_support=True, misc_mpl_mods=False,
                          color_scheme='fastf1')

session = fastf1.get_session(2025, 'Bahrain', 'Q')

session.load()
fast_piastri = session.laps.pick_driver('PIA').pick_fastest()
pia_car_data = fast_piastri.get_car_data()
t_pia = pia_car_data['Time']
vCar_pia = pia_car_data['Speed']

fast_norris = session.laps.pick_driver('NOR').pick_fastest()
nor_car_data = fast_norris.get_car_data()
t_nor = nor_car_data['Time']
vCar_nor = nor_car_data['Speed']

pia_tel = fast_piastri.get_car_data().add_distance()
nor_tel = fast_norris.get_car_data().add_distance()

circuit_info = session.get_circuit_info()
x=circuit_info.corners['Distance']
num=circuit_info.corners['Number']


# saving data in csv
import csv
Data_pia = [vCar_pia,
        t_pia, pia_tel['Distance']]
with open("Data_pia.csv", "w", newline="") as file:
    writer = csv.writer(file)
    writer.writerows(Data_pia)

Data_nor = [vCar_nor,
        t_nor, nor_tel['Distance']]
with open("Data_nor.csv", "w", newline="") as file:
    writer = csv.writer(file)
    writer.writerows(Data_nor)


Data_Circuit = [x,
                num]
with open("Data_Circuit.csv", "w", newline="") as file:
    writer = csv.writer(file)
    writer.writerows(Data_Circuit)


# The rest is just plotting

fig, ax = plt.subplots()
ax.plot(pia_tel['Distance'], vCar_pia, color='white', label='pia')
ax.plot(nor_tel['Distance'], vCar_nor, color='red', label='nor')

ax.set_xlabel('Distance in m')
ax.set_ylabel('Speed in km/h')

ax.legend()
plt.suptitle(f"Fastest Lap Comparison \n "
             f"{session.event['EventName']} {session.event.year} Qualifying")

plt.show()