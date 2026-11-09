/**
 * Portfolio Admin Dashboard Scripts
 */

function runDashboardInit() {
  initDashboardTheme();
  initDashboardSidebar();
  initAutoDismissAlerts();
  initFileInputPreviews();
}

if (document.readyState === 'loading') {
  document.addEventListener('DOMContentLoaded', runDashboardInit);
} else {
  runDashboardInit();
}

function initDashboardTheme() {
  const toggleBtn = document.getElementById('dash-theme-toggle');
  const root = document.documentElement;
  let storedTheme = null;
  try {
    storedTheme = localStorage.getItem('portfolio-theme');
  } catch (e) {
    storedTheme = null;
  }

  if (storedTheme === 'light' || storedTheme === 'dark') {
    root.setAttribute('data-theme', storedTheme);
  }

  if (toggleBtn) {
    toggleBtn.addEventListener('click', (e) => {
      e.preventDefault();
      const currentTheme = root.getAttribute('data-theme') || 'dark';
      const newTheme = currentTheme === 'light' ? 'dark' : 'light';
      root.setAttribute('data-theme', newTheme);
      try {
        localStorage.setItem('portfolio-theme', newTheme);
      } catch (e) {}
    });
  }
}

function initDashboardSidebar() {
  const mobileBtn = document.getElementById('dash-mobile-toggle');
  const sidebar = document.getElementById('dash-sidebar');
  const overlay = document.getElementById('dash-sidebar-overlay');

  if (mobileBtn && sidebar) {
    mobileBtn.addEventListener('click', (e) => {
      e.stopPropagation();
      sidebar.classList.toggle('open');
      if (overlay) overlay.classList.toggle('active');
    });

    if (overlay) {
      overlay.addEventListener('click', () => {
        sidebar.classList.remove('open');
        overlay.classList.remove('active');
      });
    }

    document.addEventListener('click', (e) => {
      if (sidebar.classList.contains('open') && !sidebar.contains(e.target) && e.target !== mobileBtn) {
        sidebar.classList.remove('open');
        if (overlay) overlay.classList.remove('active');
      }
    });
  }
}

function initAutoDismissAlerts() {
  const alerts = document.querySelectorAll('.dash-alert');
  alerts.forEach(alert => {
    setTimeout(() => {
      alert.style.opacity = '0';
      alert.style.transform = 'translateY(-8px)';
      alert.style.transition = 'all 0.4s ease';
      setTimeout(() => alert.remove(), 400);
    }, 5000);
  });
}

function initFileInputPreviews() {
  const fileInputs = document.querySelectorAll('input[type="file"]');
  fileInputs.forEach(input => {
    input.addEventListener('change', () => {
      const file = input.files[0];
      if (file && file.type.startsWith('image/')) {
        let preview = input.parentElement.querySelector('.dash-file-preview');
        if (!preview) {
          preview = document.createElement('img');
          preview.className = 'dash-file-preview';
          preview.style.maxHeight = '100px';
          preview.style.marginTop = '0.5rem';
          preview.style.borderRadius = '4px';
          input.parentElement.appendChild(preview);
        }
        const reader = new FileReader();
        reader.onload = (e) => {
          preview.src = e.target.result;
        };
        reader.readAsDataURL(file);
      }
    });
  });
}
