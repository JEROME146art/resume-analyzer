# visualizer.py
# Charts, word clouds, and visualizations

import matplotlib.pyplot as plt
from wordcloud import WordCloud
import plotly.graph_objects as go
import plotly.express as px
from analyzer import categorize_skills


def create_match_gauge(score):
    """Create a beautiful gauge chart showing match score."""
    fig = go.Figure(go.Indicator(
        mode="gauge+number+delta",
        value=score,
        domain={'x': [0, 1], 'y': [0, 1]},
        title={'text': "Match Score (%)", 'font': {'size': 24}},
        delta={'reference': 70, 'increasing': {'color': "green"}},
        gauge={
            'axis': {'range': [None, 100], 'tickwidth': 1},
            'bar': {'color': "darkblue"},
            'steps': [
                {'range': [0, 40], 'color': "#ffcccc"},
                {'range': [40, 70], 'color': "#ffe0b3"},
                {'range': [70, 100], 'color': "#ccffcc"}
            ],
            'threshold': {
                'line': {'color': "red", 'width': 4},
                'thickness': 0.75,
                'value': 70
            }
        }
    ))
    fig.update_layout(height=350, margin=dict(l=20, r=20, t=50, b=20))
    return fig


def create_skills_pie_chart(matched_count, missing_count):
    """Create a pie chart of matched vs missing skills."""
    labels = ['Matched Skills', 'Missing Skills']
    values = [matched_count, missing_count]
    colors = ['#2ecc71', '#e74c3c']
    
    fig = go.Figure(data=[go.Pie(
        labels=labels,
        values=values,
        marker=dict(colors=colors),
        hole=0.4,
        textinfo='label+percent',
        textfont_size=14
    )])
    fig.update_layout(
        title="Skills Match Overview",
        height=400,
        showlegend=True
    )
    return fig


def create_category_bar_chart(skills):
    """Create a bar chart showing skills by category."""
    categorized = categorize_skills(skills)
    categories = list(categorized.keys())
    counts = [len(categorized[cat]) for cat in categories]
    
    fig = go.Figure(data=[go.Bar(
        x=categories,
        y=counts,
        marker_color='#3498db',
        text=counts,
        textposition='auto'
    )])
    fig.update_layout(
        title="Skills by Category",
        xaxis_title="Category",
        yaxis_title="Number of Skills",
        height=400,
        xaxis_tickangle=-45
    )
    return fig


def create_wordcloud(text):
    """Generate a word cloud from text."""
    wordcloud = WordCloud(
        width=800,
        height=400,
        background_color='white',
        colormap='viridis',
        max_words=100
    ).generate(text)
    
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.imshow(wordcloud, interpolation='bilinear')
    ax.axis('off')
    plt.tight_layout(pad=0)
    return fig


def create_comparison_chart(resume_data):
    """Create a bar chart comparing multiple resumes."""
    names = [r['name'] for r in resume_data]
    scores = [r['score'] for r in resume_data]
    
    colors = ['#2ecc71' if s >= 70 else '#f39c12' if s >= 40 else '#e74c3c' for s in scores]
    
    fig = go.Figure(data=[go.Bar(
        x=names,
        y=scores,
        marker_color=colors,
        text=[f"{s:.1f}%" for s in scores],
        textposition='auto'
    )])
    fig.update_layout(
        title="Resume Comparison",
        xaxis_title="Resume",
        yaxis_title="Match Score (%)",
        height=450,
        yaxis_range=[0, 100]
    )
    return fig