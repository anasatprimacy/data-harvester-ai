from __future__ import annotations

from pathlib import Path
from typing import Iterable, Mapping, Any, List

import gspread
from oauth2client.service_account import ServiceAccountCredentials

from utils.schema_formatter import OUTPUT_FIELDS


def _get_client(credentials_path: Path) -> gspread.Client:
    scopes = [
        "https://www.googleapis.com/auth/spreadsheets",
        "https://www.googleapis.com/auth/drive",
    ]
    creds = ServiceAccountCredentials.from_json_keyfile_name(str(credentials_path), scopes)
    return gspread.authorize(creds)


def append_to_sheet(
    credentials_path: Path,
    sheet_name: str,
    worksheet_name: str,
    records: Iterable[Mapping[str, Any]],
) -> None:
    if not credentials_path.exists():
        # Fail silently if credentials are missing; user can add them later.
        return
    try:
        client = _get_client(credentials_path)
    except Exception:
        # Invalid or placeholder credentials; skip Sheets integration gracefully.
        return
    sh = client.open(sheet_name)
    try:
        ws = sh.worksheet(worksheet_name)
    except gspread.WorksheetNotFound:
        ws = sh.add_worksheet(title=worksheet_name, rows="1000", cols=str(len(OUTPUT_FIELDS)))

    rows: List[Mapping[str, Any]] = list(records)
    if not rows:
        return

    values: List[List[Any]] = []
    for row in rows:
        values.append([row.get(field, "") for field in OUTPUT_FIELDS])

    # Ensure header exists.
    existing = ws.get_all_values()
    if not existing:
        ws.append_row(OUTPUT_FIELDS)

    ws.append_rows(values)

