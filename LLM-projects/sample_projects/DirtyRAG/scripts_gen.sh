#!/bin/bash
targets=(
    "deactivate_venv"
    "install_requirements"
    "activate_venv"
    "create_env"
    "check_env"
    "update_pip"
    "save_deps"
)

alias_dir="./scripts"
mkdir -p "$alias_dir"
for target in "${targets[@]}"; do
    alias_file="$alias_dir/$target"
    echo "#!/bin/bash" > "$alias_file"
    echo "make $target" >> "$alias_file"
    chmod +x "$alias_file"
    echo "Created executable alias: $alias_file"
done
echo "All aliases created in '$alias_dir'."
