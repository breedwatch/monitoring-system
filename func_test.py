from helper.logger import SensorDataError

mynumber = input("gib eine Nummer ein: ")
try:
    if int(mynumber) > 10:
        raise SensorDataError("aht20")
    else:
        print("nummer ist kleiner als 10 - gratuliere!")
except ValueError:
    print("keine nummer")
