from __future__ import annotations

import asyncio
from pathlib import Path
from typing import Any, Dict, List

import pandas as pd
from loguru import logger

from config.settings import Settings
from core.job_manager import JobManager
from core.pipeline import Pipeline
from core.scheduler import Scheduler
from core.scraper_engine import ScraperEngine
from storage.csv_writer import write_csv
from storage.json_writer import write_json
from storage.sheet_writer import append_to_sheet
from utils.query_builder import QueryInput, build_queries


class Orchestrator:
    def __init__(self, project_root: Path, settings: Settings, logger_instance) -> None:
        self.project_root = project_root
        self.settings = settings
        self.logger = logger_instance
        self.engine = ScraperEngine(settings)
        self.pipeline = Pipeline()
        self.job_manager = JobManager()
        self.scheduler = Scheduler()

    def _load_input_queries(self) -> List[QueryInput]:
        input_path = self.project_root / "input" / "queries.csv"
        if not input_path.exists():
            logger.warning(f"No input file found at {input_path}, nothing to do.")
            return []
        df = pd.read_csv(input_path)
        queries: List[QueryInput] = []
        for _, row in df.iterrows():
            def _str(v: Any) -> str:
                if pd.isna(v) or v is None:
                    return ""
                s = str(v).strip()
                return "" if s.lower() == "nan" else s

            keyword = _str(row.get("keyword", ""))
            loc = _str(row.get("location", ""))
            ind = _str(row.get("industry", ""))
            queries.append(
                QueryInput(
                    keyword=keyword,
                    location=loc or None,
                    industry=ind or None,
                )
            )
        return queries

    def run(self) -> None:
        raw_inputs = self._load_input_queries()
        if not raw_inputs:
            return

        search_queries = build_queries(raw_inputs)
        jobs = self.job_manager.build_jobs(search_queries)
        scheduled = self.scheduler.schedule(jobs)

        self.logger.info(f"Running scraper engine for {len(scheduled)} jobs / queries.")
        queries = [j.query for j in scheduled]

        scraper_result = asyncio.run(self.engine.run_async(queries))
        self.logger.info(f"Collected {len(scraper_result.records)} raw records.")

        final_records = self.pipeline.run(scraper_result.records)
        self.logger.info(f"Pipeline produced {len(final_records)} final records.")

        # Save locally.
        json_path = self.project_root / "output" / "results.json"
        csv_path = self.project_root / "output" / "results.csv"
        write_json(json_path, final_records)
        write_csv(csv_path, final_records)

        # Push to Google Sheets.
        creds_path = self.project_root / "credentials" / "google_credentials.json"
        append_to_sheet(
            credentials_path=creds_path,
            sheet_name=self.settings.google_sheet_name,
            worksheet_name=self.settings.google_worksheet_name,
            records=final_records,
        )

