from joblib import load
import numpy as np
from psutil import virtual_memory, cpu_percent

aet_model = load("Model/aether_ai.pkl")
x_scaler = load("Model/x_scaler.pkl")
y_scaler = load("Model/y_scaler.pkl")

cpu_data = round(cpu_percent())
ram_data = round(virtual_memory().percent)

def find_cpu_load(val):
    if 0 <= val <= 30:
        return 0
    elif 31 <= val <= 70:
        return 1
    elif 71 <= val <= 100:
        return 2
    else:
        print("There is an error in the CPU load value")

def find_ram_load(val):
    if 0 <= val <= 50:
        return 3
    elif 51 <= val <= 80:
        return 4
    elif 81 <= val <= 100:
        return 5
    else:
        print("There is an error in the RAM load value")

cpu_load = find_cpu_load(cpu_data)
ram_load = find_ram_load(ram_data)

def start_model(model, cpu, cpu_load, ram, ram_load):
    eat_md = model
    predictData = np.array([[cpu, cpu_load, ram, ram_load]])
    predictData = x_scaler.transform(predictData)
    prediction = eat_md.predict(predictData)
    prediction = y_scaler.inverse_transform(prediction)
    return print(prediction)

print(f"CPU Usage: {cpu_data}%")
print(f"RAM Usage: {ram_data}%")
start_model(aet_model, cpu_data, cpu_load, ram_data, ram_load)