import xml.etree.ElementTree as ET
def getDataTasteline(soup):
    # This will get special data from tastline pages

    #Name
    try:
        name = soup.find("h1", class_="md:u-text-4xl u-text-4xl u-mb-2v u-order-first").text
        ingred  = soup.find_all("li", class_="Ingredient u-contents")

        recept = {
                "name":name
            }
        ingr_out=[]
        for ing in ingred:
            print("############")
            ingrequnt = ing.find("span", class_="Ingredient-quantity").attrs
            ingr = ing.find("span", class_="Ingredient-name").attrs
            ingrname = ing.find("span", class_="Ingredient-name").text
            ingre={
                "name": ingrname,
                "quant": ingrequnt,
                "ingre": ingr

            }

            ingr_out.append(ingre)
        recept['ingr']=ingr_out
        print(recept)



        return recept
    except:
        return {'recept':'no data'}