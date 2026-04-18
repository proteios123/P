"""
================================================================
PROTEIOS EDUCATION — FLASK BACKEND  (app.py)
Build Spec v1.3
================================================================
"""

from flask import Flask, render_template, jsonify, request
from datetime import datetime

# SAFE IMPORT FOR VERCEL (prevents crash if bundling fails)
try:
    import requests as req_lib
except Exception:
    req_lib = None


app = Flask(__name__, template_folder="templates", static_folder="static")
app.secret_key = "proteios-edu-v1.3"

# ── FORMSPREE CONFIG ──────────────────────────────────────────
FORMSPREE_URL = "https://formspree.io/f/mjgjwwlr"

# ── SITE DATA ─────────────────────────────────────────────────
SITE = {
    "name": "Proteios Education",
    "tagline": "Together, We Turn Ambition Into Action",
    "year": datetime.now().year,

    "logo": "https://raw.githubusercontent.com/proteios123/Proteios/5f1c60295b9d84ee135cbce338d6a0cb037c8d8f/IMG-20260417-WA0104.jpg",
    "video": "https://raw.githubusercontent.com/proteios123/Proteios/5f1c60295b9d84ee135cbce338d6a0cb037c8d8f/8196816-hd_1920_1080_25fps.mp4",

    "maps_url": "https://maps.app.goo.gl/xCXdo4xhjCA3ytqk6?g_st=aw",

    "stats": [
        {"value": 24, "suffix": "+", "label": "Years of Experience", "data_count": "24"},
        {"value": 3, "suffix": "", "label": "Continents", "data_count": "3"},
        {"value": "∞", "suffix": "", "label": "Endless Possibilities", "data_count": None},
    ],
}

# ── MAIN ROUTES ───────────────────────────────────────────────
@app.route("/")
def index():
    return render_template("index.html", site=SITE, page="home")

@app.route("/six-pathways")
def six_pathways():
    return render_template("form_page.html", site=SITE, page="six-pathways")

@app.route("/internships")
def internships():
    return render_template("form_page.html", site=SITE, page="internships")

@app.route("/programs-events")
def programs_events():
    return render_template("form_page.html", site=SITE, page="programs-events")

@app.route("/contact")
def contact():
    return render_template("form_page.html", site=SITE, page="contact")

# ── API: STATS ────────────────────────────────────────────────
@app.route("/api/stats")
def api_stats():
    return jsonify({
        "stats": SITE["stats"],
    })

# ── API: CONTACT (VERCEL SAFE) ────────────────────────────────
@app.route("/api/contact", methods=["POST"])
def api_contact():
    data = request.get_json(silent=True) or {}

    required = ["name", "parentage", "school", "student_class"]
    for field in required:
        if not data.get(field, "").strip():
            return jsonify({"ok": False, "error": f"'{field}' is required."}), 400

    payload = {
        "name": data.get("name"),
        "parentage": data.get("parentage"),
        "school": data.get("school"),
        "class": data.get("student_class"),
        "message": data.get("message", ""),
        "_subject": f"New enquiry from {data.get('name')}",
    }

    try:
        if req_lib is None:
            return jsonify({"ok": False, "error": "Server dependency missing (requests)."}), 500

        resp = req_lib.post(
            FORMSPREE_URL,
            json=payload,
            headers={"Accept": "application/json"},
            timeout=8
        )

        if resp.status_code == 200:
            return jsonify({"ok": True, "message": "Thank you. Our team will reach out soon."})

        return jsonify({"ok": False, "error": "Something went wrong. Try again."}), 502

    except Exception as e:
        return jsonify({"ok": False, "error": str(e)}), 500


# ── ERROR HANDLER ─────────────────────────────────────────────
@app.errorhandler(404)
def not_found(e):
    return render_template("index.html", site=SITE, page="404"), 404


# ── VERCEL ENTRY POINT ────────────────────────────────────────
app = app