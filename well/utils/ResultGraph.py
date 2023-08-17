import math
import numpy as np
from operator import neg
import plotly.graph_objects as go
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D


def create_result_graph_2d_tipo_vertical(well_head, target, target_end):

    x_point = np.array([round(well_head[0], 2), round(target[0], 2), round(target_end[0], 2)])
    y_point = np.array([round(well_head[1], 2), round(target[1], 2), round(target_end[1], 2)])
    z_point = np.array([round(well_head[2], 2), round(target[2], 2), round(target_end[2], 2)])

    create_subplots_configuration(x_point, y_point, z_point, 'Vertical')
    create_result_graph_3d(x_point, y_point, z_point, 'Vertical')


def create_result_graph_2d_tipo1(well_head, start_kop_xyz, target, target_end, depth_eob_y, length_eob_y, depth_kop):

    x_start = np.array([round(well_head[0], 2), round(target[0], 2), round(target_end[0], 2)])
    y_start = np.array([round(well_head[1], 2), round(target[1], 2), round(target_end[1], 2)])
    z_start = np.array([round(well_head[2], 2), round(target[2], 2), round(target_end[2], 2)])

    x_point, y_point, z_point = create_points_graph(start_kop_xyz, depth_eob_y, length_eob_y, depth_kop)

    x_finally = np.insert(x_start, 1, x_point)
    y_finally = np.insert(y_start, 1, y_point)
    z_finally = np.insert(z_start, 1, z_point)

    #create_subplots_configuration(x_finally, y_finally, z_finally, '1')
    create_graph_web(y_finally, z_finally, '1')
    #create_result_graph_3d(x_finally, y_finally, z_finally, '1')


def create_result_graph_2d_tipo_S_or_horizontal(well_head, start_point1, start_point2, start_target, end_target,
                                                depth_point1, length_point1, depth_point2, length_point2,
                                                depth_projection1, depth_projection2, name):

    x_start = np.array([round(well_head[0], 2), round(start_target[0], 2), round(end_target[0], 2)])
    y_start = np.array([round(well_head[1], 2), round(start_target[1], 2), round(end_target[1], 2)])
    z_start = np.array([round(well_head[2], 2), round(start_target[2], 2), round(end_target[2], 2)])

    first_x_point, first_y_point, first_z_point = create_points_graph(start_point1, depth_point1, length_point1,
                                                                      depth_projection1)

    first_x_finally = np.insert(x_start, 1, first_x_point)
    first_y_finally = np.insert(y_start, 1, first_y_point)
    first_z_finally = np.insert(z_start, 1, first_z_point)

    position = len(first_x_finally) - 2

    second_x_point, second_y_point, second_z_point = create_points_graph(start_point2, depth_point2, length_point2,
                                                                         depth_projection2)

    second_x_finally = np.insert(first_x_finally, position, second_x_point)
    second_y_finally = np.insert(first_y_finally, position, second_y_point)
    second_z_finally = np.insert(first_z_finally, position, second_z_point)

    #create_subplots_configuration(second_x_finally, second_y_finally, second_z_finally, name)
    create_graph_web(second_y_finally, second_z_finally, name)
    #create_result_graph_3d(second_x_finally, second_y_finally, second_z_finally, name)


def create_result_graph_3d(point_x, point_y, point_z, name):

    d3 = plt.axes(projection="3d")
    d3.set_title('Trajetoria tipo ' + name)
    d3.set_xlabel('X')
    d3.set_ylabel('Y')
    d3.set_zlabel('Z')
    d3.plot3D(point_x, point_y, point_z, marker='o')

    for vx, vy, vz in zip(point_x, point_y, point_z):
        d3.text(vx - 0.5, vy + 0.2, vz + 0.2, vy)
    plt.show()


def create_points_graph(start, depth_xyz, length_xyz, depth_kop_or_dropp_off):

    axle_x = []
    axle_y = []
    axle_z = []

    for angle in range(0, 90+1, 1):

        axle_x.append(round((start[0] - abs(length_xyz[0] * math.sin(math.radians(angle)))), 2))
        axle_y.append(round((start[1] - abs(length_xyz[1] * math.sin(math.radians(angle)))), 2))
        axle_z.append(round((start[2] - abs((max(depth_xyz[0], depth_xyz[1]) - depth_kop_or_dropp_off) *
                                            (1 - math.cos(math.radians(angle))))), 2))

    axle_z.reverse()

    return axle_x, axle_y, axle_z


def create_subplots_configuration(point_x, point_y, point_z, text):

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(20, 10))

    fig.text(0.4, 0.95, 'Trajetoria tipo ' + text, fontsize=15)

    ax1.plot(point_x, neg(point_z))
    ax1.set_xlabel('Eixo X')
    ax1.set_ylabel('Eixo Z')

    ax2.plot(point_y, neg(point_z))
    ax2.set_xlabel("Eixo Y")
    ax2.set_ylabel('Eixo Z')

    plt.show()


def create_graph_web(point_y, point_z, name):

    fig_new = go.Figure()
    fig_new.add_trace(go.Scatter(x=point_y, y=neg(point_z), name='tipo1',
                                 line=dict(color='blue', width=4, dash='dot')))

    fig_new.update_layout(title='Trajetoria tipo ' + name,
                          xaxis_title='Y',
                          yaxis_title='Z')
    fig_new.show()
