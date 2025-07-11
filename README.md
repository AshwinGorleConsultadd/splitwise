# 🧱 Django Project - Initial Setup

This project is a **EaseSlpit** built with Django. It allows users to **track shared expenses**, **split bills**, and **settle balances** among friends, roommates, or groups. The app focuses on making group expense management simple, transparent, and fair — just like Splitwise.

Core features include:

- Group creation & member management
- Adding and splitting expenses
- Tracking who owes whom
- Balancing and settling up debts
- Minmum cash-flow algorithm

---

##  Getting Started

These instructions will help you get a copy of the project up and running on your local machine for development and testing.

---

##  Prerequisites

Make sure you have the following installed:

* Python 3.8+
* pip
* Git
* virtualenv (optional but recommended)
* PostgreSQL/MySQL (optional, default is SQLite)

---

## 🛠️ Installation

### 1. Clone the Repository

```bash
https://github.com/AshwinGorleConsultadd/splitwise.git
cd splitwise
```

### 2. Create and Activate a Virtual Environment

```bash
python -m venv venv
source venv/bin/activate      # On Windows: venv\Scripts\activate
```

### 3. Install Project Dependencies

```bash
pip install -r requirements.txt
```

### 4. Set Up Environment Variables

Create a `.env` file in the project root with the following content:

```
DEBUG=True
SECRET_KEY=your-secret-key
ALLOWED_HOSTS=127.0.0.1,localhost
DATABASE_URL=sqlite:///db.sqlite3
# For PostgreSQL:
# DATABASE_URL=postgres://user:password@localhost:5432/dbname
```

> You can use `python-decouple` or `os.environ` to read these values in `settings.py`.

---

### 5. Run Database Migrations

```bash
python manage.py migrate
```

### 6. Create a Superuser (Admin)

```bash
python manage.py createsuperuser
```

### 7. Start the Development Server

```bash
python manage.py runserver
```

Then visit: [http://127.0.0.1:8000](http://127.0.0.1:8000)

---

## 🧪 Running Tests

```bash
python manage.py test
```

---

## 📁 Project Structure

```
your-repo-name/
├── your_project/
│   ├── settings.py
│   ├── urls.py
│   └── ...
├── manage.py
├── requirements.txt
└── README.md
```


## Contact

*Email:* ashwingorle7777@gmail.com 

*GitHub Username:* AshwinGorleConsultadd
[your-username](https://github.com/your-username)
## 💡 Core Algorithm: Minimum Cash Flow for Debt Settlement

To efficiently settle debts between users, this project uses the **Minimum Cash Flow Algorithm**. The goal is to minimize the number of transactions required to balance all expenses, ensuring that users don’t have to send multiple payments unnecessarily.

---

### 🔍 How It Works

Given a list of net balances for each user (positive for creditors, negative for debtors), the algorithm:

1. Identifies the person with the maximum credit and the person with the maximum debt.
2. Settles the minimum of those two amounts between them.
3. Updates the net balances.
4. Repeats the process recursively until all balances are zero.

This approach guarantees debt resolution using the **fewest number of transactions**.

---

### 📘 Reference

This algorithm was adapted from the following GitHub source:

🔗 [Minimum Cash Flow Algorithm – Java Implementation](https://github.com/mission-peace/interview/blob/master/src/com/interview/misc/MinCashFlow.java)  
> Credit to [mission-peace](https://github.com/mission-peace)

---

### 🧠 Python Implementation

```python
def get_min_index(arr):
    """Returns the index of the minimum value in the array"""
    return arr.index(min(arr))


def get_max_index(arr):
    """Returns the index of the maximum value in the array"""
    return arr.index(max(arr))


def min_cash_flow(amount):
    """
    Recursive function to minimize cash flow among a group.
    
    Parameters:
    - amount: list of net amounts each person owes or is owed.
              Positive means person is to receive money,
              Negative means person owes money.
              
    Returns:
    - A list of transactions (from_person, to_person, amount)
    """
    transactions = []

    def settle(amount):
        max_credit_index = get_max_index(amount)
        max_debit_index = get_min_index(amount)

        # If both are zero, all debts are settled
        if amount[max_credit_index] == 0 and amount[max_debit_index] == 0:
            return

        # Find the minimum of what to pay vs what to receive
        min_amount = min(-amount[max_debit_index], amount[max_credit_index])

        # Update balances
        amount[max_credit_index] -= min_amount
        amount[max_debit_index] += min_amount

        # Record the transaction
        transactions.append((
            max_debit_index,  # from_person
            max_credit_index, # to_person
            min_amount
        ))

        # Recurse until settled
        settle(amount)

    settle(amount.copy())  # avoid modifying original list
    return transactions
```

---

### 📌 Example Usage

```python
# Index 0 owes 500, Index 1 is neutral, Index 2 is to receive 500
net_balances = [-500, 0, 500]

result = min_cash_flow(net_balances)

# Output: [(0, 2, 500)]
# Meaning: Person 0 pays Person 2 an amount of 500
print(result)
```

This core logic powers the **"Settle Up"** feature in the application, ensuring optimal transaction efficiency between group members.

---
