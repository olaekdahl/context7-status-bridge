from __future__ import annotations

import argparse
import json
from dataclasses import asdict, dataclass

from status_bridge.config import STATUSPAGE_FIXTURE_PATH
from status_bridge.db import get_connection, initialize_db
from status_bridge.feeds import load_statuspage_fixture, statuspage_to_incidents
from status_bridge.repository import IncidentRepository
from status_bridge.service import summarize_incidents


@dataclass
class SummaryOutput:
    total: int
    open_count: int
    major_open: int
    sources: list[str]


def import_fixture() -> int:
    connection = get_connection()
    initialize_db(connection)
    payload = load_statuspage_fixture(str(STATUSPAGE_FIXTURE_PATH))
    incidents = statuspage_to_incidents(payload)
    IncidentRepository(connection).replace_all(incidents)
    return len(incidents)


def print_summary() -> None:
    connection = get_connection()
    initialize_db(connection)
    summary = summarize_incidents(IncidentRepository(connection).list_incidents())
    print(json.dumps(asdict(SummaryOutput(**summary.model_dump())), indent=2))


def main() -> None:
    parser = argparse.ArgumentParser(prog="status-bridge")
    subparsers = parser.add_subparsers(dest="command", required=True)
    subparsers.add_parser("import-fixture")
    subparsers.add_parser("summary")
    args = parser.parse_args()

    if args.command == "import-fixture":
        imported = import_fixture()
        print(f"Imported {imported} incidents from the local fixture.")
    elif args.command == "summary":
        print_summary()


if __name__ == "__main__":
    main()
