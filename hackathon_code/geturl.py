import requests

def scan_url(url):
    error=False
    try:
        response = requests.get(url)
        if response.status_code == 200:
            print("URL is accessible and returns a 200 OK status code.")
            # Optionally, you can analyze the response content here
            # For example, check for specific keywords or patterns in the HTML content
        else:
            print(f"URL is accessible but returns a {response.status_code} status code.")
    except requests.exceptions.RequestException as e:
        print("Error:", e)
        error=True
        return error

def clickjack(url):
    bool_array = [False, False,False,False,False,False,False]
    clickjackScore=0
    try:
        response = requests.get(url)
        if "Strict-Transport-Security" in response.headers:
            bool_array[0]= True
            clickjackScore+=2
        if "X-Content-Type-Options" in response.headers:
            bool_array[1]= True
            clickjackScore+=2
        if "Content-Security-Policy" in response.headers:
            bool_array[2]= True
            clickjackScore+=2
        if "X-Frame-Options" in response.headers:
            bool_array[3]= True
            clickjackScore+=2
        if "X-XSS-Protection" in response.headers:
            bool_array[4]= True
            clickjackScore+=2
        if "Referrer-Policy" in response.headers:
            bool_array[5]= True
            clickjackScore+=2
        if "Feature-policy" in response.headers:
            bool_array[6]= True
            clickjackScore+=2
        
    except requests.RequestException as e:
        print("Error making HTTP request:", e)

    return bool_array,clickjackScore
