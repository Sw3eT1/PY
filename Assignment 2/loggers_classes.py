import json
import os
import csv


class SimulationLogger:
    def __init__(self):
        self.round_number = 0
        self.last_eaten_sheep = None
        self.currently_chased_sheep = None

    def start_new_round(self):
        self.round_number += 1
        self.last_eaten_sheep = None

    def log_wolf_chasing(self, sheep):
        self.currently_chased_sheep = sheep.id if sheep else None

    def log_sheep_eaten(self, sheep):
        self.last_eaten_sheep = sheep.id if sheep else None

    def print_round_summary(self, wolf, sheep_list):
        print("\n===================================")
        print(f"Round: {self.round_number}")
        print(f"Wolf position: ({wolf.coordinates[0]:.3f}, {wolf.coordinates[1]:.3f})")
        print(f"Alive sheep: {len(sheep_list)}")

        if self.last_eaten_sheep is not None:
            print(f"Wolf ate sheep ID: {self.last_eaten_sheep}")
        elif self.currently_chased_sheep is not None:
            print(f"Wolf is chasing sheep ID: {self.currently_chased_sheep}")

class JasonLogger:
    def __init__(self, filename="logs/pos.json"):
        self.filename = filename
        self.data = []

        if os.path.exists(self.filename):
            os.remove(self.filename)

    def log_round(self, round_no, wolf, sheep_list):
        round_entry = {
            "round_no": round_no,
            "wolf_pos": [round(wolf.coordinates[0], 6), round(wolf.coordinates[1], 6)],
            "sheep_pos": []
        }

        for sheep in sheep_list:
            if sheep is None:
                round_entry["sheep_pos"].append(None)
            else:
                round_entry["sheep_pos"].append([
                    round(sheep.coordinates[0], 6),
                    round(sheep.coordinates[1], 6)
                ])

        self.data.append(round_entry)

    def save(self):
        with open(self.filename, "w") as file:
            json.dump(self.data, file, indent=4)

class CSVLogger:
    def __init__(self, filename="logs/alive.csv"):
        self.filename = filename
        self.data = []

        if os.path.exists(self.filename):
            os.remove(self.filename)

    def log_round(self, round_no, sheep_list):
        alive_count = sum(1 for sheep in sheep_list if sheep is not None)
        self.data.append([round_no, alive_count])

    def save(self):
        with open(self.filename, "w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(["round_no", "alive_sheep"])
            writer.writerows(self.data)

