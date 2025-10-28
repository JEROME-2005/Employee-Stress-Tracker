"""
pages/login_page.py - Login Page with Supabase Authentication
Handles user authentication for both admin and user roles.
"""

import tkinter as tk
from tkinter import messagebox
from config import COLORS
from supabase_client import supabase

def show_login(app):
    """Display the login page."""
    app.clear_window()
    main_frame = tk.Frame(app.root, bg=COLORS['bg_dark'])
    main_frame.pack(fill='both', expand=True)
    
    center_frame = tk.Frame(main_frame, bg=COLORS['bg_dark'])
    center_frame.place(relx=0.5, rely=0.5, anchor='center')
    
    card = tk.Frame(center_frame, bg=COLORS['bg_card'], padx=60, pady=60)
    card.pack()
    
    tk.Label(card, text="Stress Monitor", font=('Segoe UI', 36, 'bold'),
            bg=COLORS['bg_card'], fg=COLORS['text_primary']).pack(pady=(0, 15))
    tk.Label(card, text="Sign in to access your dashboard", font=('Segoe UI', 12),
            bg=COLORS['bg_card'], fg=COLORS['text_secondary']).pack(pady=(0, 35))
    
    # User type selection
    type_frame = tk.Frame(card, bg=COLORS['bg_card'])
    type_frame.pack(fill='x', pady=(0, 30))
    
    app.user_type_var = tk.StringVar(value="user")
    
    app.user_btn = tk.Button(type_frame, text="User", font=('Segoe UI', 12, 'bold'),
                        bg=COLORS['accent_blue'], fg=COLORS['text_primary'],
                        relief='flat', padx=40, pady=14, cursor='hand2', bd=0,
                        command=lambda: select_user_type(app, "user"))
    app.user_btn.pack(side='left', expand=True, fill='x', padx=(0, 8))
    
    app.admin_btn = tk.Button(type_frame, text="Admin", font=('Segoe UI', 12, 'bold'),
                         bg=COLORS['bg_input'], fg=COLORS['text_primary'],
                         relief='flat', padx=40, pady=14, cursor='hand2', bd=0,
                         command=lambda: select_user_type(app, "admin"))
    app.admin_btn.pack(side='left', expand=True, fill='x', padx=(8, 0))
    
    # Email input
    tk.Label(card, text="Email", font=('Segoe UI', 10), bg=COLORS['bg_card'],
            fg=COLORS['text_secondary'], anchor='w').pack(fill='x', pady=(0, 10))
    email_entry = tk.Entry(card, font=('Segoe UI', 12), bg=COLORS['bg_input'],
            fg=COLORS['text_primary'], relief='flat', bd=0,
            insertbackground=COLORS['text_primary'])
    email_entry.pack(fill='x', ipady=12, pady=(0, 20))
    
    # Password input
    tk.Label(card, text="Password", font=('Segoe UI', 10), bg=COLORS['bg_card'],
            fg=COLORS['text_secondary'], anchor='w').pack(fill='x', pady=(0, 10))
    password_entry = tk.Entry(card, font=('Segoe UI', 12), bg=COLORS['bg_input'],
            fg=COLORS['text_primary'], show='*', relief='flat', bd=0,
            insertbackground=COLORS['text_primary'])
    password_entry.pack(fill='x', ipady=12, pady=(0, 35))
    
    # Sign in button
    tk.Button(card, text="Sign In", font=('Segoe UI', 12, 'bold'),
             bg=COLORS['accent_blue'], fg=COLORS['text_primary'],
             relief='flat', padx=40, pady=14, cursor='hand2', bd=0,
             command=lambda: login(app, email_entry.get(), password_entry.get())).pack(fill='x')
    
    # Store references for later use
    app.email_entry = email_entry
    app.password_entry = password_entry


def select_user_type(app, user_type):
    """Handle user type selection."""
    app.user_type_var.set(user_type)
    if user_type == "user":
        app.user_btn.config(bg=COLORS['accent_blue'])
        app.admin_btn.config(bg=COLORS['bg_input'])
    else:
        app.admin_btn.config(bg=COLORS['accent_blue'])
        app.user_btn.config(bg=COLORS['bg_input'])


def login(app, email, password):
    """Authenticate user with Supabase and route to appropriate dashboard."""
    
    # Validate inputs
    if not email or not password:
        messagebox.showerror("Error", "Please enter email and password")
        return
    
    user_type = app.user_type_var.get()
    
    try:
        if user_type == "admin":
            # Query admin table
            response = supabase.table('admins').select('*').eq('email', email).execute()
            
            if response.data and len(response.data) > 0:
                admin = response.data[0]
                # Verify password (plain text comparison)
                if admin['password'] == password:
                    # Login successful
                    app.current_user = admin
                    app.current_user_type = "admin"
                    from pages.admin_dashboard_page import show_admin_dashboard
                    show_admin_dashboard(app)
                else:
                    messagebox.showerror("Error", "Invalid email or password")
            else:
                messagebox.showerror("Error", "Admin not found")
        
        else:  # user
            # Query user1 table
            response = supabase.table('user1').select('*').eq('email', email).execute()
            
            if response.data and len(response.data) > 0:
                user = response.data[0]
                # Verify password (plain text comparison)
                if user['password'] == password:
                    # Login successful
                    app.current_user = user
                    app.current_user_type = "user"
                    from pages.user_dashboard_page import show_user_dashboard
                    show_user_dashboard(app)
                else:
                    messagebox.showerror("Error", "Invalid email or password")
            else:
                messagebox.showerror("Error", "User not found")
    
    except Exception as e:
        messagebox.showerror("Error", f"Authentication failed: {str(e)}")