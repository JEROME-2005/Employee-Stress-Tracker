# pages/admin_panel_page.py
import tkinter as tk
from tkinter import messagebox
from datetime import datetime
from config import COLORS
from supabase_client import supabase
from components.sidebar import create_sidebar


class ScrollableFrame(tk.Frame):
    """Reusable scrollable frame with modern style."""
    def __init__(self, container, *args, **kwargs):
        super().__init__(container, *args, **kwargs)
        canvas = tk.Canvas(self, bg=COLORS['bg_dark'], highlightthickness=0)
        scrollbar = tk.Scrollbar(self, orient="vertical", command=canvas.yview)
        self.scrollable_frame = tk.Frame(canvas, bg=COLORS['bg_dark'])

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")


def show_admin_panel(app):
    app.clear_window()

    container = tk.Frame(app.root, bg=COLORS['bg_dark'])
    container.pack(fill='both', expand=True)

    create_sidebar(app, container, is_admin=True)

    main = tk.Frame(container, bg=COLORS['bg_dark'])
    main.pack(side='left', fill='both', expand=True, padx=50, pady=30)  # Increased padx from 30 to 50

    # Header
    header = tk.Frame(main, bg=COLORS['bg_dark'])
    header.pack(fill='x', pady=(0, 20))

    tk.Label(header, text="User Management", font=('Segoe UI', 24, 'bold'),
             bg=COLORS['bg_dark'], fg=COLORS['text_primary']).pack(side='left')

    # Search & Add User
    search_frame = tk.Frame(header, bg=COLORS['bg_dark'])
    search_frame.pack(side='right')

    search_var = tk.StringVar()
    search_entry = tk.Entry(
        search_frame, font=('Segoe UI', 11), bg=COLORS['bg_input'],
        fg=COLORS['text_secondary'], relief='flat', width=45, bd=0,  # Increased width from 35 to 45
        textvariable=search_var, insertbackground=COLORS['text_secondary']
    )
    search_entry.pack(side='left', ipady=8, padx=(0, 12))

    tk.Button(search_frame, text="Add User", font=('Segoe UI', 11, 'bold'),
              bg=COLORS['accent_blue'], fg='white', relief='flat',
              padx=20, pady=8, cursor='hand2', bd=0,
              command=lambda: add_user_popup(app)).pack(side='left')

    # Scrollable table content
    content = ScrollableFrame(main)
    content.pack(fill='both', expand=True)

    table = tk.Frame(content.scrollable_frame, bg=COLORS['bg_card'],
                     highlightbackground=COLORS['border'], highlightthickness=1)
    table.pack(fill='x', expand=True)

    # Table Header - Increased width values
    headers = ["User", "Role", "Status", "Stress Events", "Last Active", "Actions"]
    widths = [30, 15, 15, 15, 20, 12]  # Increased all width values

    header_row = tk.Frame(table, bg=COLORS['bg_input'])
    header_row.pack(fill='x')

    for i, h in enumerate(headers):
        lbl = tk.Label(header_row, text=h, font=('Segoe UI', 10, 'bold'),
                       bg=COLORS['bg_input'], fg=COLORS['text_secondary'],
                       anchor='w')
        lbl.pack(side='left', fill='x', expand=True, ipadx=widths[i], padx=10, pady=10)

    # Fetch Users
    response = supabase.table('user1').select('*').execute()
    users = response.data if response.data else []

    def refresh_table(*args):
        for widget in table.winfo_children():
            if widget != header_row:
                widget.destroy()
        filtered = [
            u for u in users if search_var.get().lower() in u['first_name'].lower()
            or search_var.get().lower() in u['last_name'].lower()
            or search_var.get().lower() in u['email'].lower()
        ]
        for user in filtered:
            create_user_row(app, table, user)

    search_var.trace_add("write", refresh_table)
    refresh_table()


def create_user_row(app, parent, user):
    # Increased width by adding more horizontal padding
    row = tk.Frame(parent, bg=COLORS['bg_card'])
    row.pack(fill='x', pady=1, padx=10)  # Added horizontal padding
    
    user_frame = tk.Frame(row, bg=COLORS['bg_card'])
    user_frame.pack(side='left', fill='x', expand=True, padx=20, pady=12)  # Increased padding
    
    avatar = tk.Label(user_frame, text="👤", bg=COLORS['bg_card'], font=('Segoe UI Emoji', 16))
    avatar.pack(side='left', padx=(0, 15))  # Increased from 10 to 15
    
    info = tk.Frame(user_frame, bg=COLORS['bg_card'])
    info.pack(side='left', fill='x', expand=True)
    
    tk.Label(info, text=f"{user['first_name']} {user['last_name']}",
             font=('Segoe UI', 11, 'bold'), bg=COLORS['bg_card'],
             fg=COLORS['text_primary']).pack(anchor='w')
    tk.Label(info, text=user['email'], font=('Segoe UI', 9),
             bg=COLORS['bg_card'], fg=COLORS['text_secondary']).pack(anchor='w')

    role_color = COLORS['accent_purple'] if user['role'] == 'Admin' else COLORS['accent_blue']
    tk.Label(row, text=user['role'], font=('Segoe UI', 9), bg=role_color, fg='white',
             padx=15, pady=3).pack(side='left', padx=30)  # Increased padx from 20 to 30

    status_color = COLORS['accent_green'] if user['status'] == 'Active' else '#64748b'
    tk.Label(row, text=user['status'], font=('Segoe UI', 9), bg=status_color, fg='white',
             padx=15, pady=3).pack(side='left', padx=30)  # Increased padx from 20 to 30

    tk.Label(row, text=str(user.get('stress_events', 0)), font=('Segoe UI', 11),
             bg=COLORS['bg_card'], fg=COLORS['text_primary']).pack(side='left', padx=50)  # Increased from 40 to 50

    last_active = user.get('last_active', 'Never')
    tk.Label(row, text=last_active, font=('Segoe UI', 11),
             bg=COLORS['bg_card'], fg=COLORS['text_primary']).pack(side='left', padx=50)  # Increased from 40 to 50

    actions = tk.Frame(row, bg=COLORS['bg_card'])
    actions.pack(side='right', padx=30)  # Increased from 20 to 30
    tk.Button(actions, text="✏️", font=('Segoe UI', 10), bg=COLORS['bg_input'],
              fg='white', relief='flat', cursor='hand2', width=4,
              command=lambda: edit_user_popup(app, user)).pack(side='left', padx=3)
    tk.Button(actions, text="🗑️", font=('Segoe UI', 10), bg=COLORS['bg_input'],
              fg='white', relief='flat', cursor='hand2', width=4,
              command=lambda: handle_delete_user(app, user['id'])).pack(side='left', padx=3)


# ---------- POPUPS WITH SCROLL (COMPACT FIXED VERSION) ----------

def create_scrollable_popup(title, fields, app, user_data=None, on_save=None):
    window = tk.Toplevel(app.root)
    window.title(title)
    window.configure(bg=COLORS['bg_dark'])
    window.resizable(False, False)

    # Use minimal width + auto height
    content_frame = tk.Frame(window, bg=COLORS['bg_dark'])
    content_frame.pack(fill='both', expand=True, padx=20, pady=20)

    tk.Label(content_frame, text=title, font=('Segoe UI', 18, 'bold'),
             bg=COLORS['bg_dark'], fg=COLORS['text_primary']).pack(anchor='w', pady=(5, 15))

    entries = {}
    for f in fields:
        frame = tk.Frame(content_frame, bg=COLORS['bg_dark'])
        frame.pack(fill='x', pady=6)
        tk.Label(frame, text=f, font=('Segoe UI', 11),
                 bg=COLORS['bg_dark'], fg=COLORS['text_primary']).pack(anchor='w')
        e = tk.Entry(frame, font=('Segoe UI', 11),
                     bg=COLORS['bg_input'], fg=COLORS['text_primary'],
                     relief='flat', bd=0)
        e.pack(fill='x', ipady=7)
        if user_data and f in user_data:
            e.insert(0, user_data[f])
        entries[f] = e

    btn = tk.Button(content_frame, text="Save", font=('Segoe UI', 11, 'bold'),
                    bg=COLORS['accent_green'], fg='white',
                    relief='flat', padx=25, pady=10, cursor='hand2',
                    bd=0, command=lambda: on_save(entries, window))
    btn.pack(anchor='e', pady=(15, 5))

    # Auto-size to content
    window.update_idletasks()
    window.geometry(f"{content_frame.winfo_reqwidth()+40}x{content_frame.winfo_reqheight()+40}")
    window.transient(app.root)
    window.grab_set()
    window.focus_force()

    return entries


def add_user_popup(app):
    fields = ['first_name', 'last_name', 'email', 'phone', 'password', 'role', 'department']

    def save(entries, window):
        data = {k: v.get() for k, v in entries.items()}
        data.update({'status': 'Active', 'created_at': datetime.now().isoformat()})

        if not data['first_name'] or not data['last_name'] or not data['email']:
            messagebox.showerror("Error", "Please fill in all required fields")
            return

        try:
            supabase.table('user1').insert(data).execute()
            messagebox.showinfo("Success", "User added successfully!")
            window.destroy()
            show_admin_panel(app)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to add user: {str(e)}")

    create_scrollable_popup("Add New User", fields, app, on_save=save)


def edit_user_popup(app, user):
    fields = ['first_name', 'last_name', 'email', 'phone', 'password', 'role', 'department', 'status']

    def save(entries, window):
        data = {k: v.get() for k, v in entries.items()}
        data.update({'updated_at': datetime.now().isoformat()})
        if not data['first_name'] or not data['last_name'] or not data['email']:
            messagebox.showerror("Error", "Please fill in all required fields")
            return
        try:
            supabase.table('user1').update(data).eq('id', user['id']).execute()
            messagebox.showinfo("Success", "User updated successfully!")
            window.destroy()
            show_admin_panel(app)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to update user: {str(e)}")

    create_scrollable_popup("Edit User", fields, app, user, on_save=save)


def handle_delete_user(app, user_id):
    if messagebox.askyesno("Confirm Delete", "Are you sure you want to delete this user?"):
        try:
            supabase.table('user1').delete().eq('id', user_id).execute()
            messagebox.showinfo("Deleted", "User deleted successfully.")
            show_admin_panel(app)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to delete user: {str(e)}")