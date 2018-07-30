import argparse
import logging

from pylogging import HandlerType, setup_logger

logger = logging.getLogger(__name__)

if __name__ == "__main__":
    ############################################################################
    # Argparse
    ############################################################################
    parser = argparse.ArgumentParser()
    parser.add_argument('--config_filename', action='store', dest='config_filename',
                        required=True, help='Config filename.')
    parser.add_argument('--set_param', action='store_true', dest='set_param', default=False,
                        required=True, help='Set parameter called param.')
    command_args = parser.parse_args()

    ############################################################################
    # Config
    ############################################################################
    config = read_config(command_args.config_filename)

    ############################################################################
    # Logging
    ############################################################################
    log_dir = config['log_dir']
    setup_logger(log_directory=log_dir,
                 file_handler_type=HandlerType.ROTATING_FILE_HANDLER,
                 max_file_size_bytes=1000000,
                 allow_file_logging=True,
                 allow_console_logging=True,
                 console_log_level=logging.DEBUG)
