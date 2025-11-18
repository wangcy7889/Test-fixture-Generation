import yaml

def add_key_to_yaml(yaml_file_path, key, value):
    try:
        with open(yaml_file_path, 'r', encoding='utf-8') as f:
            data = yaml.safe_load(f)

        data[key] = value

        with open(yaml_file_path, 'w', encoding='utf-8') as f:
            yaml.dump(data, f, allow_unicode=True)
        return True
    except FileNotFoundError:
        raise FileNotFoundError("Error: file not found")
    except yaml.YAMLError as e:
        raise yaml.YAMLError
    except Exception as e:
        raise e
