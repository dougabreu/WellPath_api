from operator import neg

import numpy as np

from well.utils.generalUtils import deserializer
from well.model.EngineModel import EngineManager

from scipy.spatial import distance
import os
import math
import plotly.graph_objects as go


class TrajectoryServiceManager:

    def __init__(self, input_data):

        self.input_data = input_data
        self.well_info = deserializer(self.input_data)
        self.service = EngineManager(self.well_info)

        # dados de entrada
        self.start_target = [float(x) for x in self.well_info["xyz_star"].split(',')]
        self.end_target = [float(x) for x in self.well_info["xyz_end"].split(',')]
        self.well_head = [float(x) for x in self.well_info["well_head_start"].split(',')]

        # restricao operacional
        self.kop_vertical_projection = float(self.well_info["kop_depth"])
        self.reservoir_vertical_projection = float(self.well_info["trecho_verticalizacao"])
        self.reservoir_horizontal_projection = 0  # float(self.well_info["trecho_horizontal"])
        self.dog_leg_build_up = float(self.well_info[".DogLegSeverity(Â°/30,48m)"])
        self.dog_leg_drop_off = float(self.well_info["DogLegDropOff(Â°/30,48m)"])

        self.delta_x = self.start_target[0] - self.well_head[0]
        self.delta_y = self.start_target[1] - self.well_head[1]
        self.depth_eob_x_y = []
        self.depth_drop_off_eob_x_y = []
        self.length_eob_x_y = []
        self.length_drop_off_eob_x_y = []
        self.arc_angle_x_y = []
        self.angle_kop_and_drop_off = []
        self.va = self.start_target[2] - self.well_head[2]

    def check_target_trajectory(self):

        ## Vertical dentro do reservatorio
        if distance.euclidean((self.start_target[0], self.start_target[1]), (self.end_target[0], self.end_target[1])) < 1e-3:
            if not self.create_well_vertical_trajectory():
                return self.create_well_type_S_trajectory()

        ## Direcional dentro do reservatorio #######verificar validacao do tipo
        elif distance.euclidean((self.start_target[0], self.start_target[2]), (self.end_target[0], self.end_target[2])) < 1e-3:
            return self.create_well_type_1_trajectory()  # separar 1 kop
        else:
            return self.create_well_type_horizontal_trajectory() ## totalmente Horizontal dentro do reservatorio com 2 kop

    def create_well_vertical_trajectory(self):

        if distance.euclidean((self.well_head[0], self.well_head[1]), (self.end_target[0], self.end_target[1])) < 1e-3:
            save_state_data = {'cabeca_poco': self.well_head, ' inicio objetivo': self.start_target, 'fim objetivo': self.end_target}
            #serialize_data(save_state_data, os.path.basename(self.input_data))
            #create_result_graph_2d_tipo_vertical(self.well_head, self.start_target, self.end_target)
            return True

        return False

    def create_well_type_1_trajectory(self):

        try:

            ray = self.service.ray_curvature_calculation(self.dog_leg_build_up)

            #if self.kop_vertical_projection > (self.end_target[2] + ray):
            #    raise ExceptionManager.LengthKopAboveTheLimit()
            #if self.delta_x and self.delta_y != 0:
            #    if self.arc_angle_x_y[0] != self.arc_angle_x_y[1]:
            #        raise ExceptionManager.AngleEqualsValidation()
            #    if self.length_eob_x_y[0] != self.length_eob_x_y[1]:
             #       raise ExceptionManager.LengthEobEqualsValidation()

            self.arc_angle_x_y = self.service.arc_angle_projection_calculation(ray, self.kop_vertical_projection)

            start_kop1_xyz = self.start_build_up_calculation(self.well_head, 0, 0, self.kop_vertical_projection, '1')

            self.depth_eob_x_y, self.length_eob_x_y = self.service.arc_distance_projection_calculation(self.arc_angle_x_y, ray, start_kop1_xyz, self.start_target, self.kop_vertical_projection)

            if self.delta_x < 0:
                self.length_eob_x_y[0] = -1 * self.length_eob_x_y[0]
            if self.delta_y < 0:
                self.length_eob_x_y[1] = -1 * self.length_eob_x_y[1]

            #if round(max(self.arc_angle_x_y[0], self.arc_angle_x_y[1])) > 90:
            #    raise ExceptionManager.AngleAboveTheLimit()

            end_kop1_xyz = self.end_build_up_calculation(start_kop1_xyz)

            slant_angle = self.slant_inclination_calculation(end_kop1_xyz, self.start_target)

            length_well_head_to_kop, length_slant, length_vertical, length_finally, length_buildup, length_drop_off = self.well_length_calculation(slant_angle, start_kop1_xyz, end_kop1_xyz, self.start_target)

            length_total = length_well_head_to_kop + length_buildup + length_slant + length_finally

            distance_horizontal = self.service.distance_horizontal_calculation()

            save_state_data = {'cabeca_poco': str(self.well_head), 'kop': str(start_kop1_xyz), 'eob': str(end_kop1_xyz),
                               'inicio_objetivo': str(self.start_target), 'fim_objetivo': str(self.end_target),
                               'angulo': slant_angle, 'direcao_objetivo': self.service.direction_azimuth_calculation(),
                               'afastamento_objetivo': distance_horizontal,
                               'profundidade_vertical': self.end_target[2] - self.kop_vertical_projection,
                               'trecho_cabeca_kop': round(length_well_head_to_kop, 2),
                               'trecho_arco_buildup': round(length_buildup, 2), 'trecho_slant': round(length_slant, 2),
                               'trecho_canhoneado': round(length_finally, 2), 'comprimento_total': round(length_total, 2)}

            # self.create_result_graph_2d_tipo1(self.well_head, start_kop1_xyz, self.start_target, self.end_target,
            #

            return save_state_data

        except (
               # ExceptionManager.LengthKopAboveTheLimit,
               ## ExceptionManager.AngleAboveTheLimit,
              #  ExceptionManager.AngleEqualsValidation,
               # ExceptionManager.LengthEobEqualsValidation
        ) as exception:

            raise exception

    def create_well_type_S_trajectory(self):

        ray_1 = self.service.ray_curvature_calculation(self.dog_leg_build_up)
        ray_2 = self.service.ray_curvature_calculation(self.dog_leg_drop_off)

        self.arc_angle_x_y = self.service.arc_angle_projection_type_S_calculation(self.start_target[2] - self.reservoir_vertical_projection, ray_1 + ray_2)

        self.depth_eob_x_y, self.length_eob_x_y = self.service.arc_distance_projection_calculation(self.arc_angle_x_y, ray_1, self.well_head, self.start_target, self.kop_vertical_projection)

        if self.delta_x < 0:
            self.length_eob_x_y[0] = -1 * self.length_eob_x_y[0]
        if self.delta_y < 0:
            self.length_eob_x_y[1] = -1 * self.length_eob_x_y[1]

        start_kop1_xyz = self.start_build_up_calculation(self.well_head, 0, 0, self.kop_vertical_projection, '1')
        end_kop1_xyz = self.end_build_up_calculation(start_kop1_xyz)

        self.depth_drop_off_eob_x_y, self.length_drop_off_eob_x_y = self.service.arc_distance_projection_calculation(self.arc_angle_x_y, ray_2, self.start_target, start_kop1_xyz, self.reservoir_vertical_projection)

        if self.delta_x < 0:
            self.length_drop_off_eob_x_y[0] = -1 * self.length_drop_off_eob_x_y[0]
        if self.delta_y < 0:
            self.length_drop_off_eob_x_y[1] = -1 * self.length_drop_off_eob_x_y[1]

        end_drop_off_xyz = self.end_drop_off_calculation()
        start_drop_off_xyz = self.start_drop_off_calculation(end_drop_off_xyz)

        slant_angle = self.slant_inclination_calculation(end_kop1_xyz, start_drop_off_xyz)

        length_well_head_to_kop, length_slant, length_vertical, length_finally, length_buildup, length_drop_off = self.well_length_calculation(slant_angle, start_kop1_xyz, end_kop1_xyz, start_drop_off_xyz)

        length_total = length_well_head_to_kop + length_buildup + length_slant + length_drop_off + length_vertical + length_finally

        distance_horizontal = self.service.distance_horizontal_calculation()

        save_state_data = {'cabeca_poco': self.well_head, 'first_kop': start_kop1_xyz, 'eob': end_kop1_xyz, 'drop_off_xyz': start_drop_off_xyz,
                           'trecho_reto': end_drop_off_xyz, 'objetivo': self.start_target, 'fim_objetivo': self.end_target,
                           'angulo': slant_angle, 'direcao_objetivo': self.service.direction_azimuth_calculation(),
                           'afastamento do objetivo': distance_horizontal,
                           'profundidade vertical': self.end_target[2] - self.kop_vertical_projection,
                           'trecho_cabeca_kop': round(length_well_head_to_kop, 2),
                           'trecho_arco_buildup': round(length_buildup, 2), 'trecho_slant': round(length_slant, 2),
                           'trecho_drop_off': round(length_drop_off, 2), 'trecho_verticalizacao': round(length_vertical, 2),
                           'trecho_canhoneado': round(length_finally, 2), 'comprimento_total': round(length_total, 2)}

        #serialize_data(save_state_data, os.path.basename(self.input_data))

       # create_result_graph_2d_tipo_S_or_horizontal(self.well_head, start_kop1_xyz, start_drop_off_xyz,
        #                                            self.start_target, self.end_target, self.depth_eob_x_y,
        #                                            self.length_eob_x_y, self.depth_drop_off_eob_x_y,
        #                                            self.length_drop_off_eob_x_y, self.kop_vertical_projection,
        #                                            self.reservoir_vertical_projection, 'S')

    def create_well_type_horizontal_trajectory(self):

        ray = self.service.ray_curvature_calculation(self.dog_leg_build_up)

        self.arc_angle_x_y = self.service.arc_angle_projection_calculation(ray, self.kop_vertical_projection)

        start_kop1_xyz = self.start_build_up_calculation(self.well_head, 0, 0, self.kop_vertical_projection, '1')

        self.depth_eob_x_y, self.length_eob_x_y = self.service.arc_distance_projection_calculation(self.arc_angle_x_y, ray,
                                                                                                   start_kop1_xyz,
                                                                                                   self.start_target,
                                                                                                   self.kop_vertical_projection)

        if self.delta_x < 0:
            self.length_eob_x_y[0] = -1 * self.length_eob_x_y[0]
        if self.delta_y < 0:
            self.length_eob_x_y[1] = -1 * self.length_eob_x_y[1]

        end_kop1_xyz = self.end_build_up_calculation(start_kop1_xyz)

        # second_kop__xyz
        arc_angle_x_y = self.service.arc_angle_projection_calculation(ray, self.reservoir_horizontal_projection)

        depth_eob_x_y, length_eob_x_y = self.service.arc_distance_projection_calculation(arc_angle_x_y, ray,
                                                                                         self.start_target, end_kop1_xyz,
                                                                                         self.reservoir_horizontal_projection)

        if self.delta_x < 0:
            length_eob_x_y[0] = -1 * length_eob_x_y[0]
        if self.delta_y < 0:
            length_eob_x_y[1] = -1 * length_eob_x_y[1]

        end_kop2_xyz = self.end_kop2_segment_calculation()

        start_kop2_xyz = self.start_build_up_calculation(end_kop2_xyz, length_eob_x_y[0], length_eob_x_y[1],
                                                         self.reservoir_horizontal_projection, '2')

        angle_new = self.slant_inclination_calculation(end_kop1_xyz, start_kop2_xyz)

        angle_new2 = self.slant_inclination_calculation(end_kop2_xyz, self.start_target)

        length_well_head_to_kop, length_slant, length_vertical, length_finally, length_buildup, length_drop_off = \
            self.well_length_calculation(angle_new, start_kop1_xyz, end_kop1_xyz, start_kop2_xyz)

        length_total = length_well_head_to_kop + length_buildup + length_slant + length_buildup + length_vertical + length_finally

        distance_horizontal = self.service.distance_horizontal_calculation()

        save_state_data = {'cabeca_poco': self.well_head, 'first_kop': start_kop1_xyz, 'eob': end_kop1_xyz,
                           'second_kop': start_kop2_xyz,
                           'trecho_reto': end_kop2_xyz, 'objetivo': self.start_target,
                           'fim_objetivo': self.end_target,
                           'angulo_kop': angle_new, 'angulo_second_kop': angle_new2,
                           'direcao_objetivo': self.service.direction_azimuth_calculation(),
                           'afastamento do objetivo': distance_horizontal,
                           'profundidade vertical': self.end_target[2] - self.kop_vertical_projection,
                           'trecho_cabeca_kop': round(length_well_head_to_kop, 2),
                           'trecho_arco_buildup': round(length_buildup, 2), 'trecho_slant': round(length_slant, 2),
                           'trecho_arco_buildup2': round(length_buildup, 2),
                           'trecho_verticalizacao': round(length_vertical, 2),
                           'trecho_canhoneado': round(length_finally, 2), 'comprimento_total': round(length_total, 2)}

        #serialize_data(save_state_data, os.path.basename(self.input_data))

        #create_result_graph_2d_tipo_S_or_horizontal(self.well_head, start_kop1_xyz, start_kop2_xyz, self.start_target,
        #                                            self.end_target, self.depth_eob_x_y, self.length_eob_x_y,
        #                                            depth_eob_x_y, length_eob_x_y, self.kop_vertical_projection,
        #                                            self.reservoir_vertical_projection, 'Horizontal com 2 kops')

    def end_build_up_calculation(self, kop_xyz):

        length_eob_z = max(self.depth_eob_x_y[0], self.depth_eob_x_y[1]) - self.kop_vertical_projection

        eob_x = kop_xyz[0] + self.length_eob_x_y[0]
        eob_y = kop_xyz[1] + self.length_eob_x_y[1]
        eob_z = kop_xyz[2] + length_eob_z

        return [round(eob_x, 2), round(eob_y, 2), round(eob_z, 2)]

    def start_drop_off_calculation(self, initial_finally_target_xyz):

        length_second_kop_z = max(self.depth_drop_off_eob_x_y[0], self.depth_drop_off_eob_x_y[1]) - self.reservoir_vertical_projection

        drop_off_x = initial_finally_target_xyz[0] - self.length_drop_off_eob_x_y[0]
        drop_off_y = initial_finally_target_xyz[1] - self.length_drop_off_eob_x_y[1]
        drop_off_z = initial_finally_target_xyz[2] - length_second_kop_z

        return [round(drop_off_x, 2), round(drop_off_y, 2), round(drop_off_z, 2)]

    def end_drop_off_calculation(self):

        vertical_segment_x = self.start_target[0]
        vertical_segment_y = self.start_target[1]
        vertical_segment_z = self.start_target[2] - self.reservoir_vertical_projection

        return [round(vertical_segment_x, 2), round(vertical_segment_y, 2), round(vertical_segment_z, 2)]

    def well_length_calculation(self, slant_angle, kop_xyz, eob_xyz, drop_off_xyz):

        length_well_head_to_kop = self.service.segment_length_calculation(self.well_head, kop_xyz)
        length_slant = self.service.segment_length_calculation(eob_xyz, drop_off_xyz)
        length_vertical = self.reservoir_vertical_projection
        length_finally = self.service.segment_length_calculation(self.start_target, self.end_target)

        length_buildup = self.service.arc_length_calculation(slant_angle, self.dog_leg_build_up)
        length_drop_off = self.service.arc_length_calculation(slant_angle, self.dog_leg_drop_off)

        return length_well_head_to_kop, length_slant, length_vertical, length_finally, length_buildup, length_drop_off

    @staticmethod
    def start_build_up_calculation(start_point, point_x, point_y, point_z, location_kop):

        if location_kop == '1':
            kop_x = start_point[0]
            kop_y = start_point[1]
            kop_z = start_point[2] + point_z
        else:
            length_kop_z = max(point_x, point_y) + point_z
            kop_x = start_point[0] - point_x
            kop_y = start_point[1] - point_y
            kop_z = start_point[2] - length_kop_z

        return [round(kop_x, 2), round(kop_y, 2), round(kop_z, 2)]

    @staticmethod
    def slant_inclination_calculation(start, end):

        try:
            distance_xy = math.sqrt((start[0] - end[0]) ** 2 + (start[1] - end[1]) ** 2)
            distance_z = end[2] - start[2]
            angle = round(math.degrees(math.atan(distance_xy / distance_z)), 2)
        except ZeroDivisionError:
            angle = 0.0

        return angle

    def end_kop2_segment_calculation(self):

        point_x = self.start_target[0]
        point_y = self.start_target[1] - self.reservoir_vertical_projection
        point_z = self.start_target[2]

        return [round(point_x, 2), round(point_y, 2), round(point_z, 2)]

    def create_result_graph_2d_tipo1(self, well_head, start_kop_xyz, target, target_end, depth_eob_y, length_eob_y, depth_kop):

        x_start = np.array([round(well_head[0], 2), round(target[0], 2), round(target_end[0], 2)])
        y_start = np.array([round(well_head[1], 2), round(target[1], 2), round(target_end[1], 2)])
        z_start = np.array([round(well_head[2], 2), round(target[2], 2), round(target_end[2], 2)])

        x_point, y_point, z_point = self.create_points_graph(start_kop_xyz, depth_eob_y, length_eob_y, depth_kop)

        x_finally = np.insert(x_start, 1, x_point)
        y_finally = np.insert(y_start, 1, y_point)
        z_finally = np.insert(z_start, 1, z_point)

        fig_new = go.Figure()
        fig_new.add_trace(go.Scatter(x=y_finally, y=neg(z_finally), name='tipo1',
                                     line=dict(color='blue', width=4, dash='dot')))

        fig_new.update_layout(title='Trajetoria tipo !',
                              xaxis_title='Y',
                              yaxis_title='Z')
        fig_new.show()

    def create_points_graph(self, start, depth_xyz, length_xyz, depth_kop_or_dropp_off):

        axle_x = []
        axle_y = []
        axle_z = []

        for angle in range(0, 90 + 1, 1):
            x = length_xyz[0] * math.sin(math.radians(angle))
            y = length_xyz[1] * math.sin(math.radians(angle))
            z = (max(depth_xyz[0], depth_xyz[1]) - depth_kop_or_dropp_off) * (1 - math.cos(math.radians(angle)))

            axle_x.append(round((start[0] - abs(x)), 2))
            axle_y.append(round((start[1] - abs(y)), 2))
            axle_z.append(round((start[2] - abs(z)), 2))

        axle_z.reverse()

        return axle_x, axle_y, axle_z
