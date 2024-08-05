import requests
import json
import pandas as pd

from django.core.files.base import ContentFile
from django.db.models import Q, Count

from book.models import Book
from book.serializers import BookSerializer

def fetch_books(query: str):
    url = f"https://www.googleapis.com/books/v1/volumes?q={query}"
    response = requests.get(url)
    data = response.json()

    data_items = data.get("items", list())
    if data_items:
        data['items'] = manipulate_data(data_items)

    return data
    
def manipulate_data(data: list):
    df = pd.DataFrame(data)
    df['google_book_id'] = df['id']
    id_items = df['id'].tolist()

    books_data = list(Book.objects.filter(
        Q(recommended_by__gt=0) | Q(liked_by__gt=0) | Q(comments__gt=0),
          google_book_id__in=id_items).annotate(
              num_liked_by=Count('liked_by'))\
    .values('liked_by', 'recommended_by', 'comments', 'google_book_id', 'id'))
    books_df = pd.DataFrame(books_data)
    if books_df.empty:
        return data

    books_df = books_df.groupby('google_book_id').agg({
        'liked_by': 'count',
        'recommended_by': 'count',
        'comments': 'count',
    }).reset_index()

    books_df = books_df.rename(columns={
        'liked_by': 'total_likes',
        'recommended_by': 'total_recommendations',
        'comments': 'total_comments'
    })

    for col in ['total_likes', 'total_recommendations', 'total_comments']:
        if col in df.columns:
            df.drop(columns=[col], inplace=True)

    merged_df = pd.merge(df, books_df, on='google_book_id', how='left')
    merged_df = merged_df.fillna(0)
    return merged_df.to_dict(orient='records')

def get_data(byte_string_response):
    decoded_string = byte_string_response.decode('utf-8')
    return json.loads(decoded_string)

def create_content(book_id, image_url):
    response = requests.get(image_url)
    if response.status_code == 200:
        image_content = response.content

        file_name = f"cover_image_{book_id}.jpg"
        return ContentFile(image_content, file_name)

def get_books(user, interaction_type=None, sort_by=None, filter_by=None):
    if interaction_type == 'recommendation':
        if filter_by == 'mine':
            books = Book.objects.filter(recommended_by=user)
        else:
            books = Book.objects.all()
    else:
        books = Book.objects.filter(liked_by=user)

    if sort_by:
        books = books.order_by(f"-{sort_by}")
    return BookSerializer(books, many=True, context={'user_id': user.id}).data
