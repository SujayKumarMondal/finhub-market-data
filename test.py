import os

# Root directory
root_dir = r"D:\SUJAY\Projects\fastapi-microservice"

# Define folders and files structure
structure = {
    "": ["fastapi_server.py", ".env", "README.md"],
    "services": ["product_service.py", "order_service.py", "payment_service.py", "auth_service.py"],
    "db": ["models.py", "crud.py", "database.py"],
    "utils": ["kafka_producer.py", "kafka_consumer.py", "config.py"]
}

# Function to create folders and files
for folder, files in structure.items():
    folder_path = os.path.join(root_dir, folder)
    os.makedirs(folder_path, exist_ok=True)
    for file in files:
        file_path = os.path.join(folder_path, file)
        if not os.path.exists(file_path):
            with open(file_path, "w") as f:
                f.write("")  # create empty file
            print(f"Created file: {file_path}")
        else:
            print(f"File already exists: {file_path}")

print("\nProject structure created successfully!")
