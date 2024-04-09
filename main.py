from gui import *
from database import connect_to_database
def main():

   db_connection = connect_to_database()
   if db_connection is None:
       raise Exception("Failed to connect to the database.")
   home_page = create_home_page(
       open_customer_management_callback = open_customer_management_form,
       open_view_form_callback=open_view_form,
       open_search_form_callback=open_search_form,
       open_queries_form_callback= open_queries_form,
       db_connection=db_connection
   )
   home_page.mainloop()


if __name__ == "__main__":
    main()