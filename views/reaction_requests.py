import sqlite3
import json
from models import Reaction

def get_single_reaction(id):
  #docstring
  with sqlite3.connect("./db.sqlite3") as conn:
    conn.row_factory = sqlite3.Row
    db_cursor = conn.cursor()
    
    db_cursor.execute("""
    SELECT
      r.id,
      r.label,
      r.imague_url
    FROM reaction r
    WHERE r.id = ?
    """, ( id, ))
    
    data = db_cursor.fetchone()
    
    reaction = Reaction(data['id'], data['label'], data['image_url'])
    
    return reaction.__dict__
  
def get_all_reactions():
  #docstring
  with sqlite3.connect("./db.sqlite3") as conn:
      conn.row_factory = sqlite3.Row
      db_cursor = conn.cursor()
      
      db_cursor.execute("""
      SELECT
        a.id,
        a.label,
        a.image_url
      FROM reaction r
      """)
      
      reactions = []
      dataset = db_cursor.fetchall()
      for row in dataset:
        reaction = Reaction(row['id'], row['label'], row['image_url'])
        reactions.append(reaction.__dict__)
      return reactions
