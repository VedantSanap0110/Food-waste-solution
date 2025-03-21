from flask import render_template, redirect, url_for, request, flash
from werkzeug.security import generate_password_hash, check_password_hash
from . import auth
from extensions import mongo  # Import mongo from extensions.py

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = mongo.db.users.find_one({'email': email})
        
        if user and check_password_hash(user['password'], password):
            flash('Login successful!', 'success')
            return redirect(url_for('main.dashboard'))
        
        flash('Invalid login credentials. Please try again.', 'danger')
        return redirect(url_for('auth.login'))
    
    return render_template('login.html')

@auth.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')

        if password != confirm_password:
            flash('Passwords do not match!', 'danger')
            return redirect(url_for('auth.signup'))

        existing_user = mongo.db.users.find_one({'email': email})
        if existing_user:
            flash('Email already registered!', 'danger')
            return redirect(url_for('auth.signup'))

        hashed_password = generate_password_hash(password, method='pbkdf2:sha256')
        mongo.db.users.insert_one({'name': name, 'email': email, 'password': hashed_password})

        flash('Account created successfully! Please log in.', 'success')
        return redirect(url_for('auth.login'))

    return render_template('signup.html')

@auth.route('/forgot-password', methods=['GET', 'POST'])
def forgot_password():
    if request.method == 'POST':
        email = request.form.get('email')
        user = mongo.db.users.find_one({'email': email})

        if not user:
            flash('No account found with that email.', 'danger')
            return redirect(url_for('auth.forgot_password'))

        flash('Password reset instructions have been sent to your email.', 'success')
        return redirect(url_for('auth.login'))

    return render_template('forgot_password.html')

@auth.route('/reset-password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    if request.method == 'POST':
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')

        if password != confirm_password:
            flash('Passwords do not match.', 'danger')
            return redirect(url_for('auth.reset_password', token=token))

        user = mongo.db.users.find_one({'reset_token': token})
        if not user:
            flash('Invalid or expired token.', 'danger')
            return redirect(url_for('auth.forgot_password'))

        hashed_password = generate_password_hash(password, method='pbkdf2:sha256')
        mongo.db.users.update_one({'reset_token': token}, {'$set': {'password': hashed_password, 'reset_token': None}})

        flash('Password updated successfully! You can now log in.', 'success')
        return redirect(url_for('auth.login'))

    return render_template('reset_password.html')

@auth.route('/logout')
def logout():
    flash('You have been logged out.', 'info')
    return redirect(url_for('auth.login'))