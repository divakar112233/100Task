from flask import Flask, render_template_string, request, redirect, url_for, flash
import os
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'portfolio-secret-key'

# ====================== HTML TEMPLATE ======================
PORTFOLIO_HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{{ name }} | Portfolio</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.0/css/all.min.css">
    <style>
        body { font-family: 'Segoe UI', sans-serif; }
        .hero { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); }
    </style>
</head>
<body class="bg-gray-50 text-gray-800">
    <!-- Navbar -->
    <nav class="bg-white shadow-md sticky top-0 z-50">
        <div class="max-w-6xl mx-auto px-6 py-4 flex justify-between items-center">
            <h1 class="text-2xl font-bold text-indigo-600">{{ name }}</h1>
            <div class="space-x-8">
                <a href="#about" class="hover:text-indigo-600 transition">About</a>
                <a href="#skills" class="hover:text-indigo-600 transition">Skills</a>
                <a href="#projects" class="hover:text-indigo-600 transition">Projects</a>
                <a href="#contact" class="hover:text-indigo-600 transition">Contact</a>
            </div>
        </div>
    </nav>

    <!-- Hero -->
    <section class="hero text-white py-32">
        <div class="max-w-6xl mx-auto px-6 text-center">
            <h2 class="text-5xl font-bold mb-4">Hi, I'm {{ name }}</h2>
            <p class="text-2xl mb-8">{{ title }}</p>
            <a href="#contact" 
               class="inline-block bg-white text-indigo-600 px-8 py-3 rounded-full font-semibold hover:bg-gray-100 transition">
                Get In Touch
            </a>
        </div>
    </section>

    <!-- About -->
    <section id="about" class="py-20 bg-white">
        <div class="max-w-6xl mx-auto px-6">
            <h2 class="text-4xl font-bold text-center mb-12">About Me</h2>
            <div class="grid md:grid-cols-2 gap-12 items-center">
                <div>
                    <img src="https://via.placeholder.com/500x500/6366f1/ffffff?text=Your+Photo" 
                         alt="Profile" class="rounded-2xl shadow-xl w-full">
                </div>
                <div class="space-y-6 text-lg">
                    <p>{{ about_text }}</p>
                    <p>Passionate about building beautiful and functional web applications using Flask, Python, and modern technologies.</p>
                </div>
            </div>
        </div>
    </section>

    <!-- Skills -->
    <section id="skills" class="py-20 bg-gray-100">
        <div class="max-w-6xl mx-auto px-6">
            <h2 class="text-4xl font-bold text-center mb-12">Skills</h2>
            <div class="grid grid-cols-2 md:grid-cols-4 gap-6">
                {% for skill in skills %}
                <div class="bg-white p-6 rounded-xl shadow text-center">
                    <i class="{{ skill.icon }} text-4xl text-indigo-600 mb-4"></i>
                    <h3 class="font-semibold">{{ skill.name }}</h3>
                </div>
                {% endfor %}
            </div>
        </div>
    </section>

    <!-- Projects -->
    <section id="projects" class="py-20 bg-white">
        <div class="max-w-6xl mx-auto px-6">
            <h2 class="text-4xl font-bold text-center mb-12">Featured Projects</h2>
            <div class="grid md:grid-cols-2 lg:grid-cols-3 gap-8">
                {% for project in projects %}
                <div class="border border-gray-200 rounded-2xl overflow-hidden hover:shadow-xl transition">
                    <img src="{{ project.image }}" class="w-full h-48 object-cover">
                    <div class="p-6">
                        <h3 class="font-bold text-xl mb-2">{{ project.title }}</h3>
                        <p class="text-gray-600 mb-4">{{ project.description }}</p>
                        <a href="{{ project.link }}" target="_blank" 
                           class="text-indigo-600 hover:underline inline-flex items-center">
                            View Project <i class="ml-2 fas fa-external-link-alt"></i>
                        </a>
                    </div>
                </div>
                {% endfor %}
            </div>
        </div>
    </section>

    <!-- Contact -->
    <section id="contact" class="py-20 bg-gray-900 text-white">
        <div class="max-w-6xl mx-auto px-6">
            <h2 class="text-4xl font-bold text-center mb-12">Get In Touch</h2>
            
            {% if message %}
            <div class="max-w-md mx-auto bg-green-600 text-white p-4 rounded-xl text-center mb-8">
                {{ message }}
            </div>
            {% endif %}
            
            <form method="POST" class="max-w-md mx-auto space-y-6">
                <input type="text" name="name" placeholder="Your Name" required
                       class="w-full px-6 py-4 rounded-xl bg-gray-800 border border-gray-700 focus:outline-none focus:border-indigo-500">
                <input type="email" name="email" placeholder="Your Email" required
                       class="w-full px-6 py-4 rounded-xl bg-gray-800 border border-gray-700 focus:outline-none focus:border-indigo-500">
                <textarea name="message" rows="6" placeholder="Your Message" required
                          class="w-full px-6 py-4 rounded-xl bg-gray-800 border border-gray-700 focus:outline-none focus:border-indigo-500"></textarea>
                <button type="submit"
                        class="w-full bg-indigo-600 hover:bg-indigo-700 py-4 rounded-xl font-semibold transition">
                    Send Message
                </button>
            </form>
        </div>
    </section>

    <footer class="bg-gray-900 text-gray-400 py-8 text-center">
        <p>&copy; {{ year }} {{ name }}. Built with Flask ❤️</p>
    </footer>
</body>
</html>
"""

# ====================== DATA ======================
portfolio_data = {
    "name": "Alex Rivera",
    "title": "Full Stack Developer & Designer",
    "about_text": "I'm a passionate developer with 3+ years of experience building web applications. I love turning ideas into reality using clean code and beautiful design.",
    "skills": [
        {"name": "Python", "icon": "fab fa-python"},
        {"name": "Flask", "icon": "fas fa-flask"},
        {"name": "JavaScript", "icon": "fab fa-js"},
        {"name": "Tailwind CSS", "icon": "fas fa-paint-brush"},
        {"name": "SQL", "icon": "fas fa-database"},
        {"name": "Git", "icon": "fab fa-git-alt"},
    ],
    "projects": [
        {
            "title": "Blog Platform",
            "description": "Full-featured blog with admin panel, authentication, and rich text editor.",
            "image": "https://via.placeholder.com/600x400/4f46e5/ffffff?text=Blog+Platform",
            "link": "#"
        },
        {
            "title": "E-commerce Store",
            "description": "Online store with cart, payment integration, and admin dashboard.",
            "image": "https://via.placeholder.com/600x400/7c3aed/ffffff?text=E-commerce",
            "link": "#"
        },
        {
            "title": "Task Management App",
            "description": "Collaborative task manager with real-time updates.",
            "image": "https://via.placeholder.com/600x400/2563eb/ffffff?text=Task+App",
            "link": "#"
        }
    ]
}

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        # Simulate message sent
        flash("Thank you! Your message has been received.", "success")
        return redirect(url_for('home'))
    
    return render_template_string(PORTFOLIO_HTML, 
                                  name=portfolio_data["name"],
                                  title=portfolio_data["title"],
                                  about_text=portfolio_data["about_text"],
                                  skills=portfolio_data["skills"],
                                  projects=portfolio_data["projects"],
                                  year=datetime.now().year,
                                  message=request.args.get('message'))

if __name__ == '__main__':
    print("🚀 Portfolio is running at http://127.0.0.1:5000")
    print("Default name: Alex Rivera (you can change it easily)")
    app.run(debug=True)