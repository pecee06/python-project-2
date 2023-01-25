import pandas as pd
import matplotlib.pyplot as plt

df_collections = pd.read_csv('Collections.csv')

df_users = pd.read_csv('Users.csv')

df_refurbished = pd.read_csv('Refurbished.csv')

df_order = pd.read_csv('Order.csv')

def donate():
    # Taking inputs
    i_serial = 1 + len(df_collections)
    i_category = input('Item category {Book/Notebook} : ')
    i_name = input('Item name {Followed by its serial number} : ')
    i_type = input('Item type : ')
    i_price = float(input('Price : '))
    i_quantity = int(input('Quantity : '))
    i_condition = input('Condition {Fit/Needs mending/Unfit} : ')

    # Writing the data into DataFrame
    l1 = [i_serial,i_category,i_name,i_type,i_price,i_quantity,i_condition]
    n = df_collections['S.no.'].count()   # n is defined here to append data one after the other in the DataFrame
    df_collections.loc[n] = l1
    df_collections.to_csv('Collections.csv',index=False)   # Appending data into CSV file

def manage():
    print('__________Availibility__________')
    print(df_collections)
    print('________________________________________________________________________')

    if df_collections.empty is False:   # Code only runs if this condition is True
        
        i_ID = input('ItemID : ')

        df1 = df_refurbished.loc[df_refurbished['ItemID']==i_ID]    # That Series of df_refurbished whose ItemID is equal to given input
        
        if df1.empty:
            i_ID_unique = i_ID

        else:
            while(df1.empty is False):  # Ensuring unique IDs
                print('Reinput a valid ID')
                i_ID = input('ItemID : ')
                i_ID1 = i_ID
            i_ID_unique = i_ID1

        i_name = input('Item name {Followed by its serial number} : ')

        while(i_name not in list(df_collections['Item name'])): # Ensuring valid Item names
            print('This item is not Available')
            i_name = input('Item name {Followed by its serial number} : ')

        df2 = df_collections.loc[df_collections['Item name']==i_name]   # That Series of df_collections whose Item name is equal to given input

        if df2['Condition'].values == 'Unfit':  # Taking pre-given conditions into consideration
            i_category = 'Paper bag'

        else:
            i_category = input('Category {Book/Notebook} : ')
        
        i_quantity = int(input('Quantity : '))

        if df2['Quantity'].values >= i_quantity:

            i_quantity_actual = i_quantity

            q = df2['Quantity'].values  # Upadating one file due to change in other
            q = q-i_quantity_actual
            df_collections.at[df2.index,'Quantity'] = q
            df_collections.to_csv('Collections.csv',index=False)

        else:

            while(df2['Quantity'].values < i_quantity): # Ensuring valid Quantity input
                print('Reinput a valid Quantity')
                i_quantity = int(input('Quantity : '))
                i_quantity1 = i_quantity

            i_quantity_actual = i_quantity1

            q = df2['Quantity'].values  # Upadating one file due to change in other
            q = q-i_quantity_actual
            df_collections.at[df2.index,'Quantity'] = q
            df_collections.to_csv('Collections.csv',index=False)

        l2 = [i_ID_unique,i_name,i_category,i_quantity_actual]

        n = len(df_refurbished) # Another way to define n
        df_refurbished.loc[n] = l2
        df_refurbished.to_csv('Refurbished.csv',index=False)

        print('________________________________________________________________________')

    else:
        quit()          
     
def login():
    i_user = input('Enter Username : ')
    i_pwd = input('Password : ')
    l3 = [i_user,i_pwd]
    for (row,rowSeries) in df_users.iterrows():
        if l3 == list(rowSeries):
            manage()
        elif l3 != list(rowSeries):
            print('Invalid Username or Password')

def order():
    print('-------------------------Stock-------------------------')
    print(df_refurbished)
    print('________________________________________________________________________')

    if df_refurbished.empty is False:

        i_category = input('Category : ')

        if i_category in list(df_refurbished['Item category']):
            i_category_correct = i_category
        else:
            while i_category not in list(df_refurbished['Item category']):
                print('Enter an available category')
                i_category = input('Category : ')
            i_category_correct = i_category
    
        i_name = input('Item name : ')

        if i_name in list(df_refurbished['Item name']):
            i_name_correct = i_name
        else:
            while i_name not in list(df_refurbished['Item name']):
                print('Not Available!!')
                i_name = input('Item name : ')
            i_name_correct = i_name
    
        df1 = df_refurbished.loc[df_refurbished['Item name']==i_name_correct]    # That Series of df_refurbished whose Item name is equal to given input

        i_quantity = int(input('Quantity : '))

        if df1['Quantity'].values >= i_quantity:
        
            i_quantity_actual = i_quantity

            q = df1['Quantity'].values  # Upadating one file due to change in other
            q = q-i_quantity_actual
            df_refurbished.at[df1.index,'Quantity'] = q
            df_refurbished.to_csv('Refurbished.csv',index=False)
    
        else:
            while df1['Quantity'].values < i_quantity:
                print('Out of Stock')
                i_quantity = int(input('Quantity : '))

            i_quantity_actual = i_quantity

            q = df1['Quantity'].values  # Upadating one file due to change in other
            q = q-i_quantity_actual
            df_refurbished.at[df1.index,'Quantity'] = q
            df_refurbished.to_csv('Refurbished.csv',index=False)
    
        df2 = df_collections.loc[df_collections['Item name']==i_name_correct]

        price = (df2['Price {per unit}'].values)/2
        if df2['Item category'].values == 'Paper bag':
                price_value = 15
        else:
            for j in price:
                price_value = j
        total = (price_value*i_quantity_actual)//1    # Making sure total is an integer

        l = [i_category_correct,i_name_correct,i_quantity_actual,total]
        n = len(df_order)
        df_order.loc[n] = l
        df_order.to_csv('Order.csv',index=False)

        print('________________________________________________________________________')
    
    else:
        quit()

def collect_graph():
    x = df_collections['Item name']
    y = df_collections['Quantity']
    plt.bar(x,y)
    plt.xlabel('Items')
    plt.ylabel('Collected')
    plt.legend(["Collections' Data"])
    plt.show()

def refurb_graph():
    x = df_refurbished['Item name']
    y = df_refurbished['Quantity']
    plt.bar(x,y)
    plt.xlabel('Items')
    plt.ylabel('Refurbished')
    plt.legend(['Refurbished Items'])
    plt.show()

def sales_graph():
    x = df_order['Item name']
    y = df_order['Quantity']
    plt.bar(x,y)
    plt.xlabel('Items')
    plt.ylabel('Sold')
    plt.legend(["Sales' Data"])
    plt.show()

while True:

    print('__________________________________________________________________________')
    print('------------------------------------Welcome to BookWorm Club-------------------------------------')
    print('__________________________________________________________________________')

    print('D--> Donate')
    print('M--> Manage')
    print('O--> Order')
    print('G--> Graphs')
    print('E--> Close Program')

    i1 = input('Enter your choice : ')

    if i1 == 'D':
        print('__________________________________________')
        print('----------------------Donation Pane----------------------')
        print('__________________________________________')
        donate()
        print('Successfully Donated!!')
        print('Thank You')

    elif i1 == 'M':
        print('_________________________________________')
        print('-------------------Management Pane-------------------')
        print('_________________________________________')
        login()

    elif i1 == 'O':
        print('__________________________________________')
        print('----------------------Buy your Stuff----------------------')
        print('__________________________________________')
        order()
        print('Pay Cash at the Counter')
        print('Thank You')
    
    elif i1 == 'G':
        print('-----------Available Plots-----------')
        print('C--> Items collected')
        print('R--> Items refurbished')
        print('S--> Sales')
        i2 = input('Enter your choice : ')
        
        if i2 == 'C':
            collect_graph()
            
        elif i2 == 'R':
            refurb_graph()
            
        elif i2 == 'S':
            sales_graph()
            
        else:
            print('Thank You')
            quit()

    elif i1 == 'E':
        break

    else:
        print('Thank You')
        quit()

quit()
