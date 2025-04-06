from fastapi import APIRouter, HTTPException
from app.models.post import Post
from app.db.fake_db import fake_posts_db

router = APIRouter()


@router.get("/")
def get_all_posts():
    return fake_posts_db


@router.get("/{post_id}")
def get_post(post_id: int):
    for post in fake_posts_db:
        if post.id == post_id:
            return post
    raise HTTPException(status_code=404, detail="Post not found")


@router.post("/", status_code=201)
def create_post(post: Post):
    fake_posts_db.append(post)
    return post


@router.put("/{post_id}")
def update_post(post_id: int, updated_post: Post):
    for i, post in enumerate(fake_posts_db):
        if post.id == post_id:
            fake_posts_db[i] = updated_post
            return updated_post
    raise HTTPException(status_code=404, detail="Post not found")


@router.delete("/{post_id}", status_code=204)
def delete_post(post_id: int):
    for i, post in enumerate(fake_posts_db):
        if post.id == post_id:
            fake_posts_db.pop(i)
            return
    raise HTTPException(status_code=404, detail="Post not found")