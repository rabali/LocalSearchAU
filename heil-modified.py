import re, csv, string
from bs4 import BeautifulSoup

import requests

# GET THE LIST OF THE CATEGORIES RESULTS

UPPER = string.ascii_uppercase[2:]
for upper in UPPER:
    listsCat = requests.get("http://www.localsearch.com.au/Categories/List_"+upper).content
    listsoup = BeautifulSoup(listsCat, 'html.parser')

    urls_Cat = []
    print("processing categories...")
    for h in listsoup.find_all("ul", {"class": "list-unstyled"}):
        li = h.find_all('li')
        for number1 in li:
            a = number1.findChildren().pop()
            urls_Cat.append("http://www.localsearch.com.au/Categories/" + a['href'])


    # print(urls_Cat)
    with open('categories_'+upper+'.csv', 'a') as csvfile:
        spamwriter = csv.writer(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL, lineterminator="\n")
        spamwriter.writerow(urls_Cat)



    # GET THE LOCATION LIST FOR ALL THE CATEGORIES
    urls_Loc = []
    for count, l in enumerate(urls_Cat):
        listsLoc = requests.get(l).content
        locsoup = BeautifulSoup(listsLoc, 'html.parser')

        for rows in locsoup.find_all("div", {"class": "list-of-markets"}):
            for division in rows.find_all('div'):
                for unlist in division('ul'):
                    for regions in unlist('li'):
                        koko = regions.findChildren('a').pop()
                        urls_Loc.append("http://www.localsearch.com.au/" + koko['href'])


    with open('DataLinks_'+upper+'.csv', 'a') as csvfile:
        spamwriter = csv.writer(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL, lineterminator="\n")
        spamwriter.writerow(urls_Loc)

    # GET THE PAGE WITH FINAL RESULTS
    for kount, iop in enumerate(urls_Loc):
        print("Address which is scraped " + urls_Loc[kount])
        page = requests.get(urls_Loc[kount]).content
        soup = BeautifulSoup(page, 'html.parser')

        with open('eggs'+upper+'.csv', 'a') as csvfile:
            spamwriter = csv.writer(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL, lineterminator="\n")

            titledata = []
            addressdata = []
            phonedata = []
            emaildata = []
            websitedata = []

            kopok = soup.find_all(class_="business")
            for comp in kopok:
                try:
                    ytdn = comp.find_all("span", {"itemprop": "telephone"})
                except IndexError:
                    ytdn = "null"

                phonenum = []
                for itemm in ytdn:
                    phonenum.append(itemm.text)
                phonedata.append(phonenum)

            ji = soup.find_all(class_="quick-links")  # to get email and website into the tree
            for whole in ji:
                child = whole.findChildren()

                for quicknum, kkkk in enumerate(child):
                    try:
                        jio1 = kkkk.find_all("link", {"itemprop": "email"}).pop()['href']
                    except IndexError:
                        jio1 = 'null'
                    try:
                        jio2 = kkkk.find_all("link", {"itemprop": "url"}).pop()['href']
                    except IndexError:
                        jio2 = 'null'
                    emaildata.append(jio1)
                    websitedata.append(jio2)

            for title in soup.find_all("h3", {"itemprop": "name"}):
                titledata.append(title.text)

            for address in soup.find_all("address", {"itemprop": "location"}):
                addressdata.append(address.text)



                # for email in soup.find_all("link", {"itemprop": "email"}):
                #     fhfdf = email['href'][7:]
                #     emaildata.append(fhfdf)
                #
                # for website in soup.find_all("link", {"itemprop": "url"}):
                #     print(website['href'])
                #     print(website.parent.parent)
                #     websitedata.append(website['href'])


                # child = whole.findChildren()
                # numberchild = len(child)
                # print("------=====" + str(numberchild) + "=====-----------")
                # print(child)
                # for website, kkkk in enumerate(child):
                #     print(kkkk)
                #
                #     # check for empty strings, if any
                #     try:
                #         url = kkkk.findChildren()
                #     except IndexError:
                #         url = 'null'
                #
                #     if url == 'null':
                #         print("null")
                #     else:
                #         print(url)

            for ikor in range(0, min(len(titledata), len(addressdata), len(emaildata), len(websitedata))):
                spamwriter.writerow([titledata[ikor],
                                     iop,
                                     addressdata[ikor],
                                     phonedata[ikor],
                                     emaildata[ikor],
                                     websitedata[ikor]])



    #
    # print("------------------------------------")
    #
    # for open_time in soup.find_all(class_="qihours"):
    #     print(open_time.text)

    '''

    for more_tags in soup.find_all("span"):
        print(more_tags.text)

    '''
