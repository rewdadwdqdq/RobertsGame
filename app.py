

import streamlit as st
import streamlit.components.v1 as components
import random
import time

st.set_page_config(
    page_title="Steal the Brainrots",
    page_icon="🧠",
    layout="wide"
)

# ---------- GAME DATA ----------

BRAINROTS = {
    "Noobini Pizzanini": {
        "price": 50, "income": 5, "rarity": "Common", "emoji": "🍕"
    },
    "Trippi Troppi": {
        "price": 150, "income": 15, "rarity": "Rare", "emoji": "🦈"
    },
    "Ballerina Cappuccina": {
        "price": 500, "income": 50, "rarity": "Epic", "emoji": "☕"
    },
    "Bombardiro Crocodilo": {
        "price": 1500, "income": 150, "rarity": "Legendary", "emoji": "🐊"
    },
    "Tung Tung Tung Sahur": {
        "price": 5000, "income": 500, "rarity": "Mythic", "emoji": "🪵"
    },
    "Secret Brainrot": {
        "price": 15000, "income": 2000, "rarity": "Secret", "emoji": "👽"
    }
}

# ---------- SESSION STATE ----------

if "coins" not in st.session_state:
    st.session_state.coins = 100

if "inventory" not in st.session_state:
    st.session_state.inventory = []

if "bots" not in st.session_state:
    st.session_state.bots = {
        "Bot Alex": ["Trippi Troppi", "Noobini Pizzanini"],
        "Bot Mike": ["Bombardiro Crocodilo"],
        "Bot John": ["Ballerina Cappuccina", "Trippi Troppi"]
    }

if "last_time" not in st.session_state:
    st.session_state.last_time = time.time()

if "multiplier" not in st.session_state:
    st.session_state.multiplier = 1

# ---------- INCOME SYSTEM ----------

current_time = time.time()
elapsed = current_time - st.session_state.last_time

income = sum(
    BRAINROTS[name]["income"]
    for name in st.session_state.inventory
)

st.session_state.coins += int(
    elapsed * income * st.session_state.multiplier
)

st.session_state.last_time = current_time

# ---------- HTML / CSS DESIGN ----------

st.markdown("""
<style>
.stApp {
    background: linear-gradient(135deg, #151525, #25254a);
    color: white;
}

h1, h2, h3, p {
    color: white;
}

div.stButton > button {
    background: #7c3aed;
    color: white;
    border-radius: 12px;
    border: none;
    font-weight: bold;
    padding: 10px;
}

div.stButton > button:hover {
    background: #a855f7;
    color: white;
}

.brainrot-card {
    background: linear-gradient(145deg, #303052, #19192e);
    border: 2px solid #7045bd;
    border-radius: 18px;
    padding: 20px;
    text-align: center;
    margin-bottom: 15px;
}

.brainrot-emoji {
    font-size: 55px;
}

.coin {
    color: #facc15;
    font-weight: bold;
}
</style>
""", unsafe_allow_html=True)

# ---------- HTML ELEMENT ----------

components.html("""
<div style="
    background: linear-gradient(90deg, #7c3aed, #ec4899);
    padding: 20px;
    border-radius: 18px;
    text-align: center;
    color: white;
    font-family: Arial;
">
    <h1 style="margin:0;">🧠 STEAL THE BRAINROTS</h1>
    <p>Collect. Upgrade. Steal. Become the richest player!</p>
    <div style="font-size:35px; animation: bounce 1s infinite alternate;">
        🤑 🧠 💰
    </div>
</div>

<style>
@keyframes bounce {
    from { transform: translateY(0); }
    to { transform: translateY(-12px); }
}
</style>
""", height=170)

# ---------- PLAYER INFORMATION ----------

st.title("🏠 Your Brainrot Base")

col1, col2, col3 = st.columns(3)

col1.metric("💰 Coins", f"{st.session_state.coins:,}")
col2.metric("🧠 Brainrots", len(st.session_state.inventory))
col3.metric("⚡ Income / sec", 
            f"{income * st.session_state.multiplier}")

st.divider()

# ---------- SHOP ----------

st.header("🛒 Brainrot Shop")

columns = st.columns(3)

for index, (name, data) in enumerate(BRAINROTS.items()):

    with columns[index % 3]:

        st.markdown(f"""
        <div class="brainrot-card">
            <div class="brainrot-emoji">{data['emoji']}</div>
            <h3>{name}</h3>
            <p>Rarity: {data['rarity']}</p>
            <p class="coin">Price: {data['price']} coins</p>
            <p>Income: +{data['income']}/sec</p>
        </div>
        """, unsafe_allow_html=True)

        if st.button(f"Buy {name}", key=f"buy_{name}"):

            if st.session_state.coins >= data["price"]:

                st.session_state.coins -= data["price"]
                st.session_state.inventory.append(name)

                st.success(f"You bought {name}!")
                st.rerun()

            else:
                st.error("Not enough coins!")

# ---------- YOUR INVENTORY ----------

st.divider()
st.header("🏠 Your Inventory")

if st.session_state.inventory:

    for i, name in enumerate(st.session_state.inventory):

        data = BRAINROTS[name]

        st.write(
            f"{data['emoji']} **{name}** — "
            f"+{data['income']}/sec"
        )

else:
    st.info("Your base is empty! Buy your first Brainrot.")

# ---------- STEALING SYSTEM ----------

st.divider()
st.header("🥷 Steal From Other Players")

st.write("Choose a bot and attempt to steal one of its Brainrots!")

for bot, characters in st.session_state.bots.items():

    with st.expander(f"🏠 {bot}"):

        if characters:

            st.write("Brainrots:")

            for character in characters:
                data = BRAINROTS[character]
                st.write(f"{data['emoji']} {character}")

            if st.button(f"Steal from {bot}", key=f"steal_{bot}"):

                if random.random() < 0.65:

                    stolen = random.choice(characters)

                    characters.remove(stolen)
                    st.session_state.inventory.append(stolen)

                    st.success(f"Successfully stole {stolen}!")
                else:
                    st.error("You failed to steal! Try again.")

                st.rerun()

        else:
            st.warning("This player's base is empty!")

# ---------- UPGRADES ----------

st.divider()
st.header("⚡ Upgrades")

upgrade_price = 1000 * st.session_state.multiplier

st.write(
    f"Income multiplier: x{st.session_state.multiplier}"
)

if st.button(f"Upgrade income ({upgrade_price} coins)"):

    if st.session_state.coins >= upgrade_price:

        st.session_state.coins -= upgrade_price
        st.session_state.multiplier += 1

        st.success("Upgrade purchased!")
        st.rerun()

    else:
        st.error("Not enough coins!")

# ---------- REFRESH ----------

st.divider()

if st.button("🔄 Refresh Game"):
    st.rerun()

st.caption("Steal the Brainrots - Fan-made mini game")
