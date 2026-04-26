import streamlit as st
import requests
import os
import json
import streamlit.components.v1 as components

st.set_page_config(page_title="Onboarding Assistant", layout="wide")

st.title("Onboarding Assistant Dashboard")
st.write("AI-powered documentation consistency checker")

st.header("Upload Repository")

# Upload zip file
uploaded_file = st.file_uploader("Upload your repository (.zip)", type=["zip"])

# Session state
if "scan_result" not in st.session_state:
    st.session_state.scan_result = None

API_URL = os.getenv("BACKEND_URL", "http://localhost:8000")

# Run Scan
if st.button("Run Scan"):
    if not uploaded_file:
        st.error("Please upload a repository zip file first.")
    else:
        with st.spinner("Uploading and scanning repository..."):
            try:
                files = {
                    "file": (uploaded_file.name, uploaded_file, "application/zip")
                }

                response = requests.post(
                    f"{API_URL}/api/scan",
                    files=files
                )

                if response.status_code == 200:
                    data = response.json()
                    st.session_state.scan_result = data
                    st.success(f"Scan complete: {data['total_files']} files analyzed.")
                else:
                    st.error(f"Backend error: {response.status_code}")
                    st.text(response.text)

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

                # Browser-side copy avoids server clipboard limitations.
                copy_payload = json.dumps(generated_value)
                components.html(
                        f"""
                        <button id=\"copy-btn\" style=\"padding: 8px 12px; border: 1px solid #c7c7c7; border-radius: 6px; background: white; cursor: pointer;\">Copy generated README</button>
                        <span id=\"copy-status\" style=\"margin-left: 8px; font-size: 13px; color: #2f855a;\"></span>
                        <script>
                            const textToCopy = {copy_payload};
                            const button = document.getElementById('copy-btn');
                            const status = document.getElementById('copy-status');
                            button.onclick = async () => {{
                                try {{
                                    await navigator.clipboard.writeText(textToCopy);
                                    status.textContent = 'Copied';
                                    setTimeout(() => status.textContent = '', 1500);
                                }} catch (err) {{
                                    status.textContent = 'Copy failed';
                                }}
                            }};
                        </script>
                        """,
                        height=48,
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
