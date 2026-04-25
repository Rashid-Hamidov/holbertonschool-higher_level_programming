#!/usr/bin/python3
"""
Simple templating program.
"""

import logging
import os


logging.basicConfig(level=logging.ERROR, format="%(message)s")


def generate_invitations(template, attendees):
    """
    Generate personalized invitation files from a template and a list of
    attendee dictionaries.

    Args:
        template (str): Template text with placeholders.
        attendees (list): List of dictionaries with attendee data.

    Returns:
        None
    """
    if not isinstance(template, str):
        logging.error(f"Invalid input type for template: {type(template).__name__}")
        return

    if not isinstance(attendees, list) or not all(isinstance(item, dict) for item in attendees):
        logging.error(f"Invalid input type for attendees: {type(attendees).__name__}")
        return

    if template.strip() == "":
        logging.error("Template is empty, no output files generated")
        return

    if len(attendees) == 0:
        logging.error("No data provided, no output files generated")
        return

    placeholders = ["name", "event_title", "event_date", "event_location"]

    for index, attendee in enumerate(attendees, start=1):
        processed_template = template

        for key in placeholders:
            value = attendee.get(key, "N/A")
            if value is None or value == "":
                value = "N/A"
            processed_template = processed_template.replace("{" + key + "}", str(value))

        output_filename = f"output_{index}.txt"

        try:
            with open(output_filename, "w", encoding="utf-8") as file:
                file.write(processed_template)
        except Exception as e:
            logging.error(f"Error writing file {output_filename}: {e}")
            return
