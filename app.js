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

if (typeof window !== 'undefined') {
  loadDashboardData();
}
