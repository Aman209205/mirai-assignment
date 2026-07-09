import streamlit as st

# =====================================================================
# TASK 1: The UI Shell
# =====================================================================
st.title("🌌 Echo Chamber 9000")
st.write(
    "Welcome to the Identity Echo Interface. Provide your credentials and your "
    "intended communication below to broadcast your message across the void."
)

st.write("---")  # Visual separator for clean UI

# =====================================================================
# TASK 2: Multi-Data Collection
# =====================================================================
# Collecting inputs and stripping whitespace to prevent accidental spacebar-only bypasses
user_name = st.text_input("Name", placeholder="Enter your designation...").strip()
user_message = st.text_input("Message", placeholder="Type your transmission...").strip()

# =====================================================================
# TASK 3: The Action Gate
# =====================================================================
transmit_button = st.button("Transmit 🚀")

# All logical operations occur downstream from the Action Gate
if transmit_button:
    
    # =====================================================================
    # TASK 4: Conditional Routing (Edge Cases)
    # =====================================================================
    if not user_name:
        st.error("Please provide your name.")
        
    elif not user_message:
        st.warning("Please type a message to transmit.")
        
    # =====================================================================
    # TASK 5: The Formatted Output & ADVANCED CHALLENGE
    # =====================================================================
    else:
        # Core Requirement Output
        st.success(f"Transmission successful! Greetings, {user_name}. We received your message: {user_message}")
        
        # --- Advanced Challenge: Token Cost Estimator ---
        # 1. Calculate total character length
        char_count = len(user_message)
        
        # 2. Calculate token count (1 token ≈ 4 characters)
        # Using floating-point division or rounding up can work; here we keep it as a float or int.
        token_count = char_count / 4
        
        # 3. Display the system metric
        st.info(f" System Check: Your message will consume approximately {token_count} tokens from our context window.")