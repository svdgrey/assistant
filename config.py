import json
from pathlib import Path
from platformdirs import user_config_path, user_data_path

# Configuration module for the PersonalAssistant application

APP_NAME = "PersonalAssistant"

# user application configuration directory in the operating system
CONFIG_DIR = user_config_path(
    appname=APP_NAME,
    appauthor=False,
    roaming=True
)

# file path for the configuration file
CONFIG_FILE = CONFIG_DIR / "config.json"

# default directory for storing application data in the operating system
DEFAULT_DATA_DIR = user_data_path(
    appname=APP_NAME,
    appauthor=False,
    roaming=True
)


# Validate the user-provided directory path
def validate_data_path(user_path):
    data_directory = Path(user_path).expanduser()

    if not data_directory.is_absolute():
        raise ValueError(
            "Invalid path. Enter an absolute path or use ~/."
        )

    return data_directory.resolve()


# Get the directory where application data will be stored
def get_data_directory():
    if CONFIG_FILE.exists():
        try:
            with open(CONFIG_FILE, "r", encoding="utf-8") as file:
                config = json.load(file)

            data_directory = validate_data_path(config["data_directory"])

        except (json.JSONDecodeError, KeyError, TypeError, ValueError):
            print("Invalid configuration. Using the default data directory.")

            # Keep corrupted configuration for possible recovery
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

        # Do not change the configuration if the directory is missing
        if not data_directory.is_dir():
            raise FileNotFoundError(
                f"Data directory not found: {data_directory}"
            )

        return data_directory

    print(f"Default data directory: {DEFAULT_DATA_DIR}")

    while True:
        user_path = input(
            "Enter data directory (Enter for default): "
        ).strip()

        try:
            if user_path:
                data_directory = validate_data_path(user_path)
            else:
                data_directory = DEFAULT_DATA_DIR

            data_directory.mkdir(parents=True, exist_ok=True)
            break

        except (ValueError, OSError) as error:
            print(f"Invalid data directory: {error}")

    CONFIG_DIR.mkdir(parents=True, exist_ok=True)

    with open(CONFIG_FILE, "w", encoding="utf-8") as file:
        json.dump(
            {"data_directory": str(data_directory)},
            file,
            indent=4
        )

    return data_directory



# Ask the user to choose a data directory
def recover_data_directory():
    while True:
        print("\nChoose an action:")
        print("1. Retry the current directory")
        print("2. Change the data directory")
        print("3. Exit")

        choice = input("Your choice [3]: ").strip()

        if choice in ("", "3"):
            return False

        if choice == "1":
            try:
                    with open(CONFIG_FILE, "r", encoding="utf-8") as file:
                        config = json.load(file)

                    data_directory = validate_data_path(config["data_directory"])

                    if not data_directory.exists():
                        print(f"Directory not found: {data_directory}")
                        data_directory.mkdir(parents=True, exist_ok=True)
                        print("Data directory created successfully.")

                    if not data_directory.is_dir():
                        raise ValueError("The specified path is not a directory.")

                    if not any(data_directory.iterdir()):
                        print("Warning: Data directory is empty.")

                    return True

            except (OSError, ValueError, KeyError, TypeError, json.JSONDecodeError) as error:
                print(f"Failed to access data directory: {error}")            

        elif choice == "2":
            print(f"Default data directory: {DEFAULT_DATA_DIR}")

            while True:
                user_path = input(
                    "Enter new data directory (Enter for default): "
                ).strip()

                try:
                    if user_path:
                        new_directory = validate_data_path(user_path)
                    else:
                        new_directory = DEFAULT_DATA_DIR

                    # Create the directory if it does not exist
                    new_directory.mkdir(parents=True, exist_ok=True)

                    # Save the new data directory
                    config = {"data_directory": str(new_directory)}

                    with open(CONFIG_FILE, "w", encoding="utf-8") as file:
                        json.dump(config, file, indent=4)

                    return True

                except (ValueError, OSError) as error:
                    print(f"Invalid data directory: {error}")

        else:
            print("Invalid choice.")