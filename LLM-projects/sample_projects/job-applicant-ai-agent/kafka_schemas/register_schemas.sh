#!/bin/bash

SCHEMA_REGISTRY_URL="http://host.docker.internal:8081"
SCHEMA_DIR="./schemas"
PY_OUTDIR_SCHEMAS="./python_schemas"

function schemaPost {
  cat <<EOF
{
  "schemaType": "PROTOBUF",
  "schema": "${escapedSchema}"
}
EOF
}

# Ensure output directory exists
mkdir -p ${PY_OUTDIR_SCHEMAS}

# Iterate over all .proto files in the directory
for proto_file in ${SCHEMA_DIR}/*.proto; do
  if [[ -f "$proto_file" ]]; then
    # Extract the base name without extension for the subject name
    base_name=$(basename "$proto_file" .proto)
    SUBJECT_NAME="${base_name}-value"

    echo "Processing schema file: $proto_file"
    echo "Registering schema for subject: $SUBJECT_NAME"

    # Read the Protobuf schema file
    valueSchema=$(cat "$proto_file")

    # Escape double quotes
    escapedSchema=${valueSchema//\"/\\\"}

    # Register the schema
    response=$(curl -s -o /dev/null -w "%{http_code}" "${SCHEMA_REGISTRY_URL}/subjects/${SUBJECT_NAME}/versions" -H "Content-Type: application/vnd.schemaregistry.v1+json" --data @<(schemaPost))

    if [[ $response -eq 200 || $response -eq 201 ]]; then
      echo "Schema registration for ${SUBJECT_NAME} complete."
    else
      echo "Failed to register schema for ${SUBJECT_NAME}. HTTP response code: $response"
      exit 1
    fi

    # Compile the Protobuf schema
    protoc --python_out=${PY_OUTDIR_SCHEMAS} ${proto_file}
    if [[ $? -ne 0 ]]; then
      echo "Failed to compile Protobuf schema for ${proto_file}."
      exit 1
    fi

    echo "Protobuf schema compiled for ${proto_file}."
  fi
done

echo "All schemas registered."
