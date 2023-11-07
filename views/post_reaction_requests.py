import json
import sqlite3
from models import PostReaction, Reaction

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
            r.image_url reaction_image_url
        FROM postreactions pr
        JOIN reactions r
            ON r.id = pr.reaction_id        
        """) 
        
        postreactions = []
        
        dataset = db_cursor.fetchall()
        
        for row in dataset:
          
            postreaction = PostReaction(row['id'], row['user_id'], row['post_id'], row['reaction_id']) 
            
            reaction = Reaction(row['id'], row['reaction_label'], row['reaction_image_url'])
            
            postreaction.reaction = reaction.__dict__
            
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
        FROM postreactions pr    
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
    INSERT INTO postreactions
      ( user_id, reaction_id, post_id )
    VALUES
      ( ?, ?, ?);
    """, (new_post_reaction['userId'], new_post_reaction['reactionId'], new_post_reaction['postId'] ))
    id = db_cursor.lastrowid
    new_post_reaction['id'] = id
  return new_post_reaction

def delete_post_reaction(id):
  with sqlite3.connect("./db.sqlite3") as conn:
    db_cursor = conn.cursor()
    db_cursor.execute("""
    DELETE FROM postreactions
    WHERE id = ?
    """, (id, ))      
  
  
    
