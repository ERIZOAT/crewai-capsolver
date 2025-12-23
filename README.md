# CrewAI CapSolver Integration: CAPTCHA Bypass Tools

[![CrewAI](https://img.shields.io/badge/CrewAI-Python%20Framework-blue?style=for-the-badge&logo=python)](https://github.com/crewAIInc/crewAI)
[![CapSolver](https://img.shields.io/badge/CapSolver-CAPTCHA%20Solver-green?style=for-the-badge)](https://www.capsolver.com/?utm_source=github&utm_medium=repo&utm_campaign=crewai-capsolver)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg?style=for-the-badge)](https://opensource.org/licenses/MIT)

## 🚀 Overview

This repository provides a set of custom **CrewAI Tools** designed to integrate with the **CapSolver API**, enabling autonomous AI agents to automatically solve various CAPTCHA challenges (reCAPTCHA, Turnstile, Cloudflare, etc.) encountered during web-based tasks.

The integration ensures your CrewAI workflows remain uninterrupted and scalable, even when dealing with protected websites.

## ✨ Features

*   **`CaptchaSolverTool`**: Generic tool for solving token-based CAPTCHAs (reCAPTCHA v2/v3, Turnstile).
*   **`CloudflareChallengeTool`**: Specialized tool for bypassing Cloudflare 5-second challenges, returning necessary cookies and User-Agent.
*   **Robust Error Handling**: Built-in polling and timeout logic for reliable task completion.

## 🛠️ Installation

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/your-username/crewai-capsolver-tools.git
    cd crewai-capsolver-tools
    ```

2.  **Install dependencies:**
    ```bash
    pip install crewai 'crewai[tools]' requests pydantic
    ```

## ⚙️ Configuration

1.  **Get your CapSolver API Key:**
    Sign up for CapSolver and obtain your API key.
    > **Tip:** Get an extra **6% bonus** on your recharge using the code **CREWAI** when you [Sign up for CapSolver here](https://www.capsolver.com/?utm_source=github&utm_medium=repo&utm_campaign=crewai-capsolver).

2.  **Set the API Key:**
    For security, it is highly recommended to set your API key as an environment variable.
    ```bash
    export CAPSOLVER_API_KEY="YOUR_CAPSOLVER_API_KEY"
    ```
    Alternatively, you can directly edit the `CAPSOLVER_API_KEY` variable in `capsolver_tools.py`.

## 💡 Usage Example

The following example demonstrates how to set up a CrewAI agent with the custom CapSolver tool and use the resulting token for a web action.

### `example_crew.py`

```python
import os
from crewai import Agent, Task, Crew, Process
from capsolver_tools import CaptchaSolverTool # Import the custom tool

# Ensure API Key is set
if not os.getenv("CAPSOLVER_API_KEY"):
    print("Error: CAPSOLVER_API_KEY environment variable not set.")
    exit()

# 1. Define the Tool
captcha_solver = CaptchaSolverTool()

# 2. Define the Agent
# The agent is given the tool and instructed on when to use it.
captcha_agent = Agent(
    role='CAPTCHA Solver Specialist',
    goal='Solve reCAPTCHA and Turnstile challenges to enable web access for other agents.',
    backstory="An expert in bypassing automated web protections using AI services.",
    tools=[captcha_solver],
    verbose=True,
    allow_delegation=False
)

# 3. Define the Task
# The agent will automatically call the tool when it sees the input schema matches its goal.
target_url = "https://www.example.com/protected-page"
site_key = "YOUR_SITE_KEY" # The data-sitekey from the target page

solve_task = Task(
    description=f"Use the captcha_solver tool to get the reCAPTCHA token for the following page: URL: {target_url}, Site Key: {site_key}. The CAPTCHA type is ReCaptchaV2TaskProxyLess.",
    agent=captcha_agent,
    expected_output="The successfully retrieved reCAPTCHA token (a long string)."
)

# 4. Create and Run the Crew
crew = Crew(
    agents=[captcha_agent],
    tasks=[solve_task],
    process=Process.sequential,
    verbose=2
)

result = crew.kickoff()
print("\n\n########################")
print("## Crew Execution Result")
print("########################")
print(result)

# The resulting token can then be used by another agent (e.g., a Web Scraper Agent) 
# to submit the form and access the protected content.
```

## 🔗 Submission Helper Functions

For completeness, here are helper functions for submitting the tokens/cookies obtained from CapSolver.

### `submission_helpers.py`

```python
from selenium import webdriver
from selenium.webdriver.common.by import By
import requests

def submit_recaptcha_token(driver: webdriver.Chrome, token: str):
    """Inject reCAPTCHA token into the hidden textarea and submit the form."""
    recaptcha_response = driver.find_element(By.ID, "g-recaptcha-response")
    driver.execute_script("arguments[0].style.display = 'block';", recaptcha_response)
    recaptcha_response.clear()
    recaptcha_response.send_keys(token)
    driver.find_element(By.TAG_NAME, "form").submit()

def access_protected_page_with_cf_solution(url: str, cf_solution: dict) -> str:
    """
    Uses the Cloudflare Challenge solution (cookies and user_agent) 
    to access the protected page via a requests session.
    """
    session = requests.Session()
    
    # Set the cookies from the CapSolver solution
    for cookie in cf_solution["cookies"]:
        session.cookies.set(cookie["name"], cookie["value"])
    
    # Set the User-Agent that was used to solve the challenge
    headers = {
        "User-Agent": cf_solution["user_agent"]
    }

    # Access the protected page
    response = session.get(url, headers=headers)
    return response.text
```

## 📚 Resources

*   [CrewAI Documentation](https://www.crewai.com/)
*   [CapSolver API Documentation](https://docs.capsolver.com/)
*   [Sign up for CapSolver (Use code **CREWAI** for 6% bonus)](https://www.capsolver.com/?utm_source=github&utm_medium=repo&utm_campaign=crewai-capsolver)
