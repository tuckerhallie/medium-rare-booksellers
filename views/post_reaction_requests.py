import json
import sqlite3
from models import PostReaction, Reaction, Post, User

def get_all_post_reactions():
    with sqlite3.connect("./db.sqlite3") as conn:
        
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()
        
        db_cursor.execute("""
        SELECT
            pr.id,
            pr.user_id,
            pr.post_id,
            pr.reaction_id,
            r.label reaction_label,
            r.image_url reaction_image_url,
            u.username user_username,
            p.title post_title,
            p.content post_content
        FROM PostReactions pr
        JOIN Users u
            ON u.id = pr.user_id
        JOIN Posts p
            ON p.id = pr.post_id
        JOIN Reactions r
            ON r.id = pr.reaction_id        
        """) 
        
        postreactions = []
        
        dataset = db_cursor.fetchall()
        
        for row in dataset:
          
            postreaction = PostReaction(row['id'], row['user_id'], row['post_id'], row['reaction_id']) 
            
            reaction = Reaction(row['id'], row['reaction_label'], row['reaction_image_url'])
            
            postreaction.reaction = reaction.__dict__
            
            user = User(row['id'], row['user_username'])
            
            postreaction.user = user.__dict__ 
            
            post = Post(row['id'], row['post_title'], row['post_content'])
            
            postreaction.post = post.__dict__
          
            postreactions.append(postreaction.__dict__)
            
    return postreactions
  
def get_single_post_reaction(id):
    with sqlite3.connect("./db.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()
        
        db_cursor.execute("""
        SELECT
            pr.id,
            pr.user_id,
            pr.post_id,
            pr.reaction_id
        FROM PostReactions pr    
        WHERE pr.id = ?
        """, ( id, ))
        
        data = db_cursor.fetchone()
        
        postreaction = PostReaction(data['id'], data['user_id'], data['post_id'], data['reaction_id'])
        
        return postreaction.__dict__
      
def create_post_reaction(new_post_reaction):
  '''docstring'''
  with sqlite3.connect("./db.sqlite3") as conn:
    db_cursor = conn.cursor()
    db_cursor.execute("""
    INSERT INTO PostReaction
      ( user_id, reaction_id, post_id )
    VALUES
      ( ?, ?, ?);
    """, (new_post_reaction['user_id'], new_post_reaction['reaction_id'], new_post_reaction['post_id'] ))
    id = db_cursor.lastrowid
    new_post_reaction['id'] = id
  return new_post_reaction

def delete_post_reaction(id):
  with sqlite3.connect("./db.sqlite3") as conn:
    db_cursor = conn.cursor()
    db_cursor.execute("""
    DELETE FROM PostReaction
    WHERE id = ?
    """, (id, ))      
  
  
    
