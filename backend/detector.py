MAX_ATTEMPTS = 5
TIME_WINDOW = 60


def detect_brute_force(events):
    alerts = []

    attempts_by_ip = {}

    for event in events:
        if event["status"] != "failed":
            continue
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
    root_by_ip = {}
    for event in events:
        if event["status"] == "failed" and event["user"] == "root":
            root_by_ip.setdefault(event["ip"], []).append(event["timestamp"])

    for ip, attempts in root_by_ip.items():
        attempts.sort()
        start = 0
        best_count = 0
        for end in range(len(attempts)):
            while (attempts[end] - attempts[start]).total_seconds() > TIME_WINDOW:
                start += 1
            best_count = max(best_count, end - start + 1)
        if best_count >= ROOT_ATTEMPT_THRESHOLD:
            alerts.append({"type": "root_attack", "severity": "high", "ip": ip,
                           "attempts": best_count, "user": "root"})
    return alerts


FAILED_BEFORE_SUCCESS_THRESHOLD = 3


def detect_success_after_failures(events):
    alerts = []
    failed_attempts = {}

    # sorted cria uma nova lista e preserva a ordem recebida pelo chamador.
    for event in sorted(events, key=lambda event: event["timestamp"]):
        key = (event["ip"], event["user"])
        timestamp = event["timestamp"]
        previous = failed_attempts.get(key, [])
        previous = [time for time in previous
                    if (timestamp - time).total_seconds() <= TIME_WINDOW]

        if event["status"] == "failed":
            previous.append(timestamp)
            failed_attempts[key] = previous
        elif event["status"] == "success":
            if len(previous) >= FAILED_BEFORE_SUCCESS_THRESHOLD:
                alerts.append({
                    "type": "success_after_failures", "severity": "critical",
                    "ip": event["ip"], "failed_attempts": len(previous),
                    "user": event["user"], "timestamp": timestamp
                })
            failed_attempts[key] = []
    return alerts
