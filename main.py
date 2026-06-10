import streamlit as st
from streamlit_agraph import agraph, Node, Edge, Config
import asyncio
import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from swarm.orchestrator import run_complex_swarm
from swarm.agents import DOMAINS

st.set_page_config(page_title="Pan-Epistemic Swarm Tutor", layout="wide")

# ══════════════════════════════════════════════════════════════
#  PROFESSIONAL DESIGN SYSTEM — Clean, Minimal, Sophisticated
# ══════════════════════════════════════════════════════════════
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap');

    /* ═══════════════════════════════════════════ */
    /*  KEYFRAME ANIMATIONS                       */
    /* ═══════════════════════════════════════════ */
    @keyframes borderShift {
        0%   { border-color: rgba(99, 102, 241, 0.2); }
        25%  { border-color: rgba(139, 92, 246, 0.25); }
        50%  { border-color: rgba(6, 182, 212, 0.2); }
        75%  { border-color: rgba(236, 72, 153, 0.2); }
        100% { border-color: rgba(99, 102, 241, 0.2); }
    }
    @keyframes livePulse {
        0%, 100% { box-shadow: 0 0 0 0 rgba(34, 197, 94, 0.6); }
        50% { box-shadow: 0 0 0 4px rgba(34, 197, 94, 0); }
    }
    @keyframes gradientBg {
        0%   { background-position: 0% 50%; }
        50%  { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
    @keyframes fadeInUp {
        from { opacity: 0; transform: translateY(8px); }
        to   { opacity: 1; transform: translateY(0); }
    }
    @keyframes titleGlow {
        0%, 100% { text-shadow: 0 0 20px rgba(139, 92, 246, 0.0); }
        50%      { text-shadow: 0 0 30px rgba(139, 92, 246, 0.15); }
    }
    @keyframes textShimmer {
        0%   { background-position: -200% center; }
        100% { background-position: 200% center; }
    }
    @keyframes labelColorShift {
        0%   { color: #cbd5e1; }
        33%  { color: #c4b5fd; }
        66%  { color: #67e8f9; }
        100% { color: #cbd5e1; }
    }
    @keyframes agentFlicker {
        0%, 100% { opacity: 1; text-shadow: 0 0 4px rgba(56, 189, 248, 0.3); }
        50%      { opacity: 0.85; text-shadow: 0 0 8px rgba(56, 189, 248, 0.5); }
    }
    @keyframes gentleFloat {
        0%, 100% { transform: translateY(0); }
        50%      { transform: translateY(-2px); }
    }
    @keyframes typeReveal {
        from { max-width: 0; }
        to   { max-width: 100%; }
    }

    /* ═══════════════════════════════════════════ */
    /*  GLOBAL RESET & CURSORS                    */
    /* ═══════════════════════════════════════════ */
    html, body, [class*="css"], .stApp, p, span, li, label {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif !important;
        cursor: default;
    }
    a, button, [role="button"], input[type="submit"],
    .badge, .section-header .icon, .tel-line {
        cursor: pointer !important;
    }
    [data-testid="stChatInput"] textarea {
        cursor: text !important;
        color: #e2e8f0 !important;
        font-size: 0.9rem !important;
    }

    /* ═══════════════════════════════════════════ */
    /*  HIDE STREAMLIT CHROME                     */
    /* ═══════════════════════════════════════════ */
    header[data-testid="stHeader"],
    footer,
    #MainMenu,
    .stDeployButton,
    [data-testid="stToolbar"],
    [data-testid="stDecoration"],
    [data-testid="stStatusWidget"] {
        display: none !important;
    }

    /* ═══════════════════════════════════════════ */
    /*  ANIMATED BACKGROUND                       */
    /* ═══════════════════════════════════════════ */
    .stApp {
        background: linear-gradient(135deg, #0a0a14 0%, #0f0f1a 30%, #0d0b1a 60%, #0a0a14 100%) !important;
        background-size: 400% 400% !important;
        animation: gradientBg 20s ease infinite !important;
    }

    /* ═══════════════════════════════════════════ */
    /*  3D COLUMN CARDS WITH HOVER TRANSFORMS     */
    /* ═══════════════════════════════════════════ */
    [data-testid="column"] {
        background: rgba(19, 19, 31, 0.85) !important;
        border: 1px solid rgba(99, 102, 241, 0.12) !important;
        border-radius: 16px !important;
        padding: 1.25rem 1.5rem !important;
        margin: 0 0.35rem !important;
        backdrop-filter: blur(16px) !important;
        -webkit-backdrop-filter: blur(16px) !important;
        box-shadow:
            0 4px 6px rgba(0, 0, 0, 0.25),
            0 10px 20px rgba(0, 0, 0, 0.15),
            inset 0 1px 0 rgba(255, 255, 255, 0.04) !important;
        transition: transform 0.4s cubic-bezier(0.25, 0.46, 0.45, 0.94),
                    box-shadow 0.4s ease,
                    border-color 0.4s ease !important;
        animation: borderShift 12s ease-in-out infinite, fadeInUp 0.6s ease-out !important;
        perspective: 1000px !important;
    }
    [data-testid="column"]:hover {
        transform: translateY(-4px) scale(1.005) !important;
        box-shadow:
            0 8px 16px rgba(0, 0, 0, 0.35),
            0 20px 40px rgba(99, 102, 241, 0.08),
            inset 0 1px 0 rgba(255, 255, 255, 0.06) !important;
        border-color: rgba(139, 92, 246, 0.3) !important;
    }

    /* ═══════════════════════════════════════════ */
    /*  HERO TITLE WITH GLOW PULSE                */
    /* ═══════════════════════════════════════════ */
    h1 {
        font-family: 'Inter', sans-serif !important;
        font-size: 1.7rem !important;
        font-weight: 700 !important;
        letter-spacing: -0.03em !important;
        margin-bottom: 1.25rem !important;
        background: linear-gradient(90deg, #e2e8f0 0%, #c4b5fd 25%, #67e8f9 50%, #c4b5fd 75%, #e2e8f0 100%) !important;
        background-size: 200% auto !important;
        -webkit-background-clip: text !important;
        background-clip: text !important;
        -webkit-text-fill-color: transparent !important;
        animation: textShimmer 4s linear infinite, titleGlow 4s ease-in-out infinite !important;
    }
    [data-testid="stSubheader"] { display: none !important; }

    /* ═══════════════════════════════════════════ */
    /*  SECTION HEADERS WITH ICON HOVER           */
    /* ═══════════════════════════════════════════ */
    .section-header {
        display: flex;
        align-items: center;
        gap: 0.6rem;
        padding: 0.6rem 0;
        margin-bottom: 1rem;
        border-bottom: 1px solid rgba(139, 92, 246, 0.12);
        animation: fadeInUp 0.5s ease-out;
    }
    .section-header .icon {
        width: 32px; height: 32px;
        border-radius: 8px;
        display: flex; align-items: center; justify-content: center;
        font-size: 1rem;
        flex-shrink: 0;
        transition: transform 0.3s ease, box-shadow 0.3s ease;
    }
    .section-header:hover .icon {
        transform: scale(1.15) rotate(-5deg);
        box-shadow: 0 0 12px rgba(139, 92, 246, 0.25);
    }
    .section-header .title {
        font-size: 0.85rem;
        font-weight: 600;
        letter-spacing: 0.03em;
        text-transform: uppercase;
        transition: color 0.3s ease;
        background: linear-gradient(90deg, #e2e8f0, #c4b5fd, #67e8f9, #e2e8f0);
        background-size: 300% auto;
        -webkit-background-clip: text;
        background-clip: text;
        -webkit-text-fill-color: transparent;
        animation: textShimmer 6s linear infinite;
    }
    .section-header:hover .title {
        animation: textShimmer 2s linear infinite;
    }
    .section-header .subtitle {
        font-size: 0.7rem;
        color: #94a3b8;
        font-weight: 400;
    }

    /* ═══════════════════════════════════════════ */
    /*  LIVE INDICATOR DOT                        */
    /* ═══════════════════════════════════════════ */
    .live-dot {
        display: inline-block;
        width: 7px; height: 7px;
        border-radius: 50%;
        background: #22c55e;
        margin-right: 6px;
        animation: livePulse 2s ease-in-out infinite;
        vertical-align: middle;
    }

    /* ═══════════════════════════════════════════ */
    /*  CHAT MESSAGES WITH HOVER LIFT             */
    /* ═══════════════════════════════════════════ */

    [data-testid="stChatMessage"] {
        background: #191928 !important;
        border: 1px solid #232340 !important;
        border-radius: 12px !important;
        padding: 0.85rem 1rem !important;
        margin-bottom: 0.6rem !important;
        transition: transform 0.25s ease, border-color 0.3s ease, box-shadow 0.3s ease !important;
        animation: fadeInUp 0.4s ease-out backwards !important;
    }
    [data-testid="stChatMessage"]:nth-child(odd) { animation-delay: 0.05s !important; }
    [data-testid="stChatMessage"]:nth-child(even) { animation-delay: 0.15s !important; }
    [data-testid="stChatMessage"]:hover {
        transform: translateX(3px) !important;
        border-color: rgba(99, 102, 241, 0.2) !important;
        box-shadow: -3px 0 0 0 #8b5cf6 !important;
    }

    /* ═══════════════════════════════════════════ */
    /*  CHAT INPUT WITH GLOW FOCUS                */
    /* ═══════════════════════════════════════════ */
    [data-testid="stChatInput"] > div {
        background: #16162a !important;
        border: 1px solid #2a2a45 !important;
        border-radius: 12px !important;
        transition: all 0.3s ease !important;
    }
    [data-testid="stChatInput"] > div:focus-within {
        border-color: #8b5cf6 !important;
        box-shadow: 0 0 0 3px rgba(139, 92, 246, 0.12), 0 0 20px rgba(139, 92, 246, 0.06) !important;
        transform: scale(1.01) !important;
    }

    /* ═══════════════════════════════════════════ */
    /*  TELEMETRY CONSOLE WITH LINE HOVER         */
    /* ═══════════════════════════════════════════ */
    .tel-wrap {
        background: linear-gradient(180deg, #08081a, #0c0c18);
        border: 1px solid #1a1a30;
        border-radius: 10px;
        padding: 0.85rem 1rem;
        max-height: 180px;
        overflow-y: auto;
        animation: borderShift 10s ease-in-out infinite;
    }
    .tel-line {
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.75rem;
        line-height: 1.7;
        color: #c0c8d8;
        padding: 0.25rem 0.5rem;
        border-radius: 4px;
        border-bottom: 1px solid rgba(255,255,255,0.02);
        transition: background 0.2s ease, transform 0.2s ease;
    }
    .tel-line:hover {
        background: rgba(139, 92, 246, 0.06);
        transform: translateX(4px);
    }
    .tel-line .agent {
        color: #38bdf8;
        font-weight: 500;
        animation: agentFlicker 3s ease-in-out infinite;
    }
    .tel-line .thought {
        color: #a78bfa;
        font-style: italic;
        animation: fadeInUp 0.4s ease-out;
    }

    /* ═══════════════════════════════════════════ */
    /*  MASTERY BADGES WITH 3D HOVER              */
    /* ═══════════════════════════════════════════ */
    .badge {
        display: inline-block;
        padding: 0.3rem 0.7rem;
        border-radius: 6px;
        font-size: 0.72rem;
        font-weight: 500;
        font-family: 'Inter', sans-serif;
        margin: 0.2rem 0.25rem 0.2rem 0;
        letter-spacing: 0.01em;
        transition: transform 0.25s ease, box-shadow 0.25s ease, filter 0.25s ease;
        animation: fadeInUp 0.5s ease-out backwards;
    }
    .badge:nth-child(1) { animation-delay: 0.1s; }
    .badge:nth-child(2) { animation-delay: 0.2s; }
    .badge:nth-child(3) { animation-delay: 0.3s; }
    .badge:hover {
        transform: translateY(-2px) scale(1.05);
        filter: brightness(1.2);
    }
    .badge-g {
        background: #0d2818; border: 1px solid #166534; color: #4ade80;
    }
    .badge-g:hover { box-shadow: 0 4px 15px rgba(74, 222, 128, 0.15); }
    .badge-y {
        background: #271e05; border: 1px solid #854d0e; color: #fbbf24;
    }
    .badge-y:hover { box-shadow: 0 4px 15px rgba(251, 191, 36, 0.15); }
    .badge-r {
        background: #2a0a0a; border: 1px solid #991b1b; color: #f87171;
    }
    .badge-r:hover { box-shadow: 0 4px 15px rgba(248, 113, 113, 0.15); }

    /* ═══════════════════════════════════════════ */
    /*  CATEGORY LABELS                           */
    /* ═══════════════════════════════════════════ */
    .cat-label {
        font-size: 0.68rem;
        font-weight: 600;
        color: #cbd5e1;
        text-transform: uppercase;
        letter-spacing: 0.08em;
        margin: 0.85rem 0 0.35rem 0;
        animation: labelColorShift 8s ease-in-out infinite;
    }
    .cat-label:first-child { margin-top: 0; }
    .empty-hint {
        font-size: 0.72rem;
        color: #94a3b8;
        font-style: italic;
        animation: gentleFloat 3s ease-in-out infinite;
    }

    /* ═══════════════════════════════════════════ */
    /*  STATUS BAR (BOTTOM)                       */
    /* ═══════════════════════════════════════════ */
    .status-bar {
        position: fixed;
        bottom: 0; left: 0; right: 0;
        height: 28px;
        background: rgba(15, 15, 23, 0.9);
        backdrop-filter: blur(12px);
        border-top: 1px solid #1e1e30;
        display: flex;
        align-items: center;
        padding: 0 1rem;
        font-size: 0.65rem;
        color: #64748b;
        font-family: 'JetBrains Mono', monospace;
        z-index: 9999;
        gap: 1.5rem;
    }
    .status-bar .status-item {
        display: flex; align-items: center; gap: 0.3rem;
    }

    /* ═══════════════════════════════════════════ */
    /*  SCROLLBARS                                */
    /* ═══════════════════════════════════════════ */
    ::-webkit-scrollbar { width: 5px; }
    ::-webkit-scrollbar-track { background: transparent; }
    ::-webkit-scrollbar-thumb { background: #2a2a45; border-radius: 10px; }
    ::-webkit-scrollbar-thumb:hover { background: #3a3a5e; }
    
    /* ═══════════════════════════════════════════ */
    /*  STREAMLIT CONTAINERS                      */
    /* ═══════════════════════════════════════════ */
    [data-testid="stVerticalBlockBorderWrapper"] {
        border-color: #1e1e30 !important;
        border-radius: 12px !important;
    }
    
    /* ═══════════════════════════════════════════ */
    /*  GLOBAL TEXT                                */
    /* ═══════════════════════════════════════════ */
    p, span, li { color: #cbd5e1 !important; }
    strong { color: #e2e8f0 !important; }
</style>
""", unsafe_allow_html=True)

# Animated Logo + Title
import base64
logo_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "logo.png")
with open(logo_path, "rb") as f:
    logo_b64 = base64.b64encode(f.read()).decode()

st.markdown(f"""
<style>
    .logo-row {{
        display: flex;
        align-items: center;
        gap: 1.2rem;
        margin-bottom: 0.75rem;
    }}
    @keyframes logoSpin {{
        from {{ transform: rotate(0deg); }}
        to   {{ transform: rotate(360deg); }}
    }}
    @keyframes logoGlow {{
        0%, 100% {{ filter: drop-shadow(0 0 8px rgba(139,92,246,0.3)); }}
        50%      {{ filter: drop-shadow(0 0 18px rgba(139,92,246,0.6)) drop-shadow(0 0 30px rgba(34,211,238,0.2)); }}
    }}
    .logo-img {{
        width: 56px;
        height: 56px;
        border-radius: 50%;
        animation: logoSpin 20s linear infinite, logoGlow 3s ease-in-out infinite;
        flex-shrink: 0;
    }}
</style>
<div class="logo-row">
    <img class="logo-img" src="data:image/png;base64,{logo_b64}" alt="Logo"/>
    <div>
        <div style="font-family:'Inter',sans-serif; font-size:1.7rem; font-weight:700; letter-spacing:-0.03em;
                    background:linear-gradient(90deg,#e2e8f0,#c4b5fd,#67e8f9,#c4b5fd,#e2e8f0);
                    background-size:200% auto; -webkit-background-clip:text; background-clip:text;
                    -webkit-text-fill-color:transparent; animation:textShimmer 4s linear infinite;">
            Pan-Epistemic Galaxy
        </div>
        <div style="font-size:0.72rem; color:#64748b; font-family:'JetBrains Mono',monospace; letter-spacing:0.05em; margin-top:2px;">
            100+ NODE OMNI-DISCIPLINARY SWARM
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# --- Initialize Session State ---
if "messages" not in st.session_state:
    st.session_state.messages = []
if "telemetry" not in st.session_state:
    st.session_state.telemetry = []
if "active_agent" not in st.session_state:
    st.session_state.active_agent = "User"
if "student_profile" not in st.session_state:
    st.session_state.student_profile = {"mastered": [], "struggling": [], "misconceptions": []}

# --- Layout ---
col_chat, col_graph, col_profile = st.columns([2.5, 3.5, 1.5])

# ═══════════════════════════════════
#  COL 1 — CHAT
# ═══════════════════════════════════
with col_chat:
    st.markdown("""<div class="section-header">
        <div class="icon" style="background:#1e1b4b;">💬</div>
        <div><div class="title">Chat</div><div class="subtitle">Omni-disciplinary Socratic dialogue</div></div>
    </div>""", unsafe_allow_html=True)
    
    chat_container = st.container(height=580)
    with chat_container:
        for msg in st.session_state.messages:
            avatar = "👤" if msg["role"] == "user" else "🧠"
            with st.chat_message(msg["role"], avatar=avatar):
                st.markdown(msg["content"])
            
    if prompt := st.chat_input("Ask anything across all human knowledge..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with chat_container.chat_message("user", avatar="👤"):
            st.markdown(prompt)
            
        async def process_turn():
            st.session_state.telemetry.clear()
            async for event in run_complex_swarm(prompt, api_key=os.environ.get("AZURE_OPENAI_API_KEY")):
                if event["type"] == "agent_active":
                    st.session_state.active_agent = event["agent"]
                elif event["type"] in ["thought", "log"]:
                    st.session_state.telemetry.append(event)
                elif event["type"] == "profile_update":
                    content = event["content"]
                    if "mastered" in content: st.session_state.student_profile["mastered"] = content["mastered"]
                    if "struggling" in content: st.session_state.student_profile["struggling"] = content["struggling"]
                    if "misconceptions" in content: st.session_state.student_profile["misconceptions"] = content["misconceptions"]
                elif event["type"] == "message":
                    st.session_state.messages.append({"role": "assistant", "content": event["content"]})
                    st.session_state.active_agent = "User"
            st.rerun()

        try:
            loop = asyncio.get_running_loop()
        except RuntimeError:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
        loop.run_until_complete(process_turn())

# ═══════════════════════════════════
#  COL 2 — GRAPH + TELEMETRY
# ═══════════════════════════════════
with col_graph:
    st.markdown("""<div class="section-header">
        <div class="icon" style="background:#172554;">🔭</div>
        <div><div class="title">Swarm Topology</div><div class="subtitle">100+ node real-time agent network</div></div>
    </div>""", unsafe_allow_html=True)
    
    nodes = []
    edges = []
    
    core_nodes = {
        "User": "#64748b",
        "OmniscientOrchestrator": "#8b5cf6",
        "PedagogicalEngine": "#f59e0b",
        "EpistemicCritic": "#ef4444",
        "GlobalCognitiveModeler": "#10b981"
    }
    for c, base_color in core_nodes.items():
        is_active = (st.session_state.active_agent == c)
        nodes.append(Node(id=c, label=c, size=30 if is_active else 18, 
                          color="#ffffff" if is_active else base_color,
                          font={"color": "#e2e8f0", "size": 12}))
    
    edges.append(Edge(source="User", target="OmniscientOrchestrator", color="#2a2a45"))
    edges.append(Edge(source="PedagogicalEngine", target="EpistemicCritic", color="#2a2a45"))
    edges.append(Edge(source="EpistemicCritic", target="PedagogicalEngine", color="#2a2a45"))
    edges.append(Edge(source="User", target="GlobalCognitiveModeler", color="#2a2a45"))

    domain_colors = ["#6366f1", "#8b5cf6", "#06b6d4", "#ec4899", "#f59e0b", 
                     "#10b981", "#f43f5e", "#3b82f6", "#a855f7", "#14b8a6", "#e879f9", "#22d3ee"]
    
    for idx, (domain, smes) in enumerate(DOMAINS.items()):
        dc = domain_colors[idx % len(domain_colors)]
        d_active = (st.session_state.active_agent == domain)
        nodes.append(Node(id=domain, label=domain, size=22 if d_active else 10, 
                          color="#ffffff" if d_active else dc,
                          font={"color": "#e2e8f0", "size": 11}))
        edges.append(Edge(source="OmniscientOrchestrator", target=domain, color="#1e1e30"))
        
        for sme in smes:
            s_active = (st.session_state.active_agent == sme)
            nodes.append(Node(id=sme, label=sme.replace("SME", ""), size=18 if s_active else 4, 
                              color="#ffffff" if s_active else "#475569",
                              font={"color": "#cbd5e1", "size": 10}))
            edges.append(Edge(source=domain, target=sme, color="#1a1a2e"))
            edges.append(Edge(source=sme, target="PedagogicalEngine", color="#0f0f17"))

    config = Config(width=780, height=400, directed=True, nodeHighlightBehavior=True, 
                    physics=True, hierarchical=False, minZoom=0.2, maxZoom=3)
    agraph(nodes=nodes, edges=edges, config=config)

    # Telemetry
    st.markdown("""<div class="section-header" style="margin-top:0.5rem;">
        <div class="icon" style="background:#1a1a2e;">⚡</div>
        <div><div class="title">Telemetry</div><div class="subtitle">Live agent reasoning stream</div></div>
    </div>""", unsafe_allow_html=True)
    
    tel_html = '<div class="tel-wrap">'
    if not st.session_state.telemetry:
        tel_html += '<div class="tel-line" style="color:#334155;">Waiting for query...</div>'
    for item in st.session_state.telemetry[::-1]:
        if item["type"] == "thought":
            tel_html += f'<div class="tel-line"><span class="agent">{item["agent"]}</span> → <span class="thought">{item["content"]}</span></div>'
        else:
            tel_html += f'<div class="tel-line"><span class="agent">{item["agent"]}</span> — {item["content"]}</div>'
    tel_html += '</div>'
    st.markdown(tel_html, unsafe_allow_html=True)

# ═══════════════════════════════════
#  COL 3 — COGNITIVE PROFILE
# ═══════════════════════════════════
with col_profile:
    st.markdown("""<div class="section-header">
        <div class="icon" style="background:#14332b;">🧠</div>
        <div><div class="title">Mastery</div><div class="subtitle">Cognitive model</div></div>
    </div>""", unsafe_allow_html=True)
    
    # Mastered
    st.markdown('<div class="cat-label">✓ Mastered</div>', unsafe_allow_html=True)
    if not st.session_state.student_profile["mastered"]:
        st.markdown('<div class="empty-hint">Awaiting data...</div>', unsafe_allow_html=True)
    for t in st.session_state.student_profile["mastered"]:
        st.markdown(f'<span class="badge badge-g">{t}</span>', unsafe_allow_html=True)
        
    # Struggling
    st.markdown('<div class="cat-label">⚠ Struggling</div>', unsafe_allow_html=True)
    if not st.session_state.student_profile["struggling"]:
        st.markdown('<div class="empty-hint">Clear</div>', unsafe_allow_html=True)
    for t in st.session_state.student_profile["struggling"]:
        st.markdown(f'<span class="badge badge-y">{t}</span>', unsafe_allow_html=True)
        
    # Misconceptions
    st.markdown('<div class="cat-label">✕ Misconceptions</div>', unsafe_allow_html=True)
    if not st.session_state.student_profile["misconceptions"]:
        st.markdown('<div class="empty-hint">None flagged</div>', unsafe_allow_html=True)
    for t in st.session_state.student_profile["misconceptions"]:
        st.markdown(f'<span class="badge badge-r">{t}</span>', unsafe_allow_html=True)

# ═══════════════════════════════════
#  BOTTOM STATUS BAR
# ═══════════════════════════════════
active = st.session_state.active_agent
node_count = sum(len(v) for v in DOMAINS.values()) + len(DOMAINS) + 5
tel_count = len(st.session_state.telemetry)

st.markdown(f"""
<div class="status-bar">
    <div class="status-item"><span class="live-dot"></span> LIVE</div>
    <div class="status-item">Active: <strong style="color:#c4b5fd;">{active}</strong></div>
    <div class="status-item">Nodes: <strong style="color:#94a3b8;">{node_count}</strong></div>
    <div class="status-item">Events: <strong style="color:#94a3b8;">{tel_count}</strong></div>
    <div class="status-item" style="margin-left:auto;">Pan-Epistemic Swarm v4.0</div>
</div>
""", unsafe_allow_html=True)
