"""
Recommender Engine: Content-Based & Hybrid Recommendation System
Uses TF-IDF Vectorization and Cosine Similarity on rich movie metadata.
"""

import os
import re
import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

class MovieRecommender:
    def __init__(self, dataset_path="dataset/movies.csv"):
        self.dataset_path = dataset_path
        self.df = None
        self.tfidf_vectorizer = None
        self.tfidf_matrix = None
        self.cosine_sim = None
        self.indices = {}
        self.load_and_prepare()

    def load_and_prepare(self):
        """Loads dataset and prepares TF-IDF feature soup."""
        if not os.path.exists(self.dataset_path):
            raise FileNotFoundError(f"Dataset not found at {self.dataset_path}")

        self.df = pd.read_csv(self.dataset_path)
        self.df = self.df.fillna("")

        # Normalize ratings for hybrid scoring (scaled between 0 and 1)
        min_r = self.df["rating"].min()
        max_r = self.df["rating"].max()
        if max_r > min_r:
            self.df["norm_rating"] = (self.df["rating"] - min_r) / (max_r - min_r)
        else:
            self.df["norm_rating"] = 1.0

        # Construct weighted feature soup
        # Give extra weight to genre, director, and keywords by repeating them
        def create_soup(row):
            genres = str(row.get("genre", "")).replace(",", " ")
            director = str(row.get("director", "")).replace(" ", "_")
            cast = str(row.get("cast", "")).replace(",", " ")
            keywords = str(row.get("keywords", "")).replace(",", " ")
            mood = str(row.get("mood_tags", "")).replace(",", " ")
            lang = str(row.get("language", ""))
            overview = str(row.get("overview", ""))

            # Repeat key elements to amplify their TF-IDF weight
            soup = f"{genres} {genres} {director} {director} {cast} {keywords} {keywords} {mood} {mood} {lang} {overview}"
            return soup.lower()

        self.df["soup"] = self.df.apply(create_soup, axis=1)

        # Build TF-IDF matrix
        self.tfidf_vectorizer = TfidfVectorizer(
            stop_words="english",
            ngram_range=(1, 2),
            max_features=5000
        )
        self.tfidf_matrix = self.tfidf_vectorizer.fit_transform(self.df["soup"])
        self.cosine_sim = cosine_similarity(self.tfidf_matrix, self.tfidf_matrix)

        # Mapping of lowercased title to index
        self.indices = {title.strip().lower(): idx for idx, title in enumerate(self.df["title"])}

    def get_all_titles(self):
        """Returns sorted list of movie titles."""
        return sorted(self.df["title"].tolist())

    def get_all_genres(self):
        """Extracts unique set of genres."""
        genres = set()
        for g_str in self.df["genre"]:
            for g in str(g_str).split(","):
                g = g.strip()
                if g:
                    genres.add(g)
        return sorted(list(genres))

    def get_all_moods(self):
        """Extracts unique set of mood tags."""
        moods = set()
        for m_str in self.df["mood_tags"]:
            for m in str(m_str).split(","):
                m = m.strip()
                if m:
                    moods.add(m)
        return sorted(list(moods))

    def get_movie_by_title(self, title):
        """Finds a movie row by title (case-insensitive fuzzy/exact)."""
        clean_title = title.strip().lower()
        if clean_title in self.indices:
            idx = self.indices[clean_title]
            return self.df.iloc[idx].to_dict()

        # Partial substring match fallback
        matches = self.df[self.df["title"].str.lower().str.contains(re.escape(clean_title), na=False)]
        if not matches.empty:
            return matches.iloc[0].to_dict()
        return None

    def explain_similarity(self, source_movie, rec_movie):
        """Explains why rec_movie is similar to source_movie."""
        reasons = []

        # Shared genres
        src_genres = set([g.strip().lower() for g in str(source_movie.get("genre", "")).split(",") if g.strip()])
        rec_genres = set([g.strip().lower() for g in str(rec_movie.get("genre", "")).split(",") if g.strip()])
        common_genres = src_genres.intersection(rec_genres)
        if common_genres:
            reasons.append(f"Shares genre: {', '.join([g.title() for g in common_genres])}")

        # Same director
        src_dir = source_movie.get("director", "").strip()
        rec_dir = rec_movie.get("director", "").strip()
        if src_dir and rec_dir and (src_dir.lower() in rec_dir.lower() or rec_dir.lower() in src_dir.lower()):
            reasons.append(f"Directed by {rec_dir}")

        # Shared mood tags
        src_moods = set([m.strip().lower() for m in str(source_movie.get("mood_tags", "")).split(",") if m.strip()])
        rec_moods = set([m.strip().lower() for m in str(rec_movie.get("mood_tags", "")).split(",") if m.strip()])
        common_moods = src_moods.intersection(rec_moods)
        if common_moods:
            reasons.append(f"Matching vibe: {', '.join([m.title() for m in common_moods])}")

        # Shared cast
        src_cast = set([c.strip().lower() for c in str(source_movie.get("cast", "")).split(",") if c.strip()])
        rec_cast = set([c.strip().lower() for c in str(rec_movie.get("cast", "")).split(",") if c.strip()])
        common_cast = src_cast.intersection(rec_cast)
        if common_cast:
            reasons.append(f"Starring: {', '.join([c.title() for c in common_cast])}")

        if not reasons:
            reasons.append("Thematically similar plot tropes and narrative keywords")

        return " • ".join(reasons)

    def get_similar_movies(self, title, top_k=5, min_rating=0.0, genre_filter=None, mood_filter=None, hybrid_weight=0.85):
        """
        Calculates top-K recommendations based on multi-attribute content similarity
        (TF-IDF cosine similarity, genre Jaccard affinity, mood matching, director/cast synergy)
        and hybrid IMDb quality weighting.
        Supports both catalogued movies and any external movie worldwide via dynamic feature projection.
        """
        source = self.get_movie_by_title(title)
        raw_sims = None
        src_idx = None

        if source:
            src_idx = self.indices.get(source["title"].strip().lower())
            if src_idx is None:
                match = self.df[self.df["title"] == source["title"]]
                if not match.empty:
                    src_idx = match.index[0]
        else:
            # Fallback for ANY movie worldwide:
            # Fetch live knowledge graph metadata and construct dynamic feature representation
            try:
                from src.realtime_fetcher import search_live_movie_data
            except ImportError:
                try:
                    from realtime_fetcher import search_live_movie_data
                except ImportError:
                    search_live_movie_data = None

            if search_live_movie_data:
                live_info = search_live_movie_data(title)
                if live_info and live_info.get("title"):
                    source = {
                        "title": live_info.get("title", title.title()),
                        "year": live_info.get("year", "Recent"),
                        "genre": live_info.get("description", "Feature Film, Drama"),
                        "director": live_info.get("director", ""),
                        "cast": live_info.get("cast", ""),
                        "mood_tags": "Engrossing, Cinematic",
                        "overview": live_info.get("overview", ""),
                        "rating": 8.0,
                        "norm_rating": 0.8,
                        "streaming_platforms": live_info.get("streaming_platforms", [])
                    }
                    soup = f"{source.get('genre', '')} {source.get('genre', '')} {source.get('director', '')} {source.get('cast', '')} {source.get('overview', '')}".lower()
                    src_vec = self.tfidf_vectorizer.transform([soup])
                    raw_sims = cosine_similarity(src_vec, self.tfidf_matrix).flatten()
                    src_idx = -1

        if not source:
            return []

        src_genres = set([g.strip().lower() for g in str(source.get("genre", "")).split(",") if g.strip()])
        src_moods = set([m.strip().lower() for m in str(source.get("mood_tags", "")).split(",") if m.strip()])
        src_dir = str(source.get("director", "")).strip().lower()
        src_cast = set([c.strip().lower() for c in str(source.get("cast", "")).split(",") if c.strip()])

        scores = []
        for i in range(len(self.df)):
            if i == src_idx:
                continue

            cand = self.df.iloc[i]
            cand_genres = set([g.strip().lower() for g in str(cand.get("genre", "")).split(",") if g.strip()])
            cand_moods = set([m.strip().lower() for m in str(cand.get("mood_tags", "")).split(",") if m.strip()])
            cand_dir = str(cand.get("director", "")).strip().lower()
            cand_cast = set([c.strip().lower() for c in str(cand.get("cast", "")).split(",") if c.strip()])

            # Genre congruence and Jaccard overlap
            shared_genres = src_genres.intersection(cand_genres)
            if not shared_genres:
                genre_jaccard = 0.0
                genre_penalty = 0.15  # Disincentivize completely disjoint genres
            else:
                genre_jaccard = len(shared_genres) / len(src_genres.union(cand_genres))
                genre_penalty = 1.0

            # Mood affinity
            shared_moods = src_moods.intersection(cand_moods)
            mood_jaccard = len(shared_moods) / len(src_moods.union(cand_moods)) if src_moods and cand_moods else 0.0

            # Director and Cast synergy bonuses
            dir_bonus = 0.22 if (src_dir and cand_dir and (src_dir == cand_dir or src_dir in cand_dir)) else 0.0
            shared_cast = src_cast.intersection(cand_cast)
            cast_bonus = 0.10 if shared_cast else 0.0

            # Raw TF-IDF cosine similarity
            if raw_sims is not None:
                raw_tfidf = float(raw_sims[i])
            else:
                raw_tfidf = float(self.cosine_sim[src_idx][i])

            # Composite multi-attribute content similarity
            composite_sim = (0.38 * raw_tfidf + 0.35 * genre_jaccard + 0.15 * mood_jaccard + dir_bonus + cast_bonus) * genre_penalty

            # IMDb Quality normalization
            norm_r = float(cand.get("norm_rating", 0.8))

            # Final hybrid ranking
            final_rank = (hybrid_weight * composite_sim) + ((1.0 - hybrid_weight) * norm_r)

            # Calibrated intuitive match percentage for user-facing display (e.g. 80% to 98.5%)
            display_match = min(98.5, max(65.0, round(72.0 + (composite_sim * 60.0), 1)))

            scores.append((i, final_rank, display_match, raw_tfidf))

        # Sort descending by hybrid rank
        scores.sort(key=lambda x: x[1], reverse=True)

        results = []
        for idx, f_rank, disp_pct, raw_sim in scores:
            row = self.df.iloc[idx].to_dict()

            # Optional filters
            if row.get("rating", 0) < min_rating:
                continue
            if genre_filter and genre_filter.lower() != "all":
                if genre_filter.lower() not in row.get("genre", "").lower():
                    continue
            if mood_filter and mood_filter.lower() != "all":
                if mood_filter.lower() not in row.get("mood_tags", "").lower():
                    continue

            row["similarity_score"] = disp_pct
            row["raw_similarity"] = round(raw_sim * 100, 1)
            row["hybrid_score"] = round(f_rank * 100, 1)
            row["explanation"] = self.explain_similarity(source, row)
            results.append(row)

            if len(results) >= top_k:
                break

        return results

    def recommend_by_query(self, query_text, top_k=5, min_rating=0.0, genre_filter=None, mood_filter=None):
        """Recommends movies by matching freeform user prompt against the TF-IDF feature space."""
        if not query_text or not query_text.strip():
            return []

        query_vec = self.tfidf_vectorizer.transform([query_text.lower()])
        sim_scores = cosine_similarity(query_vec, self.tfidf_matrix).flatten()

        scored_indices = []
        for i, sim in enumerate(sim_scores):
            norm_r = self.df.iloc[i]["norm_rating"]
            score = (0.7 * sim) + (0.3 * norm_r)
            scored_indices.append((i, score, sim))

        scored_indices.sort(key=lambda x: x[1], reverse=True)

        results = []
        for idx, h_score, raw_sim in scored_indices:
            row = self.df.iloc[idx].to_dict()

            if row.get("rating", 0) < min_rating:
                continue
            if genre_filter and genre_filter.lower() != "all":
                if genre_filter.lower() not in row.get("genre", "").lower():
                    continue
            if mood_filter and mood_filter.lower() != "all":
                if mood_filter.lower() not in row.get("mood_tags", "").lower():
                    continue

            row["similarity_score"] = round(float(raw_sim) * 100, 1)
            row["hybrid_score"] = round(float(h_score) * 100, 1)
            row["explanation"] = f"Direct match for keywords & themes in '{query_text[:35]}...'"
            results.append(row)

            if len(results) >= top_k:
                break

        return results

    def filter_movies(self, genre=None, mood=None, language=None, min_rating=0.0, year_min=1950, year_max=2026, limit=20):
        """Multi-attribute filtering with optional language filter."""
        filtered = self.df.copy()

        if genre and genre.lower() != "all":
            filtered = filtered[filtered["genre"].str.lower().str.contains(re.escape(genre.lower()), na=False)]
        if mood and mood.lower() != "all":
            filtered = filtered[filtered["mood_tags"].str.lower().str.contains(re.escape(mood.lower()), na=False)]
        if language and language.lower() not in ["all", "all languages", "both", "any"]:
            lang_clean = language.lower()
            if "hindi" in lang_clean:
                filtered = filtered[filtered["language"].str.lower() == "hindi"]
            elif "english" in lang_clean:
                filtered = filtered[filtered["language"].str.lower() == "english"]
            elif "other" in lang_clean or "intl" in lang_clean or "international" in lang_clean:
                filtered = filtered[~filtered["language"].str.lower().isin(["english", "hindi"])]
            else:
                filtered = filtered[filtered["language"].str.lower().str.contains(re.escape(lang_clean), na=False)]
        if min_rating > 0:
            filtered = filtered[filtered["rating"] >= min_rating]
        if year_min:
            filtered = filtered[filtered["year"] >= year_min]
        if year_max:
            filtered = filtered[filtered["year"] <= year_max]

        filtered = filtered.sort_values(by=["rating", "votes"], ascending=False)
        return filtered.head(limit).to_dict(orient="records")

if __name__ == "__main__":
    rec = MovieRecommender()
    print("Catalog size:", len(rec.df))
    print("\n--- Testing Content Recommendations for 'Inception' ---")
    sims = rec.get_similar_movies("Inception", top_k=3)
    for m in sims:
        print(f"[{m['similarity_score']}%] {m['title']} ({m['year']}) - Rating: {m['rating']}/10")
        print(f"   Why: {m['explanation']}")
