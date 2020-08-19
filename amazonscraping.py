from urllib.request import urlopen as uReq
from bs4 import BeautifulSoup as soup
my_url = 'https://www.amazon.com.br/s?k=iphone&ref=nb_sb_noss'
#open connection & grab page

uClient = uReq(my_url,timeout=3)

page_html = uClient.read()
uClient.close()
#html parser
page_soup = soup(page_html, "html.parser")
content = page_soup.find("div",{"class":"s-main-slot s-result-list s-search-results sg-row"}) 
#product area
products = content.findAll("div",{"class":"sg-col-4-of-24 sg-col-4-of-12 sg-col-4-of-36 s-result-item s-asin sg-col-4-of-28 sg-col-4-of-16 sg-col sg-col-4-of-20 sg-col-4-of-32"})
#open file
filename = "iphones.csv"
f = open(filename, "w")
headers = "product_name, price\n"
f.write(headers)
#foreach products
count = 1
for prod in products:
    print('\n-----------------------------------------------------\n') 
    print(count)
    print("\n")
    count = count + 1   
    prod_col = prod.find("div",{"class":"sg-col-inner"})
    prod_span = prod_col.find("span",{"class":"celwidget slot=MAIN template=SEARCH_RESULTS widgetId=search-results"}) 
    prod_div = prod_span.div #s-expand-height s-include-content-margin s-border-bottom s-latency-cf-section
    prod_info = prod_div.div #a-section a-spacing-medium

    prod_name_div = prod_info.find("div", {"class":"a-section a-spacing-none a-spacing-top-small"})
    prod_name_h2 = prod_name_div.h2 
    prod_name = prod_name_h2.a.span
    name = prod_name.text

    prod_price_top_small = prod_info.findAll("div",{"class":"a-section a-spacing-none a-spacing-top-small"})
    print('\nQuantidade de Top-small: '+str(len(prod_price_top_small))+'\n')
    prod_price_top_mini = prod_info.find("div", {"class":"a-section a-spacing-none a-spacing-top-mini"})
    print(prod_price_top_mini)
    if len(prod_price_top_small) > 1:
        print('\nTem mais de 1 top-small\n')
        price_small = prod_price_top_small[1].div.find("span",{"class":"a-offscreen"})
        price = price_small.text
    elif prod_price_top_mini:
        print('\nTem pelo menos 1 top-mini\n')
        price_mini = prod_price_top_mini.div.find("span",{"class":"a-color-base"})
        price = price_mini.text
    else:
        price = 'SEM PRECO'
    
    print('\nProduto: '+name+' Preco: '+price) 
    f.write(name.replace(","," | ") + ","+ price.replace(",",".") + "\n")
f.close()