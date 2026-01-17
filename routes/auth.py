from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required
from models import db, User
import logging

auth_bp = Blueprint('auth', __name__)
logger = logging.getLogger(__name__)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    """
    Handle user login.
    
    GET: Display login form.
    POST: Authenticate user credentials and create session.
    
    Contributor users must be approved by admin before they can log in.
    
    Returns:
        GET: Rendered login template.
        POST: Redirect to home page on success, or login page with error.
    """
    print(f"[PROGRESSIVE LOG] [auth] > login > ENTRY: method={request.method}")
    logger.info("Login page accessed")
    
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        print(f"[PROGRESSIVE LOG] [auth] > login > QUERY: Fetching user '{username}'")
        user = User.query.filter_by(username=username).first()
        
        if user and user.check_password(password):
            print(f"[PROGRESSIVE LOG] [auth] > login > LOGIC: Password check successful for '{username}'")
            if user.role == 'contributor' and not user.is_approved:
                print(f"[PROGRESSIVE LOG] [auth] > login > LOGIC: Contributor '{username}' pending approval")
                flash('Your account is pending approval by the admin.', 'warning')
                return redirect(url_for('auth.login'))
                
            print(f"[PROGRESSIVE LOG] [auth] > login > SUCCESS: User '{username}' logged in")
            logger.info(f"User '{username}' with role '{user.role}' logged in successfully")
            login_user(user)
            return redirect(url_for('public.index'))
        print(f"[PROGRESSIVE LOG] [auth] > login > ERROR: Invalid credentials for '{username}'")
        flash('Invalid username or password', 'error')
    print(f"[PROGRESSIVE LOG] [auth] > login > RENDER: Rendering login.html")
    return render_template('auth/login.html')

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    """
    Handle new user registration for barangay contributors.
    
    Creates a new contributor account that requires admin approval.
    Validates that username and email are unique.
    
    Returns:
        GET: Rendered registration template.
        POST: Redirect to login page with confirmation message.
    """
    print(f"[PROGRESSIVE LOG] [auth] > register > ENTRY: method={request.method}")
    logger.info("Registration page accessed")
    
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        barangay = request.form.get('barangay')
        
        print(f"[PROGRESSIVE LOG] [auth] > register > QUERY: Checking existence for username='{username}', email='{email}'")
        if User.query.filter_by(username=username).first():
            print(f"[PROGRESSIVE LOG] [auth] > register > ERROR: Username '{username}' already exists")
            flash('Username already exists.', 'error')
            return redirect(url_for('auth.register'))
            
        if User.query.filter_by(email=email).first():
            print(f"[PROGRESSIVE LOG] [auth] > register > ERROR: Email '{email}' already exists")
            flash('Email already exists.', 'error')
            return redirect(url_for('auth.register'))
        
        # Enforce one contributor per barangay
        print(f"[PROGRESSIVE LOG] [auth] > register > QUERY: Checking existing representative for '{barangay}'")
        existing_rep = User.query.filter_by(barangay=barangay, role='contributor', is_approved=True).first()
        if existing_rep:
            print(f"[PROGRESSIVE LOG] [auth] > register > ERROR: Representative already exists for '{barangay}'")
            flash('This Barangay already has a registered representative.', 'error')
            return redirect(url_for('auth.register'))
            
        print(f"[PROGRESSIVE LOG] [auth] > register > LOGIC: Creating new user '{username}'")
        user = User(username=username, email=email, role='contributor', barangay=barangay, is_approved=False)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        
        print(f"[PROGRESSIVE LOG] [auth] > register > SUCCESS: New user '{username}' registered for barangay '{barangay}'")
        logger.info(f"New contributor user '{username}' registered for barangay '{barangay}', awaiting approval")
        
        flash('Registration successful! Please wait for admin approval.', 'success')
        return redirect(url_for('auth.login'))
        
    print(f"[PROGRESSIVE LOG] [auth] > register > RENDER: Rendering register.html")
    return render_template('auth/register.html')

@auth_bp.route('/logout')
@login_required
def logout():
    """
    Log out the current user and end their session.
    
    Returns:
        Redirect to home page.
    """
    print(f"[PROGRESSIVE LOG] [auth] > logout > ENTRY: user='{current_user.username}'")
    logger.info("User logged out successfully")
    logout_user()
    print(f"[PROGRESSIVE LOG] [auth] > logout > REDIRECT: Redirecting to home")
    return redirect(url_for('public.index'))
