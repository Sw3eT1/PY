import math
import random
import uuid


class Animal:
    def __init__(self, range_of_movement, starting_possible_spawn_range):
        self.coordinates = [0.0, 0.0]
        self.id = uuid.uuid4()
        self.range_of_movement = range_of_movement
        self.starting_possible_spawn_range = starting_possible_spawn_range

    def generate_starting_position(self):
            rand_starting_x = random.uniform(
                self.starting_possible_spawn_range[0],
                self.starting_possible_spawn_range[1])

            rand_starting_y = random.uniform(
                self.starting_possible_spawn_range[0],
                self.starting_possible_spawn_range[1])

            self.coordinates[0] = rand_starting_x
            self.coordinates[1] = rand_starting_y

    def generate_direction(self):
        POSSIBLE_DIRECTIONS = ["left", "right", "up", "down"]
        return random.choice(POSSIBLE_DIRECTIONS)


    def move_using_direction(self, direction):
        if direction == "left":
            self.coordinates[0] -= self.range_of_movement
        elif direction == "right":
            self.coordinates[0] += self.range_of_movement
        elif direction == "up":
            self.coordinates[1] += self.range_of_movement
        elif direction == "down":
            self.coordinates[1] -= self.range_of_movement


class Wolf(Animal):
    def __init__(self):
        super().__init__(1.0, (0.0, 0.0))
        self.current_pray_to_chase = None
        self.logger = None

    def attach_logger(self, logger):
        self.logger = logger

    def find_closest_sheep(self, all_sheep):
        if not all_sheep:
            self.current_pray_to_chase = None
            return

        closest_sheep = all_sheep[0]
        closest_distance = math.dist(self.coordinates, closest_sheep.coordinates)

        for sheep in all_sheep[1:]:
            distance = math.dist(self.coordinates, sheep.coordinates)
            if distance < closest_distance:
                closest_sheep = sheep
                closest_distance = distance

        self.current_pray_to_chase = closest_sheep
        if self.logger:
            self.logger.log_wolf_chasing(closest_sheep)

    def chase_or_kill(self, all_sheep):
        if not all_sheep:
            self.current_pray_to_chase = None
            return

        if self.current_pray_to_chase is None:
            self.find_closest_sheep(all_sheep)
            return

        target = self.current_pray_to_chase
        distance = math.dist(self.coordinates, target.coordinates)

        if distance <= self.range_of_movement:
            self.coordinates = target.coordinates.copy()
            all_sheep.remove(target)

            if self.logger:
                self.logger.log_sheep_eaten(target)

            self.current_pray_to_chase = None
            return

        dx = target.coordinates[0] - self.coordinates[0]
        dy = target.coordinates[1] - self.coordinates[1]
        length = math.sqrt(dx ** 2 + dy ** 2)

        self.coordinates[0] += (dx / length) * self.range_of_movement
        self.coordinates[1] += (dy / length) * self.range_of_movement


class Sheep(Animal):
    def __init__(self):
        super().__init__( 0.5, (-10.0, 10.0))
        self.generate_starting_position()
