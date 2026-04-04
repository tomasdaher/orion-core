def run(data):
    print("Data Formatter Tool Running")

    # ejemplo simple de formateo
    if isinstance(data, dict):
        return {k: str(v).strip() for k, v in data.items()}

    return data