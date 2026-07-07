import requests
from .models import Book

OPEN_LIBRARY_URL = "https://openlibrary.org"

def search_open_library(query: str) -> list:
    
    if not query:
        return []
    
    url = f"{OPEN_LIBRARY_URL}/search.json"
    params = {
        "q": query,
        "fields": "key,title,author_name,isbn,cover_i,first_publish_year",
        "limit": 10
    }

    try:
        response = requests.get(url, params=params, timeout=15)
        response.raise_for_status()
        data = response.json()

        results = []
        for doc in data.get("docs", []):
            # ključ dolazi u obliku "/works/OL12345W"
            external_id = doc.get("key", "").split("/")[-1]
            
            if not external_id:
                continue
                
            authors_list = doc.get("author_name", [])
            authors = ", ".join(authors_list) if authors_list else "Nepoznat autor"
            
            isbns = doc.get("isbn", [])
            isbn = isbns[0] if isbns else None
            
            cover_i = doc.get("cover_i")
            cover_url = f"https://covers.openlibrary.org/b/id/{cover_i}-L.jpg" if cover_i else None
            
            results.append({
                "external_id": external_id,
                "title": doc.get("title"),
                "authors": authors,
                "isbn": isbn,
                "cover_url": cover_url,
                "published_year": doc.get("first_publish_year")
            })
        return results
    except requests.RequestException:
        # Vraćamo praznu listu za sada radi testiranja
        return []
    
def get_or_create_book(external_id: str) -> Book:

    # 1) Provjerimo ako imamo knjigu u bazi
    book = Book.objects.filter(external_id = external_id).first()
    if book:
        return book
    
    # 2) Ako smo došli do ovdje - knjiga nije u bazi, šaljemo query na Open Library
    url = f"{OPEN_LIBRARY_URL}/works/{external_id}.json"
    try:
        response = requests.get(url, timeout=15)
        response.raise_for_status()
        data = response.json()

        title = data.get("title", "Nepoznat naslov.")

        description_data = data.get("description","")
        # Opis može biti objekt ili string
        if isinstance(description_data, dict):
            description = description_data.get("value", "")
        else:
            description = description_data

        covers = data.get("covers", [])
        cover_url = f"https://covers.openlibrary.org/b/id/{covers[0]}-L.jpg" if covers else None

        # Kreiramo knjigu i spremimo ju u bazu
        book = Book.objects.create(
            external_id=external_id,
            title=title,
            authors="Autor (Dohvaća se kroz pretragu)",  # Ovo ćemo elegantno povezati kroz serializer
            description=description,
            cover_url=cover_url,
            published_year=None
        )
        return book
    except requests.RequestException:
        raise ValueError("Nije moguće dohvatiti podatke o knjizi s Open Library API-ja.")
