import io
import math
import re
from dataclasses import dataclass
from typing import Dict, List, Optional, Tuple

import pandas as pd


@dataclass
class CheckStatus:
    level: str  # "PASS" | "WARN" | "FAIL" | "INFO"
    title: str
    details: List[str]


def smart_find_col(df: pd.DataFrame, candidates: List[str]) -> Optional[str]:
    cols = {c.lower(): c for c in df.columns}
    for cand in candidates:
        if cand.lower() in cols:
            return cols[cand.lower()]
    return None


def extract_bom_signals(df: pd.DataFrame) -> Dict:
    """
    Extract signals from BoM with flexible column names.
    Required for checks:
      - Voc_STC per module
      - Temp coefficient for Voc (per °C)
      - Modules per string
      - Inverter DC max voltage
      - Inverter model/name (optional)
    """
    c_voc = smart_find_col(df, ["Voc_STC", "Voc", "Module_Voc", "PV_Voc"])
    c_tc = smart_find_col(
        df, ["TempCoeff", "Temp_Coeff", "Voc_TempCoeff", "TempCoeff_Voc"]
    )
    c_mps = smart_find_col(
        df, ["ModulesPerString", "Modules_per_string", "MPS", "PanelsPerString"]
    )
    c_inv = smart_find_col(df, ["Inverter_Vmax", "InverterVmax", "DC_Vmax", "Vmax_DC"])
    c_inv_name = smart_find_col(
        df, ["Inverter", "InverterModel", "INV_Model", "Inverter_Model"]
    )

    voc_stc = (
        float(df[c_voc].dropna().iloc[0])
        if c_voc and not df[c_voc].dropna().empty
        else 49.5
    )
    temp_coeff = (
        float(df[c_tc].dropna().iloc[0])
        if c_tc and not df[c_tc].dropna().empty
        else -0.0029
    )
    mps = (
        int(df[c_mps].dropna().iloc[0])
        if c_mps and not df[c_mps].dropna().empty
        else 22
    )
    inverter_vmax = (
        float(df[c_inv].dropna().iloc[0])
        if c_inv and not df[c_inv].dropna().empty
        else 1100.0
    )
    inverter_name = (
        str(df[c_inv_name].dropna().iloc[0])
        if c_inv_name and not df[c_inv_name].dropna().empty
        else "Inverter model not specified"
    )

    # normalize percent coefficients
    if abs(temp_coeff) > 0.05:
        temp_coeff = temp_coeff / 100.0

    meta = {
        "voc_source": c_voc or "DEFAULT",
        "tc_source": c_tc or "DEFAULT",
        "mps_source": c_mps or "DEFAULT",
        "vmax_source": c_inv or "DEFAULT",
        "invname_source": c_inv_name or "DEFAULT",
    }

    return {
        "voc_stc": voc_stc,
        "temp_coeff": temp_coeff,
        "modules_per_string": mps,
        "inverter_vmax": inverter_vmax,
        "inverter_name": inverter_name,
        "meta": meta,
    }


def try_extract_from_sld(pdf_bytes: bytes) -> Dict:
    """
    Best-effort PDF text extraction (first pages) + regex.
    Returns: inverter_vmax, modules_per_string, notes
    """
    out = {"inverter_vmax": None, "modules_per_string": None, "notes": ""}

    try:
        import PyPDF2  # type: ignore

        reader = PyPDF2.PdfReader(io.BytesIO(pdf_bytes))
        text = ""
        for i in range(min(len(reader.pages), 3)):
            text += "\n" + (reader.pages[i].extract_text() or "")

        if not text.strip():
            out["notes"] = "SLD text extraction empty (scan/image likely)."
            return out

        vmax_patterns = [
            r"(?:DC\s*MAX|DC\s*MAXIMUM|VDC\s*MAX|V\s*MAX|MAX\s*DC)\s*[:=]?\s*(\d{3,4})\s*V",
            r"(?:Vmax|V\s*max)\s*[:=]?\s*(\d{3,4})\s*V",
            r"(\d{3,4})\s*V\s*(?:DC\s*MAX|VDC\s*MAX|MAX\s*DC)",
        ]
        for pat in vmax_patterns:
            m = re.search(pat, text, flags=re.IGNORECASE)
            if m:
                out["inverter_vmax"] = float(m.group(1))
                break

        mps_patterns = [
            r"(?:MODULES\s*/\s*STRING|MODULES\s*PER\s*STRING|MOD\s*/\s*STR)\s*[:=]?\s*(\d{1,3})",
            r"\bMPS\b\s*[:=]?\s*(\d{1,3})",
            r"(?:STRING)\s*[:=]?\s*(\d{1,3})\s*(?:MODULES|MOD)",
        ]
        for pat in mps_patterns:
            m = re.search(pat, text, flags=re.IGNORECASE)
            if m:
                out["modules_per_string"] = int(m.group(1))
                break

        out["notes"] = "SLD signals extracted from text (best-effort)."
        return out

    except Exception as e:
        out["notes"] = f"SLD extraction unavailable ({type(e).__name__})."
        return out


def compare_bom_vs_sld(bom_sig: Dict, sld_sig: Dict) -> CheckStatus:
    mismatch = []
    gaps = []

    if sld_sig.get("inverter_vmax") is None:
        gaps.append("Inverter DC max voltage not detected in SLD.")
    else:
        if (
            abs(float(bom_sig["inverter_vmax"]) - float(sld_sig["inverter_vmax"]))
            > 1e-6
        ):
            mismatch.append(
                f"Inverter DC max differs (BoM {bom_sig['inverter_vmax']:.0f} V vs SLD {float(sld_sig['inverter_vmax']):.0f} V)."
            )

    if sld_sig.get("modules_per_string") is None:
        gaps.append("Modules/string not detected in SLD.")
    else:
        if int(bom_sig["modules_per_string"]) != int(sld_sig["modules_per_string"]):
            mismatch.append(
                f"Modules/string differs (BoM {bom_sig['modules_per_string']} vs SLD {int(sld_sig['modules_per_string'])})."
            )

    if mismatch:
        return CheckStatus("WARN", "BoM ↔ SLD consistency", mismatch)
    if gaps:
        # Not a mismatch, but extraction incomplete
        return CheckStatus(
            "INFO",
            "BoM ↔ SLD consistency",
            gaps + ["If SLD is scanned, OCR/Vision is needed for reliable extraction."],
        )
    return CheckStatus(
        "PASS", "BoM ↔ SLD consistency", ["BoM values match the detected SLD signals."]
    )


def calc_voc_cold(voc_stc: float, temp_coeff: float, tmin: float) -> float:
    # Voc_cold = Voc_STC * (1 + |temp_coeff| * (25 - Tmin))
    delta = 25.0 - float(tmin)
    return voc_stc * (1.0 + abs(temp_coeff) * delta)


def climate_voltage_check(
    bom_sig: Dict, tmin: float
) -> Tuple[CheckStatus, Dict, List[str]]:
    """
    Critical if string Voc at Tmin exceeds inverter DC max.
    Recommend reducing modules/string to meet limit.
    """
    voc_cold = calc_voc_cold(bom_sig["voc_stc"], bom_sig["temp_coeff"], tmin)
    mps = int(bom_sig["modules_per_string"])
    vmax = float(bom_sig["inverter_vmax"])
    string_v = voc_cold * mps

    numbers = {
        "Voc_STC_per_module_V": bom_sig["voc_stc"],
        "TempCoeff_per_C": bom_sig["temp_coeff"],
        "Tmin_C": float(tmin),
        "Voc_cold_per_module_V": voc_cold,
        "Modules_per_string": mps,
        "String_Voc_at_Tmin_V": string_v,
        "Inverter_DC_max_V": vmax,
    }

    recs = []

    if string_v <= vmax:
        return (
            CheckStatus(
                "PASS",
                "Winter overvoltage risk",
                ["Worst-case string Voc at Tmin is within inverter DC max."],
            ),
            numbers,
            recs,
        )

    # find safe MPS
    suggested = mps
    while suggested > 1 and (voc_cold * suggested) > vmax:
        suggested -= 1

    recs.append(
        f"Reduce modules/string from {mps} to {suggested} to keep string Voc at Tmin ≤ {vmax:.0f} V."
    )
    recs.append(
        "Re-check string sizing for all MPPT inputs and confirm manufacturer absolute max DC voltage limits."
    )
    return (
        CheckStatus(
            "FAIL",
            "Winter overvoltage risk",
            [
                "String Voc at Tmin exceeds inverter DC max. Potential inverter damage risk."
            ],
        ),
        numbers,
        recs,
    )


def saudi_standards_snapshot(
    climate_ok: bool, bom_sld_level: str
) -> Tuple[List[str], List[str]]:
    """
    Provide a professional snapshot aligned to typical Saudi / IEC expectations.
    Output:
      - compliant_points
      - gaps_points (actionable)
    """
    compliant = []
    gaps = []

    # SEC / IEC 62548 / IEC 60364 / labeling / protection 
    if climate_ok:
        compliant.append(
            "String sizing vs minimum temperature (overvoltage) check passed."
        )
        compliant.append("Inverter DC maximum verified against worst-case string Voc.")
    else:
        gaps.append(
            "String sizing vs minimum temperature fails (overvoltage). Update design string length / MPPT allocation."
        )

    if bom_sld_level in ("PASS", "INFO"):
        compliant.append("BoM and SLD consistency check performed (best-effort).")
        if bom_sld_level == "INFO":
            gaps.append(
                "SLD key signals not fully extracted. Provide native PDF (text) or enable OCR/Vision extraction."
            )
    else:
        gaps.append("BoM and SLD values mismatch. Resolve before procurement/approval.")

    gaps.extend(
        [
            "Protection coordination (DC fuses/breakers, SPD type and ratings) not validated from current inputs.",
            "Labeling and isolation (DC isolators, emergency shutdown labels) require drawing confirmation.",
            "Cable sizing/derating (installation method, ambient, grouping) not validated from current inputs.",
            "Earthing/bonding continuity and conductor sizing not validated from current inputs.",
            "Fire safety routing and rooftop requirements require site/fire review.",
        ]
    )

    return compliant, gaps
