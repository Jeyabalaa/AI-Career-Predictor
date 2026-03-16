
from django.contrib import messages
from django.contrib.auth import login as auth_login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import HttpResponse, redirect, render
from django.utils.text import slugify

from .ml_model.predict import predict_career
from .models import StudentSkill


def home(request):
    return render(request, "predictor/home.html")


def career_info():
    # Each career has a slug (used in URLs), a name, roadmap, and external resources.
    return {
        "data-scientist": {
            "name": "Data Scientist",
            "roadmap": [
                "Learn Python for data analysis (pandas, numpy)",
                "Practice SQL and data visualization (matplotlib, seaborn)",
                "Study statistics and machine learning fundamentals",
                "Build a portfolio with real datasets",
            ],
            "description": "Data Scientists analyze data to extract insights and build predictive models.",
            "resources": [
                {"label": "Kaggle Data Science Courses", "url": "https://www.kaggle.com/learn/data-science"},
                {"label": "Coursera Data Science Specialization", "url": "https://www.coursera.org/specializations/jhu-data-science"},
            ],
            "courses": [
                {"label": "Machine Learning (Coursera)", "url": "https://www.coursera.org/learn/machine-learning"},
                {"label": "Data Science A-Z (Udemy)", "url": "https://www.udemy.com/course/datascience/"},
            ],
            "projects": [
                "Build a movie recommendation system",
                "Create a customer churn prediction model",
                "Analyze a real dataset with insights",
            ],
            "internships": [
                "Data Analyst Intern",
                "Machine Learning Intern",
                "AI Research Intern",
            ],
            "difficulty": "Hard",
        },
        "machine-learning-engineer": {
            "name": "Machine Learning Engineer",
            "roadmap": [
                "Master Python and machine learning libraries (scikit-learn, TensorFlow)",
                "Learn model deployment (Flask/Django, Docker)",
                "Study algorithms and model evaluation",
                "Work on end-to-end ML projects",
            ],
            "description": "Machine Learning Engineers build and deploy models that power intelligent applications.",
            "resources": [
                {"label": "TensorFlow Tutorials", "url": "https://www.tensorflow.org/tutorials"},
                {"label": "Fast.ai Practical Deep Learning", "url": "https://www.fast.ai/"},
            ],
            "courses": [
                {"label": "Deep Learning Specialization (Coursera)", "url": "https://www.coursera.org/specializations/deep-learning"},
                {"label": "ML A-Z (Udemy)", "url": "https://www.udemy.com/course/machinelearning/"},
            ],
            "projects": [
                "Build a neural network from scratch",
                "Create an image classification model",
                "Deploy a model with Docker",
            ],
            "internships": [
                "ML Engineering Intern",
                "Data Science Intern",
                "AI Research Intern",
            ],
            "difficulty": "Hard",
        },
        "software-developer": {
            "name": "Software Developer",
            "roadmap": [
                "Learn a modern programming language (Python, JavaScript, Java)",
                "Practice problem solving and algorithms",
                "Build web or mobile applications",
                "Contribute to open-source projects",
            ],
            "description": "Software Developers design, build, and maintain applications used by millions of people.",
            "resources": [
                {"label": "freeCodeCamp", "url": "https://www.freecodecamp.org/"},
                {"label": "CS50 (Harvard)", "url": "https://cs50.harvard.edu/"},
            ],
            "courses": [
                {"label": "Complete Python Bootcamp (Udemy)", "url": "https://www.udemy.com/course/complete-python-bootcamp/"},
                {"label": "The Web Developer Bootcamp (Udemy)", "url": "https://www.udemy.com/course/the-web-developer-bootcamp/"},
            ],
            "projects": [
                "Build a personal website",
                "Create a REST API",
                "Develop a full-stack web app",
            ],
            "internships": [
                "Software Engineering Intern",
                "Backend Developer Intern",
                "Frontend Developer Intern",
            ],
            "difficulty": "Medium",
        },
        "ui-ux-designer": {
            "name": "UI/UX Designer",
            "roadmap": [
                "Study design principles and user research",
                "Learn tools like Figma or Adobe XD",
                "Build wireframes and prototypes",
                "Practice creating accessible interfaces",
            ],
            "description": "UI/UX Designers craft user experiences and interfaces that are both usable and delightful.",
            "resources": [
                {"label": "Figma Learn Design", "url": "https://www.figma.com/learn/"},
                {"label": "NN/g UX Training", "url": "https://www.nngroup.com/"},
            ],
            "courses": [
                {"label": "UI/UX Design Specialization (Coursera)", "url": "https://www.coursera.org/specializations/ui-ux-design"},
                {"label": "The Ultimate UX Design Course (Udemy)", "url": "https://www.udemy.com/course/ux-design/"},
            ],
            "projects": [
                "Design a mobile app interface",
                "Create a usability study and report",
                "Build a design system",
            ],
            "internships": [
                "UI/UX Design Intern",
                "Product Design Intern",
                "UX Research Intern",
            ],
            "difficulty": "Medium",
        },
        "web-developer": {
            "name": "Web Developer",
            "roadmap": [
                "Master HTML, CSS, and JavaScript",
                "Learn a modern frontend framework (React, Vue, or Angular)",
                "Build full-stack projects with a backend",
                "Deploy apps using cloud platforms",
            ],
            "description": "Web Developers build modern websites and web applications that run in browsers.",
            "resources": [
                {"label": "MDN Web Docs", "url": "https://developer.mozilla.org/"},
                {"label": "Frontend Mentor", "url": "https://www.frontendmentor.io/"},
            ],
            "courses": [
                {"label": "The Complete Web Developer Bootcamp (Udemy)", "url": "https://www.udemy.com/course/the-web-developer-bootcamp/"},
                {"label": "Responsive Web Design Certification (freeCodeCamp)", "url": "https://www.freecodecamp.org/learn"},
            ],
            "projects": [
                "Build a personal portfolio website",
                "Create an e-commerce site",
                "Deploy a full-stack app",
            ],
            "internships": [
                "Frontend Developer Intern",
                "Full-Stack Developer Intern",
                "DevOps Intern",
            ],
            "difficulty": "Medium",
        },
        "digital-marketer": {
            "name": "Digital Marketer",
            "roadmap": [
                "Learn about social media and content strategy",
                "Study SEO and analytics tools",
                "Practice running ad campaigns",
                "Build a personal brand or blog",
            ],
            "description": "Digital Marketers promote products and services online using content, ads, and analytics.",
            "resources": [
                {"label": "Google Digital Garage", "url": "https://learndigital.withgoogle.com/digitalgarage"},
                {"label": "HubSpot Academy", "url": "https://academy.hubspot.com/"},
            ],
            "courses": [
                {"label": "Digital Marketing Specialization (Coursera)", "url": "https://www.coursera.org/specializations/digital-marketing"},
                {"label": "The Complete Digital Marketing Course (Udemy)", "url": "https://www.udemy.com/course/learn-digital-marketing-course/"},
            ],
            "projects": [
                "Run a social media campaign",
                "Build a blog and track analytics",
                "Create a small ad campaign and measure results",
            ],
            "internships": [
                "Digital Marketing Intern",
                "Content Marketing Intern",
                "SEO Intern",
            ],
            "difficulty": "Medium",
        },
    }


def get_career_slug(career_name: str) -> str:
    # Normalize career names into URL-friendly slugs.
    return slugify(career_name)


def get_career_details(career_name: str):
    """Return career details given a slug or a display name.

    This helper is resilient to inputs like:
    - "data-scientist" (slug)
    - "Data Scientist" (display name)
    - "data scientist" (lowercase name)

    If the career is not in the supported list, this returns a generic
    fallback object so every career has a resources page.
    """
    if not career_name:
        return None

    careers = career_info()

    # 1) Match exact slug key first
    if career_name in careers:
        return careers[career_name]

    # 2) Match by display name (case-insensitive)
    name_lower = career_name.strip().lower()
    for detail in careers.values():
        if detail.get("name", "").strip().lower() == name_lower:
            return detail

    # 3) Try slugifying the input (handles strings like "Data Scientist")
    slug = get_career_slug(career_name)
    if slug in careers:
        return careers[slug]

    # 4) Fallback: generic career support (supports all careers)
    display_name = career_name.replace("-", " ").title()
    return {
        "name": display_name,
        "roadmap": [
            "Start with the fundamentals of the field.",
            "Build small projects to apply what you learn.",
            "Look for online courses and tutorials specific to this domain.",
            "Join communities, attend workshops, and collaborate with others.",
        ],
        "description": "This is a general career path. Use the steps below to build skills and experience relevant to your chosen field.",
        "resources": [
            {"label": "Coursera", "url": "https://www.coursera.org"},
            {"label": "Udemy", "url": "https://www.udemy.com"},
            {"label": "LinkedIn Learning", "url": "https://www.linkedin.com/learning"},
        ],
        "courses": [
            {"label": "Learning How to Learn (Coursera)", "url": "https://www.coursera.org/learn/learning-how-to-learn"},
            {"label": "Google Career Certificates", "url": "https://grow.google/certificates/"},
        ],
        "projects": [
            "Build a small portfolio project that highlights your skills.",
            "Document your process and outcomes to share with recruiters.",
            "Contribute to open-source or volunteer projects to gain experience.",
        ],
        "internships": [
            "Search for internships related to your field on LinkedIn or Internshala.",
            "Apply to volunteer or part-time roles to gain practical experience.",
        ],
        "difficulty": "Varies",
    }


def career_roadmap(career_name: str):
    details = get_career_details(career_name)
    if not details:
        return []
    return details.get("roadmap", [])


def career_requirements(career_name: str):
    """Return required skill levels for a career."""
    # Skill scale is 1-10.
    requirements = {
        "Data Scientist": {
            "coding": 8,
            "math": 8,
            "creativity": 6,
            "communication": 6,
        },
        "Machine Learning Engineer": {
            "coding": 8,
            "math": 8,
            "creativity": 6,
            "communication": 5,
        },
        "Software Developer": {
            "coding": 8,
            "math": 6,
            "creativity": 6,
            "communication": 6,
        },
        "UI/UX Designer": {
            "coding": 4,
            "math": 5,
            "creativity": 9,
            "communication": 7,
        },
        "Web Developer": {
            "coding": 7,
            "math": 6,
            "creativity": 7,
            "communication": 6,
        },
        "Digital Marketer": {
            "coding": 4,
            "math": 5,
            "creativity": 7,
            "communication": 8,
        },
    }
    return requirements.get(career_name, {})


def skill_gap(student_skills: dict, required_skills: dict):
    """List skill areas where student is below required level."""
    gap = []
    for key, required in required_skills.items():
        student = student_skills.get(key, 0)
        if student < required:
            gap.append(f"{key.capitalize()}: {student} → {required}")
    return gap


def career_demand_info(career_name: str):
    """Return demand and salary info for a career."""
    info = {
        "Data Scientist": {
            "demand": "High",
            "growth": "35%",
            "salary": "₹10–20 LPA",
        },
        "Machine Learning Engineer": {
            "demand": "High",
            "growth": "38%",
            "salary": "₹12–22 LPA",
        },
        "Software Developer": {
            "demand": "High",
            "growth": "30%",
            "salary": "₹8–16 LPA",
        },
        "UI/UX Designer": {
            "demand": "Medium",
            "growth": "20%",
            "salary": "₹6–12 LPA",
        },
        "Web Developer": {
            "demand": "High",
            "growth": "28%",
            "salary": "₹7–14 LPA",
        },
        "Digital Marketer": {
            "demand": "Medium",
            "growth": "22%",
            "salary": "₹5–10 LPA",
        },
    }
    return info.get(career_name, {})


def learning_path_by_year(career_name: str):
    """Provide a year-by-year learning roadmap based on career."""
    plans = {
        "Data Scientist": {
            "Year 1": [
                "Python for data analysis",
                "Intro to statistics",
                "SQL basics",
            ],
            "Year 2": [
                "Machine learning fundamentals",
                "Data visualization (matplotlib, seaborn)",
                "Begin portfolio projects",
            ],
            "Year 3": [
                "Advanced ML / deep learning",
                "Deploy ML models (Flask/Django)",
                "Internship or real-world project",
            ],
        },
        "Machine Learning Engineer": {
            "Year 1": [
                "Python and data structures",
                "Linear algebra and statistics",
                "Algorithms basics",
            ],
            "Year 2": [
                "Machine learning algorithms",
                "Model evaluation and tuning",
                "Introduction to TensorFlow/PyTorch",
            ],
            "Year 3": [
                "Deploying ML systems",
                "Scaling models in production",
                "Real-world ML projects",
            ],
        },
        "Software Developer": {
            "Year 1": [
                "Learn a modern language (Python/JavaScript)",
                "Basic data structures and algorithms",
                "Build small apps",
            ],
            "Year 2": [
                "Web frameworks (Django/React)",
                "Databases and APIs",
                "Contribute to open source",
            ],
            "Year 3": [
                "System design basics",
                "Deploy applications",
                "Work on collaborative projects",
            ],
        },
        "UI/UX Designer": {
            "Year 1": [
                "Design fundamentals",
                "User research basics",
                "Wireframing and prototyping",
            ],
            "Year 2": [
                "Design tools (Figma, Adobe XD)",
                "Interaction design",
                "Build design case studies",
            ],
            "Year 3": [
                "Design systems",
                "Accessibility and usability testing",
                "Design leadership skills",
            ],
        },
        "Web Developer": {
            "Year 1": [
                "HTML, CSS, JavaScript",
                "Responsive design",
                "Build static websites",
            ],
            "Year 2": [
                "Frontend frameworks (React/Vue)",
                "Backend APIs",
                "Deploy full-stack apps",
            ],
            "Year 3": [
                "Performance optimization",
                "Cloud deployment",
                "Real-world client projects",
            ],
        },
        "Digital Marketer": {
            "Year 1": [
                "Basics of digital marketing",
                "Content creation",
                "Social media strategy",
            ],
            "Year 2": [
                "SEO and analytics",
                "Paid ads (Google/Facebook)",
                "Email marketing",
            ],
            "Year 3": [
                "Marketing automation",
                "Brand building",
                "Campaign analysis",
            ],
        },
    }
    return plans.get(career_name, {})


def signup(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)
            messages.success(request, "Account created successfully. You are now logged in.")
            return redirect("test")
    else:
        form = UserCreationForm()

    return render(request, "predictor/signup.html", {"form": form})


@login_required(login_url="login")
def dashboard(request):
    history = StudentSkill.objects.filter(user=request.user)
    return render(request, "predictor/dashboard.html", {"history": history})


@login_required(login_url="login")
def export_history(request):
    history = StudentSkill.objects.filter(user=request.user).order_by("-created_at")
    rows = [
        ["Date", "Career", "Coding", "Math", "Creativity", "Communication", "Academic", "Interests"],
    ]
    for item in history:
        rows.append([
            item.created_at.isoformat(),
            item.predicted_career,
            str(item.coding),
            str(item.math),
            str(item.creativity),
            str(item.communication),
            item.academic_performance or "",
            item.interests or "",
        ])

    content = "\n".join(
        [",".join([f'"{cell}"' if "," in cell or '"' in cell else cell for cell in row]) for row in rows]
    )
    response = HttpResponse(content, content_type="text/csv")
    response["Content-Disposition"] = "attachment; filename=career_history.csv"
    return response


@login_required(login_url="login")
def career_resources(request, career_slug=None):
    details = get_career_details(career_slug)
    if not details:
        # If the career was not found, show the user the available career paths.
        available = [
            {"name": c.get("name"), "slug": slug}
            for slug, c in career_info().items()
        ]
        return render(
            request,
            "predictor/career_resources.html",
            {"career": None, "available_careers": available},
        )

    return render(request, "predictor/career_resources.html", {"career": details})


@login_required(login_url="login")
def test(request):
    if request.method == "POST":
        coding = int(request.POST.get('coding', 0))
        math = int(request.POST.get('math', 0))
        creativity = int(request.POST.get('creativity', 0))
        communication = int(request.POST.get('communication', 0))
        academic = request.POST.get('academic', "")
        interests = request.POST.get('interests', "")

        data = [coding, math, creativity, communication]
        result = predict_career(data)

        if isinstance(result, str) and "Model not trained" in result:
            messages.error(request, "Model not trained yet. Run 'python manage.py train_model' to create the prediction model.")
            return render(request, "predictor/result.html", {"career": None, "roadmap": []})

        # Save the attempt for the user
        StudentSkill.objects.create(
            user=request.user,
            coding=coding,
            math=math,
            creativity=creativity,
            communication=communication,
            academic_performance=academic,
            interests=interests,
            predicted_career=result,
        )

        requirements = career_requirements(result)
        student_skills = {
            "coding": coding,
            "math": math,
            "creativity": creativity,
            "communication": communication,
        }
        gap = skill_gap(student_skills, requirements)
        demand = career_demand_info(result)
        path_by_year = learning_path_by_year(result)

        roadmap = career_roadmap(result)
        career_slug = get_career_slug(result)
        return render(
            request,
            "predictor/result.html",
            {
                "career": result,
                "career_slug": career_slug,
                "roadmap": roadmap,
                "requirements": requirements,
                "skill_gap": gap,
                "demand": demand,
                "learning_path": path_by_year,
                "inputs": {
                    "coding": coding,
                    "math": math,
                    "creativity": creativity,
                    "communication": communication,
                    "academic": academic,
                    "interests": interests,
                },
            },
        )

    return render(request, "predictor/test.html")


@login_required(login_url="login")
def career_comparison(request):
    careers = []
    for slug, details in career_info().items():
        demand = career_demand_info(details["name"])
        careers.append(
            {
                "slug": slug,
                "name": details["name"],
                "demand": demand.get("demand", "—"),
                "growth": demand.get("growth", "—"),
                "salary": demand.get("salary", "—"),
                "difficulty": details.get("difficulty", "—"),
            }
        )

    return render(request, "predictor/career_comparison.html", {"careers": careers})


@login_required(login_url="login")
def career_chatbot(request):
    history = []
    if request.method == "POST":
        message = request.POST.get("message", "").strip().lower()
        if message:
            reply = get_chatbot_response(message)

            history = request.session.get("chat_history", [])
            history.insert(0, {"user": request.POST.get("message", ""), "bot": reply})
            request.session["chat_history"] = history[:20]

    history = request.session.get("chat_history", [])
    return render(request, "predictor/chatbot.html", {"history": history})


def get_chatbot_response(message):
    """Generate intelligent chatbot responses based on user queries."""
    message = message.lower()

    # Career-specific questions
    if "data scientist" in message or "data science" in message:
        if "without coding" in message:
            return "Data science requires some coding, but you can start with tools like Excel, Tableau, or no-code platforms. However, learning Python or R will significantly boost your career prospects."
        elif "salary" in message:
            return "Data scientists earn ₹10-20 LPA in India, with experienced professionals making ₹25+ LPA. Entry-level positions start around ₹6-8 LPA."
        elif "skills" in message or "learn" in message:
            return "Key skills for data science: Python, SQL, statistics, machine learning, data visualization. Start with Python basics, then move to pandas and scikit-learn."
        else:
            return "Data science involves analyzing data to extract insights. Focus on Python, statistics, and building real projects. Check out our learning roadmap for a structured path!"

    elif "machine learning" in message or "ml engineer" in message:
        if "salary" in message:
            return "ML engineers earn ₹12-22 LPA in India. Senior roles can go up to ₹30+ LPA."
        elif "skills" in message:
            return "Essential skills: Python, algorithms, TensorFlow/PyTorch, statistics, cloud platforms (AWS/GCP). Start with Python fundamentals."
        else:
            return "ML engineering focuses on building and deploying ML models. You'll need strong coding skills and understanding of algorithms. Our roadmap provides a year-by-year learning plan."

    elif "web developer" in message or "frontend" in message or "backend" in message:
        if "salary" in message:
            return "Web developers earn ₹7-14 LPA. Full-stack developers with experience can earn ₹15-20 LPA."
        elif "skills" in message:
            return "Frontend: HTML, CSS, JavaScript, React/Vue. Backend: Node.js, Python/Django, databases. Full-stack combines both."
        else:
            return "Web development is great for beginners! Start with HTML/CSS/JS, then choose frontend (React) or backend (Django/Node). Build projects to showcase your skills."

    elif "ui/ux" in message or "designer" in message:
        if "salary" in message:
            return "UI/UX designers earn ₹6-12 LPA in India. Senior designers can make ₹15+ LPA."
        elif "skills" in message:
            return "Key skills: Figma, Adobe XD, user research, prototyping, design principles. Portfolio is crucial!"
        else:
            return "UI/UX design combines creativity with user psychology. Learn design tools, conduct user research, and build a strong portfolio of case studies."

    elif "digital marketing" in message or "marketing" in message:
        if "salary" in message:
            return "Digital marketers earn ₹5-10 LPA. Specialists in SEO or PPC can earn more."
        elif "skills" in message:
            return "Skills: SEO, Google Ads, social media marketing, content creation, analytics tools like Google Analytics."
        else:
            return "Digital marketing involves promoting brands online. Learn about SEO, social media, and analytics. Great for creative people who enjoy content creation."

    # General career advice
    elif "coding" in message and "without" in message:
        return "Most tech careers benefit from coding skills. You can start with no-code tools, but learning programming opens more opportunities. Try Python - it's beginner-friendly!"

    elif "beginner" in message or "start" in message:
        return "Start with our skill assessment test! It will recommend a career path and provide a learning roadmap. Focus on building small projects to gain experience."

    elif "resume" in message or "cv" in message:
        return "Use our resume analyzer tool! Key tips: Include projects, GitHub links, relevant skills, and quantifiable achievements. Tailor your resume for each job application."

    elif "interview" in message:
        return "Practice coding problems on LeetCode, explain your projects clearly, and research the company. Behavioral questions assess culture fit, technical questions test your skills."

    elif "portfolio" in message or "projects" in message:
        return "Build a portfolio website or GitHub profile. Include 3-5 projects that demonstrate your skills. Each career page has project suggestions to get you started."

    elif "internship" in message:
        return "Look for internships on LinkedIn, Indeed, or company career pages. Focus on gaining experience rather than high pay initially. Network and attend career fairs."

    elif "courses" in message or "learning" in message:
        return "Great platforms: Coursera, Udemy, edX, freeCodeCamp. Each career page has recommended courses. Combine online learning with hands-on projects."

    elif "salary" in message:
        return "Salaries vary by experience, location, and company. Check our career comparison tool for estimates. Focus on skills and experience over initial pay."

    elif "difficult" in message or "hard" in message:
        return "All careers require dedication! Data science and ML are challenging but rewarding. Web development is more accessible for beginners. Choose based on your interests."

    # Default responses
    elif any(word in message for word in ["hello", "hi", "hey"]):
        return "Hello! I'm here to help with career advice. Ask me about specific careers, skills, salaries, or how to get started in tech!"

    elif "thank" in message:
        return "You're welcome! Keep learning and building projects. Check out our other tools for more guidance."

    else:
        return "I'd recommend taking our skill assessment test first - it will give you personalized career recommendations and a learning roadmap. What specific career are you interested in?"


@login_required(login_url="login")
def personality_test(request):
    result = None
    if request.method == "POST":
        # Get all form data
        responses = {
            'q1': request.POST.get("q1", ""),
            'q2': request.POST.get("q2", ""),
            'q3': request.POST.get("q3", ""),
            'q4': request.POST.get("q4", ""),
            'q5': request.POST.get("q5", ""),
            'q6': request.POST.get("q6", ""),
            'q7': request.POST.get("q7", ""),
            'interests': request.POST.get("interests", ""),
            'aptitude': request.POST.get("aptitude", ""),
        }

        # Analyze personality traits
        traits = []
        career_matches = []

        # Question 1: Problem solving preference
        if responses['q1'] == "complex":
            traits.append("Analytical Thinker")
            career_matches.extend(["Data Scientist", "Machine Learning Engineer"])
        elif responses['q1'] == "practical":
            traits.append("Practical Problem Solver")
            career_matches.extend(["Software Developer", "Web Developer"])
        else:
            traits.append("Creative Problem Solver")
            career_matches.extend(["UI/UX Designer", "Digital Marketer"])

        # Question 2: Work style
        if responses['q2'] == "team":
            traits.append("Team Player")
            career_matches.extend(["Digital Marketer", "UI/UX Designer"])
        elif responses['q2'] == "solo":
            traits.append("Independent Worker")
            career_matches.extend(["Data Scientist", "Software Developer"])
        else:
            traits.append("Flexible Collaborator")

        # Question 3: Motivation
        if responses['q3'] == "impact":
            traits.append("Impact-driven")
            career_matches.extend(["Digital Marketer", "UI/UX Designer"])
        elif responses['q3'] == "innovation":
            traits.append("Innovation-focused")
            career_matches.extend(["Machine Learning Engineer", "Data Scientist"])
        else:
            traits.append("Learning-oriented")
            career_matches.extend(["Software Developer", "Web Developer"])

        # Question 4: Data vs Design
        if responses['q4'] == "data":
            traits.append("Data-oriented")
            career_matches.extend(["Data Scientist", "Machine Learning Engineer"])
        elif responses['q4'] == "design":
            traits.append("Design-oriented")
            career_matches.extend(["UI/UX Designer", "Web Developer"])
        else:
            traits.append("Content-oriented")
            career_matches.extend(["Digital Marketer"])

        # Question 5: Learning style
        if responses['q5'] == "structured":
            traits.append("Structured Learner")
            career_matches.extend(["Software Developer", "Machine Learning Engineer"])
        elif responses['q5'] == "experimental":
            traits.append("Experimental Learner")
            career_matches.extend(["Data Scientist", "UI/UX Designer"])
        else:
            traits.append("Adaptive Learner")

        # Question 6: Work environment
        if responses['q6'] == "office":
            traits.append("Office Environment")
        elif responses['q6'] == "remote":
            traits.append("Remote Work Preference")
        else:
            traits.append("Flexible Environment")

        # Question 7: Career priority
        if responses['q7'] == "growth":
            traits.append("Career Growth Focused")
        elif responses['q7'] == "balance":
            traits.append("Work-Life Balance")
        else:
            traits.append("Stability-oriented")

        # Count career matches to find top recommendations
        from collections import Counter
        career_counts = Counter(career_matches)
        top_careers = [career for career, count in career_counts.most_common(3)]

        # Generate personalized suggestions
        suggestions = []
        if "Data Scientist" in top_careers:
            suggestions.append("Consider data science - you'll enjoy analyzing complex datasets and finding patterns.")
        if "Machine Learning Engineer" in top_careers:
            suggestions.append("ML engineering could be perfect - you seem to enjoy technical challenges and innovation.")
        if "Software Developer" in top_careers:
            suggestions.append("Software development suits your analytical and structured approach to problem-solving.")
        if "Web Developer" in top_careers:
            suggestions.append("Web development offers creative freedom with technical structure.")
        if "UI/UX Designer" in top_careers:
            suggestions.append("UI/UX design would leverage your creative and user-focused thinking.")
        if "Digital Marketer" in top_careers:
            suggestions.append("Digital marketing aligns with your interest in impact and communication.")

        result = {
            "traits": traits,
            "top_careers": top_careers,
            "interests": responses['interests'],
            "aptitude": responses['aptitude'],
            "suggestions": suggestions,
            "next_steps": [
                "Take our skill assessment test for detailed recommendations",
                "Explore the suggested careers using our comparison tool",
                "Check out learning roadmaps for your top career matches"
            ]
        }

    return render(request, "predictor/personality_test.html", {"result": result})


@login_required(login_url="login")
def resume_analyzer(request):
    analysis = None
    if request.method == "POST" and request.FILES.get("resume"):
        resume_file = request.FILES["resume"]
        filename = resume_file.name.lower()
        text = ""

        # Attempt to parse the resume from common formats.
        # Supports: .txt, .pdf, .docx
        if filename.endswith(".txt") or filename.endswith(".md") or filename.endswith(".csv"):
            text = resume_file.read().decode("utf-8", errors="ignore")
        elif filename.endswith(".pdf"):
            try:
                from PyPDF2 import PdfReader

                reader = PdfReader(resume_file)
                pages = [p.extract_text() for p in reader.pages if p]
                text = "\n".join(pages)
            except ImportError:
                messages.error(
                    request,
                    "PDF resume support requires the 'PyPDF2' package. Install it with 'pip install PyPDF2' and try again."
                )
                return render(request, "predictor/resume_analyzer.html", {"analysis": None})
            except Exception:
                text = resume_file.read().decode("utf-8", errors="ignore")
        elif filename.endswith(".docx"):
            try:
                from docx import Document

                doc = Document(resume_file)
                text = "\n".join(p.text for p in doc.paragraphs)
            except ImportError:
                messages.error(
                    request,
                    "DOCX resume support requires the 'python-docx' package. Install it with 'pip install python-docx' and try again."
                )
                return render(request, "predictor/resume_analyzer.html", {"analysis": None})
            except Exception:
                text = resume_file.read().decode("utf-8", errors="ignore")
        else:
            # Fallback for any other type: try to decode as text.
            text = resume_file.read().decode("utf-8", errors="ignore")

        text = text.lower()

        # Comprehensive skill analysis
        skill_categories = {
            "Programming Languages": [
                "python", "java", "javascript", "c++", "c#", "ruby", "php", "swift", "kotlin", "go", "rust", "typescript"
            ],
            "Data Science & ML": [
                "machine learning", "data science", "pandas", "numpy", "scikit-learn", "tensorflow", "pytorch", "keras",
                "data analysis", "statistics", "matplotlib", "seaborn", "jupyter", "sql", "mysql", "postgresql"
            ],
            "Web Development": [
                "html", "css", "react", "vue", "angular", "node.js", "django", "flask", "express", "bootstrap", "sass"
            ],
            "Tools & Technologies": [
                "git", "github", "docker", "kubernetes", "aws", "azure", "gcp", "linux", "bash", "powershell"
            ],
            "Design Tools": [
                "figma", "adobe xd", "photoshop", "illustrator", "sketch", "invision", "zeplin"
            ],
            "Marketing Tools": [
                "google analytics", "google ads", "facebook ads", "seo", "sem", "hubspot", "mailchimp"
            ]
        }

        found_skills = {}
        missing_skills = {}
        total_found = 0

        for category, skills in skill_categories.items():
            found = [skill for skill in skills if skill in text]
            found_skills[category] = found
            missing_skills[category] = [skill for skill in skills if skill not in text]
            total_found += len(found)

        # Calculate score based on skills found
        max_possible_skills = sum(len(skills) for skills in skill_categories.values())
        skill_score = min(100, (total_found / max_possible_skills) * 100)

        # Content analysis
        content_score = 0
        suggestions = []

        # Check for essential sections
        has_projects = any(word in text for word in ["project", "projects", "portfolio", "github"])
        has_experience = any(word in text for word in ["experience", "work", "internship", "job"])
        has_education = any(word in text for word in ["education", "degree", "university", "college"])
        has_skills = any(word in text for word in ["skills", "technologies", "tools"])

        section_score = (has_projects + has_experience + has_education + has_skills) * 15
        content_score += section_score

        # Length check (rough estimate)
        word_count = len(text.split())
        if word_count < 200:
            suggestions.append("Your resume seems short. Aim for 300-500 words to provide more detail.")
            content_score -= 10
        elif word_count > 800:
            suggestions.append("Your resume might be too long. Consider condensing to focus on the most relevant information.")

        # Specific suggestions
        if not has_projects:
            suggestions.append("Add a projects section showcasing your work. Include GitHub links and descriptions of what you built.")
        if not has_experience:
            suggestions.append("Include work experience, internships, or volunteer roles that demonstrate your skills.")
        if not has_skills:
            suggestions.append("Add a dedicated skills section listing technical skills, tools, and technologies you know.")
        if "github" not in text and "portfolio" not in text:
            suggestions.append("Include links to your GitHub profile or personal portfolio website.")

        # Check for quantifiable achievements
        has_quantifiable = any(word in text for word in ["%", "increased", "improved", "reduced", "built", "created", "developed"])
        if not has_quantifiable:
            suggestions.append("Add quantifiable achievements (e.g., 'Increased performance by 30%', 'Built app used by 100+ users').")

        # Final score calculation
        final_score = max(0, min(100, skill_score * 0.7 + content_score * 0.3))

        # Generate improvement recommendations
        top_missing_categories = sorted(missing_skills.items(), key=lambda x: len(x[1]), reverse=True)[:3]
        improvement_areas = []
        for category, skills in top_missing_categories:
            if skills:
                improvement_areas.extend(skills[:3])  # Top 3 missing skills per category

        analysis = {
            "score": round(final_score),
            "skill_score": round(skill_score),
            "content_score": round(content_score),
            "found_skills": found_skills,
            "missing_skills": improvement_areas[:10],  # Top 10 missing skills
            "suggestions": suggestions,
            "strengths": [
                f"Found {total_found} relevant skills across {len([cat for cat, skills in found_skills.items() if skills])} categories"
            ] if total_found > 0 else ["Start building technical skills relevant to your target career"],
            "word_count": word_count
        }

    return render(request, "predictor/resume_analyzer.html", {"analysis": analysis})
