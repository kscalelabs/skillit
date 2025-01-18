"""Script to configure and zero actuators in the KOS system."""

# Standard library imports
import logging
import time
import traceback

# Third-party imports
import colorlogging
import pykos  # type: ignore[import-untyped]

# Local imports
from skillet.setup.maps import ACTUATOR_NAME_TO_ID

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


def main() -> None:
    """Configure and zero actuators, reading their states."""
    colorlogging.configure()
    kos = pykos.KOS(ip="192.168.42.1")

    for actuator_name, actuator_id in ACTUATOR_NAME_TO_ID.items():
        try:
            # Configure actuator
            logger.info("Configuring actuator %s with id %d to zero position", actuator_name, actuator_id)
            result = kos.actuator.configure_actuator(actuator_id=actuator_id, zero_position=True)
            logger.info("Result for actuator %s with id %d: %s", actuator_name, actuator_id, result)

            # Get and log actuator state
            state = kos.actuator.get_actuators_state([actuator_id])
            logger.info("Current state for actuator %s with id %d: %s", actuator_name, actuator_id, state)

            time.sleep(0.1)
        except Exception as e:
            logger.error(
                "Error while configuring/checking actuator %s (ID: %d): %s", actuator_name, actuator_id, str(e)
            )
            logger.error("Traceback:\n%s", traceback.format_exc())


if __name__ == "__main__":
    main()
