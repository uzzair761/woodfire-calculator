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

st.title("🍔 Restaurant Order App")

# ---------- SESSION INIT ----------
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
            f"Name for Person {i+1}", key=f"name_input_{i}"
        )
    if st.button("Start Ordering"):
        if all(p["name"].strip() for p in st.session_state.persons):
            st.session_state.step = 2
            st.rerun()
        else:
            st.warning("Please enter all names.")

# ---------- STEP 3 (ORDERING) ----------
elif st.session_state.step == 2:
    person = st.session_state.persons[st.session_state.current_person]
    st.header(f"Ordering for {person['name']}")

    cols = st.columns(2)

    for idx, (item_name, item_data) in enumerate(menu.items()):
        with cols[idx % 2]:
            selected = any(o["name"] == item_name for o in person["orders"])
            # Display image (grey if selected)
            if selected:
                st.markdown(
                    f'<img src="{item_data["image"]}" style="width:100%; border-radius:15px; opacity:0.4;">',
                    unsafe_allow_html=True
                )
            else:
                st.image(item_data["image"], use_container_width=True)
            st.caption(f"{item_name} — RM {item_data['price']}")
            # Invisible button to detect image click
            if st.button(" ", key=f"{person['name']}_{item_name}", use_container_width=True):
                if selected:
                    # Deselect
                    person["orders"] = [o for o in person["orders"] if o["name"] != item_name]
                else:
                    # Select
                    price = item_data["price"]
                    service_charge = price * SERVICE_CHARGE_RATE
                    sst = price * SST_RATE
                    final_price = price + service_charge + sst
                    person["orders"].append({
                        "name": item_name,
                        "price_before_tax": price,
                        "service_charge": service_charge,
                        "sst": sst,
                        "final_price": final_price
                    })
                st.rerun()

    # ---------- SELECTED ITEMS ----------
    st.markdown("---")
    st.subheader("Selected Items")
    total = 0
    for item in person["orders"]:
        st.write(f"{item['name']} - RM {item['final_price']:.2f}")
        total += item['final_price']
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

# ---------- STEP 4 (RECEIPTS WITH TAX BREAKDOWN) ----------
elif st.session_state.step == 3:
    st.header("🧾 Receipts (Detailed Breakdown)")

    overall_before_tax = 0
    overall_service = 0
    overall_sst = 0
    overall_final = 0

    for person in st.session_state.persons:
        st.subheader(person["name"])
        person_before = sum(i["price_before_tax"] for i in person["orders"])
        person_service = sum(i["service_charge"] for i in person["orders"])
        person_sst = sum(i["sst"] for i in person["orders"])
        person_final = sum(i["final_price"] for i in person["orders"])

        overall_before_tax += person_before
        overall_service += person_service
        overall_sst += person_sst
        overall_final += person_final

        for item in person["orders"]:
            st.write(f"{item['name']}")
            st.write(f"  Price Before Tax: RM {item['price_before_tax']:.2f}")
            st.write(f"  Service Charge (8%): RM {item['service_charge']:.2f}")
            st.write(f"  SST (6%): RM {item['sst']:.2f}")
            st.write(f"  Price After Tax: RM {item['final_price']:.2f}")
            st.markdown("---")

        st.write(f"**Subtotal for {person['name']}: RM {person_final:.2f}**")
        st.markdown("===")

    st.header("💰 Overall Total Breakdown")
    st.write(f"Total Before Tax: RM {overall_before_tax:.2f}")
    st.write(f"Total Service Charge (8%): RM {overall_service:.2f}")
    st.write(f"Total SST (6%): RM {overall_sst:.2f}")
    st.write(f"Grand Total (After Tax): RM {overall_final:.2f}")

    if st.button("Start Over"):
        st.session_state.clear()
        st.rerun()
