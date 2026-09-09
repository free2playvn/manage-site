const API_BASE = 'http://127.0.0.1:8001';

function escapeHtml(value) {
  return String(value ?? '').replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;').replace(/'/g, '&#39;');
}

const menuToggle = document.getElementById('menuToggle');
const closeSidebar = document.getElementById('closeSidebar');
const sidebar = document.getElementById('sidebar');

if (menuToggle && sidebar) {
  menuToggle.addEventListener('click', () => {
    sidebar.classList.toggle('open');
  });
}

if (closeSidebar && sidebar) {
  closeSidebar.addEventListener('click', () => {
    sidebar.classList.remove('open');
  });
}

const today = new Date();
const dateEl = document.getElementById('todayDate');
if (dateEl) {
  const dateOptions = { year: 'numeric', month: 'long', day: 'numeric' };
  dateEl.textContent = today.toLocaleDateString('en-US', dateOptions);
}

const filterButtons = Array.from(document.querySelectorAll('.filter-chip'));
const rows = Array.from(document.querySelectorAll('#people-table tbody tr'));

filterButtons.forEach(button => {
  button.addEventListener('click', () => {
    const role = button.dataset.filter;

    filterButtons.forEach(item => item.classList.toggle('active', item === button));

    rows.forEach(row => {
      const visible = role === 'all' || row.dataset.role === role;
      row.style.display = visible ? '' : 'none';
    });
  });
});

const navLinks = Array.from(document.querySelectorAll('.nav-link'));
navLinks.forEach(link => {
  link.addEventListener('click', event => {
    event.preventDefault();
    navLinks.forEach(item => item.classList.toggle('active', item === link));
  });
});

function updateStats(stats) {
  const statCards = {
    users: document.querySelector('.stat-card:nth-child(1) .stat-number'),
    departments: document.querySelector('.stat-card:nth-child(2) .stat-number'),
    managers: document.querySelector('.stat-card:nth-child(3) .stat-number'),
    access: document.querySelector('.stat-card:nth-child(4) .stat-number')
  };

  if (statCards.users) statCards.users.textContent = stats.total_users || 286;
  if (statCards.departments) statCards.departments.textContent = stats.departments || 9;
  if (statCards.managers) statCards.managers.textContent = stats.managers || 34;
  if (statCards.access) statCards.access.textContent = stats.access_level || '76%';
}

function renderPeople(data) {
  const roleRows = Array.from(document.querySelectorAll('#people-table tbody tr'));
  if (roleRows.length >= (data.employees || []).length) return;

  const tbody = document.querySelector('#people-table tbody');
  if (!tbody || !Array.isArray(data.employees)) return;

  data.employees.slice(0, 8).forEach(employee => {
    const tr = document.createElement('tr');
    const departmentRole = (employee.department || '').toLowerCase();
    tr.dataset.role = departmentRole;
    tr.innerHTML = `
      <td>
        <div class="person">
          <span class="person-avatar avatar-one">${escapeHtml(employee.avatar)}</span>
          <div>
            <span class="person-name">${escapeHtml(employee.name)}</span>
            <span class="person-mail">${escapeHtml(employee.email)}</span>
          </div>
        </div>
      </td>
      <td><span class="position-tag">${escapeHtml(employee.position)}</span></td>
      <td>${escapeHtml(employee.department)}</td>
      <td>${escapeHtml(employee.team)}</td>
      <td><span class="status dot-online">${escapeHtml(employee.status)}</span></td>
      <td><span class="access-badge access-${escapeHtml(String(employee.access_level || 'user').toLowerCase())}">${escapeHtml(employee.access_level)}</span></td>
      <td><button class="table-action">•••</button></td>
    `;
    tbody.appendChild(tr);
  });
}

async function loadDashboardData() {
  try {
    const response = await fetch(API_BASE + '/api/overview');
    if (!response.ok) {
      throw new Error('API error: ' + response.status);
    }
    const data = await response.json();

    updateStats(data.stats || {});
    renderPeople(data);
    renderDeviceList(data.devices || []);
    renderDocumentList(data.documents || []);
    renderProjectList(data.projects || []);
    renderPermissionList(data.permissions || []);
    renderSalaryList(data.salaries || []);
    renderBenefitList(data.benefits || []);
    renderLeaveList(data.leave_requests || []);
    renderTimekeepingList(data.timekeeping || []);
    renderCapacityList(data.employee_capacity || []);
  } catch (error) {
    console.warn('Dashboard API unavailable:', error.message);
  }
}

function renderDeviceList(devices) {
  const deviceList = document.getElementById('device-list');
  if (!deviceList || !Array.isArray(devices)) return;

  deviceList.innerHTML = devices.slice(0, 4).map(device => `
    <div class="device-item">
      <div class="device-left">
        <span class="device-icon">
          <svg viewBox="0 0 24 24">
            <path d="M4 5h12v10H4z"></path>
            <path d="M8 17h8"></path>
            <path d="M12 17v4"></path>
          </svg>
        </span>
        <div>
          <span class="device-title">${escapeHtml(device.name)}</span>
          <span class="device-meta">${escapeHtml(device.type)} · ${escapeHtml(device.owner)} · ${escapeHtml(device.location)}</span>
        </div>
      </div>
      <span class="status-label ${device.status === 'Active' ? '' : 'warning'}">${escapeHtml(device.status)}</span>
    </div>
  `).join('');
}

function renderDocumentList(documents) {
  const docList = document.getElementById('document-list');
  if (!docList || !Array.isArray(documents)) return;

  docList.innerHTML = documents.slice(0, 4).map(doc => `
    <div class="document-item">
      <div class="document-left">
        <span class="document-icon">
          <svg viewBox="0 0 24 24">
            <path d="M4 4h11l5 5v15H4z"></path>
            <path d="M14 4v6h6"></path>
          </svg>
        </span>
        <div>
          <span class="document-title">${escapeHtml(doc.name)}</span>
          <span class="document-meta">${escapeHtml(doc.type)} · ${escapeHtml(doc.department)} · ${escapeHtml(doc.access_level)}</span>
        </div>
      </div>
      <span class="status-label ${doc.status === 'Approved' ? '' : 'warning'}">${escapeHtml(doc.status)}</span>
    </div>
  `).join('');
}

function renderProjectList(projects) {
  const projectList = document.getElementById('project-list');
  if (!projectList || !Array.isArray(projects)) return;

  projectList.innerHTML = projects.slice(0, 4).map(project => `
    <div class="project-item">
      <div class="project-left">
        <span class="project-icon">
          <svg viewBox="0 0 24 24">
            <path d="M3 12h7l4-7 4 14 3-7h4"></path>
          </svg>
        </span>
        <div>
          <span class="project-title">${escapeHtml(project.name)}</span>
          <span class="project-meta">${escapeHtml(project.department)} · ${escapeHtml(project.owner)} · ${escapeHtml(project.progress)}%</span>
        </div>
      </div>
      <span class="status-label ${project.status === 'In Progress' ? '' : 'warning'}">${escapeHtml(project.status)}</span>
    </div>
  `).join('');
}

function renderPermissionList(permissions) {
  const permissionList = document.getElementById('permission-list');
  if (!permissionList || !Array.isArray(permissions)) return;

  permissionList.innerHTML = permissions.slice(0, 4).map(permission => `
    <div class="permission-item">
      <div class="permission-left">
        <span class="permission-icon">
          <svg viewBox="0 0 24 24">
            <path d="M7 11V7a5 5 0 0 1 10 0v4"></path>
            <path d="M5 11h14v10H5z"></path>
          </svg>
        </span>
        <div>
          <span class="permission-title">${escapeHtml(permission.resource_name)}</span>
          <span class="permission-meta">${escapeHtml(permission.employee)} · ${escapeHtml(permission.resource_type)} · ${escapeHtml(permission.access_level)}</span>
        </div>
      </div>
      <span class="permission-status ${permission.status === 'Granted' ? '' : 'pending'}">${escapeHtml(permission.status)}</span>
    </div>
  `).join('');
}

function renderSalaryList(salaries) {
  const salaryList = document.getElementById('salary-list');
  if (!salaryList || !Array.isArray(salaries)) return;

  salaryList.innerHTML = salaries.slice(0, 4).map(salary => `
    <div class="salary-item">
      <div class="salary-left">
        <span class="salary-icon">
          <svg viewBox="0 0 24 24">
            <path d="M4 7h16v10H4z"></path>
            <path d="M4 19h16"></path>
          </svg>
        </span>
        <div>
          <span class="salary-title">${escapeHtml(salary.employee)}</span>
          <span class="salary-meta">${escapeHtml(salary.job_title)} · ${escapeHtml(salary.department)} · ${escapeHtml(salary.currency)} ${Number(salary.amount).toLocaleString()}</span>
        </div>
      </div>
      <span class="status-label ${salary.status === 'Paid' ? '' : 'warning'}">${escapeHtml(salary.status)}</span>
    </div>
  `).join('');
}

function renderBenefitList(benefits) {
  const benefitList = document.getElementById('benefit-list');
  if (!benefitList || !Array.isArray(benefits)) return;

  benefitList.innerHTML = benefits.slice(0, 4).map(benefit => `
    <div class="benefit-item">
      <div class="benefit-left">
        <span class="benefit-icon">
          <svg viewBox="0 0 24 24">
            <path d="M12 3a8 8 0 1 0 8 8"></path>
            <path d="M12 3a8 8 0 0 0 8 8"></path>
            <path d="M12 3l-4 8 4 4 4-4z"></path>
          </svg>
        </span>
        <div>
          <span class="benefit-title">${escapeHtml(benefit.benefit_type)}</span>
          <span class="benefit-meta">${escapeHtml(benefit.employee)} · ${escapeHtml(benefit.provider)} · ${escapeHtml(benefit.coverage)}</span>
        </div>
      </div>
      <span class="status-label ${benefit.status === 'Active' ? '' : 'warning'}">${escapeHtml(benefit.status)}</span>
    </div>
  `).join('');
}

function renderLeaveList(leaveRequests) {
  const leaveList = document.getElementById('leave-list');
  if (!leaveList || !Array.isArray(leaveRequests)) return;

  leaveList.innerHTML = leaveRequests.slice(0, 4).map(leave => `
    <div class="leave-item">
      <div class="leave-left">
        <span class="leave-icon">
          <svg viewBox="0 0 24 24">
            <path d="M4 20V8l4-4h12v16z"></path>
            <path d="M8 12h8"></path>
          </svg>
        </span>
        <div>
          <span class="leave-title">${escapeHtml(leave.employee)}</span>
          <span class="leave-meta">${escapeHtml(leave.leave_type)} · ${escapeHtml(leave.start_date)} → ${escapeHtml(leave.end_date)} · ${escapeHtml(leave.days)}d</span>
        </div>
      </div>
      <span class="permission-status ${leave.status === 'Approved' ? '' : 'pending'}">${escapeHtml(leave.status)}</span>
    </div>
  `).join('');
}

function renderTimekeepingList(timekeeping) {
  const timekeepingList = document.getElementById('timekeeping-list');
  if (!timekeepingList || !Array.isArray(timekeeping)) return;

  timekeepingList.innerHTML = timekeeping.slice(0, 4).map(item => `
    <div class="timekeeping-item">
      <div class="timekeeping-left">
        <span class="timekeeping-icon">
          <svg viewBox="0 0 24 24">
            <path d="M12 6a6 6 0 1 0 6 6"></path>
            <path d="M12 2a10 10 0 1 0 10 10"></path>
            <path d="M12 8h.01"></path>
          </svg>
        </span>
        <div>
          <span class="timekeeping-title">${escapeHtml(item.employee)}</span>
          <span class="timekeeping-meta">${escapeHtml(item.date)} · ${escapeHtml(item.check_in)}–${escapeHtml(item.check_out)} · ${Number(item.total_hours).toFixed(1)}h</span>
        </div>
      </div>
      <span class="status-label ${item.status === 'Present' ? '' : 'warning'}">${escapeHtml(item.status)}</span>
    </div>
  `).join('');
}

function renderCapacityList(capacityRows) {
  const capacityList = document.getElementById('capacity-list');
  if (!capacityList || !Array.isArray(capacityRows)) return;

  capacityList.innerHTML = capacityRows.slice(0, 4).map(row => `
    <div class="capacity-item">
      <div class="capacity-left">
        <span class="capacity-icon">
          <svg viewBox="0 0 24 24">
            <path d="M3 12h7l4-7 3 14 2-5h5"></path>
          </svg>
        </span>
        <div>
          <span class="capacity-title">${escapeHtml(row.name)}</span>
          <span class="capacity-meta">${escapeHtml(row.department)} · ${escapeHtml(row.role_name)} · ${escapeHtml(row.position)} · ${escapeHtml(row.status)} · ${Number(row.assigned_tasks)} tasks · ${Number(row.pending_leave_days)}d leave</span>
        </div>
      </div>
      <span class="capacity-score">${Number(row.capacity_score)}%</span>
    </div>
  `).join('');
}

function bindWorkflowForms() {
  const createAccountForm = document.getElementById('create-account-form');
  if (createAccountForm) {
    createAccountForm.addEventListener('submit', async (event) => {
      event.preventDefault();
      const formData = new FormData(createAccountForm);
      const payload = {
        name: formData.get('name'),
        email: formData.get('email'),
        password: formData.get('password'),
        role: formData.get('role')
      };
      const message = document.getElementById('account-message');
      try {
        const response = await fetch(API_BASE + '/api/accounts', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(payload)
        });
        const body = await response.json();
        if (!response.ok) {
          throw new Error(body.error || 'Unable to create account');
        }
        if (message) message.textContent = 'Account created successfully';
        createAccountForm.reset();
      } catch (error) {
        if (message) message.textContent = error.message;
      }
    });
  }

  const profileForm = document.getElementById('profile-form');
  if (profileForm) {
    profileForm.addEventListener('submit', async (event) => {
      event.preventDefault();
      const profileEmail = profileForm.querySelector('#profile-email').value.trim();
      const result = document.getElementById('profile-result');
      try {
        const response = await fetch(API_BASE + '/api/me?email=' + encodeURIComponent(profileEmail));
        const body = await response.json();
        if (!response.ok || !body.employee) {
          throw new Error(body.error || 'Employee profile unavailable');
        }
        const employee = body.employee;
        if (result) {
          result.innerHTML = `
            <div class="profile-card">
              <span class="profile-title">${escapeHtml(employee.name)}</span>
              <span class="profile-meta">${escapeHtml(employee.email)} · ${escapeHtml(employee.department)} · ${escapeHtml(employee.role_name)}</span>
              <span class="profile-meta">${escapeHtml(employee.position)} · ${escapeHtml(employee.access_level)}</span>
            </div>
          `;
        }
      } catch (error) {
        if (result) {
          result.innerHTML = `<span class="profile-empty">${escapeHtml(error.message)}</span>`;
        }
      }
    });
  }

  const leaveForm = document.getElementById('leave-form');
  if (leaveForm) {
    leaveForm.addEventListener('submit', async (event) => {
      event.preventDefault();
      const formData = new FormData(leaveForm);
      const payload = {
        employee: formData.get('employee'),
        department: formData.get('department'),
        leave_type: formData.get('leave_type'),
        start_date: formData.get('start_date'),
        end_date: formData.get('end_date'),
        days: Number(formData.get('days')),
        reviewer: formData.get('reviewer')
      };
      const message = document.getElementById('leave-message');
      try {
        const response = await fetch(API_BASE + '/api/leave-requests/register', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(payload)
        });
        const body = await response.json();
        if (!response.ok) {
          throw new Error(body.error || 'Unable to register leave');
        }
        if (message) message.textContent = 'Leave request submitted';
        leaveForm.reset();
      } catch (error) {
        if (message) message.textContent = error.message;
      }
    });
  }

  const taskForm = document.getElementById('task-form');
  if (taskForm) {
    taskForm.addEventListener('submit', async (event) => {
      event.preventDefault();
      const formData = new FormData(taskForm);
      const payload = {
        id: Number(formData.get('id')),
        title: formData.get('title'),
        status: formData.get('status'),
        priority: formData.get('priority'),
        due_date: formData.get('due_date'),
        description: formData.get('description'),
        department: formData.get('department'),
        assignee: formData.get('assignee'),
        document_id: formData.get('document_id') ? Number(formData.get('document_id')) : null
      };
      const message = document.getElementById('task-message');
      try {
        const response = await fetch(API_BASE + '/api/tasks/update', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(payload)
        });
        const body = await response.json();
        if (!response.ok) {
          throw new Error(body.error || 'Unable to update task');
        }
        if (message) message.textContent = 'Task updated successfully';
        taskForm.reset();
      } catch (error) {
        if (message) message.textContent = error.message;
      }
    });
  }

  const approveForm = document.getElementById('approve-leave-form');
  if (approveForm) {
    approveForm.addEventListener('submit', async (event) => {
      event.preventDefault();
      const formData = new FormData(approveForm);
      const payload = {
        id: Number(formData.get('id')),
        status: formData.get('status'),
        reviewer: formData.get('reviewer')
      };
      const message = document.getElementById('approve-leave-message');
      try {
        const response = await fetch(API_BASE + '/api/leave-requests/approve', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(payload)
        });
        const body = await response.json();
        if (!response.ok) {
          throw new Error(body.error || 'Unable to approve leave');
        }
        if (message) message.textContent = 'Leave updated';
        approveForm.reset();
      } catch (error) {
        if (message) message.textContent = error.message;
      }
    });
  }
}

if (typeof window !== 'undefined') {
  loadDashboardData();
  bindWorkflowForms();
}
