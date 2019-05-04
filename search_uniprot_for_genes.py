#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Sep  1 13:27:09 2018

@author: pranaydogra
"""
import pandas as pd
import smtplib

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException

# =============================================================================
# define function to extract gene information and send email upon completion
# =============================================================================
def search_genes(gene_list, tissue, out_dir, receiver):
    f= open(out_dir + "{}_gene_info.docx".format(tissue),"w+")
    for entry in searchterms:
        window_size = "1920,1080"
        chrome_options = Options()
        chrome_options.add_argument("--headless") # this enables no popup option for chrome windows
        chrome_options.add_argument("--wind-size = {}".format(window_size))
        driver = webdriver.Chrome(executable_path = "ENTER PATH TO YOUR CHROME DRIVER LOCATION",
                                  options = chrome_options)
        driver.get("https://www.uniprot.org/uniprot/")
        inputElement = driver.find_element(By.XPATH,'//*[@id="query"]')
        inputElement.send_keys(entry + ' AND organism:"Homo sapiens (Human) [9606]"')
        inputElement.send_keys(Keys.ENTER)
        driver.implicitly_wait(30)
        try:
            element = driver.find_element(By.XPATH, "//*/td[2]/a")
            driver.execute_script("arguments[0].click();", element)
            content = driver.find_element_by_tag_name("body")
            text_only = content.text
            protein = text_only[text_only.index("Feedback\nProtein") + 16 : text_only.index("\nGene")]
            if "Functioni" in text_only:
                ind1 = text_only.index('Functioni')
                if "GO - Molecular functioni" in text_only: # get molecular function information
                    ind2 = text_only.index('GO - Molecular functioni')
                elif "GO - Biological processi" in text_only:  # get biological process information
                    ind2 = text_only.index('GO - Biological processi')
                elif "Names & Taxonomyi" in text_only: # get information about the protein and gene name(s) and synonym(s)
                    ind2 = text_only.index("Names & Taxonomyi")
                function = text_only[ind1+9:ind2]
                f.write("\n{} \n".format(entry) + "Protein: " + protein + "\nFunction: " + function)
            
            else:
                f.write("\n{} \n".format(entry) + "Protein: " + protein + "No function information available")
            
        except NoSuchElementException:
            f.write("\n{} \n".format(entry) + 'No information about this gene')
        
        print("Processed information for gene: {}".format(entry))
        driver.quit()
        
    f.close()
    
    # this code below sends an email to the "customer" after the script is done running for all search terms
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.ehlo()
    user = "ENTER YOUR EMAIL ADDRESS"
    pwd = "ENTER YOUR LOGIN PASSWORD"
    
    server.login(user,pwd)
    msg = ("Gene information script for {} done running".format(tissue))
    server.sendmail(user, receiver, msg) # send email
    server.quit()
    
# =============================================================================
# call function
# =============================================================================
searchterms = []
ans = input(r"Do you have a file with list of genes (y/n): ")

if ans == 'y':
    file_path = input(r"Enter path to file with list of genes: ")
    out_path = input(r"Enter path to output directory: ")
    cust_email = input(r"Enter receiver's email address: ")
    site = file_path.split('/')[-1].replace('.csv','')
    data = pd.read_csv(file_path, header = 0)
    searchterms = data['x'].values
    search_genes(searchterms, site, out_path, cust_email)

if ans == 'n':
    out_path = input(r"Enter path to output directory: ")
    cust_email = input(r"Enter receiver's email address: ")
    searchterms = list(map(str,input(r"Enter genes names separated by space: ").split()))
    site = input("Enter tissue site: ")
    search_genes(searchterms, site, out_path,cust_email)
