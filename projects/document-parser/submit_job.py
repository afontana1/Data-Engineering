import argparse
import json
import sys
import time
from pathlib import Path
from typing import Any, Dict, Optional
import urllib.parse

import requests


def _guess_content_type(path: Path) -> str:
    # You can expand this, but PDFs are your main case.
    if path.suffix.lower() == ".pdf":
        return "application/pdf"
    return "application/octet-stream"


def _safe_get(d: Dict[str, Any], keys: str) -> Any:
    """
    Pull nested dict keys using dot notation, e.g. "upload.url".
    Returns None if any level missing.
    """
    cur: Any = d
    for k in keys.split("."):
        if not isinstance(cur, dict) or k not in cur:
            return None
        cur = cur[k]
    return cur


def create_job(api_base: str, tenant_id: str, filename: str, content_type: str, timeout_s: int) -> Dict[str, Any]:
    url = f"{api_base.rstrip('/')}/jobs"
    payload = {"tenantId": tenant_id, "filename": filename, "contentType": content_type}
    r = requests.post(url, json=payload, timeout=timeout_s)
    r.raise_for_status()
    return r.json()


def upload_to_presigned_put(presigned_url: str, file_path: Path, content_type: str, timeout_s: int) -> None:
    # Use raw binary upload; presigned PUT usually requires Content-Type to match what was signed.
    with file_path.open("rb") as f:
        r = requests.put(
            presigned_url,
            data=f,
            headers={"Content-Type": content_type},
            timeout=timeout_s,
        )
    # Many presigned PUTs return 200 or 204
    if r.status_code not in (200, 201, 204):
        raise RuntimeError(f"Upload failed: HTTP {r.status_code} - {r.text[:500]}")


def start_job(api_base: str, job_id: str, timeout_s: int) -> Dict[str, Any]:
    url = f"{api_base.rstrip('/')}/jobs/{urllib.parse.quote(job_id)}/start"
    r = requests.post(url, timeout=timeout_s)
    r.raise_for_status()
    # Might return JSON or empty
    try:
        return r.json()
    except Exception:
        return {"status": "started"}


def get_job(api_base: str, job_id: str, timeout_s: int) -> Dict[str, Any]:
    url = f"{api_base.rstrip('/')}/jobs/{urllib.parse.quote(job_id)}"
    r = requests.get(url, timeout=timeout_s)
    r.raise_for_status()
    return r.json()


def get_result(api_base: str, job_id: str, timeout_s: int) -> Dict[str, Any]:
    url = f"{api_base.rstrip('/')}/jobs/{urllib.parse.quote(job_id)}/result"
    r = requests.get(url, timeout=timeout_s)
    r.raise_for_status()
    return r.json()


def download_file(url: str, out_path: Path, timeout_s: int) -> None:
    with requests.get(url, stream=True, timeout=timeout_s) as r:
        r.raise_for_status()
        out_path.parent.mkdir(parents=True, exist_ok=True)
        with out_path.open("wb") as f:
            for chunk in r.iter_content(chunk_size=1024 * 1024):
                if chunk:
                    f.write(chunk)


def poll_until_done(
    api_base: str,
    job_id: str,
    timeout_total_s: int,
    timeout_s: int,
    initial_sleep_s: float = 1.0,
    max_sleep_s: float = 20.0,
) -> Dict[str, Any]:
    """
    Exponential backoff polling until status is SUCCEEDED/FAILED or timeout_total_s elapsed.
    """
    start = time.time()
    sleep_s = initial_sleep_s
    last = None

    while True:
        job = get_job(api_base, job_id, timeout_s=timeout_s)
        last = job

        status = (job.get("status") or "").upper()
        parts_done = job.get("partsDone")
        parts_total = job.get("partsTotal")

        if parts_done is not None and parts_total is not None:
            print(f"status={status} progress={parts_done}/{parts_total}")
        else:
            print(f"status={status}")

        if status in ("SUCCEEDED", "FAILED"):
            return job

        if time.time() - start > timeout_total_s:
            raise TimeoutError(f"Timed out waiting for job {job_id} after {timeout_total_s}s")

        time.sleep(sleep_s)
        sleep_s = min(max_sleep_s, sleep_s * 1.6)


def main():
    p = argparse.ArgumentParser(description="Submit a PDF to the document parsing service and poll for results.")
    p.add_argument("--api-base", required=True, help="API base URL, e.g. https://...execute-api.../v1")
    p.add_argument("--pdf", required=True, help="Path to local PDF")
    p.add_argument("--tenant-id", default="t1", help="Tenant ID (default: t1)")
    p.add_argument("--out", default="document.json", help="Where to save output JSON (default: document.json)")
    p.add_argument("--timeout", type=int, default=30, help="HTTP timeout seconds (default: 30)")
    p.add_argument("--poll-timeout", type=int, default=3600, help="Max seconds to poll (default: 3600)")
    args = p.parse_args()

    pdf_path = Path(args.pdf)
    if not pdf_path.exists():
        print(f"PDF not found: {pdf_path}", file=sys.stderr)
        sys.exit(2)

    api_base = args.api_base.rstrip("/")
    content_type = _guess_content_type(pdf_path)

    print(f"Creating job for {pdf_path.name} ...")
    job_resp = create_job(api_base, args.tenant_id, pdf_path.name, content_type, timeout_s=args.timeout)

    # Try common response shapes:
    job_id = job_resp.get("jobId") or _safe_get(job_resp, "job.jobId") or job_resp.get("id")
    upload_url = _safe_get(job_resp, "upload.url") or job_resp.get("uploadUrl") or job_resp.get("url")

    if not job_id or not upload_url:
        print("Unexpected /jobs response. Got:", file=sys.stderr)
        print(json.dumps(job_resp, indent=2), file=sys.stderr)
        sys.exit(1)

    print(f"jobId={job_id}")
    print("Uploading PDF to presigned URL ...")
    upload_to_presigned_put(upload_url, pdf_path, content_type, timeout_s=args.timeout)
    print("Upload OK.")

    print("Starting job ...")
    start_job(api_base, job_id, timeout_s=args.timeout)

    print("Polling for completion ...")
    final_job = poll_until_done(
        api_base,
        job_id,
        timeout_total_s=args.poll_timeout,
        timeout_s=args.timeout,
        initial_sleep_s=1.5,
        max_sleep_s=20.0,
    )

    status = (final_job.get("status") or "").upper()
    if status == "FAILED":
        print("Job FAILED.")
        print(json.dumps(final_job, indent=2))
        sys.exit(3)

    print("Job SUCCEEDED. Fetching result link ...")
    result = get_result(api_base, job_id, timeout_s=args.timeout)

    download_url = result.get("downloadUrl") or _safe_get(result, "result.downloadUrl") or result.get("url")
    if not download_url:
        print("Unexpected /result response. Got:", file=sys.stderr)
        print(json.dumps(result, indent=2), file=sys.stderr)
        sys.exit(1)

    out_path = Path(args.out)
    print(f"Downloading output to {out_path} ...")
    download_file(download_url, out_path, timeout_s=args.timeout)
    print("Done.")


if __name__ == "__main__":
    main()