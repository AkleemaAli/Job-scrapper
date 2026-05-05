import streamlit as st
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import pandas as pd
import time

st.set_page_config(page_title="Pro Job Scraper", page_icon="🔍", layout="wide")

def get_linkedin_jobs(keywords, location, exp_level):
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--disable-gpu')

    options.binary_location = "/usr/bin/chromium" 

    try:
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=options)
        
        
        search_url = f"https://www.linkedin.com/jobs/search/?keywords={keywords.replace(' ', '%20')}&location={location.replace(' ', '%20')}"
        if exp_code:
            search_url += f"&f_E={exp_code}"
        
        driver.get(search_url)
        time.sleep(5) 

        job_data = []
        
        selectors = [
            "a.base-card__full-link", 
            "a.job-search-card__alt-link", 
            ".base-search-card__title"
        ]
        
        found_elements = []
        for selector in selectors:
            found_elements = driver.find_elements(By.CSS_SELECTOR, selector)
            if found_elements:
                break

        for j in found_elements[:15]:
            try:
                title = j.text.strip()
                if not title:
                    title = j.get_attribute('innerText').strip()
                
                link = j.get_attribute('href')
                if link:
                    link = link.split('?')[0]
                
                if title and link:
                    job_data.append({"Job Title": title, "Location": location, "Link": link})
            except:
                continue
        
        driver.quit()
        return job_data
    except Exception as e:
        st.error(f"Technical Error: {e}")
        return []

st.title("🚀One Search, Infinite Opportunities.")

with st.sidebar:
    st.header("Search Filters")
    job_field = st.text_input("Job Title / Field", placeholder="Typing...")
    city = st.selectbox("Select City", ["Pakistan", "Karachi", "Lahore", "Islamabad"])
    experience = st.radio("Experience Level", ["Any"])
    search_btn = st.button("Search Jobs")

if search_btn:
    if job_field:
        with st.spinner("Connecting to LinkedIn..."):
            results = get_linkedin_jobs(job_field, city, experience)
            if results:
                st.success(f"Found {len(results)} jobs!")
                df = pd.DataFrame(results)
                st.table(df) # Simple table for testing
            else:
                st.warning("No jobs found. Try: 1. Different Keywords 2. Set Experience to 'Any' 3. Check your internet.")
    else:
        st.error("Please enter a job title.")
