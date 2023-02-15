## FastAPI-Classy

Inspired by [Flask-Classy](https://github.com/apiguy/flask-classy).

### Features

- Declarative class based routes
- DRY: inferred response models
- ORM agnostic

### Examples

Look in the [examples](examples/) directory.

### Why?

[FastAPI-Utils](https://github.com/dmontagu/fastapi-utils) provides an implementation of class-based views for FastAPI. FastAPI Classy (this project) takes the concept to the next level and lets you create REST APIs with minimal code. Let me explain.

Imagine you have a users endpoint. Your code would look something like this:

```python
@router.get("/{user_id}", response_model=UserSchema)
def get_user(
    user_id: int,
    db: Session = Depends(get_db),
) -> Any:
    user = db.get(User, user_id)
    if not user:
        raise HTTPException(404)
    return user
```


FastAPI Classy is opinionated, and lets you write this to achieve the same result:


```python
from fastapi_classy import FastAPIClassy

class UserRouter(FastAPIClassy):
    def get(self, user_id: int, db: Session = Depends(get_db)) -> UserSchema:
        user = db.get(User, user_id)
        if not user:
            raise HTTPException(404)
        return user

app.add_router(UserRouter.make_router())
```

What's the difference, you might ask? In a nutshell: you don't need to use `@router.get`. The `get` method maps directly to `/`.

`get` isn't the only special method, there's six of them provided by FastAPI-Classy

```python
class UserRouter(FastAPIClassy):
    def get(self, user_id: int, db: Session = Depends(get_db)) -> UserSchema:
        # Maps to GET /{user_id}
        ...

    def post(...) -> UserSchema:
        # Maps to POST /
        ...

    def index(self, db: Session = Depends(get_db)) -> List[UserSchema]:
        # Maps to GET /
        ...

    def delete(...) -> dict:
        # Maps to DELETE /{user_id}
        ...

    def patch(...) -> UserSchema:
        # Maps to PATCH /{user_id}
        ...

    def put(...) -> UserSchema:
        # Maps to PUT /{user_id}
        ...
```

What if you wanted something which isn't mapped? Easy peasy:

```python
class UserRouter(FastAPIClassy):
    ...

    def random(...):
        # Maps to /random
        ...

```
