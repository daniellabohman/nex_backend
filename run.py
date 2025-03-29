from app import create_app
from app.models import db
from dotenv import load_dotenv
import os
from flask_cors import CORS
from sqlalchemy import text  # Import text for safely using raw SQL expressions

# Indlæs miljøvariabler fra .env-filen
load_dotenv()

# Opret appen via fabrikfunktionen
app = create_app()
CORS(app)

# Test databaseforbindelse
with app.app_context():
    try:
        # Use text() here for the raw SQL query
        db.session.execute(text("SELECT 1"))  # Test databaseforbindelse
        print("✅ Databaseforbindelse virker!")
    except Exception as e:
        print("❌ Fejl ved forbindelse til databasen:", e)

# Kør serveren
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)
