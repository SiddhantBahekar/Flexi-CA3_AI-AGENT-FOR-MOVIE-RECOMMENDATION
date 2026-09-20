"""
AI Agent for Movie Recommendation - Gradio GUI Application
Symbiosis Flexi Credit CA3 Mini Project
Includes Real-Time Data Radar & Multi-Model LLM Agent (Groq / Gemini / Local)
"""

import os
import sys
import pandas as pd
import gradio as gr

# Load environment variables from .env
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

# Ensure src in path
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from src.recommender import MovieRecommender
from src.agent import MovieAgent, fetch_live_poster
from src.realtime_fetcher import (
    search_live_movie_data,
    get_trending_movies_live,
    detect_streaming_platforms
)
from src.visualizer import (
    plot_genre_distribution,
    plot_rating_vs_year,
    plot_mood_distribution,
    plot_top_directors
)

# Initialize engines
recommender = MovieRecommender(dataset_path="dataset/movies.csv")
agent = MovieAgent(recommender)

# --- Helper: Render Movie Cards in HTML ---
def render_movie_cards(movies):
    if not movies:
        return """
        <div style="text-align: center; padding: 36px 20px; color: #cbd5e1; background: rgba(15, 23, 42, 0.7); border: 1px dashed #475569; border-radius: 14px;">
            <p style="font-size: 1.05rem; font-weight: 600; margin: 0; color: #f1f5f9;">No movies matched your current query or filters.</p>
            <p style="font-size: 0.85rem; color: #94a3b8; margin: 6px 0 0 0;">Try relaxing your rating or genre filters to discover more titles.</p>
        </div>
        """

    cards_html = ['<div style="display: grid; grid-template-columns: repeat(auto-fill, minmax(320px, 1fr)); gap: 16px; margin-top: 12px;">']

    for m in movies:
        title = m.get("title", "Unknown Title")
        year = m.get("year", "")
        rating = m.get("rating", "N/A")
        director = m.get("director", "Unknown")
        genres = [g.strip() for g in str(m.get("genre", "")).split(",") if g.strip()]
        moods = [md.strip() for md in str(m.get("mood_tags", "")).split(",") if md.strip()]
        cast = m.get("cast", "")
        overview = m.get("overview", "")
        poster = m.get("poster_url", "")
        if not poster or "image.tmdb.org" in str(poster):
            poster = fetch_live_poster(title, year)
        sim_score = m.get("similarity_score")
        explanation = m.get("explanation", "")

        lang = m.get("language", "")
        lang_badge = f'<span style="background: rgba(245, 158, 11, 0.20); color: #fbbf24; border: 1px solid rgba(245, 158, 11, 0.55); padding: 2px 8px; border-radius: 9999px; font-size: 0.72rem; font-weight: 700; margin-right: 5px; display: inline-block; margin-bottom: 4px;">🌐 {lang}</span>' if lang else ""

        genre_badges = "".join([f'<span style="background: rgba(56, 189, 248, 0.20); color: #38bdf8; border: 1px solid rgba(56, 189, 248, 0.5); padding: 3px 9px; border-radius: 9999px; font-size: 0.74rem; font-weight: 700; margin-right: 5px; display: inline-block; margin-bottom: 4px;">{g}</span>' for g in genres[:3]])
        mood_badges = "".join([f'<span style="background: rgba(168, 85, 247, 0.20); color: #d8b4fe; border: 1px solid rgba(168, 85, 247, 0.5); padding: 3px 9px; border-radius: 9999px; font-size: 0.74rem; font-weight: 700; margin-right: 5px; display: inline-block; margin-bottom: 4px;">{md}</span>' for md in moods[:2]])

        streaming_list = m.get("streaming_platforms")
        if not streaming_list:
            streaming_list = detect_streaming_platforms(title, overview)
        streaming_badges = "".join([f'<span style="background: rgba(16, 185, 129, 0.22); color: #6ee7b7; border: 1px solid rgba(16, 185, 129, 0.55); padding: 2px 8px; border-radius: 6px; font-size: 0.72rem; font-weight: 700; margin-right: 4px; display: inline-block; margin-bottom: 4px;">📺 {s}</span>' for s in streaming_list[:2]])

        sim_badge = ""
        if sim_score is not None:
            sim_badge = f'<div class="match-badge" style="position: absolute; top: 10px; right: 10px; background: linear-gradient(135deg, #0284c7, #6366f1); color: #ffffff; padding: 4px 10px; border-radius: 8px; font-size: 0.78rem; font-weight: 800; box-shadow: 0 4px 12px rgba(99, 102, 241, 0.5); border: 1px solid rgba(255,255,255,0.3);">{sim_score}% Match</div>'

        card = f"""
        <div class="movie-card">
            {sim_badge}
            <div style="flex-shrink: 0; overflow: hidden; border-radius: 8px; box-shadow: 0 4px 12px rgba(0,0,0,0.6); border: 1px solid #334155;">
                <img src="{poster}" alt="{title}" style="width: 95px; height: 140px; object-fit: cover; background-color: #0f172a;" onerror="this.src='https://images.unsplash.com/photo-1489599849927-2ee91cede3ba?w=200';"/>
            </div>
            <div style="flex: 1; display: flex; flex-direction: column; justify-content: space-between;">
                <div>
                    <div style="display: flex; align-items: baseline; gap: 6px; flex-wrap: wrap;">
                        <h4 style="margin: 0; color: #ffffff; font-size: 1.05rem; font-weight: 800; letter-spacing: -0.2px;">{title}</h4>
                        <span style="color: #cbd5e1; font-size: 0.85rem; font-weight: 500;">({year})</span>
                    </div>
                    <div style="display: flex; align-items: center; gap: 6px; margin: 4px 0 6px 0;">
                        <span style="color: #fbbf24; font-weight: 800; font-size: 0.92rem;">⭐ {rating}/10</span>
                        <span style="color: #cbd5e1; font-size: 0.78rem; font-weight: 500;">• Dir: {director}</span>
                    </div>
                    <div style="margin-bottom: 6px;">
                        {lang_badge}
                        {genre_badges}
                        {mood_badges}
                        {streaming_badges}
                    </div>
                </div>
                <div>
                    {f'<div style="color: #38bdf8; font-size: 0.78rem; font-weight: 600; font-style: italic; margin-bottom: 6px;">💡 {explanation}</div>' if explanation else ''}
                    <p style="color: #e2e8f0; font-size: 0.80rem; margin: 0; line-height: 1.4; display: -webkit-box; -webkit-line-clamp: 2; -webkit-box-orient: vertical; overflow: hidden;" title="{overview}">
                        {overview}
                    </p>
                </div>
            </div>
        </div>
        """
        cards_html.append(card)

    cards_html.append("</div>")
    return "".join(cards_html)

# --- Helper: Render Real-Time Intelligence Card ---
def render_live_intelligence_card(data):
    if not data:
        return ""

    title = data.get("title", "")
    year = data.get("year", "Recent")
    poster = data.get("poster_url", "")
    overview = data.get("overview", "")
    description = data.get("description", "")
    streaming = data.get("streaming_platforms", [])
    page_url = data.get("page_url", "#")
    live_status = data.get("live_status", "🟢 Live Ground-Truth")

    streaming_pills = ""
    for s in streaming:
        badge_bg = "rgba(16, 185, 129, 0.25)"
        badge_border = "#10b981"
        badge_color = "#34d399"
        if "netflix" in s.lower():
            badge_bg = "rgba(229, 9, 20, 0.25)"
            badge_border = "#ef4444"
            badge_color = "#fca5a5"
        elif "prime" in s.lower() or "amazon" in s.lower():
            badge_bg = "rgba(0, 168, 225, 0.25)"
            badge_border = "#0284c7"
            badge_color = "#38bdf8"
        elif "disney" in s.lower():
            badge_bg = "rgba(17, 60, 207, 0.25)"
            badge_border = "#3b82f6"
            badge_color = "#93c5fd"
        elif "max" in s.lower() or "hbo" in s.lower():
            badge_bg = "rgba(88, 34, 180, 0.25)"
            badge_border = "#8b5cf6"
            badge_color = "#c4b5fd"

        streaming_pills += f'<span style="background: {badge_bg}; border: 1px solid {badge_border}; color: {badge_color}; padding: 5px 13px; border-radius: 9999px; font-size: 0.84rem; font-weight: 700; margin-right: 8px; display: inline-block; margin-bottom: 6px;">📺 {s}</span>'

    html = f"""
    <div style="background: linear-gradient(135deg, rgba(30, 41, 59, 0.95) 0%, rgba(15, 23, 42, 0.98) 100%); border: 1px solid #6366f1; border-radius: 16px; padding: 22px; box-shadow: 0 10px 30px rgba(0,0,0,0.6); margin-top: 12px;">
        <div style="display: flex; gap: 24px; flex-wrap: wrap;">
            <div style="flex-shrink: 0;">
                <img src="{poster}" alt="{title}" style="width: 140px; height: 210px; object-fit: cover; border-radius: 12px; box-shadow: 0 8px 20px rgba(0,0,0,0.7); border: 1px solid #475569;" onerror="this.src='https://images.unsplash.com/photo-1489599849927-2ee91cede3ba?w=300';"/>
            </div>
            <div style="flex: 1; min-width: 260px;">
                <div style="display: flex; justify-content: space-between; align-items: flex-start; flex-wrap: wrap; gap: 10px;">
                    <div>
                        <h2 style="margin: 0; color: #ffffff; font-size: 1.65rem; font-weight: 800;">{title} <span style="color: #cbd5e1; font-size: 1.15rem; font-weight: 500;">({year})</span></h2>
                        <p style="color: #38bdf8; margin: 4px 0 12px 0; font-size: 0.95rem; font-weight: 600;">{description}</p>
                    </div>
                    <span style="background: rgba(34, 197, 94, 0.25); border: 1px solid #22c55e; color: #4ade80; padding: 5px 14px; border-radius: 9999px; font-size: 0.80rem; font-weight: 700; box-shadow: 0 0 10px rgba(34, 197, 94, 0.25);">
                        {live_status}
                    </span>
                </div>

                <div style="margin: 12px 0 16px 0;">
                    <div style="color: #f1f5f9; font-size: 0.84rem; text-transform: uppercase; letter-spacing: 0.05em; margin-bottom: 8px; font-weight: 800;">
                        📡 Official Where to Watch / Streaming Availability:
                    </div>
                    <div>
                        {streaming_pills if streaming_pills else '<span style="color: #cbd5e1; font-weight: 500;">Theatrical / Digital Store Platforms</span>'}
                    </div>
                </div>

                <div style="margin-top: 14px;">
                    <div style="color: #f1f5f9; font-size: 0.84rem; text-transform: uppercase; letter-spacing: 0.05em; margin-bottom: 6px; font-weight: 800;">
                        📖 Verified Real-Time Synopsis:
                    </div>
                    <p style="color: #f1f5f9; font-size: 0.90rem; line-height: 1.55; margin: 0;">
                        {overview}
                    </p>
                </div>

                <div style="margin-top: 18px; text-align: right;">
                    <a href="{page_url}" target="_blank" style="color: #93c5fd; text-decoration: underline; font-size: 0.86rem; font-weight: 700; display: inline-flex; align-items: center; gap: 4px;">
                        🔗 View Full Live Knowledge Article ➜
                    </a>
                </div>
            </div>
        </div>
    </div>
    """
    return html

# --- Helper: Render Trending Grid ---
def render_trending_grid(trending_list):
    cards_html = ['<div style="display: grid; grid-template-columns: repeat(auto-fill, minmax(280px, 1fr)); gap: 16px; margin-top: 14px;">']
    for m in trending_list:
        title = m["title"]
        year = m["year"]
        genre = m["genre"]
        rating = m["rating"]
        highlight = m["highlight"]
        poster = m["poster_url"]
        streaming = ", ".join(m["streaming_platforms"])

        card = f"""
        <div style="background: rgba(26, 36, 54, 0.95); border: 1px solid #475569; border-radius: 14px; padding: 14px; display: flex; gap: 14px; box-shadow: 0 6px 18px rgba(0,0,0,0.4);">
            <img src="{poster}" alt="{title}" style="width: 85px; height: 125px; object-fit: cover; border-radius: 8px; flex-shrink: 0; border: 1px solid #334155;" onerror="this.src='https://images.unsplash.com/photo-1489599849927-2ee91cede3ba?w=200';"/>
            <div style="display: flex; flex-direction: column; justify-content: space-between;">
                <div>
                    <h4 style="margin: 0; color: #ffffff; font-size: 1.0rem; font-weight: 800;">{title} <span style="color: #cbd5e1; font-size: 0.82rem; font-weight: 500;">({year})</span></h4>
                    <div style="color: #fbbf24; font-size: 0.86rem; font-weight: 800; margin: 3px 0;">⭐ {rating}/10 • <span style="color: #38bdf8; font-weight: 600;">{genre}</span></div>
                    <p style="color: #d8b4fe; font-size: 0.78rem; margin: 4px 0; font-style: italic; font-weight: 600;">🏆 {highlight}</p>
                </div>
                <div>
                    <span style="color: #34d399; font-size: 0.76rem; font-weight: 700; background: rgba(52, 211, 153, 0.15); border: 1px solid rgba(52, 211, 153, 0.35); padding: 3px 8px; border-radius: 6px; display: inline-block;">📺 {streaming}</span>
                </div>
            </div>
        </div>
        """
        cards_html.append(card)
    cards_html.append('</div>')
    return "".join(cards_html)


# --- Gradio Callback Functions ---

def on_chat_submit(message, chat_history, provider_choice, model_choice, api_key):
    if not message or not message.strip():
        return "", chat_history, "", render_movie_cards([])

    chat_history = list(chat_history) if chat_history else []
    
    provider_str = "Local"
    if "groq" in str(provider_choice).lower():
        provider_str = "Groq"
    elif "gemini" in str(provider_choice).lower():
        provider_str = "Gemini"

    reply, recs, thought = agent.chat(
        user_message=message,
        api_key=api_key if api_key else None,
        api_provider=provider_str,
        model=model_choice
    )

    chat_history.append({"role": "user", "content": message})
    chat_history.append({"role": "assistant", "content": reply})
    cards_rendered = render_movie_cards(recs)
    thought_display = f"**🧠 Agent Thought Process & Live Tools:**\n\n`{thought}`" if thought else ""

    return "", chat_history, thought_display, cards_rendered

def on_quick_prompt(prompt_text, chat_history, provider_choice, model_choice, api_key):
    return on_chat_submit(prompt_text, chat_history, provider_choice, model_choice, api_key)

def on_clear_chat():
    agent.reset()
    welcome_message = [
        {"role": "assistant", "content": "👋 **Hello! I'm your CineAgent AI.**\n\nI can recommend movies across **all cinema worldwide** and fetch **real-time data** (where to stream, trending titles, live box office). Tell me what you feel like watching!"}
    ]
    return welcome_message, "", render_movie_cards([])

def on_provider_change(provider_choice):
    prov_str = str(provider_choice).lower()
    if "gemini" in prov_str:
        gemini_k = os.environ.get("GEMINI_API_KEY", "")
        return (
            gr.update(choices=["gemini-1.5-flash", "gemini-1.5-pro", "gemini-2.0-flash"], value="gemini-1.5-flash"),
            gr.update(value=gemini_k, placeholder="Enter Google Gemini API key (AIzaSy...)", info="Google Gemini API key (starts with AIzaSy...). Pre-loaded from .env if set.")
        )
    elif "groq" in prov_str:
        groq_k = os.environ.get("GROQ_API_KEY", "")
        return (
            gr.update(choices=["openai/gpt-oss-120b", "qwen/qwen3.8-27b", "openai/gpt-oss-20b", "llama-3.3-70b-versatile"], value="openai/gpt-oss-120b"),
            gr.update(value=groq_k, placeholder="Pre-loaded from .env or enter Groq key (gsk_...)", info="Pre-configured with your Groq API key from .env.")
        )
    else:
        return (
            gr.update(choices=["local-catalog"], value="local-catalog"),
            gr.update(value="", placeholder="Offline engine active - no key needed", info="Offline heuristic & real-time knowledge graph active.")
        )

def on_live_movie_search(query_title):
    if not query_title or not query_title.strip():
        return "Please enter a movie title.", ""
    data = search_live_movie_data(query_title)
    summary = f"Found real-time intelligence for **{data['title']} ({data['year']})**."
    return summary, render_live_intelligence_card(data)

def on_find_similar(movie_title, top_k, min_rating, genre_filter, hybrid_w):
    if not movie_title or not str(movie_title).strip():
        return "Please select or type a movie.", render_movie_cards([])

    clean_title = str(movie_title).strip()
    similar = recommender.get_similar_movies(
        title=clean_title,
        top_k=int(top_k),
        min_rating=float(min_rating),
        genre_filter=genre_filter if genre_filter != "All" else None,
        hybrid_weight=float(hybrid_w) / 100.0
    )

    source_movie = recommender.get_movie_by_title(clean_title)
    if source_movie:
        streaming = detect_streaming_platforms(source_movie["title"], source_movie.get("overview", ""))
        stream_str = ", ".join(streaming) if streaming else "Digital Platforms"
        src_info = f"### 🎬 Showing movies most similar to: **{source_movie['title']} ({source_movie['year']})**\n*Genres: {source_movie['genre']} | Director: {source_movie['director']} | Rating: ⭐ {source_movie['rating']}/10 | 📺 Streaming on: **{stream_str}***"
    else:
        live_m = search_live_movie_data(clean_title)
        st_str = ", ".join(live_m.get("streaming_platforms", [])) if live_m.get("streaming_platforms") else "Digital Stores"
        src_info = f"### 🎬 Showing movies most similar to: **{live_m['title']} ({live_m['year']})**\n*Live Overview: {live_m.get('description', '')} | Director: {live_m.get('director', '')} | 📺 Streaming on: **{st_str}***"

    return src_info, render_movie_cards(similar)

def on_filter_movies(mood, language, genre, min_rating, year_min, year_max):
    results = recommender.filter_movies(
        genre=genre if genre != "All" else None,
        mood=mood if mood != "All" else None,
        language=language if language != "All Languages" else None,
        min_rating=float(min_rating),
        year_min=int(year_min),
        year_max=int(year_max),
        limit=18
    )
    lang_info = f" in **{language}**" if language and language != "All Languages" else ""
    summary_text = f"Found **{len(results)}** curated titles matching your filters{lang_info}."
    return summary_text, render_movie_cards(results)


# --- Custom Cinema CSS & Animations ---
CINEMA_CSS = """
/* Google Font & Root Variables */
@import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700;800&family=Inter:wght@300;400;500;600;700&display=swap');

:root {
    --cinema-primary: #6366f1;
    --cinema-accent: #38bdf8;
    --cinema-glow: rgba(99, 102, 241, 0.4);
    --cinema-bg-dark: #090d16;
}

/* Base Page Styling */
html, body {
    background-color: var(--cinema-bg-dark) !important;
    color: #f8fafc !important;
    font-family: 'Inter', system-ui, -apple-system, sans-serif !important;
    overflow-x: hidden;
}

.gradio-container {
    max-width: 1280px !important;
    margin: 0 auto !important;
    background: transparent !important;
    position: relative;
    z-index: 2;
    padding-top: 10px !important;
}

/* Ambient Video Background Layer */
.cinema-ambient-bg {
    position: fixed;
    top: 0;
    left: 0;
    width: 100vw;
    height: 100vh;
    z-index: 0;
    overflow: hidden;
    pointer-events: none;
}

.cinema-ambient-bg video {
    position: absolute;
    top: 50%;
    left: 50%;
    min-width: 100vw;
    min-height: 100vh;
    width: auto;
    height: auto;
    transform: translate(-50%, -50%) scale(1.06);
    object-fit: cover;
    filter: brightness(0.20) saturate(1.35) contrast(1.15);
    transition: opacity 0.6s ease, filter 0.6s ease;
}

.cinema-ambient-overlay {
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background: radial-gradient(circle at 50% 15%, rgba(99, 102, 241, 0.15), transparent 65%),
                linear-gradient(180deg, rgba(15, 23, 42, 0.88) 0%, rgba(15, 23, 42, 0.94) 50%, rgba(9, 13, 22, 0.98) 100%);
    backdrop-filter: blur(3px);
    transition: background 0.5s ease;
}

/* Floating Cinema Particles */
.cinema-floating-particles {
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background-image: radial-gradient(rgba(255, 255, 255, 0.08) 1px, transparent 1px),
                      radial-gradient(rgba(99, 102, 241, 0.12) 1px, transparent 1px);
    background-size: 55px 55px, 85px 85px;
    background-position: 0 0, 25px 25px;
    animation: particleFloat 40s linear infinite;
    opacity: 0.5;
}

@keyframes particleFloat {
    0% { background-position: 0 0, 25px 25px; }
    100% { background-position: 500px 1000px, 525px 1025px; }
}

/* Hero Header Styling */
.hero-header {
    background: rgba(15, 23, 42, 0.88) !important;
    backdrop-filter: blur(18px) !important;
    -webkit-backdrop-filter: blur(18px) !important;
    padding: 24px 30px !important;
    border-radius: 18px !important;
    border: 1px solid rgba(99, 102, 241, 0.45) !important;
    margin-bottom: 22px !important;
    box-shadow: 0 14px 40px -5px rgba(0, 0, 0, 0.75), 0 0 30px rgba(99, 102, 241, 0.20), inset 0 1px 0 rgba(255, 255, 255, 0.15) !important;
    animation: fadeInDown 0.8s cubic-bezier(0.16, 1, 0.3, 1);
}

@keyframes fadeInDown {
    from { opacity: 0; transform: translateY(-16px); }
    to { opacity: 1; transform: translateY(0); }
}

.shimmer-text {
    font-family: 'Outfit', sans-serif !important;
    background: linear-gradient(90deg, #38bdf8, #818cf8, #c084fc, #f43f5e, #38bdf8) !important;
    background-size: 300% auto !important;
    -webkit-background-clip: text !important;
    -webkit-text-fill-color: transparent !important;
    animation: textShimmer 7s ease infinite !important;
}

@keyframes textShimmer {
    0% { background-position: 0% 50%; }
    50% { background-position: 100% 50%; }
    100% { background-position: 0% 50%; }
}

.radar-pulse-dot {
    display: inline-block;
    width: 9px;
    height: 9px;
    background: #22c55e;
    border-radius: 50%;
    animation: radarPulse 1.8s infinite;
    margin-right: 6px;
}

@keyframes radarPulse {
    0% { box-shadow: 0 0 0 0 rgba(34, 197, 94, 0.7); }
    70% { box-shadow: 0 0 0 8px rgba(34, 197, 94, 0); }
    100% { box-shadow: 0 0 0 0 rgba(34, 197, 94, 0); }
}

/* Ambient Video Controller Buttons */
.cinema-ctrl-btn {
    background: rgba(30, 41, 59, 0.95) !important;
    border: 1px solid rgba(99, 102, 241, 0.5) !important;
    color: #e0e7ff !important;
    padding: 7px 16px !important;
    border-radius: 20px !important;
    font-size: 0.80rem !important;
    font-weight: 700 !important;
    cursor: pointer !important;
    transition: all 0.25s ease !important;
    box-shadow: 0 2px 10px rgba(0, 0, 0, 0.4) !important;
}

.cinema-ctrl-btn:hover {
    background: rgba(99, 102, 241, 0.45) !important;
    border-color: #a5b4fc !important;
    color: #ffffff !important;
    transform: translateY(-2px) !important;
    box-shadow: 0 4px 16px rgba(99, 102, 241, 0.5) !important;
}

/* =========================================================
   CINEMA AGENT HIGH-CONTRAST ACCESSIBILITY DESIGN SYSTEM
   ========================================================= */

/* Section Card Containers - High Visibility */
.cinema-section-card {
    background: rgba(15, 23, 42, 0.92) !important;
    backdrop-filter: blur(18px) !important;
    -webkit-backdrop-filter: blur(18px) !important;
    border: 1px solid rgba(99, 102, 241, 0.42) !important;
    border-radius: 16px !important;
    padding: 22px 24px !important;
    margin-bottom: 22px !important;
    box-shadow: 0 12px 35px -5px rgba(0, 0, 0, 0.75), 0 0 22px rgba(99, 102, 241, 0.16) !important;
    transition: border-color 0.25s ease, box-shadow 0.25s ease !important;
}

.cinema-section-card:hover {
    border-color: rgba(99, 102, 241, 0.7) !important;
    box-shadow: 0 14px 40px -4px rgba(0, 0, 0, 0.85), 0 0 28px rgba(99, 102, 241, 0.25) !important;
}

/* Luminous Section Header Badges */
.section-badge {
    display: inline-flex;
    align-items: center;
    gap: 8px;
    background: linear-gradient(135deg, rgba(99, 102, 241, 0.35), rgba(56, 189, 248, 0.30));
    border: 1px solid rgba(129, 140, 248, 0.6);
    color: #ffffff !important;
    font-family: 'Outfit', sans-serif;
    font-size: 0.94rem;
    font-weight: 800;
    padding: 6px 16px;
    border-radius: 9999px;
    letter-spacing: 0.02em;
    margin-bottom: 14px;
    box-shadow: 0 3px 12px rgba(99, 102, 241, 0.35);
}

/* Quick Seed Chips */
.quick-btn {
    border-radius: 20px !important;
    font-size: 0.84rem !important;
    font-weight: 700 !important;
    padding: 6px 14px !important;
    background: rgba(30, 41, 59, 0.95) !important;
    backdrop-filter: blur(8px) !important;
    border: 1px solid #475569 !important;
    color: #bae6fd !important;
    transition: all 0.2s ease !important;
}

.quick-btn:hover {
    background: rgba(99, 102, 241, 0.45) !important;
    border-color: #818cf8 !important;
    color: #ffffff !important;
    transform: translateY(-2px) !important;
    box-shadow: 0 4px 14px rgba(99, 102, 241, 0.4) !important;
}

/* Modern Movie Cards */
.movie-card {
    background: rgba(26, 36, 54, 0.95) !important;
    backdrop-filter: blur(14px) !important;
    -webkit-backdrop-filter: blur(14px) !important;
    border: 1px solid rgba(99, 102, 241, 0.38) !important;
    border-radius: 14px !important;
    padding: 15px !important;
    position: relative !important;
    display: flex !important;
    gap: 15px !important;
    transition: transform 0.28s cubic-bezier(0.4, 0, 0.2, 1), box-shadow 0.28s cubic-bezier(0.4, 0, 0.2, 1), border-color 0.28s ease !important;
    box-shadow: 0 8px 24px rgba(0, 0, 0, 0.5), inset 0 1px 0 rgba(255, 255, 255, 0.08) !important;
}

.movie-card:hover {
    transform: translateY(-6px) scale(1.015) !important;
    border-color: #818cf8 !important;
    box-shadow: 0 16px 36px -4px rgba(0, 0, 0, 0.75), 0 0 25px rgba(99, 102, 241, 0.45) !important;
}

.movie-card img {
    transition: transform 0.4s ease !important;
}

.movie-card:hover img {
    transform: scale(1.05) !important;
}

/* Floating Match Badge */
@keyframes badgeFloat {
    0%, 100% { transform: translateY(0); }
    50% { transform: translateY(-3px); }
}

.match-badge {
    animation: badgeFloat 3.5s ease-in-out infinite;
}

/* Force Universal High Contrast Text */
h1, h2, h3, h4, h5, h6 {
    color: #ffffff !important;
    font-family: 'Outfit', sans-serif !important;
    font-weight: 800 !important;
    letter-spacing: -0.01em !important;
}

/* Gradio Component Labels - Maximum Contrast */
label, 
label span, 
.block label, 
span[data-testid="block-label"],
.label-wrap,
.wrap-default {
    color: #f8fafc !important;
    font-size: 0.92rem !important;
    font-weight: 700 !important;
    letter-spacing: 0.015em !important;
}

/* Form Helper and Info Text */
.form span.info,
p.info,
.info {
    color: #93c5fd !important;
    font-size: 0.82rem !important;
    font-weight: 500 !important;
}

/* Generic Form Blocks & Panels */
.block, 
.gr-box, 
.gr-form, 
fieldset {
    background: rgba(15, 23, 42, 0.85) !important;
    border: 1px solid #334155 !important;
    border-radius: 12px !important;
}

/* Inputs, Textareas, Password Inputs */
input[type="text"], 
input[type="password"], 
input[type="number"], 
textarea,
.gr-input,
.gr-text-input {
    background-color: #0b1329 !important;
    color: #ffffff !important;
    border: 1px solid #475569 !important;
    border-radius: 10px !important;
    padding: 10px 14px !important;
    font-size: 0.95rem !important;
    font-weight: 500 !important;
    transition: all 0.2s ease !important;
}

input:focus, 
textarea:focus {
    border-color: #818cf8 !important;
    box-shadow: 0 0 0 3px rgba(99, 102, 241, 0.35) !important;
    background-color: #0f172a !important;
    outline: none !important;
}

input::placeholder, 
textarea::placeholder {
    color: #94a3b8 !important;
    opacity: 1 !important;
}

/* Dropdowns & Selections */
.dropdown,
.gr-dropdown,
select,
.wrap {
    background: #0b1329 !important;
    color: #ffffff !important;
    border: 1px solid #475569 !important;
    border-radius: 10px !important;
}

ul.options,
.options,
ul[role="listbox"],
.choices__list--dropdown {
    background: #0f172a !important;
    border: 1px solid #6366f1 !important;
    box-shadow: 0 12px 30px rgba(0,0,0,0.85) !important;
    border-radius: 10px !important;
    z-index: 9999 !important;
}

ul.options li,
li[role="option"],
.choices__item--choice {
    color: #f8fafc !important;
    padding: 10px 14px !important;
    border-bottom: 1px solid #1e293b !important;
    background: #0f172a !important;
}

ul.options li:hover,
li[role="option"]:hover,
li.selected,
.choices__item--choice:hover {
    background: #312e81 !important;
    color: #ffffff !important;
}

/* Radio Groups */
.radio-group,
.gr-radio,
fieldset.gr-radio {
    background: rgba(15, 23, 42, 0.85) !important;
    border: 1px solid #475569 !important;
    border-radius: 12px !important;
    padding: 10px !important;
}

.gr-radio label,
.radio-group label,
span.ml-2 {
    color: #f1f5f9 !important;
    font-weight: 600 !important;
    font-size: 0.90rem !important;
}

/* Chatbot Component */
.chatbot,
[data-testid="chatbot"] {
    background: rgba(11, 19, 41, 0.95) !important;
    border: 1px solid #334155 !important;
    border-radius: 14px !important;
    box-shadow: inset 0 2px 6px rgba(0,0,0,0.5) !important;
}

.chatbot .user,
[data-testid="user"] {
    background: linear-gradient(135deg, #4338ca, #6366f1) !important;
    color: #ffffff !important;
    border: 1px solid #818cf8 !important;
    border-radius: 16px 16px 4px 16px !important;
    padding: 12px 16px !important;
    box-shadow: 0 4px 14px rgba(79, 70, 229, 0.35) !important;
    font-size: 0.95rem !important;
    font-weight: 500 !important;
}

.chatbot .bot,
[data-testid="bot"] {
    background: #1e293b !important;
    color: #f8fafc !important;
    border: 1px solid #475569 !important;
    border-radius: 16px 16px 16px 4px !important;
    padding: 14px 18px !important;
    box-shadow: 0 4px 14px rgba(0, 0, 0, 0.4) !important;
    font-size: 0.95rem !important;
    line-height: 1.6 !important;
}

.chatbot .bot p,
.chatbot .bot span,
.chatbot .bot li {
    color: #f8fafc !important;
}

.chatbot .bot strong {
    color: #38bdf8 !important;
    font-weight: 700 !important;
}

/* Reasoning Box Callout */
.reasoning-box {
    background: rgba(15, 23, 42, 0.95) !important;
    border: 1px solid #6366f1 !important;
    border-left: 5px solid #38bdf8 !important;
    border-radius: 10px !important;
    padding: 14px 18px !important;
    margin: 12px 0 !important;
    box-shadow: 0 4px 16px rgba(0, 0, 0, 0.4) !important;
    color: #f8fafc !important;
}

/* Accordion Component */
.accordion {
    border: 1px solid #475569 !important;
    border-radius: 12px !important;
    overflow: hidden !important;
    background: rgba(15, 23, 42, 0.88) !important;
    margin-top: 10px !important;
}

.accordion > .label-wrap {
    background: linear-gradient(90deg, #1e293b, #111e38) !important;
    border-bottom: 1px solid #334155 !important;
    padding: 12px 18px !important;
    color: #ffffff !important;
    font-size: 0.95rem !important;
    font-weight: 700 !important;
}

.accordion > .label-wrap:hover {
    background: linear-gradient(90deg, #28354f, #1e293b) !important;
}

/* Tab Navigation Bar - High Visibility */
div.tab-nav {
    display: flex !important;
    gap: 8px !important;
    background: rgba(15, 23, 42, 0.94) !important;
    border: 1px solid #475569 !important;
    border-radius: 14px !important;
    padding: 8px 10px !important;
    margin-bottom: 18px !important;
    box-shadow: 0 4px 20px rgba(0,0,0,0.5) !important;
    flex-wrap: wrap !important;
}

div.tab-nav button {
    background: transparent !important;
    color: #e2e8f0 !important;
    border: 1px solid transparent !important;
    border-radius: 10px !important;
    font-family: 'Outfit', sans-serif !important;
    font-weight: 700 !important;
    font-size: 0.92rem !important;
    padding: 8px 16px !important;
    transition: all 0.22s ease !important;
}

div.tab-nav button:hover {
    color: #ffffff !important;
    background: rgba(99, 102, 241, 0.3) !important;
    border-color: rgba(99, 102, 241, 0.55) !important;
    transform: translateY(-1px) !important;
}

div.tab-nav button.selected {
    color: #ffffff !important;
    background: linear-gradient(135deg, #4f46e5, #6366f1) !important;
    border: 1px solid #a5b4fc !important;
    box-shadow: 0 4px 16px rgba(99, 102, 241, 0.45) !important;
    text-shadow: 0 1px 2px rgba(0, 0, 0, 0.4) !important;
}

/* Action Buttons */
button.primary,
.gr-button-primary {
    background: linear-gradient(135deg, #4f46e5 0%, #0284c7 100%) !important;
    color: #ffffff !important;
    font-weight: 800 !important;
    font-size: 0.95rem !important;
    border: 1px solid rgba(255, 255, 255, 0.25) !important;
    border-radius: 12px !important;
    box-shadow: 0 4px 14px rgba(79, 70, 229, 0.45) !important;
    transition: all 0.25s cubic-bezier(0.4, 0, 0.2, 1) !important;
}

button.primary:hover,
.gr-button-primary:hover {
    background: linear-gradient(135deg, #4338ca 0%, #0369a1 100%) !important;
    box-shadow: 0 6px 20px rgba(79, 70, 229, 0.65) !important;
    transform: translateY(-2px) !important;
}

button.secondary,
.gr-button-secondary {
    background: #1e293b !important;
    color: #f1f5f9 !important;
    border: 1px solid #475569 !important;
    border-radius: 10px !important;
    font-weight: 600 !important;
}

button.secondary:hover,
.gr-button-secondary:hover {
    background: #28354f !important;
    color: #ffffff !important;
    border-color: #818cf8 !important;
    transform: translateY(-1px) !important;
}

/* Tables & DataFrames */
table, 
.table-wrap, 
[data-testid="dataframe"] {
    background: #0b1329 !important;
    border: 1px solid #475569 !important;
    border-radius: 12px !important;
    overflow: hidden !important;
}

table th,
thead th {
    background: #131d38 !important;
    color: #38bdf8 !important;
    font-family: 'Outfit', sans-serif !important;
    font-weight: 800 !important;
    font-size: 0.88rem !important;
    padding: 12px 14px !important;
    border-bottom: 2px solid #6366f1 !important;
    border-right: 1px solid #334155 !important;
    text-transform: uppercase !important;
    letter-spacing: 0.05em !important;
}

table td,
tbody td {
    background: #0f172a !important;
    color: #f1f5f9 !important;
    font-size: 0.86rem !important;
    padding: 10px 14px !important;
    border-bottom: 1px solid #1e293b !important;
    border-right: 1px solid #1e293b !important;
}

tbody tr:nth-child(even) td {
    background: #15223e !important;
}

tbody tr:hover td {
    background: #1e2e54 !important;
    color: #ffffff !important;
}

/* Markdown Prose Universal Contrast */
.prose,
.markdown-body {
    color: #e2e8f0 !important;
    line-height: 1.65 !important;
}

.prose h1, .prose h2, .prose h3, .prose h4 {
    color: #ffffff !important;
    border-bottom-color: #334155 !important;
    margin-top: 14px !important;
    margin-bottom: 8px !important;
}

.prose p, .prose li {
    color: #e2e8f0 !important;
    font-size: 0.94rem !important;
}

.prose strong {
    color: #38bdf8 !important;
    font-weight: 700 !important;
}

.prose em {
    color: #cbd5e1 !important;
}

.prose hr {
    border-color: #334155 !important;
    margin: 18px 0 !important;
}

/* Academic Report Table in Tab 6 */
.prose table {
    width: 100% !important;
    border-collapse: collapse !important;
    margin: 16px 0 !important;
    border: 1px solid #475569 !important;
    border-radius: 10px !important;
    overflow: hidden !important;
}

.prose table th {
    background: #1e293b !important;
    color: #38bdf8 !important;
    padding: 12px 14px !important;
    font-size: 0.90rem !important;
    border: 1px solid #475569 !important;
}

.prose table td {
    background: #0f172a !important;
    color: #f1f5f9 !important;
    padding: 10px 14px !important;
    border: 1px solid #334155 !important;
    font-size: 0.88rem !important;
}

.prose table tr:nth-child(even) td {
    background: #162038 !important;
}
"""

CINEMA_HEAD = """
<script>
// Force dark class on root document and observe changes
function ensureDarkMode() {
    if (document.documentElement && !document.documentElement.classList.contains('dark')) {
        document.documentElement.classList.add('dark');
    }
    if (document.body && !document.body.classList.contains('dark')) {
        document.body.classList.add('dark');
    }
}
ensureDarkMode();

let videoPlaying = true;
let dimLevels = [0.88, 0.95, 0.72];
let dimIdx = 0;

function toggleAmbientVideo() {
    const v = document.getElementById('cinema-video-player');
    const btn = document.getElementById('video-toggle-btn');
    if (!v) return;
    if (videoPlaying) {
        v.pause();
        videoPlaying = false;
        if (btn) btn.innerHTML = '▶️ Play Video';
    } else {
        v.play();
        videoPlaying = true;
        if (btn) btn.innerHTML = '⏸️ Pause Video';
    }
}

function toggleCinemaDim() {
    const ov = document.getElementById('ambient-overlay');
    if (!ov) return;
    dimIdx = (dimIdx + 1) % dimLevels.length;
    ov.style.background = 'radial-gradient(circle at 50% 15%, rgba(99, 102, 241, 0.15), transparent 65%), linear-gradient(180deg, rgba(15, 23, 42, ' + dimLevels[dimIdx] + ') 0%, rgba(15, 23, 42, ' + (dimLevels[dimIdx] + 0.05) + ') 50%, rgba(9, 13, 22, 0.98) 100%)';
}

document.addEventListener('DOMContentLoaded', () => {
    ensureDarkMode();
    const v = document.getElementById('cinema-video-player');
    if (v) {
        v.play().catch(e => console.log('Autoplay started muted'));
    }
    const observer = new MutationObserver(() => ensureDarkMode());
    observer.observe(document.documentElement, { attributes: true, attributeFilter: ['class'] });
});
</script>
"""

# --- Gradio UI Layout ---
all_movie_titles = recommender.get_all_titles()
all_genres = ["All"] + recommender.get_all_genres()
all_moods = ["All"] + recommender.get_all_moods()
cinema_theme = gr.themes.Soft(
    primary_hue="indigo",
    neutral_hue="slate"
).set(
    body_background_fill="#090d16",
    body_text_color="#f8fafc",
    body_text_color_subdued="#cbd5e1",
    block_background_fill="rgba(15, 23, 42, 0.92)",
    block_border_color="rgba(99, 102, 241, 0.40)",
    block_label_text_color="#f8fafc",
    input_background_fill="#0b1329",
    input_border_color="#475569",
    input_border_color_focus="#818cf8",
    button_primary_background_fill="linear-gradient(135deg, #4f46e5, #0284c7)",
    button_primary_text_color="#ffffff",
    button_secondary_background_fill="#1e293b",
    button_secondary_text_color="#f1f5f9",
    button_secondary_border_color="#475569"
)

with gr.Blocks(
    title="CineAgent | Real-Time AI Movie Recommender",
) as demo:
    
    # Ambient Cinema Video Background Layer & Hero Header
    gr.HTML("""
    <!-- Ambient Cinema Background Video Layer -->
    <div class="cinema-ambient-bg" id="ambient-cinema-bg">
        <video id="cinema-video-player" autoplay loop muted playsinline>
            <source src="https://upload.wikimedia.org/wikipedia/commons/2/2f/DGB_%28large_feed_reels%29_-_Cinema_projector.webm" type="video/webm">
        </video>
        <div class="cinema-ambient-overlay" id="ambient-overlay"></div>
        <div class="cinema-floating-particles"></div>
    </div>

    <!-- Hero Header with Glassmorphic Shimmer & Ambient Controls -->
    <div class="hero-header">
        <div style="display: flex; align-items: center; justify-content: space-between; flex-wrap: wrap; gap: 15px;">
            <div>
                <div style="display: flex; align-items: center; gap: 12px;">
                    <span style="font-size: 2.3rem; animation: badgeFloat 3s ease-in-out infinite; display: inline-block;">🎬</span>
                    <h1 class="shimmer-text" style="margin: 0; font-size: 2.0rem; font-weight: 800; letter-spacing: -0.5px;">
                        CineAgent: Real-Time AI Movie Recommendation System
                    </h1>
                </div>
                <p style="margin: 6px 0 0 0; color: #94a3b8; font-size: 0.95rem; display: flex; align-items: center; gap: 8px; flex-wrap: wrap;">
                    <span><span class="radar-pulse-dot"></span><strong>Live Ambient Cinema Mode Active</strong></span>
                    <span>•</span>
                    <span>ReAct Tool-Calling Agent</span>
                    <span>•</span>
                    <span>Real-Time Streaming Radar</span>
                    <span>•</span>
                    <span>Multi-Model LLM Execution (Groq / Gemini / Local)</span>
                </p>
            </div>
            <div style="display: flex; align-items: center; gap: 10px; flex-wrap: wrap;">
                <button onclick="toggleAmbientVideo()" id="video-toggle-btn" class="cinema-ctrl-btn" title="Pause or Resume Background Cinema Video">
                    ⏸️ Pause Video
                </button>
                <button onclick="toggleCinemaDim()" class="cinema-ctrl-btn" title="Cycle Background Brightness">
                    🎚️ Dim Ambient
                </button>
                <span style="background: rgba(99, 102, 241, 0.25); border: 1px solid rgba(99, 102, 241, 0.45); color: #c7d2fe; padding: 5px 14px; border-radius: 9999px; font-size: 0.82rem; font-weight: 700; box-shadow: 0 0 12px rgba(99, 102, 241, 0.3);">
                    CA3 Mini Project • Sem 5
                </span>
            </div>
        </div>
    </div>
    """)

    with gr.Tabs():

        # ==========================================
        # TAB 1: Conversational AI Agent (with Real-Time Tool Calling)
        # ==========================================
        with gr.TabItem("🤖 AI Recommendation Agent", id="tab_agent"):
            with gr.Row():
                with gr.Column(scale=5, elem_classes=["cinema-section-card"]):
                    gr.HTML('<div class="section-badge">💬 CineAgent Interactive Console</div>')
                    chatbot = gr.Chatbot(
                        label="Conversation with CineAgent",
                        height=420,
                        value=[
                            {"role": "assistant", "content": "👋 **Hello! I'm your CineAgent AI.**\n\nI can recommend movies across **all cinema worldwide** and fetch **real-time data** (where to stream, trending titles, live box office).\n\nAsk me anything!"}
                        ],
                        show_label=False
                    )

                    with gr.Row():
                        user_input = gr.Textbox(
                            placeholder="e.g. 'Where can I stream Inception right now?' or 'Recommend a mind-bending sci-fi film'",
                            show_label=False,
                            scale=9,
                            lines=1
                        )
                        send_btn = gr.Button("Send 🚀", variant="primary", scale=2)

                    gr.Markdown("**Quick Prompts (Real-Time & Recommendations):**")
                    with gr.Row():
                        qp1 = gr.Button("📺 Where to stream Inception?", elem_classes=["quick-btn"], size="sm")
                        qp2 = gr.Button("🔥 What movies are trending?", elem_classes=["quick-btn"], size="sm")
                        qp3 = gr.Button("🌀 Mind-bending like Interstellar", elem_classes=["quick-btn"], size="sm")
                        qp4 = gr.Button("🦁 Epic Indian Action (RRR / Kalki)", elem_classes=["quick-btn"], size="sm")

                    with gr.Row():
                        clear_btn = gr.Button("🔄 Clear Conversation", size="sm")

                    with gr.Accordion("⚙️ Multi-Model LLM Engine & Provider Settings", open=True):
                        with gr.Row():
                            provider_radio = gr.Radio(
                                choices=[
                                    "⚡ Groq Cloud LPU (Ultra-Fast All Cinema & Real-Time Tools)",
                                    "✨ Google Gemini API (Multimodal Reasoning)",
                                    "📁 Offline Engine (Local Dataset)"
                                ],
                                value="⚡ Groq Cloud LPU (Ultra-Fast All Cinema & Real-Time Tools)",
                                label="Reasoning Provider",
                                scale=6
                            )
                            model_dd = gr.Dropdown(
                                choices=[
                                    "openai/gpt-oss-120b",
                                    "qwen/qwen3.8-27b",
                                    "openai/gpt-oss-20b",
                                    "gemini-1.5-flash",
                                    "gemini-1.5-pro"
                                ],
                                value="openai/gpt-oss-120b",
                                label="LLM Model",
                                scale=4
                            )
                        api_key_input = gr.Textbox(
                            label="API Key (Groq or Gemini)",
                            placeholder="Pre-loaded from .env file or enter key here...",
                            value=os.environ.get("GROQ_API_KEY", ""),
                            type="password",
                            info="Pre-configured with your Groq API key from .env. The agent automatically executes real-time retrieval tools when live movie data or streaming queries are asked!"
                        )

                with gr.Column(scale=5, elem_classes=["cinema-section-card"]):
                    gr.HTML('<div class="section-badge">🍿 Recommendation & Discovery Canvas</div>')
                    thought_box = gr.Markdown("", label="Agent Reasoning & Tools")
                    gr.Markdown("### 🎬 Recommended & Live Findings")
                    cards_output = gr.HTML(
                        value=render_movie_cards(recommender.filter_movies(limit=2)),
                        label="Movie Recommendations"
                    )

            # Event bindings for Tab 1
            send_btn.click(
                fn=on_chat_submit,
                inputs=[user_input, chatbot, provider_radio, model_dd, api_key_input],
                outputs=[user_input, chatbot, thought_box, cards_output]
            )
            user_input.submit(
                fn=on_chat_submit,
                inputs=[user_input, chatbot, provider_radio, model_dd, api_key_input],
                outputs=[user_input, chatbot, thought_box, cards_output]
            )
            clear_btn.click(
                fn=on_clear_chat,
                outputs=[chatbot, thought_box, cards_output]
            )
            provider_radio.change(
                fn=on_provider_change,
                inputs=[provider_radio],
                outputs=[model_dd, api_key_input]
            )

            qp1.click(
                fn=lambda h, p, m, k: on_quick_prompt("Where can I stream Inception right now and what are its details?", h, p, m, k),
                inputs=[chatbot, provider_radio, model_dd, api_key_input],
                outputs=[user_input, chatbot, thought_box, cards_output]
            )
            qp2.click(
                fn=lambda h, p, m, k: on_quick_prompt("What movies are trending globally at the box office right now?", h, p, m, k),
                inputs=[chatbot, provider_radio, model_dd, api_key_input],
                outputs=[user_input, chatbot, thought_box, cards_output]
            )
            qp3.click(
                fn=lambda h, p, m, k: on_quick_prompt("Recommend a mind-bending sci-fi movie with twists like Interstellar", h, p, m, k),
                inputs=[chatbot, provider_radio, model_dd, api_key_input],
                outputs=[user_input, chatbot, thought_box, cards_output]
            )
            qp4.click(
                fn=lambda h, p, m, k: on_quick_prompt("Recommend an intense, epic Indian action spectacle like RRR or Kalki 2898 AD", h, p, m, k),
                inputs=[chatbot, provider_radio, model_dd, api_key_input],
                outputs=[user_input, chatbot, thought_box, cards_output]
            )

        # ==========================================
        # TAB 2: 🔴 Real-Time Cinema Radar & Live Search
        # ==========================================
        with gr.TabItem("🔴 Real-Time Cinema Radar", id="tab_radar"):
            with gr.Column(elem_classes=["cinema-section-card"]):
                gr.HTML('<div class="section-badge">📡 Real-Time Live Movie Intelligence & Streaming Radar</div>')
                gr.Markdown(
                    "Query live ground-truth facts for **any film worldwide** (Wikipedia Knowledge Graph & Streaming Directories). Get instant verified streaming platforms, real-time synopses, and live posters."
                )
                with gr.Row():
                    live_search_input = gr.Textbox(
                        placeholder="Enter any movie title in the world (e.g. 'Dune: Part Two', 'Kalki 2898 AD', 'Oppenheimer', 'RRR')...",
                        label="Search Any Movie in Real Time",
                        scale=9
                    )
                    live_search_btn = gr.Button("🔍 Fetch Live Intelligence", variant="primary", scale=3)

                DEFAULT_RADAR_SEED = {
                    "title": "Oppenheimer",
                    "year": "2023",
                    "description": "Epic biographical drama directed by Christopher Nolan",
                    "overview": "The story of American scientist J. Robert Oppenheimer and his role in the development of the atomic bomb during World War II with the Manhattan Project.",
                    "poster_url": "https://image.tmdb.org/t/p/w500/8Gxv8gSFCU0XGDykEGv7zR1n2ua.jpg",
                    "streaming_platforms": ["Prime Video", "JioCinema", "Apple TV"],
                    "live_status": "🟢 Verified Live Ground-Truth",
                    "source": "Wikipedia Real-Time Knowledge Graph",
                    "page_url": "https://en.wikipedia.org/wiki/Oppenheimer_(film)"
                }
                live_radar_status = gr.Markdown("Enter a movie above to retrieve live data.")
                live_radar_output = gr.HTML(value=render_live_intelligence_card(DEFAULT_RADAR_SEED))

            with gr.Column(elem_classes=["cinema-section-card"]):
                gr.HTML('<div class="section-badge">🔥 Global Trending Cinema & Box Office Milestones</div>')
                trending_grid_output = gr.HTML(value=render_trending_grid(get_trending_movies_live()))

            live_search_btn.click(
                fn=on_live_movie_search,
                inputs=[live_search_input],
                outputs=[live_radar_status, live_radar_output]
            )
            live_search_input.submit(
                fn=on_live_movie_search,
                inputs=[live_search_input],
                outputs=[live_radar_status, live_radar_output]
            )

        # ==========================================
        # TAB 3: Content-Based Movie Matcher
        # ==========================================
        with gr.TabItem("🎯 Movie Matcher (Content-Based)", id="tab_matcher"):
            with gr.Row():
                with gr.Column(scale=5, elem_classes=["cinema-section-card"]):
                    gr.HTML('<div class="section-badge">⚙️ Feature Matching Engine & Seed Selector</div>')
                    gr.Markdown(
                        "Select a reference movie to extract its underlying feature soup (genres, director, cast, synopsis keywords) and discover closest matching films via TF-IDF Cosine Similarity."
                    )
                    gr.Markdown("💡 **Quick Seeds (Bollywood Classics & Global Hits):**")
                    with gr.Row():
                        seed_ddlj = gr.Button("💖 DDLJ (1995)", elem_classes=["quick-btn"], size="sm")
                        seed_3idiots = gr.Button("🌟 3 Idiots (2009)", elem_classes=["quick-btn"], size="sm")
                        seed_znmd = gr.Button("🏖️ ZNMD (2011)", elem_classes=["quick-btn"], size="sm")
                        seed_andhadhun = gr.Button("🕵️ Andhadhun (2018)", elem_classes=["quick-btn"], size="sm")
                    with gr.Row():
                        seed_wasseypur = gr.Button("⚔️ Gangs of Wasseypur", elem_classes=["quick-btn"], size="sm")
                        seed_inception = gr.Button("🍿 Inception (2010)", elem_classes=["quick-btn"], size="sm")
                        seed_summer = gr.Button("🎭 500 Days of Summer", elem_classes=["quick-btn"], size="sm")
                        seed_sholay = gr.Button("🔥 Sholay (1975)", elem_classes=["quick-btn"], size="sm")

                    movie_dropdown = gr.Dropdown(
                        choices=all_movie_titles,
                        value="Dilwale Dulhania Le Jayenge" if "Dilwale Dulhania Le Jayenge" in all_movie_titles else "Inception",
                        label="Select or Type Any Movie in the World (e.g. 'Dune 2', 'Kalki', 'Bramayugam', 'Stree 2')",
                        filterable=True,
                        allow_custom_value=True
                    )
                    with gr.Row():
                        num_recs = gr.Slider(minimum=2, maximum=8, value=4, step=1, label="Number of Matches")
                        min_rating_slider = gr.Slider(minimum=6.0, maximum=9.0, value=7.2, step=0.1, label="Min IMDb Rating")
                    with gr.Row():
                        genre_filter_dd = gr.Dropdown(choices=all_genres, value="All", label="Filter by Specific Genre (Optional)")
                        hybrid_slider = gr.Slider(
                            minimum=10, maximum=100, value=85, step=5,
                            label="Content Similarity Weight (%)",
                            info="Higher = stricter content match. Lower = boost top IMDb rated movies."
                        )
                    match_btn = gr.Button("🎬 Find Similar Movies", variant="primary")

                with gr.Column(scale=5, elem_classes=["cinema-section-card"]):
                    gr.HTML('<div class="section-badge">🎬 TF-IDF Cosine Similarity Matches</div>')
                    matcher_header = gr.Markdown("### 🎬 Recommendation Results")
                    default_seed = "Dilwale Dulhania Le Jayenge" if "Dilwale Dulhania Le Jayenge" in all_movie_titles else "Inception"
                    matcher_cards = gr.HTML(
                        value=render_movie_cards(recommender.get_similar_movies(default_seed, top_k=4))
                    )

            match_btn.click(
                fn=on_find_similar,
                inputs=[movie_dropdown, num_recs, min_rating_slider, genre_filter_dd, hybrid_slider],
                outputs=[matcher_header, matcher_cards]
            )
            movie_dropdown.change(
                fn=on_find_similar,
                inputs=[movie_dropdown, num_recs, min_rating_slider, genre_filter_dd, hybrid_slider],
                outputs=[matcher_header, matcher_cards]
            )

            seed_ddlj.click(fn=lambda: "Dilwale Dulhania Le Jayenge", outputs=[movie_dropdown])
            seed_3idiots.click(fn=lambda: "3 Idiots", outputs=[movie_dropdown])
            seed_znmd.click(fn=lambda: "Zindagi Na Milegi Dobara", outputs=[movie_dropdown])
            seed_andhadhun.click(fn=lambda: "Andhadhun", outputs=[movie_dropdown])
            seed_wasseypur.click(fn=lambda: "Gangs of Wasseypur", outputs=[movie_dropdown])
            seed_inception.click(fn=lambda: "Inception", outputs=[movie_dropdown])
            seed_summer.click(fn=lambda: "500 Days of Summer", outputs=[movie_dropdown])
            seed_sholay.click(fn=lambda: "Sholay", outputs=[movie_dropdown])

        # ==========================================
        # TAB 4: Mood & Vibe Explorer
        # ==========================================
        with gr.TabItem("🎭 Mood & Vibe Explorer", id="tab_vibe"):
            with gr.Column(elem_classes=["cinema-section-card"]):
                gr.HTML('<div class="section-badge">🎭 Emotional Atmosphere & Filters</div>')
                gr.Markdown(
                    "Filter the catalog by emotional vibe, preferred language (Hindi, English, International, or Both), genre categories, release era, and minimum rating."
                )
                with gr.Row():
                    mood_dropdown = gr.Dropdown(choices=all_moods, value="Mind-Bending", label="Target Mood / Vibe", scale=4)
                    language_dropdown = gr.Dropdown(
                        choices=[
                            "All Languages",
                            "Hindi (Bollywood / Indian)",
                            "English (Hollywood & Global)",
                            "Other / International (Korean, Japanese, French)"
                        ],
                        value="All Languages",
                        label="🌐 Preferred Language / Industry",
                        scale=4
                    )
                    genre_dropdown = gr.Dropdown(choices=all_genres, value="All", label="Genre Category", scale=4)

                gr.Markdown("💡 **Quick Language Choices:**")
                with gr.Row():
                    lang_btn_all = gr.Button("🌐 Both / All Languages", elem_classes=["quick-btn"], size="sm")
                    lang_btn_hindi = gr.Button("🇮🇳 Hindi / Bollywood Only", elem_classes=["quick-btn"], size="sm")
                    lang_btn_eng = gr.Button("🎬 English / Hollywood Only", elem_classes=["quick-btn"], size="sm")
                    lang_btn_intl = gr.Button("🌍 International / World Cinema", elem_classes=["quick-btn"], size="sm")

                with gr.Row():
                    rating_filter = gr.Slider(minimum=6.5, maximum=9.2, value=7.5, step=0.1, label="Minimum Rating", scale=4)
                    year_min_input = gr.Number(value=1980, label="Released After (Year)", precision=0, scale=4)
                    year_max_input = gr.Number(value=2026, label="Released Before (Year)", precision=0, scale=4)

                explore_btn = gr.Button("✨ Discover Matching Movies", variant="primary")

            with gr.Column(elem_classes=["cinema-section-card"]):
                gr.HTML('<div class="section-badge">✨ Curated Mood Matches</div>')
                vibe_status = gr.Markdown("Found matching titles:")
                vibe_cards = gr.HTML(
                    value=render_movie_cards(recommender.filter_movies(mood="Mind-Bending", min_rating=7.5, limit=6))
                )

            explore_btn.click(
                fn=on_filter_movies,
                inputs=[mood_dropdown, language_dropdown, genre_dropdown, rating_filter, year_min_input, year_max_input],
                outputs=[vibe_status, vibe_cards]
            )
            language_dropdown.change(
                fn=on_filter_movies,
                inputs=[mood_dropdown, language_dropdown, genre_dropdown, rating_filter, year_min_input, year_max_input],
                outputs=[vibe_status, vibe_cards]
            )
            mood_dropdown.change(
                fn=on_filter_movies,
                inputs=[mood_dropdown, language_dropdown, genre_dropdown, rating_filter, year_min_input, year_max_input],
                outputs=[vibe_status, vibe_cards]
            )
            genre_dropdown.change(
                fn=on_filter_movies,
                inputs=[mood_dropdown, language_dropdown, genre_dropdown, rating_filter, year_min_input, year_max_input],
                outputs=[vibe_status, vibe_cards]
            )

            lang_btn_all.click(fn=lambda: "All Languages", outputs=[language_dropdown])
            lang_btn_hindi.click(fn=lambda: "Hindi (Bollywood / Indian)", outputs=[language_dropdown])
            lang_btn_eng.click(fn=lambda: "English (Hollywood & Global)", outputs=[language_dropdown])
            lang_btn_intl.click(fn=lambda: "Other / International (Korean, Japanese, French)", outputs=[language_dropdown])

        # ==========================================
        # TAB 5: Dataset & Visual Analytics
        # ==========================================
        with gr.TabItem("📊 Analytics & Catalog Explorer", id="tab_analytics"):
            with gr.Column(elem_classes=["cinema-section-card"]):
                gr.HTML('<div class="section-badge">📈 Catalog Distribution Analytics</div>')
                with gr.Row():
                    plot_1 = gr.Plot(value=plot_genre_distribution(recommender.df), label="Genre Distribution")
                    plot_2 = gr.Plot(value=plot_rating_vs_year(recommender.df), label="Ratings by Era")

                with gr.Row():
                    plot_3 = gr.Plot(value=plot_mood_distribution(recommender.df), label="Mood Breakdown")
                    plot_4 = gr.Plot(value=plot_top_directors(recommender.df), label="Top Directors")

            with gr.Column(elem_classes=["cinema-section-card"]):
                gr.HTML('<div class="section-badge">🔍 Search & Inspect Movie Database</div>')
                dataset_table = gr.DataFrame(
                    value=recommender.df[["title", "year", "language", "genre", "director", "rating", "mood_tags", "keywords"]],
                    headers=["Title", "Year", "Language", "Genre", "Director", "Rating", "Mood", "Keywords"],
                    interactive=False,
                    wrap=True
                )

        # ==========================================
        # TAB 6: Academic Report & Viva Guide
        # ==========================================
        with gr.TabItem("📘 Project Report & Viva Guide", id="tab_docs"):
            with gr.Column(elem_classes=["cinema-section-card"]):
                gr.HTML('<div class="section-badge">📘 Course Mini Project Report & Viva Examination Guide</div>')
                gr.Markdown("""
# 📘 AI Movie Recommendation System — Mini Project Report
**Course:** SEM 5 Flexi Credit (Continuous Assessment CA3)  
**Interface:** Gradio GUI Framework  
**Architectures:** ReAct Agent Tool Calling, Real-Time Knowledge Retrieval, Multi-Model LLMs (Groq LPU / Gemini), TF-IDF Cosine Similarity.

---

### 1. ReAct Tool-Calling Agent Architecture
Modern recommendation systems go beyond static lookups. CineAgent implements a **ReAct (Reasoning + Acting)** Agent workflow:
1. **User Query Analysis**: The agent determines whether the query requires subjective recommendation or real-time live data.
2. **Dynamic Tool Invocation**: If the user asks about live streaming availability (*"Where can I watch..."*), trending box office (*"What's trending right now?"*), or real-time release details, the agent invokes `src/realtime_fetcher.py`.
3. **Knowledge Augmentation**: Real-time facts (distributors, OTT platforms, verified plot synopsis) are fetched from live web knowledge graphs and injected into the LLM context.
4. **Grounded Synthesis**: The LLM synthesizes an accurate response citing official streaming platforms alongside high-definition live posters.

---

### 2. Multi-Model LLM Execution
- **Groq Cloud LPU (`openai/gpt-oss-120b`, `qwen/qwen3.8-27b`)**: Language Processing Units designed for sub-second deterministic inference, powering global movie retrieval.
- **Google Gemini API (`gemini-1.5-flash`)**: Multi-turn dialogue with large context window.
- **Local Fallback Engine**: Mathematical TF-IDF and Cosine Similarity vector space matching.

---

### 3. Top Viva & Evaluation Questions

| # | Question | Model Answer for Viva |
|---|---|---|
| **1** | **How does the Agent fetch real-time movie data?** | It uses an agentic tool-calling pipeline that interfaces with live REST APIs (Wikipedia Knowledge Graph & streaming platform detectors) to retrieve current OTT availability and real-time box office facts. |
| **2** | **What is the ReAct agent framework?** | ReAct combines Reasoning (LLM thought generation) with Acting (calling external tools to fetch live facts), allowing the agent to answer questions beyond its training cutoff. |
| **3** | **How does the system support multiple LLM models?** | It features a unified provider abstraction supporting Groq LPUs (`openai/gpt-oss-120b`), Google Gemini, and an offline TF-IDF heuristic engine. |
| **4** | **What is TF-IDF?** | Term Frequency-Inverse Document Frequency calculates the importance of words in a document relative to a corpus, amplifying unique thematic keywords. |
| **5** | **Why Cosine Similarity over Euclidean Distance?** | Cosine similarity measures vector angles rather than lengths, making it invariant to the number of words in a plot summary. |
                """)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 7860))

    demo.launch(
        server_name="0.0.0.0",
        server_port=port,
        inbrowser=False,
        theme=cinema_theme,
        css=CINEMA_CSS,
        head=CINEMA_HEAD
    )