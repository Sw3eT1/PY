import math
import random
import uuid
import logging


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
        direction = random.choice(POSSIBLE_DIRECTIONS)
        return direction

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
    def __init__(self, move_dist):
        super().__init__(move_dist, (0.0, 0.0))
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

        logging.debug(f"Wolf determined closest sheep ID: {closest_sheep.id} distance: {closest_distance}")

        self.current_pray_to_chase = closest_sheep
        if self.logger:
            self.logger.log_wolf_chasing(closest_sheep)

        logging.info(f"Wolf is chasing sheep sequence number: {all_sheep.index(closest_sheep) + 1}")

    def chase_or_kill(self, all_sheep):
        if not all_sheep:
            self.current_pray_to_chase = None
            return

        if self.current_pray_to_chase is None or self.current_pray_to_chase not in all_sheep:
            self.find_closest_sheep(all_sheep)
            if self.current_pray_to_chase is None: return

        target = self.current_pray_to_chase
        distance = math.dist(self.coordinates, target.coordinates)

        if distance <= self.range_of_movement:
            self.coordinates = target.coordinates.copy()

            logging.debug(f"Wolf moved to eaten sheep position: {self.coordinates}")
            logging.info("Wolf moved")

            try:
                seq_num = all_sheep.index(target) + 1
            except ValueError:
                seq_num = "?"

            all_sheep.remove(target)
            logging.info(f"Sheep was eaten. Sequence number: {seq_num}")

            if self.logger:
                self.logger.log_sheep_eaten(seq_num)

            self.current_pray_to_chase = None
            return

        dx = target.coordinates[0] - self.coordinates[0]
        dy = target.coordinates[1] - self.coordinates[1]
        length = math.sqrt(dx ** 2 + dy ** 2)

        self.coordinates[0] += (dx / length) * self.range_of_movement
        self.coordinates[1] += (dy / length) * self.range_of_movement

        logging.debug(f"Wolf moved to: {self.coordinates}")
        logging.info("Wolf moved")


class Sheep(Animal):
    def __init__(self, init_pos_limit, move_dist, seq_number):
        super().__init__(move_dist, (-init_pos_limit, init_pos_limit))
        self.generate_starting_position()
        self.seq_number = seq_number

        logging.debug(f"Sheep {self.seq_number} init pos determined: {self.coordinates}")

    def move(self):
        direction = self.generate_direction()
        logging.debug(f"Sheep {self.seq_number} chose direction: {direction}")

        self.move_using_direction(direction)

        logging.debug(f"Sheep {self.seq_number} moved to: {self.coordinates}")