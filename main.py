# Universidad del Valle de Guatemala
# CC3039 - Modelacion y Simulacion
# Julio Herrera 19402
# Oliver De León 19
# Miniproyecto 4 - Modelacion de servidores

import random
import math
import numpy as np

# Representa un servidor de los utilizados en la simulacion
class Server(object):
    def __init__(self, name, limit_quantity, max):
        self.name = name
        self.limit_quantity = limit_quantity # Cantidad de servidores disponibles
        self.quantity = 1 # Cantidad de servidores en uso
        self.max = max # Maximo de solicitudes por segundo
        self.servers_requests = [[] for _ in range(self.quantity)] # tiempos de llegada de las solicitudes
        self.servers_response = [[] for _ in range(self.quantity)] # tiempos de respuesta de las solicitudes
        self.servers_states = [0 for _ in range(self.quantity)] # Usuarios en cada servidor
        self.servers_busy_time = [0 for _ in range(self.quantity)] # Suma del tiempo ocupado de cada servidor

    def get_free_server(self):
        min_current_users = math.inf
        server_index = -1
        for i in range(self.quantity):
            if self.servers_states[i] < min_current_users and self.servers_states[i] < self.max:
                min_current_users = self.servers_states[i]
                server_index = i
        return server_index

    def get_server_with_minor_next_response_time(self):
        minor_next_response_time = math.inf
        server_index = -1
        for i in range(self.quantity):
            if len(self.servers_response[i]) > 0:
                if self.servers_response[i][-1] < minor_next_response_time:
                    minor_next_response_time = self.servers_response[i][-1]
                    server_index = i
        return server_index

    def handle_request(self, request_time, server_index):
        if self.servers_states[server_index] < self.max:
            # Servidor disponible
            self.servers_states[server_index] += 1
            self.servers_requests[server_index].append(request_time)
            self.servers_response[server_index].append(math.inf)
            return True
        return False # Servidor ocupado

    def return_response(self, response_time, server_index):
        self.servers_states[server_index] -= 1
        self.servers_response[server_index].append(response_time)
        self.servers_busy_time[server_index] += response_time - self.servers_requests[server_index][-1]

    def add_server(self):
        if self.server.quantity < self.server.limit_quantity:
            self.server.quantity += 1
            self.server.servers_requests.append([])
            self.server.servers_response.append([])
            self.server.servers_states.append(0)
            self.server.servers_busy_time.append(0)
            return True
        return False # No se puede agregar mas servidores

# Entorno de simulacion de un servidor por tiempo
class Environment(object):
    def __init__(self, server, max_requests, simulation_time):
        self.server = server
        self.max_requests = max_requests
        self.simulation_time = simulation_time
        random.seed(0)

    # genera una nueva solicitud random
    def gen_poisson(self, lambda_):
        return -math.log(1.0 - random.random()) / lambda_

    # genera tiempo de solicitud random
    def gen_exponential(self, lambda_):
        return -math.log(1.0 - random.random()) / lambda_

    # ejecuta la simulacion
    def execute_one_server(self):
        requests_n = 0
        responses_n = 0
        current_users = 0
        t = 0 # tiempo inicial

        # Calculando primera solicitud
        time_next_request = self.gen_poisson(self.max_requests)
        time_next_response = math.inf

        # Almacenamiento de datos
        requests = {}
        responses = {}
        total_time = []

        while t <= self.simulation_time or current_users > 0:
            # Entra solicitud con tiempo menot a la siguiente respuesta
            if (time_next_request <= time_next_response and time_next_request <= self.simulation_time):
                t = time_next_request
                requests_n += 1
                current_users += 1
                time_next_request = t + self.gen_poisson(self.max_requests)
                if (current_users == 1):
                    random_var = self.gen_exponential(self.server.max)
                    time_next_response = t + random_var
                requests[requests_n] = t
                total_time.append(random_var)
            elif (time_next_response < time_next_request and time_next_response <= self.simulation_time):
                t = time_next_response
                current_users -= 1
                responses_n += 1
                if (current_users == 0):
                    time_next_response = math.inf
                else:
                    random_var = self.gen_exponential(self.server.max)
                    time_next_response = t + random_var
                responses[responses_n] = t
                total_time.append(random_var)
            # Hay todavia una solicitud o respuesta por procesar
            elif (min(time_next_request, time_next_response) > self.simulation_time and current_users > 0):
                t = time_next_response
                current_users -= 1
                responses_n += 1
                if (current_users > 0):
                    random_var = self.gen_exponential(self.server.max)
                    time_next_response = t + random_var   
                responses[responses_n] = t
                total_time.append(random_var)
            # Termina la simulacion
            elif (min(time_next_request, time_next_response) > self.simulation_time and current_users == 0):
                break

        self.print_results_one_server(responses_n, requests, responses, total_time)

    def print_results_one_server(self, responses_n, requests, responses, total_time):
        busy_time = sum(total_time)/3600
        idle_time = 3600-sum(total_time)
        attended_n = min(len(requests), len(responses))
        requests_list = list(requests.values())
        responses_list = list(responses.values())
        times = [(responses_list[i]-requests_list[i]) for i in range(attended_n)]
        time_mean = sum(times)/attended_n
        attended_mean = len(responses)/3600
        print(f"Resultados para el servidor {self.server.name}")
        print(f"Solicitudes atendidas: {str(responses_n)}")
        print(f"Tiempo ocupado: {str(busy_time)}")
        print(f"Tiempo idle: {str(idle_time)}")
        print(f"Tiempo total de solicitudes en cola: {str(sum(total_time))}")
        print(f"Promedio de tiempo de solicitudes en cola: {str(time_mean)}")
        print(f"Promedio de solicitudes en cola cada segundo: {str(attended_mean)}")
        print(f"Momento de ultima solicitud {str(list(requests.values())[-1])}")

    def execute_n_servers(self):
        requests_n = 0
        responses_n = 0
        current_users = 0
        # Por cada servidor
        servers_request_attendance = [0 for _ in range(self.server.limit_quantity)]
        servers_users_state = [0 for _ in range(self.server.limit_quantity)]
        servers_busy_time = [0 for _ in range(self.server.limit_quantity)]
        next_responses = [math.inf for _ in range(self.server.limit_quantity)]
        time_next_request = self.gen_poisson(self.max_requests)
        # Guardando datos
        requests, responses = {}, {}
        # Solicitudes en cola
        queue_times, dequeue_times = {}, {}
        t = time_next_request
        while t <= self.simulation_time or current_users > 0:
            # La solicitud entrante se hara en un tiempo antes que la siguiente respuesta por cualquier servidor
            if (time_next_request <= np.amin(next_responses)) and time_next_request <= self.simulation_time:
                t = time_next_request
                requests_n = requests_n + 1
                time_next_request = t + self.gen_poisson(self.max_requests)
                requests[requests_n] = t
                # Se busca un servidor libre
                if current_users < self.server.limit_quantity:
                    for i in range(self.server.limit_quantity):
                        if servers_users_state[i] == 0:
                            servers_users_state[i] = requests_n
                            next_duration = self.gen_exponential(self.server.max)
                            next_responses[i] = t + next_duration
                            servers_busy_time[i] += next_duration
                            break
                else:
                    queue_times[requests_n] = t
                current_users = current_users + 1
            else:
                min_time = math.inf
                server_index = 0
                for i in range(self.server.limit_quantity):
                    if next_responses[i] < min_time:
                        min_time = next_responses[i]
                        server_index = i
                t = next_responses[server_index]
                responses_n = responses_n + 1
                temp = servers_request_attendance[server_index]
                servers_request_attendance[server_index] = temp + 1
                responses[responses_n] = t
                current_users = current_users - 1

                if current_users >= self.server.limit_quantity:
                    m = np.amax(servers_users_state)
                    servers_users_state[server_index] = m + 1
                    next_duration = self.gen_exponential(self.server.max)
                    next_responses[server_index] = t + next_duration
                    servers_busy_time[server_index] += next_duration
                    dequeue_times[servers_users_state[server_index]] = t
                else:
                    servers_users_state[server_index] = 0
                    next_responses[server_index] = math.inf

        self.print_results_n_servers(t, requests_n, servers_request_attendance, servers_busy_time, requests, responses, queue_times, dequeue_times)

    def print_results_n_servers(self, t, requests_n, servers_request_attendance, servers_busy_time, requests, responses, queue_times, dequeue_times):
        q_sum = 0
        for k in queue_times:
            q_sum += (dequeue_times[k] - queue_times[k])
        req_time = 0
        for k in requests:
            req_time += (responses[k] - requests[k])
        print(f"Resultados para el servidor {self.server.name}")
        print(f"Tiempo total de solicitudes en cola: {q_sum}")
        print(f"Promedio de tiempo de solicitudes en cola: {q_sum / len(queue_times) if len(queue_times) > 0 else 0}")
        print(f"Promedio de solicitudes en cola cada segundo: {req_time / len(requests)}")
        print(f"Momento de ultima solicitud {t}")

        n_servers = len(servers_request_attendance)
        for i in range(n_servers):
            print("Servidor " + str(i + 1))
            print("Solicitudes atendidas: " + str(servers_request_attendance[i]))
            print("Tiempo ocupado: " + str(servers_busy_time[i]))
            print("Tiempo idle: " + str(t - servers_busy_time[i]))
            print()

def task1():
    # Parametros de simulacion
    simulation_time = 3600 # 3600 segundos = 1 hora
    server1 = Server("Mountain Mega Computing", 1, 100)
    server2 = Server("Pizzita computing", 10, 10)
    environment1 = Environment(server1, 2400 / 60, simulation_time)
    environment1.execute_one_server()
    environment2 = Environment(server2, 2400 / 60, simulation_time)
    environment2.execute_n_servers()

def task2():
    limit_quantity = [15, 16, 17]
    simulation_time = 3600 # 3600 segundos = 1 hora
    for i in limit_quantity:
        server = Server("Pizzita computing", i, 10)
        environment = Environment(server, 2400 / 60, simulation_time)
        environment.execute_n_servers()

def task3_1():
    # Parametros de simulacion
    simulation_time = 3600 # 3600 segundos = 1 hora
    server1 = Server("Mountain Mega Computing", 1, 100)
    server2 = Server("Pizzita computing", 10, 10)
    environment1 = Environment(server1, 6000 / 60, simulation_time)
    environment1.execute_one_server()
    environment2 = Environment(server2, 6000 / 60, simulation_time)
    environment2.execute_n_servers()

def task3_2():
    # task 2 para 6000 solicitudes por hora
    limit_quantity = [26, 27, 28]
    simulation_time = 3600 # 3600 segundos = 1 hora
    for i in limit_quantity:
        server = Server("Pizzita computing", i, 10)
        environment = Environment(server, 6000 / 60, simulation_time)
        environment.execute_n_servers()

task3_1()