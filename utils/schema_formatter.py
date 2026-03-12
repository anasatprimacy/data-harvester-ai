from __future__ import annotations

from typing import Any, Dict, Iterable, List


OUTPUT_FIELDS = [
    "SL No.",
    "Company Name",
    "Website",
    "Owner/ IT Head/ CEO/Finance Head Name",
    "Phone Number",
    "EMail Address",
    "Address",
    "Industry_Type",
    "Employee _No",
    "Branch/ Warehouse _No",
    "Annual_Turnover",
    "Current_Use_ERP Software_Name",
    "Additional_Information",
]


def to_output_schema(records: Iterable[Dict[str, Any]]) -> List[Dict[str, Any]]:
    result: List[Dict[str, Any]] = []
    for idx, rec in enumerate(records, start=1):
        mapped: Dict[str, Any] = {
            "SL No.": idx,
            "Company Name": rec.get("company_name") or rec.get("name") or "",
            "Website": rec.get("website") or "",
            "Owner/ IT Head/ CEO/Finance Head Name": rec.get("decision_maker") or "",
            "Phone Number": rec.get("phone") or "",
            "EMail Address": rec.get("email") or "",
            "Address": rec.get("address") or "",
            "Industry_Type": rec.get("industry_type") or rec.get("industry") or "",
            "Employee _No": rec.get("employee_no") or "",
            "Branch/ Warehouse _No": rec.get("branch_no") or "",
            "Annual_Turnover": rec.get("annual_turnover") or "",
            "Current_Use_ERP Software_Name": rec.get("current_erp") or "",
            "Additional_Information": rec.get("additional_info") or rec.get("description") or "",
        }
        result.append(mapped)
    return result

