import streamlit as st

# ---------- TAX SETTINGS ----------
SERVICE_CHARGE_RATE = 0.08
SST_RATE = 0.06

# ---------- MENU WITH IMAGES ----------
menu = {
    "Smoked Burger (Mixed)": {
        "price": 29.90,
        "image": "https://via.placeholder.com/200?text=Mixed+Burger"
    },
    "Mushroom Burger": {
        "price": 23.90,
        "image": "https://via.placeholder.com/200?text=Mushroom+Burger"
    },
    "Brisket Burger": {
        "price": 39.90,
        "image": "https://via.placeholder.com/200?text=Brisket+Burger"
    },
    "Curly Fries": {
        "price": 6.90,
        "image": "https://via.placeholder.com/200?text=Curly+Fries"
    },
}

st.title("🍔 Restaurant Order App")

# ---------- INITIALIZE SESSION STATE ----------
if "step" not in st.session_state:
    st.session_state.step = 0

if "orders" not in st.session_state:
    st.session_state.orders = []

if "persons" not in st.session_state:
    st.session_state.persons = []

# ---------- STEP 1: SET NUMBER OF PERSONS ----------
if st.session_state.step == 0:
    num = st.number_input("How many Persons?", min_value=1, step=1)
    if st.button("Start Ordering"):
        st.session_state.persons = [{"name": f"Person {i+1}", "orders": []} for i in range(num)]
        st.session_state.current_person = 0
        st.session_state.step = 1
        st.rerun()

# ---------- STEP 2: ORDERING (ONE PERSON AT A TIME) ----------
elif st.session_state.step == 1:

    person = st.session_state.persons[st.session_state.current_person]
    st.header(f"Ordering for {person['name']}")

    cols = st.columns(2)

    index = 0
    for item_name, item_data in menu.items():
        with cols[index % 2]:
            st.image(item_data["image"], use_container_width=True)
            if st.button(f"{item_name}\nRM {item_data['price']}", key=f"{person['name']}_{item_name}"):

                service_charge = item_data["price"] * SERVICE_CHARGE_RATE
                sst = item_data["price"] * SST_RATE
                final_price = item_data["price"] + service_charge + sst

                person["orders"].append({
                    "name": item_name,
                    "final_price": final_price
                })

        index += 1

    st.markdown("---")

    if st.button("Next Person"):
        if st.session_state.current_person < len(st.session_state.persons) - 1:
            st.session_state.current_person += 1
            st.rerun()
        else:
            st.session_state.step = 2
            st.rerun()

# ---------- STEP 3: RECEIPTS ----------
elif st.session_state.step == 2:

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
