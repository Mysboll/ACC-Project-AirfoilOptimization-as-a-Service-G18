from celery import Celery
import subprocess

app = Celery('tasks', backend='amqp', broker='pyamqp://user:password@192.168.1.33:5672/vhost')

@app.tasks
def airfoil_simulation(angle, n_nodes, n_levels, num_samples, viscosity, velocity, duration):
    subprocess.run(["./airfoil_task.sh", angle, n_nodes, n_levels, num_samples, viscosity, velocity, duration])
    results = subprocess.run(['docker', 'exec', '-it', 'd08a03148001', 'cat', 'results/drag_ligt.m'], stdout=subprocess.PIPE)
    print(results.stdout)
    return results.stdout

@app.tasks
def sumcalc():

#airfoil_simulation('5', '200', '1', '10', '0.0001', '10', '0.1)