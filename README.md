# NexaBank — Enterprise Full-Stack Banking Management System

[![Django](https://img.shields.io/badge/Django-092E20?style=for-the-badge&logo=django&logoColor=white)](https://www.djangoproject.com/)
[![Django REST Framework](https://img.shields.io/badge/DRF-ff1709?style=for-the-badge&logo=django&logoColor=white)](https://www.django-rest-framework.org/)
[![React](https://img.shields.io/badge/React_19-20232A?style=for-the-badge&logo=react&logoColor=61DAFB)](https://react.dev/)
[![Vite](https://img.shields.io/badge/Vite_8-646CFF?style=for-the-badge&logo=vite&logoColor=white)](https://vitejs.dev/)
[![JWT](https://img.shields.io/badge/JWT_Auth-000000?style=for-the-badge&logo=jsonwebtokens&logoColor=white)](https://jwt.io/)
[![SQLite](https://img.shields.io/badge/SQLite-003B57?style=for-the-badge&logo=sqlite&logoColor=white)](https://www.sqlite.org/)
[![Recharts](https://img.shields.io/badge/Recharts-22b5bf?style=for-the-badge&logo=d3.js&logoColor=white)](https://recharts.org/)

---

## 📌 Project Overview

**NexaBank** is a full-stack, enterprise-grade banking and treasury management system engineered to simulate real-world commercial retail banking workflows. Built with a robust **Django REST Framework** backend and a responsive, high-performance **React 19 + Vite** frontend, NexaBank provides a multi-tenant, multi-branch architecture governed by strict **Role-Based Access Control (RBAC)** across three primary user personas: **Bank Administrators**, **Branch Staff (Tellers)**, and **Retail Customers**.

The platform models operational integrity by implementing true-to-life banking business rules, including:
- **Central Treasury & Branch Liquidity Management**: Central HQ Vault with capital allocation pipelines to branch vaults.
- **Physical vs. Digital Transaction Scoping**: Physical counter-only cash operations (Deposits & Withdrawals) vs. self-service online fund transfers.
- **Mandatory KYC Compliance**: Automatic enforcement of Know-Your-Customer (KYC) details (Aadhar, PAN, Date of Birth, Address) prior to account activation.
- **Transaction Safety & Re-Authentication**: Real-time counterparty account lookups, minimum balance enforcement, and step-up password confirmation on transfers.
- **Auditable Printable Receipts & Analytics**: Thermal-style printable transaction receipts and an executive business intelligence dashboard with financial charting.

---

## 🛠️ Tech Stack

### Backend (`BANK_MANAGEMENT_SYSTEM`)
| Component | Technology | Description |
| :--- | :--- | :--- |
| **Framework** | **Django 5.x / 6.x** | Core web framework powering ORM, settings, and migrations |
| **REST API** | **Django REST Framework (DRF)** | API endpoints, ModelViewSets, serializers, and parsers |
| **Authentication** | **SimpleJWT (`djangorestframework-simplejwt`)** | Stateless JWT authentication (Access & Refresh tokens) with custom role claims |
| **CORS Middleware** | **`django-cors-headers`** | Secure Cross-Origin Resource Sharing for frontend communication |
| **Search & Filtering** | **`django-filter` & DRF Filters** | Field-level filtering, search query parsers, and field ordering |
| **Database** | **SQLite 3** | Default relational database engine with foreign keys and cascade protections |
| **Language** | **Python 3.10+ / 3.14** | Modern Python syntax and type safety |

### Frontend (`BANK_MANAGEMENT_FRONTEND`)
| Component | Technology | Description |
| :--- | :--- | :--- |
| **Library** | **React 19** | Declarative component-driven UI architecture with modern hooks |
| **Build Tool** | **Vite 8** | Lightning-fast development server with Hot Module Replacement (HMR) |
| **Routing** | **React Router DOM v7** | Client-side routing with role-aware `PrivateRoute` guards |
| **HTTP Client** | **Axios** | Promised-based HTTP client equipped with request interceptors for Bearer JWT tokens |
| **Data Visualization** | **Recharts** | Interactive charts (Donut charts, Area growth charts, Bar balance distributions) |
| **UI Icons** | **Lucide React** | Clean, lightweight modern banking and action icon set |
| **Alerts & Modals** | **SweetAlert2** | Interactive confirmation dialogues, warning prompts, and toast alerts |
| **Styling** | **Vanilla CSS3** | Custom design system with modern banking cards, responsive tables, and theme badges |

---

## 👥 Role-Based Capabilities & Features

```
                   ┌──────────────────────────────────────┐
                   │               NexaBank               │
                   └──────────────────┬───────────────────┘
                                      │
        ┌─────────────────────────────┼─────────────────────────────┐
        ▼                             ▼                             ▼
┌──────────────┐              ┌──────────────┐              ┌──────────────┐
│  👑 Admin    │              │  🏦 Staff    │              │ 👤 Customer  │
├──────────────┤              ├──────────────┤              ├──────────────┤
│• HQ Vault    │              │• Branch KYC  │              │• View Account│
│• Capital Ops │              │• Open Account│              │• Fund Transfer│
│• Fund Alloc  │              │• Cash Dep/Wd │              │• Verify Pwd  │
│• Branch CRUD │              │• Counter Txns│              │• View Ledger │
│• Staff Mgmt  │              │• Branch Vault│              │• Print Receipt│
│• Analytics   │              │• Activation  │              │• Profile     │
└──────────────┘              └──────────────┘              └──────────────┘
```

### 1. 👑 Headquarters Administrator (`admin`)
- **HQ Treasury & Liquidity Control**:
  - View real-time central **HQ Vault Balance**.
  - Inject new capital into the HQ Vault.
  - Allocate funds directly to individual branch vaults with unique reference tracking and automated audit trails.
- **Branch Infrastructure Management**:
  - Create, view, and update bank branches (Branch Name, Code, Address, City, State).
  - Live tracking of cash balances and staff headcounts per branch.
- **Staff Provisioning**:
  - Onboard and register bank staff members with verified **PAN** (10 chars) and **Aadhar** (12 digits).
  - Assign staff members directly to designated branches.
  - View staff directory with branch associations and contact info.
- **Account Policy Administration**:
  - Define, update, and manage **Account Types** (e.g., Savings, Current, Fixed Deposit) with configurable minimum balance requirements.
  - Protected cascade rules prevent deleting account types currently in use by active accounts.
- **Executive Analytics Dashboard**:
  - **KPI Metrics**: Total Accounts, Total Deposited Funds, Active Accounts Count, and Low Balance Warnings.
  - **Branch Performance Chart**: Donut chart visualizing total funds distribution across branches.
  - **Growth Trend Chart**: 6-month historical area chart illustrating deposit vs. withdrawal trends.
  - **Account Balance Distribution**: Bar chart categorizing accounts across balance brackets (`0-1K`, `1K-10K`, `10K-50K`, `50K+`).
  - **Branch Leaderboard**: Top performing branches ranked by total deposit volume.
  - **Live Audit Feed**: Monitor latest transactions across the entire banking network.

### 2. 🏦 Branch Counter Staff / Teller (`staff`)
- **Branch-Scoped Workspace**:
  - Automatically constrained to the staff member's assigned branch.
  - Real-time monitor of the local **Branch Vault Balance**.
- **Customer Onboarding & KYC Verification**:
  - Create walk-in customer user profiles.
  - Update customer KYC profile data (Date of Birth, Residential Address, 12-digit Aadhar number).
  - Branch-restricted edit permissions (staff can only edit customers belonging to their branch).
- **Account Lifecycle Management**:
  - Open new accounts for customers under authorized account types.
  - **Strict KYC Pre-Activation Check**: Backend automatically blocks activating any pending account until the customer has completed DOB, address, and Aadhar details.
- **Teller Counter Cash Operations**:
  - **Cash Deposit**: Credits customer balance and debits branch vault balance. *Failsafe prevents deposits if the branch vault balance is insufficient.*
  - **Cash Withdrawal**: Debits customer balance and credits branch vault balance. Enforces account minimum balance rules.
  - **Assisted Transfers**: Conduct counter transfers between accounts with instant lookup and validation.

### 3. 👤 Retail Customer (`customer`)
- **Self-Service Registration & Guided Onboarding**:
  - Online customer registration with instant customer ID generation (`CUSTXXXXXX`).
  - Guided welcome interface presenting branch information and available account types.
- **Account & Portfolio Overview**:
  - View all personal accounts, current balances, account types, and assigned branches.
  - KYC and profile status overview.
- **Secure Online Fund Transfers**:
  - Initiate transfers from active accounts to any recipient account.
  - **Instant Counterparty Verification**: As-you-type account number validation displaying the recipient's name and branch before funds move.
  - **Step-Up Authentication**: Mandatory password re-confirmation before the transfer payload is submitted.
  - **Business Rules Enforcement**: Prevents self-transfers, transfers to inactive accounts, or transfers that breach the account type's minimum balance requirement.
- **Digital Receipts & Transaction Ledger**:
  - Detailed transaction history categorizing inward (received) and outward (sent) transfers.
  - **Printable Transaction Receipt**: Built-in popup engine formatting an official NexaBank receipt ready for printing or PDF saving.

---

## 🏛️ Business Rules & System Validations

| Rule | Enforcement Level | Description |
| :--- | :--- | :--- |
| **Separation of Duties** | Backend (`views.py`) | Admin accounts are strictly forbidden from executing deposits, withdrawals, or transfers to maintain financial auditing integrity. |
| **KYC Before Activation** | Backend (`views.py`) | An account status cannot be updated from `pending` to `active` unless the customer record contains a valid `date_of_birth`, `address`, and `aadhar_number`. |
| **Cash Vault Liquidity** | Backend (`views.py`) | Deposits can only be completed if the branch vault has sufficient liquidity to back the transaction. |
| **Minimum Balance** | Backend (`views.py`) | Withdrawals and transfers cannot lower the account balance below the threshold configured in `AccountType.minimum_balance`. |
| **Transfer Password Check** | Backend & Frontend | Customer online transfers require typing their account password, verified server-side using Django's `check_password()`. |
| **Identifier Validations** | Serializers (`serializers.py`) | PAN numbers must be exactly 10 alphanumeric characters; Aadhar numbers must be exactly 12 numeric digits; Phone numbers must be exactly 10 numeric digits. |
| **Protected Deletions** | ORM (`ProtectedError`) | Deletion of an `AccountType` or `Branch` tied to existing records is intercepted and safely reported without database crashes. |

---

## 📂 Project Directory Structure

```text
.
├── BANK_MANAGEMENT_SYSTEM/                  # Django REST Framework Backend
│   ├── bank_management/                     # Main Django Project Root
│   │   ├── bank/                            # Core Banking Application
│   │   │   ├── migrations/                  # Database migration files
│   │   │   │   ├── 0001_initial.py
│   │   │   │   ├── 0002_hqvault_branch_vault_balance_fundallocation.py
│   │   │   │   └── 0003_user_aadhar_number_user_pan_number_and_more.py
│   │   │   ├── admin.py                     # Django Admin model registrations
│   │   │   ├── apps.py                      # App configuration
│   │   │   ├── models.py                    # Relational schema (User, Branch, Account, etc.)
│   │   │   ├── permission.py                # Custom DRF permissions (IsAdminRole)
│   │   │   ├── serializers.py               # DRF ModelSerializers & JWT token claims
│   │   │   ├── tests.py                     # Unit & integration test suites
│   │   │   ├── urls.py                      # Bank API routing table & ViewSet routes
│   │   │   └── views.py                     # ViewSets, business logic & analytics views
│   │   ├── bank_management/                 # Django Configuration Module
│   │   │   ├── __init__.py
│   │   │   ├── asgi.py                      # ASGI entrypoint
│   │   │   ├── settings.py                  # Project settings, CORS, SimpleJWT, Auth
│   │   │   ├── urls.py                      # Root URL dispatching (/admin/, /api/)
│   │   │   └── wsgi.py                      # WSGI entrypoint
│   │   ├── db.sqlite3                       # Local SQLite database
│   │   └── manage.py                        # Django administrative CLI script
│   ├── env/                                 # Python virtual environment (optional/local)
│   ├── .gitignore                           # Git ignore rules
│   ├── requirements.txt                     # Backend Python dependencies
│   └── README.md                            # Comprehensive full-stack documentation
│
└── BANK_MANAGEMENT_FRONTEND/                # React 19 + Vite Frontend
    ├── bank_management/                     # Vite Application Root
    │   ├── public/                          # Static assets and icons
    │   │   ├── favicon.svg
    │   │   └── icons.svg
    │   ├── src/                             # React Source Code
    │   │   ├── assets/                      # Application images & SVG graphics
    │   │   │   ├── hero.png
    │   │   │   ├── react.svg
    │   │   │   └── vite.svg
    │   │   ├── component/                   # UI View Components
    │   │   │   ├── Accounts.jsx             # Account creation, KYC activation & search
    │   │   │   ├── AccountTypes.jsx         # Account type policy CRUD
    │   │   │   ├── Branches.jsx             # Branch management & staff assignment
    │   │   │   ├── Customers.jsx            # Customer directory & KYC editor
    │   │   │   ├── Dashboard.jsx            # Executive charts & role-based dashboards
    │   │   │   ├── Login.jsx                # Secure login screen with role routing
    │   │   │   ├── Register.jsx             # Customer registration & welcome banner
    │   │   │   ├── StaffList.jsx            # Bank staff directory
    │   │   │   ├── Transactions.jsx         # Txn forms, lookup, password verification & receipts
    │   │   │   └── Vault.jsx                # HQ capital addition & branch fund allocations
    │   │   ├── api.js                       # Axios instance with JWT Bearer token interceptor
    │   │   ├── App.css                      # Global NexaBank styles, themes & UI classes
    │   │   ├── App.jsx                      # Navigation, routes & PrivateRoute auth wrappers
    │   │   ├── index.css                    # Base CSS variables & resets
    │   │   └── main.jsx                     # React root DOM mount point
    │   ├── index.html                       # HTML5 template
    │   ├── package.json                     # Frontend dependencies & scripts
    │   ├── package-lock.json                # Locked dependency tree
    │   └── vite.config.js                   # Vite React plugin configuration
    └── package.json                         # Workspace root package manifest
```

---

## 🗄️ Database Schema & Data Models

```
┌──────────────┐         ┌──────────────┐         ┌──────────────┐
│    Branch    │1       *│     User     │1       1│   Customer   │
├──────────────┼─────────┼──────────────┼─────────┼──────────────┤
│id (PK)       │         │id (PK)       │         │id (PK)       │
│name          │         │username      │         │user_id (FK)  │
│branch_code   │         │role          │         │customer_id   │
│vault_balance │         │branch_id (FK)│         │aadhar_number │
└──────┬───────┘         │pan_number    │         │date_of_birth │
       │                 │aadhar_number │         └──────┬───────┘
       │                 └──────────────┘                │
       │1                                                │1
       │                                                 │
       │*                                                │*
┌──────┴─────────────────────────────────────────────────┴───────┐
│                            Account                             │
├────────────────────────────────────────────────────────────────┤
│id (PK)                                                         │
│customer_id (FK -> Customer)                                    │
│account_type_id (FK -> AccountType)                             │
│branch_id (FK -> Branch)                                        │
│account_number (Unique)                                         │
│balance                                                         │
│status (pending / active / blocked / closed)                    │
└───────────────────────────────┬────────────────────────────────┘
                                │1
                                │
                                │*
                 ┌──────────────┴──────────────┐
                 │         Transaction         │
                 ├─────────────────────────────┤
                 │id (PK)                      │
                 │account_id (FK -> Account)   │
                 │transaction_type (dep/wth/tr)│
                 │amount                       │
                 │balance_after                │
                 │reference (Unique)           │
                 │related_account_id (FK)      │
                 │status                       │
                 └─────────────────────────────┘
```

1. **`User` (`bank.User`)**: Extended Django `AbstractUser` incorporating `role` (`admin`, `staff`, `customer`), `phone`, `pan_number`, `aadhar_number`, and a foreign key to `Branch`.
2. **`Branch`**: Represents physical bank branches with a unique `branch_code`, address details, and its allocated `vault_balance`.
3. **`Customer`**: 1-to-1 profile linked to `User` tracking `customer_id`, `date_of_birth`, residential `address`, and `aadhar_number`.
4. **`AccountType`**: Banking products (e.g. Savings, Current) with a mandatory `minimum_balance` threshold and active flag.
5. **`Account`**: Represents a customer's bank account with unique `account_number`, current `balance`, state machine `status` (`pending`, `active`, `blocked`, `closed`), branch link, and account type link.
6. **`Beneficiary`**: Whitelisted destination accounts linked to a customer for quick transfers.
7. **`Transaction`**: Immutable ledger record storing `transaction_type`, `amount`, `balance_after`, unique 12-char hex `reference`, status, and optional `related_account` for inter-account transfers.
8. **`HQVault`**: Singleton treasury model (`id=1`) maintaining central bank funds.
9. **`FundAllocation`**: Audit trail of capital transfers dispatched from `HQVault` to specific `Branch` vaults.

---

## 🌐 REST API Reference

All backend API endpoints are exposed under the `/api/` prefix.

### Authentication & Staff Management
| Method | Endpoint | Access | Description |
| :--- | :--- | :--- | :--- |
| `POST` | `/api/auth/register/` | Public | Register a new retail customer account |
| `POST` | `/api/auth/login/` | Public | Login with credentials; returns JWT tokens & user profile |
| `POST` | `/api/auth/refresh/` | Public | Refresh expired JWT access token using refresh token |
| `POST` | `/api/auth/register-staff/` | Admin | Provision and assign a new staff member with PAN/Aadhar |
| `GET` | `/api/auth/staff-list/` | Admin | Retrieve directory of all bank staff and assigned branches |

### Branches & Vault Treasury
| Method | Endpoint | Access | Description |
| :--- | :--- | :--- | :--- |
| `GET`, `POST` | `/api/branches/` | Auth / Admin | List all branches (all users) or create branch (Admin) |
| `PUT`, `PATCH` | `/api/branches/<id>/` | Admin | Update branch information |
| `GET`, `POST` | `/api/hq-vault/` | Admin | View central HQ Vault balance or inject capital |
| `GET` | `/api/branch-vault/` | Staff | Retrieve vault balance of staff member's assigned branch |
| `GET`, `POST` | `/api/fund-allocations/` | Admin | View allocation ledger or transfer funds from HQ to a branch |
| `GET` | `/api/financial-summary/` | Admin | Executive summary: charts, monthly trends & branch metrics |

### Accounts & Customers
| Method | Endpoint | Access | Description |
| :--- | :--- | :--- | :--- |
| `GET`, `POST` | `/api/account-types/` | Auth / Admin | List available account types or create new policy (Admin) |
| `DELETE` | `/api/account-types/<id>/` | Admin | Delete account type (protected if accounts are linked) |
| `GET`, `POST` | `/api/customers/` | Authenticated | List customers (scoped by role/branch) or register profile |
| `PATCH` | `/api/customers/<id>/` | Staff / Admin | Update customer KYC details (DOB, Address, Aadhar) |
| `GET`, `POST` | `/api/accounts/` | Authenticated | List accounts (scoped by role) or open new account |
| `PATCH` | `/api/accounts/<id>/` | Staff / Admin | Change account status (e.g., to `active` after KYC validation) |
| `GET` | `/api/accounts/lookup/?account_number=...` | Authenticated | Look up counterparty details (name, branch, status) by number |

### Transactions
| Method | Endpoint | Access | Description |
| :--- | :--- | :--- | :--- |
| `GET` | `/api/transactions/` | Authenticated | List transaction history (scoped to customer, branch, or all) |
| `POST` | `/api/transactions/` | Customer / Staff | Execute deposit, withdrawal, or transfer with strict checks |
| `GET`, `POST` | `/api/beneficiaries/` | Customer | Manage saved transfer beneficiaries |

---

## 🚀 How to Run the Project

### Prerequisites
- **Python**: Version `3.10` or higher installed
- **Node.js**: Version `18.x` or higher installed (`node -v`)
- **npm**: Version `9.x` or higher installed (`npm -v`)
- **Git**

---

### Step 1: Backend Setup (Django)

1. Open your terminal and navigate to the backend project root:
   ```bash
   cd /path/to/BANK_MANAGEMENT_SYSTEM
   ```

2. Create and activate a Python virtual environment:
   ```bash
   # On Linux / macOS:
   python3 -m venv env
   source env/bin/activate

   # On Windows (PowerShell):
   python -m venv env
   .\env\Scripts\Activate.ps1
   ```

3. Install the required Python packages:
   ```bash
   pip install -r requirements.txt
   ```

4. Navigate into the inner `bank_management` directory where `manage.py` is located:
   ```bash
   cd bank_management
   ```

5. Apply database migrations:
   ```bash
   python manage.py migrate
   ```

6. *(Optional)* Create a superuser / admin account if you don't have one:
   ```bash
   python manage.py createsuperuser
   ```

7. Start the Django development server on port `8000`:
   ```bash
   python manage.py runserver 8000
   ```
   > The backend API will be live at: **`http://127.0.0.1:8000/api/`**  
   > The Django Admin panel will be available at: **`http://127.0.0.1:8000/admin/`**

---

### Step 2: Frontend Setup (React + Vite)

1. Open a **new terminal window** and navigate to the Vite frontend directory:
   ```bash
   cd /path/to/BANK_MANAGEMENT_FRONTEND/bank_management
   ```

2. Install the node dependencies:
   ```bash
   npm install
   ```

3. Launch the Vite development server:
   ```bash
   npm run dev
   ```

4. Open your web browser and navigate to:
   ```
   http://localhost:5173
   ```

---

## 🔑 Demo Walkthrough & Testing Roles

To test all the capabilities of the system, test with the following three user workflows:

### Scenario A: Headquarters Admin (`admin`)
1. Log in with your admin credentials.
2. Go to **Vault**: Add capital (e.g. `₹1,000,000`) into the **HQ Vault**, then allocate funds (e.g. `₹200,000`) to a branch.
3. Go to **Branches**: Create a new branch (e.g. *Chennai Central - CH001*) and immediately create a bank staff member assigned to that branch.
4. Go to **Account Types**: Review minimum balances (e.g. Savings: `₹1,000`).
5. Go to **Dashboard**: Inspect the Recharts analytics widgets, branch performance donut chart, and growth trends.

### Scenario B: Branch Staff (`staff`)
1. Log in with the staff user created in Scenario A.
2. The dashboard will show your assigned branch and its live vault liquidity balance.
3. Go to **Accounts**: Onboard a walk-in customer using the customer creation form.
4. Open a new account for this customer (initially in `pending` status).
5. Go to **Customers**: Fill in the customer's KYC details (Date of Birth, Address, 12-digit Aadhar number).
6. Return to **Accounts** and click **Activate Account** (the system validates KYC and activates it).
7. Go to **Transactions**: Process a counter cash **Deposit** or **Withdrawal** on behalf of the customer.

### Scenario C: Retail Customer (`customer`)
1. Go to `/register` and create an online customer account.
2. View your personal **Dashboard** and **Profile**.
3. Go to **Transactions**: Select your active account, enter a destination account number, click **Verify** to view the counterparty's name, enter an amount, type your login password for confirmation, and click **Transfer**.
4. Click the **Print Receipt** button next to the completed transaction to generate an official branded PDF/paper receipt.

---

## 🔒 Security Highlights
- **JWT Protection**: All sensitive banking endpoints verify Bearer tokens via `rest_framework_simplejwt`.
- **CORS Whitelisting**: Strict origin restrictions prevent unauthorized cross-domain calls.
- **SQL Injection & XSS Guard**: Django ORM parameterization and React JSX escaping guard against standard web attack vectors.
- **Password Hashing**: Industry-standard PBKDF2 with SHA256 password hashing.

---

## 📄 License & Attribution
Developed as part of the **NexaBank Full-Stack Banking Suite**.  
Designed and maintained for robust, multi-branch banking simulations and financial software operations.
