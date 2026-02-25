import streamlit as st

# ---------- TAX SETTINGS ----------
SERVICE_CHARGE_RATE = 0.08
SST_RATE = 0.06

# ---------- MENU WITH IMAGES ----------
menu = {
    "Smoked Burger (Mixed)": {
        "price": 29.90,
        "image": "https://woodfire.com.my/wp-content/uploads/2024/12/Artboard-7-2-1024x1024.png"
    },
    "Mushroom Burger": {
        "price": 23.90,
        "image": "https://woodfire.com.my/wp-content/uploads/2024/11/Mushroom-Burger-1024x1024.webp"
    },
    "Brisket Burger": {
        "price": 39.90,
        "image": "https://woodfire.com.my/wp-content/uploads/2024/11/Brisket-Burger-1024x1024.webp"
    },
    "Curly Fries": {
        "price": 6.90,
        "image": "https://woodfire.com.my/wp-content/uploads/2024/11/Curly-Fries-1.webp"
    },
}

st.set_page_config(page_title="Woodfire Order", layout="centered")
st.title("🍔 Restaurant Order App")

# ---------- CUSTOM CSS FOR IMAGE BUTTONS ----------
st.markdown("""
    <style>
    .menu-container {
        position: relative;
        text-align: center;
        margin-bottom: 20px;
    }
    /* Styles the button to be invisible but cover the image area */
    div.stButton > button {
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        height: 250px; /* Adjust this to match your image height */
        background-color: transparent !important;
        color: transparent !important;
        border: none !important;
        z-index: 10;
        cursor: pointer;
    }
    div.stButton > button:hover {
        background-color: rgba(255, 255, 255, 0.1) !important;
    }
    .burger-img {
        width: 100%;
        height: 250px;
        object-fit: cover;
        border-radius: 15px;
        transition: 0.3s;
    }
    .selected-img {
        opacity: 0.3;
        filter: grayscale(100%);
    }
    </style>
""", unsafe_allow_html=True)

# ---------- SESSION INIT ----------
if "step" not in st.session_state:
    st.session_state.step = 0
if "persons" not in st.session_state:
    st.session_state.persons = []
if "current_person" not in st.session_state:
    st.session_state.current_person = 0

# ---------- STEP 0: PERSON COUNT ----------
if st.session_state.step == 0:
    num = st.number_input("How many Persons?", min_value=1, step=1)
    if st.button("Next"):
        st.session_state.persons = [{"name": "", "orders": []} for _ in range(num)]
        st.session_state.step = 1
        st.rerun()

# ---------- STEP 1: ENTER NAMES ----------
elif st.session_state.step == 1:
    st.header("Enter Names")
    for i in range(len(st.session_state.persons)):
        st.session_state.persons[i]["name"] = st.text_input(
            f"Name for Person {i+1}",
            key=f"name_input_{i}"
        )

    if st.button("Start Ordering"):
        if all(p["name"].strip() for p in st.session_state.persons):
            st.session_state.step = 2
            st.rerun()
        else:
            st.warning("Please enter all names.")

# ---------- STEP 2: ORDERING (IMAGE BUTTONS) ----------
elif st.session_state.step == 2:
    person = st.session_state.persons[st.session_state.current_person]
    st.header(f"Ordering for {person['name']}")

    cols = st.columns(2)

    for idx, (item_name, item_data) in enumerate(menu.items()):
        with cols[idx % 2]:
            selected = any(o["name"] == item_name for o in person["orders"])
            img_class = "burger-img selected-img" if selected else "burger-img"

            # 1. Create the container
            st.markdown(f'<div class="menu-container">', unsafe_allow_html=True)
            
            # 2. Show the Image
            st.markdown(f'<img src="{item_data["image"]}" class="{img_class}">', unsafe_allow_html=True)

            # 3. Transparent Button Overlay
            if st.button("Select", key=f"btn_{person['name']}_{item_name}"):
                if selected:
                    person["orders"] = [o for o in person["orders"] if o["name"] != item_name]
                else:
                    price = item_data["price"]
                    taxed_price = price * (1 + SERVICE_CHARGE_RATE + SST_RATE)
                    person["orders"].append({
                        "name": item_name,
                        "final_price": taxed_price
                    })
                st.rerun()
            
            st.markdown('</div>', unsafe_allow_html=True)
            st.markdown(f"**{item_name}** <br> RM {item_data['price']:.2f}", unsafe_allow_html=True)

    # SELECTED ITEMS SUMMARY
    st.markdown("---")
    st.subheader("Selected Items")
    total = sum(item["final_price"] for item in person["orders"])
    for item in person["orders"]:
        st.write(f"✅ {item['name']} - RM {item['final_price']:.2f}")
    
    st.write(f"### Current Total: RM {total:.2f}")

    col1, col2 = st.columns(2)
    with col1:
        btn_text = "Next Person" if st.session_state.current_person < len(st.session_state.persons) - 1 else "Finish"
        if st.button(btn_text):
            if st.session_state.current_person < len(st.session_state.persons) - 1:
                st.session_state.current_person += 1
                st.rerun()
            else:
                st.session_state.step = 3
                st.rerun()

# ---------- STEP 3: FINAL RECEIPTS ----------
elif st.session_state.step == 3:
    st.header("🧾 Final Receipts")
    overall_total = 0

    for person in st.session_state.persons:
        st.subheader(f"👤 {person['name']}")
        p_total = 0
        if not person["orders"]:
            st.write("No items ordered.")
        else:
            for item in person["orders"]:
                st.write(f"- {item['name']}: RM {item['final_price']:.2f}")
                p_total += item["final_price"]
        
        st.write(f"**Total for {person['name']}: RM {p_total:.2f}**")
        overall_total += p_total
        st.markdown("---")

    st.success(f"## 💰 Grand Total: RM {overall_total:.2f}")

    if st.button("New Order"):
        st.session_state.clear()
        st.rerun()
