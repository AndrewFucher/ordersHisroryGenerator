# Logger
LOGGER_FILE_EXTENSION = "txt"
LOGGER_DEFAULT_FORMAT = "[%(asctime)s.%(msecs)03d]:%(name)s:%(levelname)s: %(message)s"
LOGGER_DEFAULT_DATETIME_FORMAT = "%Y-%m-%d %I:%M:%S"

# Config
CONFIG_FILE_PATH = "./config.json"

# LCG
LCG_A = 1664530
LCG_M = 1099511627776
LCG_C = 1013904223
SEED_INCREMENTER = 1

# Dump
DUMP_FILE_PATH = "./dumps/dump.txt"

# Dependencies of field on status field
FILL_WITH_ZERO: int = 0
FILL_WITH_DEFAULT: int = 1
FILL_WITH_CHANGED: int = 2
FILL_FROM_LAST: int = 3

# MySQL
MYSQL_STRING_FORMAT = "INSERT INTO `{}` VALUES ('{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}');\n"