from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required
from models import db, User

auth_bp = Blueprint('auth', __name__)

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
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = User.query.filter_by(username=username).first()
        
        if user and user.check_password(password):
            if user.role == 'contributor' and not user.is_approved:
                flash('Your account is pending approval by the admin.', 'warning')
                return redirect(url_for('auth.login'))
                
            login_user(user)
            return redirect(url_for('public.index'))
        flash('Invalid username or password', 'error')
    return render_template('login.html')

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
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        barangay = request.form.get('barangay')
        
        if User.query.filter_by(username=username).first():
            flash('Username already exists.', 'error')
            return redirect(url_for('auth.register'))
            
        if User.query.filter_by(email=email).first():
            flash('Email already exists.', 'error')
            return redirect(url_for('auth.register'))
        
        # Enforce one contributor per barangay
        existing_rep = User.query.filter_by(barangay=barangay, role='contributor', is_approved=True).first()
        if existing_rep:
            flash('This Barangay already has a registered representative.', 'error')
            return redirect(url_for('auth.register'))
            
        user = User(username=username, email=email, role='contributor', barangay=barangay, is_approved=False)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        
        flash('Registration successful! Please wait for admin approval.', 'success')
        return redirect(url_for('auth.login'))
        
    return render_template('register.html')

@auth_bp.route('/logout')
@login_required
def logout():
    """
    Log out the current user and end their session.
    
    Returns:
        Redirect to home page.
    """
    logout_user()
    return redirect(url_for('public.index'))
