# PLAN-newsletter-history.md - Newsletter Sending History Log

This document outlines the detailed implementation plan to introduce a newsletter campaign history recorder. This feature will track and log all newsletter campaigns sent by admins, showing the subject, date, recipient count, and content summary.

---

## 🏛️ Objective
Introduce a persistent record of sent newsletters so that administrator users can review previous announcements, inspect who received them, and track historical outreach performance.

---

## 🏛️ Proposed Changes

### 1. Database Model (`modules/notifications/models.py`)
Add a new SQLAlchemy model `NewsletterHistory` to store the historical logs.

```python
class NewsletterHistory(db.Model):
    __tablename__ = 'NEWSLETTER_HISTORY'
    id = db.Column(db.Integer, primary_key=True)
    subject = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text, nullable=False)
    recipient_count = db.Column(db.Integer, default=0)
    sent_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<NewsletterHistory {self.subject}>'
```

### 2. Register with Import Shim (`models.py`)
Import the new model in the core model import hub at the root of the project to ensure SQLAlchemy registers it correctly.
```python
# notifications models shim
from modules.notifications.models import NewsletterSubscriber, NewsletterHistory
```

### 3. Record History on Compose (`routes/admin/newsletter.py`)
When sending a newsletter successfully:
- In the POST handler of `compose()`, instantiate a new `NewsletterHistory` record.
- Populate `subject`, `content`, and `recipient_count` (which equals `success_count`).
- Commit the record to the database along with the mailing events.

### 4. Create History Route (`routes/admin/newsletter.py`)
Define a new route to render the list of past newsletters.
- **Route**: `/admin/newsletter/history`
- **Method**: `GET`
- **Controller**:
  ```python
  @newsletter_admin_bp.route("/admin/newsletter/history")
  @login_required
  @admin_required
  def history():
      """List historical newsletter campaigns."""
      history_records = NewsletterHistory.query.order_by(NewsletterHistory.sent_at.desc()).all()
      return render_template("admin/newsletter/history.html", history=history_records)
  ```
- **Optional Route**: `/admin/newsletter/history/<int:id>` to view the full details/body of a specific historical email.

### 5. Create History Template (`templates/admin/newsletter/history.html`)
Design a high-quality dashboard component utilizing the app's established design token styles:
- Sleek modern grid/table layout inside glass-cards.
- Display `Sent Date` (formatted), `Subject`, `Recipient Count`, and a "View" action button.
- A modal or side-drawer using standard CSS/JS or a dedicated page to view the sanitized newsletter content.

### 6. Update Navigation / Index (`templates/admin/newsletter/index.html`)
Add a new action button next to "Compose Newsletter" and "Export CSV" to navigate to the Newsletter History page:
```html
<a href="{{ url_for('newsletter_admin.history') }}" class="px-8 py-4 bg-white border border-emerald-900/10 text-emerald-950 rounded-2xl font-bold hover:bg-emerald-50 transition flex items-center gap-2">
    <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
    </svg>
    View History
</a>
```

---

## ❓ Open Questions / Decisions
1. **Details Page vs Modal**: Should clicking "View" open a dedicated page showing the email details, or open a secure HTML preview modal inline? *Recommended: A clean modal or a dedicated preview page so the layout is not broken by the custom HTML stored in the newsletter.*
2. **Recipient List Storage**: Do we need to track exactly which email addresses received which campaign? (This requires a many-to-many junction table, which increases database weight. A simple `recipient_count` is usually preferred for basic analytics). *We plan to use `recipient_count` first unless granular subscriber-level receipt tracking is requested.*

---

## 🏁 Verification & Testing Plan
1. **Database Schema Setup**: Run the server locally. Verify that the table `NEWSLETTER_HISTORY` is successfully created by Sqlite.
2. **Feature Workflow**:
   - Compose a newsletter, target it to a few subscribers, and click send.
   - Verify that the newsletter is processed.
   - Access `/admin/newsletter/history` and check if the campaign appears correctly.
   - View details and confirm the subject and body render nicely.
3. **Automated Tests**:
   - Create a basic pytest model validation unit test in `tests/test_notifications.py` (if test suite is initialized).
