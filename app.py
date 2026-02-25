import streamlit as st

# ---------- TAX SETTINGS ----------
SERVICE_CHARGE_RATE = 0.08
SST_RATE = 0.06

# ---------- MENU ----------
menu = {
    "Smoked Burger (Mixed)": 29.90,
    "Mushroom Burger": 23.90,
    "Brisket Burger": 39.90,
    "Curly Fries": 6.90,
}

st.title("🍔 Restaurant Order Calculator")

# ---------- FRIEND INPUT ----------
num_friends = st.number_input("How many Persons?", min_value=1, step=1)

friends = []
for i in range(num_friends):
    name = st.text_input(f"Enter name of Person {i+1}", key=f"name_{i}")
    friends.append({"name": name, "orders": []})

# ---------- ORDERS ----------
for friend in friends:
    st.subheader(f"Orders for {friend['name']}")
    for item_name, price in menu.items():
        qty = st.number_input(
            f"{item_name} (RM {price})",
            min_value=0,
            step=1,
            key=f"{friend['name']}_{item_name}"
        )

        service_charge = price * SERVICE_CHARGE_RATE
        sst = price * SST_RATE,
        final_price = price + service_charge + sst

        friend['orders'].append({
            "name": item_name,
            "quantity": qty,
            "final_price": final_price
            })

# ---------- RECEIPTS ----------
st.header("🧾 Receipts")

overall_total = 0

for friend in friends:
    st.subheader(f"Receipt for {friend['name']}")
    total = 0

    for item in friend['orders']:
        line_total = item['final_price'] * item['quantity']
        total += line_total
        st.write(f"{item['quantity']} x {item['name']} = RM {line_total:.2f}")

    overall_total += total
    st.write(f"**Grand Total: RM {total:.2f}**")
    st.markdown("---")

st.header("💰 Overall Total")
st.write(f"**RM {overall_total:.2f}**")







