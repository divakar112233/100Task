from flask import Flask, render_template_string, request, session, redirect, url_for
import random

app = Flask(__name__)
app.secret_key = "movie-app-secret"

# Movie Database
movies = {
    1: {"id": 1, "title": "Dune: Part Two", "genre": "Sci-Fi", "rating": 8.6, "year": 2024,
        "desc": "Paul Atreides unites with Chani and the Fremen while seeking revenge.", 
        "image": "https://picsum.photos/id/1015/300/400"},
    2: {"id": 2, "title": "Oppenheimer", "genre": "Biography", "rating": 8.3, "year": 2023,
        "desc": "The story of American scientist J. Robert Oppenheimer.", 
        "image": "https://picsum.photos/id/201/300/400"},
    3: {"id": 3, "title": "The Batman", "genre": "Action", "rating": 7.8, "year": 2022,
        "desc": "When a killer targets Gotham's elite, Batman must investigate.", 
        "image": "https://picsum.photos/id/180/300/400"},
    4: {"id": 4, "title": "RRR", "genre": "Action", "rating": 7.8, "year": 2022,
        "desc": "A fictitious story about two legendary revolutionaries.", 
        "image": "https://picsum.photos/id/237/300/400"},
    5: {"id": 5, "title": "Everything Everywhere All at Once", "genre": "Sci-Fi", "rating": 7.8, "year": 2022,
        "desc": "An aging Chinese immigrant is swept up in an insane adventure.", 
        "image": "https://picsum.photos/id/870/300/400"},
    6: {"id": 6, "title": "La La Land", "genre": "Romance", "rating": 8.0, "year": 2016,
        "desc": "Two aspiring artists in Los Angeles fall in love.", 
        "image": "https://picsum.photos/id/1016/300/400"},
}

def get_recommendations(genre=None):
    if genre:
        recs = [m for m in movies.values() if m['genre'] == genre]
    else:
        recs = list(movies.values())
    return random.sample(recs, min(3, len(recs)))

@app.route('/')
def home():
    recommendations = get_recommendations()
    search_query = request.args.get('search', '')
    
    filtered_movies = movies.values()
    if search_query:
        filtered_movies = [m for m in movies.values() if search_query.lower() in m['title'].lower()]
    
    return render_template_string("""
    <!DOCTYPE html>
    <html>
    <head>
        <title>MovieRec</title>
        <script src="https://cdn.tailwindcss.com"></script>
    </head>
    <body class="bg-zinc-950 text-white">
        <div class="max-w-6xl mx-auto p-6">
            <div class="flex justify-between items-center mb-8">
                <h1 class="text-5xl font-bold text-red-500">🎬 MovieRec</h1>
                <a href="/watchlist" class="bg-red-600 px-6 py-3 rounded-full font-semibold">My Watchlist ({{ watchlist_count }})</a>
            </div>
            
            <form class="mb-8">
                <input type="text" name="search" value="{{ search_query }}" 
                       placeholder="Search movies..." 
                       class="w-full bg-zinc-900 p-4 rounded-2xl text-lg focus:outline-none">
            </form>

            <h2 class="text-2xl font-semibold mb-6">Recommended for You</h2>
            <div class="grid grid-cols-1 md:grid-cols-3 gap-6 mb-12">
                {% for movie in recommendations %}
                <a href="/movie/{{ movie.id }}" class="block bg-zinc-900 rounded-3xl overflow-hidden hover:scale-105 transition">
                    <img src="{{ movie.image }}" class="w-full h-80 object-cover">
                    <div class="p-5">
                        <h3 class="font-bold text-xl">{{ movie.title }}</h3>
                        <p class="text-zinc-400">{{ movie.genre }} • {{ movie.year }}</p>
                        <p class="text-yellow-400">⭐ {{ movie.rating }}</p>
                    </div>
                </a>
                {% endfor %}
            </div>

            <h2 class="text-2xl font-semibold mb-6">All Movies</h2>
            <div class="grid grid-cols-2 md:grid-cols-4 gap-6">
                {% for movie in filtered_movies %}
                <a href="/movie/{{ movie.id }}" class="bg-zinc-900 rounded-2xl overflow-hidden hover:scale-105 transition">
                    <img src="{{ movie.image }}" class="w-full h-64 object-cover">
                    <div class="p-4">
                        <h4 class="font-semibold">{{ movie.title }}</h4>
                        <p class="text-sm text-zinc-400">{{ movie.genre }}</p>
                    </div>
                </a>
                {% endfor %}
            </div>
        </div>
    </body>
    </html>
    """, recommendations=recommendations, filtered_movies=filtered_movies, 
         watchlist_count=len(session.get('watchlist', [])), search_query=search_query)

@app.route('/movie/<int:movie_id>')
def movie_detail(movie_id):
    movie = movies.get(movie_id)
    if not movie:
        return "Movie not found"
    
    return render_template_string("""
    <!DOCTYPE html>
    <html>
    <head><title>{{ movie.title }}</title><script src="https://cdn.tailwindcss.com"></script></head>
    <body class="bg-zinc-950 text-white p-6">
        <div class="max-w-4xl mx-auto bg-zinc-900 rounded-3xl overflow-hidden">
            <img src="{{ movie.image }}" class="w-full h-96 object-cover">
            <div class="p-8">
                <h1 class="text-4xl font-bold">{{ movie.title }}</h1>
                <p class="text-2xl text-yellow-400 mt-2">⭐ {{ movie.rating }} • {{ movie.year }} • {{ movie.genre }}</p>
                <p class="mt-6 text-zinc-300 text-lg">{{ movie.desc }}</p>
                
                <div class="mt-10 flex gap-4">
                    <form method="post" action="/add-to-watchlist/{{ movie.id }}">
                        <button type="submit" class="bg-red-600 hover:bg-red-700 px-8 py-4 rounded-2xl font-semibold">
                            ➕ Add to Watchlist
                        </button>
                    </form>
                    <a href="/" class="bg-zinc-700 hover:bg-zinc-600 px-8 py-4 rounded-2xl font-semibold">Back to Home</a>
                </div>
            </div>
        </div>
    </body>
    </html>
    """, movie=movie)

@app.route('/add-to-watchlist/<int:movie_id>', methods=['POST'])
def add_to_watchlist(movie_id):
    if 'watchlist' not in session:
        session['watchlist'] = []
    if movie_id not in session['watchlist']:
        session['watchlist'].append(movie_id)
    return redirect(url_for('movie_detail', movie_id=movie_id))

@app.route('/watchlist')
def watchlist():
    watchlist_ids = session.get('watchlist', [])
    watchlist_movies = [movies[i] for i in watchlist_ids if i in movies]
    
    return render_template_string("""
    <!DOCTYPE html>
    <html>
    <head><title>Watchlist</title><script src="https://cdn.tailwindcss.com"></script></head>
    <body class="bg-zinc-950 text-white p-6">
        <div class="max-w-5xl mx-auto">
            <h1 class="text-4xl font-bold mb-8">My Watchlist</h1>
            {% if watchlist_movies %}
                <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
                    {% for movie in watchlist_movies %}
                    <div class="bg-zinc-900 rounded-3xl overflow-hidden">
                        <img src="{{ movie.image }}" class="w-full h-80 object-cover">
                        <div class="p-5">
                            <h3 class="font-bold">{{ movie.title }}</h3>
                            <p class="text-zinc-400">{{ movie.genre }} • ⭐ {{ movie.rating }}</p>
                        </div>
                    </div>
                    {% endfor %}
                </div>
            {% else %}
                <p class="text-center text-2xl text-zinc-500 py-32">Your watchlist is empty</p>
            {% endif %}
            <div class="text-center mt-10">
                <a href="/" class="text-red-500 text-xl">← Browse More Movies</a>
            </div>
        </div>
    </body>
    </html>
    """, watchlist_movies=watchlist_movies)

if __name__ == '__main__':
    print("🚀 Movie Recommendation App Running!")
    print("Open → http://127.0.0.1:5000")
    app.run(debug=True)