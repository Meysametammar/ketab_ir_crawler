from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time
import urllib.request
import sqlite3

connection = sqlite3.connect('bookdatabase.db')
cursor = connection.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS book 
(bookId int PRIMARY KEY AUTO_INCREMENT , bookName VARCHAR , ISBN VARCHAR , subjects VARCHAR , creator VARCHAR , publisher VARCHAR , deweyCode  varchar , languageBook VARCHAR , description VARCHAR )
""")
idCode = 1
I = 2
driver = webdriver.Chrome()
while I <= 1000:
    driver.get(f'https://db.ketab.ir/bookview.aspx?bookid={I}')

    # find book name :

    bookname = driver.find_element_by_xpath('//*[@id="ctl00_ContentPlaceHolder1_lblBookTitle"]').text
    print(bookname)

    if not bookname == "Label":

        # find ISBN :
        ISBN = ''
        ISBN += driver.find_element_by_xpath('//*[@id="ctl00_ContentPlaceHolder1_lblISBN"]').text
        if not ISBN == " ISBN: ":
            ISBN += ' '
            ISBN = ISBN[6:-1:1]
        else:
            ISBN = ""

        print(ISBN)


        # find subjects list :

        subjectsListUncorrect = []
        subjectsListCorrect = []
        try:
            subjectsListUncorrect = driver.find_element_by_xpath('//*[@id="ctl00_ContentPlaceHolder1_rptSubject"]').text.split("\n")

            for x in subjectsListUncorrect:
                strReturn = ''
                text_text = x.split('\u200c')
                for y in text_text:
                    strReturn += y
                subjectsListCorrect.append(strReturn)
        except:
            pass

        print(subjectsListCorrect)
        subjects = ""
        u = 0
        while u <= len(subjectsListCorrect)-1:
            subjects += subjectsListCorrect[u]
            if u != len(subjectsListCorrect)-1:
                subjects += "_"
            u += 1
        print(subjects)
        # find creators list :

        creatorListUncorrect = []
        creatorListCorrect = []
        try:
            creatorListUncorrect = driver.find_element_by_xpath('//*[@id="ctl00_ContentPlaceHolder1_rptAuthor"]').text.split('\n')
            for x in creatorListUncorrect:
                strReturn2 = ''
                text_text = x.split('\u200c')
                for y in text_text:
                    strReturn2 += y
                    strReturn2 += " "

                creatorListCorrect.append(strReturn2[0:-1])

        except:
            pass
        print(creatorListCorrect)
        creators = ""

        p = 0
        while p <= len(creatorListCorrect)-1:
            creators += creatorListCorrect[p]
            if p != len(creatorListCorrect)-1:
                creators += "_"
            p += 1
        # find publishers list :

        publishersList = []
        i = 0

        while i <= 10:
            try:
                publishersList.append(driver.find_element_by_xpath(f'//*[@id="ctl00_ContentPlaceHolder1_rptPublisher_ctl0{i}_HyperLink2"]').text)
            except:
                break
            i += 1

        print(publishersList)
        publishers = ""
        z = 0
        while z <= len(publishersList)-1:
            publishers += publishersList[z]
            if z != len(publishersList)-1:
                publishers += "_"
            z += 1
        # find Dewey code :
        deweyCode = ''
        try :
            deweyCode += driver.find_element_by_xpath('//*[@id="ctl00_ContentPlaceHolder1_lblDoe"]/a').text
        except:
            pass
        print(deweyCode)

        # find language book :
        languageBook = ''
        try:
            languageBook += driver.find_element_by_xpath('//*[@id="ctl00_ContentPlaceHolder1_Labellang"]/a').text
        except:
            pass
        print(languageBook)

        # find description book :
        listDescription = ['','']
        uncorrectDescription = driver.find_element_by_xpath('//*[@id="aspnetForm"]/div[4]/div/div/div/div[2]/div/div[3]/p[2]').text
        if not uncorrectDescription == "معرفی مختصر كتاب":
            listDescription = uncorrectDescription.split("\n")

        try:
            img = driver.find_element_by_xpath('//*[@id="ctl00_ContentPlaceHolder1_imgBook"]')
            src = img.get_attribute('src')
            urllib.request.urlretrieve(src, f"pictures/{I}.png")
        except:
            pass

        cursor.execute("INSERT INTO book VALUES (? , ? , ? , ? , ? , ? , ? , ? , ?)",(idCode, bookname, ISBN, subjects, creators, publishers, deweyCode, languageBook , listDescription[1]))
        idCode += 1
    else:
        pass
    I += 1

connection.commit()
connection.close()