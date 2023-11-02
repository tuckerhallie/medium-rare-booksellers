import sqlite3
import json
from models.post import Post

def get_all_posts():
    with sqlite3.connect("./db.sqlite3") as conn:

        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        db_cursor.execute("""
        SELECT
            p.id,
            p.user_id,
            p.category_id,
            p.title,
            p.publication_date,
            p.image_url,
            p.content,
            p.approved
            
        FROM POSTS p
        """)

        posts = []

        dataset = db_cursor.fetchall()

        for row in dataset:
            post = Post(
              row['id'],
              row['user_id'],
              row['category_id'],
              row['title'],
              row['publication_id'],
              row['image_url'],
              row['content'],
              row['approved']
              )

            posts.append(post.__dict__)

    return posts
