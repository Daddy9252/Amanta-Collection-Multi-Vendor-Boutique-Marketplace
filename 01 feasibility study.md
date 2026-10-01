# 1. Feasibility Study — Amanta Collection

## 1.1 Technical Feasibility
Amanta Collection is built using Flask (Python), SQLite, SQLAlchemy, and Bootstrap — all free, open-source, well-documented technologies that run on standard student hardware (Windows/Mac/Linux) with modest requirements (Python 3.x, ~200MB disk, 4GB+ RAM). No specialized hardware, licenses, or paid services are required. The stack is proven for small-to-medium web applications.

**Conclusion: Technically feasible.**

## 1.2 Economic Feasibility
- **Development cost:** £0 — all tools (Python, Flask, SQLite, VS Code, Bootstrap CDN) are free and open-source.
- **Hosting (if deployed):** Free tiers exist (e.g., PythonAnywhere, Render) sufficient for demonstration purposes.
- **Maintenance cost:** Minimal — single-developer project, no ongoing subscription costs during coursework.

**Conclusion: Economically feasible.**

## 1.3 Operational Feasibility
- Target users (buyers, vendors, admins) perform tasks analogous to existing platforms they already understand (e.g. Etsy, ASOS Marketplace), so the learning curve is low.
- The interface uses familiar e-commerce conventions (search bar, product cards, cart icon, checkout flow).
- Role-based dashboards mean each user type only sees relevant functionality.

**Conclusion: Operationally feasible.**

## 1.4 Legal Feasibility
- No real payment processing means no PCI-DSS compliance burden for this coursework version.
- User data (names, emails, hashed passwords) is stored locally in SQLite for demo purposes only.
- All third-party libraries used (Flask, SQLAlchemy, Bootstrap, etc.) are open-source with permissive licenses (BSD/MIT).
- Any research data (interviews/questionnaires) not genuinely collected is clearly disclosed as simulated/example data.

**Conclusion: Legally feasible within an academic/demo context.**

## 1.5 Schedule Feasibility

| Phase | Estimated Duration |
|---|---|
| Planning & Analysis | 1 week |
| Design | 1 week |
| Development | 2–3 weeks |
| Security, Testing, Docs | 1 week |
| Final Report & Submission | 1 week |

**Total: ~6–7 weeks**, assuming steady part-time effort — feasible for a typical coursework deadline (adjust against your actual deadline).

**Conclusion: Schedule feasible.**
