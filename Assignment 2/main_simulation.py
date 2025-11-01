from animals_classes import Sheep, Wolf
from loggers_classes import SimulationLogger, JasonLogger, CSVLogger

MAX_NUMBER_OF_ROUNDS = 50
NUMBER_OF_SHEEP_TO_GENERATE = 15

all_alive_sheep = [Sheep() for _ in range(NUMBER_OF_SHEEP_TO_GENERATE)]
main_wolf = Wolf()

logger = SimulationLogger()
jason_logger = JasonLogger()
csv_logger = CSVLogger()

main_wolf.attach_logger(logger)

while MAX_NUMBER_OF_ROUNDS > 0 and all_alive_sheep:
    logger.start_new_round()

    if main_wolf.current_pray_to_chase is None and all_alive_sheep:
        main_wolf.find_closest_sheep(all_alive_sheep)

    for sheep in list(all_alive_sheep):
        sheep.move_using_direction(sheep.generate_direction())

    main_wolf.chase_or_kill(all_alive_sheep)

    logger.print_round_summary(main_wolf, all_alive_sheep)
    jason_logger.log_round(logger.round_number, main_wolf, all_alive_sheep.copy())
    csv_logger.log_round(logger.round_number, all_alive_sheep.copy())

    MAX_NUMBER_OF_ROUNDS -= 1

if not all_alive_sheep:
    print("\nWolf ate all sheep and won!")
else:
    print("\nMax rounds reached — simulation ended.")

jason_logger.save()
csv_logger.save()