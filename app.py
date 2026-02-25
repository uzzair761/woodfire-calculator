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

}

st.title("🍔 Restaurant Order App")

# ---------- SESSION STATE ----------
if "step" not in st.session_state:
    st.session_state.step = 0

if "persons" not in st.session_state:
    st.session_state.persons = []

if "current_person" not in st.session_state:
    st.session_state.current_person = 0

# ---------- STEP 1 ----------
if st.session_state.step == 0:
    num = st.number_input("How many Persons?", min_value=1, step=1)

    if st.button("Next"):
        st.session_state.persons = [{"name": "", "orders": []} for _ in range(num)]
        st.session_state.step = 1
        st.rerun()

# ---------- STEP 2 ----------
elif st.session_state.step == 1:
    st.header("Enter Names")

    for i in range(len(st.session_state.persons)):
        st.session_state.persons[i]["name"] = st.text_input(
            f"Name for Person {i+1}",
            key=f"name_input_{i}"
        )

    if st.button("Start Ordering"):
        if all(p["name"].strip() != "" for p in st.session_state.persons):
            st.session_state.step = 2
            st.rerun()
        else:
            st.warning("Please enter all names.")

# ---------- STEP 3 ----------
elif st.session_state.step == 2:

    person = st.session_state.persons[st.session_state.current_person]
    st.header(f"Ordering for {person['name']}")

    if "selected_items" not in st.session_state:
        st.session_state.selected_items = {}

    if person["name"] not in st.session_state.selected_items:
        st.session_state.selected_items[person["name"]] = []

    cols = st.columns(2)
    index = 0

    for item_name, item_data in menu.items():

        selected = item_name in st.session_state.selected_items[person["name"]]

        with cols[index % 2]:

            style = "opacity:0.4;" if selected else ""

            clicked = st.markdown(
                f"""
                <div style="text-align:center;">
                    <img src="{item_data['image']}" 
                         style="width:100%; border-radius:12px; cursor:pointer; {style}">
                    <p><b>{item_name}</b><br>RM {item_data['price']}</p>
                </div>
                """,
                unsafe_allow_html=True
            )

            if st.button(f"Select {item_name}", key=f"{person['name']}_{item_name}"):

                service_charge = item_data["price"] * SERVICE_CHARGE_RATE
                sst = item_data["price"] * SST_RATE
                final_price = item_data["price"] + service_charge + sst

                person["orders"].append({
                    "name": item_name,
                    "final_price": final_price
                })

                st.session_state.selected_items[person["name"]].append(item_name)
                st.rerun()

        index += 1

    # ---------- SHOW SELECTED ITEMS ----------
    st.markdown("---")
    st.subheader("Selected Items")

    total = 0
    for item in person["orders"]:
        st.write(f"{item['name']} - RM {item['final_price']:.2f}")
        total += item["final_price"]

    st.write(f"**Current Total: RM {total:.2f}**")

    st.markdown("---")

    col1, col2 = st.columns(2)

    with col1:
        if st.button("Next Person"):
            if st.session_state.current_person < len(st.session_state.persons) - 1:
                st.session_state.current_person += 1
                st.rerun()
            else:
                st.session_state.step = 3
                st.rerun()

    with col2:
        if st.button("View Receipt"):
            st.session_state.step = 3
            st.rerun()

# ---------- STEP 4 ----------
elif st.session_state.step == 3:

    st.header("🧾 Receipts")

    overall_total = 0

    for person in st.session_state.persons:
        st.subheader(person["name"])
        total = 0

        for item in person["orders"]:
            st.write(f"{item['name']} - RM {item['final_price']:.2f}")
            total += item["final_price"]

        overall_total += total
        st.write(f"**Grand Total: RM {total:.2f}**")
        st.markdown("---")

    st.header(f"💰 Overall Total: RM {overall_total:.2f}")

    if st.button("Start Over"):
        st.session_state.clear()
        st.rerun()

