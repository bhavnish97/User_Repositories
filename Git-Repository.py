import streamlit as st
import requests
from bs4 import BeautifulSoup
import pandas as pd
import math

st.title("Github Repository Details")

user_name = st.text_input("Enter the user name to check")

if st.button('Submit'):
    page =1

    url = "https://github.com/"+ user_name + "/?page=" + str(page) + "&tab=repositories"
    response = requests.get(url)
    html = response.content
    soup = BeautifulSoup(html, 'html.parser')

    total_repositories = soup.find('span', {'class':"Counter"})
    pages = max(1,math.ceil(int(total_repositories.text)/30))


    repositories = []
    for page in range(pages):

        url = "https://github.com/"+ user_name + "/?page=" + str(page+1) + "&tab=repositories" # generic for all pages
        response = requests.get(url)
        html = response.content
        soup = BeautifulSoup(html, 'html.parser')
        
        all_repo = soup.find_all(class_ = 'col-10 col-lg-9 d-inline-block')

        for repo in all_repo:
            repositories.append(str(repo))

    my_dict = dict({
        'repo_name':[],
        #'repo_link':[],
        'repo_description':[],
        'Repository Language':[],
        'Number of Stars':[],
        'last_updated':[]
    })
    for repo in repositories:
        if repo :
            soup1 = BeautifulSoup(repo, 'html.parser')

            # Extract the repository name
            repo_name = soup1.find("a", itemprop="name codeRepository").text
            my_dict['repo_name'].append(repo_name.split('\n')[1].replace(" ", ""))
            #my_dict['repo_link'].append("https://github.com/"+ user_name + "/?page=" + str(page+1) + "&tab=repositories")

            # Extract the repository description
            if soup1.find("p", itemprop="description") is None:
                my_dict['repo_description'].append("None")
            else:
                repo_description = soup1.find("p", itemprop="description").text
                my_dict['repo_description'].append(repo_description.split('\n')[1])
            
            # Extract the repository language
            if soup1.find("span", itemprop="programmingLanguage") is None:
                my_dict['Repository Language'].append("None")
            else:
                prog_lang = soup1.find("span", itemprop="programmingLanguage").text
                my_dict['Repository Language'].append(prog_lang)

            # Extract the number of stars
            if soup1.find("a", href="/"+user_name+"/"+repo_name.replace(" ", "").replace("\n", "")+"/stargazers") is None:
            #print("/campusx-official/"+repo_name.replace(" ", "").replace("\n", "")+"/stargazers")
                my_dict['Number of Stars'].append(str(0))
            else:
                stars = soup1.find("a", href="/"+user_name+"/"+repo_name.replace(" ", "").replace("\n", "")+"/stargazers").text
                my_dict['Number of Stars'].append(stars.replace(" ", "").replace("\n",""))

            # Extract the last updated date
            last_updated = soup1.find("relative-time").text
            my_dict['last_updated'].append(last_updated)
    repo_details = pd.DataFrame(my_dict)

    st.write(repo_details)







