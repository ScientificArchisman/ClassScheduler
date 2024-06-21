def validate_data(data, required_fields):
    for entry in data:
        for field in required_fields:
            if field not in entry:
                raise ValueError(f"Missing required field '{field}' in data: {entry}")
            if not entry[field]:
                raise ValueError(f"Field '{field}' in data cannot be empty: {entry}")
