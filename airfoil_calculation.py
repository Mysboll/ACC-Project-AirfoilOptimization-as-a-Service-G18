from flask import Flask, jsonify, request
from celery import group
from datetime import datetime
from docker_call import airfoil_simulation

app = Flask(__name__)

@app.route('/airfoil/api', methods=['GET'])
def airfoil_calculation():
    angle_start = int(request.args.get('angle_start'))
    angle_stop = int(request.args.get('angle_stop'))
    n_angles = int(request.args.get('n_angles'))
    n_nodes = int(request.args.get('n_nodes'))
    n_levels = int(request.args.get('n_levels'))
    num_samples = int(request.args.get('num_samples'))
    viscosity = float(request.args.get('viscosity'))
    velocity = float(request.args.get('velocity'))
    duration = float(request.args.get('duration'))
    start = datetime.today()
    anglediff = ((angle_stop - angle_start)/n_angles)
    header = []
    print(anglediff)

    group(airfoil_simulation.s(angle_start+i*anglediff, n_nodes, n_levels, num_samples, viscosity, velocity, duration) for i in range (n_angles))()
    """for i in range(n_angles):
        angle = angle_start+i*anglediff
        header.append(airfoil_simulation.s(angle, n_nodes, n_levels, num_samples, viscosity, velocity, duration))"""

    ###callback = sumcalc.s()
    result = chord(header)()
    ret = jsonify(result.wait())
    stop = datetime.today()
    print (stop - start)
    return ret
"""curl "http://130.238.29.7:5000/airfoil/api?angle_start=10&angle_stop=16&n_angles=2&n_nodes=100&n_levels=1&num_samples=10&viscosity=0.0001&velocity=10&duration=1"
"""


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug = False)