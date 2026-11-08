import ipaddress
import re
from datetime import datetime


def parse_lines(lines):
    lines = list(lines)
    events = []

    # Logs tradicionais não informam o ano. Usamos o ano atual para o
    # último evento e voltamos um ano em cada passagem de janeiro para dezembro.
    years = {}
    year = datetime.now().year
    next_month = None
    months = {name: number for number, name in enumerate(
        ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"], 1
    )}
    for index in range(len(lines) - 1, -1, -1):
        date = re.match(r"^(\w+)\s+\d+\s+\d+:\d+:\d+", lines[index])
        if date and date.group(1) in months:
            month = months[date.group(1)]
            if month == 12 and next_month == 1:
                year -= 1
            years[index] = year
            next_month = month

    for index, line in enumerate(lines):
        if "Failed password" in line:
            status = "failed"
            user_match = re.search(r"Failed password for (?:invalid user )?(\S+)", line)
        elif "Accepted password" in line:
            status = "success"
            user_match = re.search(r"Accepted password for (\S+)", line)
        else:
            continue

        ip_match = re.search(r"from (\S+)", line)
        if not ip_match or not user_match:
            continue
        try:
            ip = str(ipaddress.ip_address(ip_match.group(1)))
        except ValueError:
            continue

        full_date = re.match(r"^(\d{4}-\d{2}-\d{2})\s+(\d+:\d+:\d+)", line)
        traditional_date = re.match(r"^(\w+)\s+(\d+)\s+(\d+:\d+:\d+)", line)
        try:
            if full_date:
                timestamp = datetime.strptime(
                    f"{full_date.group(1)} {full_date.group(2)}", "%Y-%m-%d %H:%M:%S"
                )
            elif traditional_date and index in years:
                month = months[traditional_date.group(1)]
                timestamp = datetime.strptime(
                    f"{years[index]}-{month:02d}-{traditional_date.group(2)} {traditional_date.group(3)}",
                    "%Y-%m-%d %H:%M:%S"
                )
            else:
                continue
        except ValueError:
            # Uma linha com data inválida não deve interromper todo o arquivo.
            continue

        events.append({
            "ip": ip,
            "user": user_match.group(1),
            "timestamp": timestamp,
            "status": status
        })
    return events


def read_failed_attempts(log_file):
    with open(log_file, "r", encoding="utf-8") as file:
        return parse_lines(file)
