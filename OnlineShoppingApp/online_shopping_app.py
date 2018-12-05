from urllib.request import urlopen
from tkinter import *
import webbrowser
from re import findall, finditer, MULTILINE, DOTALL
from sqlite3 import *

## Back end
def download(url, target_filename, filename_extension):

    # Import an exception raised when a web server denies access
    # to a document
    from urllib.error import HTTPError

    # Open the web document for reading
    try:
        web_page = urlopen(url)
    except ValueError:
        raise Exception("Download error - Cannot find document at URL '" + url + "'")
    except HTTPError:
        raise Exception("Download error - Access denied to document at URL '" + url + "'")
    except:
        raise Exception("Download error - Something went wrong when trying to download " + \
                        "the document at URL '" + url + "'")

    # Read its contents as a Unicode string
    try:
        web_page_contents = web_page.read().decode('UTF-8')
    except UnicodeDecodeError:
        raise Exception("Download error - Unable to decode document at URL '" + \
                        url + "' as Unicode text")

    # Write the contents to a local text file as Unicode
    # characters (overwriting the file if it
    # already exists)
    try:
        text_file = open(target_filename + '.' + filename_extension,
                         'w', encoding = 'UTF-8')
        text_file.write(web_page_contents)
        text_file.close()
    except:
        raise Exception("Download error - Unable to write to file '" + \
                        target_file + "'")

    # Return the downloaded document to the caller
    return web_page_contents

# Name of the invoice file
invoice_file = 'invoice.html'

# Scrape the electronics sections of amazon.com for item prices, names and
# images live from the website
amazon_electronics = download('https://www.amazon.com.au/gp/bestsellers/'\
                              + 'electronics', 'download', 'html')
# Uncomment line below and comment line above to use backup saved HTML file
#amazon_electronics = open('Amazon_electronics.html', 'U').read()
amazon_electronics_name = findall('alt="([^\"]+)"', amazon_electronics)[17:27]
amazon_electronics_price = findall("\$[0-9]+\.[0-9][0-9]", amazon_electronics)\
                           [:10]
amazon_electronics_image = findall('src="([^\"]+)"', amazon_electronics)[1:11]
amazon_electronics_list = []
for index in range(len(amazon_electronics_name)):
    amazon_electronics_list += [[amazon_electronics_price[index], \
                                 amazon_electronics_name[index], \
                                 amazon_electronics_image[index]]]

# Scrape the books section of amazon.com for item prices, names and images
# live from the website
amazon_books = download('https://www.amazon.com.au/gp/bestsellers/books',\
                        'download', 'html')
# Uncomment line below and comment line above to use backup saved HTML file
#amazon_books = open('Amazon_books.html', 'U').read()
amazon_books_name = findall('alt="([^\"]+)"', amazon_books)[17:27]
amazon_books_price = findall("\$[0-9]+\.[0-9][0-9]", amazon_books)[:10]
amazon_books_image = findall('src="([^\"]+)"', amazon_books)[1:11]
amazon_books_list = []
for index in range(len(amazon_books_name)):
    amazon_books_list += [[amazon_books_price[index], amazon_books_name[index],\
                           amazon_electronics_image[index]]]

# Scrape the clothing section of amazon.com for item prices, names and images
# from the stored HTML file
amazon_games = open('Amazon_games.html', 'U').read()
amazon_games_name = findall('alt="([^\"]+)"', amazon_games)[15:25]
amazon_games_price = findall("\$[0-9]+\.[0-9][0-9]", amazon_games)[:10]
amazon_games_image = findall('src="([^\"]+)"', amazon_games)[1:11]
amazon_games_list = []
for index in range(len(amazon_games_name)):
    amazon_games_list += [[amazon_games_price[index], amazon_games_name[index],\
                           amazon_electronics_image[index]]]

# Scrape the laptop section of amazon.com for item prices, names and images
# from the stored HTML file
amazon_movies = open('Amazon_movies.html', 'U').read()
amazon_movies_name = findall('alt="([^\"]+)"', amazon_movies)[15:25]
amazon_movies_price = findall("\$[0-9]+\.[0-9][0-9]", amazon_movies)[:10]
amazon_movies_image = findall('src="([^\"]+)"', amazon_movies)[1:11]
amazon_movies_list = []
for index in range(len(amazon_movies_name)):
    amazon_movies_list += [[amazon_movies_price[index], amazon_movies_name\
                            [index], amazon_electronics_image[index]]]


## Intermediate funcitons
# Create list to hold shopping cart items
shopping_cart_list = []
        
# Define functions to add items to shopping cart
def add_to_cart_electronics():
    try:
        option = electronics_var.get()
        shopping_cart_list.append(option)
    except:
        print('Item could not be added to cart.')
    
def add_to_cart_books():
    try:
        option = books_var.get()
        shopping_cart_list.append(option) 
    except:
        print('Item could not be added to cart.')
        
def add_to_cart_games():
    try:
        option = games_var.get()
        shopping_cart_list.append(option) 
    except:
        print('Item could not be added to cart.')           
            
def add_to_cart_movies():
    try:
        option = movies_var.get()
        shopping_cart_list.append(option)
    except:
        print('Item could not be added to cart.')

# Define a function to calculate total price from shopping cart
def calculate_total_price(list_of_prices):
        total_price_list = findall('[0-9]+\.[0-9][0-9]', str(list_of_prices))
        total_price = 0
        for number in total_price_list:
            total_price += float(number)
        total_price = round(total_price, 2)
        return(str(total_price))

# Define a function to open the URL when clicked on    
def hyperlink_electronics(event):
    webbrowser.open_new(r"https://www.amazon.com.au/gp/bestsellers/electronics")
    
def hyperlink_books(event):
    webbrowser.open_new(r"https://www.amazon.com.au/gp/bestsellers/books")
    
def hyperlink_games(event):
    webbrowser.open_new(r"https://www.amazon.com.au/gp/bestsellers/videogames")
    
def hyperlink_movies(event):
    webbrowser.open_new(r"https://www.amazon.com.au/gp/bestsellers/"\
                        + "movies-and-tv")

# Define a function to open a new window to show cart
def open_my_cart():
    try:
        # Define a function to clear the shopping cart
        def clear_cart():
            for index in range(len(shopping_cart_list)):
                del shopping_cart_list[-1]
            new_window.destroy()
        # Open new window and give it a title
        new_window = Toplevel()
        new_window.configure(bg = 'peru')
        new_window.title('Online Shopping Tool(Shopping Cart)')
        Label(new_window, text = 'My Cart', font = heading_font, fg = 'maroon',\
              bg = 'peru').pack(side = TOP, pady = 5)
        # Pack in labels and widgets in new window
        for index in shopping_cart_list:
            Label(new_window, text = index, font = text_font, fg = 'maroon',\
                  bg = 'peru', wraplength = 400).pack(padx = 10)
        Label(new_window, text = 'Total Price: $' + calculate_total_price\
              (shopping_cart_list), font = text_font, fg = 'maroon', \
              bg = 'peru').pack(pady = 10)
        Button(new_window, text = 'Purchase Items and Download Invoice',\
               font = button_font, fg = 'maroon', bg = 'peru', command =\
               download_invoice, cursor = 'hand2').pack(side = BOTTOM,\
                                                        pady = 10, padx = 10)
        Button(new_window, text = 'Clear Cart', font = button_font,\
               fg = 'maroon', bg = 'peru', command = lambda:[clear_cart(),\
                                                             open_my_cart()],\
               cursor = 'hand2').pack(side = BOTTOM)
    except:
        print('Cart could not be opened.')

# Define a function to download invoice and save it to the database
def download_invoice():
    try:
        # Download invoice to invoice.html
        invoice = ''
        for index in shopping_cart_list:
            invoice += '<li align="center">' + index + '</li>'
        invoice = '<!DOCTYPE html> <html> <head> <title>Invoice</title> '\
                        +'<style>body{background-color: peru; color: maroon;}'\
                        +'</style> </head><body><h1>Ye Olde Online Shoppe</h1>'\
                        +'<img src="penquill.gif">'\
        + '<h2> Your invoice includes the following items: </h2>'\
        + '<ol>' + invoice + '</ol> <h3> Total Price: $' + calculate_total_price\
        (shopping_cart_list) + ' (AUD)</h3> <h4>References:</h4><ol><li><a'\
        + ' href="https://www.amazon.com.au/gp/bestsellers/electronics">'\
        + 'https://www.amazon.com.au/gp/bestsellers/electronics</a></li><li>'\
        + '<a href="https://www.amazon.com.au/gp/bestsellers/books">'\
        + 'https://www.amazon.com.au/gp/bestsellers/books</a></li><li><a '\
        + 'href="https://www.amazon.com.au/gp/bestsellers/videogames">'\
        + 'https://www.amazon.com.au/gp/bestsellers/videogames</a></li><li><a '\
        + 'href="https://www.amazon.com.au/gp/bestsellers/movies-and-tv">'\
        + 'https://www.amazon.com.au/gp/bestsellers/movies-and-tv</a></li></ol>'\
        + '</body></html>'
        with open("invoice.html", "w") as file:
            file.write(invoice)
        webbrowser.open_new(r"invoice.html")
        # Save invoice to SQL database to shopping_cart.db
        connection = connect(database = 'shopping_cart.db')
        insert_items_db = connection.cursor()
        sql_statement = "DELETE FROM ShoppingCart"
        insert_items_db.execute(sql_statement)
        for product in shopping_cart_list:
            product_split = product.split(",", 1)
            item = str(findall("'(.+)'\)", product_split[1]))
            price = str(findall("\('(.+)'", product_split[0]))
            item = item.replace('[', '').replace(']', '').replace("'", '')
            price = price.replace('[', '').replace(']', '').replace("'", '')\
                    .replace('$', '')
            sql_statement_template = "INSERT INTO ShoppingCart VALUES ('ITEM', "\
                                     + "'PRICE')"
            sql_statement = sql_statement_template.replace('ITEM', item).replace\
                            ('PRICE', price)
            insert_items_db.execute(sql_statement)
        connection.commit()
        insert_items_db.close()
        connection.close()
    except:
        print('Invoice could not be downloaded.')
      
## Front End
# Create a window and frames
online_shopping = Tk()
left_frame = Frame(bg = 'peru')
right_frame = Frame(bg = 'peru')
left_frame.pack(side = LEFT)
right_frame.pack(side = RIGHT)
online_shopping.configure(bg = 'peru')

# Give the window a title
online_shopping.title('Online Shopping Tool')

# Create font types
title_font = ('Old English Text MT', 25, 'underline')
heading_font = ('Bernard MT Condensed', 18)
text_font = ('Times New Roman', 16)
button_font = ('Times New Roman', 12, 'bold')
hyperlink_font = ('Times New Roman', 12)

# Save logo as a variable
pen_quill_image = PhotoImage(file = 'penquill.gif')

# Create labels and widgets
title = Label(left_frame, text = 'Ye Olde Online Shoppe', font = title_font,\
              fg = 'maroon', bg = 'peru')
static = Label(right_frame, text = 'Static Deals', font = heading_font,\
               fg = 'maroon', bg = 'peru')
live = Label(right_frame, text = 'Live Deals', font = heading_font,\
             fg = 'maroon', bg = 'peru')
pen_quill = Label(left_frame, image = pen_quill_image, bg = 'peru')
see_cart = Button(right_frame, text = 'See Your Cart', font = button_font,\
                  fg = 'maroon', bg = 'peru', command = open_my_cart,\
                  cursor = 'hand2')
hyperlink_amazon_electronics = Label(left_frame, text =\
                                     "https://www.amazon.com.au/gp/bestsellers/"\
                                     + "electronics", font = hyperlink_font, \
                                     fg = 'blue', bg = 'peru', cursor = 'hand2')
hyperlink_amazon_electronics.bind("<Button-1>", hyperlink_electronics)
hyperlink_amazon_books = Label(left_frame, text = "https://www.amazon.com.au"\
                               +"/gp/bestsellers/books", font = hyperlink_font,\
                               fg = 'blue', bg = 'peru', cursor = 'hand2')          
hyperlink_amazon_books.bind("<Button-1>", hyperlink_books)
hyperlink_amazon_games = Label(left_frame, text = "https://www.amazon.com.au"\
                               +"/gp/bestsellers/videogames", font =\
                               hyperlink_font, fg = 'blue', bg = 'peru',\
                               cursor = 'hand2')          
hyperlink_amazon_games.bind("<Button-1>", hyperlink_games)
hyperlink_amazon_movies = Label(left_frame, text = "https://www.amazon.com.au"\
                                +"/gp/bestsellers/movies-and-tv",\
                                font = hyperlink_font, fg = 'blue', bg = 'peru'\
                                , cursor = 'hand2')          
hyperlink_amazon_movies.bind("<Button-1>", hyperlink_movies)

# Create drop down menu for Amazon electronics
electronics_var = StringVar()
try:
    choices = [amazon_electronics_list[0][:2], amazon_electronics_list[1][:2],\
               amazon_electronics_list[2][:2], amazon_electronics_list[3][:2],\
               amazon_electronics_list[4][:2], amazon_electronics_list[5][:2],\
               amazon_electronics_list[6][:2], amazon_electronics_list[7][:2],\
               amazon_electronics_list[8][:2], amazon_electronics_list[9][:2]]
    electronics_var.set('Browse Amazon: electronics')
except:
    choices = ['Item 1', 'Item 2', 'Item 3', 'Item 4', 'Item 5', 'Item 6',\
               'Item 7', 'Item 8', 'Item 9', 'Item 10']
    electronics_var.set('Item1')
amazon_electronics_menu = OptionMenu(right_frame, electronics_var, *choices)
amazon_electronics_menu.config(width = 25, cursor = 'hand2', bg = 'burlywood',\
                               fg = 'maroon')
add_to_cart_button_electronics = Button(right_frame, text = 'Add to cart',\
                                        font = button_font, fg = 'maroon',\
                                        bg = 'peru',command = \
                                        add_to_cart_electronics, cursor =\
                                        'hand2')

# Create drop down menu for Amazon books
books_var = StringVar()
try:
    choices = [amazon_books_list[0][:2], amazon_books_list[1][:2],\
               amazon_books_list[2][:2], amazon_books_list[3][:2], \
               amazon_books_list[4][:2], amazon_books_list[5][:2], \
               amazon_books_list[6][:2], amazon_books_list[7][:2], \
               amazon_books_list[8][:2], amazon_books_list[9][:2]]
    books_var.set('Browse Amazon: books')
except:
    choices = ['Item 1', 'Item 2', 'Item 3', 'Item 4', 'Item 5', 'Item 6',\
               'Item 7', 'Item 8', 'Item 9', 'Item 10']
    books_var.set('Item1')
amazon_books_menu = OptionMenu(right_frame, books_var, *choices)
amazon_books_menu.config(width= 25, cursor = 'hand2', bg = 'burlywood',\
                         fg = 'maroon')
add_to_cart_button_books = Button(right_frame, text = 'Add to cart', font =\
                                  button_font, fg = 'maroon', bg = 'peru',\
                                  command = add_to_cart_books, cursor = 'hand2')

# Create drop down menu for Amazon games
games_var = StringVar()
try:
    choices = [amazon_games_list[0][:2], amazon_games_list[1][:2],\
               amazon_games_list[2][:2], amazon_games_list[3][:2],\
               amazon_games_list[4][:2], amazon_games_list[5][:2],\
               amazon_games_list[6][:2], amazon_games_list[7][:2],\
               amazon_games_list[8][:2], amazon_games_list[9][:2]]
    games_var.set('Browse Amazon: games')
except:
    choices = ['Item 1', 'Item 2', 'Item 3', 'Item 4', 'Item 5', 'Item 6',\
               'Item 7', 'Item 8', 'Item 9', 'Item 10']
    games_var.set('Item1')
amazon_games_menu = OptionMenu(right_frame, games_var, *choices)
amazon_games_menu.config(width= 25, cursor = 'hand2', bg = 'burlywood',\
                         fg = 'maroon')
add_to_cart_button_games = Button(right_frame, text = 'Add to cart', font =\
                                  button_font, fg = 'maroon', bg = 'peru',\
                                  command = add_to_cart_games, cursor = 'hand2')

# Create drop down menu for Amazon movies
movies_var = StringVar()
try:
    choices = [amazon_movies_list[0][:2], amazon_movies_list[1][:2],\
               amazon_movies_list[2][:2], amazon_movies_list[3][:2],\
               amazon_movies_list[4][:2], amazon_movies_list[5][:2],\
               amazon_movies_list[6][:2], amazon_movies_list[7][:2],\
               amazon_movies_list[8][:2], amazon_movies_list[9][:2]]
    movies_var.set('Browse Amazon: movies')
except:
    choices = ['Item 1', 'Item 2', 'Item 3', 'Item 4', 'Item 5', 'Item 6',\
               'Item 7', 'Item 8', 'Item 9', 'Item 10']
    movies_var.set('Item1')
amazon_movies_menu = OptionMenu(right_frame, movies_var, *choices)
amazon_movies_menu.config(width= 25,  cursor = 'hand2', bg = 'burlywood',\
                          fg = 'maroon')
add_to_cart_button_movies = Button(right_frame, text = 'Add to cart', font =\
                                   button_font, fg = 'maroon', bg = 'peru',\
                                   command = add_to_cart_movies,\
                                   cursor = 'hand2')

# Pack widgets in the left frame
title.pack(pady = 5, padx = 10)
pen_quill.pack(pady = 10, padx = 10)
hyperlink_amazon_electronics.pack()
hyperlink_amazon_books.pack()
hyperlink_amazon_games.pack()
hyperlink_amazon_movies.pack()

# Place widgits in a grid in the right frame
live.grid(column = 1, row = 2, pady = 5)
amazon_electronics_menu.grid(column = 1, row = 3, padx = 10)
add_to_cart_button_electronics.grid(column = 2, row = 3, padx = 10)
amazon_books_menu.grid(column = 1, row = 4, padx = 10)
add_to_cart_button_books.grid(column = 2, row = 4, pady = 10)
static.grid(column = 1, row = 5, pady = 5)
amazon_games_menu.grid(column = 1, row = 6, padx = 10)
add_to_cart_button_games.grid(column = 2, row = 6, padx = 10)
amazon_movies_menu.grid(column = 1, row = 7, padx = 10)
add_to_cart_button_movies.grid(column = 2, row = 7, pady = 10)
see_cart.grid(column = 1, row = 8, pady = 10)

# Start the event loop
online_shopping.mainloop()

