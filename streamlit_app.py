# Import python packages
import streamlit as st
# from snowflake.snowpark.context import get_active_session
from snowflake.snowpark.functions import col
import requests
import pandas as pd
# Write directly to the app
st.title(":cup_with_straw: Customize your smoothie! :cup_with_straw:")
st.write(
    """ **Choose the fruits you want in your custom Smoothie!**
    """
)


# import streamlit as st
title = ''
title = st.text_input("""**Name of Smoothie:** """ )
st.write(""" **The name of your Smoothie will be:** """, title)

# *.snowflakeapp
cnx = st.connection("snowflake")
session = cnx.session()
my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'))
# st.dataframe(data=my_dataframe, use_container_width=True)

Ingredients_list = st.multiselect(
    """ **Choose upto 5 Ingredients:** """
    , my_dataframe
    ,max_selections=5
    
)

if Ingredients_list:
   # st.write(Ingredients_list)
   # st.text(Ingredients_list) 

   Ingredients_string = ''

   for fruit_chosen in Ingredients_list:
       Ingredients_string += fruit_chosen + ' '
       st.subheader(fruit_chosen + ' ' + 'Nutrition_Information')
       fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + fruit_chosen)
       fv_df = st.dataframe(data=fruityvice_response.json(), use_container_width=True)
       

   # st.write(Ingredients_string)


   my_insert_stmt = """ insert into smoothies.public.orders(ingredients,name_on_order)
            values ('""" + Ingredients_string + """','""" + title + """' )"""

   # st.write(my_insert_stmt)
   # st.stop()

   time_to_insert =st.button('Submit Order')

   if time_to_insert:
        session.sql(my_insert_stmt).collect()
        st.success('Your Smoothie is ordered!', icon="✅")
