import yaml


class YamlConfigReader:
    def __init__(self, yaml_file_path):
        self.yaml_file_path = yaml_file_path
        self.config = self._load_yaml()

    def _load_yaml(self):
        with open(self.yaml_file_path, "r") as file:
            return yaml.safe_load(file)

    def get_prompt_template(self, template_name):
        return self.config.get("prompt_templates", {}).get(template_name, None)

    def get(self, variable_name):
        return self.config.get(variable_name, None)
