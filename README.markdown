
```markdown
# 🏋️‍♂️ KODE Membership Management - Odoo Module

This module provides a complete membership management system for **KODE Sports Club**, supporting the lifecycle of member registration, blacklisting, revision requests, and reporting.

---

## 📦 Module Features

### ✅ Member Management
- Manage member details including names, images, partner links, and branches.
- Status tracking: `draft`, `approved`, `black_list`.

### 🛡️ Access Control
- **Manager Group**: Full access to members and revision workflows.
- **User Group**: Limited access to approved and blacklisted members only.

### ⛔ Blacklisting Workflow
- Blacklist members with reasons using a dedicated wizard.
- Record stored in `kode.blacklist.history`.

### 🔄 Revision Request Workflow
- Request a revision to a blacklisted member’s status via a wizard.
- Only one pending request per blacklist entry is allowed.
- Managers can `accept` or `deny` requests.
- Upon acceptance, the member's status is set back to `draft`.

### 📄 Reporting
- **Excel Report**: Download detailed member reports with financials.
- **HTML Print Report**: Elegant QWeb report including personal and branch information.

---

## 🗂️ Module Structure

```

kode\_membership/
│
├── models/
│   ├── kode\_member.py
│   ├── blacklist\_history.py
│   ├── blacklist\_revision\_request.py
│   └── ...
│
├── wizards/
│   ├── blacklist\_wizard.py
│   └── revision\_request\_wizard.py
│
├── reports/
│   ├── xlsx\_member\_report.py
│   └── member\_report.xml
│
├── security/
│   ├── ir.model.access.csv
│   ├── rules.xml
│   └── groups.xml
│
├── views/
│   └── \*.xml (not included here)
│
└── README.md  ← You are here!

```

---

## 🔐 Security & Permissions

### Groups (`groups.xml`)
- **Manager**: `group_membership_manager`
- **User**: `group_membership_user`

### Record Rules (`rules.xml`)
- Users see only `approved` or `black_list` members.
- Managers see all members.

### Access Rights (`ir.model.access.csv`)
| Model                            | Manager | User | Public |
|----------------------------------|---------|------|--------|
| `kode.member`                   | ✅ Full | ✅ R/W | ❌     |
| `kode.blacklist.history`       | ✅ Full | ✅ Full | ✅     |
| `kode.blacklist.revision.request` | ✅ Full | ✅ Full | ✅     |
| `wizards` (both)                | ✅ Full | ✅ Full | ✅     |

---

## 🧠 Business Logic Highlights

- Only **Managers** can change the `revision_status`.
- When a revision is **accepted**, member status becomes `draft`.
- Revision request duplicates are prevented (must resolve the pending one first).
- Status transitions and user actions are tracked via `mail.thread`.

---

## 📤 Excel Report (`xlsx_member_report.py`)

- Route: `/member/excel/report/<member_ids>`
- Returns an Excel file including:
  - Names
  - Status
  - Last renewal date
  - Total amount
  - Currency
  - Branches

### Sample Headers:
```

English Full Name | Arabic Full Name | Status | Renewal Date | Total Last Order

```

---

## 🖨️ QWeb Report (`member_report.xml`)

- Elegant printable report showing:
  - Member information
  - Renewal history
  - Assigned branches
  - Styled with Bootstrap layout

---

## 🚀 Future Enhancements (Suggestions)
- Add approval/rejection messages on revision decisions.
- Track blacklist duration and expiry.
- Send automated email notifications on blacklist or revision updates.
- Add filters for reporting (e.g. by branch or renewal date).

---

## 🧩 Dependencies
- Built on **Odoo 17**
- Uses standard `mail.thread`, `ir.model.access`, `ir.rule`, 'sale', and QWeb reporting features.

---

## 👤 Author
**Abdelrahman Naser**
Front-End & Odoo Developer | Cairo, Egypt

---

## 📃 License
This module is developed for private use by **KODE Sports Club** and is not publicly licensed unless specified.

---
```

---

## 👨‍💻 Author & Maintainer

**Abdelrahman Naser**  
📍 [LinkedIn](https://www.linkedin.com/in/abdelrahman-naser-muhammed)  
📂 [GitHub](https://github.com/abdonaser)