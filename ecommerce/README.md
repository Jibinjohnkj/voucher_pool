# Voucher Pool
A simple Voucher management system based on Django

Prerequisite
------------
Docker must be installed

Installation
------------
Run the follwing commands in your terminal
>docker pull jibinjohnkj/voucher_pool
>
>docker run -d --name voucher_pool -p 8000:8000 jibinjohnkj/voucher_pool

Open http://127.0.0.1:8000/ in your rest client(Postman) and try the following APIs


APIs
----

Create a customer

>POST /customer/
>
>{ "first_name": "Jibin", "last_name": "John", "email":
>"jibinjohn@gmail.com" }

Create a special offer
>POST /offer/
>
>{
>    "name": "Christmas Discount",
>    "discount": 50
>}

Generate Voucher Code for each customer for a given Special Offer and expiration data
>POST /generate_vouchers/
>
>{
>	"offer":"Christmas Discount",
>	"expiration":"2022-01-01"
>}

For a given Email return all its valid Voucher Codes with the Name of the Special Offer
>GET /voucher/?jibinjohn@gmail.com&format=json

Provide an endpoint, which receives a Voucher Code and Email and validates the Voucher Code. In Case it is valid, return the Percentage Discount and set the date of usage
>GET /discount/?code=68PV8N99&email=jibinjohn@gmail.com&format=json




