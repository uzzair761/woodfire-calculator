import streamlit as st

# ---------- AUTOPLAY VIDEO ----------
video_url = "https://www.w3schools.com/html/mov_bbb.mp4"  # replace with your own video

st.markdown(
    f"""
    <video width="100%" autoplay muted loop playsinline>
        <source src="{video_url}" type="video/mp4">
    </video>
    """,
    unsafe_allow_html=True
)

# ---------- TAX SETTINGS ----------
SERVICE_CHARGE_RATE = 0.08
SST_RATE = 0.06

# ---------- MENU ----------
menu = {
    "Gourmet Burger": 20.90,
    "Stuffed Cheese": 20.90,
    "BBQ Burger": 21.90,
    "Double Patty": 29.90,
    "Smoked Brisket Platter": 46.00,
    "Smoked Burger (Beef/Chicken)": 24.90,
    "Smoked Burger (Mixed)": 29.90,
    "Mushroom Burger": 23.90,
    "Brisket Burger": 39.90,
    "Cheese Steak (2.0)": 19.90,
    "Smoked Chicken Platter": 23.00,
    "Smoked Beef Rib": 70.00,
    "Smoked Lamb Rib": 70.00,
    "Madhen Hot Chicken": 24.90,
    "Curly Fries": 6.90,
    "Cheese Fries": 12.90,
    "Coney Fries": 13.90,
    "Beef & Cheese Fries": 16.90,
    "Mineral Water": 3.90,
    "Iced Lemon Tea": 4.70,
    "F&N Cola": 4.70,
    "F&N Strawberry": 4.70,
    "Sarsi": 4.70,
    "Grape": 4.70,
    "100 Plus": 4.70,
    "Butter Soda": 6.90,
    "Cheese": 3.00,
    "Egg": 2.50,
    "Beef Patty": 8.00,
    "Chicken Patty": 7.00,
    "Turkey Slice": 2.00,
    "Smoked Beef Slice": 3.00,
    "Dill Pickle": 1.00,
    "Smoked Brisket Slice": 20.00,
    "Vanilla Shake": 16.90,
    "Chocolate Shake": 16.90,
    "Oreo Shake": 16.90,
    "Biscoff Shake": 16.90,
    "Nutella Shake": 16.90,
    "Matcha Shake": 16.90,
    "Buttercream Shake": 16.90
}

st.title("🍔 Restaurant Order Calculator")

# ---------- FRIEND INPUT ----------
num_friends = st.number_input("How many friends?", min_value=1, step=1)

friends = []
for i in range(num_friends):
    name = st.text_input(f"Enter name of friend {i+1}", key=f"name_{i}")
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

        if qty > 0:
            service_charge = round(price * SERVICE_CHARGE_RATE, 2)
            sst = round(price * SST_RATE, 2)
            final_price = round(price + service_charge + sst, 2)

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
