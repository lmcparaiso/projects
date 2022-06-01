import re
import openpyxl
import pandas as pd

filename = 'HOR_orders_may2022.xlsx' #output file name

odate = list()
price = list()
cname = list()
email = list()
phone = list()
ddate = list()
dname = list()

#This is to parse the required fields Item: and Address: since they could be multiline
fhand = open('HOR_ORDERS.txt', encoding="utf8")
txt1 = fhand.read().strip()
txt = txt1.replace('Full delivery address:','Delivery Address:')
item = re.findall(r'Item:(.+?)\n\n', txt, re.DOTALL)
address = re.findall(r'Delivery Address:(.+?)\n\n', txt, re.DOTALL)


#get the order dates from the chat log date. First line of chat is included in this line need to parse separately
fhand = open('HOR_ORDERS.txt', encoding="utf8")
for lines in fhand:
    if re.search('[0-9]+/[0-9]+/[0-9]+,', lines) != None and lines.find('deleted') == -1 and lines.find('omitted') == -1:
        date = re.findall(r'([0-9]+/[0-9]+/[0-9]+),',lines)
        odate.append(date[0])
    continue

# get lines with Item: Name: Phone: Email: Delivery date: Delivery contact name:
fhand = open('HOR_ORDERS.txt', encoding="utf8")
for lines in fhand:
    if lines.find('Item:') >=0:
        p = re.findall('Item: ([0-9]+)\s', lines)
        if p == []:
            p = '0'
        price.append(p[0])
    elif lines.find('Name:') >= 0:
        name = re.findall(r'Name:(.*)', lines)
        cname.append(name[0].strip())
    elif lines.find('Email:') >= 0:
        e = re.findall(r'Email:(.*)', lines)
        email.append(e[0].strip())
    elif lines.find('Phone:') >= 0 or lines.find('Contact:') >= 0:
        lines = lines.replace('Contact:', 'Phone:')
        ph = re.findall(r'Phone:(.*)', lines)
        phone.append(ph[0].strip())
    elif lines.find('Delivery date:') >= 0:
        dd = re.findall(r'Delivery date:(.*)', lines)
        ddate.append(dd[0].strip())
    elif lines.find('Delivery contact name:') >= 0:
        dn = re.findall(r'Delivery contact name:(.*)', lines)
        dname.append(dn[0].strip())
#    elif lines.lower().find('ig @') >= 0 or lines.lower().find('viber') >= 0 or lines.lower().find('website') >= 0 or lines.lower().find('fb @') >= 0 :
#        word = lines.split()
#        print(word[0])
#        touchpoint.append(word[0])
    continue
#test
#all lists should have same number of records
print('Item:',len(item))
print('Price:',len(price))
print('Cname:',len(cname))
print('address:',len(address))
print('odate:',len(odate))
print('phone:',len(phone))
print('ddate:',len(ddate))
print('dname:',len(dname))
print('Email:',len(email))

#column names
colprice = 'price'
colitem = 'item'
colcname = 'contact_name'
coladdress = 'delivery_address'
colodate = 'order_date'
colddate = 'delivery_date'
colphone = 'phone'
colrecipient = 'recipient'
colemail = 'email'

#Output data to excel. dataframe needs to have exact number of values per list
try:
    data = pd.DataFrame({colcname:cname,colrecipient:dname,colemail:email,colphone:phone,coladdress:address,colitem:item,colprice:price,colodate:odate,colddate:ddate})
    data.to_excel(filename)
    print(filename,'has been created')
except:
    print('PROGRAM FAILED. ALL LISTS SHOULD HAVE SAME LENGTH.')
