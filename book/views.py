from django.shortcuts import render

from book.models import Author, Book, Comment, Genre
from .utils import *
from django.http import JsonResponse
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from rest_framework.views import APIView
# Create your views here.

class IndexPage(APIView):
    def get(self, request, *args, **kwargs):
        return render(request, 'index.html')
    
class Recommendations(APIView):
    def get(self, request, *args, **kwargs):
        sort_by = request.GET.get("sort_by")
        filter_by = request.GET.get("filter_by")
        user = request.user
        if user.is_anonymous:
            return render(request, 'recommendation.html', context={"message": "You need to be authenticated to look at liked books"})
        
        books = get_books(user, 'recommendation', sort_by, filter_by)
        if not books:
            return render(request, 'recommendation.html', context={"error": "No books recommendations. Explore and recommend books to see them here."})

        return render(request, 'recommendation.html', context={"books": books})
    
    def post(self, request, *args, **kwargs):
        user = request.user
        if user.is_anonymous:
            return render(request, 'index.html', context={"message": "You need to be authenticated to recommend books"})

        book = request.data

        title = book.get("title")
        authors = book.get("authors") or list()
        if authors:
            authors = authors.split(",")

        description = book.get("description")
        cover_image = book.get("thumbnail")
        ratings = book.get("ratingsCount") or -1
        google_book_id = book.get("googleBookId")
        publication_date = book.get("publishedDate")
        genres = book.get("genre") or list()
        if genres:
            genres = genres.split(",")

        if not google_book_id and not (title or authors):
            return JsonResponse({"error": "Not able to like this book"})
        
        existing_books = Book.objects.filter(Q(google_book_id=google_book_id) | Q(title=title, authors__name__in=authors))
        if existing_books:
            liked_book = existing_books.filter(recommended_by=user).first()
            if liked_book:
                # un-recommend
                liked_book.recommended_by.remove(user)
                return JsonResponse({"success": True, "action": "unlike"})
            else:
                # recommend
                unliked_book = existing_books.first()
                unliked_book.recommended_by.add(user)

            return JsonResponse({"success": True, "action": "like"})
        
        new_authors = list()
        for author in authors:
            author_obj, _ = Author.objects.get_or_create(name=author.strip())
            new_authors.append(author_obj)
            
        new_genre = list()
        for genre in genres:
            genre_obj, _ = Genre.objects.get_or_create(name=genre.strip())
            new_genre.append(genre_obj)

        cover_image = create_content(google_book_id, cover_image)
        new_book = Book.objects.create(
            title=title,
            description=description,
            cover_image=cover_image,
            ratings=ratings,
            google_book_id=google_book_id,
            publication_date=publication_date,
        )
        new_book.authors.add(*new_authors)
        new_book.genres.add(*new_genre)
        new_book.recommended_by.add(user)
        return JsonResponse({"success": True, "action": "like"})


class Likes(APIView):
    def get(self, request, *args, **kwargs):
        user = request.user
        if user.is_anonymous:
            return render(request, 'liked_by_user.html', context={"message": "You need to be authenticated to look at liked books"})
        
        books = get_books(user)
        if not books:
            return render(request, 'liked_by_user.html', context={"error": "No books liked. Explore and like books to see them here."})

        return render(request, 'liked_by_user.html', context={"books": books})
    
    def post(self, request, *args, **kwargs):
        try:
            user = request.user
            if user.is_anonymous:
                return render(request, 'liked_by_user.html', context={"message": "You need to be authenticated to look at liked books"})
            google_book_id = request.POST.get("google_book_id")

            book = Book.objects.get(google_book_id=google_book_id)
            book.liked_by.remove(user)
            books = get_books(user)
            return render(request, 'liked_by_user.html', context={"books": books})
        except Comment.DoesNotExist as e:
            return JsonResponse({"error": f"Does not exist: {str(e)}"})
        except Exception as e:
            return JsonResponse({"error": f"Unexpected error occurred: {str(e)}"})
        
        
class RemoveRecommendation(APIView):
    def get(self, request, *args, **kwargs):
        sort_by = request.GET.get("sort_by")
        filter_by = request.GET.get("filter_by")
        user = request.user
        if user.is_anonymous:
            return render(request, 'recommendation.html', context={"message": "You need to be authenticated to look at liked books"})
        
        books = get_books(user, 'recommendation', sort_by, filter_by)
        if not books:
            return render(request, 'recommendation.html', context={"error": "No books recommendations. Explore and recommend books to see them here."})

        return render(request, 'recommendation.html', context={"books": books})
    
    def post(self, request, *args, **kwargs):
        try:
            user = request.user
            if user.is_anonymous:
                return render(request, 'recommendation.html', context={"message": "You need to be authenticated to look at recommended books"})
            google_book_id = request.POST.get("google_book_id")

            book = Book.objects.get(google_book_id=google_book_id)
            book.recommended_by.remove(user)
            books = get_books(user, "recommendation")
            return render(request, 'recommendation.html', context={"books": books})
        except Comment.DoesNotExist as e:
            return JsonResponse({"error": f"Does not exist: {str(e)}"})
        except Exception as e:
            return JsonResponse({"error": f"Unexpected error occurred: {str(e)}"})
        

class LikeBook(LoginRequiredMixin, APIView):
    def post(self, request, *args, **kwargs):
        user = request.user
        if user.is_anonymous:
            return render(request, 'index.html', context={"message": "You need to be authenticated to like books"})
        
        book = request.data

        title = book.get("title")
        authors = book.get("authors") or list()
        if authors:
            authors = authors.split(",")

        description = book.get("description")
        cover_image = book.get("thumbnail")
        ratings = book.get("ratingsCount") or -1
        google_book_id = book.get("googleBookId")
        publication_date = book.get("publishedDate")
        genres = book.get("genre") or list()
        if genres:
            genres = genres.split(",")

        if not google_book_id and not (title or authors):
            return JsonResponse({"error": "Not able to like this book"})
        
        existing_books = Book.objects.filter(Q(google_book_id=google_book_id) | Q(title=title, authors__name__in=authors))
        if existing_books:
            liked_book = existing_books.filter(liked_by=user).first()
            if liked_book:
                # unlike
                liked_book.liked_by.remove(user)
                return JsonResponse({"success": True, "action": "unlike"})
            else:
                # like
                unliked_book = existing_books.first()
                unliked_book.liked_by.add(user)

            return JsonResponse({"success": True, "action": "like"})
        
        new_authors = list()
        for author in authors:
            author_obj, _ = Author.objects.get_or_create(name=author.strip())
            new_authors.append(author_obj)
            
        new_genre = list()
        for genre in genres:
            genre_obj, _ = Genre.objects.get_or_create(name=genre.strip())
            new_genre.append(genre_obj)

        cover_image = create_content(google_book_id, cover_image)
        new_book = Book.objects.create(
            title=title,
            description=description,
            cover_image=cover_image,
            ratings=ratings,
            google_book_id=google_book_id,
            publication_date=publication_date,
        )
        new_book.authors.add(*new_authors)
        new_book.genres.add(*new_genre)
        new_book.liked_by.add(user)
        return JsonResponse({"success": True, "action": "like"})


class SearchBooksView(APIView):
    def get(self, request, *args, **kwargs):
        query = request.GET.get('q', '') # normal query / basically will search all fields in data

        authors = request.GET.get('authors', '')
        title = request.GET.get('title', '')
        categories = request.GET.get('categories', '')
        publisher = request.GET.get('publisher', '')

        if categories:
            query += f'+subject:{categories}'
        if title:
            query += f'+intitle:{title}'
        if authors:
            query += f'+inauthor:{authors}'
        if publisher:
            query += f'+inpublisher:{publisher}'

        if not query:
            return JsonResponse({"error": "No search query provided"})

        data = fetch_books(query)
        return JsonResponse(data)
    
class CommentAPI(APIView):
    def post(self, request):
        user = request.user
        try:
            if user.is_anonymous:
                return JsonResponse({"error": "You need to be authenticated to comment"})
            
            google_book_id = request.POST.get('google_book_id')
            if not google_book_id:
                google_book_id = request.data.get('google_book_id')

            comment = request.POST.get('comment')
            if not comment:
                comment = request.data.get('comment')

            book = Book.objects.get(google_book_id=google_book_id)
            Comment.objects.create(
                book=book,
                user=user,
                comment=comment,
            )
            return render(request, 'liked_by_user.html', context={"books": get_books(user)})
        except Book.DoesNotExist as e:
            return JsonResponse({"error": f"Does not exist: {str(e)}"})
        except Exception as e:
            return JsonResponse({"error": f"Unexpected error occurred: {str(e)}"})
        