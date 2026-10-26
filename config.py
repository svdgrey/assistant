import json
from pathlib import Path
from platformdirs import user_config_path, user_data_path

# Configuration module for the PersonalAssistant application

APP_NAME = "PersonalAssistant"

# user application configuration directory in the operating system
CONFIG_DIR = user_config_path(APP_NAME, roaming=True)

# file path for the configuration file
CONFIG_FILE = CONFIG_DIR / "config.json"

# default directory for storing application data in the operating system
DEFAULT_DATA_DIR = user_data_path(APP_NAME, roaming=True)


# Get the directory where application data will be stored
def get_data_directory():
    if CONFIG_FILE.exists():
        try:
            with open(CONFIG_FILE, "r", encoding="utf-8") as file:
                config = json.load(file)

            data_directory = Path(config["data_directory"]).expanduser()

            if not data_directory.is_dir():
                raise ValueError("Data directory does not exist.")

            return data_directory

        except (json.JSONDecodeError, KeyError, TypeError, ValueError):
            print("Invalid configuration. Using the default data directory.")

            # Keep the original configuration for possible recovery
            backup_config = CONFIG_DIR / "config.json.corrupted"
            CONFIG_FILE.replace(backup_config)

            data_directory = DEFAULT_DATA_DIR
            data_directory.mkdir(parents=True, exist_ok=True)

            with open(CONFIG_FILE, "w", encoding="utf-8") as file:
                json.dump(
                    {"data_directory": str(data_directory)},
                    file,
                    indent=4
                )

            return data_directory

    print(f"Default data directory: {DEFAULT_DATA_DIR}")
    user_path = input("Enter data directory (Enter for default): ").strip()

    data_directory = (
        Path(user_path).expanduser().resolve()
        if user_path else DEFAULT_DATA_DIR
    )

    data_directory.mkdir(parents=True, exist_ok=True)
    CONFIG_DIR.mkdir(parents=True, exist_ok=True)

    with open(CONFIG_FILE, "w", encoding="utf-8") as file:
        json.dump({"data_directory": str(data_directory)}, file, indent=4)

    return data_directory