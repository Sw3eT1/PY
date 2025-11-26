import argparse
import configparser
import logging
import sys

from animals_classes import Sheep, Wolf
from loggers_classes import SimulationLogger, JasonLogger, CSVLogger

DEFAULT_ROUNDS = 50
DEFAULT_SHEEP_COUNT = 15
DEFAULT_SHEEP_MOVE = 0.5
DEFAULT_WOLF_MOVE = 1.0
DEFAULT_INIT_POS_LIMIT = 10.0


def validate_positive_int(value, name):
    try:
        ivalue = int(value)
        if ivalue <= 0:
            raise ValueError
        return ivalue
    except ValueError:
        raise argparse.ArgumentTypeError(f"{name} must be a positive integer.")


def validate_positive_float(value, name):
    try:
        fvalue = float(value)
        if fvalue <= 0:
            raise ValueError
        return fvalue
    except ValueError:
        raise ValueError(f"{name} must be a positive float.")


def setup_logging(level_str):
    if not level_str:
        return

    numeric_level = getattr(logging, level_str.upper(), None)
    if not isinstance(numeric_level, int):
        raise ValueError(f'Invalid log level: {level_str}')

    # Tworzenie folderu log, jeśli nie istnieje
    if not os.path.exists('log'):
        os.makedirs('log')

    # Zapis do log/chase.log
    logging.basicConfig(
        filename='log/chase.log',
        filemode='w',
        level=numeric_level,
        format='%(levelname)s: %(message)s'
    )


def main():
    parser = argparse.ArgumentParser(description="Wolf and Sheep Simulation")

    parser.add_argument('-c', '--config', help="Path to configuration file", metavar="FILE")
    parser.add_argument('-l', '--log', help="Log level (DEBUG, INFO, WARNING, ERROR, CRITICAL)", metavar="LEVEL")
    parser.add_argument('-r', '--rounds', help="Maximum number of rounds", type=int, metavar="NUM")
    parser.add_argument('-s', '--sheep', help="Number of sheep", type=int, metavar="NUM")
    parser.add_argument('-w', '--wait', help="Wait for key press after each round", action='store_true')

    args = parser.parse_args()

    rounds = DEFAULT_ROUNDS
    sheep_count = DEFAULT_SHEEP_COUNT

    if args.rounds is not None:
        rounds = validate_positive_int(args.rounds, "Number of rounds")

    if args.sheep is not None:
        sheep_count = validate_positive_int(args.sheep, "Number of sheep")

    if args.log:
        setup_logging(args.log)


    if rounds > 1000:
        logging.warning(f"High number of rounds selected ({rounds}). Simulation might take a long time.")

    sheep_move_dist = DEFAULT_SHEEP_MOVE
    wolf_move_dist = DEFAULT_WOLF_MOVE
    init_pos_limit = DEFAULT_INIT_POS_LIMIT

    if args.config:
        config = configparser.ConfigParser()
        try:
            read_files = config.read(args.config)
            if not read_files:
                raise FileNotFoundError(f"Config file not found: {args.config}")

            if 'Sheep' in config:
                if 'InitPosLimit' in config['Sheep']:
                    init_pos_limit = validate_positive_float(config['Sheep']['InitPosLimit'], "Sheep InitPosLimit")
                if 'MoveDist' in config['Sheep']:
                    sheep_move_dist = validate_positive_float(config['Sheep']['MoveDist'], "Sheep MoveDist")

            if 'Wolf' in config:
                if 'MoveDist' in config['Wolf']:
                    wolf_move_dist = validate_positive_float(config['Wolf']['MoveDist'], "Wolf MoveDist")

            logging.debug(
                f"Loaded config. Sheep limit: {init_pos_limit}, Sheep move: {sheep_move_dist}, Wolf move: {wolf_move_dist}")

        except Exception as e:
            print(f"Error loading config file: {e}")
            logging.error(f"Error loading config file: {e}")
            sys.exit(1)

    all_alive_sheep = []
    for i in range(sheep_count):
        s = Sheep(init_pos_limit, sheep_move_dist, i + 1)
        all_alive_sheep.append(s)

    logging.info("Initial positions of all sheep were determined")

    main_wolf = Wolf(wolf_move_dist)

    console_logger = SimulationLogger()
    jason_logger = JasonLogger()
    csv_logger = CSVLogger()

    main_wolf.attach_logger(console_logger)

    current_round = 0

    while current_round < rounds and all_alive_sheep:
        console_logger.start_new_round()
        current_round += 1

        logging.info(f"Start new round: {current_round}")

        for sheep in list(all_alive_sheep):
            sheep.move()

        logging.info("All alive sheep moved")

        main_wolf.chase_or_kill(all_alive_sheep)

        console_logger.print_round_summary(main_wolf, all_alive_sheep)
        jason_logger.log_round(current_round, main_wolf, all_alive_sheep.copy())
        csv_logger.log_round(current_round, all_alive_sheep.copy())

        logging.info(f"Round {current_round} ended. Alive sheep: {len(all_alive_sheep)}")

        if args.wait:
            input("Press Enter to continue...")

    if not all_alive_sheep:
        msg = "Wolf ate all sheep and won!"
        print(f"\n{msg}")
        logging.info(f"Simulation terminated: {msg}")
    else:
        msg = "Max rounds reached — simulation ended."
        print(f"\n{msg}")
        logging.info(f"Simulation terminated: {msg}")

    jason_logger.save()
    csv_logger.save()


if __name__ == "__main__":
    main()