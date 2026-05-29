from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

def analyze_resume(resume_text):
    strengths = """• Clear and concise format
- Good educational background mentioned
- Relevant technical skills listed
- Projects section is present"""

    weaknesses = """• Work experience section needs more detail
- Quantifiable achievements missing
- No GitHub profile or project links mentioned
- Objective/summary section is weak"""

    missing_skills = """• Version control (Git/GitHub) not mentioned
- No mention of DSA practice
- Cloud basics (AWS/Azure) not listed
- No soft skills mentioned (teamwork, communication)"""

    improvements = """• Add 2-3 live project links with descriptions
- Mention internships or college projects in detail
- Add a strong summary at the top (2-3 lines)
- Keep resume to 1 page only
- Use action verbs — Built, Developed, Designed"""

    return strengths, weaknesses, missing_skills, improvements

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/analyze", methods=["POST"])
def analyze():
    resume_text = request.form["resume"]
    strengths, weaknesses, missing_skills, improvements = analyze_resume(resume_text)
    return render_template("result.html",
        strengths=strengths,
        weaknesses=weaknesses,
        missing_skills=missing_skills,
        improvements=improvements,
        resume_text=resume_text
    )

@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    user_message = data.get("message", "")
    msg = user_message.lower()

    if any(w in msg for w in ["skill", "learn", "technology"]):
        reply = "Based on your resume, I'd suggest focusing on:\n\n• Git & GitHub — essential for any IT role\n• Python basics — great for automation and AI\n• SQL — almost every company needs this\n• One framework — Flask (Python) or Spring Boot (Java)\n\nStart with Git first — takes only 2 days to learn basics!"
    elif any(w in msg for w in ["intern", "ready", "job"]):
        reply = "You're on the right track! To be internship-ready:\n\n• Have at least 2 complete projects on GitHub\n• Be comfortable explaining your code\n• Know OOPs concepts in Java\n• Practice 20-30 LeetCode Easy problems\n\nYou're closer than you think! 💪"
    elif any(w in msg for w in ["project", "improve", "better"]):
        reply = "To make your projects stand out:\n\n• Add a live demo link (deploy on Vercel/Railway)\n• Write a clear README\n• Mention the tech stack used\n• Add screenshots in the README\n\nThis ResumeAI project is already impressive! 🚀"
    elif any(w in msg for w in ["30 days", "month", "plan"]):
        reply = "Your 30-day power plan:\n\nWeek 1 — DSA basics (arrays, strings)\nWeek 2 — Complete 1 solid project\nWeek 3 — SQL + DBMS concepts\nWeek 4 — Mock interviews + GitHub cleanup\n\nConsistency > intensity!"
    elif any(w in msg for w in ["resume", "cv", "format"]):
        reply = "Resume quick wins:\n\n• Keep it to 1 page\n• Start bullet points with action verbs\n• Add numbers where possible\n• Put your GitHub link at the top\n• Skills section should match the job description"
    else:
        reply = "Great question! My top advice:\n\n• Focus on building real, deployed projects\n• Practice explaining your work out loud\n• Keep learning consistently — even 1 hour daily makes a huge difference\n\nFeel free to ask me anything! 😊"

    return jsonify({"reply": reply})

@app.route("/builder")
def builder():
    return render_template("resume_builder.html")

@app.route("/build-resume", methods=["POST"])
def build_resume():
    name = request.form.get("name", "")
    role = request.form.get("role", "")
    email = request.form.get("email", "")
    phone = request.form.get("phone", "")
    linkedin = request.form.get("linkedin", "")
    location = request.form.get("location", "")
    summary = request.form.get("summary", "")

    degrees = request.form.getlist("edu_degree")
    colleges = request.form.getlist("edu_college")
    years = request.form.getlist("edu_year")
    cgpas = request.form.getlist("edu_cgpa")
    education = [{"degree": d, "college": c, "year": y, "cgpa": g}
                 for d, c, y, g in zip(degrees, colleges, years, cgpas) if d or c]

    skills_raw = request.form.get("skills", "")
    skills = [s.strip() for s in skills_raw.split(",") if s.strip()]
    soft_raw = request.form.get("soft_skills", "")
    soft_skills = [s.strip() for s in soft_raw.split(",") if s.strip()]

    proj_names = request.form.getlist("proj_name")
    proj_techs = request.form.getlist("proj_tech")
    proj_descs = request.form.getlist("proj_desc")
    projects = [{"name": n, "tech": t, "desc": d}
                for n, t, d in zip(proj_names, proj_techs, proj_descs) if n or d]

    exp_roles = request.form.getlist("exp_role")
    exp_companies = request.form.getlist("exp_company")
    exp_durations = request.form.getlist("exp_duration")
    exp_descs = request.form.getlist("exp_desc")
    experience = [{"role": r, "company": c, "duration": du, "desc": de}
                  for r, c, du, de in zip(exp_roles, exp_companies, exp_durations, exp_descs) if r or c]

    return render_template("resume_output.html",
        name=name, role=role, email=email, phone=phone,
        linkedin=linkedin, location=location, summary=summary,
        education=education, skills=skills, soft_skills=soft_skills,
        projects=projects, experience=experience
    )

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
