from pathlib import Path

from dotenv import load_dotenv

from config.settings import load_settings
from core.orchestrator import Orchestrator
from utils.logger import setup_logging


def main() -> None:
    project_root = Path(__file__).parent
    load_dotenv(project_root / ".env")

    logger = setup_logging(project_root / "output" / "logs")
    logger.info("DataHarvester starting up")

    settings = load_settings(project_root)
    orchestrator = Orchestrator(project_root=project_root, settings=settings, logger_instance=logger)

    orchestrator.run()


if __name__ == "__main__":
    main()

