 import streamlit as st

class BankAccount:
    def init(self, name, balance=0):
        self.name = name
        self.balance = balance

    def deposit(self, amount):
        if amount > 0:
            self.balance += amount
            return f"✅ Deposited £{amount}. New balance: £{self.balance}"
        return "❌ Deposit amount must be positive."

    def check_balance(self):
        return self.balance


class SavingsAccount(BankAccount):
    WITHDRAWAL_LIMIT = 500

    def withdraw(self, amount):
        if amount > self.balance:
            return "❌ Insufficient funds."
        elif amount > SavingsAccount.WITHDRAWAL_LIMIT:
            return f"❌ Limit exceeded. Max is £{SavingsAccount.WITHDRAWAL_LIMIT}."
        elif amount <= 0:
            return "❌ Enter a valid amount."
        self.balance -= amount
        return f"💸 Withdrew £{amount}. New balance: £{self.balance}"


class CurrentAccount(BankAccount):
    def withdraw(self, amount):
        if amount > self.balance:
            return "❌ Insufficient funds."
        elif amount <= 0:
            return "❌ Enter a valid amount."
        self.balance -= amount
        return f"💸 Withdrew £{amount}. New balance: £{self.balance}"


if "savings" not in st.session_state:
    st.session_state.savings = SavingsAccount("Savings", 1000)

if "current" not in st.session_state:
    st.session_state.current = CurrentAccount("Current", 1500)

st.title("🏦 Simple Bank App (Streamlit Version)")

account_type = st.selectbox("Choose Account Type", ["Savings", "Current"])
amount = st.number_input("Enter amount (£):", min_value=0.0, step=10.0)

account = st.session_state.savings if account_type == "Savings" else st.session_state.current

col1, col2, col3 = st.columns(3)

with col1:
    if st.button("💰 Deposit"):
        result = account.deposit(amount)
        st.success(result)

with col2:
    if st.button("💸 Withdraw"):
        result = account.withdraw(amount)
        if result.startswith("❌"):
            st.error(result)
        else:
            st.success(result)

with col3:
    if st.button("📊 Check Balance"):
        st.info(f"💼 {account.name} Balance: £{account.check_balance()}")