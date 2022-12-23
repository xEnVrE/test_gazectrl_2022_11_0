import numpy
import time
import yarp


def look_at(gaze, position):

    position_yarp = yarp.Vector(3)
    for i in range(3):
        position_yarp[i] = position[i]

    gaze.lookAtFixationPointSync(position_yarp)


def main():

    robot_name = 'icubSim'

    props = yarp.Property()
    props.put('device', 'gazecontrollerclient');
    props.put('local', '/example/gaze')
    props.put('remote', '/' + robot_name + '/gazecontroller')
    gaze_driver = yarp.PolyDriver(props)
    if not gaze_driver:
        print('Cannot open the gaze driver.')
        exit(1)

    gaze = gaze_driver.viewIGazeControl()
    if not gaze:
        print('Cannot get the IGazeControl view.')
        exit(1)

    fixation = [-0.5, 0.0, 0.2]
    look_at(gaze, fixation)

    time.sleep(3.0)
    gaze_driver.close()


if __name__ == '__main__':
    main()
