def run(input_data=None):

    print("🤖 Hello from Orion Tool")

    if input_data:
        print(f"Received input: {input_data}")

    return {
        "status": "success",
        "message": "Hello tool executed",
        "input": input_data
    }