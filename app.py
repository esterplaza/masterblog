from flask import Flask, render_template, request, redirect, url_for
import json
app = Flask(__name__)

DATA_FILE = "data.json"


def load_posts():
    """Loads the information in the Json file"""
    with open("data.json", "r", encoding="utf-8") as json_file:
        return json.load(json_file)


def save_posts(blog_posts):
    """Saves the information in the Json file

    Args:
        blog_posts (int): The Json file.
    """
    json_str = json.dumps(blog_posts)
    with open("data.json", "w", encoding="utf-8") as json_file:
        json_file.write(json_str)

@app.route('/')
def index():
    """Renders the main blog homepage with all published posts.

    Loads the complete list of blog posts from the data store and passes
    them to the index template for rendering.
    """
    blog_posts = load_posts()
    return render_template("index.html", post=blog_posts)


@app.route('/add', methods=['GET', 'POST'])
def add():
    """Handles the creation of a new blog post.

    GET request: Renders the blank form creation page.
    POST request: Extracts form data, generates a new unique integer ID,
    appends the post to the existing data store, and saves it.

    Returns:
        The rendered HTML of the add post form on GET.
        A redirect to the index page on successful POST.
    """
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


@app.route('/delete/<int:post_id>')
def delete(post_id):
    """Deletes a blog post by its unique ID.

    Searches the list of blog posts for a post matching the provided ID.
    If found, the post is removed from the list, the updated list is saved,
    and the user is redirected to the home page.

    Args:
        post_id (int): The unique identifier of the blog post to delete.

    Returns:
        A redirect to the index page.
    """
    blog_posts = load_posts()
    for position, post in enumerate(blog_posts):
        if post.get("id") == post_id:
            blog_posts.pop(position)
            break
    save_posts(blog_posts)
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)
