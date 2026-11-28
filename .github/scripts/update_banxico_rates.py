#!/usr/bin/env python3
"""Fetch latest Mexican government rates from Banxico SIE API and write rates.json.

Uses only the Python standard library so GitHub Actions needs no pip installs.
"""

from __future__ import annotations

import argparse
import json
import math
import os
import sys
import urllib.error
import urllib.request
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any

# Banxico SIE REST API endpoints:
# - oportuno: latest available observation for each series
# - range: exact date range (used for SP68257 UDI so we get today's value instead of Banxico's 15-day advance schedule)
SIE_BASE_URL = (
    "https://www.banxico.org.mx/SieAPIRest/service/v1/series/{series}/datos/oportuno"
)
SIE_RANGE_URL = (
    "https://www.banxico.org.mx/SieAPIRest/service/v1/series/{series}/datos/{start}/{end}"
)
MX_TZ = timezone(timedelta(hours=-6))

# Estimated annual management fee subtracted from Banxico's target rate to
# approximate BONDDIA net-of-fee yield (BONDDIA has no direct SIE series).
BONDDIA_FEE_SPREAD = 0.25

# Verified Banxico SIE series IDs:
#   SF43936  - CETES 28 días, tasa de rendimiento (subasta primaria semanal)
#   SF43939  - CETES 91 días, tasa de rendimiento (subasta primaria semanal)
#   SF43942  - CETES 182 días, tasa de rendimiento (subasta primaria semanal)
#   SF43945  - CETES 364 días, tasa de rendimiento (subasta primaria semanal)
#   SF349785 - CETES 728 días (2 años), tasa de rendimiento (subasta primaria)
#   SF43924  - Udibonos a 10 años, tasa de interés real (subasta primaria)
#   SP68257  - Valor de la UDI en pesos
#   SP30578  - Inflación anual INPC (variación porcentual anual)
#   SP1      - Índice Nacional de Precios al Consumidor (INPC general, para detectar umbral Art. 152 LISR > 10%)
#   SF61745  - Tasa objetivo de Banxico (referencia para estimar BONDDIA)
SERIES_MAP = {
    "c28": {
        "id": "SF43936",
        "label": "Banxico SIE (SF43936), subasta",
    },
    "c91": {
        "id": "SF43939",
        "label": "Banxico SIE (SF43939), subasta",
    },
    "c182": {
        "id": "SF43942",
        "label": "Banxico SIE (SF43942), subasta",
    },
    "c364": {
        "id": "SF43945",
        "label": "Banxico SIE (SF43945), subasta",
    },
    "c2y": {
        "id": "SF349785",
        "label": "Banxico SIE (SF349785), subasta",
    },
    "udi_rate": {
        "id": "SF43924",
        "label": "Banxico SIE (SF43924), tasa real",
    },
    "udi_val": {
        "id": "SP68257",
        "label": "Banxico SIE (SP68257)",
    },
    "inf": {
        "id": "SP30578",
        "label": "Banxico SIE (SP30578)",
    },
    "inpc": {
        "id": "SP1",
        "label": "Banxico SIE (SP1)",
    },
    "target_rate": {
        "id": "SF61745",
        "label": "Estimado desde tasa objetivo Banxico (SF61745) menos comisión BONDDIA",
    },
}

DEFAULT_DATA: dict[str, Any] = {
    "updated_at": "2026-11-19",
    "udi": 8.60,
    "inf": 4.00,
    "rates": {
        "liq": {
            "g": 6.00,
            "date": "2026-11-19",
            "src": "Estimado: tasa objetivo Banxico menos comisión del fondo",
        },
        "c28": {"g": 6.19, "date": "2026-11-19", "src": "Banxico SIE, subasta 19/11/2026"},
        "c91": {"g": 6.49, "date": "2026-11-19", "src": "Banxico SIE, subasta 19/11/2026"},
        "c182": {"g": 6.67, "date": "2026-11-19", "src": "Banxico SIE, subasta 19/11/2026"},
        "c364": {"g": 6.95, "date": "2026-11-12", "src": "Banxico SIE, subasta 12/11/2026"},
        "c2y": {"g": 7.87, "date": "2026-11-19", "src": "Banxico SIE, subasta 19/11/2026"},
        "udi": {"g": 4.93, "date": "2026-11-19", "src": "Banxico SIE, tasa real 19/11/2026"},
    },
}


def parse_bmx_date(raw: str) -> str | None:
    """Convert Banxico DD/MM/YYYY date string to ISO YYYY-MM-DD."""
    try:
        return datetime.strptime(raw.strip(), "%d/%m/%Y").strftime("%Y-%m-%d")
    except ValueError:
        return None


def fmt_es_date(iso_date: str) -> str:
    """Convert ISO YYYY-MM-DD to DD/MM/YYYY for Spanish labels."""
    try:
        return datetime.strptime(iso_date, "%Y-%m-%d").strftime("%d/%m/%Y")
    except ValueError:
        return iso_date


def parse_bmx_number(raw: Any) -> float | None:
    """Parse Banxico numeric string, returning None for 'N/E' or invalid values."""
    if raw is None:
        return None
    text = str(raw).strip().replace(",", "")
    if not text or text.upper() == "N/E":
        return None
    try:
        val = float(text)
    except ValueError:
        return None
    return val if math.isfinite(val) else None


def fetch_series(
    series_ids: list[str],
    token: str,
    url_override: str | None = None,
) -> dict[str, tuple[float, str]]:
    """Query Banxico SIE for one or more series in a single HTTP request."""
    url = url_override or SIE_BASE_URL.format(series=",".join(series_ids))
    req = urllib.request.Request(
        url,
        headers={
            "Bmx-Token": token,
            "Accept": "application/json",
            "User-Agent": "habibapez-liquidacion-rates-updater/1.0",
        },
    )
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            payload = json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as exc:
        body = exc.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"Banxico SIE HTTP {exc.code}: {body[:400]}") from exc
    except urllib.error.URLError as exc:
        raise RuntimeError(f"Banxico SIE network error: {exc}") from exc

    results: dict[str, tuple[float, str]] = {}
    for serie in payload.get("bmx", {}).get("series", []):
        sid = serie.get("idSerie")
        datos = serie.get("datos") or []
        if not sid or not datos:
            continue
        obs = datos[-1]
        val = parse_bmx_number(obs.get("dato"))
        iso_date = parse_bmx_date(obs.get("fecha", ""))
        if val is not None and iso_date is not None:
            results[sid] = (val, iso_date)
    return results


def fetch_today_udi(token: str) -> tuple[float, str] | None:
    """Fetch today's UDI value (Mexico City date) instead of Banxico's advance schedule."""
    sid = SERIES_MAP["udi_val"]["id"]
    today_mx = datetime.now(MX_TZ).strftime("%Y-%m-%d")
    url = SIE_RANGE_URL.format(series=sid, start=today_mx, end=today_mx)
    try:
        res = fetch_series([sid], token, url_override=url)
        return res.get(sid)
    except RuntimeError as exc:
        print(f"Notice: could not fetch today's UDI ({exc}); falling back to oportuno.", file=sys.stderr)
        return None


def load_previous(path: Path | None) -> dict[str, Any]:
    if path and path.is_file():
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
            if isinstance(data, dict) and isinstance(data.get("rates"), dict):
                return data
        except (OSError, json.JSONDecodeError) as exc:
            print(f"Warning: could not parse previous rates.json ({exc}); using defaults.", file=sys.stderr)
    return json.loads(json.dumps(DEFAULT_DATA))


def load_fiscal(path: Path | None) -> dict[str, Any] | None:
    if path and path.is_file():
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
            if isinstance(data, dict) and isinstance(data.get("isr_m"), list):
                return data
        except (OSError, json.JSONDecodeError) as exc:
            print(f"Warning: could not parse fiscal_mx.json ({exc}).", file=sys.stderr)
    return None


def evaluate_fiscal_alert(
    fiscal: dict[str, Any] | None,
    fetched: dict[str, tuple[float, str]],
) -> tuple[bool, str]:
    """Check whether annual DOF fiscal parameters or Art. 152 LISR (>10% INPC) need review."""
    if not fiscal:
        return False, ""
    reasons: list[str] = []
    now_year = datetime.now(MX_TZ).year
    f_year = int(fiscal.get("fiscal_year") or 0)
    if f_year and now_year > f_year:
        reasons.append(
            f"New calendar year {now_year} (fiscal_mx.json is still set to {f_year}): "
            "review SM, UMA, and LIF interest withholding rate."
        )

    inpc_sid = SERIES_MAP["inpc"]["id"]
    base_val = fiscal.get("inpc_base_value")
    if inpc_sid in fetched and isinstance(base_val, (int, float)) and base_val > 0:
        cur_inpc, inpc_date = fetched[inpc_sid]
        cum_pct = (cur_inpc / base_val - 1.0) * 100.0
        if cum_pct >= 10.0:
            reasons.append(
                f"Cumulative INPC since {fiscal.get('inpc_base_date', 'base')} reached "
                f"{cum_pct:.2f}% ({cur_inpc:.3f} on {inpc_date} vs base {base_val:.3f}), "
                "crossing the 10% Art. 152 LISR threshold: verify Anexo 8 RMF monthly ISR table."
            )

    return bool(reasons), " | ".join(reasons)


def numeric_snapshot(data: dict[str, Any]) -> dict[str, Any]:
    """Extract numeric and fiscal fields so we commit only when actual values change."""
    rates = data.get("rates", {})
    return {
        "udi": data.get("udi"),
        "inf": data.get("inf"),
        "rates": {k: rates.get(k, {}).get("g") for k in ("liq", "c28", "c91", "c182", "c364", "c2y", "udi")},
        "fiscal": data.get("fiscal"),
    }


def build_rates_json(
    fetched: dict[str, tuple[float, str]],
    prev: dict[str, Any],
    fiscal: dict[str, Any] | None = None,
) -> dict[str, Any]:
    prev_rates = prev.get("rates", {})
    out_rates: dict[str, dict[str, Any]] = {}
    observed_dates: list[str] = []

    # Direct rate series
    for key, cfg_key in (
        ("c28", "c28"),
        ("c91", "c91"),
        ("c182", "c182"),
        ("c364", "c364"),
        ("c2y", "c2y"),
        ("udi", "udi_rate"),
    ):
        sid = SERIES_MAP[cfg_key]["id"]
        label = SERIES_MAP[cfg_key]["label"]
        if sid in fetched:
            val, iso_date = fetched[sid]
            out_rates[key] = {
                "g": round(val, 2),
                "date": iso_date,
                "src": f"{label} {fmt_es_date(iso_date)}",
            }
            observed_dates.append(iso_date)
        elif key in prev_rates:
            out_rates[key] = prev_rates[key]
        else:
            out_rates[key] = DEFAULT_DATA["rates"][key]

    # Estimated BONDDIA from Banxico target rate (SF61745)
    t_sid = SERIES_MAP["target_rate"]["id"]
    if t_sid in fetched:
        target_val, iso_date = fetched[t_sid]
        bonddia_est = round(max(0.0, target_val - BONDDIA_FEE_SPREAD), 2)
        out_rates["liq"] = {
            "g": bonddia_est,
            "date": iso_date,
            "src": (
                f"Estimado: tasa objetivo Banxico ({target_val:.2f}%, {fmt_es_date(iso_date)}) "
                f"menos ~{BONDDIA_FEE_SPREAD:.2f}% de comisión. Verifica en cetesdirecto"
            ),
        }
        observed_dates.append(iso_date)
    elif "liq" in prev_rates:
        out_rates["liq"] = prev_rates["liq"]
    else:
        out_rates["liq"] = DEFAULT_DATA["rates"]["liq"]

    # Order keys cleanly to match expected schema
    ordered_rates = {k: out_rates[k] for k in ("liq", "c28", "c91", "c182", "c364", "c2y", "udi")}

    # UDI value (SP68257). Do not include its date in updated_at because Banxico
    # publishes UDI schedules up to 15 days in advance.
    udi_sid = SERIES_MAP["udi_val"]["id"]
    if udi_sid in fetched:
        udi_val = round(fetched[udi_sid][0], 2)
    else:
        udi_val = prev.get("udi", DEFAULT_DATA["udi"])

    # Annual inflation INPC (SP30578)
    inf_sid = SERIES_MAP["inf"]["id"]
    if inf_sid in fetched:
        inf_val = round(fetched[inf_sid][0], 2)
        observed_dates.append(fetched[inf_sid][1])
    else:
        inf_val = prev.get("inf", DEFAULT_DATA["inf"])

    today_mx = datetime.now(MX_TZ).strftime("%Y-%m-%d")
    updated_at = min(max(observed_dates), today_mx) if observed_dates else today_mx

    out: dict[str, Any] = {
        "updated_at": updated_at,
        "udi": udi_val,
        "inf": inf_val,
        "rates": ordered_rates,
    }
    if fiscal is not None:
        out["fiscal"] = fiscal
    elif isinstance(prev.get("fiscal"), dict):
        out["fiscal"] = prev["fiscal"]
    return out


def main() -> int:
    parser = argparse.ArgumentParser(description="Update Banxico rates.json from SIE API.")
    parser.add_argument("--output", required=True, type=Path, help="Output path for rates.json")
    parser.add_argument("--previous", type=Path, default=None, help="Optional previous rates.json for fallback and diff")
    parser.add_argument("--fiscal", type=Path, default=None, help="Optional fiscal_mx.json to embed in rates.json")
    args = parser.parse_args()

    token = os.environ.get("BANXICO_TOKEN", "").strip()
    if not token:
        print("Error: BANXICO_TOKEN environment variable is missing.", file=sys.stderr)
        return 1

    prev = load_previous(args.previous)
    fiscal = load_fiscal(args.fiscal)
    series_ids = [cfg["id"] for cfg in SERIES_MAP.values()]
    fetched = fetch_series(series_ids, token)

    # Prefer today's UDI (Mexico City date) over Banxico's 15-day advance schedule
    today_udi = fetch_today_udi(token)
    if today_udi is not None:
        fetched[SERIES_MAP["udi_val"]["id"]] = today_udi

    if not fetched:
        print("Error: Banxico SIE returned no valid observations for any series.", file=sys.stderr)
        return 1

    missing = [f"{k}({cfg['id']})" for k, cfg in SERIES_MAP.items() if cfg["id"] not in fetched]
    if missing:
        print(f"Notice: kept previous values for unavailable series: {', '.join(missing)}", file=sys.stderr)

    new_data = build_rates_json(fetched, prev, fiscal=fiscal)
    fiscal_alert, fiscal_reason = evaluate_fiscal_alert(fiscal, fetched)

    prev_exists = bool(args.previous and args.previous.is_file())
    today_mx = datetime.now(MX_TZ).strftime("%Y-%m-%d")
    stale_future = str(prev.get("updated_at") or "") > today_mx
    changed = (not prev_exists) or stale_future or (numeric_snapshot(new_data) != numeric_snapshot(prev))

    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(new_data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    gh_output = os.environ.get("GITHUB_OUTPUT")
    if gh_output:
        with open(gh_output, "a", encoding="utf-8") as fh:
            fh.write(f"changed={'true' if changed else 'false'}\n")
            fh.write(f"updated_at={new_data['updated_at']}\n")
            fh.write(f"fiscal_alert={'true' if fiscal_alert else 'false'}\n")
            fh.write(f"fiscal_reason={fiscal_reason}\n")

    print(
        f"Wrote {args.output} (updated_at={new_data['updated_at']}, "
        f"fetched={len(fetched)}/{len(series_ids)}, changed={changed}, fiscal_alert={fiscal_alert})"
    )
    if fiscal_alert:
        print(f"Fiscal review alert: {fiscal_reason}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
