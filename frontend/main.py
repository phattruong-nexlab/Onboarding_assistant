import streamlit as st
import requests
import os
import tkinter as tk
from tkinter import filedialog
from dotenv import load_dotenv

# Calculate path to the root .env file
env_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "../.env")
load_dotenv(env_path)

st.set_page_config(page_title="Onboarding Assistant", layout="wide")

st.title("Onboarding Assistant Dashboard")
st.write("Welcome to the AI-powered documentation consistency checker.")

st.header("Scan Repository")

# Initialize session state for directory path
if "repo_path" not in st.session_state:
    st.session_state.repo_path = "./"
if "scan_result" not in st.session_state:
    st.session_state.scan_result = None

col1, col2 = st.columns([4, 1])
with col1:
    repo_path = st.text_input("Repository Path", value=st.session_state.repo_path)
    st.session_state.repo_path = repo_path

with col2:
    st.write("") # Add spacing to align with input box
    st.write("")
    if st.button("📁 Browse Folder"):
        # Open a local folder picker dialog using Tkinter
        root = tk.Tk()
        root.attributes('-topmost', True)
        root.withdraw()
        folder_path = filedialog.askdirectory(master=root)
        root.destroy()
        if folder_path:
            st.session_state.repo_path = folder_path
            st.rerun()

if st.button("Run Scan"):
    with st.spinner("Scanning codebase and generating README preview..."):
        try:
            API_URL = os.getenv("BACKEND_URL", "http://localhost:8000")
            response = requests.post(f"{API_URL}/api/scan", json={"repo_path": repo_path})
            
            if response.status_code == 200:
                data = response.json()
                st.session_state.scan_result = data
                st.success(f"Scan complete: {data['total_files']} source files analyzed.")
            else:
                st.error(f"Error connecting to backend API: {response.status_code}")
                try:
                    st.json(response.json())
                except Exception:
                    pass
        except Exception as e:
            st.error(f"Connection error: {e}")

if st.session_state.scan_result:
    st.header("README Comparison")
    st.caption("Left: current README.md | Right: generated README preview")

    left_col, right_col = st.columns(2)
    with left_col:
        st.subheader("Current README.md")
        st.text_area(
            "Current README",
            value=st.session_state.scan_result.get("current_readme", ""),
            height=500,
            key="current_readme_view",
            disabled=True,
            label_visibility="collapsed",
        )

    with right_col:
        st.subheader("Generated README.md")
        generated_value = st.text_area(
            "Generated README",
            value=st.session_state.scan_result.get("generated_readme", ""),
            height=500,
            key="generated_readme_edit",
            label_visibility="collapsed",
        )

    st.write("Details:")
    st.json(
        {
            "repo_path": st.session_state.scan_result.get("repo_path"),
            "readme_path": st.session_state.scan_result.get("readme_path"),
            "total_files": st.session_state.scan_result.get("total_files"),
            "details": st.session_state.scan_result.get("details", []),
        }
    )

    if st.button("✅ Update README at path"):
        with st.spinner("Writing generated README to file..."):
            try:
                API_URL = os.getenv("BACKEND_URL", "http://localhost:8000")
                payload = {
                    "repo_path": st.session_state.scan_result.get("repo_path"),
                    "generated_readme": generated_value,
                }
                response = requests.post(f"{API_URL}/api/update_readme", json=payload)

                if response.status_code == 200:
                    data = response.json()
                    st.success("README.md has been updated successfully.")
                    st.json(data)
                else:
                    st.error(f"Failed to update README. Backend responded with: {response.status_code}")
                    try:
                        st.json(response.json())
                    except Exception:
                        pass
            except Exception as e:
                st.error(f"Connection error: {e}")
