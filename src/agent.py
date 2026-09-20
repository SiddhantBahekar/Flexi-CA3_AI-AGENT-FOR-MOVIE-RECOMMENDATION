"""
AI Agent for Movie Recommendation
Combines Intent Parsing, Mood Detection, Multi-Turn Memory,
Real-Time Live Data Tool Calling, and Multi-Model LLM Execution (Groq / Gemini / Local).
"""

import re
import json
import os
import sys
import urllib.request
import urllib.parse
from functools import lru_cache

# Ensure workspace root is in sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
if hasattr(sys.stdout, 'reconfigure'):
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

try:
    from src.recommender import MovieRecommender
except ImportError:
    from recommender import MovieRecommender

try:
    from src.realtime_fetcher import (
        search_live_movie_data,
        get_trending_movies_live,
        detect_streaming_platforms,
        resolve_movie_title,
        TITLE_ALIASES,
        STREAMING_GROUND_TRUTH
    )
except ImportError:
    from realtime_fetcher import (
        search_live_movie_data,
        get_trending_movies_live,
        detect_streaming_platforms,
        resolve_movie_title,
        TITLE_ALIASES,
        STREAMING_GROUND_TRUTH
    )


# --- In-memory cache for live movie posters ---
POSTER_CACHE = {}

def fetch_live_poster(title, year=None):
    """
    Fetches real theatrical poster thumbnail for any movie in the world
    using Wikipedia REST API with fallback to high-quality cinema backdrops.
    """
    clean_title = title.strip()
    cache_key = f"{clean_title.lower()}_{year}"
    if cache_key in POSTER_CACHE:
        return POSTER_CACHE[cache_key]

    queries = [
        f"{clean_title} ({year} film)" if year else f"{clean_title} (film)",
        f"{clean_title} (film)",
        clean_title
    ]

    for q in queries:
        formatted = q.replace(" ", "_")
        url = f"https://en.wikipedia.org/api/rest_v1/page/summary/{urllib.parse.quote(formatted)}"
        req = urllib.request.Request(
            url,
            headers={"User-Agent": "CineAgentMovieBot/1.0 (academic mini project; mailto:student@symbiosis.ac.in)"}
        )
        try:
            with urllib.request.urlopen(req, timeout=3.5) as resp:
                data = json.loads(resp.read().decode("utf-8"))
                thumb = data.get("thumbnail", {}).get("source")
                if thumb:
                    POSTER_CACHE[cache_key] = thumb
                    return thumb
        except Exception:
            continue

    fallback = "https://images.unsplash.com/photo-1489599849927-2ee91cede3ba?w=400&q=80"
    POSTER_CACHE[cache_key] = fallback
    return fallback


class MovieAgent:
    def __init__(self, recommender: MovieRecommender):
        self.recommender = recommender
        self.conversation_history = []
        self.user_state = {
            "preferred_genres": set(),
            "preferred_moods": set(),
            "favorite_movies": set(),
            "disliked_movies": set(),
            "target_era": None,
            "min_rating": 7.0
        }

        # Mood keyword mappings
        self.mood_map = {
            "mind-bending": ["mind-bending", "twist", "confusing", "complex", "psychological", "trippy", "intellectual", "paradox", "time travel", "multiverse"],
            "feel-good": ["feel-good", "happy", "uplifting", "cheer me up", "wholesome", "smile", "lighthearted", "fun", "warm", "comfort"],
            "adrenaline rush": ["action", "intense", "adrenaline", "fast-paced", "explosion", "fight", "chase", "thrilling", "superhero"],
            "dark & gritty": ["dark", "gritty", "noir", "crime", "bleak", "depressing", "violent", "grim", "mafia", "gangster"],
            "romantic/cozy": ["romantic", "romance", "love", "date night", "cozy", "cute", "sweet", "lovers", "heartbreak"],
            "spooky & chilling": ["scary", "spooky", "horror", "creepy", "ghost", "halloween", "chilling", "eerie", "jump scare"],
            "epic & grand": ["epic", "grand", "historical", "war", "huge", "cinematic", "scale", "battle", "kingdom", "mythology"],
            "thought-provoking": ["philosophical", "deep", "thought-provoking", "meaningful", "existential", "morality", "documentary"]
        }

    def reset(self):
        """Clears conversation memory and user profile state."""
        self.conversation_history = []
        self.user_state = {
            "preferred_genres": set(),
            "preferred_moods": set(),
            "favorite_movies": set(),
            "disliked_movies": set(),
            "target_era": None,
            "min_rating": 7.0
        }

    def extract_intent(self, text):
        """Extracts user desires: moods, genres, mentioned titles, min ratings."""
        text_lower = text.lower()

        detected_moods = []
        for mood, keywords in self.mood_map.items():
            if any(kw in text_lower for kw in keywords):
                detected_moods.append(mood)

        detected_genres = []
        for genre in self.recommender.get_all_genres():
            if genre.lower() in text_lower:
                detected_genres.append(genre)

        mentioned_movies = []
        for title in self.recommender.get_all_titles():
            pattern = r'\b' + re.escape(title.lower()) + r'\b'
            if re.search(pattern, text_lower):
                mentioned_movies.append(title)

        # High-precision scan: Check known aliases and global streaming ground-truth titles (sorted by longest first)
        sorted_aliases = sorted(TITLE_ALIASES.items(), key=lambda x: len(x[0]), reverse=True)
        for alias_key, canon_val in sorted_aliases:
            if len(alias_key) >= 2:
                pattern = r'\b' + re.escape(alias_key) + r'\b'
                if re.search(pattern, text_lower):
                    if canon_val not in mentioned_movies:
                        mentioned_movies.append(canon_val)

        sorted_gt = sorted(STREAMING_GROUND_TRUTH.keys(), key=lambda x: len(x), reverse=True)
        for gt_key in sorted_gt:
            if len(gt_key) >= 3:
                pattern = r'\b' + re.escape(gt_key) + r'\b'
                if re.search(pattern, text_lower):
                    cap_val = gt_key.title()
                    if cap_val not in mentioned_movies:
                        mentioned_movies.append(cap_val)

        min_rating = None
        rating_match = re.search(r'(above|over|rated|at least|minimum)\s+(\d+(\.\d+)?)', text_lower)
        if rating_match:
            try:
                min_rating = float(rating_match.group(2))
            except ValueError:
                pass

        # Invalid words that should not be parsed as movie titles
        stop_title_words = {
            'it', 'this', 'that', 'any', 'the', 'a', 'an', 'movie', 'film', 'movies', 'films',
            'something', 'recommendation', 'recommendations', 'good movie', 'best movie',
            'recommend', 'suggest', 'find', 'show', 'watch', 'new', 'latest', 'trending',
            'top', 'best', 'good', 'great', 'favorite', 'action', 'comedy', 'drama',
            'horror', 'thriller', 'sci-fi', 'sci fi', 'romance', 'romantic', 'streaming', 'platform',
            'where', 'what', 'who', 'how', 'when', 'ott', 'available', 'stream', 'is', 'are', 'now', 'right now'
        }

        # Candidate movie extraction for any film in world cinema
        candidate_patterns = [
            # Similar movies/shows patterns (e.g. "recommed movies like Mirzapur", "movies like Interstellar", "shows like Breaking Bad")
            r'(?:recommend|recommed|recomended|recommand|recommened|reccomend|suggest|sugest|find|show|give|look for)?\s*(?:me\s+)?(?:movies|movie|films|film|shows|show|series|cinema|titles)?\s*(?:like|similar\s+to|akin\s+to)\s+([a-z0-9\s:\'\-]+?)(?:\s*\?|\s*$)',

            # Streaming questions
            r'(?:where\s+(?:is|are|can\s+i\s+watch|to\s+watch|can\s+i\s+stream|to\s+stream|can\s+i\s+find))\s+(?:the\s+)?([a-z0-9\s:\'\-]+?)(?:\s+streaming|\s+available|\s+on\s+ott|\s+on|\s+right\s+now|\s*\?|\s*$)',
            r'(?:streaming\s+platform|ott\s+platform|platform)\s+(?:for|of)\s+(?:the\s+)?([a-z0-9\s:\'\-]+?)(?:\s+movie|\s+film|\s*\?|\s*$)',
            r'(?:which\s+platform\s+is)\s+(?:the\s+)?([a-z0-9\s:\'\-]+?)(?:\s+streaming\s+on|\s+streaming|\s+available\s+on|\s*\?|\s*$)',
            r'([a-z0-9\s:\'\-]+?)\s+(?:streaming\s+platform|ott\s+platform|streaming\s+on|where\s+to\s+watch)',
            r'([a-z0-9\s:\'\-]+?)\s+(?:streaming|where\s+to\s+stream)',

            # General movie knowledge questions
            r'(?:do you know|have you heard of|what do you know|tell me|give me\s+(?:some\s+)?(?:info|information)|information|info)\s+(?:about\s+)?(?:the\s+)?([a-z0-9\s:\'\-]+?)(?:\s+movie|\s+film|\s+cast|\s*\?|\s*$)',
            r'(?:who directed|who is in|who stars in|cast of|director of|details of|synopsis of|rating of|release date of|story of)\s+(?:the\s+)?([a-z0-9\s:\'\-]+?)(?:\s+movie|\s+film|\s*\?|\s*$)',
            r'(?:what is|what about)\s+(?:the\s+)?([a-z0-9\s:\'\-]+?)(?:\s+about|\s+movie|\s+film|\s*\?|\s*$)',
            r'(?:is|can you tell me about|have you watched)\s+(?:the\s+)?([a-z0-9\s:\'\-]+?)(?:\s+a\s+real\s+movie|\s+a\s+good\s+movie|\s+a\s+movie|\s+a\s+film|\s+good|\s*\?|\s*$)',
            r'["\']([a-z0-9\s:\'\-]+)["\']',
            r'\b([a-z0-9\s:\'\-]{3,30}?)\s+(?:movie|film)\b'
        ]

        def clean_candidate_text(cand):
            if not cand:
                return None
            words = cand.lower().split()
            # Strip question / auxiliary / recommendation words from beginning
            lead_stop = {'where', 'what', 'who', 'is', 'are', 'can', 'i', 'watch', 'stream', 'to', 'the', 'a', 'an', 'on', 'recommend', 'recommed', 'recomended', 'recommand', 'suggest', 'sugest', 'movies', 'movie', 'films', 'film', 'shows', 'show', 'series', 'like', 'similar'}
            while words and words[0] in lead_stop:
                words.pop(0)
            # Strip trailing stop words
            trail_stop = {'streaming', 'available', 'now', 'right', 'online', 'ott', 'platform', 'movie', 'film'}
            while words and words[-1] in trail_stop:
                words.pop(-1)
            if not words or len(words) < 1:
                return None
            joined = " ".join(words)
            if all(w in stop_title_words for w in words):
                return None
            return joined.title()

        candidate_title = None
        clean_prompt = re.sub(r'[\?!.,]+$', '', text_lower).strip()
        for p in candidate_patterns:
            m = re.search(p, clean_prompt)
            if m:
                cand = m.group(1).strip()
                cleaned = clean_candidate_text(cand)
                if cleaned:
                    candidate_title = resolve_movie_title(cleaned)
                    break

        # Standalone short query fallback (1-4 words, e.g. "Bramayugam", "Kalki 2898 AD", "Dhurandhar 2025")
        if not candidate_title and not mentioned_movies:
            words = clean_prompt.split()
            rec_verbs = ('recommend', 'recommed', 'recomended', 'recommand', 'recommened', 'reccomend', 'suggest', 'sugest', 'show me', 'give me', 'find me', 'i want', 'i feel', 'i need', 'what should i watch', 'movies like', 'films like', 'shows like', 'movie like', 'film like', 'recommed movies')
            if 1 <= len(words) <= 4 and clean_prompt not in stop_title_words:
                if not any(clean_prompt.startswith(v) for v in rec_verbs):
                    cleaned = clean_candidate_text(clean_prompt)
                    if cleaned:
                        candidate_title = resolve_movie_title(cleaned)

        if candidate_title:
            if not mentioned_movies:
                mentioned_movies.append(candidate_title)
            elif candidate_title.lower() not in [m.lower() for m in mentioned_movies]:
                mentioned_movies.append(candidate_title)

        # Check for real-time tool queries
        realtime_intent = None
        streaming_kw = ["where to watch", "where can i watch", "where to stream", "where is", "where are", "streaming on", "streaming platform", "which ott", "on netflix", "on prime", "on disney", "ott platform", "which platform", "stream", "streaming"]
        is_similar_query = (
            any(kw in text_lower for kw in ["like", "similar to", "akin to", "recommend", "recommed", "recomended", "suggest", "sugest"]) and
            any(w in text_lower for w in ["movie", "movies", "film", "films", "show", "shows", "series", "like", "similar"])
        )
        if any(w in text_lower for w in streaming_kw):
            realtime_intent = "streaming"
        elif any(w in text_lower for w in ["trending", "box office", "highest grossing", "in theatres", "current movies", "latest releases", "new releases"]):
            realtime_intent = "trending"
        elif mentioned_movies and not is_similar_query:
            realtime_intent = "movie_info"

        return {
            "moods": detected_moods,
            "genres": detected_genres,
            "movies": mentioned_movies,
            "min_rating": min_rating,
            "realtime_intent": realtime_intent
        }

    def execute_realtime_tools(self, intent, user_message):
        """
        Agent tool calling: queries real-time movie knowledge base
        and returns live factual context for LLM prompt.
        """
        tool_findings = []
        movie_cards = []

        if intent["realtime_intent"] == "trending":
            trending_list = get_trending_movies_live()
            tool_findings.append("### 🔴 Real-Time Trending Movies Worldwide:\n" + "\n".join([
                f"- **{m['title']}** ({m['year']}) | {m['genre']} | ⭐ {m['rating']}/10 | Highlights: {m['highlight']} | Stream: {', '.join(m['streaming_platforms'])}"
                for m in trending_list[:4]
            ]))
            for m in trending_list[:4]:
                movie_cards.append({
                    "title": m["title"],
                    "year": m["year"],
                    "genre": m["genre"],
                    "director": "Top Visionary",
                    "cast": m["highlight"],
                    "rating": m["rating"],
                    "overview": m["overview"],
                    "mood_tags": "Trending, Acclaimed",
                    "explanation": f"Streaming on: {', '.join(m['streaming_platforms'])}",
                    "poster_url": m["poster_url"],
                    "similarity_score": 99.0
                })
        elif intent["movies"]:
            target_movie = intent["movies"][0]
            live_data = search_live_movie_data(target_movie)
            platforms_str = ", ".join(live_data.get("streaming_platforms", []))
            
            tool_findings.append(
                f"### 🔴 Live Ground-Truth Facts for '{live_data['title']}':\n"
                f"- Official Title: {live_data['title']}\n"
                f"- Release Year / Status: {live_data.get('year', 'N/A')}\n"
                f"- Director: {live_data.get('director', 'Verified Filmmaker')}\n"
                f"- Primary Cast: {live_data.get('cast', 'Ensemble Cast')}\n"
                f"- Live Knowledge Graph Description: {live_data.get('description', '')}\n"
                f"- Verified Synopsis: {live_data.get('overview', '')[:500]}\n"
                f"- Streaming Availability: {platforms_str}\n"
                f"- Source: {live_data.get('source', 'Wikipedia Real-Time Knowledge Graph')}"
            )
            movie_cards.append({
                "title": live_data["title"],
                "year": live_data.get("year", ""),
                "genre": live_data.get("description", "Feature Film"),
                "director": live_data.get("director", "Verified Filmmaker"),
                "cast": live_data.get("cast") or f"Stream: {platforms_str}",
                "rating": 8.8,
                "overview": live_data.get("overview", ""),
                "mood_tags": "Live Ground Truth",
                "explanation": f"Verified Real-Time Intelligence • Stream: {platforms_str}",
                "poster_url": live_data.get("poster_url", ""),
                "similarity_score": 100.0
            })

        return "\n\n".join(tool_findings), movie_cards

    def generate_local_recommendations(self, intent, user_message, top_k=3):
        """Generates recommendations from local dataset."""
        candidates = []
        thought_process = []

        for m in intent["moods"]:
            self.user_state["preferred_moods"].add(m)
        for g in intent["genres"]:
            self.user_state["preferred_genres"].add(g)
        for mv in intent["movies"]:
            self.user_state["favorite_movies"].add(mv)
        if intent["min_rating"]:
            self.user_state["min_rating"] = intent["min_rating"]

        if intent["movies"]:
            primary_movie = intent["movies"][0]
            thought_process.append(f"Detected interest in '{primary_movie}'. Querying content-based similarity engine...")
            similar = self.recommender.get_similar_movies(
                primary_movie,
                top_k=top_k,
                min_rating=self.user_state["min_rating"]
            )
            for m in similar:
                if m["title"] not in self.user_state["favorite_movies"]:
                    candidates.append(m)
        elif intent["moods"]:
            target_mood = intent["moods"][0]
            thought_process.append(f"Detected emotional vibe request: '{target_mood}'. Matching mood vectors & ratings...")
            filtered = self.recommender.filter_movies(
                mood=target_mood,
                min_rating=self.user_state["min_rating"],
                limit=top_k * 2
            )
            candidates.extend(filtered[:top_k])
        elif intent["genres"]:
            target_genre = intent["genres"][0]
            thought_process.append(f"Filtering catalog for genre '{target_genre}' with rating >= {self.user_state['min_rating']}...")
            filtered = self.recommender.filter_movies(
                genre=target_genre,
                min_rating=self.user_state["min_rating"],
                limit=top_k * 2
            )
            candidates.extend(filtered[:top_k])
        else:
            thought_process.append("Parsing natural language query against TF-IDF keyword corpus...")
            recs = self.recommender.recommend_by_query(
                user_message,
                top_k=top_k,
                min_rating=self.user_state["min_rating"]
            )
            candidates.extend(recs)

        unique_candidates = []
        seen = set(self.user_state["disliked_movies"]).union(self.user_state["favorite_movies"])
        for m in candidates:
            if m["title"] not in seen:
                seen.add(m["title"])
                unique_candidates.append(m)

        if not unique_candidates:
            thought_process.append("No direct filter match. Falling back to top universally acclaimed selections...")
            fallback = self.recommender.filter_movies(min_rating=8.2, limit=top_k)
            unique_candidates = fallback

        return unique_candidates[:top_k], " ➜ ".join(thought_process)

    def chat_offline(self, user_message):
        """Local AI Agent conversation logic."""
        msg_clean = user_message.strip().lower()

        if any(g == msg_clean or msg_clean.startswith(g + " ") for g in ["hi", "hello", "hey", "hola", "sup", "greetings"]):
            reply = (
                "👋 **Hello! I'm your CineAgent AI.**\n\n"
                "I can recommend movies across **all of cinema history** based on your **mood, favorite movies, actors, directors, or genres**.\n"
                "I also support **Real-Time Data Lookup** (where to stream, live box office, trending movies).\n\n"
                "💡 *Try asking me:*\n"
                "- *'What movies are trending right now?'*\n"
                "- *'Where can I stream Inception or Oppenheimer?'*\n"
                "- *'I want a mind-bending sci-fi movie with great twists like Interstellar.'*\n"
                "- *'Recommend an intense, epic Indian cinema action masterpiece.'*"
            )
            return reply, None, "Agent State: Ready with Real-Time & Recommendation Tools."

        intent = self.extract_intent(user_message)

        # Check if real-time tool applies even in offline/heuristic mode
        if intent["realtime_intent"]:
            live_text, live_cards = self.execute_realtime_tools(intent, user_message)
            if live_cards:
                reply = f"Here is the latest real-time information regarding your query:\n\n{live_text}"
                return reply, live_cards, f"🛠️ Real-Time Tool Triggered [{intent['realtime_intent']}]"

        recs, thought = self.generate_local_recommendations(intent, user_message, top_k=3)

        response_lines = []
        if intent["movies"]:
            primary = intent["movies"][0]
            live_src = search_live_movie_data(primary)
            src_stream = ", ".join(live_src.get("streaming_platforms", []))
            stream_note = f" *(streaming on {src_stream})*" if src_stream and "Not currently" not in src_stream else ""
            response_lines.append(f"Since you're looking for cinema like **{primary}**{stream_note}, here are top-tier films with matching gritty themes & atmosphere:")
        elif intent["moods"]:
            response_lines.append(f"Setting the mood to **{intent['moods'][0].title()}**. Handpicked recommendations:")
        elif intent["genres"]:
            response_lines.append(f"Top-rated **{', '.join(intent['genres'])}** titles:")
        else:
            response_lines.append("Here are top recommendations picked by my recommendation engine:")

        return "\n".join(response_lines), recs, thought

    def _call_groq_api(self, user_message, api_key, model="openai/gpt-oss-120b"):
        """
        Calls Groq Cloud API for ultra-fast global movie recommendations and tool integration.
        """
        clean_key = api_key.strip()
        from groq import Groq
        client = Groq(api_key=clean_key)

        intent = self.extract_intent(user_message)
        realtime_context = ""
        tool_cards = []

        # Tool calling check
        if intent["realtime_intent"]:
            realtime_context, tool_cards = self.execute_realtime_tools(intent, user_message)

        system_prompt = (
            "You are CineAgent, an expert, charismatic AI movie connoisseur with comprehensive knowledge "
            "of ALL global cinema history (Hollywood, Bollywood, European, Asian cinema, classics, indies, anime).\n"
            "You have access to live real-time movie tools and streaming availability data.\n"
        )
        if realtime_context:
            system_prompt += (
                f"\n=== REAL-TIME GROUND-TRUTH DATA FROM LIVE TOOLS ===\n"
                f"{realtime_context}\n"
                f"STRICT ACCURACY MANDATE:\n"
                f"- The user's query directly concerns the above movie/topic.\n"
                f"- You MUST use the above verified facts (actual title, release year, director, cast, language, synopsis).\n"
                f"- NEVER invent, assume, or hallucinate fake directors, fake actors, or fake languages!\n"
                f"- If asked 'do you know about X', confirm knowledge using the exact real-time facts above!\n"
            )

        system_prompt += (
            "\nWhen the user asks for recommendations, mentions a movie, or discusses cinema, recommend or discuss 3 to 4 fitting films.\n\n"
            "CRITICAL FORMAT RULES:\n"
            "1. DO NOT write 'Part 1', 'Part 2', or any headers. Begin directly with your warm, charismatic conversational response to the user.\n"
            "2. Highlight directing style, plot intrigue, and streaming options in your message (under 160 words).\n"
            "3. At the end of your message, provide exactly ONE valid JSON code block enclosed in ```json ... ``` with this exact schema:\n"
            "```json\n"
            "{\n"
            '  "thought": "Brief 1-sentence reasoning of user taste & findings",\n'
            '  "movies": [\n'
            "    {\n"
            '      "title": "Movie Title",\n'
            '      "year": 2023,\n'
            '      "genre": "Genre1, Genre2",\n'
            '      "director": "Director Name",\n'
            '      "cast": "Actor 1, Actor 2",\n'
            '      "rating": 8.5,\n'
            '      "overview": "Engaging 2-sentence synopsis",\n'
            '      "mood_tags": "Mood1, Mood2",\n'
            '      "explanation": "Why this specific film was chosen or where to watch"\n'
            "    }\n"
            "  ]\n"
            "}\n"
            "```\n"
            "IMPORTANT: Inside the JSON strings, NEVER use unescaped double quotes (use single quotes ' instead). No trailing commas."
        )

        messages = [
            {"role": "system", "content": system_prompt}
        ]

        for h in self.conversation_history[-4:]:
            messages.append({"role": h["role"], "content": h["content"]})

        messages.append({"role": "user", "content": user_message})

        selected_model = model
        try:
            chat_completion = client.chat.completions.create(
                model=selected_model,
                messages=messages,
                temperature=0.6,
                max_tokens=1400
            )
        except Exception:
            selected_model = "qwen/qwen3.8-27b"
            chat_completion = client.chat.completions.create(
                model=selected_model,
                messages=messages,
                temperature=0.6,
                max_tokens=1400
            )

        raw_content = chat_completion.choices[0].message.content

        tool_tag = f" ➜ 🛠️ Real-Time Tool [{intent['realtime_intent'].upper()}]" if intent["realtime_intent"] else ""
        thought = f"Groq [{selected_model}]{tool_tag} completed."
        raw_movies = []

        # Extract JSON code block
        json_str = None
        json_match = re.search(r'```(?:json)?\s*(\{[\s\S]*?\})\s*```', raw_content)
        if json_match:
            json_str = json_match.group(1)
        else:
            match_brace = re.search(r'(\{[\s\S]*"movies"[\s\S]*\})', raw_content)
            if match_brace:
                json_str = match_brace.group(1)

        # Layer 1: Standard JSON parse
        if json_str:
            try:
                parsed = json.loads(json_str)
                thought = parsed.get("thought", thought) + tool_tag
                raw_movies = parsed.get("movies", [])
            except Exception:
                # Layer 2: Sanitize trailing commas and common syntax mistakes
                try:
                    cleaned_json = re.sub(r',\s*([\]\}])', r'\1', json_str)
                    cleaned_json = re.sub(r'[\x00-\x1f\x7f-\x9f]', ' ', cleaned_json)
                    parsed = json.loads(cleaned_json)
                    thought = parsed.get("thought", thought) + tool_tag
                    raw_movies = parsed.get("movies", [])
                except Exception:
                    # Layer 3: Regex extract individual movie blocks
                    title_matches = re.findall(
                        r'"title"\s*:\s*"([^"]+)"',
                        json_str
                    )
                    year_matches = re.findall(r'"year"\s*:\s*(\d{4})', json_str)
                    genre_matches = re.findall(r'"genre"\s*:\s*"([^"]*)"', json_str)
                    overview_matches = re.findall(r'"overview"\s*:\s*"([^"]*)"', json_str)

                    for i, t in enumerate(title_matches):
                        raw_movies.append({
                            "title": t,
                            "year": year_matches[i] if i < len(year_matches) else "",
                            "genre": genre_matches[i] if i < len(genre_matches) else "Action, Thriller",
                            "overview": overview_matches[i] if i < len(overview_matches) else f"Curated cinema experience related to {t}."
                        })

        # Layer 4: Fallback to extract bolded movie titles from text if no movies parsed
        if not raw_movies:
            bold_titles = re.findall(r'\*\*([A-Za-z0-9\s:’\'\-]+)\*\*', raw_content)
            for bt in bold_titles:
                clean_bt = bt.strip()
                if len(clean_bt) > 2 and clean_bt.lower() not in ["part 1", "part 2", "chat", "movies", "recommendations", "thought", "summary", "note", "why"]:
                    raw_movies.append({
                        "title": clean_bt,
                        "year": "Recent",
                        "genre": "Cinema",
                        "overview": f"Curated title discussed in connection to {clean_bt}."
                    })
                if len(raw_movies) >= 4:
                    break

        movie_cards = []
        for m in raw_movies:
            title = m.get("title", "").strip()
            if not title:
                continue
            year = m.get("year", "")
            local_match = self.recommender.get_movie_by_title(title)
            poster_url = None
            if local_match and local_match.get("poster_url"):
                poster_url = local_match["poster_url"]
            else:
                poster_url = fetch_live_poster(title, year)

            movie_cards.append({
                "title": title,
                "year": year,
                "genre": m.get("genre", "Drama, Thriller"),
                "director": m.get("director", "Acclaimed Director"),
                "cast": m.get("cast", ""),
                "rating": float(m.get("rating", 8.2)),
                "overview": m.get("overview", "An engaging and captivating film experience."),
                "mood_tags": m.get("mood_tags", "Thrilling"),
                "explanation": m.get("explanation", "Recommended by CineAgent AI"),
                "poster_url": poster_url,
                "similarity_score": 98.0
            })

        # Prioritize ground-truth tool card at position 0 if user inquired about a specific movie
        if tool_cards:
            target_title = tool_cards[0]["title"].lower()
            existing_idx = next((i for i, c in enumerate(movie_cards) if c["title"].lower() == target_title), None)
            if existing_idx is not None:
                movie_cards[existing_idx] = tool_cards[0]
            else:
                movie_cards.insert(0, tool_cards[0])

        # Clean conversational reply text
        clean_text = raw_content
        if json_match:
            clean_text = clean_text.replace(json_match.group(0), "")
        clean_text = re.sub(r'```(?:json)?[\s\S]*?```', '', clean_text)
        clean_text = re.sub(r'^(?:Part\s*1\s*[-–—:]*\s*(?:Chat)?|Response:)\s*', '', clean_text.strip(), flags=re.IGNORECASE)
        clean_text = clean_text.strip()

        return clean_text, movie_cards, thought

    def _call_gemini_api(self, user_message, api_key, model="gemini-1.5-flash"):
        """Calls Google Gemini API for conversational agent with live movie reasoning."""
        intent = self.extract_intent(user_message)
        recs, thought = self.generate_local_recommendations(intent, user_message, top_k=3)

        movies_context = "\n".join([
            f"- Title: {m['title']} ({m.get('year', '')}), Genre: {m.get('genre', '')}, Rating: {m.get('rating', '8.0')}/10, Streaming: {m.get('explanation', '')}, Synopsis: {m.get('overview', '')[:200]}"
            for m in recs
        ])

        system_instruction = (
            "You are CineAgent, an expert, charismatic AI movie connoisseur. "
            "A recommendation engine has selected the following best matching candidates from the catalog:\n"
            f"{movies_context}\n\n"
            "Respond conversationally to the user. Enthusiastically explain why these movies match their taste or mood, "
            "highlighting creative aspects like cinematography, story twists, or director style. Mention verified streaming services where available. Keep it under 180 words."
        )

        clean_model = model.replace("models/", "").strip()
        if not clean_model or "gemini" not in clean_model.lower():
            clean_model = "gemini-1.5-flash"

        url = f"https://generativelanguage.googleapis.com/v1beta/models/{clean_model}:generateContent?key={api_key.strip()}"
        payload = {
            "contents": [
                {
                    "parts": [
                        {"text": f"{system_instruction}\n\nUser request: {user_message}"}
                    ]
                }
            ],
            "generationConfig": {
                "temperature": 0.7,
                "maxOutputTokens": 500
            }
        }

        req = urllib.request.Request(
            url,
            data=json.dumps(payload).encode("utf-8"),
            headers={"Content-Type": "application/json"}
        )

        try:
            with urllib.request.urlopen(req, timeout=12) as resp:
                data = json.loads(resp.read().decode("utf-8"))
                candidates = data.get("candidates", [])
                if candidates:
                    parts = candidates[0].get("content", {}).get("parts", [])
                    if parts and "text" in parts[0]:
                        llm_text = parts[0]["text"]
                        return llm_text, recs, f"Google Gemini [{clean_model}] inference completed."
                return "I've analyzed your cinematic tastes and selected the finest recommendations below!", recs, f"Google Gemini [{clean_model}] completed."
        except urllib.error.HTTPError as e:
            err_detail = ""
            try:
                err_data = json.loads(e.read().decode("utf-8", errors="ignore"))
                err_detail = err_data.get("error", {}).get("message", "")
            except Exception:
                pass
            if not err_detail:
                err_detail = f"HTTP {e.code}: {e.reason}"
            raise RuntimeError(f"Gemini API Error: {err_detail}")

    def chat(self, user_message, api_key=None, api_provider="Groq", model="openai/gpt-oss-120b"):
        """
        Unified multi-model chat entry point.
        Supports Groq (default), Google Gemini, or Offline Catalog.
        """
        # Distinguish keys so a Groq key (gsk_...) is never accidentally passed to Gemini
        clean_key = (api_key or "").strip()
        groq_key = (clean_key if clean_key.startswith("gsk_") else None) or os.environ.get("GROQ_API_KEY", "")
        gemini_key = (clean_key if not clean_key.startswith("gsk_") else None) or os.environ.get("GEMINI_API_KEY", "")

        self.conversation_history.append({"role": "user", "content": user_message})

        if api_provider.lower().startswith("groq") and groq_key and groq_key.strip():
            try:
                reply, recs, thought = self._call_groq_api(user_message, groq_key, model=model)
                self.conversation_history.append({"role": "assistant", "content": reply})
                return reply, recs, f"⚡ {thought}"
            except Exception as e:
                reply, recs, thought = self.chat_offline(user_message)
                error_summary = str(e)
                if "401" in error_summary:
                    notice = "*(⚠️ Note: Groq API Key invalid or expired. Switched to Offline Engine)*\n\n"
                else:
                    notice = f"*(⚠️ Note: Groq connection notice: {error_summary[:60]}... Switched to Offline Engine)*\n\n"
                reply = notice + reply
                self.conversation_history.append({"role": "assistant", "content": reply})
                return reply, recs, f"Offline Fallback ➜ {thought}"

        elif api_provider.lower().startswith("gemini"):
            # Check if user provided a Groq key while selecting Gemini:
            if clean_key.startswith("gsk_") and not os.environ.get("GEMINI_API_KEY"):
                reply, recs, thought = self.chat_offline(user_message)
                notice = (
                    "*(⚠️ Notice: You selected Google Gemini API, but the key entered is a Groq key (`gsk_...`). "
                    "Please enter your Google Gemini API key (starts with `AIzaSy...`) in the API Key box, or switch back to Groq Cloud LPU.)*\n\n"
                )
                self.conversation_history.append({"role": "assistant", "content": notice + reply})
                return notice + reply, recs, f"Config Notice ➜ {thought}"

            if not gemini_key or not gemini_key.strip():
                reply, recs, thought = self.chat_offline(user_message)
                notice = (
                    "*(⚠️ Notice: Google Gemini API requires a Gemini API key. "
                    "Please enter your Gemini API key in the API Key box or set GEMINI_API_KEY in your .env file.)*\n\n"
                )
                self.conversation_history.append({"role": "assistant", "content": notice + reply})
                return notice + reply, recs, f"Offline Engine ➜ {thought}"

            try:
                gemini_model = model if "gemini" in model.lower() else "gemini-1.5-flash"
                reply, recs, thought = self._call_gemini_api(user_message, gemini_key, model=gemini_model)
                self.conversation_history.append({"role": "assistant", "content": reply})
                return reply, recs, f"✨ {thought}"
            except Exception as e:
                reply, recs, thought = self.chat_offline(user_message)
                reply = f"*(⚠️ Gemini API notice: {str(e)[:90]}... Switched to Offline Engine)*\n\n" + reply
                self.conversation_history.append({"role": "assistant", "content": reply})
                return reply, recs, f"Offline Fallback ➜ {thought}"

        else:
            reply, recs, thought = self.chat_offline(user_message)
            self.conversation_history.append({"role": "assistant", "content": reply})
            return reply, recs, f"Offline Engine ➜ {thought}"

if __name__ == "__main__":
    rec = MovieRecommender()
    agent = MovieAgent(rec)
    print("Testing Tool Calling with Real-Time Data...")
    reply, recs, thought = agent.chat("Where can I stream Inception and what are its details?", api_provider="Groq")
    print("Thought:", thought)
    print("Reply:", reply)
    print(f"Cards count: {len(recs or [])}")
