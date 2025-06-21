import streamlit as st

# -------------------------------
# Account Classes (OOP)
# -------------------------------

class BankAccount:
    def __init__(self, name, balance=0):
        self.name = name
        self.balance = balance

    def deposit(self, amount):
        if amount > 0:
            self.balance += amount
            return True
        return False

    def withdraw(self, amount):
        if 0 < amount <= self.balance:
            self.balance -= amount
            return True
        return False

    def get_balance(self):
        return self.balance


class SavingsAccount(BankAccount):
    def __init__(self, name, balance=0, interest_rate=0.05):
        super().__init__(name, balance)
        self.interest_rate = interest_rate

    def add_interest(self):
        interest = self.balance * self.interest_rate
        self.balance += interest
        return interest


class CurrentAccount(BankAccount):
    def __init__(self, name, balance=0, overdraft_limit=1000):
        super().__init__(name, balance)
        self.overdraft_limit = overdraft_limit

    def withdraw(self, amount):
        if 0 < amount <= self.balance + self.overdraft_limit:
            self.balance -= amount
            return True
        return False


# -------------------------------
# Streamlit App
# -------------------------------

st.title("💰 Simple Bank App")

# Sidebar navigation
menu = st.sidebar.selectbox("Select Account Type", ["🏠 Home", "💼 Current Account", "💳 Savings Account"])

# Global accounts (in-memory; resets on refresh)
if 'current_account' not in st.session_state:
    st.session_state.current_account = CurrentAccount("John Doe", 500)

if 'savings_account' not in st.session_state:
    st.session_state.savings_account = SavingsAccount("John Doe", 1000)

# -------------------------------
# Homepage
# -------------------------------
if menu == "🏠 Home":
    st.subheader("Welcome to COS104 Bank App")
    st.write("Select an account type from the sidebar to get started.")

# -------------------------------
# Current Account Page
# -------------------------------
elif menu == "💼 Current Account":
    st.subheader("Current Account")

    acc = st.session_state.current_account
    st.write(f"**Balance:** ₦{acc.get_balance():,.2f}")
    st.write(f"**Overdraft Limit:** ₦{acc.overdraft_limit:,.2f}")

    action = st.radio("Choose an action:", ["Deposit", "Withdraw"])
    amount = st.number_input("Enter amount", min_value=0.0, step=100.0)

    if st.button("Submit"):
        if action == "Deposit":
            if acc.deposit(amount):
                st.success(f"₦{amount} deposited.")
            else:
                st.error("Invalid deposit.")
        elif action == "Withdraw":
            if acc.withdraw(amount):
                st.success(f"₦{amount} withdrawn.")
            else:
                st.error("Insufficient funds (even with overdraft).")

# -------------------------------
# Savings Account Page
# -------------------------------
elif menu == "💳 Savings Account":
    st.subheader("Savings Account")

    acc = st.session_state.savings_account
    st.write(f"**Balance:** ₦{acc.get_balance():,.2f}")
    st.write(f"**Interest Rate:** {acc.interest_rate * 100:.1f}%")

    action = st.radio("Choose an action:", ["Deposit", "Withdraw", "Add Interest"])
    amount = 0
    if action in ["Deposit", "Withdraw"]:
        amount = st.number_input("Enter amount", min_value=0.0, step=100.0)

    if st.button("Submit"):
        if action == "Deposit":
            if acc.deposit(amount):
                st.success(f"₦{amount} deposited.")
            else:
                st.error("Invalid deposit.")
        elif action == "Withdraw":
            if acc.withdraw(amount):
                st.success(f"₦{amount} withdrawn.")
            else:
                st.error("Insufficient funds.")
        elif action == "Add Interest":
            interest = acc.add_interest()
            st.success(f"₦{interest:.2f} interest added.")