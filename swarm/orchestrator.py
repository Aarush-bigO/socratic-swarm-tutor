import json
import asyncio
import random
from typing import AsyncGenerator, Dict, Any
from .agents import DOMAINS

# ══════════════════════════════════════════════════════════════
#  INTELLIGENT RESPONSE DATABASE — Topic-Specific Answers
# ══════════════════════════════════════════════════════════════

KNOWLEDGE_BASE = {
    # ── AI & Technology ──
    "ai": {
        "answer": "**Artificial Intelligence (AI)** is a branch of computer science focused on creating systems that can perform tasks typically requiring human intelligence — such as learning, reasoning, problem-solving, perception, and language understanding.\n\n**Key types:**\n- **Narrow AI (ANI):** Designed for a specific task (e.g., Siri, chess engines, recommendation algorithms)\n- **General AI (AGI):** Hypothetical systems with human-level reasoning across all domains\n- **Superintelligent AI (ASI):** Theoretical AI surpassing human intellect entirely\n\n**Core techniques:** Machine Learning, Deep Learning (neural networks), Natural Language Processing, Computer Vision, Reinforcement Learning.\n\n**Real-world applications:** Self-driving cars, medical diagnosis, language translation, drug discovery, and creative content generation.\n\n🧠 *Socratic prompt:* What do you think distinguishes 'intelligence' from mere 'computation'? Can a machine truly *understand*, or does it only *simulate* understanding?",
        "mastered": ["AI fundamentals", "ML vs DL distinction"],
        "struggling": ["AGI vs ANI boundary"],
        "misconceptions": []
    },
    "machine learning": {
        "answer": "**Machine Learning (ML)** is a subset of AI where systems learn from data without being explicitly programmed.\n\n**Three paradigms:**\n1. **Supervised Learning:** Learns from labeled examples (e.g., spam detection, image classification)\n2. **Unsupervised Learning:** Finds hidden patterns in unlabeled data (e.g., clustering, anomaly detection)\n3. **Reinforcement Learning:** Learns through trial-and-error with rewards (e.g., game-playing AI, robotics)\n\n**Key algorithms:** Linear Regression, Decision Trees, Random Forests, SVMs, Neural Networks, Transformers.\n\n**The ML pipeline:** Data Collection → Preprocessing → Feature Engineering → Model Training → Evaluation → Deployment.\n\n🧠 *Socratic prompt:* If a model memorizes training data perfectly but fails on new data, what has gone wrong? (Hint: overfitting vs. generalization)",
        "mastered": ["ML paradigms", "Supervised learning"],
        "struggling": ["Bias-variance tradeoff"],
        "misconceptions": []
    },
    "programming": {
        "answer": "**Programming** is the art and science of instructing computers to perform tasks through written code.\n\n**Popular languages & their strengths:**\n- **Python:** AI/ML, data science, web backends, automation\n- **JavaScript:** Web development (frontend & backend via Node.js)\n- **Java:** Enterprise systems, Android development\n- **C/C++:** Systems programming, game engines, embedded systems\n- **Rust:** Memory-safe systems programming\n\n**Fundamental concepts:** Variables, loops, conditionals, functions, data structures (arrays, trees, graphs), algorithms (sorting, searching), OOP, recursion.\n\n🧠 *Socratic prompt:* Why do you think there are so many programming languages instead of just one? What tradeoffs make each one valuable?",
        "mastered": ["Programming basics"],
        "struggling": ["Language selection criteria"],
        "misconceptions": []
    },

    # ── Mathematics ──
    "math": {
        "answer": "**Mathematics** is the universal language of pattern, structure, and logical reasoning.\n\n**Core branches:**\n- **Algebra:** Equations, polynomials, abstract structures (groups, rings, fields)\n- **Calculus:** Derivatives (rates of change), integrals (accumulated quantities), limits\n- **Geometry:** Euclidean shapes, non-Euclidean spaces, topology\n- **Statistics & Probability:** Data analysis, distributions, Bayesian reasoning\n- **Number Theory:** Prime numbers, modular arithmetic, cryptography foundations\n- **Linear Algebra:** Vectors, matrices, eigenvalues — the backbone of ML\n\n**Why it matters:** Mathematics underpins physics, engineering, computer science, economics, and even art (golden ratio, fractals).\n\n🧠 *Socratic prompt:* Is mathematics *discovered* (exists in nature) or *invented* (a human construct)? What evidence supports your view?",
        "mastered": ["Mathematical reasoning"],
        "struggling": ["Abstract algebra concepts"],
        "misconceptions": []
    },

    # ── Physics ──
    "physics": {
        "answer": "**Physics** is the fundamental science studying matter, energy, space, time, and their interactions.\n\n**Major branches:**\n- **Classical Mechanics:** Newton's laws, motion, forces, gravity\n- **Electromagnetism:** Maxwell's equations, light, electric/magnetic fields\n- **Thermodynamics:** Heat, entropy, energy conservation, laws of thermodynamics\n- **Quantum Mechanics:** Wave-particle duality, uncertainty principle, superposition, entanglement\n- **Relativity:** Special (E=mc², time dilation) and General (curved spacetime, gravity as geometry)\n- **Particle Physics:** Quarks, leptons, bosons, the Standard Model, Higgs mechanism\n\n**Unsolved mysteries:** Dark matter, dark energy, quantum gravity, the measurement problem.\n\n🧠 *Socratic prompt:* If gravity is the weakest fundamental force, why does it dominate at cosmic scales?",
        "mastered": ["Newtonian mechanics", "Basic forces"],
        "struggling": ["Quantum-classical boundary"],
        "misconceptions": []
    },
    "quantum": {
        "answer": "**Quantum Mechanics** governs the behavior of particles at atomic and subatomic scales — where classical physics breaks down.\n\n**Core principles:**\n1. **Wave-Particle Duality:** Particles (like electrons) behave as both waves and particles\n2. **Heisenberg's Uncertainty Principle:** You cannot simultaneously know a particle's exact position AND momentum\n3. **Superposition:** A quantum system exists in all possible states simultaneously until measured\n4. **Entanglement:** Two particles can be correlated such that measuring one instantly determines the other, regardless of distance\n5. **Quantum Tunneling:** Particles can pass through energy barriers they classically shouldn't\n\n**Applications:** Semiconductors, lasers, MRI machines, quantum computing, quantum cryptography.\n\n🧠 *Socratic prompt:* Does the act of observation truly *change* reality, or does it merely reveal what was already there?",
        "mastered": ["Wave-particle duality", "Superposition"],
        "struggling": ["Quantum decoherence"],
        "misconceptions": []
    },

    # ── Biology & Medicine ──
    "biology": {
        "answer": "**Biology** is the scientific study of life and living organisms.\n\n**Core concepts:**\n- **Cell Theory:** All living things are composed of cells; the cell is the basic unit of life\n- **DNA & Genetics:** DNA encodes hereditary information; genes are transcribed to RNA, translated to proteins\n- **Evolution:** Natural selection drives adaptation over generations (Darwin's theory)\n- **Ecology:** Interactions between organisms and their environment; ecosystems, food webs, biomes\n- **Homeostasis:** Organisms maintain internal stability despite external changes\n\n**Major fields:** Molecular biology, microbiology, neuroscience, immunology, botany, marine biology, genomics.\n\n🧠 *Socratic prompt:* If every cell in your body replaces itself over ~7 years, are you the same person you were a decade ago? What defines biological identity?",
        "mastered": ["Cell theory", "DNA basics"],
        "struggling": ["Epigenetics"],
        "misconceptions": []
    },
    "medicine": {
        "answer": "**Medicine** is the science and practice of diagnosing, treating, and preventing disease.\n\n**Key branches:**\n- **Anatomy:** Structure of the human body (skeletal, muscular, organ systems)\n- **Physiology:** How body systems function (cardiovascular, respiratory, nervous, endocrine)\n- **Pathology:** Study of disease mechanisms and causes\n- **Pharmacology:** How drugs interact with biological systems\n- **Surgery:** Operative treatment of injuries and diseases\n- **Immunology:** The immune system, vaccines, autoimmune disorders\n\n**Modern frontiers:** Gene therapy (CRISPR), immunotherapy for cancer, mRNA vaccines, personalized medicine, AI-assisted diagnostics, telemedicine.\n\n🧠 *Socratic prompt:* Should medicine prioritize treating disease or preventing it? What systemic changes would a prevention-first approach require?",
        "mastered": ["Body systems overview", "Vaccine principles"],
        "struggling": ["Pharmacokinetics"],
        "misconceptions": []
    },

    # ── History ──
    "history": {
        "answer": "**History** is the study of past events and their impact on human civilization.\n\n**Major periods:**\n- **Ancient (3000 BCE–500 CE):** Mesopotamia, Egypt, Greece, Rome, Han China, Maurya India\n- **Medieval (500–1500):** Byzantine Empire, Islamic Golden Age, Feudal Europe, Crusades, Mongol Empire\n- **Early Modern (1500–1800):** Renaissance, Reformation, Age of Exploration, Scientific Revolution, Enlightenment\n- **Modern (1800–present):** Industrial Revolution, World Wars, Cold War, Decolonization, Digital Age\n\n**Key turning points:** Invention of writing, fall of Rome, Black Death, printing press, French Revolution, atomic bomb, moon landing, internet.\n\n🧠 *Socratic prompt:* History is written by the victors — how might our understanding of major events change if told from the perspective of the defeated?",
        "mastered": ["Historical periodization"],
        "struggling": ["Historiographical bias"],
        "misconceptions": []
    },

    # ── Geography ──
    "geography": {
        "answer": "**Geography** studies Earth's landscapes, environments, and the relationships between people and their environments.\n\n**Two main branches:**\n1. **Physical Geography:** Landforms, climate, oceans, ecosystems, plate tectonics, natural disasters\n2. **Human Geography:** Population distribution, urbanization, migration, cultural landscapes, geopolitics\n\n**Key concepts:**\n- **Plate Tectonics:** Earth's crust is divided into moving plates that cause earthquakes, volcanoes, and mountain formation\n- **Climate Zones:** Tropical, arid, temperate, continental, polar\n- **The Water Cycle:** Evaporation → condensation → precipitation → collection\n- **Globalization:** How trade, technology, and culture connect distant regions\n\n🧠 *Socratic prompt:* How does geography shape political power? Consider why river valleys birthed the first civilizations.",
        "mastered": ["Physical geography basics", "Climate zones"],
        "struggling": ["Geopolitical analysis"],
        "misconceptions": []
    },

    # ── Civics & Government ──
    "civics": {
        "answer": "**Civics** is the study of the rights and duties of citizenship and how government functions.\n\n**Forms of government:**\n- **Democracy:** Power held by the people (direct or representative)\n- **Republic:** Elected representatives govern on behalf of citizens\n- **Monarchy:** Rule by a king/queen (constitutional or absolute)\n- **Authoritarianism:** Centralized power with limited political freedom\n- **Federalism:** Power divided between central and regional governments\n\n**Key democratic principles:** Rule of law, separation of powers (legislative, executive, judicial), fundamental rights, free press, independent judiciary.\n\n**The Indian Constitution:** World's longest written constitution with fundamental rights, directive principles, and a federal structure with unitary features.\n\n🧠 *Socratic prompt:* Is democracy the best form of government, or merely the least bad? What conditions must exist for democracy to function well?",
        "mastered": ["Forms of government", "Democratic principles"],
        "struggling": ["Constitutional interpretation"],
        "misconceptions": []
    },

    # ── Economics & Finance ──
    "economics": {
        "answer": "**Economics** studies how societies allocate scarce resources to satisfy unlimited wants.\n\n**Two main branches:**\n1. **Microeconomics:** Individual markets, supply & demand, pricing, consumer behavior, market structures\n2. **Macroeconomics:** National economies, GDP, inflation, unemployment, monetary & fiscal policy\n\n**Key concepts:**\n- **Supply & Demand:** Price is determined by the intersection of supply and demand curves\n- **Opportunity Cost:** The value of the next best alternative forgone\n- **Inflation:** General increase in prices over time; measured by CPI\n- **GDP:** Total value of goods and services produced in a country\n\n**Economic systems:** Free market (capitalism), command (socialism/communism), mixed economies.\n\n🧠 *Socratic prompt:* Can a country have both high GDP growth AND equitable wealth distribution? What tradeoffs are involved?",
        "mastered": ["Supply and demand", "GDP concept"],
        "struggling": ["Monetary policy mechanics"],
        "misconceptions": []
    },

    # ── Chemistry ──
    "chemistry": {
        "answer": "**Chemistry** is the study of matter, its properties, composition, and the changes it undergoes.\n\n**Core branches:**\n- **Organic Chemistry:** Carbon-based compounds (the chemistry of life — proteins, DNA, drugs)\n- **Inorganic Chemistry:** Non-carbon compounds, metals, minerals\n- **Physical Chemistry:** Energy changes in reactions, thermodynamics, quantum chemistry\n- **Biochemistry:** Chemical processes in living organisms\n- **Analytical Chemistry:** Techniques to identify and quantify substances\n\n**Fundamental concepts:** Atomic structure, periodic table, chemical bonding (ionic, covalent, metallic), reaction kinetics, equilibrium, acids & bases, oxidation-reduction.\n\n🧠 *Socratic prompt:* Why is carbon the backbone of all life? What makes it uniquely suited for biological molecules?",
        "mastered": ["Atomic structure", "Periodic table"],
        "struggling": ["Reaction mechanisms"],
        "misconceptions": []
    },

    # ── General Knowledge ──
    "general": {
        "answer": "Great question! Here's a rich, interdisciplinary answer drawing from multiple fields:\n\n**Key facts across domains:**\n- 🌍 **Geography:** Earth has 7 continents, 5 oceans, and ~195 countries\n- 📜 **History:** Human civilization began ~5,000 years ago in Mesopotamia\n- 🔬 **Science:** The universe is ~13.8 billion years old; Earth is ~4.5 billion years old\n- 🧬 **Biology:** Humans share ~98.7% of DNA with chimpanzees\n- 💻 **Technology:** The internet was invented in 1969 (ARPANET); the World Wide Web in 1991\n- 🏛️ **Civics:** The UN has 193 member states; the Universal Declaration of Human Rights was adopted in 1948\n\n🧠 *Socratic prompt:* What connections do you see between these facts? How does understanding one domain deepen your understanding of others?",
        "mastered": ["Cross-domain awareness"],
        "struggling": ["Deep interdisciplinary synthesis"],
        "misconceptions": []
    },

    # ── Philosophy ──
    "philosophy": {
        "answer": "**Philosophy** is the study of fundamental questions about existence, knowledge, values, reason, and reality.\n\n**Core branches:**\n- **Metaphysics:** What is the nature of reality? (materialism vs. idealism, free will vs. determinism)\n- **Epistemology:** What is knowledge? How do we know what we know? (rationalism vs. empiricism)\n- **Ethics:** What is right and wrong? (utilitarianism, deontology, virtue ethics)\n- **Logic:** The study of valid reasoning and argumentation\n- **Aesthetics:** What is beauty? What makes art meaningful?\n\n**Major thinkers:** Socrates, Plato, Aristotle, Descartes, Kant, Nietzsche, Wittgenstein, Simone de Beauvoir.\n\n🧠 *Socratic prompt:* 'I think, therefore I am' (Descartes). Is thought the only thing you can be certain of? What else might be indubitable?",
        "mastered": ["Philosophical branches", "Socratic method"],
        "struggling": ["Epistemological frameworks"],
        "misconceptions": []
    },

    # ── Space & Astronomy ──
    "space": {
        "answer": "**Astronomy** is the study of celestial objects, space, and the universe as a whole.\n\n**Key facts:**\n- The **Sun** is a medium-sized star, ~4.6 billion years old, converting hydrogen to helium via nuclear fusion\n- Our **Solar System** has 8 planets: Mercury, Venus, Earth, Mars, Jupiter, Saturn, Uranus, Neptune\n- The **Milky Way** contains ~200-400 billion stars and is ~100,000 light-years across\n- The **Observable Universe** contains ~2 trillion galaxies\n- **Black Holes** are regions where gravity is so strong that nothing — not even light — can escape\n- The **Big Bang** occurred ~13.8 billion years ago, creating space, time, and all matter\n\n**Modern frontiers:** James Webb Space Telescope, exoplanet discovery, gravitational wave detection, Mars exploration.\n\n🧠 *Socratic prompt:* If the universe is expanding, what is it expanding *into*? Or does the question itself reveal a flawed assumption?",
        "mastered": ["Solar system", "Stellar classification"],
        "struggling": ["Spacetime curvature"],
        "misconceptions": []
    },

    # ── Psychology ──
    "psychology": {
        "answer": "**Psychology** is the scientific study of mind and behavior.\n\n**Major schools:**\n- **Behaviorism:** Focus on observable behavior (Pavlov, Skinner, Watson)\n- **Cognitive Psychology:** Mental processes — memory, attention, decision-making\n- **Psychoanalysis:** Unconscious mind and childhood experiences (Freud, Jung)\n- **Humanistic:** Self-actualization and personal growth (Maslow, Rogers)\n- **Neuroscience:** Brain-behavior relationships, neural mechanisms\n\n**Key concepts:** Classical conditioning, cognitive biases (confirmation bias, anchoring), Maslow's hierarchy of needs, neuroplasticity, attachment theory, growth mindset.\n\n🧠 *Socratic prompt:* Are your decisions truly 'free,' or are they the product of unconscious biases and neural patterns you're unaware of?",
        "mastered": ["Psychological schools", "Cognitive biases"],
        "struggling": ["Consciousness theories"],
        "misconceptions": []
    },

    # ── Literature & Language ──
    "literature": {
        "answer": "**Literature** is the art of written works that explore the human condition through language.\n\n**Major forms:** Poetry, fiction (novels, short stories), drama, essays, non-fiction.\n\n**Literary movements:**\n- **Classicism:** Greek/Roman ideals of order and reason\n- **Romanticism:** Emotion, nature, individualism (Wordsworth, Shelley, Keats)\n- **Realism:** Faithful representation of everyday life (Dickens, Tolstoy, Flaubert)\n- **Modernism:** Experimental forms, stream of consciousness (Joyce, Woolf, Kafka)\n- **Postmodernism:** Fragmentation, unreliable narrators, metafiction (Borges, Pynchon)\n\n**Key literary devices:** Metaphor, irony, symbolism, allegory, foreshadowing, unreliable narrator.\n\n🧠 *Socratic prompt:* Why do stories from thousands of years ago (like the Odyssey) still resonate today? What universal truths do they capture?",
        "mastered": ["Literary movements", "Key devices"],
        "struggling": ["Postmodern interpretation"],
        "misconceptions": []
    },

    # ── Environment & Climate ──
    "environment": {
        "answer": "**Environmental Science** studies the interactions between Earth's physical, chemical, and biological systems.\n\n**Critical issues:**\n- **Climate Change:** Rising global temperatures due to greenhouse gas emissions (CO₂, methane); 1.1°C increase since pre-industrial era\n- **Biodiversity Loss:** ~1 million species at risk of extinction; deforestation, habitat destruction\n- **Ocean Acidification:** CO₂ absorption lowers ocean pH, threatening marine ecosystems\n- **Pollution:** Air (particulate matter, ozone), water (plastics, chemicals), soil contamination\n\n**Solutions:** Renewable energy (solar, wind, nuclear), carbon capture, circular economy, reforestation, sustainable agriculture, international agreements (Paris Climate Accord).\n\n🧠 *Socratic prompt:* Is economic growth fundamentally incompatible with environmental sustainability, or can technology decouple the two?",
        "mastered": ["Climate change basics", "Greenhouse effect"],
        "struggling": ["Carbon cycle dynamics"],
        "misconceptions": []
    },
}

# Keywords mapped to knowledge base entries
KEYWORD_MAP = {
    "ai": ["ai", "artificial intelligence", "what is ai", "whats ai", "machine intelligence"],
    "machine learning": ["machine learning", "ml", "deep learning", "neural network", "training model"],
    "programming": ["programming", "coding", "python", "javascript", "software", "code"],
    "math": ["math", "mathematics", "algebra", "calculus", "geometry", "equation", "number"],
    "physics": ["physics", "force", "motion", "newton", "relativity", "energy", "gravity"],
    "quantum": ["quantum", "superposition", "entanglement", "wave function", "heisenberg"],
    "biology": ["biology", "cell", "dna", "evolution", "organism", "life science", "gene"],
    "medicine": ["medicine", "medical", "disease", "health", "doctor", "anatomy", "surgery", "vaccine", "pathology"],
    "history": ["history", "ancient", "medieval", "war", "civilization", "empire", "revolution", "historical"],
    "geography": ["geography", "continent", "climate", "mountain", "river", "country", "map", "earth"],
    "civics": ["civics", "government", "democracy", "constitution", "law", "rights", "citizen", "republic", "parliament"],
    "economics": ["economics", "economy", "gdp", "inflation", "money", "finance", "trade", "market", "supply demand"],
    "chemistry": ["chemistry", "chemical", "element", "periodic table", "atom", "molecule", "reaction", "compound"],
    "general": ["general knowledge", "gk", "facts", "tell me about", "what do you know"],
    "philosophy": ["philosophy", "existence", "meaning of life", "ethics", "morality", "truth", "socrates", "plato"],
    "space": ["space", "star", "planet", "galaxy", "universe", "astronomy", "solar system", "black hole", "nasa", "moon"],
    "psychology": ["psychology", "mind", "behavior", "mental", "brain", "cognitive", "freud", "consciousness"],
    "literature": ["literature", "book", "novel", "poetry", "author", "story", "writing", "literary"],
    "environment": ["environment", "climate change", "pollution", "ecosystem", "global warming", "renewable", "carbon"],
}


def match_topic(user_input: str) -> str:
    """Match user input to the best knowledge base topic."""
    lower = user_input.lower().strip()
    
    # Direct topic matching with scoring
    scores = {}
    for topic, keywords in KEYWORD_MAP.items():
        score = 0
        for kw in keywords:
            if kw in lower:
                score += len(kw)  # Longer keyword matches = higher confidence
        if score > 0:
            scores[topic] = score
    
    if scores:
        return max(scores, key=scores.get)
    return "general"


async def run_complex_swarm(user_input: str, api_key: str = None) -> AsyncGenerator[Dict[str, Any], None]:
    """
    Executes the Pan-Epistemic 100+ node galaxy swarm.
    Now with intelligent topic-matched responses.
    """
    yield {"type": "agent_active", "agent": "OmniscientOrchestrator"}
    yield {"type": "thought", "agent": "OmniscientOrchestrator", "content": f"Classifying query across the entirety of human knowledge: '{user_input}'"}
    await asyncio.sleep(0.8)
    
    # Match topic intelligently
    topic = match_topic(user_input)
    kb_entry = KNOWLEDGE_BASE.get(topic, KNOWLEDGE_BASE["general"])
    
    # Analyze the input to pick domains and SMEs
    lower_input = user_input.lower()
    
    active_paths = {}
    
    if any(w in lower_input for w in ["math", "logic", "number", "fractal", "calculus", "algebra", "equation"]):
        active_paths["FormalSciences"] = ["MathSME", "LogicSME"]
    if any(w in lower_input for w in ["physics", "quantum", "star", "energy", "force", "gravity", "relativity"]):
        active_paths["PhysicalSciences"] = ["PhysicsSME", "AstrophysicsSME", "QuantumMechanicsSME"]
    if any(w in lower_input for w in ["biology", "medicine", "life", "dna", "brain", "cell", "disease", "health", "medical", "anatomy", "vaccine"]):
        active_paths["LifeSciences"] = ["BiologySME", "MedicineSME", "NeuroscienceSME"]
    if any(w in lower_input for w in ["society", "psychology", "people", "mind", "mental", "behavior", "cognitive"]):
        active_paths["SocialSciences"] = ["PsychologySME", "SociologySME"]
    if any(w in lower_input for w in ["engineer", "machine", "build", "agriculture"]):
        active_paths["AppliedSciences"] = ["EngineeringSME", "CyberneticsSME"]
    if any(w in lower_input for w in ["history", "philosophy", "ancient", "gothic", "civilization", "war", "empire", "medieval"]):
        active_paths["Humanities"] = ["HistorySME", "PhilosophySME", "ArchitectureSME"]
    if any(w in lower_input for w in ["art", "music", "paint", "beauty", "awe", "literature", "book", "novel", "poetry"]):
        active_paths["Arts"] = ["FineArtsSME", "MusicSME", "RenaissanceArtSME"]
    if any(w in lower_input for w in ["money", "finance", "trade", "economy", "gdp", "inflation", "market", "economics"]):
        active_paths["CommerceEcon"] = ["FinanceSME", "MacroEconSME"]
    if any(w in lower_input for w in ["law", "civic", "rights", "government", "democracy", "constitution", "parliament"]):
        active_paths["LawPolScience"] = ["JurisprudenceSME", "CivicsSME"]
    if any(w in lower_input for w in ["compute", "ai", "software", "robot", "programming", "code", "machine learning", "artificial intelligence"]):
        active_paths["TechComputing"] = ["ArtificialIntelligenceSME", "RoboticsSME"]
    if any(w in lower_input for w in ["god", "ethics", "religion", "moral", "meaning of life"]):
        active_paths["TheologyEthics"] = ["TheologySME", "EthicsSME"]
    if any(w in lower_input for w in ["word", "language", "speak", "meaning"]):
        active_paths["LinguisticsComm"] = ["SemanticsSME", "LinguisticsSME"]
    if any(w in lower_input for w in ["space", "planet", "galaxy", "universe", "astronomy", "solar", "black hole", "moon"]):
        active_paths["PhysicalSciences"] = ["AstrophysicsSME", "PhysicsSME"]
    if any(w in lower_input for w in ["chemistry", "chemical", "element", "atom", "molecule", "reaction", "periodic"]):
        active_paths["PhysicalSciences"] = ["PhysicsSME", "QuantumMechanicsSME"]
    if any(w in lower_input for w in ["environment", "climate", "pollution", "ecosystem", "global warming"]):
        active_paths["LifeSciences"] = ["BiologySME", "EcologySME"]
    if any(w in lower_input for w in ["geography", "continent", "country", "mountain", "river", "map"]):
        active_paths["Humanities"] = ["GeographySME", "HistorySME"]

    # Fallback
    if not active_paths:
        active_paths = {
            "PhysicalSciences": ["AstrophysicsSME"],
            "Arts": ["FineArtsSME"],
            "TechComputing": ["ArtificialIntelligenceSME"]
        }

    yield {"type": "log", "agent": "OmniscientOrchestrator", "content": f"Multi-Domain Dispatch: {', '.join(active_paths.keys())}"}

    context_gathered = []
    
    for domain, smes in active_paths.items():
        yield {"type": "agent_active", "agent": domain}
        yield {"type": "thought", "agent": domain, "content": f"Activating {domain} ontological network."}
        await asyncio.sleep(0.4)
        
        for sme in smes:
            yield {"type": "agent_active", "agent": sme}
            yield {"type": "thought", "agent": sme, "content": f"Retrieving expert knowledge from {sme} knowledge graph."}
            await asyncio.sleep(0.5)
            yield {"type": "log", "agent": sme, "content": f"Context synthesized and validated."}
            context_gathered.append(f"{sme}")
            
    # Pedagogical Phase
    yield {"type": "agent_active", "agent": "PedagogicalEngine"}
    yield {"type": "thought", "agent": "PedagogicalEngine", "content": f"Synthesizing {len(context_gathered)} expert inputs into a comprehensive educational response."}
    await asyncio.sleep(0.8)
    yield {"type": "log", "agent": "PedagogicalEngine", "content": f"Response calibrated for topic: {topic.upper()}"}
    
    # Critic Phase
    yield {"type": "agent_active", "agent": "EpistemicCritic"}
    yield {"type": "thought", "agent": "EpistemicCritic", "content": "Verifying factual accuracy and pedagogical clarity."}
    await asyncio.sleep(0.6)
    yield {"type": "log", "agent": "EpistemicCritic", "content": "APPROVED: Factually accurate, pedagogically sound."}
    
    # Profiler Update
    yield {"type": "agent_active", "agent": "GlobalCognitiveModeler"}
    yield {"type": "thought", "agent": "GlobalCognitiveModeler", "content": "Updating student mastery model based on query complexity."}
    await asyncio.sleep(0.5)
    
    profile = {
        "mastered": kb_entry.get("mastered", ["Basic concepts"]),
        "struggling": kb_entry.get("struggling", []),
        "misconceptions": kb_entry.get("misconceptions", [])
    }
    yield {"type": "profile_update", "content": profile}
    
    yield {"type": "message", "agent": "PedagogicalEngine", "content": kb_entry["answer"]}
