let allUsers = [];

function createEmptyState(message) {
  const div = document.createElement('div');
  div.className = 'empty-state';
  div.textContent = message;
  return div;
}

function formatTimestamp(isoString) {
  if (!isoString) return 'Sem horario';
  const date = new Date(isoString);
  if (Number.isNaN(date.getTime())) return 'Sem horario';
  return new Intl.DateTimeFormat('pt-BR', {
    dateStyle: 'short',
    timeStyle: 'medium',
  }).format(date);
}

function renderAlerts(alerts) {
  const container = document.getElementById('alerts_list');
  container.innerHTML = '';

  if (!alerts.length) {
    container.appendChild(createEmptyState('Nenhum alerta operacional no momento.'));
    return;
  }

  alerts.forEach(alert => {
    const article = document.createElement('article');
    article.className = `alert-item alert-${alert.level || 'info'}`;
    article.innerHTML = `
      <strong>${alert.title || 'Alerta'}</strong>
      <span>${alert.message || ''}</span>
    `;
    container.appendChild(article);
  });
}

function renderEntityList(containerId, items, emptyMessage, formatter) {
  const container = document.getElementById(containerId);
  container.innerHTML = '';

  if (!items.length) {
    container.appendChild(createEmptyState(emptyMessage));
    return;
  }

  items.forEach(item => {
    const li = document.createElement('li');
    li.className = 'entity-item';
    li.innerHTML = formatter(item);
    container.appendChild(li);
  });
}

function renderMetricBars(containerId, items) {
  const container = document.getElementById(containerId);
  container.innerHTML = '';

  const maxValue = Math.max(...items.map(item => item.value || 0), 0);
  if (!maxValue) {
    container.appendChild(createEmptyState('Sem dados suficientes para exibir a distribuicao.'));
    return;
  }

  items.forEach(item => {
    const row = document.createElement('div');
    row.className = 'metric-row';
    const percentage = item.value ? Math.max(8, Math.round(((item.value || 0) / maxValue) * 100)) : 0;
    row.innerHTML = `
      <header>
        <strong>${item.label}</strong>
        <span>${item.value}</span>
      </header>
      <div class="metric-track">
        <div class="metric-fill" style="width: ${percentage}%"></div>
      </div>
    `;
    container.appendChild(row);
  });
}

function buildStatusPill(status) {
  const normalized = (status || 'desconhecido').toLowerCase();
  const label = normalized === 'active' ? 'ativo' : normalized;
  return `<span class="status-pill status-${normalized}">${label}</span>`;
}

function buildPlanPill(plan) {
  return `<span class="plan-pill">${plan || 'sem plano'}</span>`;
}

function renderUsersTable(users) {
  const tbody = document.getElementById('users_table');
  tbody.innerHTML = '';

  if (!users.length) {
    const tr = document.createElement('tr');
    tr.innerHTML = '<td colspan="6"><div class="empty-state">Nenhum usuario encontrado com esse filtro.</div></td>';
    tbody.appendChild(tr);
    return;
  }

  users.forEach(user => {
    const tr = document.createElement('tr');
    tr.innerHTML = `
      <td>${user.name || ''}</td>
      <td>${user.email || ''}</td>
      <td>${user.role || ''}</td>
      <td>${buildPlanPill(user.plan)}</td>
      <td>${buildStatusPill(user.status)}</td>
      <td>${user.devices_count ?? 0}</td>
    `;
    tbody.appendChild(tr);
  });
}

function applyUserFilter() {
  const term = document.getElementById('user_search').value.trim().toLowerCase();
  if (!term) {
    renderUsersTable(allUsers);
    return;
  }

  const filtered = allUsers.filter(user => {
    const haystack = [user.name, user.email, user.role, user.plan, user.status]
      .join(' ')
      .toLowerCase();
    return haystack.includes(term);
  });
  renderUsersTable(filtered);
}

async function carregarDashboard() {
  try {
    document.getElementById('refresh_status').textContent = 'Atualizando dados...';
    const resp = await fetch('/server/dashboard-data');
    const payload = await resp.json();
    const data = payload.data || {};

    allUsers = data.users || [];

    document.getElementById('users_total').textContent = data.users_total ?? 0;
    document.getElementById('users_online').textContent = data.users_online ?? 0;
    document.getElementById('devices_total').textContent = data.devices_total ?? 0;
    document.getElementById('online_rate_copy').textContent = `Taxa ativa: ${data.online_rate ?? 0}%`;
    document.getElementById('generated_at').textContent = `Atualizado em ${formatTimestamp(data.generated_at)}`;
    document.getElementById('refresh_status').textContent = 'Sincronizado';

    renderAlerts(data.alerts || []);
    renderMetricBars('plan_breakdown', data.plan_breakdown || []);
    renderMetricBars('platform_breakdown', data.platform_breakdown || []);

    renderEntityList(
      'online_list',
      data.online_users || [],
      'Nenhum usuario online agora.',
      user => `
        <div class="entity-main">
          <strong>${user.name || 'Usuario'}</strong>
          <span class="entity-meta">${user.email || ''}</span>
        </div>
        ${buildPlanPill(user.plan)}
      `,
    );

    renderEntityList(
      'recent_devices',
      data.recent_devices || [],
      'Nenhum dispositivo registrado ainda.',
      item => `
        <div class="entity-main">
          <strong>${item.device_name || 'Dispositivo'}</strong>
          <span class="entity-meta">${item.user_name || 'Usuario'} · ${item.platform || 'unknown'}</span>
        </div>
        <span class="status-pill">${item.user_email || ''}</span>
      `,
    );

    applyUserFilter();
  } catch (err) {
    console.error('Erro no dashboard', err);
    document.getElementById('refresh_status').textContent = 'Falha ao atualizar';
    document.getElementById('alerts_list').innerHTML = '';
    document.getElementById('alerts_list').appendChild(
      createEmptyState('Nao foi possivel carregar o dashboard agora. Verifique a API local.'),
    );
  }
}

document.getElementById('user_search').addEventListener('input', applyUserFilter);

carregarDashboard();
setInterval(carregarDashboard, 5000);
