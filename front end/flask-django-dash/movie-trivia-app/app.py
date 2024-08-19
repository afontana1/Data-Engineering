from flask import Flask, render_template, request
import imdb

app = Flask(__name__)


@app.route("/")
def index_get():
    return render_template("index.html")


@app.route("/", methods=["GET", "POST"])
def index_post():
    try:
        movie_name = request.form.get("mname")
        ia = imdb.IMDb()
        m = ia.search_movie(movie_name)[0]
        mov = ia.get_movie(m.getID())
        ia.update(mov, "trivia")
        trivia = mov["trivia"]
        return render_template("index.html", trivia=trivia, m=m)
    except:
        error = "Movie does not exist!"
        return render_template("index.html")


if __name__ == "__main__":
    app.run()
