from datetime import datetime, timedelta

from backend.detector import (
    detect_brute_force,
    detect_root_attacks,
    detect_success_after_failures
)


def test_detect_brute_force():
    start_time = datetime(2026, 9, 29, 18, 0, 0)

    events = []

    # Criamos 5 tentativas do mesmo IP,
    # cada uma separada por 5 segundos.
    for i in range(5):
        event = {
            "ip": "192.0.2.10",
            "user": "root",
            "status": "failed",
            "timestamp": start_time + timedelta(seconds=i * 5)
        }

        events.append(event)

    alerts = detect_brute_force(events)

    # Esperamos exatamente 1 alerta.
    assert len(alerts) == 1

    # Conferimos se o IP detectado é o correto.
    assert alerts[0]["ip"] == "192.0.2.10"

    # Conferimos se foram detectadas 5 tentativas.
    assert alerts[0]["attempts"] == 5

    # As 5 tentativas aconteceram entre 18:00:00 e 18:00:20.
    assert alerts[0]["time_window"] == 20


def test_no_brute_force():
    start_time = datetime(2026, 9, 29, 18, 0, 0)

    events = []

    # Aqui as tentativas ficam muito espaçadas.
    # Portanto, não devem gerar brute force.
    for i in range(5):
        event = {
            "ip": "192.0.2.20",
            "user": "developer",
            "status": "failed",
            "timestamp": start_time + timedelta(minutes=i * 10)
        }

        events.append(event)

    alerts = detect_brute_force(events)

    assert len(alerts) == 0


def test_detect_root_attack():
    events = [
        {
            "ip": "192.0.2.30",
            "user": "root",
            "status": "failed",
            "timestamp": datetime(2026, 9, 29, 18, 0, 0)
        },
        {
            "ip": "192.0.2.30",
            "user": "root",
            "status": "failed",
            "timestamp": datetime(2026, 9, 29, 18, 0, 5)
        },
        {
            "ip": "192.0.2.30",
            "user": "root",
            "status": "failed",
            "timestamp": datetime(2026, 9, 29, 18, 0, 10)
        }
    ]

    alerts = detect_root_attacks(events)

    assert len(alerts) == 1
    assert alerts[0]["ip"] == "192.0.2.30"
    assert alerts[0]["user"] == "root"
    assert alerts[0]["attempts"] == 3


def test_success_after_failures():
    events = [
        {
            "ip": "203.0.113.10",
            "user": "developer",
            "status": "failed",
            "timestamp": datetime(2026, 9, 29, 19, 0, 0)
        },
        {
            "ip": "203.0.113.10",
            "user": "developer",
            "status": "failed",
            "timestamp": datetime(2026, 9, 29, 19, 0, 5)
        },
        {
            "ip": "203.0.113.10",
            "user": "developer",
            "status": "failed",
            "timestamp": datetime(2026, 9, 29, 19, 0, 10)
        },
        {
            "ip": "203.0.113.10",
            "user": "developer",
            "status": "success",
            "timestamp": datetime(2026, 9, 29, 19, 0, 20)
        }
    ]

    alerts = detect_success_after_failures(events)

    assert len(alerts) == 1
    assert alerts[0]["ip"] == "203.0.113.10"
    assert alerts[0]["user"] == "developer"
    assert alerts[0]["failed_attempts"] == 3