import os

from dotenv import load_dotenv

# Load environment variables from a file, if available
env_file_path = os.path.join(os.path.dirname(__file__), ".env")
if os.path.exists(env_file_path):
    load_dotenv(env_file_path)
    print(".env file loaded successfully!")
else:
    print("Error: .env file not found!")

if __name__ == "__main__":
    from app import app

    # Use environment variables or default values for Flask run options
    debug_mode = os.environ.get("FLASK_DEBUG", True)
    port = int(os.environ.get("FLASK_PORT", 5010))

    app.run(debug=debug_mode, port=port)
