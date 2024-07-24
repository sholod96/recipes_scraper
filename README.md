---
title: "Recipes Scraper: Datos sobre recetas"
authors: "Sofia Holod"
date: "14 de Noviembre de 2023"
---

# Ficheros

## Requirements.

* requirements.txt 

## Código

* recipesScraper.py: fichero principal, su ejecución da lugar a la base de datos.
* El código debe ejecutarse de la siguiente manera:
  python recipesScraper.py iterations.
  Iterations es un entero que indica el número máximo de iteraciones que queremos realizar sobre cada página de las distintas webs de tipos de recetas.

## Datos

* recipes_scraping: El dataset resultante en formato csv separado por "|" en utf-8 que contiene información de las distintas recetas tal como el link de la misma, los ingredientes, los comensales, el tiempo requerido y la dificultad.
