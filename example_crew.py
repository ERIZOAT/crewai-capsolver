import os
from crewai import Agent, Task, Crew, Process
from capsolver_tools import CaptchaSolverTool # Import the custom tool

# --- Configuration ---
# NOTE: This example assumes CAPSOLVER_API_KEY is set in your environment
# export CAPSOLVER_API_KEY="YOUR_CAPSOLVER_API_KEY"

if not os.getenv("CAPSOLVER_API_KEY"):
    print("Error: CAPSOLVER_API_KEY environment variable not set.")
    print("Please set the environment variable or update capsolver_tools.py.")
    exit()

# --- Crew Setup ---

# 1. Define the Tool
# The tool is instantiated and ready to be used by the agent.
captcha_solver = CaptchaSolverTool()

# 2. Define the Agent
captcha_agent = Agent(
    role='CAPTCHA Solver Specialist',
    goal='Solve reCAPTCHA and Turnstile challenges to enable web access for other agents.',
    backstory="An expert in bypassing automated web protections using AI services.",
    tools=[captcha_solver],
    verbose=True,
    allow_delegation=False
)

# 3. Define the Task
# This task instructs the agent to use its tool to solve a specific CAPTCHA.
# Replace with your actual target URL and site key.
TARGET_URL = "https://www.example.com/protected-page"
SITE_KEY = "YOUR_SITE_KEY" 

solve_task = Task(
    description=f"""
    Use the 'captcha_solver' tool to obtain the reCAPTCHA token for the following page.
    - URL: {TARGET_URL}
    - Site Key: {SITE_KEY}
    - CAPTCHA Type: ReCaptchaV2TaskProxyLess
    """,
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

print("--- Starting Crew Execution ---")
try:
    result = crew.kickoff()
    print("\n\n########################")
    print("## Crew Execution Result")
    print("########################")
    print(f"Solved CAPTCHA Token: {result}")
    
    # In a real scenario, you would pass this token to another agent 
    # (e.g., a Web Scraper Agent) to complete the form submission.

except Exception as e:
    print(f"\n\n--- Crew Execution Failed ---")
    print(f"An error occurred: {e}")
    print("Please check your CapSolver API Key and the task parameters.")
