import streamlit as st
import json
import os

st.set_page_config(page_title="EduThrift", page_icon="📘", layout="centered")

st.title("📘 EduThrift – Share & Reuse Educational Resources")
st.caption("Promoting sustainability in education through sharing and reuse")

# ---------- Data File ----------
DATA_FILE = "data.json"

if os.path.exists(DATA_FILE):
    with open(DATA_FILE, "r") as f:
        resources = json.load(f)
else:
    resources = []

# ---------- Sidebar Navigation ----------
menu = st.sidebar.radio("📍 Navigation", ["Add Resource", "View Resources", "About"])

# ---------- Add Resource Section ----------
if menu == "Add Resource":
    st.subheader("📤 Add a New Resource")

    with st.form("resource_form"):
        title = st.text_input("Title")
        category = st.text_input("Category")
        location = st.text_input("Location")
        description = st.text_area("Description")
        image = st.file_uploader("Upload Image", type=["jpg", "jpeg", "png"])
        submitted = st.form_submit_button("Add Resource")

        if submitted:
            if title and category and location:
                new_resource = {
                    "title": title,
                    "category": category,
                    "location": location,
                    "description": description,
                    "image": image.name if image else None,
                }

                if image:
                    os.makedirs("uploads", exist_ok=True)
                    img_path = os.path.join("uploads", image.name)
                    with open(img_path, "wb") as f:
                        f.write(image.getbuffer())

                resources.append(new_resource)
                with open(DATA_FILE, "w") as f:
                    json.dump(resources, f, indent=4)

                st.success("✅ Resource added successfully!")
            else:
                st.warning("⚠️ Please fill all required fields.")

# ---------- View Resources ----------
elif menu == "View Resources":
    st.subheader("📚 Available Resources")

    if not resources:
        st.info("No resources shared yet.")
    else:
        for res in resources[::-1]:
            st.markdown(f"### {res['title']}")
            st.markdown(f"**Category:** {res['category']} | **Location:** {res['location']}")
            st.markdown(res['description'])
            if res.get("image"):
                st.image(os.path.join("uploads", res["image"]), width=250)
            st.divider()

# ---------- About Section ----------
else:
    st.subheader("💡 About EduThrift")
    st.write("""
    **EduThrift** is a sustainability-focused web app designed to reduce educational waste
    by enabling students to share, donate, and reuse study materials like books and uniforms.  
    This prototype is built using **Streamlit** and stores data locally in a JSON file.  
    It promotes **Education for a Sustainable Future** and can be expanded to use cloud storage later.
    """)

st.markdown("---")
st.caption("Made with ❤️ using Streamlit | EduThrift 2025")
