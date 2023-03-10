import json

# def extractCategories():
categoriesArray=[]

# We open the file
with open('products.json', 'r') as f:
    data = json.JSONDecoder().decode(f.read())

    for obj in data:
        if obj["category"] not in categoriesArray:
            categoriesArray.append(obj["category"])

new_json = json.dumps(categoriesArray)
# print(new_json)

# write the output to a file
file_obj = open("categories.json", "w")
file_obj.write(new_json)

