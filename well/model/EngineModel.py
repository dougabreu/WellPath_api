import math


class EngineManager:

    def __init__(self, well_info):

        self.well_info = well_info

        self.start_target = [float(x) for x in self.well_info["xyz_star"].split(',')]
        self.end_target = [float(x) for x in self.well_info["xyz_end"].split(',')]
        self.well_head = [float(x) for x in self.well_info["well_head_start"].split(',')]
        self.kop_vertical_projection = float(self.well_info["kop_depth"])

        self.dog_leg_unit = '30.48'
        self.va = self.start_target[2] - self.well_head[2]

    # Raio de curvatura
    def ray_curvature_calculation(self, dog_leg_or_drop_off):

        return (180 / math.pi) * (float(self.dog_leg_unit) / float(dog_leg_or_drop_off))

    # Da
    @staticmethod
    def horizontal_distance_calculation(start, end):

        return math.sqrt((start - end) ** 2)

    def distance_horizontal_calculation(self):

        return math.sqrt((self.well_head[0] - self.start_target[0]) ** 2 + (self.well_head[1] - self.start_target[1]) ** 2)

    def arc_angle_projection_calculation(self, ray, vertical_segment):

        arc_angle_x_y = []
        distance_x = self.horizontal_distance_calculation(self.well_head[0], self.start_target[0])
        distance_y = self.horizontal_distance_calculation(self.well_head[1], self.start_target[1])

        if distance_x != 0:
            calculation_1 = math.degrees(math.asin(ray / (math.sqrt((ray - distance_x) ** 2 + (self.va - vertical_segment) ** 2))))
            calculation_2 = math.degrees(math.atan((ray - distance_x) / (self.va - vertical_segment)))
            arc_angle_x_y.append(calculation_1 - calculation_2)
        else:
            arc_angle_x_y.append(0)
        if distance_y != 0:
            calculation_1 = math.degrees(math.asin(ray / (math.sqrt((ray - distance_y) ** 2 + (self.va - vertical_segment) ** 2))))
            calculation_2 = math.degrees(math.atan((ray - distance_y) / (self.va - vertical_segment)))
            arc_angle_x_y.append(calculation_1 - calculation_2)
        else:
            arc_angle_x_y.append(0)

        return arc_angle_x_y

    # Complemento trecho em buildup - Ldc
    def build_up_length_calculation(self, arc_angle, dog_leg_kop):

        return arc_angle / (float(dog_leg_kop) / float(self.dog_leg_unit))

    # D1
    @staticmethod
    def build_up_horizontal_distance_calculation(ray, arc_angle):

        return ray * (1 - (math.cos(math.radians(arc_angle))))

    # V1
    @staticmethod
    def end_build_up_depth_calculation(ray, arc_angle, vertical_segment):

        return vertical_segment + ray * math.sin(math.radians(arc_angle))

    # Comprimento trecho reto - Lcb
    def slant_length_calculation(self, depth_eob, arc_angle):

        return (self.va - depth_eob) / math.cos(math.radians(arc_angle))

    def arc_angle_projection_type_S_calculation(self, v2, ray_total):

        arc_angle_x_y = []

        distance_x = self.horizontal_distance_calculation(self.well_head[0], self.start_target[0])
        distance_y = self.horizontal_distance_calculation(self.well_head[1], self.start_target[1])

        if distance_x != 0:
            calculation_1 = math.degrees(math.atan((self.va - self.kop_vertical_projection) / (ray_total - distance_x)))
            calculation_2 = math.degrees(math.acos(ray_total / (self.va - self.kop_vertical_projection)))
            calculation_3 = math.degrees(math.atan((v2 - self.kop_vertical_projection) / (ray_total - distance_x)))
            arc_angle_x_y.append(calculation_1 - (calculation_2 * math.sin(math.radians(calculation_3))))
        else:
            arc_angle_x_y.append(0)
        if distance_y != 0:
            calculation_1 = math.degrees(math.atan((self.va - self.kop_vertical_projection) / (ray_total - distance_y)))
            calculation_2 = math.degrees(math.acos(ray_total / (self.va - self.kop_vertical_projection)))
            calculation_3 = math.degrees(math.atan((v2 - self.kop_vertical_projection) / (ray_total - distance_y)))
            arc_angle_x_y.append((calculation_1 - (calculation_2 * math.sin(math.radians(calculation_3)))))
        else:
            arc_angle_x_y.append(0)

        return arc_angle_x_y

    def arc_distance_projection_calculation(self, arc_angle_x_y, ray, start, end, vertical_segment):

        depth_eob_x_y = []
        length_eob_x_y = []

        distance_x = self.horizontal_distance_calculation(start[0], end[0])
        distance_y = self.horizontal_distance_calculation(start[1], end[1])

        if distance_x != 0:
            depth_eob_x_y.append(self.end_build_up_depth_calculation(ray, arc_angle_x_y[0], vertical_segment))
            length_eob_x_y.append(self.build_up_horizontal_distance_calculation(ray, arc_angle_x_y[0]))
        else:
            depth_eob_x_y.append(0)
            length_eob_x_y.append(0)
        if distance_y != 0:
            depth_eob_x_y.append(self.end_build_up_depth_calculation(ray, arc_angle_x_y[1], vertical_segment))
            length_eob_x_y.append(self.build_up_horizontal_distance_calculation(ray, arc_angle_x_y[1]))
        else:
            depth_eob_x_y.append(0)
            length_eob_x_y.append(0)

        return depth_eob_x_y, length_eob_x_y

    @staticmethod
    def segment_length_calculation(start, end):

        return math.sqrt((start[0] - end[0]) ** 2 + (start[1] - end[1]) ** 2 + (start[2] - end[2]) ** 2)

    def arc_length_calculation(self, arc_angle, dog_leg):

        return self.build_up_length_calculation(arc_angle, dog_leg)

    # Direcao do objetivo
    def direction_objective_calculation(self):

        try:
            dir_objective = math.degrees(math.tan((round(self.well_head[1], 2) - round(self.start_target[1], 2)) / (round(self.well_head[0], 2) - round(self.start_target[0], 2))))
        except ZeroDivisionError:
            dir_objective = 0.0

        return abs(dir_objective)

    def direction_azimuth_calculation(self):

        azimuth = self.direction_objective_calculation()

        if azimuth <= 90:
            direction = str(round(azimuth, 2)) + ' graus NE'
        elif 90 < azimuth <= 180:
            direction = str(180 - round(azimuth, 2)) + ' graus SE'
        elif 180 < azimuth <= 270:
            direction = str(round(azimuth, 2) - 180) + ' graus SW'
        else:
            direction = str(360 - round(azimuth, 2)) + ' graus NO'

        return direction
