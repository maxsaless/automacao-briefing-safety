import os
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def load_config():
    """Load configuration from environment variables."""
    try:
        config_value = os.getenv("CONFIG_VALUE")
        if not config_value:
            logging.warning("CONFIG_VALUE not set in environment variables.")
        return config_value
    except Exception as e:
        logging.error(f"Error loading configuration: {e}")
        return None

def perform_task():
    """Perform the main task of the application."""
    try:
        logging.info("Task started.")
        # Simulated task logic
        # e.g., result = complex_operation()
        logging.info("Task completed successfully.")
    except Exception as e:
        logging.error(f"An error occurred: {e}")

def main():
    """Main entry point of the application."""
    logging.info("Application started.")
    config = load_config()
    if config is None:
        logging.error("Failed to load configuration. Exiting.")
        return
    perform_task()
    logging.info("Application finished.")

if __name__ == "__main__":
    main()