from flask import Flask, request, redirect, url_for, render_template_string, abort

app = Flask(__name__)

VERSION = "v1"
FEATURES = "Add Post"

posts = []
next_id = 1

PAGE = """
<!doctype html>
<html>
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Blog {{ version }}</title>
  <style>
    body { font-family: Arial, sans-serif; background: #f4f6f9; margin: 0; }
    header { background: #2c3e50; color: #fff; padding: 16px 24px; }
    header span { background: #e67e22; padding: 2px 10px; border-radius: 12px; font-size: 14px; margin-left: 8px; }
    main { max-width: 760px; margin: 24px auto; padding: 0 16px; }
    .card { background: #fff; border-radius: 8px; padding: 16px 20px; margin-bottom: 16px; box-shadow: 0 1px 3px rgba(0,0,0,.1); }
    input, textarea { width: 100%; padding: 8px; margin: 6px 0 12px; box-sizing: border-box; border: 1px solid #ccc; border-radius: 4px; }
    textarea { height: 110px; }
    button, .btn { background: #2980b9; color: #fff; border: 0; padding: 8px 16px; border-radius: 4px; cursor: pointer; text-decoration: none; font-size: 14px; }
    .btn-edit { background: #27ae60; }
    .btn-delete { background: #c0392b; }
    .actions { margin-top: 10px; display: flex; gap: 8px; }
    .actions form { margin: 0; }
    small { color: #777; }
  </style>
</head>
<body>
  <header><b>My Blog</b> <span>{{ version }}</span> <small style="color:#ddd">Features: {{ features }}</small></header>
  <main>
    {{ body|safe }}
  </main>
</body>
</html>
"""


def render(body):
    return render_template_string(PAGE, body=body, version=VERSION, features=FEATURES)


def find_post(post_id):
    for p in posts:
        if p["id"] == post_id:
            return p
    abort(404)


@app.route("/")
def index():
    from markupsafe import escape
    html = """
    <div class="card">
      <h2>Add Post</h2>
      <form method="post" action="/add">
        <label>Title</label><input name="title" required>
        <label>Content</label><textarea name="content" required></textarea>
        <button type="submit">Publish</button>
      </form>
    </div>
    <h2>All Posts</h2>
    """
    if not posts:
        html += '<div class="card"><i>No posts yet. Add your first post above.</i></div>'
    for p in reversed(posts):
        html += f"""
        <div class="card">
          <h3>{escape(p['title'])}</h3>
          <p>{escape(p['content'])}</p>
          <div class="actions">
          </div>
        </div>
        """
    return render(html)


@app.route("/add", methods=["POST"])
def add_post():
    global next_id
    title = request.form.get("title", "").strip()
    content = request.form.get("content", "").strip()
    if title and content:
        posts.append({"id": next_id, "title": title, "content": content})
        next_id += 1
    return redirect(url_for("index"))






@app.route("/health")
def health():
    return {"status": "ok", "version": VERSION}


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
