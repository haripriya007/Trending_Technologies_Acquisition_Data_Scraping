#Scrap Index.co Site
# __author__ = 'Harimsv007'
import locale
import re
from urllib.request import urlopen as uReq
from bs4 import BeautifulSoup as soup
locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')
file = "input.txt" # need to create an input file
f = open(file, "r")
text = f.read()
TechnologyCount = 1
with open("input.txt") as f: # open an input file
    for line in f:
        url = line
        url_split = line.split('timeline?stream=investments&page=')
        Title_url = url_split[0] + "investments"
        print("TechnologyCount : " + str(TechnologyCount))
        TechnologyCount += 1
        uclient = uReq(Title_url)
        page_html = uclient.read()
        uclient.close()
        page_soup = soup(page_html, "html.parser")
        title = page_soup.h1.text
        title1 = (title + str("(#01_06_2019 - 09_09_2019#)") + str(".csv"))  # CHECK AND CHANGE (#01_06_2019 - 09_09_2019#) Enter the date start to end
        print(title1)
        filename = title1
        f1 = open(filename, "w")
        # headers = "Category,CompanyName,FundingAmount,FundingSeries,FoundedDate,InvestmentUrl,location,AcquiredLink,Investors,AcquiredDescription,InvestmentDescription\n"
        # headers = "DATE","COMPANY NAME","COUNTRY","BUSINESS MODEL","FOUNDED YEAR","RAISED AMOUNT","FUNDING AMOUNT","SERIES","INVESTORS","FEATURES","FEATURE's LINK"
        headers = "Category,DATE,COMPANY,NAME,COUNTRY,BUSINESS MODEL,FOUNDED YEAR,RAISED AMOUNT,FUNDING AMOUNT,SERIES,INVESTORS,FEATURES,FEATURE's LINK\n"
        f1.write(headers)
        page_no = 1
        exit = 0
        page_count = 0
        Break = 0
        while page_count < page_no:
            if Break == 1:
                break
            url = url.strip()
            my_url = (url + str(page_count))
            print(my_url)
            print("Page Count :", page_count)

            uclient = uReq(my_url)
            page_html = uclient.read()
            uclient.close()
            page_soup = soup(page_html, "html.parser")
            containers = page_soup.findAll("div", {"class": "c_timeline-row u_hoverFab"})
            for container in containers:
                date_container = container.findAll("div", {"class": "c_timeline-row-time-time"})
                date = date_container[0].text.strip()
                DATE = date.replace("\n", "").replace("", "").replace("'", "")
                Date_string = DATE.replace("Jan", "01").replace("Feb", "02").replace("Mar", "03").replace("Apr","04").replace(
                "May", "05").replace("Jun", "06").replace("Jul", "07").replace("Aug", "08").replace("Sep",
                "09").replace("Oct", "10").replace("Nov", "11").replace("Dec", "12").replace("", "")
                Date_check = Date_string[4:8] + Date_string[2:4] + Date_string[0:2]
                if int(Date_check) <= 20190531: # till date to Current date
                    Break = 1
                    break
                else:
                    print("DATE  :", DATE)
                company_name_container = container.findAll("div", {"class": "c_identityTransaction-name"})
                company = company_name_container[0].text.strip()
                print("CompanyName :" + company)
                Funding_amount = container.findAll("div", {"class": "c_identityTransaction-title"})
                if 0 < len(Funding_amount):
                    F_amount = Funding_amount[0].string.strip()
                #Currency Conversion Starting
                    currsplit = {'sympol': '',
                                 'curr_value': ''
                                 }
                    def split_currency(tex):
                        _, currency, num = re.split('^(\D+)', tex, 1)
                        num = locale.atoi(num)
                        return currency, num
                    answer = (split_currency(F_amount))
                    sympol = answer[0]
                    curr_value =str(answer[1])
                    if sympol == '$':
                        result = curr_value * 1
                        print("FundingAmount :" + '$',result)
                        #print("FundingAmount :", '$',result)
                    elif sympol == 'CAD $':
                        result = (curr_value * int(0.76))
                        print("FundingAmount :" + result)
                       # amount = '$' + 'result'
                        #print("FundingAmount :", '$',result)
                    elif sympol == '₹':
                        result = curr_value * int(0.014)
                        print("FundingAmount :" + result)
                        #print("FundingAmount :", '$',result)
                    elif sympol == '€':
                        result = (curr_value * int(1.10))
                        print("FundingAmount :" + result)
                        #print("FundingAmount :", '$',result)
                    elif sympol == '£':
                        result =(curr_value * int(0.061))
                        print("FundingAmount :" + result)
                        #print("FundingAmount :", '$',result)
                    elif sympol == 'YEN ¥':
                        result = (curr_value * int(0.0094))
                        print("FundingAmount :" + result)
                        #print("FundingAmount :", '$',result)
                    elif sympol == 'AUD $':
                        result = (curr_value * int(0.68))
                        print("FundingAmount :" + result)
                        #print("FundingAmount :", '$',result)
                    else:
                        result = ""
                #    amount = '$' + 'result'
                #    '${:,.2f}'.format(1234.5)
                else:
                    result = ""

                Funding_series = container.findAll("div", {"class": "c_identityTransaction-subtitle"})
                series = Funding_series[0].string.strip()
                if Funding_series is None:
                    print(",")
                else:
                    print("FundingSeries :" + series)
                Investment_company_url = container.findAll("a", {"data-tooltip-wrap": "false"})
                InvestmentUrl = Investment_company_url[0].get('href')
                print("InvestmentUrl :" + InvestmentUrl)

                Features_Description = container.findAll("h2", {"class": "c_uiTitleHeadline"})
                if 0 < len(Features_Description):
                    Features = Features_Description[0].string.strip()
                    print("Features :" + Features)
                else:
                    print("Features :"+"")

                uclient1 = uReq(InvestmentUrl)
                page_html1 = uclient1.read()
                page_soup1 = soup(page_html1, "html.parser")
                Raised_Founded_Type = 0
                Founded = ""
                Raised = ""
                Type = ""
                match_all = page_soup1.findAll("div", {"class": "c_identityHighlights"})
                #print("matchall---------/n",match_all[0],"/n-------")
                for match_all_items in match_all:
                    matchdiv = match_all_items.findAll("strong", {"class": "c_identityHead"})
                    #print("--------------",matchdiv)
                    for m in matchdiv:
                    #print("itertaio :",m)
                        matchhead = match_all_items.find_all("strong", {"class": "c_identityHead"})
                        list(matchhead.children)
                        print(list)
                        FoundedYear = matchhead.text.strip()
                        print(FoundedYear)
                        if FoundedYear =='Founded':
                           Founded_details = match_all.div.find("\n","")
                           print(Founded_details)
                        else:
                            print("None")
                           # elif busines_model[0].span.text == " B2c":
                            # businesmodel = busines_model[0].span.text
                            # print("BusinesModel :"+ businesmodel)
                    Raised_Founded_Type += 1
                    #print("-------------",matchhead)
                    match = match_all_items.findAll("strong",{"class":"c_identityHead"})
                    print(match)
                    for mat in match:
                        print(mat)
                        Found = mat.text.strip()
                        print(Found)
                        if Found == 'Founded':
                            FoundedYear = match_all_items.findAll("div")
                            print(FoundedYear)
                    #for FoundedYear in Found:
                        #Founded_Year = FoundedYear[0].text.strip()
                        #if Founded_Year == 'Founded':
                          #  print(Founded_Year)
                        #else:
                         #   print("")
                 #print(match,"hi")
                    if match == 'Founded':
                        match_element = match_all.findAll("div").text
                #  match = "Founded"
                        print(match_element)
                    else:
                        match_element = ""

                Locationcontainers = page_soup1.findAll("div", {"class": "c_uiTitleSub"})
                Location_Container_Count = 0
                Location = ""
                for LocationContainer in Locationcontainers:
                    LocationCheck = LocationContainer.text.strip()
                    if LocationCheck == "Location":
                        AcquiredCompanyLocation = page_soup1.findAll("div", {"class": "c_identityDashboardContent"})
                        AcquiredLocation = AcquiredCompanyLocation[Location_Container_Count].findAll("div",
                                                                                                     {"class": "c_uiTitle"})
                        CompanyLocation = AcquiredLocation[0].text.strip()
                        location = CompanyLocation.replace("", "").replace("\xa0\n", "").replace("'", "").replace("\n","")
                        state = False
                        for i in range(len(location)):
                            if location[i] == ",":
                                print(location[i])
                                Location = location[i + 1:]
                                state = True
                                break
                            if not state:
                                Location = location
                        print("AcquiredCompanyLocation :", Location)
                    Location_Container_Count += 1
                featureLink = container.findAll("a", {"class": "c_articleCard"})
                print(len(featureLink))
                if 0 < len(featureLink):
                    feature_link = featureLink[0].get('href')
                    print("AcquiredLink :" + feature_link)
                else:
                    feature_link = ""
                category = title
                print("Category :" + category)
                
               # AcquiredDescription = page_soup1.findAll("div", {"class": "c_identity-info-stats"})
                #AcqDescription = AcquiredDescription[0].text
               # if AcqDescription is None:
                  #  print(",")
                #else:
                 #   print("Acquired Description :", AcqDescription)
            page_count = page_count + 1
    print("Done")
    f.close()
print("Finished")
