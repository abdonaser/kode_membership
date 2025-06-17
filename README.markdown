# 🏋️‍♂️ KODE Sports Club Membership - Odoo Module

```markdown
This Odoo module provides a comprehensive membership management system for **KODE Sports Club**, handling member registration, branch assignments, blacklist workflows, revision requests, and detailed reporting.

---

## 📦 Module Features

### ✅ Member Management

- Manage member profiles with English/Arabic names, images, and branch assignments.
- Track membership status: `Draft`, `Approved`, `Black List`.
- Link to `res.partner` for seamless integration.
- Compute renewal details (last order, date, total amount).

### 🏢 Branch Management

- Create and manage club branches with unique names and locations.
- Assign members to multiple branches (many-to-many).
- Track the number of members per branch.

### ⛔ Blacklist Workflow

- Blacklist members with reasons via a dedicated wizard.
- Store blacklist history in `kode.blacklist.history`.

### 🔄 Revision Request Workflow

- Request blacklist status revisions through a wizard.
- Prevent duplicate pending requests.
- Managers can `Accept` or `Deny` requests, with `Accepted` resetting member status to `Draft`.

### 🛡️ Access Control

- **Manager Group**: Full access to all members and revision workflows.
- **User Group**: View only `Approved` or `Black List` members.
- Managers control revision status changes.

### 📄 Reporting

- **Excel Report**: Download member details with names, status, renewal data, and currency.
- **QWeb Report**: Printable HTML report with member info and assigned branches, styled with Bootstrap.

---

## 🗂️ Module Structure

kode_membership/
│
├── models/
│ ├── kode_member.py
│ ├── kode_branch.py
│ ├── blacklist_history.py
│ ├── blacklist_revision_request.py
│ ├── blacklist_wizard.py
│ ├── revision_request_wizard.py
│
├── wizards/
│ ├── blacklist_wizard_view.xml
│ ├── revision_request_wizard_view.xml
│
├── reports/
│ ├── xlsx_member_report.py
│ ├── member_report.xml
│
├── security/
│ ├── groups.xml
│ ├── rules.xml
│ ├── ir.model.access.csv
│
├── data/
│ ├── ir_sequence_data.xml
│
├── views/
│ ├── menus.xml
│ ├── kode_member_views.xml
│ ├── kode_branch_views.xml
│ ├── res_partner_view.xml
│ ├── blacklist_history_view.xml
│ ├── blacklist_revision_request_view.xml
│
└── README.md ← You are here!
```

---

## 🔐 Security & Permissions

### Groups (`groups.xml`)

- **Manager**: `group_membership_manager`
- **User**: `group_membership_user`

### Record Rules (`rules.xml`)

- Users: Access only `Approved` or `Black List` members.
- Managers: Full access to all members.

### Access Rights (`ir.model.access.csv`)

| Model                             | Manager | User    | Public  |
| --------------------------------- | ------- | ------- | ------- |
| `kode.member`                     | ✅ Full | ✅ R/W  | ❌      |
| `kode.branch`                     | ✅ Full | ✅ Full | ✅ Full |
| `kode.blacklist.history`          | ✅ Full | ✅ Full | ✅ Full |
| `kode.blacklist.revision.request` | ✅ Full | ✅ Full | ✅ Full |
| `kode.blacklist.wizard`           | ✅ Full | ✅ Full | ✅ Full |
| `kode.revision.request.wizard`    | ✅ Full | ✅ Full | ✅ Full |
| `res.partner`                     | ✅ Full | ✅ Full | ✅ Full |

---

## 🧠 Business Logic Highlights

- Unique codes generated for members, branches, blacklist entries, and revision requests using sequences.
- Only **Managers** can update revision request statuses (`revision_status`).
- `Accepted` revision requests reset member status to `Draft`.
- Prevents duplicate pending revision requests per blacklist entry.
- Tracks user actions and status changes via `mail.thread` and `mail.activity.mixin`.

---

## 📤 Excel Report (`xlsx_member_report.py`)

- **Route**: `/member/excel/report/<member_ids>`
- Generates an Excel file with:
  - English Full Name
  - Arabic Full Name
  - First Name
  - Last Name
  - Status
  - Last Renewal Date
  - Total Last Renewal Order (with currency)
- Features formatted headers, alternating row colors, and frozen panes.

### Sample Headers:

```
English Full Name | Arabic Full Name | First Name | Last Name | Status | Last Renewal Date | Total Last Renewal Order
```

---

## 🖨️ QWeb Report (`member_report.xml`)

- Printable HTML report including:
  - Member details (English/Arabic names, status, renewal info).
  - Assigned branches with names and locations.
- Styled with Bootstrap for a modern, professional look.

---

## 🚀 Future Enhancements (Suggestions)

- Add email notifications for blacklist/revision updates.
- Implement blacklist duration tracking and automatic expiry.
- Enhance reporting with filters (e.g., by branch, status, or renewal date).
- Add dashboard widgets for quick insights (e.g., member counts, blacklist status).

---

## 🧩 Dependencies

- Built for **Odoo 17** (or later).
- Requires: `base`, `mail`, `sale`.
- Utilizes Odoo features: `mail.thread`, `ir.model.access`, `ir.rule`, QWeb, and Excel reporting.

---

## 👤 Author

**Abdelrahman Naser**  
Front-End & Odoo Developer | Cairo, Egypt  
📍 [LinkedIn](https://www.linkedin.com/in/abdelrahman-naser-muhammed)  
📂 [GitHub](https://github.com/abdonaser)

---

## 📃 License

This module is developed for private use by **KODE Sports Club** and is licensed under **OPL-1 (Odoo Proprietary License)**.
