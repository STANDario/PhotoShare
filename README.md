# PhotoShare

PhotoShare is a REST API for uploading, viewing, as well as commenting, editing comments and adding tags.

## Overview

This project is built on FastAPI and uses PostgreSQL to store user data, photos, and comments. JWT tokens are used for authentication.

## Authentication

Users have three roles: regular user, moderator, and administrator. JWT tokens are used for authentication. The first user registering in the system automatically gets the administrator role.

## Working with Photos

- Users can upload photos with descriptions.
- It's possible to add up to 5 tags per photo.
- Users can perform basic operations on photos using the Cloudinary service.
- Users can create links to transformed images for viewing photos as URL and QR codes.

## Comments

- Each photo has a block of comments.
- Users can comment on each other's photos.
- Users can edit their comment.
- Administrators and moderators can delete comments.

## Installation and Running

1. Clone this repository:

git clone https://github.com/STANDario/PhotoShare.git

2. Install dependencies:
pip install -r requirements.txt

3. Run the project
uvicorn app.main:app --reload

## Open the Swagger documentation at:

http://localhost:9000/docs

## Contribution

If you have any questions or suggestions, please open a new issue or make a pull request.