from datetime import timedelta, datetime
import logging
import logging.handlers
import os
import shutil
import tempfile

from settings import (
    DAYS_BEFORE_DELETE,
    DIR_PATTERN,
    LOGFILE_PATH,
    LOG_MAX_SIZE,
    NUMBER_OF_LOG_FILES
)

if not os.path.exists(LOGFILE_PATH):
    os.makedirs(os.path.dirname(LOGFILE_PATH), exist_ok=True)

logging.basicConfig(
    encoding='utf-8',
    format=(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    ),
    level=logging.INFO,
    handlers=[
        logging.handlers.RotatingFileHandler(
            filename=LOGFILE_PATH,
            maxBytes=LOG_MAX_SIZE,
            backupCount=NUMBER_OF_LOG_FILES,
            encoding='utf-8',
        )
    ],
)


def get_directories_list(parent_dir, days):
    all_bacups = [
        name
        for name in os.listdir(parent_dir)
        if os.path.isdir(os.path.join(parent_dir, name))
        and DIR_PATTERN in name
    ]
    backups_to_delete: list = []
    for backup in all_bacups:
        date_string = backup.split('.')[1]
        year = int('20'+date_string[0:2])
        month = int(date_string[2:4])
        day = int(date_string[4:6])
        creation_date = datetime(year, month, day)
        if creation_date < datetime.now()-days:
            backups_to_delete.append(os.path.join(
                parent_dir,
                backup,
            )
            )
    return backups_to_delete


def main():
    temp_dir = tempfile.gettempdir()
    days = timedelta(days=DAYS_BEFORE_DELETE)
    backups_to_delete = get_directories_list(temp_dir, days)
    for full_path in backups_to_delete:
        try:
            if os.path.isdir(full_path):
                shutil.rmtree(full_path)
            else:
                os.remove(full_path)
            logging.info(f"Успешно удалено: {full_path}")
        except OSError as e:
            logging.error(f"Ошибка при удалении {full_path}: {e}")


if __name__ == '__main__':
    main()
