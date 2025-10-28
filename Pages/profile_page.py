"""
pages/profile_page.py - User Profile Page
Displays and allows editing of user profile information using Supabase data.
"""

import tkinter as tk
from tkinter import messagebox
from config import COLORS
from components.sidebar import create_sidebar
from components.avatar import create_avatar_with_badge
from supabase_client import supabase


def show_profile(app, is_admin):
    """Display the profile page."""
    app.clear_window()
    
    # Fetch user data from Supabase
    user_data = fetch_user_data(app, is_admin)
    if not user_data:
        messagebox.showerror("Error", "Failed to load user data")
        return
    
    container = tk.Frame(app.root, bg=COLORS['bg_dark'])
    container.pack(fill='both', expand=True)
    
    create_sidebar(app, container, is_admin=is_admin)
    
    main = tk.Frame(container, bg=COLORS['bg_dark'])
    main.pack(side='left', fill='both', expand=True)
    
    # Header
    header = tk.Frame(main, bg=COLORS['bg_dark'])
    header.pack(fill='x', padx=40, pady=30)
    tk.Label(header, text="Stress Monitor", font=('Segoe UI', 20, 'bold'),
            bg=COLORS['bg_dark'], fg=COLORS['text_primary']).pack(side='left')
    
    icon_frame = tk.Frame(header, bg=COLORS['bg_dark'])
    icon_frame.pack(side='right')
    tk.Label(icon_frame, text="⚙", font=('Segoe UI', 24),
            bg=COLORS['bg_dark'], fg=COLORS['text_secondary']).pack(side='left', padx=10)
    
    user_icon_frame = tk.Frame(icon_frame, bg=COLORS['bg_dark'])
    user_icon_frame.pack(side='left', padx=10)
    user_canvas = tk.Canvas(user_icon_frame, width=40, height=40,
                           bg=COLORS['bg_dark'], highlightthickness=0)
    user_canvas.pack()
    user_canvas.create_oval(8, 5, 28, 25, fill='#60a5fa', outline='')
    user_canvas.create_arc(5, 18, 35, 48, start=0, extent=180, fill='#3b82f6', outline='')
    user_canvas.create_oval(28, 5, 38, 15, fill='#3b82f6', outline='')
    user_canvas.create_oval(30, 7, 36, 13, fill='#60a5fa', outline='')
    
    # Page Title
    tk.Label(main, text="Profile", font=('Segoe UI', 32, 'bold'),
            bg=COLORS['bg_dark'], fg=COLORS['text_primary']).pack(anchor='w', padx=40, pady=(0, 20))
    
    # Content
    content = tk.Frame(main, bg=COLORS['bg_dark'])
    content.pack(fill='both', expand=True, padx=40, pady=0)
    
    grid = tk.Frame(content, bg=COLORS['bg_dark'])
    grid.pack(fill='both', expand=True)
    
    # Left: Profile Card
    profile_card = tk.Frame(grid, bg=COLORS['bg_card'],
                           highlightbackground=COLORS['border'], highlightthickness=0)
    profile_card.pack(side='left', fill='y', padx=(0, 20))
    profile_card.pack_propagate(False)
    profile_card.config(width=360)
    
    create_avatar_with_badge(profile_card, is_admin=is_admin)
    
    # Get name from user data
    if is_admin:
        user_name = user_data.get('name', 'Admin')
    else:
        first_name = user_data.get('first_name', '')
        last_name = user_data.get('last_name', '')
        user_name = f"{first_name} {last_name}".strip() or "User"
    
    tk.Label(profile_card, text=user_name, font=('Segoe UI', 24, 'bold'),
            bg=COLORS['bg_card'], fg=COLORS['text_primary']).pack()
    tk.Label(profile_card, text="User", font=('Segoe UI', 16),
            bg=COLORS['bg_card'], fg=COLORS['text_primary']).pack()
    
    user_email = user_data.get('email', 'N/A')
    tk.Label(profile_card, text=user_email, font=('Segoe UI', 11),
            bg=COLORS['bg_card'], fg=COLORS['text_secondary']).pack(pady=8)
    
    badge_text = "Admin User" if is_admin else "Standard User"
    badge_bg = "#4c1d95" if is_admin else "#1e40af"
    tk.Label(profile_card, text=badge_text, font=('Segoe UI', 10),
            bg=badge_bg, fg=COLORS['text_primary'], padx=20, pady=8).pack(pady=15)
    
    menu_frame = tk.Frame(profile_card, bg=COLORS['bg_card'])
    menu_frame.pack(fill='x', padx=20, pady=20)
    tk.Button(menu_frame, text="Personal Information", font=('Segoe UI', 11),
             bg=COLORS['bg_input'], fg=COLORS['text_primary'],
             relief='flat', cursor='hand2', bd=0, height=2).pack(fill='x', pady=5)
    tk.Button(menu_frame, text="🔑  Security", font=('Segoe UI', 11),
             bg=COLORS['bg_input'], fg=COLORS['text_primary'],
             relief='flat', cursor='hand2', bd=0, height=2, anchor='w', padx=15).pack(fill='x', pady=5)
    
    # Right: Information Card
    info_card = tk.Frame(grid, bg=COLORS['bg_card'],
                        highlightbackground=COLORS['border'], highlightthickness=0)
    info_card.pack(side='left', fill='both', expand=True)
    
    tk.Label(info_card, text="Personal Information", font=('Segoe UI', 20, 'bold'),
            bg=COLORS['bg_card'], fg=COLORS['text_primary']).pack(pady=25, padx=30, anchor='w')
    
    form_frame = tk.Frame(info_card, bg=COLORS['bg_card'])
    form_frame.pack(fill='both', expand=True, padx=30, pady=(0, 30))
    
    # Row 1: Name and Email
    row1 = tk.Frame(form_frame, bg=COLORS['bg_card'])
    row1.pack(fill='x', pady=(0, 15))
    
    name_frame = tk.Frame(row1, bg=COLORS['bg_card'])
    name_frame.pack(side='left', fill='both', expand=True, padx=(0, 10))
    tk.Label(name_frame, text="Full Name", font=('Segoe UI', 10),
            bg=COLORS['bg_card'], fg=COLORS['text_secondary']).pack(anchor='w', pady=(0, 8))
    name_entry = tk.Entry(name_frame, font=('Segoe UI', 12), bg=COLORS['bg_input'],
                         fg=COLORS['text_primary'], relief='flat', bd=0)
    name_entry.insert(0, user_name)
    name_entry.pack(fill='x', ipady=12)
    
    email_frame = tk.Frame(row1, bg=COLORS['bg_card'])
    email_frame.pack(side='left', fill='both', expand=True, padx=(10, 0))
    tk.Label(email_frame, text="Email Address", font=('Segoe UI', 10),
            bg=COLORS['bg_card'], fg=COLORS['text_secondary']).pack(anchor='w', pady=(0, 8))
    email_entry = tk.Entry(email_frame, font=('Segoe UI', 12), bg=COLORS['bg_input'],
                          fg=COLORS['text_primary'], relief='flat', bd=0)
    email_entry.insert(0, user_email)
    email_entry.pack(fill='x', ipady=12)
    
    # Bio
    tk.Label(form_frame, text="Bio", font=('Segoe UI', 10),
            bg=COLORS['bg_card'], fg=COLORS['text_secondary']).pack(anchor='w', pady=(0, 8))
    bio_text = tk.Text(form_frame, font=('Segoe UI', 12), bg=COLORS['bg_input'],
                      fg=COLORS['text_primary'], relief='flat', height=4, bd=0, wrap='word')
    bio_content = user_data.get('bio', '')
    if bio_content:
        bio_text.insert('1.0', bio_content)
    bio_text.pack(fill='x', pady=(0, 15))
    
    # Row 2: Phone and Language
    row2 = tk.Frame(form_frame, bg=COLORS['bg_card'])
    row2.pack(fill='x', pady=(0, 15))
    
    phone_frame = tk.Frame(row2, bg=COLORS['bg_card'])
    phone_frame.pack(side='left', fill='both', expand=True, padx=(0, 10))
    tk.Label(phone_frame, text="Phone Number", font=('Segoe UI', 10),
            bg=COLORS['bg_card'], fg=COLORS['text_secondary']).pack(anchor='w', pady=(0, 8))
    phone_entry = tk.Entry(phone_frame, font=('Segoe UI', 12), bg=COLORS['bg_input'],
                          fg=COLORS['text_primary'], relief='flat', bd=0)
    phone_number = user_data.get('number', '') if is_admin else user_data.get('phone', '')
    phone_entry.insert(0, phone_number)
    phone_entry.pack(fill='x', ipady=12)
    
    lang_frame = tk.Frame(row2, bg=COLORS['bg_card'])
    lang_frame.pack(side='left', fill='both', expand=True, padx=(10, 0))
    tk.Label(lang_frame, text="Language", font=('Segoe UI', 10),
            bg=COLORS['bg_card'], fg=COLORS['text_secondary']).pack(anchor='w', pady=(0, 8))
    lang_select = tk.Frame(lang_frame, bg=COLORS['bg_input'])
    lang_select.pack(fill='x')
    language = user_data.get('language', 'English')
    tk.Label(lang_select, text=language, font=('Segoe UI', 12),
            bg=COLORS['bg_input'], fg=COLORS['text_primary'],
            anchor='w').pack(side='left', fill='both', expand=True, padx=12, ipady=12)
    tk.Label(lang_select, text="▼", font=('Segoe UI', 10),
            bg=COLORS['bg_input'], fg=COLORS['text_secondary']).pack(side='right', padx=12)
    
    # Timezone
    tk.Label(form_frame, text="Timezone", font=('Segoe UI', 10),
            bg=COLORS['bg_card'], fg=COLORS['text_secondary']).pack(anchor='w', pady=(0, 8))
    tz_select = tk.Frame(form_frame, bg=COLORS['bg_input'])
    tz_select.pack(fill='x', pady=(0, 25))
    tk.Label(tz_select, text="Sri Lanka (GMT+5:30)", font=('Segoe UI', 12),
            bg=COLORS['bg_input'], fg=COLORS['text_primary'],
            anchor='w').pack(side='left', fill='both', expand=True, padx=12, ipady=12)
    tk.Label(tz_select, text="▼", font=('Segoe UI', 10),
            bg=COLORS['bg_input'], fg=COLORS['text_secondary']).pack(side='right', padx=12)
    
    # Save Button
    save_btn = tk.Button(form_frame, text="💾  Save Changes", font=('Segoe UI', 12, 'bold'),
                        bg=COLORS['accent_blue'], fg=COLORS['text_primary'],
                        relief='flat', padx=30, pady=14, cursor='hand2', bd=0,
                        command=lambda: save_profile_changes(app, is_admin, user_data,
                                                            name_entry, email_entry,
                                                            bio_text, phone_entry))
    save_btn.pack(anchor='e')


def fetch_user_data(app, is_admin):
    """Fetch user data from Supabase based on current user."""
    try:
        if is_admin:
            user_id = app.current_user['id']
            response = supabase.table('admins').select('*').eq('id', user_id).execute()
        else:
            user_id = app.current_user['id']
            response = supabase.table('user1').select('*').eq('id', user_id).execute()
        
        if response.data and len(response.data) > 0:
            return response.data[0]
        return None
    except Exception as e:
        print(f"Error fetching user data: {str(e)}")
        return None


def save_profile_changes(app, is_admin, user_data, name_entry, email_entry, bio_text, phone_entry):
    """Save profile changes to Supabase."""
    try:
        user_id = user_data['id']
        
        if is_admin:
            # Update admin table
            update_data = {
                'name': name_entry.get(),
                'email': email_entry.get(),
                'bio': bio_text.get('1.0', 'end-1c'),
                'number': phone_entry.get()
            }
            supabase.table('admins').update(update_data).eq('id', user_id).execute()
        else:
            # Update user1 table
            name_parts = name_entry.get().split(' ', 1)
            first_name = name_parts[0] if len(name_parts) > 0 else ''
            last_name = name_parts[1] if len(name_parts) > 1 else ''
            
            update_data = {
                'first_name': first_name,
                'last_name': last_name,
                'email': email_entry.get(),
                'phone': phone_entry.get()
            }
            supabase.table('user1').update(update_data).eq('id', user_id).execute()
        
        messagebox.showinfo("Success", "Profile updated successfully!")
        app.current_user = fetch_user_data(app, is_admin)
    except Exception as e:
        messagebox.showerror("Error", f"Failed to save changes: {str(e)}")