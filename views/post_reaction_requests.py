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
            pr.reaction_id
            r.label,
            r.image_url
        FROM postreaction pr
        JOIN user u
            ON u.id = pr.user_id
        JOIN post p
            ON p.id = pr.post_id
        JOIN reaction r
            ON r.id = pr.reaction_id        
        """) 
        
        postreactions = []
        
        dataset = db_cursor.fetchall()
        
        for row in dataset:
          
            postreaction = PostReaction(row['id'], row['user_id'], row['post_id'], row['reaction_id']) 
            
            reaction = Reaction(row['id'], row['reaction_label'], row['reaction_image_url'])
            
            postreaction.reaction = reaction.__dict__
            
            user = User(row['id'], row['user_first_name'])
            
            postreactions.append(postreaction.__dict__)
            
    return postreactions
  
def get_single_post_reaction(id):
    
