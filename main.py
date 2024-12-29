from jaswalji import ai,crawl,scrap

jaswalji_crawl = crawl()
jaswalji_ai = ai()
jaswalji_scrap = scrap()
url_ask = str(input("Enter the website link which you want to know more about : "))

#jaswalji_crawl.find_all_links("https://botpenguin.com/contact-us")
jaswalji_crawl.find_all_links(url_ask)
user_que = ""
while user_que != "q":
    user_que = input("Ask your Question  or enter q to quit: ")
    if user_que == "q":
        break
    link_prompt = jaswalji_ai.prompt_gen_link_prob(user_que)
    link_prompt_ans = jaswalji_ai.llm_qeury(link_prompt,0.17)
    print("I think i can find your answer in this page : ")
    print(link_prompt_ans)
    #print(link_prompt_ans[0])



    ### scrap the page
    print("Scraping the "+str(link_prompt_ans)+" page data ....")
    scrap_data = jaswalji_scrap.scrap_the_site_data(link_prompt_ans)

    scrap_data_prompt = jaswalji_ai.prompt_gen_scrap_data(user_que,scrap_data)
    scrap_data_prompt_ans = jaswalji_ai.llm_qeury(scrap_data_prompt,0.17)
    print(scrap_data_prompt_ans)