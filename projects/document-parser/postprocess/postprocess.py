import os, json, time, traceback
import boto3

s3 = boto3.client("s3")
ddb = boto3.client("dynamodb")
textract = boto3.client("textract")

RAW_BUCKET = os.environ["RAW_BUCKET"]
PARSED_BUCKET = os.environ["PARSED_BUCKET"]
JOBS_TABLE = os.environ["JOBS_TABLE"]

JOB_ID = os.environ["JOB_ID"]
TENANT_ID = os.environ["TENANT_ID"]

PARTS_JSON = os.environ.get("PARTS_JSON")  # list of parts
TEXTRACT_JOBS_JSON = os.environ.get("TEXTRACT_JOBS_JSON")  # <-- UPDATED name from SFN (was TEXTRACT_JOB_IDS_JSON)

def ddb_update_status(status: str, **extras):
    expr_names = {"#s": "status"}
    expr_vals = {
        ":s": {"S": status},
        ":u": {"N": str(int(time.time()))},
    }
    update_expr = "SET #s=:s, updatedAt=:u"

    for k, v in extras.items():
        placeholder = f":{k}"
        update_expr += f", {k}={placeholder}"
        if isinstance(v, (int, float)):
            expr_vals[placeholder] = {"N": str(v)}
        else:
            # store JSON/text as string
            expr_vals[placeholder] = {"S": str(v)}

    ddb.update_item(
        TableName=JOBS_TABLE,
        Key={"jobId": {"S": JOB_ID}},
        UpdateExpression=update_expr,
        ExpressionAttributeNames=expr_names,
        ExpressionAttributeValues=expr_vals,
    )

def get_all_blocks(textract_job_id: str):
    blocks = []
    next_token = None
    while True:
        args = {"JobId": textract_job_id}
        if next_token:
            args["NextToken"] = next_token
        resp = textract.get_document_analysis(**args)
        blocks.extend(resp.get("Blocks", []))
        next_token = resp.get("NextToken")
        if not next_token:
            break
    return blocks

def build_canonical_document(all_parts_blocks):
    # TODO: implement your real canonical transformation.
    # Keep "provenance" so you can debug later.
    return {
        "documentId": f"{TENANT_ID}:{JOB_ID}",
        "jobId": JOB_ID,
        "tenantId": TENANT_ID,
        "outputVersion": "1.0",
        "processedAt": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "provenance": [
            {
                "extractor": "TEXTRACT",
                "parts": [
                    {"partIndex": p["partIndex"], "textractJobId": p["textractJobId"]}
                    for p in all_parts_blocks
                ]
            }
        ],
        "pages": []
    }

def main():
    try:
        ddb_update_status("POSTPROCESSING")

        parts = json.loads(PARTS_JSON) if PARTS_JSON else []
        textract_jobs = json.loads(TEXTRACT_JOBS_JSON) if TEXTRACT_JOBS_JSON else []

        if not textract_jobs:
            raise RuntimeError("Missing TEXTRACT_JOBS_JSON; cannot postprocess")

        # Ensure stable order by partIndex
        textract_jobs_sorted = sorted(textract_jobs, key=lambda x: int(x.get("partIndex", 0)))

        all_parts_blocks = []
        for r in textract_jobs_sorted:
            tjid = r["textractJobId"]
            part_index = r.get("partIndex")
            blocks = get_all_blocks(tjid)
            all_parts_blocks.append({"partIndex": part_index, "textractJobId": tjid, "blocks": blocks})

        doc = build_canonical_document(all_parts_blocks)

        out_key = f"{TENANT_ID}/{JOB_ID}/output/document.json"
        s3.put_object(
            Bucket=PARSED_BUCKET,
            Key=out_key,
            Body=json.dumps(doc).encode("utf-8"),
            ContentType="application/json"
        )

        # Write output pointer + success (even if SFN also sets it; ensures job record is correct)
        ddb_update_status("SUCCEEDED", outputBucket=PARSED_BUCKET, outputKey=out_key)

    except Exception as e:
        # Keep error message compact but helpful
        msg = f"{type(e).__name__}: {e}"
        ddb_update_status("FAILED", errorMessage=msg)
        raise

if __name__ == "__main__":
    main()