MAX_ATTEMPTS = 5
TIME_WINDOW = 60


def detect_brute_force(events):
    alerts = []

    attempts_by_ip = {}

    for event in events:
        ip = event["ip"]
        timestamp = event["timestamp"]

        if ip not in attempts_by_ip:
            attempts_by_ip[ip] = []

        attempts_by_ip[ip].append(timestamp)

    for ip, attempts in attempts_by_ip.items():

        attempts.sort()

        start = 0

        best_count = 0
        best_start = None
        best_end = None

        for end in range(len(attempts)):

            # Enquanto a diferença entre a tentativa atual
            # e a primeira da janela for maior que 60 segundos,
            # movemos o início da janela.
            while (
                attempts[end] - attempts[start]
            ).total_seconds() > TIME_WINDOW:

                start += 1

            # Quantas tentativas existem dentro da janela atual
            current_count = end - start + 1

            if current_count > best_count:
                best_count = current_count
                best_start = start
                best_end = end

        if best_count >= MAX_ATTEMPTS:

            first_attempt = attempts[best_start]
            last_attempt = attempts[best_end]

            time_difference = (
                last_attempt - first_attempt
            ).total_seconds()

            alert = {
                "type": "brute_force",
                "severity": "high",
                "ip": ip,
                "attempts": best_count,
                "time_window": time_difference
            }

            alerts.append(alert)

    return alerts

ROOT_ATTEMPT_THRESHOLD = 3


def detect_root_attacks(events):
    alerts = []

    root_attempts_by_ip = {}

    for event in events:
        ip = event["ip"]
        user = event["user"]

        if user != "root":
            continue

        if ip not in root_attempts_by_ip:
            root_attempts_by_ip[ip] = 0

        root_attempts_by_ip[ip] += 1

    for ip, attempts in root_attempts_by_ip.items():

        if attempts >= ROOT_ATTEMPT_THRESHOLD:

            alert = {
                "type": "root_attack",
                "severity": "high",
                "ip": ip,
                "attempts": attempts,
                "user": "root"
            }

            alerts.append(alert)

    return alerts

FAILED_BEFORE_SUCCESS_THRESHOLD = 3


def detect_success_after_failures(events):
    alerts = []

    events.sort(key=lambda event: event["timestamp"])

    failed_attempts_by_ip = {}

    for event in events:
        ip = event["ip"]
        status = event["status"]

        if ip not in failed_attempts_by_ip:
            failed_attempts_by_ip[ip] = 0

        if status == "failed":
            failed_attempts_by_ip[ip] += 1

        elif status == "success":

            if failed_attempts_by_ip[ip] >= FAILED_BEFORE_SUCCESS_THRESHOLD:

                alert = {
                    "type": "success_after_failures",
                    "severity": "critical",
                    "ip": ip,
                    "failed_attempts": failed_attempts_by_ip[ip],
                    "user": event["user"],
                    "timestamp": event["timestamp"]
                }

                alerts.append(alert)

            failed_attempts_by_ip[ip] = 0

    return alerts