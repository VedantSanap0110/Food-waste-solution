import os
from flask import Flask, render_template, redirect, url_for
from dotenv import load_dotenv
from extensions import mongo
import certifi  # For SSL certificate handling

# Load environment variables
load_dotenv()

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'your-secret-key'  # Change this to a secure random key

    # Set MongoDB URI with SSL certificate
    app.config['MONGO_URI'] = os.getenv("MONGO_URI")
    app.config['MONGO_CA_FILE'] = certifi.where()  # Use certifi for SSL certificates

    # Initialize MongoDB
    mongo.init_app(app, tlsCAFile=app.config['MONGO_CA_FILE'])

    # Register blueprints
    from auth.routes import auth as auth_blueprint
    app.register_blueprint(auth_blueprint, url_prefix='/auth')

    # Create a main blueprint for other routes
    from flask import Blueprint
    main = Blueprint('main', __name__)

    @main.route('/')
    def index():
        return redirect(url_for('auth.login'))

    @main.route('/dashboard')
    def dashboard():
        return render_template('dashboard.html')

    app.register_blueprint(main)

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)