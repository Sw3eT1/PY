import json
import os
import csv
import logging

class SimulationLogger:
    def __init__(self):
        self.round_number = 0
        self.last_eaten_sheep_seq = None
        self.currently_chased_sheep_id = None

    def start_new_round(self):
        self.round_number += 1
        self.last_eaten_sheep_seq = None
        self.currently_chased_sheep_id = None

    def log_wolf_chasing(self, sheep):
        self.currently_chased_sheep_id = sheep.id if sheep else None

    def log_sheep_eaten(self, sheep_seq_num):
        self.last_eaten_sheep_seq = sheep_seq_num

    def print_round_summary(self, wolf, sheep_list):
        print(f"Round: {self.round_number}")
        print(f"Wolf position: ({wolf.coordinates[0]:.3f}, {wolf.coordinates[1]:.3f})")
        print(f"Alive sheep: {len(sheep_list)}")

        if self.last_eaten_sheep_seq is not None:
            print(f"Wolf ate sheep sequence number: {self.last_eaten_sheep_seq}")
        elif self.currently_chased_sheep_id is not None:
            chased_seq = "Unknown"
            for idx, s in enumerate(sheep_list):
                if s.id == self.currently_chased_sheep_id:
                    chased_seq = idx + 1
                    break
            print(f"Wolf is chasing sheep sequence number: {chased_seq}")
        print("")

class JasonLogger:
    def __init__(self, filename="pos.json"):
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
        logging.debug("Information saved to pos.json file")

class CSVLogger:
    def __init__(self, filename="alive.csv"):
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
        logging.debug("Information saved to alive.csv file")