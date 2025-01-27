from fastapi import FastAPI, Form, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from typing import Optional

app = FastAPI()
templates = Jinja2Templates(directory="templates")

# In-memory storage for recipes
recipes = []
next_id = 1

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request, "recipes": recipes})

@app.get("/create", response_class=HTMLResponse)
async def create_recipe_form(request: Request):
    return templates.TemplateResponse("create.html", {"request": request})

@app.post("/create", response_class=HTMLResponse)
async def create_recipe(request: Request, title: str = Form(...), description: str = Form(...)):
    global next_id
    recipes.append({"id": next_id, "title": title, "description": description})
    next_id += 1
    response = RedirectResponse(url="/", status_code=status.HTTP_303_SEE_OTHER)
    response.headers["HX-Redirect"] = "/"
    return response

@app.get("/edit/{recipe_id}", response_class=HTMLResponse)
async def edit_recipe_form(request: Request, recipe_id: int):
    recipe = next((r for r in recipes if r["id"] == recipe_id), None)
    if recipe:
        return templates.TemplateResponse("edit.html", {"request": request, "recipe": recipe})
    return HTMLResponse("Recipe not found", status_code=404)

@app.post("/edit/{recipe_id}", response_class=HTMLResponse)
async def edit_recipe(request: Request, recipe_id: int, title: str = Form(...), description: str = Form(...)):
    recipe = next((r for r in recipes if r["id"] == recipe_id), None)
    if recipe:
        recipe["title"] = title
        recipe["description"] = description
        return templates.TemplateResponse("index.html", {"request": request, "recipes": recipes})
    return HTMLResponse("Recipe not found", status_code=404)

@app.post("/delete/{recipe_id}", response_class=HTMLResponse)
async def delete_recipe(request: Request, recipe_id: int):
    global recipes
    recipes = [r for r in recipes if r["id"] != recipe_id]
    return templates.TemplateResponse("index.html", {"request": request, "recipes": recipes})
