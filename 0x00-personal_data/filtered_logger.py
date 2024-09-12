#!/usr/bin/env python3
"""A module used to filter sensitive data from a log file"""
import logging
import re
from typing import List


def filter_datum(fields: List[str], redaction: str,
                 message: str, seprarator: str) -> str:
    """Obfuscate fileds inside a message"""
    for field in fields:
        message = re.sub(rf"{field}=.+?{seprarator}",
                         f"{field}={redaction}{seprarator}", message)
    return message
