import requests
from bs4 import BeautifulSoup

def test_authentication(url):
    authen=False
    try:
        # Send a GET request to a protected endpoint
        response = requests.get(url)
        
        # Check the response status code
        if response.status_code == 401:
            authen=True
            print("Authentication is required. The website has an authentication process.")
        elif response.status_code == 200:
            print("No authentication required. The website does not have an authentication process.")
        else:
            print("Unexpected response status code:", response.status_code)
    except requests.exceptions.RequestException as e:
        print("An error occurred:", e)

    return authen

def analyze_authentication_layers(url):
    authen_header=False
    try:
        # Send a GET request to the specified URL
        response = requests.get(url)
        
        # Check for authentication-related headers
        if 'WWW-Authenticate' in response.headers:
            authen_header=True
            print("The website requires authentication.")
            # You can further analyze the contents of the 'WWW-Authenticate' header
            # to gather information about the authentication mechanism.
        else:
            print("No authentication headers found. The website may not require authentication.")
    except requests.exceptions.RequestException as e:
        print("An error occurred:", e)

    return authen_header


def check_authentication_meta_tags(url):
    authen_meta=False
    try:

        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for HTTP errors
        
        # Parse the HTML content of the response
        soup = BeautifulSoup(response.content, 'html.parser')
        
        meta_tags = soup.find_all('meta')
        
        # Check for meta tags containing authentication-related information
        authentication_meta_tags = [tag for tag in meta_tags if 'authentication' in tag.get('name', '').lower()]
        
        # Print the authentication-related meta tags
        if authentication_meta_tags:
            print("Authentication-related meta tags found:")
            for tag in authentication_meta_tags:
                print(tag)
            authen_meta=True
        else:
            print("No authentication-related meta tags found.")

        return authen_meta
        
    except requests.exceptions.RequestException as e:
        print("An error occurred while fetching the URL:", e)
    except Exception as e:
        print("An error occurred:", e)


def check_authorization_meta_tags(url):
    authorization_meta_tags = []  # set a default value
    author=False

    try:
        # Send a GET request to the URL to fetch the HTML content
        response = requests.get(url)
        response.raise_for_status()

        # Parse the HTML content using BeautifulSoup
        soup = BeautifulSoup(response.content, 'html.parser')

        authorization_meta_tags = soup.find_all('meta', attrs={'name': 'authorization'})

        # Check if any authorization meta tags were found
        if authorization_meta_tags:
            print("Authorization meta tags found:")
            for tag in authorization_meta_tags:
                print(tag)
            author=True
        else:
            print("No authorization meta tags found")

    except requests.exceptions.RequestException as e:
        print("An error occurred while fetching the webpage:", e)
    except Exception as e:
        print("An error occurred:", e)
    
    return authorization_meta_tags,author

def calculate_authentication_score(url):
    auth_score = 17

    # Test authentication | Analyze authentication layers
    auth_required = test_authentication(url)
    auth_layers=analyze_authentication_layers(url)
    if (auth_required or auth_layers != True) and auth_score>0:
        auth_score -= 12

    # Check authorization meta tags
    authorization_meta_tags = check_authorization_meta_tags(url)[0]
    num_auth_tags = len(authorization_meta_tags)
    if num_auth_tags == 0:
        auth_score -= 5

    return auth_score
