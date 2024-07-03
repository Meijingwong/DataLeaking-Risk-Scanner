import requests
from bs4 import BeautifulSoup

s = requests.Session()
s.headers["User-Agent"] = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"

def get_forms(url):
    soup = BeautifulSoup(s.get(url).content, "html.parser")
    return soup.find_all("form")

def form_details(form):
    detailsOfForm = {}
    action = form.attrs.get("action")
    method = form.attrs.get("method", "get")
    inputs = []

    for input_tag in form.find_all("input"):
        input_type = input_tag.attrs.get("type", "text")
        input_name = input_tag.attrs.get("name")
        input_value = input_tag.attrs.get("value", "")
        inputs.append({
            "type": input_type, 
            "name" : input_name,
            "value" : input_value,
        })
        
    detailsOfForm['action'] = action
    detailsOfForm['method'] = method
    detailsOfForm['inputs'] = inputs
    return detailsOfForm

def vulnerable(response):
    errors = {"quoted string not properly terminated", 
              "unclosed quotation mark after charachter string",
              "you have an error in you SQL syntax" 
             }
    for error in errors:
        if error in response.content.decode().lower():
            return True
    return False

def sql_injection_scan(urlToBeChecked):
    forms = get_forms(urlToBeChecked)
    print(f"[+] Detected {len(forms)} forms on {urlToBeChecked}.")
    
    sqlScore = 17  # set sqlScore=0
    
    for form in forms:
        details = form_details(form)
        
        for i in "\"'":
            data = {}
            for input_tag in details["inputs"]:
                if input_tag["type"] == "hidden" or input_tag["value"]:
                    data[input_tag['name']] = input_tag["value"] + i
                elif input_tag["type"] != "submit":
                    data[input_tag['name']] = f"test{i}"
    
            form_details(form)

            # Make the request with modified input data
            # to avoid res has no value
            res = None
            try:
                if details["method"] == "post":
                    res = s.post(urlToBeChecked, data=data)
                elif details["method"] == "get":
                    res = s.get(urlToBeChecked, params=data)
            except Exception as e:
                print(f"Error occurred during request: {e}")

            if res is not None:
                if vulnerable(res) and sqlScore>0:
                    print("SQL injection attack vulnerability in link: ", urlToBeChecked)
                    sqlScore -= 12
                else:
                    print("No SQL injection attack vulnerability detected")
                    break
    
    return sqlScore
