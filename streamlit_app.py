# Import python packages
import streamlit as st
from snowflake.snowpark.functions import col

# Write directly to the app
st.title(":cup_with_straw: Customize Your Smoothie! :cup_with_straw:")
st.write(
        """Choose the fruits you want in your custom Smoothie!"
        """)


name_on_order = st.text_input('Name on Smoothie')
st.write('The name on your Smoothiee will be', name_on_order)

cnx = st.connection("snowflake", type="snowflake")
session = cnx.session()

#session = get_active_session()
my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'))
#st.dataframe(data=my_dataframe, use_container_width=True)
#editable_df = st.data_editor(my_dataframe)


ingredients_list = st.multiselect(
    'Choose up to 5 ingredients:'
    ,my_dataframe
    )

ingredients_string = ''   
if ingredients_list: 
    
   for fruit_chosen in ingredients_list:
       ingredients_string += fruit_chosen +' '
       #st.subheader(fruit_chosen + 'Nuitrition Information')
       
#st.write(ingredients_string)

my_insert_stmt = f"""INSERT INTO smoothies.public.orders (ingredients, name_on_order, order_filled) 
                     VALUES ('{ingredients_string}', '{name_on_order}', FALSE)"""

           
#st.write(my_insert_stmt)
time_to_insert=st.button('Submit Order')

#st.stop()

if time_to_insert:
   session.sql(my_insert_stmt).collect()    
   st.success('Your Smoothie is ordered! ✅')

#st.subheader("Pending Orders")
#pending_orders = session.table("smoothies.public.orders").filter(col("ORDER_FILLED") == False).collect()
#st.dataframe(pending_orders)

import requests
smoothiefroot_response = requests.get("https://my.smoothiefroot.com/api/fruit/watermelon")
sf_df=st.dataframe(data=smoothiefroot_response.json(), use_container_width=True)
