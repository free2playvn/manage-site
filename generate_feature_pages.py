from pathlib import Path

base = Path('.')

sidebar = '''
    <aside class="sidebar" id="sidebar">
      <div class="sidebar-top">
        <a class="brand" href="index.html">
          <span class="brand-mark">
            <svg viewBox="0 0 24 24" aria-hidden="true">
              <path d="M12 3L2 12h3l7-7 7 7h3L12 3z"></path>
              <path d="M5 13h14v8H5z"></path>
            </svg>
          </span>
          <span class="brand-text">CompanyHub</span>
        </a>
        <button class="icon-button sidebar-close mobile-hidden" id="closeSidebar" aria-label="Close sidebar">
          <svg viewBox="0 0 24 24">
            <path d="M6 6l12 12M18 6L6 18"></path>
          </svg>
        </button>
      </div>

      <div class="account-card">
        <div class="account-avatar">RB</div>
        <div class="account-meta">
          <span class="account-label">Enterprise Admin</span>
          <span class="account-name">Rina Bennett</span>
        </div>
      </div>

      <div class="sidebar-section">
        <span class="side-label">Workspace</span>
        <nav class="nav">
          <a class="nav-link" href="index.html">
            <span class="nav-icon">
              <svg viewBox="0 0 24 24"><path d="M4 13h7l3-7 3 14 2-7h4"></path></svg>
            </span>
            <span>Overview</span>
            <span class="nav-arrow">›</span>
          </a>
          <a class="nav-link" href="departments.html">
            <span class="nav-icon"><svg viewBox="0 0 24 24"><path d="M4 7h16v6H4z"></path><path d="M4 15h16v6H4z"></path></svg></span>
            <span>Departments</span>
            <span class="nav-arrow">›</span>
          </a>
          <a class="nav-link" href="employees.html">
            <span class="nav-icon"><svg viewBox="0 0 24 24"><path d="M16 8a4 4 0 1 0-8 0 4 4 0 0 0 8 0z"></path><path d="M3 20a7 7 0 0 1 14 0"></path></svg></span>
            <span>People</span>
            <span class="nav-arrow">›</span>
          </a>
          <a class="nav-link" href="roles.html">
            <span class="nav-icon"><svg viewBox="0 0 24 24"><path d="M4 18L10 12l4 4 6-8"></path><path d="M4 5h16v18H4z"></path></svg></span>
            <span>Roles & Access</span>
            <span class="nav-arrow">›</span>
          </a>
          <a class="nav-link" href="projects.html">
            <span class="nav-icon"><svg viewBox="0 0 24 24"><path d="M3 12h7l4-7 4 14 3-7h4"></path></svg></span>
            <span>Projects</span>
            <span class="nav-arrow">›</span>
          </a>
          <a class="nav-link" href="documents.html">
            <span class="nav-icon"><svg viewBox="0 0 24 24"><path d="M4 4h11l5 5v15H4z"></path><path d="M14 4v6h6"></path></svg></span>
            <span>Documents</span>
            <span class="nav-arrow">›</span>
          </a>
          <a class="nav-link" href="permissions.html">
            <span class="nav-icon"><svg viewBox="0 0 24 24"><path d="M7 11V7a5 5 0 0 1 10 0v4"></path><path d="M5 11h14v10H5z"></path></svg></span>
            <span>Permissions</span>
            <span class="nav-arrow">›</span>
          </a>
        </nav>
      </div>

      <div class="sidebar-section">
        <span class="side-label">Company Structure</span>
        <div class="structure-card">
          <div class="structure-top">
            <div>
              <span class="structure-title">Global Operations</span>
              <span class="structure-subtitle">24 Teams</span>
            </div>
            <span class="structure-badge">Live</span>
          </div>
          <div class="structure-map">
            <div class="structure-line"></div>
            <div class="structure-node"><span class="node-dot"></span><span class="node-label">Executive</span></div>
            <div class="structure-node"><span class="node-dot"></span><span class="node-label">Operations</span></div>
            <div class="structure-node"><span class="node-dot"></span><span class="node-label">Technology</span></div>
            <div class="structure-node"><span class="node-dot"></span><span class="node-label">Commercial</span></div>
          </div>
        </div>
      </div>

      <div class="sidebar-footer">
        <button class="button button-dark">
          <span class="button-icon"><svg viewBox="0 0 24 24"><path d="M5 12h14"></path><path d="M13 3l9 9-9 9"></path></svg></span>
          <span>Sync Directory</span>
        </button>
      </div>
    </aside>
'''

topbar = '''
      <section class="topbar">
        <div class="topbar-left">
          <button class="icon-button mobile-only" id="menuToggle" aria-label="Open menu">
            <svg viewBox="0 0 24 24"><path d="M4 7h16"></path><path d="M4 12h16"></path><path d="M4 17h16"></path></svg>
          </button>
          <div class="crumbs">
            <span class="crumb-home">Workspace</span>
            <span class="crumb-divider">/</span>
            <span class="crumb-current">Company Administration</span>
          </div>
        </div>

        <div class="topbar-right">
          <div class="search-wrap">
            <svg viewBox="0 0 24 24" class="search-icon"><path d="M11 19a8 8 0 1 0 0-16 8 8 0 0 0 0 16z"></path><path d="m21 21-4.2-4.2"></path></svg>
            <input type="search" id="search" placeholder="Search people or roles" />
          </div>
          <button class="icon-button notification">
            <svg viewBox="0 0 24 24"><path d="M18 8a6 6 0 0 0-12 0c0 7-3 7.5 0 10h12c3-2.5 0-3 0-10z"></path><path d="M10 21h4"></path></svg>
            <span class="notification-dot"></span>
          </button>
          <button class="button button-primary">
            <span class="button-icon"><svg viewBox="0 0 24 24"><path d="M12 5v14"></path><path d="M5 12h14"></path></svg></span>
            <span>Create Team</span>
          </button>
        </div>
      </section>
'''

page_start = '''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>CompanyHub | {title}</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=Space+Grotesk:wght@500;600;700&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="styles.css" />
</head>
<body>
  <div class="app-backdrop" id="appBackdrop" aria-hidden="true"></div>
  <div class="app-shell">
'''

page_end = '''
  </main>
  </div>
  <script src="app.js"></script>
</body>
</html>
'''

pages = [
    {"file":"departments.html", "title":"Departments", "heading":"Departments", "resource":"departments", "list_id":"department-list", "summary":"Department structure", "kind":"resource"},
    {"file":"employees.html", "title":"Employees", "heading":"People Directory", "resource":"employees", "list_id":"people-table", "summary":"People directory", "kind":"employees"},
    {"file":"roles.html", "title":"Roles", "heading":"Roles & Access", "resource":"roles", "list_id":"role-list", "summary":"Role permissions", "kind":"resource"},
    {"file":"devices.html", "title":"Devices", "heading":"Work Devices", "resource":"devices", "list_id":"device-list", "summary":"Work devices", "kind":"resource"},
    {"file":"projects.html", "title":"Projects", "heading":"Projects", "resource":"projects", "list_id":"project-list", "summary":"Project portfolio", "kind":"resource"},
    {"file":"documents.html", "title":"Documents", "heading":"Documents", "resource":"documents", "list_id":"document-list", "summary":"Documents", "kind":"resource"},
    {"file":"permissions.html", "title":"Permissions", "heading":"Permissions", "resource":"permissions", "list_id":"permission-list", "summary":"Permission grants", "kind":"resource"},
    {"file":"salaries.html", "title":"Salaries", "heading":"Employee Salary", "resource":"salaries", "list_id":"salary-list", "summary":"Salaries", "kind":"resource"},
    {"file":"benefits.html", "title":"Benefits", "heading":"Employee Benefits", "resource":"benefits", "list_id":"benefit-list", "summary":"Benefits", "kind":"resource"},
    {"file":"leave.html", "title":"Leave", "heading":"On Leave", "resource":"leave_requests", "list_id":"leave-list", "summary":"Leave requests", "kind":"resource"},
    {"file":"timekeeping.html", "title":"Timekeeping", "heading":"Timekeeping", "resource":"timekeeping", "list_id":"timekeeping-list", "summary":"Timekeeping", "kind":"resource"},
    {"file":"create-account.html", "title":"Create Account", "heading":"Create Account", "resource":"accounts", "list_id":"create-account-form", "summary":"Account flow", "kind":"form"},
    {"file":"profile.html", "title":"Employee Profile", "heading":"Employee Profile", "resource":"profile", "list_id":"profile-form", "summary":"Profile flow", "kind":"form"},
    {"file":"leave-register.html", "title":"Register Leave", "heading":"Register Leave", "resource":"leave_register", "list_id":"leave-form", "summary":"Leave request flow", "kind":"form"},
    {"file":"tasks-update.html", "title":"Update Tasks", "heading":"Update Tasks", "resource":"tasks", "list_id":"task-form", "summary":"Task flow", "kind":"form"},
    {"file":"leave-approve.html", "title":"Approve Leave", "heading":"Approve Leave", "resource":"approve_leave", "list_id":"approve-leave-form", "summary":"Approval flow", "kind":"form"},
    {"file":"capacity.html", "title":"Employee Capacity", "heading":"Evaluate Capacity", "resource":"employee_capacity", "list_id":"capacity-list", "summary":"Capacity scoring", "kind":"resource"},
]

# Create all HTML pages with shared shell and one resource workflow region.
for page in pages:
    filename = page["file"]
    heading = page["heading"]
    title = page["title"]
    kind = page["kind"]
    list_id = page["list_id"]

    if kind == 'resource':
        resource_html = f'''
      <section class="feature-page">
        <section class="panel resource-panel">
          <div class="panel-head">
            <div>
              <span class="panel-kicker">{page['summary']}</span>
              <h2>{heading}</h2>
            </div>
            <button class="button button-chip">Manage</button>
          </div>
          <div class="resource-list {page['resource']}-list" id="{list_id}"></div>
        </section>
      </section>
'''
    elif kind == 'employees':
        resource_html = '''
      <section class="feature-page">
        <section class="panel table-panel resource-panel">
          <div class="panel-head">
            <div>
              <span class="panel-kicker">People Directory</span>
              <h2>Position Management</h2>
            </div>
            <div class="panel-actions">
              <button class="button button-chip filter-chip active" data-filter="all">All</button>
              <button class="button button-chip filter-chip" data-filter="executive">Executive</button>
              <button class="button button-chip filter-chip" data-filter="operations">Operations</button>
              <button class="button button-chip filter-chip" data-filter="technology">Technology</button>
            </div>
          </div>
          <div class="people-table-wrap">
            <table class="people-table" id="people-table">
              <thead>
                <tr>
                  <th>Employee</th>
                  <th>Position</th>
                  <th>Department</th>
                  <th>Team</th>
                  <th>Status</th>
                  <th>Access</th>
                  <th></th>
                </tr>
              </thead>
              <tbody></tbody>
            </table>
          </div>
        </section>
      </section>
'''
    elif kind == 'form':
        if filename == 'create-account.html':
            resource_html = '''
      <section class="feature-page">
        <section class="panel workflow-panel resource-panel">
          <div class="panel-head compact">
            <div>
              <span class="panel-kicker">Identity Access</span>
              <h2>Create Account</h2>
            </div>
            <button class="button button-chip">Admin</button>
          </div>
          <form class="workflow-form" id="create-account-form">
            <div class="form-field">
              <label for="account-name">Full Name</label>
              <input type="text" id="account-name" name="name" placeholder="Employee name" required />
            </div>
            <div class="form-field">
              <label for="account-email">Email</label>
              <input type="email" id="account-email" name="email" placeholder="employee@companyhub.com" required />
            </div>
            <div class="form-field">
              <label for="account-password">Password</label>
              <input type="password" id="account-password" name="password" placeholder="••••••••" required />
            </div>
            <div class="form-field">
              <label for="account-role">Role</label>
              <select id="account-role" name="role" required>
                <option value="employee">Employee</option>
                <option value="admin">Admin</option>
              </select>
            </div>
            <button class="button button-primary form-button" type="submit">Create Account</button>
            <div class="form-message" id="account-message"></div>
          </form>
        </section>
      </section>
'''
        elif filename == 'profile.html':
            resource_html = '''
      <section class="feature-page">
        <section class="panel workflow-panel resource-panel">
          <div class="panel-head compact">
            <div>
              <span class="panel-kicker">Employee Directory</span>
              <h2>Check Profile</h2>
            </div>
            <button class="button button-chip">Self Info</button>
          </div>
          <form class="workflow-form" id="profile-form">
            <div class="form-field">
              <label for="profile-email">Employee Email</label>
              <input type="email" id="profile-email" name="email" placeholder="employee@companyhub.com" required />
            </div>
            <button class="button button-primary form-button" type="submit">View Profile</button>
            <div class="profile-result" id="profile-result">
              <span class="profile-empty">No employee selected</span>
            </div>
          </form>
        </section>
      </section>
'''
        elif filename == 'leave-register.html':
            resource_html = '''
      <section class="feature-page">
        <section class="panel workflow-panel resource-panel">
          <div class="panel-head compact">
            <div>
              <span class="panel-kicker">Workforce Leave</span>
              <h2>Register Leave</h2>
            </div>
            <button class="button button-chip">Request</button>
          </div>
          <form class="workflow-form" id="leave-form">
            <div class="form-field">
              <label for="leave-employee">Employee</label>
              <input type="text" id="leave-employee" name="employee" placeholder="Employee name" required />
            </div>
            <div class="form-field">
              <label for="leave-department">Department</label>
              <input type="text" id="leave-department" name="department" placeholder="Operations" required />
            </div>
            <div class="form-field">
              <label for="leave-type">Leave Type</label>
              <select id="leave-type" name="leave_type" required>
                <option value="Annual Leave">Annual Leave</option>
                <option value="Medical Leave">Medical Leave</option>
                <option value="Training Leave">Training Leave</option>
                <option value="Personal Leave">Personal Leave</option>
              </select>
            </div>
            <div class="form-row">
              <div class="form-field">
                <label for="leave-start-date">Start Date</label>
                <input type="date" id="leave-start-date" name="start_date" required />
              </div>
              <div class="form-field">
                <label for="leave-end-date">End Date</label>
                <input type="date" id="leave-end-date" name="end_date" required />
              </div>
            </div>
            <div class="form-row">
              <div class="form-field">
                <label for="leave-days">Days</label>
                <input type="number" id="leave-days" name="days" min="1" value="1" required />
              </div>
              <div class="form-field">
                <label for="leave-reviewer">Reviewer</label>
                <input type="text" id="leave-reviewer" name="reviewer" placeholder="Approver" required />
              </div>
            </div>
            <button class="button button-primary form-button" type="submit">Submit Leave</button>
            <div class="form-message" id="leave-message"></div>
          </form>
        </section>
      </section>
'''
        elif filename == 'tasks-update.html':
            resource_html = '''
      <section class="feature-page">
        <section class="panel workflow-panel resource-panel">
          <div class="panel-head compact">
            <div>
              <span class="panel-kicker">Documents & Tasks</span>
              <h2>Update Task</h2>
            </div>
            <button class="button button-chip">Task</button>
          </div>
          <form class="workflow-form" id="task-form">
            <div class="form-field">
              <label for="task-id">Task ID</label>
              <input type="number" id="task-id" name="id" min="1" placeholder="1" required />
            </div>
            <div class="form-field">
              <label for="task-title">Task Title</label>
              <input type="text" id="task-title" name="title" placeholder="Task title" required />
            </div>
            <div class="form-row">
              <div class="form-field">
                <label for="task-status">Status</label>
                <select id="task-status" name="status">
                  <option value="Open">Open</option>
                  <option value="In Progress">In Progress</option>
                  <option value="Pending">Pending</option>
                  <option value="Completed">Completed</option>
                </select>
              </div>
              <div class="form-field">
                <label for="task-priority">Priority</label>
                <select id="task-priority" name="priority">
                  <option value="Low">Low</option>
                  <option value="Medium">Medium</option>
                  <option value="High">High</option>
                  <option value="Critical">Critical</option>
                </select>
              </div>
            </div>
            <div class="form-row">
              <div class="form-field">
                <label for="task-due-date">Due Date</label>
                <input type="date" id="task-due-date" name="due_date" required />
              </div>
              <div class="form-field">
                <label for="task-assignee">Assignee</label>
                <input type="text" id="task-assignee" name="assignee" placeholder="Assignee" required />
              </div>
            </div>
            <div class="form-row">
              <div class="form-field">
                <label for="task-department">Department</label>
                <input type="text" id="task-department" name="department" placeholder="Technology" required />
              </div>
              <div class="form-field">
                <label for="task-document-id">Document ID</label>
                <input type="number" id="task-document-id" name="document_id" min="1" placeholder="1" />
              </div>
            </div>
            <div class="form-field">
              <label for="task-description">Description</label>
              <textarea id="task-description" name="description" rows="3" placeholder="Description" required></textarea>
            </div>
            <button class="button button-primary form-button" type="submit">Update Task</button>
            <div class="form-message" id="task-message"></div>
          </form>
        </section>
      </section>
'''
        elif filename == 'leave-approve.html':
            resource_html = '''
      <section class="feature-page">
        <section class="panel workflow-panel resource-panel">
          <div class="panel-head compact">
            <div>
              <span class="panel-kicker">Leave Approver</span>
              <h2>Approve On-Leave</h2>
            </div>
            <button class="button button-chip">Review</button>
          </div>
          <form class="workflow-form" id="approve-leave-form">
            <div class="form-field">
              <label for="approve-leave-id">Leave Request ID</label>
              <input type="number" id="approve-leave-id" name="id" placeholder="1" required />
            </div>
            <div class="form-field">
              <label for="approve-leave-status">Decision</label>
              <select id="approve-leave-status" name="status">
                <option value="Approved">Approve</option>
                <option value="Rejected">Reject</option>
                <option value="Pending">Pending</option>
              </select>
            </div>
            <div class="form-field">
              <label for="approve-leave-reviewer">Reviewer</label>
              <input type="text" id="approve-leave-reviewer" name="reviewer" placeholder="Admin" required />
            </div>
            <button class="button button-primary form-button" type="submit">Submit Decision</button>
            <div class="form-message" id="approve-leave-message"></div>
          </form>
        </section>
      </section>
'''
    # End if

    html = page_start.format(title=title) + sidebar + '<main class="main-content">' + topbar + '''
      <section class="page-heading">
        <div>
          <span class="section-kicker">Organization Dashboard</span>
          <h1>{}</h1>
        </div>
        <div class="heading-actions">
          <div class="date-card">
            <span class="date-label">Today</span>
            <span class="date-value" id="todayDate">September 09, 2026</span>
          </div>
          <button class="button button-soft">
            <span class="button-icon"><svg viewBox="0 0 24 24"><path d="M3 12h18"></path><path d="M12 3l9 9-9 9"></path></svg></span>
            <span>Export Report</span>
          </button>
        </div>
      </section>
'''.format(heading) + resource_html + page_end

    # Write HTML
    (base / filename).write_text(html, encoding='utf-8')

print('generated', len(pages), 'feature pages')
