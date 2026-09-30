import re
from datetime import datetime


def parse_lines(lines):
    events = []

    for line in lines:

        # Identifica se o evento foi uma falha ou um login bem-sucedido.
        if "Failed password" in line:
            status = "failed"

            user_match = re.search(
                r"Failed password for (\w+)",
                line
            )

        elif "Accepted password" in line:
            status = "success"

            user_match = re.search(
                r"Accepted password for (\w+)",
                line
            )

        else:
            # Se não for um evento que nos interessa, ignoramos.
            continue

        ip_match = re.search(
            r"from (\d+\.\d+\.\d+\.\d+)",
            line
        )

        # Formato:
        # 2026-09-23 18:42:13
        full_date_match = re.search(
            r"^(\d{4})-(\d{2})-(\d{2})\s+(\d+:\d+:\d+)",
            line
        )

        # Formato tradicional:
        # Sep 23 18:42:13
        traditional_date_match = re.search(
            r"^(\w+)\s+(\d+)\s+(\d+:\d+:\d+)",
            line
        )

        if not ip_match or not user_match:
            continue

        ip = ip_match.group(1)
        user = user_match.group(1)

        if full_date_match:
            year = full_date_match.group(1)
            month = full_date_match.group(2)
            day = full_date_match.group(3)
            time_text = full_date_match.group(4)

            date_text = f"{year}-{month}-{day} {time_text}"

            timestamp = datetime.strptime(
                date_text,
                "%Y-%m-%d %H:%M:%S"
            )

        elif traditional_date_match:
            month = traditional_date_match.group(1)
            day = traditional_date_match.group(2)
            time_text = traditional_date_match.group(3)

            # O formato tradicional não possui ano,
            # então usamos o ano atual como fallback.
            current_year = datetime.now().year

            date_text = (
                f"{current_year} "
                f"{month} {day} {time_text}"
            )

            timestamp = datetime.strptime(
                date_text,
                "%Y %b %d %H:%M:%S"
            )

        else:
            continue

        event = {
            "ip": ip,
            "user": user,
            "timestamp": timestamp,
            "status": status
        }

        events.append(event)

    return events


def read_failed_attempts(log_file):
    # Esta função continua sendo usada pelo main.py.
    # Ela abre o arquivo e envia suas linhas para parse_lines().
    with open(log_file, "r") as file:
        return parse_lines(file)