Instructions for the frontend web.
Base instructions to follow with each request:
1- language is Arabic.
2- Web style is white background with green accent and shades according to your liking.
3- Find the logo of this buiseness in tantawy/media/logo.png.
4- If you are uncertain, ask questions and do not fill the gaps yourself.
5- Follow instructions with extreme percession, after execution review the prompts to verify you did not lose context down the road.

A. Login Screen
B. Home Screen (Dashboard)
C. Pricelists Management
    - A search bar for pricelists
    - List of pricelists by ID, Name, Who created it, last update, a button to edit
    (if user has permission) allowing for updating the name, also a button to delete pricelist if it is not referenced in pricelistDetail table and the user has the right permission.
    The list has sorting by name or id feature.
    - A button to add a new price list if user has permission.
D. StoreGroups Management
    - A search bar for store groups
    - List of store groups by ID, Name,  Who created it, last update, a button to edit
    (if user has permission) allowing for updating the name, also a button to delete store group if it is not referenced in stores table and the user has the right permission.
    - A button to add a new store group if user has permission.
E. Stores
    - A search bar for stores
    - List of stores by ID,StoreGroup name, Name, Who created it, last update, a button to edit
    (if user has permission) allowing for updating the name, also a button to delete pricelist if it is not referenced in invoiceMaster table and the user has the right permission.
    - A button to add a new store group if user has permission.
    Note: Adding or updating stores there shall be a drop down to choose which store group this store is a child of, which is optional and can be left empty. have the drop down be searchable by any part of the store group name.
F. Item Management
- A search bar for items by any part of the word with drop down
- List of items ID, ItemName, Update, Delete (according to user permission)
if item was used in invoiceDetails then prevent deletion, but allow deletion if only bound to priceListsDetails
- A button to add a new item which opens a pop up dialog allowing the user to input itemName, sign, choose pricelist from drop down, then set price and binding it to this pricelist in the (priceListsDetails) table.
- A save button to save this item this dismiss the pop up dialog.
* choosing pricelist, setting price, selecting items group is all optional in creation and updating.
- When an item in the List of items is tapped it opens a new page
The page has the item name in the title of the page
followed by three tabs as a tabbar 
First tab: is called الرئيسية 
it contains options such as whether the item is in use or not
and it handles item units (check the item model) unit name, unit pack and bar code.
Second tab: is called قوائم الاسعار, it has a list of all price lists and a corresponding fields to display prices or edit them if user has permission, save the insert/update to database when enter is pressed or the save button.
Third tab:is called المخازن :
It displays a list of stores and the amount of the item in the corresponding store
Create a view in data base similar to this and read the stock of each item in each store from.

G. ItemsGroups Management
    - A search bar for items groups
    - List of Items groups by ID, Name,  Who created it, last update, a button to edit
    (if user has permission) allowing for updating the name, also a button to delete Items group if it is not referenced in items table and the user has the right permission.
    - A button to add a new Items group if user has permission.

H. Customer/Vendor Management
    - This section would be separated in 2 one for managing Customers and the other for managing Vendors, even though they are similar except for one column in the model, but for sake of ease we will split them in the view.
    - When Customer Management or Vendor Management is clicked we will navigate to a new page, the page will display a search bar where the user can search by customer/vendor using any part of their name.
    - List of customers/vendors by ID, Name, Phone 1, Phone 2 Notes
    (if user has permission) allowing for updating the model, also a button to delete customers/vendors if it is not referenced in transactions table or invoiceMaster table and the user has the right permission.
    - to be continued

# We need to create a table, model, etc called customerVendorPriceList.
# In this table we will join the customerVendorID with a priceList id to set a default pricelist for a customer/vendor
    - in the add new customer/vendor or in the update/edit customer/vendor add a dropdown holding pricelists so the user with correct permissions could bind a pricelist to this customer/vendor

I. Invoices Management (Purchase, Sales, Return Purchase, Return Sales):
1- add to the website the following
Invoice management,
it has 4 sections 
> View Purchase invoices
> View Sales invoices
> View Return Purchase invoices
> View Return Sales invoices
in each screen of the above a list of invoices sortable and filterable
. ID
. Net Total
. Notes
. Vendor/Customer based on the nature of invoice
. Created By
. Created On
We can filter by Date picker from/to dates, invoice id, the user who created it (id, user name)

# Agent management
Check the agent table and the logic we've created for it
1- create an Agent management tile in the dashboard.
2- when the tile is clicked we're taking to Agent management page where a staff user can add, view, edit and delete Agents.
3- a staff can set the password for the agent as this is ERP system and that Agents don't create their own accounts.
4- when agent name is tapped for view, display all transactions made by him in table transactions if his id exists in agentuserid_id