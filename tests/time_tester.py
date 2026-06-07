import requests
import time
import numpy as np
import random

def test_map():
    curls_map = [
        "http://localhost:8080/orbit_view/get_map?filter_groups=%5B%7B%22log_op%22%3A%22NONE%22%2C%20%22filters%22%3A%5B%7B%22field%22%3A%22lib_point%22%2C%20%22op%22%3A%22like%22%2C%20%22value%22%3A%22L1%22%7D%5D%7D%5D",
        "http://localhost:8080/orbit_view/get_map?filter_groups=%5B%7B%22log_op%22%3A%22NONE%22%2C%20%22filters%22%3A%5B%7B%22field%22%3A%22lib_point%22%2C%20%22op%22%3A%22like%22%2C%20%22value%22%3A%22L2%22%7D%5D%7D%5D",
    ]
    for url in curls_map:
        times = []
        for _ in range(10):
            start = time.time()
            response = requests.get(url)
            times.append(time.time() - start)
            time.sleep(3)
        print(f"Запрос выполнился за {np.array(times).mean():.4f} секунд")

def test_one_orbit():
    times = []
    for _ in range(10):
        start_orbit = time.time()
        response = requests.get(f"http://localhost:8080/orbit_view/get_nearest_orbit?x={random.randint(-700000, 500000)}&z={random.randint(0, 300000)}")
        end_orbit = time.time()
        start_trajectory = time.time()
        response = requests.get(f"http://localhost:8080/trajectory_points/get_chunk?filter_groups=%5B%7B%22log_op%22%3A%22NONE%22%2C%20%22filters%22%3A%5B%7B%22field%22%3A%22orbit_id%22%2C%20%22op%22%3A%22%3D%3D%22%2C%20%22value%22%3A{random.randint(1, 11000)}%7D%5D%7D%5D")
        end_trajectory = time.time()
        times.append((end_orbit-start_orbit)+(end_trajectory-start_trajectory))
        time.sleep(3)
    print(f"Запрос выполнился за {np.array(times).mean():.4f} секунд")

def test_params():
    params = ["t", "ax", "ay", "az", "dist_primary", "dist_secondary", "cj", "floke"]
    times = []
    for _ in range(10):
        start = time.time()
        response = requests.get(f"http://localhost:8080/orbit_view/get_family_param?lib_point=L2&family_tag=H.2P1&param_name_x={params[random.randint(0, len(params)-1)]}&param_name_y={params[random.randint(0, len(params)-1)]}&param_name_z={params[random.randint(0, len(params)-1)]}")
        times.append(time.time() - start)
        time.sleep(3)
    print(f"Запрос выполнился за {np.array(times).mean():.4f} секунд")

def test_sections():
    planes = ["x", "y", "z", "vx", "vy", "vz"]
    times = []
    for _ in range(10):
        start = time.time()
        response = requests.get(f"http://localhost:8080/orbit_poincare_view/get_nearest_section?x={random.randint(-700000, 500000)}&z={random.randint(0, 300000)}&plane={planes[random.randint(0, len(planes)-1)]}%20%3D%200")
        times.append(time.time() - start)
        time.sleep(3)
    print(f"Запрос выполнился за {np.array(times).mean():.4f} секунд")

def test_const():
    times = []
    for _ in range(10):
        start = time.time()
        response = requests.get(
            f"http://localhost:8080/orbit_poincare_view/get_by_cj?filter_groups=%5B%7B%22log_op%22%3A%22NONE%22%2C%20%22filters%22%3A%5B%7B%22field%22%3A%22lib_point%22%2C%20%22op%22%3A%22like%22%2C%20%22value%22%3A%22L1%22%7D%2C%7B%22field%22%3A%22plane%22%2C%20%22op%22%3A%22like%22%2C%20%22value%22%3A%22y%20%3D%200%22%7D%2C%7B%22field%22%3A%22cj%22%2C%20%22op%22%3A%22%3D%3D%22%2C%20%22value%22%3A{random.random() + 2.5}%7D%5D%7D%5D&rate={random.random()}")
        times.append(time.time() - start)
        time.sleep(3)
    print(f"Запрос выполнился за {np.array(times).mean():.4f} секунд")

if __name__=="__main__":
    print("Карта начальных условий")
    test_map()
    print("Страницы с одной орбитой")
    test_one_orbit()
    print("Страница с выбором параметров")
    test_params()
    print("Страница с сечениями Пуанкаре")
    test_sections()
    print("Страница с фиксированной константой Якоби")
    test_const()