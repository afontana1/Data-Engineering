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
    curl -s "${SCHEMA_REGISTRY_URL}/subjects/${SUBJECT_NAME}/versions" -H "Content-Type: application/vnd.schemaregistry.v1+json" --data @<(schemaPost)

    echo "Schema registration for ${SUBJECT_NAME} complete."

    # Compile the Protobuf schema
    protoc --python_out=${PY_OUTDIR_SCHEMAS} ${proto_file}

    echo "Protobuf schema compiled."
    
  fi
done

echo "All schemas registered."




# function schemaPost {
#   # Use heredoc to strip out newlines, needed so that post is pure JSON
#     cat <<EOF
# {
#   "schemaType": "PROTOBUF",
#   "schema": "${escapedSchema}"
# }
# EOF
# }

# valueSchema="`cat ./schemas/todo.proto`"
# escapedSchema=${valueSchema//\"/\\\"} # escape double quotes

# curl -s "http://localhost:8081/subjects/todo-value/versions" -H "Content-Type: application/vnd.schemaregistry.v1+json" --data @<(cat <<EOF
#   $(schemaPost)
# EOF
# )