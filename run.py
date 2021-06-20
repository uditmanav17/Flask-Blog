from flaskblog import create_app
import os


app = create_app()
port = os.environ.get('PORT') or 5000

if __name__ == "__main__":
    app.run()
