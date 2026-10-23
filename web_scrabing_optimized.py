#Web scraping is an automated method used to extract large amounts of data from websites
#and convert it into structured formats like spreadsheets, JSON, or database


from bs4 import BeautifulSoup
import csv
from itertools import zip_longest
from playwright.sync_api import sync_playwright


job_title = []
company_name = []
location = []
skills = []
links = []
salary = []
responsibilities = []
date = []
page_number = 0
with sync_playwright() as p:
    browser = p.chromium.launch(headless=False) 
    page = browser.new_page()
    #page.wait_for_timeout(100000)  
    #src = page.content()


    while True:
        url = f"https://wuzzuf.net/search/jobs?q=python&start={page_number}&a=hpb"
        print(f"Scraping search page {page_number}")
        page.goto(url)

         
        if page_number == 0:
            print("please solve any chellenge if appears, waiting...")
            page.wait_for_timeout(100000)

        else:
            try:
                page.wait_for_selector("strong", timeout=50000)
            except:
                page.wait_for_timeout(20000)

        src = page.content()
         

        soup = BeautifulSoup(src, "lxml")
        #print(soup.title)
        page_limit = int(soup.find("strong").text)

        if( page_number > page_limit // 15):
            print("pages is ended, terminate")
            break
        #print(page_limit)


         
        

        job_titles = soup.find_all("h2", {"class": "css-s5fwzh"})
        company_names = soup.find_all("a", {"class":"css-ipsyv7"})
        locations = soup.find_all("span", {"class":"css-16x61xq"})
        job_skills = soup.find_all("div", {"class":"css-1rhj4yg"})
        posted_new = soup.find_all("div",{"class":"css-eg55jf"})
        posted_old = soup.find_all("div",{"class":"css-1jldrig"})
        posted = [*posted_new,*posted_old]


        #6th step loop over returned lists to extract needed info into other lists

        for i in range(len(job_titles)):
            job_title.append(job_titles[i].text)
            job_links = job_titles[i].find("a").attrs['href']
            full_links = "https://wuzzuf.net" + job_links
            links.append(full_links)
            company_name.append(company_names[i].text)
            location.append(locations[i].text)
            skills.append(job_skills[i].text)
            date.append(posted[i].text)



        page_number +=1
        print("page switched successfully. ")
        #print(job_title, company_name, location, skills)





    for link in links:
        page.goto(link, timeout=30000)
        src = page.content()
        soup = BeautifulSoup(src,"lxml")

        salary_found ="Not specified"
        details_blocks = soup.find_all("div",{"class":"css-1ajx53j"})
        salary_text = "Not specified"  
        for block in details_blocks:
            title_span = block.find("span",{"class":"css-720fa0"})
            if title_span and "Salary:" in title_span.text:
                val_span = block.find("span",{"class":"css-iu2m7n"})
                salary_found = val_span.text
                break
            #salaries = soup.find("span",{"class":"css-2rozun"})
        salary.append(salary_found)

        requirments = soup.find("div",{"class":"css-1lqavbg"})
        respon_text = ""
        for li in requirments.find_all("li"):
            respon_text += li.text +" | "
        respon_text = respon_text[:-2]
        responsibilities.append(respon_text)


    browser.close()



file_list = [job_title, company_name, date, location, skills, links, salary, responsibilities]
exported = zip_longest(*file_list)
with open(r"PATH OF YOUR FILE", "w", 
          encoding="utf-8", newline="",) as myfile:
    wr = csv.writer(myfile)
    wr.writerow(["job title","company name","date", "location","skills", "links", "salaries","job requirments"])
    wr.writerows(exported)

print("Data exported successfully to CSV!")
