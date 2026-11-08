from datetime import datetime, timedelta

from backend.parser import parse_lines
from backend.detector import detect_brute_force, detect_root_attacks, detect_success_after_failures


def test_parser_users_ipv6_and_bad_date():
    lines = [
        'Sep 23 18:42:13 host sshd: Failed password for invalid user admin from 192.0.2.1 port 22',
        'Sep 23 18:42:14 host sshd: Failed password for john-doe from 2001:db8::1 port 22',
        '2026-99-99 18:42:13 host sshd: Failed password for root from 192.0.2.1 port 22',
    ]
    events = parse_lines(lines)
    assert [event['user'] for event in events] == ['admin', 'john-doe']
    assert events[1]['ip'] == '2001:db8::1'


def test_year_rollover():
    events = parse_lines([
        'Dec 31 23:59:50 host sshd: Failed password for root from 192.0.2.1 port 22',
        'Jan  1 00:00:10 host sshd: Failed password for root from 192.0.2.1 port 22',
    ])
    assert (events[1]['timestamp'] - events[0]['timestamp']).total_seconds() == 20
    assert events[1]['timestamp'].year == datetime.now().year


def test_successes_do_not_count_as_failures():
    start = datetime(2026, 1, 1)
    events = [{'ip': '192.0.2.1', 'user': 'root', 'status': 'success',
               'timestamp': start + timedelta(seconds=i)} for i in range(5)]
    assert detect_brute_force(events) == []
    assert detect_root_attacks(events) == []


def test_failures_must_be_recent_and_for_same_user():
    start = datetime(2026, 1, 1)
    failures = [{'ip': '192.0.2.1', 'user': 'alice', 'status': 'failed',
                 'timestamp': start + timedelta(seconds=i)} for i in range(3)]
    other_user = {'ip': '192.0.2.1', 'user': 'bob', 'status': 'success', 'timestamp': start + timedelta(seconds=4)}
    late = {'ip': '192.0.2.1', 'user': 'alice', 'status': 'success', 'timestamp': start + timedelta(seconds=120)}
    assert detect_success_after_failures(failures + [other_user, late]) == []
    assert detect_root_attacks([dict(event, user='root', timestamp=start + timedelta(minutes=i)) for i, event in enumerate(failures)]) == []
    original = list(reversed(failures))
    detect_success_after_failures(original)
    assert original == list(reversed(failures))
