import requests
from collections import defaultdict

def check_cookies(response):
    try:
        cookies = response.cookies
        domain = response.url.split('//')[1].split('/')[0]
        third_party_cookies = [cookie for cookie in cookies if cookie.domain != domain]
        return third_party_cookies
    except Exception as e:
        print("An error occurred while checking cookies:", e)
        return []

def find_external_requests(response):
    try:
        base_url = response.url.split('//')[1].split('/')[0]
        external_requests = []
        for request in response.history + [response]:
            request_url = request.url.split('//')[1].split('/')[0]
            if request_url != base_url:
                external_requests.append(request_url)
        
        return external_requests
    except Exception as e:
        print("An error occurred while finding external requests:", e)
        return []

def analyze_website(url):
    request_count=0
    thirdCookies=0
    try:
        response = requests.get(url)
        external_requests = find_external_requests(response)
        third_party_cookies = check_cookies(response)
        
        total_score = 17

        if external_requests:
            for request_url in external_requests:
                print(request_url)
                request_count+=1
                total_score -= 1 # Deduct 1 for external requests
        else:
            print("No external domain found.")
            total_score = 17
            
        if third_party_cookies:
            print("Third-party cookies found:")
            for cookie in third_party_cookies:
                print(cookie)
                thirdCookies+=1
                total_score -= 1  # Deduct 1 for third-party cookies
        else:
            print("No cookies found.")
            total_score =17
        
        # Print the final deducted score
        return total_score,request_count,thirdCookies
        
    except requests.exceptions.RequestException as e:
        print("An error occurred while fetching the URL:", e)
    except Exception as e:
        print("An unexpected error occurred:", e)
