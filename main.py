# Universidad del Valle de Guatemala
# CC3039 - Modelacion y Simulacion
# Julio Herrera 19402
# Oliver De León 19
# Miniproyecto 4 - Modelacion de servidores

import simpy
import random
import math
import numpy as np
import matplotlib.pyplot as plt

# Representa un servidor de los utilizados en la simulacion
class Server(object):
    def __init__(self, name, limit_quantity, max):
        self.name = name
        self.limit_quantity = limit_quantity # Cantidad de servidores disponibles
        self.quantity = 1 # Cantidad de servidores en uso
        self.max = max # Maximo de solicitudes por segundo

    def get_request(self):
        pass

    def return_response(self):
        pass

    def add_server(self):
        self.quantity += 1

# Entorno de simulacion de un servidor por tiempo
class Environment(object):
    def __init__(self, server, max_requests, time):
        self.server = server
        self.max_requests = max_requests
        self.time = time
        self.requests = 0
        self.responses = 0
        random.seed(0)

    # genera una nueva solicitud random
    def gen_poisson(self, lambda_):
        return -math.log(1.0 - random.random()) / lambda_

    # genera tiempo de solicitud random
    def gen_exponential(self, lambda_):
        return -math.log(1.0 - random.random()) / lambda_