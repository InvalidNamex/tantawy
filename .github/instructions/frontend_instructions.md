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
if item was used in invoiceDetails or priceListsDetails then prevent deletion
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
# CREATE OR REPLACE VIEW "itemStock" AS
SELECT 
    i.id AS id, 
    i."itemName" AS "itemName",
    i."isDeleted" AS "isDeleted",
    COALESCE(im."storeID", id."storeID") AS "storeID",  -- Derived from two tables
    COALESCE(SUM(
        CASE 
            WHEN im."invoiceType" = 1 AND im."isDeleted" = FALSE THEN id.quantity 
            ELSE 0 
        END
    ), 0) 
    - 
    COALESCE(SUM(
        CASE 
            WHEN im."invoiceType" = 2 AND im."isDeleted" = FALSE THEN id.quantity 
            ELSE 0 
        END
    ), 0) AS stock
FROM items i
LEFT JOIN "invoiceDetail" id ON i.id = id.item
LEFT JOIN "invoiceMaster" im ON id."invoiceMasterID" = im.id
GROUP BY i.id, i."itemName", i."isDeleted", COALESCE(im."storeID", id."storeID");
