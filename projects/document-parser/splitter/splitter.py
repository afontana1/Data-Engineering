import os, json, time, tempfile, subprocess, shutil
import boto3

s3 = boto3.client("s3")
ddb = boto3.client("dynamodb")

RAW_BUCKET = os.environ["RAW_BUCKET"]
JOBS_TABLE = os.environ["JOBS_TABLE"]

JOB_ID = os.environ["JOB_ID"]
TENANT_ID = os.environ["TENANT_ID"]
INPUT_BUCKET = os.environ["INPUT_BUCKET"]
INPUT_KEY = os.environ["INPUT_KEY"]

SPLIT_THRESHOLD_BYTES = int(os.environ.get("SPLIT_THRESHOLD_BYTES", "450000000"))

def ddb_update(status: str = None, **fields):
    expr_names = {}
    expr_vals = {}
    sets = []
    adds = []

    if status is not None:
        expr_names["#s"] = "status"
        expr_vals[":s"] = {"S": status}
        sets.append("#s=:s")

    # updatedAt always
    expr_vals[":u"] = {"N": str(int(time.time()))}
    sets.append("updatedAt=:u")

    for k, v in fields.items():
        ph = f":{k}"
        sets.append(f"{k}={ph}")
        if isinstance(v, (int, float)):
            expr_vals[ph] = {"N": str(v)}
        else:
            expr_vals[ph] = {"S": str(v)}

    update_expr = "SET " + ", ".join(sets)
    ddb.update_item(
        TableName=JOBS_TABLE,
        Key={"jobId": {"S": JOB_ID}},
        UpdateExpression=update_expr,
        ExpressionAttributeNames=expr_names or None,
        ExpressionAttributeValues=expr_vals,
    )

def qpdf_split_to_pages(pdf_path: str, pages_dir: str) -> list[str]:
    """
    Produces page-000001.pdf, page-000002.pdf, ... in pages_dir
    """
    os.makedirs(pages_dir, exist_ok=True)
    out_pattern = os.path.join(pages_dir, "page-%06d.pdf")
    # --split-pages writes each page to a separate file
    subprocess.run(["qpdf", "--split-pages", pdf_path, out_pattern], check=True)

    page_files = sorted(
        os.path.join(pages_dir, f) for f in os.listdir(pages_dir) if f.endswith(".pdf")
    )
    if not page_files:
        raise RuntimeError("qpdf produced no page files")
    return page_files

def qpdf_merge_pages(page_files: list[str], out_path: str):
    """
    Merge a list of single-page PDFs into one PDF.
    qpdf usage: qpdf in1.pdf in2.pdf ... -- out.pdf
    """
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    cmd = ["qpdf", *page_files, "--", out_path]
    subprocess.run(cmd, check=True)

def build_parts_under_threshold(page_files: list[str], threshold_bytes: int, work_dir: str) -> list[str]:
    """
    Greedy pack pages into parts so each part file size stays <= threshold_bytes.
    """
    parts = []
    current = []
    part_idx = 1

    def finalize_current():
        nonlocal part_idx, current
        if not current:
            return
        out_path = os.path.join(work_dir, f"part-{part_idx:04d}.pdf")
        qpdf_merge_pages(current, out_path)
        parts.append(out_path)
        part_idx += 1
        current = []

    # Heuristic: estimate part size by summing page file sizes * fudge factor.
    # Then verify by actually producing the part and checking size.
    est = 0
    fudge = 1.25  # overhead / object duplication

    for pf in page_files:
        psize = os.path.getsize(pf)
        # start a part if current would likely exceed threshold
        if current and int((est + psize) * fudge) > threshold_bytes:
            finalize_current()
            est = 0

        current.append(pf)
        est += psize

        # Optional: if a single page already exceeds threshold, it must stand alone.
        if psize > threshold_bytes:
            # finalize immediately so it becomes its own part
            finalize_current()
            est = 0

    finalize_current()

    # Verify sizes; if any part is still too large, fall back to smaller packing.
    # Usually rare, but we handle it by splitting parts into smaller halves.
    verified = []
    for p in parts:
        if os.path.getsize(p) <= threshold_bytes or len(parts) == len(page_files):
            verified.append(p)
            continue

        # If too big, re-split by halving its constituent pages
        # (simple fallback: just keep single pages for safety)
        # You can make this smarter by tracking pages per part.
        raise RuntimeError(f"Produced part exceeds threshold: {p} ({os.path.getsize(p)} bytes)")

    return verified

def upload_parts_and_write_ddb(part_paths: list[str]) -> list[dict]:
    parts = []
    for idx, p in enumerate(part_paths, start=1):
        part_key = f"{TENANT_ID}/{JOB_ID}/input/parts/part-{idx:04d}.pdf"
        s3.upload_file(p, RAW_BUCKET, part_key)
        parts.append({"partIndex": idx, "bucket": RAW_BUCKET, "key": part_key})

    ddb.update_item(
        TableName=JOBS_TABLE,
        Key={"jobId": {"S": JOB_ID}},
        UpdateExpression="SET partsJson=:pj, partsTotal=:pt, updatedAt=:u",
        ExpressionAttributeValues={
            ":pj": {"S": json.dumps(parts)},
            ":pt": {"N": str(len(parts))},
            ":u": {"N": str(int(time.time()))},
        },
    )
    return parts

def main():
    try:
        ddb_update("SPLITTING")
        with tempfile.TemporaryDirectory() as td:
            local_in = os.path.join(td, "in.pdf")
            pages_dir = os.path.join(td, "pages")
            parts_dir = os.path.join(td, "parts")

            s3.download_file(INPUT_BUCKET, INPUT_KEY, local_in)

            page_files = qpdf_split_to_pages(local_in, pages_dir)
            part_paths = build_parts_under_threshold(page_files, SPLIT_THRESHOLD_BYTES, parts_dir)

            if not part_paths:
                raise RuntimeError("No parts produced")

            upload_parts_and_write_ddb(part_paths)

            # Optional: helps UI; SFN will set TEXTRACT_RUNNING anyway
            ddb_update("TEXTRACT_RUNNING")

    except Exception as e:
        ddb_update("FAILED", errorMessage=f"{type(e).__name__}: {e}")
        raise

if __name__ == "__main__":
    main()