from flask import Flask, render_template, request, redirect, url_for
import json
app = Flask(__name__)

DATA_FILE = "data.json"


def load_posts():
    """Loads the information in the Json file"""
    with open("data.json", "r", encoding="utf-8") as json_file:
        return json.load(json_file)


def save_posts(blog_posts):
    """Saves the information in the Json file"""
    json_str = json.dumps(blog_posts)
    with open("data.json", "w", encoding="utf-8") as json_file:
        json_file.write(json_str)

@app.route('/')
def index():
    blog_posts = load_posts()
    return render_template("index.html", post=blog_posts)


@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        blog_posts = load_posts()
        ids = []
        for post in blog_posts:
            post_id = post.get("id")
            ids.append(post_id)
        if not ids:
            new_id = 1
        else:
            new_id = max(ids) + 1
        new_post = {"id": new_id,
                    "author": request.form.get("post-author"),
                    "title": request.form.get("post-title"),
                    "content": request.form.get("content")
                    }
        blog_posts.append(new_post)
        save_posts(blog_posts)
        return redirect(url_for('index'))
    return render_template('add.html')


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)
