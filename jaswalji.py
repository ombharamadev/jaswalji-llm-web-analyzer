import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse, urljoin
from collections import deque
import random
import json

class ai:
    def __init__(self):
        pass

    def prompt_gen_link_prob(self,ques):
        link_read_file = open("internal_links.txt","r")
        link_data = link_read_file.read()
        prompt = """
hey i have a website 

and all the link which webiste have are given  below 
"""+str(link_data)+"""

the User Question is : """+str(ques)+"""

so which page you think that most probably that connects the answer of the user question 
give output in url,  only one url if you  not found any thing then append the base url only
and do not expalin any thing

"""
        return prompt





    def prompt_gen_scrap_data(self,ques,website_data):
         
        prompt = """
hey this is the website content : 

"""+str(website_data)+"""

the User Question is : """+str(ques)+"""

so you need to tell the relavent info to the user
do not explain to much and give answer to the point 

"""
        return prompt

    def llm_qeury(self,prompt,temp):
      
        api_url = "https://api.groq.com/openai/v1/chat/completions"
        api_keys = [
            "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",
            "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",
            "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"
        ]

       
        api_key = random.choice(api_keys)
        
        messages = [
            {
                "role": "user",
                "content": prompt
            }
        ]

        
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}"
        }

        
        data = {
            "model": "llama3-8b-8192",  # Model name
            "messages": messages,
            "temperature":int(temp),
        }

       
        response = requests.post(api_url, headers=headers, json=data)
        #print(response)
        #print(response.text)
        
        if response.status_code == 200:
            result = response.json()  

            
            llm_ans = result['choices'][0]['message']['content'].strip()
            return llm_ans


class scrap:
    def __init__(self):
        pass
    
    
    def fetch_website_data(self,url):
        
        header = {
            "User-Agent":"Jaswaljii"
        }
        response = requests.get(url,headers=header)
        
        
        if response.status_code != 200:
            print(f"Error: Unable to fetch the website (status code: {response.status_code})")
            return None
        
     
        soup = BeautifulSoup(response.text, 'html.parser')
        
       
        paragraphs = soup.find_all('p')
        text_content = " ".join([para.get_text() for para in paragraphs])
        
        return text_content

    def scrap_the_site_data(self,url):
        website_data = self.fetch_website_data(url)
        return website_data

class crawl:
    def __init__(self):
        pass

   
    def get_internal_links(self,url, base_domain, visited):
        internal_links = []

        response = requests.get(url)
        
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            links = soup.find_all('a', href=True)
            
            for link in links:
                href = link['href']
                full_url = urljoin(url, href)  
                
              
                if base_domain in full_url and full_url not in visited:
                    internal_links.append(full_url)
                    visited.add(full_url)
        else:
            print(f"Failed to retrieve the page: {url}")
        
        return internal_links

  
    def crawl_website(self,start_url):
    
        parsed_url = urlparse(start_url)
        base_domain = f'{parsed_url.scheme}://{parsed_url.netloc}'
        
        
        visited = set()
   
        to_visit = deque([start_url])
        
       
        all_internal_links = []
        
   
        while to_visit:
            current_url = to_visit.popleft()
            if current_url not in visited:
                visited.add(current_url)
                print(f"Crawling: {current_url}")
                
              
                internal_links = self.get_internal_links(current_url, base_domain, visited)
                
           
                all_internal_links.extend(internal_links)
                to_visit.extend(internal_links)
        
        return all_internal_links

    
    def find_all_links(self,url):
      
        start_url = url  

   
        internal_links = self.crawl_website(start_url)
        internal_links.append(url)


        with open('internal_links.txt', 'w') as file:
            for link in internal_links:
                file.write(link + '\n')
        print(f"Found {len(internal_links)} internal links.")