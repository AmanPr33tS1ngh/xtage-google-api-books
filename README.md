# Django Book API Guide

## Overview
This guide is designed to help developers create custom API endpoints for book-related functionalities using Django. We will cover setting up Django, defining models, serializers, views, and URL routing. Additionally, we will provide examples and best practices for implementing CRUD operations, authentication, and data validation.

## Table of Contents
1. [Setup Django](#setup-django)
2. [Define Models](#define-models)
3. [Create Serializers](#create-serializers)
4. [Develop Views](#develop-views)
5. [URL Routing](#url-routing)
6. [CRUD Operations](#crud-operations)
7. [Authentication](#authentication)
8. [Data Validation](#data-validation)

## Setup Django
To start a new Django project, run:
```bash
django-admin startproject myproject
cd myproject
```

## Create a new Django app:

```bash
python manage.py startapp book
python manage.py startapp user
```

## Add the apps to your INSTALLED_APPS in settings.py:
```bash
INSTALLED_APPS = [
    ...
    'book',
    'user',
    ...
]
```

## Define Models
```bash
from django.db import models

class XYZ(models.Model):
  ........
```

## Create Serializers
```bash
from rest_framework import serializers
from .models import Book

class XYZSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = '__all__'
```

## Develop Views
```bash
from rest_framework.views import APIView
from .models import XYZ
from .serializers import XYZSerializer

class XYZView(APIView):
    queryset = XYZ.objects.all()
    serialized_data = BookSerializer(queryset, many=True).data
    return JsonResponse(serialized_data)
```

## URL Routing
```bash
from django.urls import path
from .views import *

urlpatterns = [
    path('xyz/', XYZView.as_view(), name='xyz'),
]
```

# API Documentation

## Overview

This document provides an overview of the API endpoints available in this Django application.

### 1. **API Schema and Documentation**
- **Path:** `/api_schema/`
- **Method:** `GET`
- **Description:** Provides a schema for the REST API.
- **Name:** `api_schema`

- **Path:** `/docs/`
- **Method:** `GET`
- **Description:** Serves the Swagger UI documentation for the API.
- **Name:** `swagger-ui`

### 2. **User Authentication**

#### **Sign Up**
- **Path:** `/user/signup/`
- **Method:** `POST`
- **Description:** Registers a new user.
- **Request Body:**
  - `username`: The username for the new user.
  - `password1`: The password for the new user.
  - `password2`: Confirmation of the password.
- **Response:** 
  - Redirects to the home page on successful registration.
  - Shows validation errors if the registration fails.
- **Name:** `signup`

#### **Sign In**
- **Path:** `/user/signin/`
- **Method:** `POST`
- **Description:** Authenticates a user and logs them in.
- **Request Body:**
  - `username`: The username of the user.
  - `password`: The password of the user.
- **Response:**
  - Redirects to the home page on successful login.
  - Shows authentication errors if login fails.
- **Name:** `signin`

#### **Logout**
- **Path:** `/user/logout/`
- **Method:** `POST`
- **Description:** Logs out the current user.
- **Response:**
  - Redirects to the signin page.
- **Name:** `logout`

### 3. **Book Management**

#### **Index Page**
- **Path:** `/`
- **Method:** `GET`
- **Description:** Displays the index page of books.
- **Name:** `index`

#### **Liked Books**
- **Path:** `/likes/`
- **Method:** `GET`
- **Description:** Displays books liked by the authenticated user.
- **Response:**
  - Renders a template with liked books.
  - Shows a message if the user is not authenticated or has no liked books.
- **Name:** `likes`

#### **Recommendations**
- **Path:** `/recommendations/`
- **Method:** `GET`
- **Description:** Displays book recommendations for the authenticated user.
- **Request Parameters:**
  - `sort_by`: Criteria for sorting recommendations.
  - `filter_by`: Criteria for filtering recommendations.
- **Response:**
  - Renders a template with recommended books.
  - Shows a message if the user is not authenticated or has no recommendations.
- **Method:** `POST`
- **Description:** Adds or removes a book recommendation for the authenticated user.
- **Request Body:**
  - `title`: Title of the book.
  - `authors`: Authors of the book.
  - `description`: Description of the book.
  - `thumbnail`: Cover image of the book.
  - `ratingsCount`: Rating count of the book.
  - `googleBookId`: Google Book ID.
  - `publishedDate`: Publication date of the book.
  - `genre`: Genres of the book.
- **Response:**
  - JSON response indicating whether the book was liked or unliked.
- **Name:** `recommendations`

#### **Like or Unlike Book**
- **Path:** `/like_book/`
- **Method:** `POST`
- **Description:** Likes or unlikes a book for the authenticated user.
- **Request Body:** Same as `/book/recommendations/` POST request.
- **Response:**
  - JSON response indicating whether the book was liked or unliked.
- **Name:** `like_book`

#### **Comment on Book**
- **Path:** `/comment/`
- **Method:** `POST`
- **Description:** Adds a comment to a book.
- **Request Body:**
  - `google_book_id`: ID of the book to comment on.
  - `comment`: The comment text.
- **Response:**
  - Redirects to the liked books page with updated data.
  - Shows errors if the book does not exist or other exceptions occur.
- **Name:** `comment`

#### **Remove Recommendation**
- **Path:** `/remove_recommendation/`
- **Method:** `POST`
- **Description:** Removes a recommendation for the authenticated user.
- **Request Body:**
  - `google_book_id`: ID of the book to remove from recommendations.
- **Response:**
  - Redirects to the recommendations page with updated data.
  - Shows errors if the book does not exist or other exceptions occur.
- **Name:** `remove_recommendation`

#### **Search Books**
- **Path:** `/search_book/`
- **Method:** `GET`
- **Description:** Searches for books based on various criteria.
- **Request Parameters:**
  - `q`: Search query.
  - `authors`: Author names.
  - `title`: Book title.
  - `categories`: Book categories.
  - `publisher`: Publisher name.
- **Response:**
  - JSON response with search results.
  - Shows an error if no query is provided.
- **Name:** `book`
