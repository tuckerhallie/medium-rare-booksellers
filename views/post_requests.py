import sqlite3
import json
from models import Post, User

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
            
        FROM Posts p
        """)

        posts = []

        dataset = db_cursor.fetchall()

        for row in dataset:
            post = Post(
              row['id'],
              row['user_id'],
              row['category_id'],
              row['title'],
              row['publication_date'],
              row['image_url'],
              row['content'],
              row['approved']
              )

            posts.append(post.__dict__)

    return posts

def get_single_post(id):
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
            
        FROM Posts p
        WHERE p.id = ?
        """, ( id, ))

        data = db_cursor.fetchone()

        post = Post(
              data['id'],
              data['user_id'],
              data['category_id'],
              data['title'],
              data['publication_id'],
              data['image_url'],
              data['content'],
              data['approved']
              )

        return post.__dict__

def get_post_by_user(user_id):
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
            
        FROM Posts p
        WHERE p.user_id = ?
        """, ( user_id, ))

        data = db_cursor.fetchone()

        post = Post(
              data['id'],
              data['user_id'],
              data['category_id'],
              data['title'],
              data['publication_id'],
              data['image_url'],
              data['content'],
              data['approved']
              )

        return post.__dict__

def create_post(new_post):
    with sqlite3.connect("./db.sqlite3") as conn:
        db_cursor = conn.cursor()

        db_cursor.execute("""
        INSERT INTO Posts
            ( user_id, category_id, title, publication_date, image_url, content, approved )
        VALUES
            ( ?, ?, ?, ?, ?, ?, ?);
        """, (new_post['userId'],
              new_post['categoryId'],
              new_post['title'],
              new_post['publicationDate'],
              new_post['imageUrl'],
              new_post['content'],
              new_post['approved']
              ))

        id = db_cursor.lastrowid

        new_post['id'] = id


    return new_post

def delete_post(id):
    with sqlite3.connect("./db.sqlite3") as conn:
        db_cursor = conn.cursor()

        db_cursor.execute("""
        DELETE FROM Posts
        WHERE id = ?
        """, (id, ))
