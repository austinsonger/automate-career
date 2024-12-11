import yaml

def load_applicant_data(filepath):
    """Load applicant data from a YAML file."""
    with open(filepath, 'r') as file:
        data = yaml.safe_load(file)
    return data
