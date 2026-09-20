# 🎬 CineAgent: AI Agent for Movie Recommendation (GUI-Based)

> **Symbiosis International University — Semester 5 Flexi Credit (CA3 Mini Project)**  
> **Topic:** AI Agent for Movie Recommendation with a Graphical User Interface (Gradio)  
> **Author:** Student Submission  

---

## 🌟 Executive Summary
**CineAgent** is an intelligent, full-featured Movie Recommendation System powered by an **Autonomous ReAct Tool-Calling AI Agent**, **Real-Time Streaming & Movie Radar**, **Multi-Model LLM Inference (Groq LPUs & Google Gemini)**, and **Content-Based TF-IDF Cosine Similarity**.

The system can **fetch real-time data** (official streaming availability, live box office figures, real-time synopses) and intelligently select across multiple state-of-the-art LLMs (`openai/gpt-oss-120b`, `qwen/qwen3.8-27b`, `gemini-1.5-flash`, and offline fallback).

---

## 🚀 Key Features

### 1. 🔴 Real-Time Cinema Radar & Live Search
- **Live OTT Streaming Availability**: Instant "Where to Watch" lookup (Netflix, Prime Video, Disney+, Apple TV+, Max).
- **Live Ground-Truth Facts**: Real-time Wikipedia Knowledge Graph data (synopses, release dates, box office milestones, official posters).
- **Global Trending Grid**: Live tracking of current box office champions and critically acclaimed releases.

### 2. ⚡ ReAct Tool-Calling Multi-Model AI Agent
- **Autonomous Tool Invocation**: Detects when queries require live factual grounding (*"Where can I stream Inception?"*, *"What movies are trending right now?"*) and calls `realtime_fetcher` dynamically.
- **Multi-Model Engine**: Seamlessly switch between **Groq Cloud LPU** (`openai/gpt-oss-120b`, `qwen/qwen3.8-27b`), **Google Gemini**, and the **Local Offline Engine**.
- **Explainable AI (XAI)**: Explicitly explains **why** a title was chosen and shows tool execution traces.

### 3. 🎯 Content-Based Movie Matcher
- Choose any reference film from the curated catalog.
- Computes cosine similarity across a rich **Feature Soup** (*Genres + Director + Lead Cast + Synopsis Keywords + Mood Tags*).
- **Hybrid Score Slider**: Blends topical content similarity with normalized IMDb ratings to guarantee high-quality suggestions.

### 4. 🎭 Mood & Atmosphere Explorer
- Direct filtering by emotional tone (*Feel-Good, Mind-Bending, Adrenaline Rush, Dark & Gritty, Romantic/Cozy, Spooky & Chilling, Epic & Grand, Thought-Provoking*).
- Era constraints (e.g., 1980s classics to 2024 releases) and IMDb minimum rating thresholds.

### 5. 📊 Dataset & Visual Analytics
- Real-time cinema-styled visual plots powered by Matplotlib:
  - Top 10 Genres in catalog.
  - IMDb Rating distributions across release eras.
  - Distribution of emotional mood tags.
  - Most featured visionary directors.

### 6. 📘 In-App Academic Report & Viva Guide
- Interactive documentation covering ReAct agent workflows, mathematical proofs, and 10 common viva questions for examination.

---

## 📁 Repository Structure

```
CA3/
├── app.py                     # Main Gradio application with Real-Time Radar & 6 feature tabs
├── .env                       # Environment configuration with your GROQ_API_KEY
├── requirements.txt           # Python dependencies (gradio, groq, pandas, scikit-learn, etc.)
├── README.md                  # Comprehensive project report and execution instructions
├── dataset/
│   └── movies.csv             # Curated dataset with genres, directors, cast, ratings, plot & poster URLs
├── scripts/
│   └── build_dataset.py       # Automated catalog generator and updater
└── src/
    ├── realtime_fetcher.py    # Real-time streaming detector, live search & trending radar
    ├── recommender.py         # TF-IDF vectorizer, cosine similarity & hybrid ranking engine
    ├── agent.py               # ReAct Tool-Calling Agent with multi-model LLM execution
    └── visualizer.py          # Cinema-styled visual analytics graphs
```
```

---

## 🧮 Mathematical Formulations

### 1. TF-IDF (Term Frequency-Inverse Document Frequency)
Each movie document $d$ is represented by a weighted feature soup:
$$\text{Soup}(d) = \text{Genre} \oplus \text{Director} \oplus \text{Cast} \oplus \text{Keywords} \oplus \text{Mood} \oplus \text{Overview}$$

The TF-IDF weight for term $t$ in movie $d$ over corpus $D$:
$$\text{TF-IDF}(t, d, D) = \text{TF}(t, d) \times \log\left(\frac{1 + |D|}{1 + |\{d' \in D : t \in d'\}|}\right) + 1$$

### 2. Cosine Similarity
Calculates the angular proximity between the query/seed movie vector $\mathbf{u}$ and candidate vector $\mathbf{v}$:
$$\text{CosineSim}(\mathbf{u}, \mathbf{v}) = \frac{\mathbf{u} \cdot \mathbf{v}}{\|\mathbf{u}\|_2 \|\mathbf{v}\|_2} = \frac{\sum_{i=1}^n u_i v_i}{\sqrt{\sum_{i=1}^n u_i^2} \sqrt{\sum_{i=1}^n v_i^2}}$$

### 3. Hybrid Quality Scoring
Prevents low-rated or obscure movies from dominating purely on keyword overlap:
$$\text{Score}_{\text{hybrid}} = \alpha \cdot \text{CosineSim}(\mathbf{u}, \mathbf{v}) + (1 - \alpha) \cdot \text{NormalizedRating}(v)$$
*(where $\alpha \in [0, 1]$ represents the similarity weight set by the user).*

---

## 🛠️ Installation & How to Run

### Step 1: Open Terminal in Project Directory
Ensure you are in the project folder:
```bash
cd "d:/Symbiosis/SEM 5/Flexi credit/CA3"
```

### Step 2: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 3: Configure Environment Variables (Optional for Cloud Models)
Copy `.example.env` to `.env`:
```bash
cp .example.env .env
```
Open `.env` and paste your free Groq API key (`https://console.groq.com/keys`) or Google Gemini API key.  
*(Note: `.env` is ignored by git to protect your secret keys. CineAgent also works completely offline with no keys).*

### Step 4: Run the Application
```bash
python app.py
```

### Step 4: Open in Web Browser
The app will automatically open in your default browser at:
```
http://127.0.0.1:7860
```

*(Tip: To create a shareable public link for instructors to test from their own devices, modify the last line in `app.py` to `demo.launch(share=True)`).*

---

## 🎓 Academic Viva Questions & Answers

| # | Viva Question | Recommended Examiner Response |
|---|---|---|
| **1** | **What problem does this project solve?** | It solves the Cold-Start problem and user choice paralysis in movie streaming by combining autonomous conversational intent extraction with content-based semantic matching. |
| **2** | **Why Content-Based Filtering instead of Collaborative Filtering?** | Collaborative filtering requires massive user-item rating matrices and fails for new users with no history. Content-based filtering leverages item features and current intent immediately. |
| **3** | **Why do we use TF-IDF rather than simple word counts?** | Simple counts over-represent frequent stop words. TF-IDF down-weights universally common words and amplifies distinct keywords (e.g. *multiverse*, *time inversion*, *noir*). |
| **4** | **Why is Cosine Similarity preferred over Euclidean Distance?** | Euclidean distance is heavily distorted by document length (word count variations). Cosine similarity measures vector angles, making it length-invariant and ideal for variable synopsis lengths. |
| **5** | **How does the AI Agent extract user intent?** | The agent parses the user's natural language input against mapped dictionaries for mood vibes, genres, mentioned titles, and minimum rating constraints, maintaining state across turns. |
| **6** | **What is the purpose of the Hybrid Scoring mechanism?** | It combines semantic similarity with normalized IMDb ratings ($\alpha \cdot Sim + (1-\alpha) \cdot Rating$) to ensure suggestions are both relevant and of proven cinematic quality. |
| **7** | **Can this system operate completely offline?** | Yes, it contains a built-in semantic heuristic reasoning agent that functions 100% offline without any API keys or network dependencies. |
| **8** | **How are N-grams utilized?** | Bi-grams $(1, 2)$ capture two-word phrases like *'science fiction'*, *'serial killer'*, and *'time travel'* as single concepts rather than disconnected words. |
| **9** | **What is the time complexity of the recommendation search?** | Querying cosine similarity against a precomputed TF-IDF matrix takes $\mathcal{O}(N)$, providing near-instant responses (<20ms). |
| **10** | **Why Gradio over standard desktop GUI libraries like Tkinter?** | Gradio provides web-native responsive layouts, rich chatbot interfaces, async streaming capabilities, and one-click public URL generation for academic assessment. |
