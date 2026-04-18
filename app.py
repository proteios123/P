"""
================================================================
PROTEIOS EDUCATION — FLASK BACKEND  (app.py)
Build Spec v1.3
================================================================
"""

from flask import Flask, render_template, jsonify, request, redirect
import requests as req_lib
from datetime import datetime

app = Flask(__name__, template_folder="templates", static_folder="static")
app.secret_key = "proteios-edu-v1.3"

# ── FORMSPREE CONFIG ──────────────────────────────────────────
FORMSPREE_URL = "https://formspree.io/f/mjgjwwlr"

# ── SITE DATA ─────────────────────────────────────────────────
SITE = {
    "name":    "Proteios Education",
    "tagline": "Together, We Turn Ambition Into Action",
    "year":    datetime.now().year,

    "logo":  "https://raw.githubusercontent.com/proteios123/Proteios/5f1c60295b9d84ee135cbce338d6a0cb037c8d8f/IMG-20260417-WA0104.jpg",
    "video": "https://raw.githubusercontent.com/proteios123/Proteios/5f1c60295b9d84ee135cbce338d6a0cb037c8d8f/8196816-hd_1920_1080_25fps.mp4",

    "maps_url": "https://maps.app.goo.gl/xCXdo4xhjCA3ytqk6?g_st=aw",

    "stats": [
        {"value": 24,       "suffix": "+", "label": "Years of Experience",  "data_count": "24"},
        {"value": 3,        "suffix": "",  "label": "Continents",           "data_count": "3"},
        {"value": "∞",      "suffix": "",  "label": "Endless Possibilities", "data_count": None},
    ],

    "why_us_bullets": [
        {"icon": "🎯", "title": "Real-world focus",    "desc": "Not just theory — actual skills and outcomes"},
        {"icon": "🧭", "title": "Clarity & direction", "desc": "Helping students understand where they stand and where they're heading"},
        {"icon": "⚡", "title": "Modern approach",     "desc": "Combining education with innovation and real-world relevance"},
        {"icon": "🤝", "title": "Strong community",   "desc": "Building a network of ambitious students and mentors"},
        {"icon": "🚀", "title": "Execution over talk", "desc": "Focusing on action, projects, and opportunities"},
        {"icon": "✨", "title": "Built for this generation", "desc": "Designed for students who want more than traditional systems"},
    ],

    "why_us_callouts": [
        "Not just learning — real-world execution",
        "Not just guidance — clear direction",
        "Not just ideas — actual opportunities",
        "Not just a platform — a growing ecosystem",
    ],

    "services": [
        {"symbol": "∑", "title": "National Competitive Exams",  "desc": "Specialized guidance for NEET, JEE, and other Indian national-level examinations. Strategic preparation and mentorship beyond scores.", "slug": "six-pathways"},
        {"symbol": "∞", "title": "Global University Admissions","desc": "End-to-end support for Ivy League, Oxford, Cambridge, and top universities worldwide.", "slug": "six-pathways"},
        {"symbol": "π", "title": "Standardized Testing",        "desc": "Comprehensive preparation for SAT, ACT, IELTS, and TOEFL.", "slug": "six-pathways"},
        {"symbol": "Δ", "title": "Career Counselling",          "desc": "Deep sessions mapping strengths, aspirations, and goals to the right academic paths.", "slug": "six-pathways"},
        {"symbol": "φ", "title": "Educator & School Programs",  "desc": "CPD programs and hands-on training for educators — improving teaching and learning outcomes.", "slug": "six-pathways"},
        {"symbol": "λ", "title": "Parent & Family Guidance",    "desc": "Helping families make informed decisions about their children's education.", "slug": "six-pathways"},
    ],

    "founders": [
        {
            "name":  "Mir Murtakib",
            "role":  "Founder",
            "photo": "https://raw.githubusercontent.com/proteios123/Proteios/5f1c60295b9d84ee135cbce338d6a0cb037c8d8f/IMG-20260417-WA0106.jpg",
            "quote": "At Proteios, my vision has always been clear — to redefine how students approach education, not just as a pathway to degrees, but as a foundation for life.",
            "bio":   "Through Proteios, the focus has been on building a platform that bridges ambition with opportunity. Working closely with students to understand their strengths, aspirations, and potential — guiding them with tailored strategies from NEET and JEE to SAT, ACT, IELTS, and TOEFL preparation for the global stage.",
        },
        {
            "name":  "Younus Beigh",
            "role":  "Co-Founder",
            "photo": "https://raw.githubusercontent.com/proteios123/Proteios/5f1c60295b9d84ee135cbce338d6a0cb037c8d8f/IMG-20260417-WA0098.jpg",
            "quote": "My vision is to create an ecosystem where students are empowered, educators are supported, and families feel confident about the journey ahead.",
            "bio":   "With over 24 years of experience across India, the UAE, and Saudi Arabia — engaging with schools and education systems — Younus brings a perspective that blends global exposure with a deep understanding of local educational needs, rooted in Kashmir.",
        },
    ],

    "internship_roles": [
        {"title": "Student Counsellor Intern",  "desc": "Support students in mapping their academic journeys with experienced mentors."},
        {"title": "Research & Content Intern",  "desc": "Create resources on global admissions, standardized testing, and career pathways."},
        {"title": "Operations Intern",          "desc": "Drive team success through coordination and organizational excellence."},
    ],

    "events": [
        {"title": "Campus Connect",    "desc": "We visit universities and colleges — bringing guidance directly to campuses."},
        {"title": "Education Summits", "desc": "Conferences across India and internationally with workshops, panels, and networking."},
        {"title": "Office Open Days",  "desc": "Visit our offices — meet the team, hear success stories, explore opportunities."},
    ],

    "regions": [
        {"name": "South Asia",          "cities": ["Kashmir", "Delhi NCR", "Mumbai", "Bangalore"]},
        {"name": "Middle East",         "cities": ["Dubai, UAE", "Abu Dhabi", "Riyadh, Saudi Arabia", "Kuwait City"]},
        {"name": "Global Partnerships", "cities": ["United Kingdom", "United States", "Canada", "Australia"]},
    ],

    "images": [
        "https://raw.githubusercontent.com/proteios123/Proteios/5f1c60295b9d84ee135cbce338d6a0cb037c8d8f/pexels-zen-chung-5538573.jpg",
        "https://raw.githubusercontent.com/proteios123/Proteios/5f1c60295b9d84ee135cbce338d6a0cb037c8d8f/pexels-yaroslav-shuraev-9490514.jpg",
        "https://raw.githubusercontent.com/proteios123/Proteios/5f1c60295b9d84ee135cbce338d6a0cb037c8d8f/pexels-mikhail-nilov-9159059.jpg",
        "https://raw.githubusercontent.com/proteios123/Proteios/5f1c60295b9d84ee135cbce338d6a0cb037c8d8f/pexels-karola-g-7692561.jpg",
        "https://raw.githubusercontent.com/proteios123/Proteios/5f1c60295b9d84ee135cbce338d6a0cb037c8d8f/pexels-ivan-s-5676678.jpg",
        "https://raw.githubusercontent.com/proteios123/Proteios/5f1c60295b9d84ee135cbce338d6a0cb037c8d8f/pexels-george-pak-7972372.jpg",
    ],

    "social": {
        "instagram": "https://www.instagram.com/proteioseducation?igsh=YnBueWQzbXZ5ZTg0",
        "facebook":  "https://www.facebook.com/share/1DJoNKSVj2/",
        "linkedin":  "https://www.linkedin.com/in/proteios-education-3050a43b6",
        "youtube":   "https://youtube.com/@proteioseducation?si=b8gWwBLwu1d2-uVf",
    },

    "nav": [
        {"label": "Who We Are",        "href": "#about"},
        {"label": "What We Do",        "href": "#services"},
        {"label": "Our Team",          "href": "#founders"},
        {"label": "Careers",           "href": "#careers"},
        {"label": "Work Opportunities","href": "/internships"},
    ],
}

# ── PAGE CONTEXT HELPERS ──────────────────────────────────────
FORM_PAGES = {
    "six-pathways":   {"h1": "Six Pathways. One Commitment.", "intro": "Tell us about yourself and we'll connect you with the right pathway."},
    "internships":    {"h1": "Internship Opportunities",       "intro": "Start your journey with Proteios. Fill in the form and we'll be in touch."},
    "programs-events":{"h1": "Programs & Events",             "intro": "Connect with us at events, campuses, conferences, and our offices."},
    "contact":        {"h1": "Contact Us",                    "intro": "Reach out to the Proteios team. We respond within 24–48 hours."},
}

# ── MAIN ROUTES ───────────────────────────────────────────────
@app.route("/")
def index():
    return render_template("index.html", site=SITE, page="home")

@app.route("/six-pathways")
def six_pathways():
    ctx = FORM_PAGES["six-pathways"]
    return render_template("form_page.html", site=SITE, page="six-pathways",
                           h1=ctx["h1"], intro=ctx["intro"])

@app.route("/internships")
def internships():
    ctx = FORM_PAGES["internships"]
    return render_template("form_page.html", site=SITE, page="internships",
                           h1=ctx["h1"], intro=ctx["intro"])

@app.route("/programs-events")
def programs_events():
    ctx = FORM_PAGES["programs-events"]
    return render_template("form_page.html", site=SITE, page="programs-events",
                           h1=ctx["h1"], intro=ctx["intro"])

@app.route("/contact")
def contact():
    ctx = FORM_PAGES["contact"]
    return render_template("form_page.html", site=SITE, page="contact",
                           h1=ctx["h1"], intro=ctx["intro"])

# ── API: STATS ────────────────────────────────────────────────
@app.route("/api/stats")
def api_stats():
    return jsonify({
        "stats":    SITE["stats"],
        "services": [s["title"] for s in SITE["services"]],
        "regions":  [r["name"]  for r in SITE["regions"]],
    })

# ── API: CONTACT (proxy to Formspree) ────────────────────────
@app.route("/api/contact", methods=["POST"])
def api_contact():
    data = request.get_json(silent=True) or {}
    required = ["name", "parentage", "school", "student_class"]
    for field in required:
        if not data.get(field, "").strip():
            return jsonify({"ok": False, "error": f"'{field}' is required."}), 400

    payload = {
        "name":          data.get("name"),
        "parentage":     data.get("parentage"),
        "school":        data.get("school"),
        "class":         data.get("student_class"),
        "message":       data.get("message", ""),
        "_subject":      f"New enquiry from {data.get('name')}",
    }
    try:
        resp = req_lib.post(FORMSPREE_URL, json=payload,
                            headers={"Accept": "application/json"}, timeout=8)
        if resp.status_code == 200:
            return jsonify({"ok": True,  "message": "Thank you. Our team will reach out soon."})
        return jsonify({"ok": False, "error": "Something went wrong. Try again."}), 502
    except Exception as e:
        return jsonify({"ok": False, "error": "Something went wrong. Try again."}), 500

# ── ERROR HANDLERS ────────────────────────────────────────────
@app.errorhandler(404)
def not_found(e):
    return render_template("index.html", site=SITE, page="404"), 404

# ── ENTRY ─────────────────────────────────────────────────────
if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)