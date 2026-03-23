"""
╔══════════════════════════════════════════════════════════════════╗
║         🐍 PYTHONIUM — Plateforme Interactive d'Algorithmique    ║
║         Version 2.0 | Architecture Modulaire | EdTech Pro        ║
╚══════════════════════════════════════════════════════════════════╝

Auteur     : Plateforme Pédagogique Pythonium
Description: Mini "Duolingo de Python" — cours interactif, gamifié,
             avec éditeur de code intégré, quiz avancé et système
             de progression basé sur session_state.

Dépendances:
    pip install streamlit streamlit-ace

Lancement:
    streamlit run python_cours_interactif.py
"""

# ─────────────────────────────────────────────────────────────────
# IMPORTS
# ─────────────────────────────────────────────────────────────────
import streamlit as st
from streamlit_ace import st_ace
import json
import traceback
from datetime import datetime
from io import StringIO
import sys

# ─────────────────────────────────────────────────────────────────
# CONFIGURATION GLOBALE DE LA PAGE
# ─────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Pythonium — Apprends Python",
    page_icon="🐍",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─────────────────────────────────────────────────────────────────
# CSS PERSONNALISÉ — UX MODERNE & ENGAGEANT
# ─────────────────────────────────────────────────────────────────
CUSTOM_CSS = """
<style>
/* Import Google Fonts */
@import url('https://fonts.googleapis.com/css2?family=Space+Mono:wght@400;700&family=Nunito:wght@400;600;700;800;900&display=swap');

/* ── Variables de thème ── */
:root {
    --primary:    #6C63FF;
    --secondary:  #FF6584;
    --success:    #43D9AD;
    --warning:    #FFB347;
    --danger:     #FF6B6B;
    --dark:       #0D1117;
    --card-bg:    #161B22;
    --border:     #30363D;
    --text:       #E6EDF3;
    --text-muted: #8B949E;
    --gold:       #FFD700;
    --silver:     #C0C0C0;
    --bronze:     #CD7F32;
}

/* ── Base ── */
html, body, [class*="css"] {
    font-family: 'Nunito', sans-serif;
    background-color: var(--dark);
    color: var(--text);
}

/* ── Header principal ── */
.main-header {
    background: linear-gradient(135deg, #1a1f2e 0%, #0d1117 50%, #1a1a2e 100%);
    border: 1px solid var(--border);
    border-radius: 16px;
    padding: 2rem 2.5rem;
    margin-bottom: 1.5rem;
    position: relative;
    overflow: hidden;
}
.main-header::before {
    content: '';
    position: absolute;
    top: -50%;
    left: -50%;
    width: 200%;
    height: 200%;
    background: radial-gradient(ellipse at center, rgba(108,99,255,0.1) 0%, transparent 60%);
    pointer-events: none;
}
.main-header h1 {
    font-size: 2.4rem;
    font-weight: 900;
    background: linear-gradient(90deg, #6C63FF, #FF6584, #43D9AD);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin: 0;
}
.main-header p {
    color: var(--text-muted);
    font-size: 1rem;
    margin-top: 0.5rem;
}

/* ── Cartes de module ── */
.module-card {
    background: var(--card-bg);
    border: 1px solid var(--border);
    border-radius: 12px;
    padding: 1.5rem;
    margin-bottom: 1.2rem;
    transition: border-color 0.2s, transform 0.2s;
}
.module-card:hover {
    border-color: var(--primary);
    transform: translateY(-2px);
}
.module-card.completed {
    border-color: var(--success);
    background: linear-gradient(135deg, rgba(67,217,173,0.05), var(--card-bg));
}
.module-card.locked {
    opacity: 0.5;
}

/* ── Badge XP ── */
.xp-badge {
    display: inline-flex;
    align-items: center;
    gap: 0.3rem;
    background: linear-gradient(135deg, #FFD700, #FF8C00);
    color: #000;
    font-weight: 800;
    font-size: 0.85rem;
    padding: 0.25rem 0.75rem;
    border-radius: 20px;
}

/* ── Barre de progression ── */
.progress-container {
    background: var(--card-bg);
    border: 1px solid var(--border);
    border-radius: 12px;
    padding: 1.2rem;
    margin-bottom: 1rem;
}
.progress-label {
    display: flex;
    justify-content: space-between;
    font-size: 0.85rem;
    color: var(--text-muted);
    margin-bottom: 0.5rem;
}
.progress-bar-outer {
    background: #21262D;
    border-radius: 8px;
    height: 12px;
    overflow: hidden;
}
.progress-bar-inner {
    height: 100%;
    border-radius: 8px;
    background: linear-gradient(90deg, var(--primary), var(--secondary));
    transition: width 0.6s ease;
}

/* ── Stat cards ── */
.stat-grid {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 0.8rem;
    margin-bottom: 1rem;
}
.stat-card {
    background: var(--card-bg);
    border: 1px solid var(--border);
    border-radius: 10px;
    padding: 1rem;
    text-align: center;
}
.stat-card .value {
    font-size: 1.6rem;
    font-weight: 900;
    color: var(--primary);
}
.stat-card .label {
    font-size: 0.75rem;
    color: var(--text-muted);
    text-transform: uppercase;
    letter-spacing: 0.05em;
}

/* ── Badge de niveau ── */
.level-badge {
    display: inline-block;
    background: linear-gradient(135deg, var(--primary), #9B59B6);
    border-radius: 50%;
    width: 48px;
    height: 48px;
    line-height: 48px;
    text-align: center;
    font-weight: 900;
    font-size: 1.2rem;
    color: white;
    margin-right: 0.5rem;
}

/* ── Boîte de théorie ── */
.theory-box {
    background: linear-gradient(135deg, rgba(108,99,255,0.08), rgba(108,99,255,0.03));
    border-left: 4px solid var(--primary);
    border-radius: 0 10px 10px 0;
    padding: 1.2rem 1.5rem;
    margin: 1rem 0;
}
.theory-box h4 {
    color: var(--primary);
    margin-top: 0;
    font-size: 1rem;
    text-transform: uppercase;
    letter-spacing: 0.05em;
}

/* ── Boîte d'exemple ── */
.example-box {
    background: linear-gradient(135deg, rgba(67,217,173,0.06), rgba(67,217,173,0.02));
    border-left: 4px solid var(--success);
    border-radius: 0 10px 10px 0;
    padding: 1.2rem 1.5rem;
    margin: 1rem 0;
}
.example-box h4 {
    color: var(--success);
    margin-top: 0;
    font-size: 1rem;
    text-transform: uppercase;
    letter-spacing: 0.05em;
}

/* ── Boîte d'exercice ── */
.exercise-box {
    background: linear-gradient(135deg, rgba(255,101,132,0.08), rgba(255,101,132,0.02));
    border: 1px solid rgba(255,101,132,0.3);
    border-radius: 10px;
    padding: 1.5rem;
    margin: 1rem 0;
}
.exercise-box h4 {
    color: var(--secondary);
    margin-top: 0;
}

/* ── Hint box ── */
.hint-box {
    background: rgba(255,179,71,0.08);
    border: 1px solid rgba(255,179,71,0.3);
    border-radius: 8px;
    padding: 1rem;
    font-size: 0.9rem;
}
.hint-box::before {
    content: '💡 ';
    font-weight: bold;
}

/* ── Badges de récompense ── */
.badge-container {
    display: flex;
    flex-wrap: wrap;
    gap: 0.5rem;
    margin: 1rem 0;
}
.badge {
    display: inline-flex;
    align-items: center;
    gap: 0.4rem;
    padding: 0.4rem 0.9rem;
    border-radius: 20px;
    font-size: 0.82rem;
    font-weight: 700;
    border: 1px solid;
}
.badge-gold   { background: rgba(255,215,0,0.1);   border-color: gold;   color: gold; }
.badge-silver { background: rgba(192,192,192,0.1); border-color: silver; color: silver; }
.badge-bronze { background: rgba(205,127,50,0.1);  border-color: #CD7F32; color: #CD7F32; }
.badge-purple { background: rgba(108,99,255,0.1);  border-color: var(--primary); color: var(--primary); }
.badge-green  { background: rgba(67,217,173,0.1);  border-color: var(--success); color: var(--success); }

/* ── Quiz ── */
.quiz-question {
    background: var(--card-bg);
    border: 1px solid var(--border);
    border-radius: 12px;
    padding: 1.5rem;
    margin: 1rem 0;
}
.quiz-question.correct { border-color: var(--success); }
.quiz-question.wrong   { border-color: var(--danger); }

/* ── Score final ── */
.score-display {
    text-align: center;
    padding: 2rem;
    background: var(--card-bg);
    border-radius: 16px;
    border: 1px solid var(--border);
}
.score-display .big-score {
    font-size: 4rem;
    font-weight: 900;
    background: linear-gradient(90deg, var(--primary), var(--secondary));
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

/* ── Sidebar ── */
section[data-testid="stSidebar"] {
    background-color: #0D1117 !important;
    border-right: 1px solid var(--border);
}

/* ── Boutons Streamlit ── */
div.stButton > button {
    background: linear-gradient(135deg, var(--primary), #9B59B6) !important;
    color: white !important;
    border: none !important;
    border-radius: 8px !important;
    font-weight: 700 !important;
    padding: 0.5rem 1.5rem !important;
    transition: all 0.2s !important;
}
div.stButton > button:hover {
    opacity: 0.9 !important;
    transform: translateY(-1px) !important;
}

/* ── Code blocks ── */
pre, code {
    font-family: 'Space Mono', monospace !important;
}

/* ── Divider ── */
hr {
    border-color: var(--border) !important;
    margin: 1.5rem 0 !important;
}

/* ── Masquer le menu par défaut ── */
#MainMenu, footer, header { visibility: hidden; }

/* ── Streamer de succès ── */
div[data-testid="stSuccess"] {
    background: rgba(67,217,173,0.1) !important;
    border: 1px solid var(--success) !important;
    border-radius: 10px !important;
}
div[data-testid="stError"] {
    background: rgba(255,107,107,0.1) !important;
    border: 1px solid var(--danger) !important;
    border-radius: 10px !important;
}
div[data-testid="stWarning"] {
    background: rgba(255,179,71,0.1) !important;
    border: 1px solid var(--warning) !important;
    border-radius: 10px !important;
}
div[data-testid="stInfo"] {
    background: rgba(108,99,255,0.1) !important;
    border: 1px solid var(--primary) !important;
    border-radius: 10px !important;
}
</style>
"""

# ─────────────────────────────────────────────────────────────────
# CONSTANTES & DONNÉES DU COURS
# ─────────────────────────────────────────────────────────────────

# Noms des modules et leur XP de récompense
MODULES = [
    {"id": "variables",   "icon": "📦", "title": "Variables & Types",    "xp": 100},
    {"id": "conditions",  "icon": "🔀", "title": "Conditions (if/else)", "xp": 150},
    {"id": "boucles",     "icon": "🔁", "title": "Boucles (for/while)",  "xp": 150},
    {"id": "fonctions",   "icon": "⚙️", "title": "Fonctions",            "xp": 200},
    {"id": "listes",      "icon": "📋", "title": "Listes & Tableaux",    "xp": 200},
    {"id": "dicts",       "icon": "🗂️", "title": "Dictionnaires",        "xp": 200},
    {"id": "quiz",        "icon": "🏆", "title": "Quiz Final",           "xp": 300},
]

TOTAL_XP = sum(m["xp"] for m in MODULES)

# Seuils de niveau
LEVELS = [
    (0,    "🥚 Œuf"),
    (100,  "🐣 Poussin"),
    (300,  "🐥 Apprenti"),
    (600,  "🐍 Pythoniste"),
    (1000, "🦅 Expert"),
    (1500, "🧙 Maître"),
]

# ─────────────────────────────────────────────────────────────────
# INITIALISATION DU SESSION STATE
# ─────────────────────────────────────────────────────────────────
def init_session():
    """Initialise les variables de session au premier lancement."""
    defaults = {
        "username":          "",
        "xp":                0,
        "completed_modules": [],   # liste des IDs de modules terminés
        "badges":            [],   # liste de tuples (emoji, label, classe CSS)
        "exercise_results":  {},   # {module_id: {exercice_n: bool}}
        "quiz_score":        None,
        "quiz_answers":      {},
        "attempts":          {},   # {module_id_ex_n: int}
        "started_at":        str(datetime.now().strftime("%d/%m/%Y %H:%M")),
        "last_page":         "🏠 Accueil",
    }
    for key, val in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = val

init_session()

# ─────────────────────────────────────────────────────────────────
# UTILITAIRES
# ─────────────────────────────────────────────────────────────────

def get_level(xp: int) -> str:
    """Retourne le titre de niveau correspondant à un score XP."""
    level = LEVELS[0][1]
    for threshold, title in LEVELS:
        if xp >= threshold:
            level = title
    return level

def get_level_number(xp: int) -> int:
    """Retourne le numéro de niveau (1-based)."""
    for i, (threshold, _) in enumerate(LEVELS):
        if xp < threshold:
            return max(1, i)
    return len(LEVELS)

def award_xp(amount: int, source: str = ""):
    """Ajoute des XP et affiche une notification."""
    st.session_state.xp += amount
    st.toast(f"✨ +{amount} XP gagnés ! {source}", icon="🎉")

def award_badge(emoji: str, label: str, css_class: str, key: str):
    """Attribue un badge unique (vérifie les doublons par clé)."""
    existing_keys = [b[3] for b in st.session_state.badges]
    if key not in existing_keys:
        st.session_state.badges.append((emoji, label, css_class, key))
        st.toast(f"🏅 Badge débloqué : {emoji} {label}", icon="🏅")

def mark_module_complete(module_id: str, xp: int):
    """Marque un module comme terminé et accorde les XP."""
    if module_id not in st.session_state.completed_modules:
        st.session_state.completed_modules.append(module_id)
        award_xp(xp, f"Module terminé !")
        # Badges spéciaux
        n = len(st.session_state.completed_modules)
        if n == 1:
            award_badge("🌱", "Premier Pas", "badge-green", "first_module")
        elif n == 3:
            award_badge("🔥", "En Feu !", "badge-gold", "three_modules")
        elif n == len(MODULES) - 1:
            award_badge("💎", "Presque Là", "badge-purple", "almost_done")

def safe_exec(code: str) -> tuple[dict, str | None]:
    """
    Exécute du code Python de manière sécurisée dans un namespace isolé.
    Retourne (namespace_local, message_erreur_ou_None).
    """
    # Vérification de sécurité basique — blocage des imports dangereux
    forbidden = ["import os", "import sys", "import subprocess",
                 "import socket", "__import__", "open(", "eval(", "exec("]
    for f in forbidden:
        if f in code:
            return {}, f"⛔ Utilisation interdite de `{f}` pour des raisons de sécurité."

    local_ns = {}
    # Capturer stdout
    old_stdout = sys.stdout
    sys.stdout = captured = StringIO()
    try:
        exec(compile(code, "<student_code>", "exec"), {}, local_ns)
        output = captured.getvalue()
        local_ns["__stdout__"] = output
        return local_ns, None
    except Exception:
        err = traceback.format_exc().split("\n")[-2]
        return {}, err
    finally:
        sys.stdout = old_stdout

def render_progress_bar(label: str, value: int, total: int, color: str = "#6C63FF"):
    """Affiche une barre de progression HTML custom."""
    pct = min(100, int(value / total * 100)) if total > 0 else 0
    st.markdown(f"""
    <div class="progress-container">
        <div class="progress-label">
            <span>{label}</span>
            <span><b>{value}</b> / {total} ({pct}%)</span>
        </div>
        <div class="progress-bar-outer">
            <div class="progress-bar-inner" style="width:{pct}%; background: linear-gradient(90deg, {color}, #FF6584);"></div>
        </div>
    </div>
    """, unsafe_allow_html=True)

def render_code_example(code: str, title: str = "Exemple"):
    """Affiche un bloc de code avec un style soigné."""
    st.markdown(f"""
    <div class="example-box">
        <h4>🔍 {title}</h4>
    </div>
    """, unsafe_allow_html=True)
    st.code(code, language="python")

def render_theory(content: str, title: str = "Théorie"):
    """Affiche une boîte de théorie stylisée."""
    st.markdown(f"""
    <div class="theory-box">
        <h4>📚 {title}</h4>
        {content}
    </div>
    """, unsafe_allow_html=True)

def exercise_header(module_id: str, ex_num: int, title: str, xp: int):
    """Affiche l'en-tête d'un exercice avec indicateur de complétion."""
    key = f"{module_id}_ex{ex_num}"
    results = st.session_state.exercise_results.get(module_id, {})
    done = results.get(f"ex{ex_num}", False)
    status = "✅" if done else "⬜"
    st.markdown(f"""
    <div class="exercise-box">
        <h4>{status} Exercice {ex_num} — {title}
            <span class="xp-badge" style="float:right; margin-top:-2px;">+{xp} XP</span>
        </h4>
    </div>
    """, unsafe_allow_html=True)

def mark_exercise_done(module_id: str, ex_key: str, xp: int):
    """Marque un exercice comme réussi et accorde les XP."""
    if module_id not in st.session_state.exercise_results:
        st.session_state.exercise_results[module_id] = {}
    if not st.session_state.exercise_results[module_id].get(ex_key, False):
        st.session_state.exercise_results[module_id][ex_key] = True
        award_xp(xp, f"Exercice réussi !")

# ─────────────────────────────────────────────────────────────────
# SIDEBAR — NAVIGATION & PROFIL
# ─────────────────────────────────────────────────────────────────

def render_sidebar():
    """Affiche la barre latérale avec profil, progression et navigation."""
    with st.sidebar:
        st.markdown("## 🐍 Pythonium")
        st.markdown("---")

        # ── Profil utilisateur ──
        if not st.session_state.username:
            with st.expander("👤 Créer mon profil", expanded=True):
                name = st.text_input("Ton prénom :", placeholder="Ex: Alice")
                if st.button("Commencer l'aventure !") and name.strip():
                    st.session_state.username = name.strip()
                    st.rerun()
        else:
            lvl = get_level_number(st.session_state.xp)
            title = get_level(st.session_state.xp)
            st.markdown(f"""
            <div style="text-align:center; padding: 0.8rem; background: #161B22;
                        border-radius: 10px; border: 1px solid #30363D; margin-bottom: 1rem;">
                <div style="font-size:2rem;">{title.split()[0]}</div>
                <div style="font-weight:800; font-size:1.1rem;">{st.session_state.username}</div>
                <div style="color:#8B949E; font-size:0.8rem;">Niveau {lvl} — {title.split(' ', 1)[1] if ' ' in title else title}</div>
                <div style="margin-top:0.5rem;">
                    <span class="xp-badge">⭐ {st.session_state.xp} XP</span>
                </div>
            </div>
            """, unsafe_allow_html=True)

        # ── Progression globale ──
        done_count = len(st.session_state.completed_modules)
        total_mod  = len(MODULES) - 1  # Quiz exclu du comptage modules
        render_progress_bar(
            "Progression du cours",
            done_count, total_mod, "#6C63FF"
        )

        # ── Navigation ──
        st.markdown("### 📖 Modules")
        nav_items = ["🏠 Accueil"] + [
            f"{m['icon']} {m['title']}" for m in MODULES
        ]
        choice = st.radio("", nav_items, label_visibility="collapsed",
                          index=nav_items.index(st.session_state.last_page)
                          if st.session_state.last_page in nav_items else 0)
        st.session_state.last_page = choice

        # ── Badges ──
        if st.session_state.badges:
            st.markdown("### 🏅 Badges")
            badge_html = '<div class="badge-container">'
            for emoji, label, css_class, _ in st.session_state.badges:
                badge_html += f'<span class="badge {css_class}">{emoji} {label}</span>'
            badge_html += '</div>'
            st.markdown(badge_html, unsafe_allow_html=True)

        st.markdown("---")
        st.markdown(f"<div style='color:#8B949E; font-size:0.75rem; text-align:center;'>Démarré le {st.session_state.started_at}</div>", unsafe_allow_html=True)

        return choice

# ─────────────────────────────────────────────────────────────────
# PAGE — ACCUEIL
# ─────────────────────────────────────────────────────────────────

def page_accueil():
    """Page d'accueil avec présentation et statistiques."""
    st.markdown("""
    <div class="main-header">
        <h1>🐍 Bienvenue sur Pythonium !</h1>
        <p>Ton parcours interactif pour maîtriser l'algorithmique avec Python — étape par étape.</p>
    </div>
    """, unsafe_allow_html=True)

    # ── Stats globales ──
    done  = len(st.session_state.completed_modules)
    total = len(MODULES) - 1
    xp    = st.session_state.xp

    st.markdown(f"""
    <div class="stat-grid">
        <div class="stat-card">
            <div class="value">{done}/{total}</div>
            <div class="label">Modules terminés</div>
        </div>
        <div class="stat-card">
            <div class="value">{xp}</div>
            <div class="label">XP totaux</div>
        </div>
        <div class="stat-card">
            <div class="value">{len(st.session_state.badges)}</div>
            <div class="label">Badges</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("### 🗺️ Carte du Cours")
    cols = st.columns(2)
    for i, module in enumerate(MODULES):
        col = cols[i % 2]
        mid = module["id"]
        completed = mid in st.session_state.completed_modules
        locked     = (mid == "quiz") and (done < total)
        css = "completed" if completed else ("locked" if locked else "")
        status_icon = "✅" if completed else ("🔒" if locked else "▶️")

        with col:
            st.markdown(f"""
            <div class="module-card {css}">
                <div style="display:flex; justify-content:space-between; align-items:center;">
                    <div>
                        <span style="font-size:1.5rem;">{module['icon']}</span>
                        <strong style="margin-left:0.5rem;">{module['title']}</strong>
                    </div>
                    <div>
                        <span class="xp-badge">+{module['xp']} XP</span>
                        <span style="margin-left:0.5rem; font-size:1.2rem;">{status_icon}</span>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)

    if not st.session_state.username:
        st.info("👈 Crée ton profil dans la barre latérale pour commencer à accumuler des XP !")
    else:
        st.success(f"👋 Bon retour, **{st.session_state.username}** ! Continue ta progression.")

# ─────────────────────────────────────────────────────────────────
# MODULE 1 — VARIABLES & TYPES
# ─────────────────────────────────────────────────────────────────

def module_variables():
    """Module pédagogique sur les variables et les types de données."""
    mod_id = "variables"
    st.markdown("## 📦 Module 1 — Variables & Types de données")

    render_theory("""
    <p>Une <b>variable</b> est un espace mémoire nommé qui stocke une valeur.
    En Python, on crée une variable en lui assignant simplement une valeur avec <code>=</code>.</p>
    <p>Python est <b>dynamiquement typé</b> : le type est inféré automatiquement.</p>
    <ul>
        <li><code>int</code> — entier (ex: <code>42</code>)</li>
        <li><code>float</code> — décimal (ex: <code>3.14</code>)</li>
        <li><code>str</code> — chaîne de caractères (ex: <code>"Bonjour"</code>)</li>
        <li><code>bool</code> — booléen (<code>True</code> ou <code>False</code>)</li>
    </ul>
    """, "Les Variables en Python")

    render_code_example("""
# Déclaration de variables
nom    = "Alice"       # str
age    = 25            # int
taille = 1.65          # float
actif  = True          # bool

# Affichage
print(f"Bonjour, je suis {nom}, j'ai {age} ans.")
print(type(age))       # <class 'int'>
    """)

    st.markdown("---")

    # ── Exercice 1 ──
    exercise_header(mod_id, 1, "Déclarer et afficher une variable", 25)
    st.write("Crée une variable `score` égale à `100`, puis affichez-la avec `print()`.")
    st.markdown('<div class="hint-box">Rappel : <code>score = 100</code> puis <code>print(score)</code></div>', unsafe_allow_html=True)

    code1 = st_ace(
        placeholder="# Écris ton code ici...\n",
        language="python", theme="monokai",
        height=120, key="var_ex1",
        auto_update=True, wrap=True,
    )
    if st.button("✅ Vérifier", key="var_check1"):
        ns, err = safe_exec(code1 or "")
        if err:
            st.error(f"❌ Erreur : `{err}`")
        elif "score" not in ns:
            st.warning("⚠️ La variable `score` n'est pas définie.")
        elif ns["score"] != 100:
            st.warning(f"⚠️ `score` vaut `{ns['score']}` mais devrait valoir `100`.")
        else:
            st.success("✅ Parfait ! `score = 100` — Tu as bien créé et affiché ta variable !")
            mark_exercise_done(mod_id, "ex1", 25)
            award_badge("📦", "Premier Stockage", "badge-green", "var_ex1_done")

    st.markdown("---")

    # ── Exercice 2 ──
    exercise_header(mod_id, 2, "Manipulation de types", 30)
    st.write("Crée 3 variables : `prenom` (ton prénom), `annee` (2024), `pi_approx` (3.14). Puis affiche leur type avec `type()`.")
    st.markdown('<div class="hint-box">Utilise <code>print(type(prenom))</code> pour chaque variable.</div>', unsafe_allow_html=True)

    code2 = st_ace(
        placeholder="# Crée tes 3 variables ici...\n",
        language="python", theme="monokai",
        height=150, key="var_ex2",
        auto_update=True, wrap=True,
    )
    if st.button("✅ Vérifier", key="var_check2"):
        ns, err = safe_exec(code2 or "")
        if err:
            st.error(f"❌ Erreur : `{err}`")
        else:
            missing = [v for v in ["prenom", "annee", "pi_approx"] if v not in ns]
            if missing:
                st.warning(f"⚠️ Variables manquantes : `{', '.join(missing)}`")
            elif not isinstance(ns["prenom"], str):
                st.warning("`prenom` doit être une chaîne de caractères (str).")
            elif ns["annee"] != 2024:
                st.warning("`annee` doit valoir exactement `2024`.")
            elif abs(ns["pi_approx"] - 3.14) > 0.001:
                st.warning("`pi_approx` doit valoir `3.14`.")
            else:
                st.success("✅ Excellent ! Tes 3 variables sont bien typées !")
                mark_exercise_done(mod_id, "ex2", 30)

    # ── Complétion du module ──
    results = st.session_state.exercise_results.get(mod_id, {})
    if all(results.get(f"ex{i}", False) for i in range(1, 3)):
        st.balloons()
        st.success("🎉 Module Variables terminé ! Tu passes au niveau suivant.")
        mark_module_complete(mod_id, 45)  # Bonus de complétion

# ─────────────────────────────────────────────────────────────────
# MODULE 2 — CONDITIONS
# ─────────────────────────────────────────────────────────────────

def module_conditions():
    """Module pédagogique sur les structures conditionnelles."""
    mod_id = "conditions"
    st.markdown("## 🔀 Module 2 — Conditions (if / elif / else)")

    render_theory("""
    <p>Les <b>conditions</b> permettent d'exécuter du code différent selon une valeur.
    La structure est basée sur l'<b>indentation</b> (4 espaces ou 1 tabulation).</p>
    <pre><code>if condition:
    # code si vrai
elif autre_condition:
    # sinon si...
else:
    # sinon</code></pre>
    <p>Opérateurs de comparaison : <code>==</code>, <code>!=</code>, <code>&gt;</code>,
    <code>&lt;</code>, <code>&gt;=</code>, <code>&lt;=</code></p>
    <p>Opérateurs logiques : <code>and</code>, <code>or</code>, <code>not</code></p>
    """, "Structures Conditionnelles")

    render_code_example("""
note = 75

if note >= 90:
    mention = "Très Bien"
elif note >= 75:
    mention = "Bien"
elif note >= 60:
    mention = "Assez Bien"
else:
    mention = "Insuffisant"

print(f"Note: {note}/100 → Mention: {mention}")
    """)

    st.markdown("---")

    # ── Exercice 1 ──
    exercise_header(mod_id, 1, "Parité d'un nombre", 30)
    st.write("Écris un programme qui déclare `n = 17` et affiche `\"pair\"` ou `\"impair\"` selon sa valeur.")
    st.markdown('<div class="hint-box">Utilise l\'opérateur modulo <code>%</code> : si <code>n % 2 == 0</code>, c\'est pair.</div>', unsafe_allow_html=True)

    code1 = st_ace(
        placeholder="n = 17\n# Vérifie si n est pair ou impair...\n",
        language="python", theme="monokai",
        height=130, key="cond_ex1",
        auto_update=True, wrap=True,
    )
    if st.button("✅ Vérifier", key="cond_check1"):
        ns, err = safe_exec(code1 or "")
        if err:
            st.error(f"❌ Erreur : `{err}`")
        elif "if" not in (code1 or ""):
            st.warning("⚠️ Utilise une condition `if` !")
        elif "n" not in ns:
            st.warning("⚠️ Définis la variable `n = 17`.")
        else:
            output = ns.get("__stdout__", "").strip().lower()
            if "impair" in output:
                st.success("✅ Correct ! 17 est bien impair.")
                mark_exercise_done(mod_id, "ex1", 30)
            elif "pair" in output:
                st.warning("⚠️ Attention : 17 est impair, pas pair.")
            else:
                st.warning("⚠️ Assure-toi d'afficher `\"pair\"` ou `\"impair\"` avec `print()`.")

    st.markdown("---")

    # ── Exercice 2 ──
    exercise_header(mod_id, 2, "Système de notes", 40)
    st.write("Crée une variable `note = 82` et affiche la mention correspondante : Très Bien (≥90), Bien (≥75), Passable (≥60), Insuffisant (<60).")

    code2 = st_ace(
        placeholder="note = 82\n# Détermine la mention...\n",
        language="python", theme="monokai",
        height=180, key="cond_ex2",
        auto_update=True, wrap=True,
    )
    if st.button("✅ Vérifier", key="cond_check2"):
        ns, err = safe_exec(code2 or "")
        if err:
            st.error(f"❌ Erreur : `{err}`")
        else:
            output = ns.get("__stdout__", "").strip().lower()
            if "bien" in output and "très" not in output and "assez" not in output:
                st.success("✅ Parfait ! 82/100 → Mention Bien.")
                mark_exercise_done(mod_id, "ex2", 40)
                award_badge("🔀", "Décideur", "badge-purple", "cond_done")
            elif "très bien" in output:
                st.warning("⚠️ 82 est ≥75 mais <90, c'est \"Bien\", pas \"Très Bien\".")
            else:
                st.warning("⚠️ Vérifie ta logique et assure-toi d'afficher la mention avec `print()`.")

    results = st.session_state.exercise_results.get(mod_id, {})
    if all(results.get(f"ex{i}", False) for i in range(1, 3)):
        st.success("🎉 Module Conditions terminé !")
        mark_module_complete(mod_id, 70)

# ─────────────────────────────────────────────────────────────────
# MODULE 3 — BOUCLES
# ─────────────────────────────────────────────────────────────────

def module_boucles():
    """Module pédagogique sur les boucles for et while."""
    mod_id = "boucles"
    st.markdown("## 🔁 Module 3 — Boucles (for / while)")

    tab1, tab2 = st.tabs(["🔄 Boucle for", "🔁 Boucle while"])

    with tab1:
        render_theory("""
        <p>La boucle <code>for</code> itère sur une séquence (liste, range, chaîne, etc.).</p>
        <pre><code>for variable in séquence:
    # code répété</code></pre>
        <p><code>range(n)</code> génère les entiers de 0 à n-1.<br>
        <code>range(a, b)</code> génère de a à b-1.</p>
        """, "Boucle for")

        render_code_example("""
# Afficher les carrés de 1 à 5
for i in range(1, 6):
    print(f"{i}² = {i**2}")

# Parcourir une liste
fruits = ["pomme", "banane", "cerise"]
for fruit in fruits:
    print(f"J'aime les {fruit}s !")
        """)

    with tab2:
        render_theory("""
        <p>La boucle <code>while</code> répète tant qu'une condition est vraie.
        Attention aux <b>boucles infinies</b> !</p>
        <pre><code>compteur = 0
while compteur < 5:
    # code
    compteur += 1   # incrémentation obligatoire !</code></pre>
        """, "Boucle while")

        render_code_example("""
# Compte à rebours
n = 5
while n > 0:
    print(f"Compte : {n}")
    n -= 1
print("Décollage ! 🚀")
        """)

    st.markdown("---")

    # ── Exercice 1 ──
    exercise_header(mod_id, 1, "Table de multiplication", 35)
    st.write("Affiche la table de multiplication de `7` (de 7×1 à 7×10) en utilisant une boucle `for`.")
    st.markdown('<div class="hint-box">Format attendu : <code>7 x 1 = 7</code>, <code>7 x 2 = 14</code>, etc.</div>', unsafe_allow_html=True)

    code1 = st_ace(
        placeholder="# Affiche la table de 7 avec une boucle for\n",
        language="python", theme="monokai",
        height=130, key="boucle_ex1",
        auto_update=True, wrap=True,
    )
    if st.button("✅ Vérifier", key="boucle_check1"):
        ns, err = safe_exec(code1 or "")
        if err:
            st.error(f"❌ Erreur : `{err}`")
        elif "for" not in (code1 or ""):
            st.warning("⚠️ Utilise une boucle `for` !")
        else:
            output = ns.get("__stdout__", "")
            lines = [l.strip() for l in output.strip().split("\n") if l.strip()]
            if len(lines) >= 10 and "70" in output:
                st.success("✅ Excellent ! Ta table de 7 est correcte !")
                mark_exercise_done(mod_id, "ex1", 35)
            elif len(lines) < 10:
                st.warning(f"⚠️ Il faut 10 lignes. Tu en as {len(lines)}.")
            else:
                st.warning("⚠️ Vérifie tes calculs — le dernier résultat doit être 70.")

    st.markdown("---")

    # ── Exercice 2 ──
    exercise_header(mod_id, 2, "Somme avec while", 40)
    st.write("Calcule et affiche la somme des entiers de 1 à 100 en utilisant une boucle `while`. (Résultat attendu : 5050)")
    st.markdown('<div class="hint-box">Initialise <code>somme = 0</code> et <code>i = 1</code>, puis incrémente jusqu\'à 100.</div>', unsafe_allow_html=True)

    code2 = st_ace(
        placeholder="# Calcule la somme 1+2+...+100 avec while\n",
        language="python", theme="monokai",
        height=150, key="boucle_ex2",
        auto_update=True, wrap=True,
    )
    if st.button("✅ Vérifier", key="boucle_check2"):
        ns, err = safe_exec(code2 or "")
        if err:
            st.error(f"❌ Erreur : `{err}`")
        elif "while" not in (code2 or ""):
            st.warning("⚠️ Utilise une boucle `while` !")
        else:
            output = ns.get("__stdout__", "")
            if "5050" in output:
                st.success("✅ Bravo ! 1+2+...+100 = 5050. Gauss serait fier !")
                mark_exercise_done(mod_id, "ex2", 40)
                award_badge("🔁", "Boucleur Pro", "badge-gold", "boucle_done")
            else:
                st.warning(f"⚠️ Résultat trouvé dans ton output : `{output.strip()}`. Attendu : `5050`.")

    results = st.session_state.exercise_results.get(mod_id, {})
    if all(results.get(f"ex{i}", False) for i in range(1, 3)):
        st.success("🎉 Module Boucles terminé !")
        mark_module_complete(mod_id, 75)

# ─────────────────────────────────────────────────────────────────
# MODULE 4 — FONCTIONS
# ─────────────────────────────────────────────────────────────────

def module_fonctions():
    """Module pédagogique sur les fonctions et procédures."""
    mod_id = "fonctions"
    st.markdown("## ⚙️ Module 4 — Fonctions & Procédures")

    render_theory("""
    <p>Une <b>fonction</b> est un bloc de code réutilisable qui prend des paramètres et <code>return</code> une valeur.</p>
    <p>Une <b>procédure</b> est une fonction sans retour (ou <code>return None</code>).</p>
    <pre><code>def nom_fonction(param1, param2):
    \"\"\"Documentation de la fonction.\"\"\"
    # corps
    return résultat</code></pre>
    <p>Les fonctions respectent le principe <b>DRY</b> : Don't Repeat Yourself.</p>
    """, "Fonctions en Python")

    render_code_example("""
def aire_rectangle(longueur, largeur):
    \"\"\"Calcule et retourne l'aire d'un rectangle.\"\"\"
    return longueur * largeur

def saluer(prenom, formel=False):
    \"\"\"Procédure : affiche un message de salutation.\"\"\"
    if formel:
        print(f"Bonjour, Monsieur/Madame {prenom}.")
    else:
        print(f"Salut, {prenom} !")

# Appels
print(aire_rectangle(5, 3))   # 15
saluer("Alice")                # Salut, Alice !
saluer("Dupont", formel=True)  # Bonjour, Monsieur/Madame Dupont.
    """)

    st.markdown("---")

    # ── Exercice 1 ──
    exercise_header(mod_id, 1, "Fonction puissance", 40)
    st.write("Crée une fonction `puissance(base, exp)` qui retourne `base` élevé à la puissance `exp`. Teste avec `puissance(2, 10)` qui doit afficher `1024`.")
    st.markdown('<div class="hint-box">En Python, l\'opérateur puissance est <code>**</code> : <code>2 ** 10 == 1024</code></div>', unsafe_allow_html=True)

    code1 = st_ace(
        placeholder="def puissance(base, exp):\n    # Ton code ici...\n    pass\n\nprint(puissance(2, 10))  # Doit afficher 1024\n",
        language="python", theme="monokai",
        height=170, key="func_ex1",
        auto_update=True, wrap=True,
    )
    if st.button("✅ Vérifier", key="func_check1"):
        ns, err = safe_exec(code1 or "")
        if err:
            st.error(f"❌ Erreur : `{err}`")
        elif "puissance" not in ns:
            st.warning("⚠️ La fonction `puissance` n'est pas définie.")
        else:
            try:
                result = ns["puissance"](2, 10)
                if result == 1024:
                    # Vérification supplémentaire
                    r2 = ns["puissance"](3, 3)
                    if r2 == 27:
                        st.success("✅ Parfait ! `puissance(2, 10) = 1024` et `puissance(3, 3) = 27` ✓")
                        mark_exercise_done(mod_id, "ex1", 40)
                    else:
                        st.warning(f"⚠️ `puissance(3, 3)` donne `{r2}` mais devrait donner `27`.")
                else:
                    st.warning(f"⚠️ `puissance(2, 10)` donne `{result}` mais devrait donner `1024`.")
            except Exception as e:
                st.error(f"❌ Erreur lors du test : {e}")

    st.markdown("---")

    # ── Exercice 2 ──
    exercise_header(mod_id, 2, "Fonction récursive — Factorielle", 50)
    st.write("Écris une fonction `factorielle(n)` qui calcule `n!` (n factorielle). Ex: `factorielle(5)` = `120`.")
    st.markdown('<div class="hint-box">Rappel: 5! = 5×4×3×2×1. Cas de base: factorielle(0) = 1.</div>', unsafe_allow_html=True)

    code2 = st_ace(
        placeholder="def factorielle(n):\n    # Cas de base :\n    # Récursion :\n    pass\n\nprint(factorielle(5))  # 120\n",
        language="python", theme="monokai",
        height=180, key="func_ex2",
        auto_update=True, wrap=True,
    )
    if st.button("✅ Vérifier", key="func_check2"):
        ns, err = safe_exec(code2 or "")
        if err:
            st.error(f"❌ Erreur : `{err}`")
        elif "factorielle" not in ns:
            st.warning("⚠️ La fonction `factorielle` n'est pas définie.")
        else:
            try:
                tests = [(0, 1), (1, 1), (5, 120), (6, 720)]
                all_ok = all(ns["factorielle"](n) == exp for n, exp in tests)
                if all_ok:
                    st.success("✅ Excellent ! Tous les tests passent. La récursion maîtrisée !")
                    mark_exercise_done(mod_id, "ex2", 50)
                    award_badge("⚙️", "Ingénieur", "badge-silver", "func_done")
                else:
                    for n, exp in tests:
                        got = ns["factorielle"](n)
                        if got != exp:
                            st.warning(f"⚠️ `factorielle({n})` donne `{got}`, attendu `{exp}`.")
                            break
            except Exception as e:
                st.error(f"❌ Erreur lors du test : {e}")

    results = st.session_state.exercise_results.get(mod_id, {})
    if all(results.get(f"ex{i}", False) for i in range(1, 3)):
        st.success("🎉 Module Fonctions terminé !")
        mark_module_complete(mod_id, 110)

# ─────────────────────────────────────────────────────────────────
# MODULE 5 — LISTES & TABLEAUX
# ─────────────────────────────────────────────────────────────────

def module_listes():
    """Module pédagogique sur les listes et tableaux Python."""
    mod_id = "listes"
    st.markdown("## 📋 Module 5 — Listes & Tableaux")

    render_theory("""
    <p>Une <b>liste</b> est une collection ordonnée et modifiable d'éléments.</p>
    <ul>
        <li>Déclaration : <code>ma_liste = [1, 2, 3]</code></li>
        <li>Accès par index (commence à 0) : <code>ma_liste[0]</code> → 1</li>
        <li>Index négatif (fin) : <code>ma_liste[-1]</code> → 3</li>
        <li>Slice : <code>ma_liste[1:3]</code> → [2, 3]</li>
    </ul>
    <p>Méthodes utiles : <code>append()</code>, <code>remove()</code>, <code>sort()</code>,
    <code>len()</code>, <code>in</code></p>
    """, "Listes Python")

    render_code_example("""
# Création
notes = [14, 18, 9, 16, 12]

# Opérations de base
print(f"Nombre de notes : {len(notes)}")
print(f"Meilleure note  : {max(notes)}")
print(f"Moyenne         : {sum(notes)/len(notes):.2f}")

# Modification
notes.append(20)      # Ajouter
notes.sort()          # Trier
notes.remove(9)       # Supprimer

# Parcours
for i, note in enumerate(notes):
    print(f"Note {i+1}: {note}/20")
    """)

    st.markdown("---")

    # ── Exercice 1 ──
    exercise_header(mod_id, 1, "Manipulation de liste", 40)
    st.write("""
    Crée une liste `temperatures = [22, 17, 30, 25, 19, 28, 15]`.
    Puis calcule et affiche :
    - La température max
    - La température min
    - La moyenne (arrondie à 1 décimale)
    """)
    st.markdown('<div class="hint-box">Utilise <code>max()</code>, <code>min()</code>, <code>sum()</code>, <code>len()</code>, <code>round()</code></div>', unsafe_allow_html=True)

    code1 = st_ace(
        placeholder="temperatures = [22, 17, 30, 25, 19, 28, 15]\n# Ton code ici...\n",
        language="python", theme="monokai",
        height=170, key="liste_ex1",
        auto_update=True, wrap=True,
    )
    if st.button("✅ Vérifier", key="liste_check1"):
        ns, err = safe_exec(code1 or "")
        if err:
            st.error(f"❌ Erreur : `{err}`")
        else:
            output = ns.get("__stdout__", "")
            checks = ["30" in output, "15" in output, "22.3" in output or "22.3" in output]
            if all(checks):
                st.success("✅ Parfait ! Max=30, Min=15, Moyenne=22.3 ✓")
                mark_exercise_done(mod_id, "ex1", 40)
            else:
                hints = []
                if "30" not in output: hints.append("max=30 manquant")
                if "15" not in output: hints.append("min=15 manquant")
                if "22.3" not in output: hints.append("moyenne≈22.3 manquante")
                st.warning(f"⚠️ Problèmes détectés : {', '.join(hints)}")

    st.markdown("---")

    # ── Exercice 2 ──
    exercise_header(mod_id, 2, "Liste en compréhension", 50)
    st.write("Crée une liste `carres` contenant les carrés des nombres pairs de 1 à 20, en une seule ligne (list comprehension). Affiche-la.")
    st.markdown('<div class="hint-box">Syntaxe : <code>[expr for x in range(...) if condition]</code></div>', unsafe_allow_html=True)

    code2 = st_ace(
        placeholder="# Une seule ligne avec une list comprehension\ncarres = [...]\nprint(carres)\n",
        language="python", theme="monokai",
        height=130, key="liste_ex2",
        auto_update=True, wrap=True,
    )
    if st.button("✅ Vérifier", key="liste_check2"):
        ns, err = safe_exec(code2 or "")
        if err:
            st.error(f"❌ Erreur : `{err}`")
        elif "carres" not in ns:
            st.warning("⚠️ La variable `carres` n'est pas définie.")
        else:
            expected = [x**2 for x in range(1, 21) if x % 2 == 0]
            if ns["carres"] == expected:
                st.success(f"✅ Magnifique ! `carres = {expected}`")
                mark_exercise_done(mod_id, "ex2", 50)
                award_badge("📋", "Liste Maître", "badge-bronze", "liste_done")
            else:
                st.warning(f"⚠️ Résultat obtenu : `{ns['carres']}`\nAttendu : `{expected}`")

    results = st.session_state.exercise_results.get(mod_id, {})
    if all(results.get(f"ex{i}", False) for i in range(1, 3)):
        st.success("🎉 Module Listes terminé !")
        mark_module_complete(mod_id, 90)

# ─────────────────────────────────────────────────────────────────
# MODULE 6 — DICTIONNAIRES (ENREGISTREMENTS)
# ─────────────────────────────────────────────────────────────────

def module_dicts():
    """Module pédagogique sur les dictionnaires (enregistrements)."""
    mod_id = "dicts"
    st.markdown("## 🗂️ Module 6 — Dictionnaires & Enregistrements")

    render_theory("""
    <p>Un <b>dictionnaire</b> est une structure clé → valeur. Il correspond à la notion
    d'<b>enregistrement</b> en algorithmique (comme une fiche avec des champs).</p>
    <pre><code>personne = {
    "nom":   "Alice",
    "age":   30,
    "ville": "Paris"
}</code></pre>
    <ul>
        <li>Accès : <code>personne["nom"]</code> → "Alice"</li>
        <li>Ajout  : <code>personne["email"] = "alice@mail.com"</code></li>
        <li>Clés   : <code>personne.keys()</code></li>
        <li>Valeurs: <code>personne.values()</code></li>
        <li>Items  : <code>personne.items()</code></li>
        <li>Test   : <code>"nom" in personne</code></li>
    </ul>
    """, "Dictionnaires = Enregistrements")

    render_code_example("""
# Modélisation d'un étudiant (enregistrement)
etudiant = {
    "nom":    "Dupont",
    "prenom": "Jean",
    "notes":  [14, 16, 12, 18],
    "actif":  True
}

# Calcul de moyenne
moyenne = sum(etudiant["notes"]) / len(etudiant["notes"])
etudiant["moyenne"] = round(moyenne, 2)

# Affichage
for cle, valeur in etudiant.items():
    print(f"  {cle:10}: {valeur}")
    """)

    st.markdown("---")

    # ── Exercice 1 ──
    exercise_header(mod_id, 1, "Créer un enregistrement", 45)
    st.write("""
    Crée un dictionnaire `produit` représentant un article avec les champs :
    - `nom` : `"Clavier"`, `prix` : `49.99`, `stock` : `15`, `disponible` : `True`

    Puis affiche chaque champ avec `print()`.
    """)

    code1 = st_ace(
        placeholder="produit = {\n    # Complète ici...\n}\n# Affiche chaque champ\n",
        language="python", theme="monokai",
        height=180, key="dict_ex1",
        auto_update=True, wrap=True,
    )
    if st.button("✅ Vérifier", key="dict_check1"):
        ns, err = safe_exec(code1 or "")
        if err:
            st.error(f"❌ Erreur : `{err}`")
        elif "produit" not in ns or not isinstance(ns["produit"], dict):
            st.warning("⚠️ `produit` doit être un dictionnaire.")
        else:
            p = ns["produit"]
            checks = {
                "nom":        p.get("nom") == "Clavier",
                "prix":       abs(p.get("prix", 0) - 49.99) < 0.01,
                "stock":      p.get("stock") == 15,
                "disponible": p.get("disponible") is True,
            }
            missing = [k for k, v in checks.items() if not v]
            if not missing:
                st.success("✅ Enregistrement parfait ! Tous les champs sont corrects.")
                mark_exercise_done(mod_id, "ex1", 45)
            else:
                st.warning(f"⚠️ Champs incorrects ou manquants : `{', '.join(missing)}`")

    st.markdown("---")

    # ── Exercice 2 ──
    exercise_header(mod_id, 2, "Liste de dictionnaires", 55)
    st.write("""
    Crée une liste `etudiants` avec 3 dictionnaires (chacun avec `nom` et `note`).
    Puis affiche le nom de l'étudiant avec la meilleure note.
    """)
    st.markdown('<div class="hint-box">Utilise <code>max(etudiants, key=lambda e: e["note"])</code> pour trouver le meilleur.</div>', unsafe_allow_html=True)

    code2 = st_ace(
        placeholder='etudiants = [\n    {"nom": "Alice", "note": 16},\n    # Ajoute 2 autres...\n]\n# Trouve et affiche le meilleur\n',
        language="python", theme="monokai",
        height=200, key="dict_ex2",
        auto_update=True, wrap=True,
    )
    if st.button("✅ Vérifier", key="dict_check2"):
        ns, err = safe_exec(code2 or "")
        if err:
            st.error(f"❌ Erreur : `{err}`")
        elif "etudiants" not in ns:
            st.warning("⚠️ La liste `etudiants` n'est pas définie.")
        elif not isinstance(ns["etudiants"], list) or len(ns["etudiants"]) < 3:
            st.warning("⚠️ `etudiants` doit contenir au moins 3 dictionnaires.")
        else:
            try:
                output = ns.get("__stdout__", "")
                best = max(ns["etudiants"], key=lambda e: e["note"])
                if best["nom"].lower() in output.lower():
                    st.success(f"✅ Correct ! Le meilleur étudiant est **{best['nom']}** avec {best['note']}/20.")
                    mark_exercise_done(mod_id, "ex2", 55)
                    award_badge("🗂️", "Data Engineer", "badge-purple", "dict_done")
                else:
                    st.warning(f"⚠️ Le meilleur étudiant est `{best['nom']}` mais il n'apparaît pas dans ton output.")
            except (KeyError, TypeError) as e:
                st.error(f"❌ Problème de structure : {e}")

    results = st.session_state.exercise_results.get(mod_id, {})
    if all(results.get(f"ex{i}", False) for i in range(1, 3)):
        st.success("🎉 Module Dictionnaires terminé !")
        mark_module_complete(mod_id, 100)

# ─────────────────────────────────────────────────────────────────
# MODULE 7 — QUIZ FINAL
# ─────────────────────────────────────────────────────────────────

# Définition des questions du quiz final
QUIZ_QUESTIONS = [
    # ── QCM ──
    {
        "type": "qcm",
        "question": "Quelle est la syntaxe correcte pour créer une liste vide en Python ?",
        "options": ["list = {}", "list = []", "list = ()", "list = <empty>"],
        "answer": "list = []",
        "explication": "`[]` crée une liste, `{}` un dict vide, `()` un tuple.",
    },
    {
        "type": "qcm",
        "question": "Quel opérateur est utilisé pour l'exponentiation (puissance) en Python ?",
        "options": ["^", "**", "^^", "pow"],
        "answer": "**",
        "explication": "Python utilise `**` pour la puissance : `2 ** 10 = 1024`.",
    },
    {
        "type": "qcm",
        "question": "Que retourne `len(\"Bonjour\")` ?",
        "options": ["6", "7", "8", "None"],
        "answer": "7",
        "explication": "`\"Bonjour\"` contient 7 caractères : B-o-n-j-o-u-r.",
    },
    {
        "type": "qcm",
        "question": "Quelle boucle est la plus adaptée quand on ne connaît pas le nombre d'itérations à l'avance ?",
        "options": ["for", "while", "do-while", "loop"],
        "answer": "while",
        "explication": "`while` continue tant qu'une condition est vraie, sans connaître le nombre d'itérations.",
    },
    {
        "type": "qcm",
        "question": "Comment accède-t-on au dernier élément d'une liste `lst` ?",
        "options": ["lst[last]", "lst[-1]", "lst[len]", "lst.last()"],
        "answer": "lst[-1]",
        "explication": "Les indices négatifs accèdent depuis la fin : `lst[-1]` = dernier, `lst[-2]` = avant-dernier…",
    },
    {
        "type": "qcm",
        "question": "Qu'affiche ce code ?\n```python\nx = 5\nif x > 3:\n    print('A')\nelse:\n    print('B')\n```",
        "options": ["A", "B", "AB", "Erreur"],
        "answer": "A",
        "explication": "5 > 3 est True, donc le bloc `if` s'exécute et affiche 'A'.",
    },
    # ── CODE ──
    {
        "type": "code",
        "question": "Écris une fonction `est_premier(n)` qui retourne `True` si `n` est premier, `False` sinon. Un nombre premier est divisible uniquement par 1 et lui-même.",
        "test_cases": [
            (2, True), (3, True), (4, False),
            (11, True), (12, False), (17, True), (1, False),
        ],
        "func_name": "est_premier",
        "placeholder": "def est_premier(n):\n    # Un nombre est premier si aucun entier de 2 à n-1 ne le divise\n    pass\n",
        "hint": "Pour chaque i de 2 à n-1, vérifie si `n % i == 0`. Si oui, pas premier.",
        "xp": 80,
    },
    {
        "type": "code",
        "question": "Crée une fonction `inverser_liste(lst)` qui retourne une nouvelle liste avec les éléments dans l'ordre inverse, **sans utiliser** `.reverse()` ni `[::-1]`.",
        "test_cases": [
            ([1, 2, 3], [3, 2, 1]),
            ([5], [5]),
            ([], []),
            (["a", "b", "c"], ["c", "b", "a"]),
        ],
        "func_name": "inverser_liste",
        "placeholder": "def inverser_liste(lst):\n    # Construis la liste inversée manuellement\n    pass\n",
        "hint": "Utilise une boucle `for i in range(len(lst)-1, -1, -1)` et `append()`.",
        "xp": 80,
    },
]

def page_quiz():
    """Page du quiz final avec QCM et exercices de code."""
    st.markdown("## 🏆 Quiz Final — Teste tes Compétences")

    # Vérification du déverrouillage
    done_count = len(st.session_state.completed_modules)
    total_mod  = len(MODULES) - 1
    if done_count < 3:
        st.warning(f"🔒 Termine au moins **3 modules** pour débloquer le quiz. ({done_count}/{total_mod} faits)")
        return

    if st.session_state.quiz_score is not None:
        _render_quiz_results()
        return

    st.info("📋 Le quiz contient des QCM et des exercices de code. Bonne chance !")

    with st.form("quiz_final_form"):
        answers = {}

        # ── Section QCM ──
        st.markdown("### 📝 Partie 1 — Questions à Choix Multiple")
        qcm_questions = [q for q in QUIZ_QUESTIONS if q["type"] == "qcm"]
        for i, q in enumerate(qcm_questions):
            st.markdown(f"""
            <div class="quiz-question">
                <b>Question {i+1}</b> : {q['question']}
            </div>
            """, unsafe_allow_html=True)
            # Affichage du code inline si présent
            if "```python" in q["question"]:
                # Déjà rendu par markdown
                pass
            ans = st.radio(
                f"Q{i+1}", q["options"],
                key=f"qcm_{i}", label_visibility="collapsed"
            )
            answers[f"qcm_{i}"] = ans

        # ── Section Code ──
        st.markdown("### 💻 Partie 2 — Exercices de Code")
        code_questions = [q for q in QUIZ_QUESTIONS if q["type"] == "code"]
        for i, q in enumerate(code_questions):
            st.markdown(f"""
            <div class="quiz-question">
                <b>Exercice {i+1}</b> : {q['question']}
            </div>
            """, unsafe_allow_html=True)
            st.markdown(f'<div class="hint-box">{q["hint"]}</div>', unsafe_allow_html=True)
            code = st_ace(
                placeholder=q["placeholder"],
                language="python", theme="monokai",
                height=160, key=f"quiz_code_{i}",
                auto_update=True, wrap=True,
            )
            answers[f"code_{i}"] = code

        submitted = st.form_submit_button("🚀 Soumettre le Quiz Final", use_container_width=True)

    if submitted:
        _evaluate_quiz(answers, qcm_questions, code_questions)
        st.rerun()

def _evaluate_quiz(answers: dict, qcm_questions: list, code_questions: list):
    """Évalue les réponses du quiz et calcule le score."""
    total_points = 0
    max_points   = len(qcm_questions) * 10 + sum(q["xp"] for q in code_questions)
    results      = {}

    # ── Évaluation QCM ──
    for i, q in enumerate(qcm_questions):
        key = f"qcm_{i}"
        correct = answers.get(key) == q["answer"]
        results[key] = {"correct": correct, "explication": q["explication"], "answer": q["answer"]}
        if correct:
            total_points += 10

    # ── Évaluation Code ──
    for i, q in enumerate(code_questions):
        key    = f"code_{i}"
        code   = answers.get(key, "")
        ns, err = safe_exec(code)
        passed  = 0
        total_t = len(q["test_cases"])

        if not err and q["func_name"] in ns:
            func = ns[q["func_name"]]
            for inp, expected in q["test_cases"]:
                try:
                    inp_arg = inp if isinstance(inp, list) else inp
                    got     = func(inp_arg)
                    if got == expected:
                        passed += 1
                except Exception:
                    pass
        score_code = int((passed / total_t) * q["xp"])
        total_points += score_code
        results[key]  = {"passed": passed, "total": total_t, "xp": score_code, "error": err}

    pct = round(total_points / max_points * 100)

    st.session_state.quiz_score   = pct
    st.session_state.quiz_answers = results

    # Badges selon le score
    if pct >= 90:
        award_badge("🥇", "Expert Python", "badge-gold", "quiz_gold")
        mark_module_complete("quiz", 300)
    elif pct >= 70:
        award_badge("🥈", "Pythoniste", "badge-silver", "quiz_silver")
        mark_module_complete("quiz", 200)
    elif pct >= 50:
        award_badge("🥉", "Apprenti", "badge-bronze", "quiz_bronze")
        mark_module_complete("quiz", 100)

def _render_quiz_results():
    """Affiche les résultats détaillés du quiz."""
    score = st.session_state.quiz_score
    results = st.session_state.quiz_answers

    # ── Détermine le message selon le score ──
    if score >= 90:
        emoji, msg, color = "🥇", "Exceptionnel ! Tu es un vrai Pythoniste !", "#FFD700"
    elif score >= 75:
        emoji, msg, color = "🥈", "Très bien ! Tu maîtrises les bases solides.", "#C0C0C0"
    elif score >= 60:
        emoji, msg, color = "🥉", "Bien joué ! Encore un peu de pratique.", "#CD7F32"
    elif score >= 40:
        emoji, msg, color = "📚", "Pas mal ! Revois les modules avant de refaire.", "#6C63FF"
    else:
        emoji, msg, color = "💪", "Continue ! Chaque expert a été débutant un jour.", "#FF6B6B"

    st.markdown(f"""
    <div class="score-display">
        <div style="font-size:3rem;">{emoji}</div>
        <div class="big-score">{score}%</div>
        <div style="font-size:1.1rem; color:{color}; font-weight:700;">{msg}</div>
        <div style="color:#8B949E; margin-top:0.5rem;">Score final : {score}/100</div>
    </div>
    """, unsafe_allow_html=True)

    # ── Détail des réponses QCM ──
    st.markdown("### 📊 Détail des résultats")
    qcm_questions = [q for q in QUIZ_QUESTIONS if q["type"] == "qcm"]
    for i, q in enumerate(qcm_questions):
        key  = f"qcm_{i}"
        info = results.get(key, {})
        icon = "✅" if info.get("correct") else "❌"
        with st.expander(f"{icon} Question {i+1} — {q['question'][:60]}..."):
            if info.get("correct"):
                st.success(f"✅ Bonne réponse : `{q['answer']}`")
            else:
                st.error(f"❌ Réponse correcte : `{info.get('answer')}`")
            st.info(f"💡 **Explication** : {info.get('explication', '')}")

    # ── Détail des réponses Code ──
    code_questions = [q for q in QUIZ_QUESTIONS if q["type"] == "code"]
    for i, q in enumerate(code_questions):
        key  = f"code_{i}"
        info = results.get(key, {})
        passed, total_t = info.get("passed", 0), info.get("total", 1)
        icon = "✅" if passed == total_t else ("⚠️" if passed > 0 else "❌")
        with st.expander(f"{icon} Exercice {i+1} — {passed}/{total_t} tests réussis ({info.get('xp', 0)} XP)"):
            if info.get("error"):
                st.error(f"Erreur : `{info['error']}`")
            elif passed == total_t:
                st.success("Tous les tests passent ! ✨")
            else:
                st.warning(f"{passed}/{total_t} tests réussis.")

    # ── Recommandations ──
    st.markdown("### 🎯 Recommandations")
    if score < 60:
        st.info("Revois les modules de base : **Variables**, **Conditions**, **Boucles**.")
    elif score < 80:
        st.info("Approfondis les **Fonctions** et les structures de données (**Listes**, **Dictionnaires**).")
    else:
        st.success("🚀 Tu es prêt pour les concepts avancés : classes, fichiers, APIs !")

    # ── Reset bouton ──
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🔄 Refaire le quiz"):
            st.session_state.quiz_score   = None
            st.session_state.quiz_answers = {}
            st.rerun()
    with col2:
        # Rapport téléchargeable (JSON)
        report = {
            "utilisateur": st.session_state.username,
            "score_pct":   score,
            "xp_total":    st.session_state.xp,
            "badges":      [b[1] for b in st.session_state.badges],
            "modules_termines": st.session_state.completed_modules,
            "date":        str(datetime.now()),
        }
        st.download_button(
            "💾 Télécharger mon rapport",
            data=json.dumps(report, ensure_ascii=False, indent=2),
            file_name=f"pythonium_rapport_{st.session_state.username or 'anonyme'}.json",
            mime="application/json",
        )

# ─────────────────────────────────────────────────────────────────
# ROUTEUR PRINCIPAL
# ─────────────────────────────────────────────────────────────────

def main():
    """Point d'entrée principal — injecte le CSS et route vers la bonne page."""
    # Injection du CSS
    st.markdown(CUSTOM_CSS, unsafe_allow_html=True)

    # Rendu de la sidebar et récupération de la page active
    page = render_sidebar()

    # ── Routing ──
    route_map = {
        "🏠 Accueil":                 page_accueil,
        "📦 Variables & Types":        module_variables,
        "🔀 Conditions (if/else)":     module_conditions,
        "🔁 Boucles (for/while)":      module_boucles,
        "⚙️ Fonctions":               module_fonctions,
        "📋 Listes & Tableaux":        module_listes,
        "🗂️ Dictionnaires":            module_dicts,
        "🏆 Quiz Final":               page_quiz,
    }

    handler = route_map.get(page, page_accueil)
    handler()

# ─────────────────────────────────────────────────────────────────
# POINT D'ENTRÉE
# ─────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    main()