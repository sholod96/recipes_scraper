import requests
from bs4 import BeautifulSoup
import pandas as pd

#Get all recipes types from https://www.recetasgratis.net/

soup_recipe_types = BeautifulSoup(requests.get('https://www.recetasgratis.net/').text)
recipes_types = soup_recipe_types.find_all('div', {'class': 'categoria ga'})
recipes_types = [i.a['href'] for i in recipes_types]
recipes_types

#Create corresponding page url for recipe_type url for a given number page

def link_page(recipe_link, i):
  return recipe_link[:-6]+str(i)+'.html'

#Get all the corresponding recipes from above url

def all_recipes(response):
  soup = BeautifulSoup(response.text)
  return [recipe.a['href'] for recipe in soup.find_all('div', {'class': 'resultado link'})]

#Get recipe link, name, ingredients, diners, duration and difficulty

def get_recipes_data(recipe_link):

  response = requests.get(recipe_link)
  soup = BeautifulSoup(response.text)

  recipe_name_pre = soup.find_all('h1', {'class': 'titulo titulo--articulo'})
  ingredients_pre= soup.find_all('li', {'class': 'ingrediente'})
  diners_pre = soup.find_all('span', {'class': 'property comensales'})
  duration_pre = soup.find_all('span', {'class': 'property duracion'})
  difficulty_pre = soup.find_all('span', {'class': 'property dificultad'})

  if (len(recipe_name_pre) > 0) & (len(diners_pre) > 0) & (len(duration_pre) > 0) & (len(difficulty_pre) > 0) & (len(ingredients_pre) > 0):

    recipe_name = recipe_name_pre[0].text.split('Receta de ')[-1]
    diners = diners_pre[0].text
    duration = duration_pre[0].text
    difficulty = difficulty_pre[0].text

    return (recipe_link, recipe_name, [ingredient.label.text.replace('\n','').strip() for ingredient in ingredients_pre if ingredient.label is not None], diners, duration, difficulty)

  else:
    return None

#Get recipe link, name and ingredients from recipes that have only this info

def get_recipes_data2(recipe_link):

  response = requests.get(recipe_link)
  soup = BeautifulSoup(response.text)

  recipe_list_pre = soup.find_all('h2', {'class': 'titulo titulo--h2 titulo--apartado'})
  ingredients_list_pre = soup.find_all('div', {'class': 'apartado'})

  if (len(recipe_list_pre) > 0) & (len(ingredients_list_pre) > 0):

    recipe_list = [title.text.replace('\n', '') for title in recipe_list_pre]
    ingredients_list = [ingredient.ul for ingredient in ingredients_list_pre]

  else:
    return None
  recipes_and_ingredients = []
  for recipe, ingredients in zip(recipe_list, ingredients_list):
    if (ingredients is not None) & (recipe is not None):
      recipes_and_ingredients.append((recipe_link, recipe, [ingredient.text for ingredient in ingredients]))
  return recipes_and_ingredients

#Iterate a given "recipe_link" "max_pages" times

def pages_iterator(recipe_link, max_pages):

  i = 1
  page_ = link_page(recipe_link, i)
  response = requests.get(page_)

  all_final_recipes = all_recipes(response)
  recipe_data = [get_recipes_data2(recipe) if get_recipes_data(recipe) is None else get_recipes_data(recipe) for recipe in all_final_recipes]

  recipes_data_list = []

  recipes_data_list.append(recipe_data)

  while i<max_pages:

    i += 1
    page_ = link_page(recipe_link, i)
    response = requests.get(page_)

    if response.url == recipe_link:
      break

    all_final_recipes = all_recipes(response)

    for recipe in all_final_recipes:
      if get_recipes_data(recipe) is not None:
        recipe_data = get_recipes_data(recipe)
        recipes_data_list.append(recipe_data)
      elif get_recipes_data2(recipe) is not None:
        recipe_data = get_recipes_data2(recipe)
        recipes_data_list.append(recipe_data)

  return recipes_data_list

#Iterates 3 times every recipe type link given in recipes_types above list

recipes_dict = {}
for recipe_type in recipes_types:
  print(recipe_type)
  recipes_dict[recipe_type] = pages_iterator(recipe_type, 3)

#Data structure cleaning for dataframe

data = [k for i in recetas_por_tipo.values() for j in i for k in j]
data_cleaned = []
for d in data:
  if len(d) == 6:
    data_cleaned.append(d)
  elif len(d) == 9:
    data_cleaned.append(tuple(list(d)[:6]))
  elif len(d) == 3:
    data_cleaned.append(tuple(list(d) + 3 * [None,]))

#Dataframe creation

data = pd.DataFrame(data_cleaned, columns=['Link','Receta', 'Ingredientes', 'Comensales', 'Tiempo', 'Dificultad'])

#Csv writer

data.to_csv('../dataset/recipes_webscraping.csv', encoding='utf-8', sep = '|', index=False)
