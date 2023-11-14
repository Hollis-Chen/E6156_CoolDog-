from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import mysql.connector
from mysql.connector import Error
import uvicorn

app = FastAPI()

# Database Connection
def create_db_connection():
    try:
        connection = mysql.connector.connect(
            host='database-paper.clelurkasv8d.us-east-2.rds.amazonaws.com',
            database='E6156',
            user='admin',
            password='6156cloudcomputing'
        )
        return connection
    except Error as e:
        print(f"Error: {e}")
        return None

@app.get("/")
def read_root():
    return {"message": "Welcome to the Paper Microservice"}

@app.get("/papers/search/byID/{paper_id}")
def get_paper_by_id(paper_id: str):
    connection = create_db_connection()
    if connection:
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM research_papers WHERE paper_id = %s", (paper_id,))
        paper = cursor.fetchone()
        cursor.close()
        connection.close()
        if paper:
            return paper
        else:
            raise HTTPException(status_code=404, detail="Paper not found")

@app.get("/papers/search/byKeyword/{keyword}")
def search_papers_by_keyword(keyword: str):
    connection = create_db_connection()
    if connection:
        cursor = connection.cursor(dictionary=True)
        query = "SELECT * FROM research_papers WHERE LOWER(title) LIKE %s"
        cursor.execute(query, ('%' + keyword.lower() + '%',))
        matching_papers = cursor.fetchall()
        cursor.close()
        connection.close()
        return matching_papers

@app.put("/papers/update/updateTitle/{paper_id}")
def update_paper_title(paper_id: str, updated_title: str):
    connection = create_db_connection()
    if connection:
        cursor = connection.cursor(dictionary=True)
        update_query = "UPDATE research_papers SET title = %s WHERE paper_id = %s"
        data = (updated_title, paper_id)
        cursor.execute(update_query, data)
        connection.commit()
        cursor.close()
        connection.close()
        return {"message": "Title updated successfully"}

class Paper(BaseModel):
    paper_id: str
    title: str
    authors: str
    abstract: str = None
    year: int
    arxiv_id: str = None
    acl_id: str = None
    pmc_id: str = None
    pubmed_id: str = None
    doi: str = None
    venue: str = None
    journal: str = None
    mag_id: str = None
    outbound_citations: str = None
    inbound_citations: str = None
    has_outbound_citations: bool
    has_inbound_citations: bool
    has_pdf_parse: bool
    s2_url: str = None

@app.post("/papers/add")
def add_paper(paper: Paper):
    connection = create_db_connection()
    if connection:
        cursor = connection.cursor(dictionary=True)
        try:
            insert_query = """
            INSERT INTO research_papers (paper_id, title, authors, abstract, year, arxiv_id, acl_id, pmc_id, pubmed_id, doi, venue, journal, mag_id, outbound_citations, inbound_citations, has_outbound_citations, has_inbound_citations, has_pdf_parse, s2_url)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            cursor.execute(insert_query, (
                paper.paper_id,
                paper.title,
                paper.authors,
                paper.abstract,
                paper.year,
                paper.arxiv_id,
                paper.acl_id,
                paper.pmc_id,
                paper.pubmed_id,
                paper.doi,
                paper.venue,
                paper.journal,
                paper.mag_id,
                paper.outbound_citations,
                paper.inbound_citations,
                paper.has_outbound_citations,
                paper.has_inbound_citations,
                paper.has_pdf_parse,
                paper.s2_url
            ))
            connection.commit()
            return {"message": "Paper added successfully"}
        except Error as e:
            connection.rollback() # Rollback the transaction in case of error
            raise HTTPException(status_code=400, detail=str(e))
        finally:
            cursor.close()
            connection.close()
    else:
        raise HTTPException(status_code=500, detail="Could not connect to the database")

@app.delete("/papers/delete/{paper_id}")
def delete_paper(paper_id: str):
    connection = create_db_connection()
    if connection:
        cursor = connection.cursor(dictionary=True)
        try:
            cursor.execute("SELECT * FROM research_papers WHERE paper_id = %s", (paper_id,))
            paper = cursor.fetchone()
            if not paper:
                raise HTTPException(status_code=404, detail="Paper not found")

            delete_query = "DELETE FROM research_papers WHERE paper_id = %s"
            cursor.execute(delete_query, (paper_id,))
            connection.commit()
            if cursor.rowcount == 0:
                raise HTTPException(status_code=404, detail="Paper not found")
            return {"message": f"Paper with ID {paper_id} deleted successfully"}
        except Error as e:
            connection.rollback()
            raise HTTPException(status_code=500, detail=str(e))
        finally:
            cursor.close()
            connection.close()
    else:
        raise HTTPException(status_code=500, detail="Could not connect to the database")


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8012)
