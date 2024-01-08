import os
import sys

from dotenv import load_dotenv

# Add the project root directory to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))


# Load environment variables from a file, if available
env_file_path = os.path.join(os.path.dirname(__file__), "../.env")
if os.path.exists(env_file_path):
    load_dotenv(env_file_path)
    print(".env file loaded successfully!")
else:
    print("Error: .env file not found!")

from app import app, db  # noqa: E402
from app.models.Region import Region  # noqa: E402


def init_regions():
    regions = [
        Region(name="Bordeaux"),
        Region(name="Bourgogne"),
        Region(name="Champagne"),
        Region(name="Alsace"),
        Region(name="Vallée du Rhône"),
        Region(name="Vallée de la Loire"),
        Region(name="Provence"),
        Region(name="Languedoc-Roussillon"),
        Region(name="Corse"),
        Region(name="Jura"),
    ]

    # Add regions to the database
    if Region.query.count() == 0:
        db.session.add_all(regions)
        db.session.commit()
        print("Regions added to the database")
    else:
        print("Regions already exist in the database")


if __name__ == "__main__":
    with app.app_context():
        init_regions()
