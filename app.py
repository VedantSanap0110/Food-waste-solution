from flask import Flask, render_template, redirect, url_for

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'your-secret-key'  # Change this to a secure random key
    
    # Register blueprints
    from auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint, url_prefix='/auth')
    
    # Create a main blueprint for other routes
    from flask import Blueprint
    main = Blueprint('main', __name__)
    
    @main.route('/')
    def index():
        return redirect(url_for('auth.login'))
    
    @main.route('/dashboard')
    def dashboard():
        # You would add authentication check here
        return render_template('dashboard.html')
    
    app.register_blueprint(main)
    
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)