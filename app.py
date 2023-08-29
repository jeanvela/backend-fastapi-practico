from fastapi import FastAPI, HTTPException
from pydantic import BaseModel #* (esquema) como van a lucir nuestro nuestro datos
from typing import Text, Optional  #* que va ser un string largo  (Optional) que el valor sera opcional
from datetime import datetime #* datetime valor por defecto que se crea el post
from uuid import uuid4 as uuid

app = FastAPI()

posts = []

#* Post Model
class Post(BaseModel):
    id: str = None
    title: str
    author: str
    context: Text
    create_at: datetime = datetime.now()
    published_at: Optional[datetime] = None
    published: bool = False

@app.get('/')
def read_root():
    return {'welcome': 'welcome to my  API'}

@app.get('/posts')
def get_posts():
    return posts

@app.post('/posts')
def save_post(post: Post):
    post.id = str(uuid())
    posts.append(post.model_dump())  
    #! dict() Lo convierto en objeto [key]: value     (post.model_dump())  Probar eso
    return posts[-1]

@app.get('/posts/{post_id}')
def get_post(post_id: str):
    for post in posts:
        if post['id'] == post_id:
            return post
    raise HTTPException(status_code=404, detail='Post not found')

@app.delete('/posts/{post_id}')
def delete_post(post_id: str):
    for index, post in enumerate(posts): #!enumerate muestra el index del objeto y el objeto
        if post['id'] == post_id:
            posts.pop(index)
            return {'message': 'Post has been deleted successfully'}
    raise HTTPException(status_code=404, detail='Post Not found')


@app.put('/posts/{post_id}')
def put_post(post_id: str, updatePost: Post):
    for index, post in enumerate(posts):
        if post['id'] == post_id:
            posts[index]['title'] = updatePost.title
            posts[index]['context'] = updatePost.context
            posts[index]['author'] = updatePost.author
            return {'message': 'Post has been updated successfully'}
    raise HTTPException(status_code=404, detail='Post Not found')
        