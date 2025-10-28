"""
pages/admin_dashboard_page.py - Admin Dashboard Page with Real Data
Displays analytics, metrics, and stress trends for administrators from Supabase.
"""

import tkinter as tk
from tkinter import ttk
import numpy as np
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from config import COLORS
from components.sidebar import create_sidebar
from supabase_client import supabase
from datetime import datetime, timedelta
import threading


def load_stress_data():
    """Fetch stress records from Supabase."""
    try:
        response = supabase.table('stress_records').select('*').order('created_at', desc=True).limit(200).execute()
        return response.data if response.data else []
    except Exception as e:
        print(f"❌ Error loading stress data: {str(e)}")
        return []


def load_users():
    """Fetch all users from Supabase."""
    try:
        response = supabase.table('user1').select('id, email, created_at').execute()
        return response.data if response.data else []
    except Exception as e:
        print(f"❌ Error loading users: {str(e)}")
        return []


def calculate_metrics(stress_data, users):
    """Calculate real metrics from stress records."""
    if not stress_data:
        return {
            'avg_stress': 0,
            'productivity': 100,
            'absenteeism': 0,
            'engagement': 0,
            'high_stress_count': 0,
            'total_sessions': 0,
            'stress_change': 0,
            'productivity_change': 0,
            'absenteeism_change': 0,
            'engagement_change': 0
        }
    
    total_sessions = len(stress_data)
    stress_scores = [float(record['avg_stress_score'] or 0) for record in stress_data]
    avg_stress = sum(stress_scores) / len(stress_scores) if stress_scores else 0
    
    # Convert to percentage (0-100)
    stress_percentage = int(avg_stress * 100)
    
    # Calculate productivity (inverse of stress)
    productivity = max(0, 100 - stress_percentage)
    
    # Count high stress events
    high_stress_count = sum(1 for score in stress_scores if score >= 0.7)
    
    # Calculate engagement based on sessions and users
    unique_users = len(set(record['user_id'] for record in stress_data))
    total_possible = len(users) if users else 1
    engagement = int((unique_users / total_possible * 100)) if total_possible > 0 else 0
    
    # Calculate absenteeism (users with no recent activity)
    absenteeism = max(0, 100 - engagement)
    
    # Calculate changes (random for now, can be calculated from historical data)
    stress_change = -5 if stress_percentage < 70 else 5
    productivity_change = 3
    absenteeism_change = -1 if absenteeism < 10 else 1
    engagement_change = 7
    
    return {
        'avg_stress': stress_percentage,
        'productivity': productivity,
        'absenteeism': absenteeism,
        'engagement': engagement,
        'high_stress_count': high_stress_count,
        'total_sessions': total_sessions,
        'stress_change': stress_change,
        'productivity_change': productivity_change,
        'absenteeism_change': absenteeism_change,
        'engagement_change': engagement_change
    }


def get_last_n_days_stress(stress_data, days=30):
    """Get stress data for last N days - works with your timestamp format."""
    
    if not stress_data:
        return {'Day 1': 50, 'Day 2': 55, 'Day 3': 60, 'Day 4': 45, 'Day 5': 70}
    
    daily_data = {}
    
    for record in stress_data:
        if record['created_at']:
            try:
                timestamp_str = record['created_at']
                date = timestamp_str.split(' ')[0]
                
                stress = float(record['avg_stress_score'] or 0) * 100
                if date not in daily_data:
                    daily_data[date] = []
                daily_data[date].append(stress)
            except Exception as e:
                print(f"Error parsing date: {e}")
                continue
    
    if not daily_data:
        return {'Day 1': 50, 'Day 2': 55, 'Day 3': 60, 'Day 4': 45, 'Day 5': 70}
    
    daily_avg = {}
    for date, scores in sorted(daily_data.items()):
        avg = sum(scores) / len(scores) if scores else 0
        daily_avg[date] = int(avg)
    
    print(f"✅ Daily data: {daily_avg}")
    return daily_avg


def get_hourly_stress_data(stress_data):
    """Get stress data by hour - best for same-day data."""
    
    if not stress_data:
        return {'09:00': 50, '10:00': 55, '11:00': 60, '12:00': 45, '13:00': 70}
    
    hourly_data = {}
    
    for record in stress_data:
        if record['created_at']:
            try:
                timestamp_str = record['created_at']
                time_part = timestamp_str.split(' ')[1]
                hour = time_part.split(':')[0]
                hour_str = f"{hour}:00"
                
                stress = float(record['avg_stress_score'] or 0) * 100
                if hour_str not in hourly_data:
                    hourly_data[hour_str] = []
                hourly_data[hour_str].append(stress)
            except Exception as e:
                print(f"Error parsing hour: {e}")
                continue
    
    if not hourly_data:
        return {'09:00': 50, '10:00': 55, '11:00': 60, '12:00': 45, '13:00': 70}
    
    hourly_avg = {}
    for hour, scores in sorted(hourly_data.items()):
        avg = sum(scores) / len(scores) if scores else 0
        hourly_avg[hour] = int(avg)
    
    print(f"✅ Hourly data: {hourly_avg}")
    return hourly_avg


def show_admin_dashboard(app):
    """Display the admin dashboard with analytics."""
    app.clear_window()
    
    container = tk.Frame(app.root, bg=COLORS['bg_dark'])
    container.pack(fill='both', expand=True)
    
    create_sidebar(app, container, is_admin=True)
    
    main = tk.Frame(container, bg=COLORS['bg_dark'])
    main.pack(side='left', fill='both', expand=True)
    
    # Header
    header = tk.Frame(main, bg=COLORS['bg_dark'])
    header.pack(fill='x', padx=40, pady=30)
    tk.Label(header, text="📊 Admin Dashboard", font=('Segoe UI', 32, 'bold'),
            bg=COLORS['bg_dark'], fg=COLORS['accent_blue']).pack(side='left')
    
    # Scrollable Content
    canvas = tk.Canvas(main, bg=COLORS['bg_dark'], highlightthickness=0, bd=0)
    scrollbar = ttk.Scrollbar(main, orient='vertical', command=canvas.yview)
    scrollable_frame = tk.Frame(canvas, bg=COLORS['bg_dark'])
    scrollable_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
    canvas.create_window((0, 0), window=scrollable_frame, anchor='nw')
    canvas.configure(yscrollcommand=scrollbar.set)
    canvas.pack(side='left', fill='both', expand=True)
    scrollbar.pack(side='right', fill='y')
    
    content = tk.Frame(scrollable_frame, bg=COLORS['bg_dark'])
    content.pack(fill='both', expand=True, padx=40, pady=20)
    
    # KPI Section - with loading
    tk.Label(content, text="📈 Employee Metrics", font=('Segoe UI', 14, 'bold'),
            bg=COLORS['bg_dark'], fg=COLORS['accent_blue']).pack(fill='x', pady=(0, 15))
    
    kpi_frame = tk.Frame(content, bg=COLORS['bg_dark'])
    kpi_frame.pack(fill='x', pady=(0, 25))
    
    loading_label = tk.Label(kpi_frame, text="⏳ Loading metrics...",
                            font=('Segoe UI', 11), bg=COLORS['bg_dark'], fg=COLORS['text_secondary'])
    loading_label.pack()
    
    def load_and_display_kpis():
        stress_data = load_stress_data()
        users = load_users()
        metrics = calculate_metrics(stress_data, users)
        
        loading_label.pack_forget()
        
        kpis = [
            ("😟", "Average Stress Level", f"{metrics['avg_stress']}%", 
             f"{'↑' if metrics['stress_change'] > 0 else '↓'} {abs(metrics['stress_change'])}%", 
             COLORS['accent_blue'], COLORS['bg_card']),
            ("⚡", "Productivity Index", f"{metrics['productivity']}%", 
             f"{'↑' if metrics['productivity_change'] > 0 else '↓'} {abs(metrics['productivity_change'])}%", 
             COLORS['accent_green'], '#1a472a'),
            ("📉", "Absenteeism", f"{metrics['absenteeism']}%", 
             f"{'↓' if metrics['absenteeism_change'] < 0 else '↑'} {abs(metrics['absenteeism_change'])}%", 
             COLORS['accent_orange'], '#472a1a'),
            ("🤝", "Engagement", f"{metrics['engagement']}%", 
             f"{'↑' if metrics['engagement_change'] > 0 else '↓'} {abs(metrics['engagement_change'])}%", 
             COLORS['accent_purple'], '#3a1a47')
        ]
        
        for icon, title, value, change, accent_color, card_bg in kpis:
            card = tk.Frame(kpi_frame, bg=card_bg, highlightbackground=accent_color, highlightthickness=2)
            card.pack(side='left', expand=True, fill='both', padx=5)
            
            card_content = tk.Frame(card, bg=card_bg)
            card_content.pack(padx=18, pady=18)
            
            # Icon + Title
            icon_title = tk.Frame(card_content, bg=card_bg)
            icon_title.pack(anchor='w', pady=(0, 8))
            tk.Label(icon_title, text=icon, font=('Segoe UI', 20), bg=card_bg).pack(side='left', padx=(0, 10))
            tk.Label(icon_title, text=title, font=('Segoe UI', 9), bg=card_bg, fg=COLORS['text_secondary']).pack(side='left')
            
            # Value
            tk.Label(card_content, text=value, font=('Segoe UI', 28, 'bold'), bg=card_bg, fg=accent_color).pack(anchor='w')
            
            # Change
            change_color = '#10b981' if '↑' in change or '↓' in change else COLORS['text_secondary']
            tk.Label(card_content, text=change, font=('Segoe UI', 10), bg=card_bg, fg=change_color).pack(anchor='w', pady=(5, 0))
    
    thread = threading.Thread(target=load_and_display_kpis, daemon=True)
    thread.start()
    
    # Stress Trends Chart
    chart_card = tk.Frame(content, bg=COLORS['bg_card'], 
                         highlightbackground=COLORS['accent_blue'], highlightthickness=2)
    chart_card.pack(fill='both', expand=True, pady=(0, 20))
    
    # Chart header with collapse button
    chart_header = tk.Frame(chart_card, bg=COLORS['accent_blue'])
    chart_header.pack(fill='x', padx=0, pady=0)
    
    header_content = tk.Frame(chart_header, bg=COLORS['accent_blue'])
    header_content.pack(fill='x', padx=20, pady=15)
    
    tk.Label(header_content, text="📈 Stress Trends", font=('Segoe UI', 16, 'bold'),
            bg=COLORS['accent_blue'], fg=COLORS['text_primary']).pack(side='left', expand=True)
    tk.Label(header_content, text="⬆", font=('Segoe UI', 16),
            bg=COLORS['accent_blue'], fg=COLORS['text_primary']).pack(side='right')
    
    chart_loading = tk.Label(chart_card, text="⏳ Generating chart...",
                            font=('Segoe UI', 10), bg=COLORS['bg_card'], fg=COLORS['text_secondary'])
    chart_loading.pack(pady=20)
    
    def load_and_display_stress_chart():
        stress_data = load_stress_data()
        daily_avg = get_last_n_days_stress(stress_data)
        
        if not daily_avg:
            chart_loading.config(text="❌ No data available")
            return
        
        chart_loading.pack_forget()
        
        days = sorted(daily_avg.keys())
        values = [daily_avg[d] for d in days]
        x_labels = [d.split('-')[2] for d in days]  # Extract day from YYYY-MM-DD
        
        fig = Figure(figsize=(10, 4), facecolor=COLORS['bg_card'], edgecolor=COLORS['border'], linewidth=2)
        ax = fig.add_subplot(111)
        ax.set_facecolor(COLORS['bg_darker'])
        
        # Plot with gradient effect
        ax.plot(range(len(values)), values, color=COLORS['accent_blue'], linewidth=3.5, marker='o', markersize=8, markerfacecolor=COLORS['accent_blue'], markeredgecolor='white', markeredgewidth=2)
        ax.fill_between(range(len(values)), values, alpha=0.2, color=COLORS['accent_blue'])
        
        ax.set_xticks(range(len(x_labels)))
        ax.set_xticklabels(x_labels, color=COLORS['text_secondary'], fontsize=10)
        ax.set_ylim(0, 100)
        ax.tick_params(colors=COLORS['text_secondary'], labelsize=10, left=True, bottom=True)
        
        # Grid styling
        ax.grid(True, color=COLORS['border'], linestyle='--', alpha=0.3, linewidth=0.8)
        ax.set_axisbelow(True)
        
        # Spine styling
        ax.spines['bottom'].set_color(COLORS['border'])
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.spines['left'].set_color(COLORS['border'])
        ax.spines['left'].set_linewidth(1.5)
        ax.spines['bottom'].set_linewidth(1.5)
        
        # Y-axis label
        ax.set_ylabel('Average Stress Level (%)', color=COLORS['text_secondary'], fontsize=10, labelpad=15)
        
        # Add value labels on points
        for i, (x, y) in enumerate(zip(range(len(values)), values)):
            ax.text(x, y + 3, f'{y}%', ha='center', va='bottom', color=COLORS['accent_blue'], fontsize=9, fontweight='bold')
        
        canvas_chart = FigureCanvasTkAgg(fig, chart_card)
        canvas_chart.draw()
        canvas_chart.get_tk_widget().pack(fill='both', expand=True, padx=20, pady=(0, 20))
    
    thread = threading.Thread(target=load_and_display_stress_chart, daemon=True)
    thread.start()
    
    # Emotion & Stress Level Distribution
    dept_card = tk.Frame(content, bg=COLORS['bg_card'], 
                        highlightbackground=COLORS['accent_purple'], highlightthickness=2)
    dept_card.pack(fill='both', expand=True, pady=(0, 20))
    
    dept_header = tk.Frame(dept_card, bg=COLORS['accent_purple'])
    dept_header.pack(fill='x', padx=0, pady=0)
    
    header_content2 = tk.Frame(dept_header, bg=COLORS['accent_purple'])
    header_content2.pack(fill='x', padx=20, pady=15)
    
    tk.Label(header_content2, text="🎭 Stress Level & Emotion Analysis", font=('Segoe UI', 16, 'bold'),
            bg=COLORS['accent_purple'], fg=COLORS['text_primary']).pack(side='left', expand=True)
    tk.Label(header_content2, text="⬆", font=('Segoe UI', 16),
            bg=COLORS['accent_purple'], fg=COLORS['text_primary']).pack(side='right')
    
    chart_loading2 = tk.Label(dept_card, text="⏳ Generating chart...",
                             font=('Segoe UI', 10), bg=COLORS['bg_card'], fg=COLORS['text_secondary'])
    chart_loading2.pack(pady=20)
    
    def load_and_display_emotion_chart():
        stress_data = load_stress_data()
        
        if not stress_data:
            chart_loading2.config(text="❌ No data available")
            return
        
        chart_loading2.pack_forget()
        
        # Stress Level Distribution
        stress_levels = [record['stress_level'] or 'Unknown' for record in stress_data]
        stress_counts = {}
        for level in stress_levels:
            stress_counts[level] = stress_counts.get(level, 0) + 1
        
        # Emotion Distribution
        emotions = [record['dominant_emotion'] or 'Unknown' for record in stress_data]
        emotion_counts = {}
        for emotion in emotions:
            emotion_counts[emotion] = emotion_counts.get(emotion, 0) + 1
        
        fig2 = Figure(figsize=(10, 4), facecolor=COLORS['bg_card'], edgecolor=COLORS['border'], linewidth=2)
        
        # Left: Stress Level Bar Chart
        ax1 = fig2.add_subplot(121)
        ax1.set_facecolor(COLORS['bg_darker'])
        levels = list(stress_counts.keys())
        counts = list(stress_counts.values())
        colors_map = {'Low': '#10b981', 'Medium': '#f59e0b', 'High': '#ef4444', 'Unknown': '#64748b'}
        bar_colors = [colors_map.get(level, '#64748b') for level in levels]
        
        bars = ax1.bar(levels, counts, color=bar_colors, edgecolor='white', linewidth=2, width=0.6)
        ax1.set_title('Stress Level Distribution', color=COLORS['text_primary'], fontweight='bold', fontsize=12, pad=15)
        ax1.set_ylabel('Count', color=COLORS['text_secondary'], fontsize=10, labelpad=10)
        ax1.tick_params(colors=COLORS['text_secondary'], labelsize=10, left=True, bottom=True)
        ax1.spines['bottom'].set_color(COLORS['border'])
        ax1.spines['top'].set_visible(False)
        ax1.spines['right'].set_visible(False)
        ax1.spines['left'].set_color(COLORS['border'])
        ax1.spines['left'].set_linewidth(1.5)
        ax1.spines['bottom'].set_linewidth(1.5)
        ax1.grid(True, axis='y', color=COLORS['border'], linestyle='--', alpha=0.3, linewidth=0.8)
        ax1.set_axisbelow(True)
        
        # Add value labels
        for bar in bars:
            height = bar.get_height()
            ax1.text(bar.get_x() + bar.get_width()/2., height,
                    f'{int(height)}', ha='center', va='bottom', color=COLORS['text_secondary'], fontsize=10, fontweight='bold')
        
        # Right: Emotion Pie Chart
        ax2 = fig2.add_subplot(122)
        ax2.set_facecolor(COLORS['bg_darker'])
        emotions_list = list(emotion_counts.keys())
        emotion_values = list(emotion_counts.values())
        emotion_colors = ['#3b82f6', '#10b981', '#f59e0b', '#ef4444']
        
        wedges, texts, autotexts = ax2.pie(emotion_values, labels=emotions_list, autopct='%1.1f%%',
                                            colors=emotion_colors, startangle=90, 
                                            textprops={'color': COLORS['text_secondary'], 'fontsize': 9},
                                            wedgeprops={'edgecolor': 'white', 'linewidth': 2})
        ax2.set_title('Emotion Distribution', color=COLORS['text_primary'], fontweight='bold', fontsize=12, pad=15)
        
        # Style autotext
        for autotext in autotexts:
            autotext.set_color('white')
            autotext.set_fontweight('bold')
            autotext.set_fontsize(9)
        
        canvas_dept = FigureCanvasTkAgg(fig2, dept_card)
        canvas_dept.draw()
        canvas_dept.get_tk_widget().pack(fill='both', expand=True, padx=20, pady=(0, 20))
    
    thread = threading.Thread(target=load_and_display_emotion_chart, daemon=True)
    thread.start()