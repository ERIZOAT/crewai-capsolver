from selenium import webdriver
from selenium.webdriver.common.by import By
import requests
from typing import Dict, Any

def submit_recaptcha_token(driver: webdriver.Chrome, token: str):
    """
    Injects the reCAPTCHA token into the hidden textarea and submits the form.
    
    Args:
        driver: The Selenium WebDriver instance.
        token: The reCAPTCHA token string obtained from CapSolver.
    """
    try:
        # Find the hidden textarea
        recaptcha_response = driver.find_element(By.ID, "g-recaptcha-response")
        
        # Make it visible (optional, for debugging) and set the token
        driver.execute_script("arguments[0].style.display = 'block';", recaptcha_response)
        recaptcha_response.clear()
        recaptcha_response.send_keys(token)

        # Submit the form
        form = driver.find_element(By.TAG_NAME, "form")
        form.submit()
        print("Successfully injected token and submitted form.")
    except Exception as e:
        print(f"Error during reCAPTCHA token submission: {e}")


def access_protected_page_with_cf_solution(url: str, cf_solution: Dict[str, Any]) -> str:
    """
    Uses the Cloudflare Challenge solution (cookies and user_agent) 
    to access the protected page via a requests session.
    
    Args:
        url: The URL of the protected page.
        cf_solution: A dictionary containing 'cookies' (list of dicts) and 'userAgent' string.
        
    Returns:
        The HTML content of the protected page as a string.
    """
    session = requests.Session()
    
    # Set the cookies from the CapSolver solution
    for cookie in cf_solution.get("cookies", []):
        session.cookies.set(cookie["name"], cookie["value"])
    
    # Set the User-Agent that was used to solve the challenge
    headers = {
        "User-Agent": cf_solution.get("userAgent")
    }

    # Access the protected page
    response = session.get(url, headers=headers)
    
    if response.status_code == 200:
        print(f"Successfully accessed protected page: {url}")
        return response.text
    else:
        print(f"Failed to access protected page. Status code: {response.status_code}")
        return f"Error: Status code {response.status_code}"
