import json
import shutil
import urllib.request
import zipfile
from datetime import date, datetime, time
from pathlib import Path
from unittest import TestCase

from pyfwf.columns import (
    CharColumn,
    DateColumn,
    DateTimeColumn,
    PositiveDecimalColumn,
    PositiveIntegerColumn,
    RightCharColumn,
    TimeColumn,
)
from pyfwf.descriptors import (
    DetailRowDescriptor,
    FileDescriptor,
    FooterRowDescriptor,
    HeaderRowDescriptor,
)
from pyfwf.readers import Reader

COMPLIANCE_DIR = Path(__file__).parent / "fwf-compliance"


def ensure_compliance_cases():
    """Ensure compliance test cases are available locally."""
    manifest_path = COMPLIANCE_DIR / "manifest.json"
    if manifest_path.exists():
        return

    # Check for local sibling repository (monorepo environment)
    sibling_repo = Path(__file__).resolve().parents[2] / "fwf-compliance-tests"
    if (sibling_repo / "manifest.json").exists():
        COMPLIANCE_DIR.mkdir(parents=True, exist_ok=True)
        if (sibling_repo / "cases").exists():
            shutil.copytree(sibling_repo / "cases", COMPLIANCE_DIR / "cases", dirs_exist_ok=True)
        shutil.copy2(sibling_repo / "manifest.json", COMPLIANCE_DIR / "manifest.json")
        return

    # Fallback: Download from GitHub main branch zip
    COMPLIANCE_DIR.mkdir(parents=True, exist_ok=True)
    zip_url = "https://github.com/fixed-width-file/fwf-compliance-tests/archive/refs/heads/main.zip"
    zip_path = COMPLIANCE_DIR / "compliance.zip"

    try:
        urllib.request.urlretrieve(zip_url, zip_path)
        with zipfile.ZipFile(zip_path, "r") as zip_ref:
            zip_ref.extractall(COMPLIANCE_DIR)
        
        extracted_root = COMPLIANCE_DIR / "fwf-compliance-tests-main"
        if extracted_root.exists():
            if (extracted_root / "cases").exists():
                shutil.copytree(extracted_root / "cases", COMPLIANCE_DIR / "cases", dirs_exist_ok=True)
            shutil.copy2(extracted_root / "manifest.json", COMPLIANCE_DIR / "manifest.json")
            shutil.rmtree(extracted_root)
        
        if zip_path.exists():
            zip_path.unlink()
    except Exception as e:
        raise RuntimeError(f"Could not download compliance test cases: {e}")


def build_column(col_def):
    c_type = col_def["type"]
    name = col_def["name"]
    desc = col_def.get("description", name)

    if c_type == "char":
        return CharColumn(name, col_def["size"], desc)
    elif c_type == "right_char":
        return RightCharColumn(name, col_def["size"], desc)
    elif c_type == "positive_integer":
        return PositiveIntegerColumn(name, col_def["size"], desc)
    elif c_type == "positive_decimal":
        decimals = col_def.get("decimals", 2)
        return PositiveDecimalColumn(name, col_def["size"], decimals=decimals, description=desc)
    elif c_type == "date":
        fmt = col_def.get("format", "%d%m%Y")
        return DateColumn(name, _format=fmt, description=desc)
    elif c_type == "time":
        fmt = col_def.get("format", "%H%M")
        return TimeColumn(name, _format=fmt, description=desc)
    elif c_type == "datetime":
        fmt = col_def.get("format", "%d%m%Y%H%M")
        return DateTimeColumn(name, _format=fmt, description=desc)
    else:
        raise ValueError(f"Unknown column type: {c_type}")


def build_row_descriptor(descriptor_class, row_def):
    cols = [build_column(c) for c in row_def["columns"]]
    return descriptor_class(cols)


def build_file_descriptor(desc_data):
    header = None
    if "header" in desc_data and desc_data["header"]:
        header = build_row_descriptor(HeaderRowDescriptor, desc_data["header"])

    footer = None
    if "footer" in desc_data and desc_data["footer"]:
        footer = build_row_descriptor(FooterRowDescriptor, desc_data["footer"])

    details = [build_row_descriptor(DetailRowDescriptor, d) for d in desc_data["details"]]

    return FileDescriptor(details=details, header=header, footer=footer)


def serialize_value(val):
    if isinstance(val, (datetime, date, time)):
        return val.isoformat()
    return val


def serialize_row(row):
    return {k: serialize_value(v) for k, v in row.items()}


class TestFWFCompliance(TestCase):
    @classmethod
    def setUpClass(cls):
        ensure_compliance_cases()
        manifest_path = COMPLIANCE_DIR / "manifest.json"
        with open(manifest_path, "r", encoding="utf-8") as f:
            cls.manifest = json.load(f)

    def test_all_compliance_cases(self):
        cases = self.manifest.get("cases", [])
        self.assertGreater(len(cases), 0, "No compliance test cases found in manifest")

        for case in cases:
            case_id = case["id"]
            case_dir = COMPLIANCE_DIR / case["path"]

            descriptor_path = case_dir / "descriptor.json"
            input_path = case_dir / "input.fwf"
            expected_path = case_dir / "expected.json"

            self.assertTrue(descriptor_path.exists(), f"Missing descriptor.json for case: {case_id}")
            self.assertTrue(input_path.exists(), f"Missing input.fwf for case: {case_id}")
            self.assertTrue(expected_path.exists(), f"Missing expected.json for case: {case_id}")

            with open(descriptor_path, "r", encoding="utf-8") as f:
                desc_data = json.load(f)

            with open(input_path, "r", encoding="utf-8") as f:
                input_content = f.read()

            with open(expected_path, "r", encoding="utf-8") as f:
                expected_data = json.load(f)

            file_descriptor = build_file_descriptor(desc_data)
            
            # Format input lines so each line has exact line_size + \n
            raw_lines = input_content.replace("\r\n", "\n").splitlines()
            formatted_lines = [
                line.ljust(file_descriptor.line_size) + "\n"
                for line in raw_lines
            ]

            reader = Reader(formatted_lines, file_descriptor, newline="\n")

            parsed_rows = [serialize_row(row) for row in reader]

            self.assertEqual(
                parsed_rows,
                expected_data,
                f"Compliance test failed for case: '{case_id}'",
            )
