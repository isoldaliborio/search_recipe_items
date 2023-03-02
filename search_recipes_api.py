
# ----- PROJECT -------
# Search 1

# ----- TEAM -------
# Barbara Packard
# Isolda Liborio
# Jurgita Miliauskaitė

# ---- CREDENTIALS -----
# Application ID
# 092316d7
# This is the application ID, you should send with each API request.
# Application Keys
# 15bbc5b6b198bea8d98bca2fb9f826a9
# These are application keys used to authenticate requests.

# ------- Project Briefing: Search ---------
# In this project you'll create a program to search for recipes based on an ingredient. 
# The standard project uses the Edamam Recipe API, 
# but can be changed to use a different API after completing the required tasks.

# ------- Required Tasks ---------
    # These are the required tasks for this project. You should aim to complete these tasks before adding your own ideas to the project.
    # 1. Read the Edamam API documentation ★ https://developer.edamam.com/edamam-docs-recipe-api
    # 2. Ask the user to enter an ingredient that they want to search for
    # 3. Create a function that makes a request to the Edamam API with the required ingredient as
    # part of the search query (also included your Application ID and Application Key
    # 4. Get the returned recipes from the API response
    # 5. Display the recipes for each search result

# # ------- Advanced Required Tasks ---------
    # 6. Save the results to a file
    # 7. Order the results by weight or another piece of data
    # 8. Ask the user additional questions to decide which recipe they should choose
    # 9. Cross-reference the ingredient against the Edamam nutrition analysis API
    # 10. Use a different searchable API (suggestions in useful resources)

# ------ About --------
    # In this code, we define two functions:
    #  display_results - FUNCTION
        #the function when it's called, runs the code ask the input (ingredient) and call the other function 
        # The other function brings the responses keys
        #  in this one we display each recipe's name and URL using a for loop.

    # the search_recipes FUNCTION  
        # Takes an ingredient as its argument.
        # The function builds a request URL with the ingredient 
        # and sends a GET request to the Edamam API using the requests library. 
        # We then get the list of recipes from the API  we put in the status_code variable 
        # also we created a erro handling to show the status code when its not the expected one (200)

import requests
import pandas as pd
from operator import itemgetter

# API credentials
# should be hidden in a real life application
app_id = "092316d7"
app_key = "15bbc5b6b198bea8d98bca2fb9f826a9"


def search_recipes(ingredient: str, app_id: str, app_key: str) -> list:
    """
    Searches for recipes and returns the results.
    :param ingredient: ingredient to be searched for
    :param app_id: string with app id
    :param app_key: string with app key
    :return: a list of recipes (strings)
    """
    # Build the request URL with the provided ingredient
    url = f"https://api.edamam.com/search?q={ingredient}&app_id={app_id}&app_key={app_key}"

    # Send the request to the Edamam API
    response = requests.get(url)
    status_code = response.status_code

    #Get the status code for the response. Should be 200 OK
    # Which means everything worked as expected
    if status_code != 200:
        raise Exception(f"Invalid status code {status_code}")

    # Get the list of recipes from the API response
    json_results = response.json()

    return json_results["hits"]


def get_ingredient_weight(recipe: dict, ingredient: str) -> float:
    # "ingredients" is a list of dictionaries inside of "recipe"
    """ 
    Get the rounded weight of an ingredient
    """
    recipe_ingredients = recipe["recipe"]["ingredients"]

    # to access each ingredient I did a for loop.  
    for recipe_ingredient in recipe_ingredients:
        # mach the user input to the ingredient in list to know its weight
        if ingredient.lower() in recipe_ingredient["food"].lower():
            ingredient_weight = recipe_ingredient["weight"]
            return round(ingredient_weight, 2)
        else:
            # check the next ingredient
            continue

    # didn't find a match
    return 0.0

def prepare_results(ingredient:str, recipes: list) -> list: 
    """
    build results dictionary with the information to be displayed
    """
    # Create a list of dictionaries with results from search_recipes()
    result_list = []

    for recipe in recipes:
        recipe_name = recipe["recipe"]["label"]
        recipe_url = recipe["recipe"]["url"]
        ingredient_weight = get_ingredient_weight(recipe, ingredient)

        info_dict = {
            "recipe_name": "",
            "recipe_url": "",
            "input_ingredient": "", 
            "ingredient_weight": "",
        } 

        info_dict["recipe_name"] = recipe_name
        info_dict["recipe_url"] = recipe_url
        info_dict["input_ingredient"] = ingredient
        info_dict["ingredient_weight"] = ingredient_weight

        result_list.append(info_dict)

    return result_list


def display_results(items: list):
    for item in items:
        recipe_name = item["recipe_name"] 
        recipe_url = item["recipe_url"]
        ingredient = item["input_ingredient"]
        ingredient_weight = item["ingredient_weight"] 
        print(f"{recipe_name}: {recipe_url} - weight needed: {ingredient_weight}")


def run(user_input: str) -> None:
    """
    Search results
    Run the code
    Sorted results by weight
    Display results
    """
    # Search results
    recipes = search_recipes(user_input, app_id, app_key)
    # Run the code and display results
    results = prepare_results(user_input, recipes)
    # sorted results by weight
    # Source: https://stackoverflow.com/questions/72899/how-do-i-sort-a-list-of-dictionaries-by-a-value-of-the-dictionary
    sorted_results = sorted(results, key=itemgetter("ingredient_weight")) 
    display_results(sorted_results)
    convert_csv(recipes_list)


def convert_csv(recipes_list: list) -> None:
    """
    convert a list of recipes (sorted results) to CSV
    """
    df = pd.DataFrame.from_dict(recipes_list)
    df.to_csv("recipe.csv", index=False)

# Run from command line
if __name__ == "__main__":
    # Ask the user to enter an ingredient to search for
    user_input = input("Enter an ingredient to search for a recipe: ")
    # user_input = "tofu"
    run(user_input)


