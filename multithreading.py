
import threading
import time
import random

max_threads_weight_sum = 20

semaphore = threading.Semaphore(max_threads_weight_sum)

def exec_aquirement(thread_weight):
	for _ in range(thread_weight):
		semaphore.acquire()

def exec_release(thread_weight):
	for _ in range(thread_weight):
		semaphore.release()

def get_file_content(file_path):
	f = open(file_path, "r")
	return f.read()

def thread_function(thread_name, thread_weight):
    
	counter = 0

	while True:
		counter += 1
		print(f"{thread_name}: esperando liberação do recurso...")
		exec_aquirement(thread_weight) 

		print(f"{thread_name}: ---- CONSUMINDO RECURSO ----")
		resource_content = get_file_content('./recurso.txt')
		print(f"{thread_name}: conteúdo do recurso: {resource_content}")
		time.sleep(5)

		exec_release(thread_weight) 
		print(f"{thread_name}: número de execuções: {counter}.")
		print(f"{thread_name}: recurso liberado.")

def create_threads(numero_de_threads):
	lista_de_threads = []
	used_ids_list = [0]
 
	for _ in range(numero_de_threads):
     
		new_id = None
		while (new_id == None) or (new_id in used_ids_list):
			new_id = random.randint(1,10)

		used_ids_list.append(new_id)

		thread_name = f"thread_{new_id}"

		thread = threading.Thread(target=thread_function, args=(thread_name, new_id))

		print(f"Thread {thread_name} criada com peso {new_id}!")

		lista_de_threads.append({
				'thread': thread,
				'id': new_id,
		})

	return lista_de_threads

def start_threads(thread_list):
	for thread_info in thread_list:
		print(f"Iniciando thread {thread_info['id']}")

		thread = thread_info['thread']
		thread.start()

thread_list = create_threads(3)

start_threads(thread_list)