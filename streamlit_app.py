# Import python packages
import streamlit as st
from snowflake.snowpark.functions import col
import requests

# Write directly to the app
st.title(":tropical_drink: Customize your Smoothie! :tropical_drink:")
st.write(
    """This is an app for customizing your own smoothie!
    """
)

cnx = st.connection("snowflake")
session = cnx.session()

ingredients = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'))
#st.dataframe(data=ingredients, use_container_width=True)
name = st.text_input('Enter your name here: ')
ingredient_list = st.multiselect(
                                'Choose up to 5 ingredients', 
                                ingredients,
                                max_selections=5)

if ingredient_list:

    ingredient_string = ''

    for ingredient in ingredient_list:
        ingredient_string += ingredient + ' '
        st.subheader(ingredient + 'Nutrition Information')
        fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + ingredient)
        fv_df = st.dataframe(data = fruityvice_response.json(), use_container_width = True)
    #st.write(ingredient_string)

    my_insert_stmt = """ insert into smoothies.public.orders(ingredients, name_on_order)
                values ('""" + ingredient_string + """', '""" + name + """')"""

    time_to_insert = st.button('Submit Order')

    if time_to_insert:
        session.sql(my_insert_stmt).collect()
        
        st.success('Your Smoothie is ordered, ' + name + "!", icon="✅")




















