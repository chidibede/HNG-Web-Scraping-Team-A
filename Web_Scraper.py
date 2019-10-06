#Import necessary utilities
from bs4 import BeautifulSoup as soup
from urllib.request import urlopen as uReq
import csv


filename = 'Computer_Science_Professors_and_Their_h-indices.csv'
f = open(filename, 'w')

headers = 'Name Of Professor, h-index \n'
f.write(headers)


#container = containers[0]
init_pg = 0
url = 'https://scholar.google.com/citations?view_op=search_authors&hl=en&mauthors=computer+science+professor&before_author=i-Gn_w-KAQAJ&astart=0'


while init_pg <= 240:
    #Opening up the content and grabbing the page
    uClient = uReq(url)

    #Read the Webpage
    page_html = uClient.read()

    #html parsing
    page_soup = soup(page_html, "html.parser")
    containers = page_soup.findAll("div", {"class":"gs_ai_t"})
    container = containers[0]
    #Grab Prof details on page
    for container in containers:
        prof_name = container.a.text
        prof_webpage_tag = container.a['href'].split('?')[1].split('=')[2]

        #Fetching the h-index for each Prof
        prof_page_url = 'https://scholar.google.com/citations?hl=en&user=' + prof_webpage_tag

        #Opening up the content and grabbing the page for each prof
        uClient = uReq(prof_page_url)

        #Read the Webpage
        prof_page_html = uClient.read()

        #html parsing
        prof_soup = soup(prof_page_html, "html.parser")

        prof_h_index = prof_soup.findAll('td', {'class':'gsc_rsb_std'})[2].text


        #Print out all of the names and Ids of the profs on current page
        f.write(prof_name.replace(',', '') + ',' + prof_h_index + '\n')
        print(prof_name + ',' + prof_h_index + '\n')

    #Grab the next page
    page_containers = page_soup.findAll("button", {"aria-label":"Next"})
    page_container = page_containers[0]

    nxt_pg = page_container['onclick'].split('\\')[9]

    init_pg = init_pg + 10

    url = ('https://scholar.google.com/citations?view_op=search_authors&hl=en&mauthors=computer+science+professor&after_author=' + nxt_pg[3:] +'&astart='+ str(init_pg))

    #Closing the webpage
    uClient.close()
f.close()
    #print(url)
