from flask import Flask, jsonify, request
from celery import chord
from datetime import datetime
from docker_call import airfoil_simulation, sumcalc

app = Flask(__name__)

@app.route('/airfoil/api/', methods=['GET'])
def airfoil_calculation():
    angle_start = request.args.get('angle_start')
    angle_stop = request.args.get('angle_stop')
    n_angles = request.args.get('n_angles')
    n_nodes = request.args.get('n_nodes')
    n_levels = request.args.get('n_levels')
    num_samples = request.arg.get('num_samples')
    viscosity = request.arg.get('viscosity')
    velocity = request.arg.get('velocity')
    duration = request.arg.get('duration')
    start = datetime.today()
    anglediff = (angle_stop - angle_start)/n_angles
    header = []
    for i in range(n_angles):
        angle = angle_start+i*anglediff
        header.append(airfoil_simulation.s(angle, n_nodes, n_levels, num_samples, viscosity, velocity, duration))

    callback = sumcalc.s()
    result = chord(header)(callback)
    ret = jsonify(result.wait())
    stop = datetime.today()
    print (stop - start)
    return ret



if __name__ == '__main__':
    app.run(host='0.0.0.0', debug = False)