Visits as a concept is designed to track agents as they go on their track.

First: we will create a table called visits.
the model will have columns (id, "transType" int, "customerVendor" int, "date", "latitude", "longitude", "agentID" int, "notes" text)

Second: create a post request
Third: create a /agents/manage/ view (html body main#main-content.main-content div.container div.row.mb-4 div.col-lg-8 div.glass-card div.glass-card-body)
create a tile next to others call it "زيارات"
when clicked it shows a display view it has a filter by date, customer, transaction type (1= sales, 2= return sales, 3= receive voucher, 4= pay voucher)
then in the tile or row itself
(html body main#main-content.main-content div.container div#data-sections.row.mt-4 div.col-12 div.glass-card div.glass-card-body div#return-sales-section.data-section div.table-responsive table.table.table-hover tbody#returns-table-body tr)
place the row as following (id, date, customername, notes, then an Icon of an eye when clicked it opens a map with longitude and latitude diplaying position of the visit)

