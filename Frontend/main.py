import streamlit as st
import requests

BASE_URL = "http://127.0.0.1:9000"  # FastAPI backend
 
print("Streamlit app started")

st.set_page_config(page_title="AI Contract Drafter", layout="wide")

# --- HEADER ---
st.title("📑 AI Contract Drafter")
st.markdown("Professional contract drafting, compliance checking, and summarization powered by AI.")

# --- SIDEBAR for Navigation ---
st.sidebar.header("Navigation")
page = st.sidebar.radio("Go to:", ["Project Details", "Draft Contract", "Compliance Check", "Summary & Export"])

# --- SESSION STATE ---
if "session_id" not in st.session_state:
    st.session_state.session_id = None
if "draft" not in st.session_state:
    st.session_state.draft = None
if "compliance" not in st.session_state:
    st.session_state.compliance = None
if "summary" not in st.session_state:
    st.session_state.summary = None


# --- PAGE 1: Project Details ---
if page == "Project Details":
    st.subheader("📝 Enter Project Details")

    with st.form("project_form"):
        company_name = st.text_input("Company Name")
        project_name = st.text_input("Project Name")
        scope = st.text_area("Project Scope / Requirements", height=120)
        tools = st.text_input("Preferred Tools/Tech Stack")
        duration = st.text_input("Estimated Duration")
        deliverables = st.text_area("Expected Deliverables", height=100)

        submitted = st.form_submit_button("✅ Submit Details")

    if submitted:
        payload = {
            "company_name": company_name,
            "project_name": project_name,
            "project_scope": scope,
            "tools": tools,
            "duration": duration,
            "deliverables": deliverables
        }
        try:
            res = requests.post(f"{BASE_URL}/input/", json=payload)
            if res.status_code == 200:
                data = res.json()
                st.session_state.session_id = data["session_id"]
                st.success("Project details stored successfully!")
            else:
                st.error(f"❌ Failed: {res.text}")
        except Exception as e:
            st.error(f"Error: {str(e)}")

# --- PAGE 2: Draft Contract ---
elif page == "Draft Contract":
    st.subheader("📃 Draft Contract")

    if st.session_state.session_id:
        if st.button("Generate Draft"):
            try:
                with st.spinner("⏳ Generating contract draft... Please wait."):
                    # Retrieve contract chunks
                    requests.post(f"{BASE_URL}/retrieve/", params={"session_id": st.session_state.session_id})
                    # Draft contract
                    res = requests.post(f"{BASE_URL}/draft/", params={"session_id": st.session_state.session_id})

                if res.status_code == 200:
                    data = res.json()
                    st.session_state.draft = data["draft"]
                    st.success("✅ Draft generated successfully!")
                    st.text_area("Drafted Contract", st.session_state.draft, height=400, key="draft_area_new")
                else:
                    st.error(f"❌ Failed: {res.text}")
            except Exception as e:
                st.error(f"Error: {str(e)}")
        
        
    else:
        st.warning("⚠️ Please submit project details first.")



## --- PAGE 3: Compliance Check ---
elif page == "Compliance Check":
    st.subheader("✅ Compliance Report")

    if st.session_state.session_id:
        if st.button("Run Compliance Check"):
            try:
                with st.spinner("🔍 Checking contract compliance... Please wait."):
                    res = requests.post(
                        f"{BASE_URL}/compliance/",
                        params={"session_id": st.session_state.session_id}
                    )

                if res.status_code == 200:
                    st.session_state.compliance = res.text
                    st.success("✅ Compliance check completed!")
                    st.info(st.session_state.compliance)

                else:
                    st.error(f"❌ Failed: {res.text}")
            except Exception as e:
                st.error(f"Error: {str(e)}")
        else:
            st.warning("⚠️ Please generate draft first.")



# --- PAGE 4: Summary & Export ---
elif page == "Summary & Export":
    st.subheader("🗂️ Plain-English Summary")

    if st.session_state.session_id and st.session_state.draft:
        if st.button("Generate Summary"):
            try:
                with st.spinner("⏳ Generating summary..."):
                    res = requests.post(
                        f"{BASE_URL}/summary/",
                        params={"session_id": st.session_state.session_id}
                    )
                if res.status_code == 200:
                    st.session_state.summary = res.text
                    st.success("✅ Summary generated!")
                else:
                    st.error(f"❌ Failed: {res.text}")
            except Exception as e:
                st.error(f"Error: {str(e)}")

        if st.session_state.summary:
            st.write("### Contract Summary")
            st.info(st.session_state.summary)

            # ✅ Only one button: Download full drafted contract
            st.download_button(
                "📥 Download Full Drafted Contract",
                st.session_state.draft.encode("utf-8"),
                file_name="contract_draft.txt"
                
            )
    else:
        st.warning("⚠️ Please generate a draft contract first.")

