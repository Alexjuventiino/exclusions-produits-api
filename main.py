from fastapi import FastAPI, Request
from pydantic import BaseModel
import snowflake.connector
import os

app = FastAPI()

class Produit(BaseModel):
    id_produit: str

class Payload(BaseModel):
    rythme_date: str
    utilisateur: str
    produits: list[Produit]

@app.post("/exclusions")
async def enregistrer_exclusions(data: Payload):
    try:
        conn = snowflake.connector.connect(
            user=os.getenv("SNOWFLAKE_USER"),
            password=os.getenv("SNOWFLAKE_PASSWORD"),
            account=os.getenv("SNOWFLAKE_ACCOUNT"),
            warehouse=os.getenv("SNOWFLAKE_WAREHOUSE"),
            database=os.getenv("SNOWFLAKE_DATABASE"),
            schema=os.getenv("SNOWFLAKE_SCHEMA")
        )
        cursor = conn.cursor()

        for produit in data.produits:
            cursor.execute("""
                INSERT INTO TABLEAU.PUBLIC.exclusions (id_produit, rythme_date, utilisateur)
                VALUES (%s, %s, %s)
            """, (produit.id_produit, data.rythme_date, data.utilisateur))

        cursor.close()
        conn.close()

        return {"success": True, "message": "Exclusions enregistrées"}
    except Exception as e:
        return {"success": False, "message": str(e)}
