# Import libraries
from urllib.request import urljoin
from bs4 import BeautifulSoup
import requests
from urllib.request import urlparse
import re
import json


# Set for storing urls with same domain
links_intern = set()
input_url = "https://www.legislation.gov.uk/ukpga/2007/15/data.xht?view=snippet&wrap=true"
links_intern.add(input_url)
# input_url = "https://www.gov.uk/standard-visitor"
# depth = 1

# Set for storing urls with different domain
# links_extern = set()
web_data = list()
pdf_urls = list()
website_count = 0
error_count = 0
checkpoint = 10000


def extract_url_data(url, input_bs4):
    result = list()
    try:
        # lang = input_bs4.find("html")["lang"].strip()
        # if(lang != "en"):
        #     raise ValueError('Not in english')
        # data['title'] = input_bs4.find("title").get_text().strip()
        # data['description'] = input_bs4.find("meta", attrs={"name": "description"})[
        #     "content"].strip()
        # data['url'] = url
        target_bs4 = input_bs4.find("div", {"id": "js-results"})
        temp_list = list()
        temp_key = "NA"
        for tag in target_bs4.find_all(["a"]):
            result.append(tag['href'])
            # if(tag.name == "span" and 'class' in tag.attrs.keys()):
            #     # print("11111111111111111111111111")
            #     class_name = str()
            #     if(isinstance(tag['class'], list)):
            #         class_name = "".join(tag['class'])
            #     else:
            #         class_name = tag['class']
                
            #     if("LegTitleBlockTitle" in class_name):
            #         text = tag.text
            #         text = text.replace("U.K.", "")
            #         text = text + ":"
            #         temp_list = list()
            #         temp_list.append(text)
            #     elif("LegPblockTitle" in class_name):
            #         text = tag.text
            #         text = text.replace("U.K.", "")
            #         text = text + ":"
            #         del temp_list[1:]
            #         temp_list.append(text)
            #     elif("LegRHS" in class_name):
            #         temp_list.append(tag.text)
            #         result[temp_key] = " ".join(temp_list)
            #     elif('id' in tag.attrs.keys() and tag['id'].startswith("schedule")):
            #         temp_key = tag['id']
            #         size = len(temp_key.split('-'))
            #         size = size-2
            #         if(size>0 and len(temp_list)>size):
            #             del temp_list[size:]
            # elif(tag.name == "p" and 'class' in tag.attrs.keys()):
                # print("3333333333333333333333333")
                # class_name = str()
                # if(isinstance(tag['class'], list)):
                #     class_name = "".join(tag['class'])
                # else:
                #     class_name = tag['class']

                # if("LegListTextStandard" in class_name):
                #     text1 = temp_list.pop()
                #     text1 = text1 + " " + tag.text
                #     temp_list.append(text1)
                #     result[temp_key] = " ".join(temp_list)
            # skip = False
            # for parent in tag.parents:
            #     if (parent.name == "li"):
            #         skip = True
            #         break

            # if (skip):
            #     continue
            # # if(para.name == "p"):
            # #     data['content'] += para.get_text() + '\n'
            # if (tag.name == "ul" or tag.name == "ol"):
            #     for index, item in enumerate(tag.find_all("li")):
            #         content += f"{index + 1}: {(' '.join(item.get_text().split())).strip()}\n"
            #     # data['content'] += tag.get_text() + '\n'
            # elif (tag.name == "p"):
            #     content += f"{(' '.join(tag.get_text().split())).strip()}\n"
            #     para_flag = True
            # else:
            #     content += f"{(' '.join(tag.get_text().split())).strip()}: "
        return result
    except Exception as err:
        print(err)
        global error_count
        error_count = error_count + 1
        print(f"Error number: {error_count}")
        return list()

def extract_pdf_urls(url, input_bs4):
    result = list()
    try:
        # lang = input_bs4.find("html")["lang"].strip()
        # if(lang != "en"):
        #     raise ValueError('Not in english')
        # data['title'] = input_bs4.find("title").get_text().strip()
        # data['description'] = input_bs4.find("meta", attrs={"name": "description"})[
        #     "content"].strip()
        # data['url'] = url
        
        target_bs4 = input_bs4.find("span", {"class": "attachment-inline"})
        print(target_bs4)
        temp_list = list()
        temp_key = "NA"
        for tag in target_bs4.find_all(["a"]):
            temp = dict()
            temp['url'] = tag['href']
            temp['name'] = tag.text
            result.append(temp)
            # if(tag.name == "span" and 'class' in tag.attrs.keys()):
            #     # print("11111111111111111111111111")
            #     class_name = str()
            #     if(isinstance(tag['class'], list)):
            #         class_name = "".join(tag['class'])
            #     else:
            #         class_name = tag['class']
                
            #     if("LegTitleBlockTitle" in class_name):
            #         text = tag.text
            #         text = text.replace("U.K.", "")
            #         text = text + ":"
            #         temp_list = list()
            #         temp_list.append(text)
            #     elif("LegPblockTitle" in class_name):
            #         text = tag.text
            #         text = text.replace("U.K.", "")
            #         text = text + ":"
            #         del temp_list[1:]
            #         temp_list.append(text)
            #     elif("LegRHS" in class_name):
            #         temp_list.append(tag.text)
            #         result[temp_key] = " ".join(temp_list)
            #     elif('id' in tag.attrs.keys() and tag['id'].startswith("schedule")):
            #         temp_key = tag['id']
            #         size = len(temp_key.split('-'))
            #         size = size-2
            #         if(size>0 and len(temp_list)>size):
            #             del temp_list[size:]
            # elif(tag.name == "p" and 'class' in tag.attrs.keys()):
                # print("3333333333333333333333333")
                # class_name = str()
                # if(isinstance(tag['class'], list)):
                #     class_name = "".join(tag['class'])
                # else:
                #     class_name = tag['class']

                # if("LegListTextStandard" in class_name):
                #     text1 = temp_list.pop()
                #     text1 = text1 + " " + tag.text
                #     temp_list.append(text1)
                #     result[temp_key] = " ".join(temp_list)
            # skip = False
            # for parent in tag.parents:
            #     if (parent.name == "li"):
            #         skip = True
            #         break

            # if (skip):
            #     continue
            # # if(para.name == "p"):
            # #     data['content'] += para.get_text() + '\n'
            # if (tag.name == "ul" or tag.name == "ol"):
            #     for index, item in enumerate(tag.find_all("li")):
            #         content += f"{index + 1}: {(' '.join(item.get_text().split())).strip()}\n"
            #     # data['content'] += tag.get_text() + '\n'
            # elif (tag.name == "p"):
            #     content += f"{(' '.join(tag.get_text().split())).strip()}\n"
            #     para_flag = True
            # else:
            #     content += f"{(' '.join(tag.get_text().split())).strip()}: "
        return result
    except Exception as err:
        print(err)
        global error_count
        error_count = error_count + 1
        print(f"Error number: {error_count}")
        return list()  
def download_pdf(url, name):
    try:
        name = name.replace("/", "-")
        if(":" in name):
            name = name.split(":")[1].strip()
        response = requests.get(url)
        if(len(response.content) < 512):
            return False
        with open(f'downloads\\{name}.pdf', 'wb') as pdf:
            pdf.write(response.content)
        return True
    except:
        print("Error")
        return False



# Method for crawling a url at next level
def level_crawler(input_url):
    temp_urls = list()
    try:
        current_url_domain = urlparse(input_url).netloc

        # Creates beautiful soup object to extract html tags
        beautiful_soup_object = BeautifulSoup(
            requests.get(input_url, verify=False).content, "lxml")
        url_data = extract_url_data(input_url, beautiful_soup_object)
        if (url_data):
            web_data.extend(url_data)

        # Access all anchor tags from input
        # url page and divide them into internal
        # and external categories
        return list()
    except:
        return list()

def level_crawler_2(input_url):
    temp_urls = list()
    try:
        current_url_domain = urlparse(input_url).netloc

        # Creates beautiful soup object to extract html tags
        beautiful_soup_object = BeautifulSoup(
            requests.get(input_url, verify=False).content, "lxml")
        url_data = extract_pdf_urls(input_url, beautiful_soup_object)
        if (url_data):
            pdf_urls.extend(url_data)

        # Access all anchor tags from input
        # url page and divide them into internal
        # and external categories
        return list()
    except:
        return list()
# if (depth == 0):
#     print("Intern - {}".format(input_url))

# elif (depth == 1):
#     level_crawler(input_url)

# else:
#     # We have used a BFS approach
#     # considering the structure as
#     # a tree. It uses a queue based
#     # approach to traverse
#     # links upto a particular depth.
#     queue = []
#     queue.append(input_url)
#     for j in range(depth):
#         for count in range(len(queue)):
#             url = queue.pop(0)
#             urls = level_crawler(url)
#             for i in urls:
#                 queue.append(i)
#             break

queue = list()
queue.append("https://www.gov.uk/administrative-appeals-tribunal-decisions?page=1&tribunal_decision_categories%5B%5D=personal-independence-payment-daily-living-activities&tribunal_decision_categories%5B%5D=personal-independence-payment-general&tribunal_decision_categories%5B%5D=personal-independence-payment-mobility-activities")
queue.append("https://www.gov.uk/administrative-appeals-tribunal-decisions?page=2&tribunal_decision_categories%5B%5D=personal-independence-payment-daily-living-activities&tribunal_decision_categories%5B%5D=personal-independence-payment-general&tribunal_decision_categories%5B%5D=personal-independence-payment-mobility-activities")
queue.append("https://www.gov.uk/administrative-appeals-tribunal-decisions?page=3&tribunal_decision_categories%5B%5D=personal-independence-payment-daily-living-activities&tribunal_decision_categories%5B%5D=personal-independence-payment-general&tribunal_decision_categories%5B%5D=personal-independence-payment-mobility-activities")
queue.append("https://www.gov.uk/administrative-appeals-tribunal-decisions?page=4&tribunal_decision_categories%5B%5D=personal-independence-payment-daily-living-activities&tribunal_decision_categories%5B%5D=personal-independence-payment-general&tribunal_decision_categories%5B%5D=personal-independence-payment-mobility-activities")
while (len(queue) > 0):
    url = queue.pop(0)
    website_count = website_count + 1
    print(f"Website count: {website_count}")
    if(website_count%checkpoint == 0):
        with open(f'section_data_{website_count/checkpoint}.json', 'w') as fout:
            json.dump(web_data, fout)
            web_data = list()
        
    queue.extend(level_crawler(url))
    print(f"Queue count: {len(queue)}")

# del web_data[0]['NA']
# web_data[0]['schedule-22-paragraph-11'] = "Compulsory purchase: consequential amendments: Postal Services Act 2000 (c. 26): In Part 2 of Schedule 5 to the Postal Services Act 2000 (acquisition of land and rights: procedure etc), in paragraph 10, for \u201csheriff's warrant\u201d there is substituted \u201c enforcement officer's or sheriff's warrant \u201d."

# valid_keys = set()
# for key in web_data[0]:
#     key_items = key.split('-')
#     key_items.pop()
#     parent_key = "-".join(key_items)
#     valid_keys.discard(parent_key)
#     valid_keys.add(key)

# final_data = dict()
# for key in valid_keys:
#     final_data[key] = web_data[0][key]
urls = list()
for item in web_data:
    urls.append("https://www.gov.uk/"+item)

with open('final_tribunals_data.json', 'w') as fout:
    json.dump(urls, fout)



print(len(urls))

for item in urls:
    level_crawler_2(item)

for item in pdf_urls:
    download_pdf(item['url'], item['name'])
# with open('section_data.txt', 'w') as fout:
#     fout.write(web_data[0]['content'])
