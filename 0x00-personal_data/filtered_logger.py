#!/usr/bin/env python3
"""A module used to filter sensitive data from a log file"""
import logging
import re
from typing import List
import os
import mysql.connector
PII_FIELDS = ('name', 'email', 'phone', 'ssn', 'password')


def filter_datum(fields: List[str], redaction: str,
                 message: str, separator: str) -> str:
    """Obfuscate fileds inside a message"""
    field = '|'.join(fields)
    return re.sub(fr'({field})=[^{separator}]*', fr'\1={redaction}', message)


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class
        """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """Format the record"""
        record.msg = filter_datum(self.fields, self.REDACTION,
                                  record.getMessage(), self.SEPARATOR)
        return super(RedactingFormatter, self).format(record)


def get_logger() -> logging.Logger:
    """Get a logger"""
    logger = logging.getLogger("user_data")
    logger.setLevel(logging.INFO)
    logger.propagate = False
    handler = logging.StreamHandler()
    handler.setFormatter(RedactingFormatter(list(PII_FIELDS)))
    logger.addHandler(handler)
    return logger


def get_db() -> mysql.connector.connection.MySQLConnection:
    """Get a database connection"""
    user = os.getenv("PERSONAL_DATA_DB_USERNAME", "root")
    pwd = os.getenv("PERSONAL_DATA_DB_PASSWORD", "")
    host = os.getenv("PERSONAL_DATA_DB_HOST", "localhost")
    db = os.getenv("PERSONAL_DATA_DB_NAME", "")
    connection = mysql.connector.connect(
        host=host,
        port=3306,
        user=user,
        password=pwd,
        database=db,
    )
    return connection


def main() -> None:
    """Obtain a database connection and retrieve all rows in the users table"""
    fields = "name,email,phone,ssn,password,ip,last_login,user_agent"
    cols = fields.split(',')
    logger = get_logger()
    db = get_db()
    cursor = db.cursor()
    cursor.execute(f"SELECT {fields} FROM users;")
    for row in cursor:
        msg = []
        for idx, col in enumerate(cols):
            msg.append(f'{col}={row[idx]}')
        new = ';'.join(msg)
        logger.info(new)
    cursor.close()
    db.close()


if __name__ == "__main__":
    main()
