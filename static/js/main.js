/**
 * Main Portfolio JavaScript
 * Features:
 *  - Dark / Light Mode with localStorage & System Sync
 *  - Interactive Developer Terminal Engine with Command Interpreter
 *  - Dynamic Hero Typewriter Effect
 *  - Mouse Pointer Spotlight Tracking (interactive-content-reveal)
 *  - Instant Copy-to-Clipboard with Floating Toast Feedback
 *  - Client-side Instant Filter for Projects & Tech Showcase
 *  - Mobile Navigation Drawer & Back-to-Top Floating Button
 */

function runInit() {
  initTheme();
  initMobileNav();
  initTypewriter();
  initSpotlightEffect();
  initCopyButtons();
  initTechStackFilters();
  initProjectFilters();
  initBackToTop();
  initOrbitalSatellitesFallback();
}

if (document.readyState === 'loading') {
  document.addEventListener('DOMContentLoaded', runInit);
} else {
  runInit();
}

/**
 * 1. THEME MANAGEMENT
 */
function initTheme() {
  const root = document.documentElement;

  // Safe localStorage reading
  let storedTheme = null;
  try {
    storedTheme = localStorage.getItem('portfolio-theme');
  } catch (e) {
    storedTheme = null;
  }

  if (storedTheme === 'light' || storedTheme === 'dark') {
    root.setAttribute('data-theme', storedTheme);
  }

  // Update toggle button title on initial load
  const activeTheme = root.getAttribute('data-theme') || 'dark';
  const initialBtn = document.getElementById('theme-toggle-btn');
  if (initialBtn) {
    initialBtn.setAttribute('title', activeTheme === 'dark' ? 'Switch to Light Mode' : 'Switch to Dark Mode');
    initialBtn.setAttribute('aria-label', activeTheme === 'dark' ? 'Switch to Light Mode' : 'Switch to Dark Mode');
  }

  // Unified global toggleTheme function with debouncing
  let lastToggleTimestamp = 0;
  window.toggleTheme = function() {
    const now = Date.now();
    if (now - lastToggleTimestamp < 300) {
      return; // Prevent rapid duplicate calls
    }
    lastToggleTimestamp = now;

    const currentTheme = root.getAttribute('data-theme') || 'dark';
    const newTheme = currentTheme === 'light' ? 'dark' : 'light';
    root.setAttribute('data-theme', newTheme);
    try {
      localStorage.setItem('portfolio-theme', newTheme);
    } catch (e) {}

    const toggleBtn = document.getElementById('theme-toggle-btn');
    if (toggleBtn) {
      toggleBtn.setAttribute('title', newTheme === 'dark' ? 'Switch to Light Mode' : 'Switch to Dark Mode');
      toggleBtn.setAttribute('aria-label', newTheme === 'dark' ? 'Switch to Light Mode' : 'Switch to Dark Mode');
    }

    if (typeof showToast === 'function') {
      showToast(`Switched to ${newTheme} theme`);
    }
  };

  // Delegated click listener ensures every theme button always works reliably
  document.addEventListener('click', (e) => {
    const btn = e.target.closest('#theme-toggle-btn, #mobile-theme-toggle-btn');
    if (btn) {
      e.preventDefault();
      e.stopPropagation();
      window.toggleTheme();
    }
  });
}

/**
 * 2. MOBILE NAVIGATION DRAWER
 */
function initMobileNav() {
  const mobileToggle = document.getElementById('mobile-toggle-btn');
  const mobileDrawer = document.getElementById('mobile-drawer');

  if (mobileToggle && mobileDrawer) {
    mobileToggle.addEventListener('click', (e) => {
      e.stopPropagation();
      const isOpen = mobileDrawer.classList.contains('open');
      if (isOpen) {
        mobileDrawer.classList.remove('open');
        mobileToggle.setAttribute('aria-expanded', 'false');
      } else {
        mobileDrawer.classList.add('open');
        mobileToggle.setAttribute('aria-expanded', 'true');
      }
    });

    // Close on outside click
    document.addEventListener('click', (e) => {
      if (!mobileDrawer.contains(e.target) && !mobileToggle.contains(e.target)) {
        mobileDrawer.classList.remove('open');
        mobileToggle.setAttribute('aria-expanded', 'false');
      }
    });

    // Close on menu link click
    const drawerLinks = mobileDrawer.querySelectorAll('a');
    drawerLinks.forEach(link => {
      link.addEventListener('click', () => {
        mobileDrawer.classList.remove('open');
        mobileToggle.setAttribute('aria-expanded', 'false');
      });
    });
  }
}

/**
 * 3. DYNAMIC HERO TYPEWRITER EFFECT
 */
function initTypewriter() {
  const el = document.getElementById('typewriter-role');
  if (!el) return;

  const roles = [
    'Software Engineer',
    'Computer Vision & YOLO Developer',
    'Python & Django Specialist',
    'Generative AI & Agent Architect'
  ];

  let roleIndex = 0;
  let charIndex = 0;
  let isDeleting = false;
  let typingSpeed = 90;

  function type() {
    const currentRole = roles[roleIndex];
    if (isDeleting) {
      el.textContent = currentRole.substring(0, charIndex - 1);
      charIndex--;
      typingSpeed = 40;
    } else {
      el.textContent = currentRole.substring(0, charIndex + 1);
      charIndex++;
      typingSpeed = 90;
    }

    if (!isDeleting && charIndex === currentRole.length) {
      isDeleting = true;
      typingSpeed = 1800; // Pause at end of word
    } else if (isDeleting && charIndex === 0) {
      isDeleting = false;
      roleIndex = (roleIndex + 1) % roles.length;
      typingSpeed = 400; // Pause before new word
    }

    setTimeout(type, typingSpeed);
  }

  type();
}



/**
 * 5. MOUSE POINTER SPOTLIGHT EFFECT (interactive-content-reveal)
 */
function initSpotlightEffect() {
  const cards = document.querySelectorAll('.spotlight-card');
  if (!cards.length) return;

  cards.forEach(card => {
    card.addEventListener('pointermove', (e) => {
      const rect = card.getBoundingClientRect();
      const x = e.clientX - rect.left;
      const y = e.clientY - rect.top;
      card.style.setProperty('--mouse-x', `${x}px`);
      card.style.setProperty('--mouse-y', `${y}px`);
    });
  });
}

/**
 * 6. INSTANT CLIPBOARD COPY WITH TOAST FEEDBACK
 */
function initCopyButtons() {
  document.addEventListener('click', (e) => {
    const copyTarget = e.target.closest('[data-copy]');
    if (!copyTarget) return;

    e.preventDefault();
    const textToCopy = copyTarget.getAttribute('data-copy');
    if (!textToCopy) return;

    navigator.clipboard.writeText(textToCopy).then(() => {
      const label = copyTarget.getAttribute('data-copy-label') || textToCopy;
      showToast(`Copied ${label} to clipboard!`);
    }).catch(() => {
      showToast(`Failed to copy to clipboard`, 'error');
    });
  });
}

/**
 * 7. FLOATING TOAST NOTIFICATION UTILITY
 */
function showToast(message, type = 'info') {
  let container = document.getElementById('toast-container');
  if (!container) {
    container = document.createElement('div');
    container.id = 'toast-container';
    container.className = 'toast-container';
    document.body.appendChild(container);
  }

  const toast = document.createElement('div');
  toast.className = 'toast-pill';

  const iconSvg = type === 'error'
    ? `<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="#ef4444" stroke-width="2.5"><circle cx="12" cy="12" r="10"/><line x1="15" y1="9" x2="9" y2="15"/><line x1="9" y1="9" x2="15" y2="15"/></svg>`
    : `<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="#00f5d4" stroke-width="2.5"><path d="M20 6L9 17l-5-5"/></svg>`;

  toast.innerHTML = `
    ${iconSvg}
    <span>${escapeHtml(message)}</span>
  `;

  container.appendChild(toast);

  setTimeout(() => {
    toast.classList.add('fade-out');
    setTimeout(() => toast.remove(), 300);
  }, 3200);
}
window.showToast = showToast;

/**
 * 8. TECH STACK CATEGORY TABS
 */
function initTechStackFilters() {
  const tabBtns = document.querySelectorAll('.tech-tab-btn');
  const techCards = document.querySelectorAll('.tech-card[data-tech-category]');

  if (!tabBtns.length || !techCards.length) return;

  tabBtns.forEach(btn => {
    btn.addEventListener('click', () => {
      tabBtns.forEach(b => b.classList.remove('active'));
      btn.classList.add('active');

      const selected = btn.getAttribute('data-tech-tab');
      techCards.forEach(card => {
        const cat = card.getAttribute('data-tech-category');
        if (selected === 'all' || cat === selected) {
          card.style.display = 'flex';
        } else {
          card.style.display = 'none';
        }
      });
    });
  });
}

/**
 * 9. DYNAMIC PROJECT SEARCH & CLIENT FILTERING
 */
function initProjectFilters() {
  const filterBtns = document.querySelectorAll('.filter-btn[data-category]');
  const projectCards = document.querySelectorAll('.project-card[data-category]');
  const searchInput = document.getElementById('project-search-input');
  const emptyState = document.getElementById('projects-empty-state');

  if (!filterBtns.length || !projectCards.length) return;

  let currentCategory = 'all';
  let currentSearch = '';

  function filterProjects() {
    let visibleCount = 0;

    projectCards.forEach(card => {
      const cardCategory = card.getAttribute('data-category');
      const cardTitle = (card.querySelector('.card-title')?.textContent || '').toLowerCase();
      const cardDesc = (card.querySelector('.card-text')?.textContent || '').toLowerCase();
      const cardTags = (card.querySelector('.card-tags')?.textContent || '').toLowerCase();

      const matchesCategory = currentCategory === 'all' || cardCategory === currentCategory;
      const matchesSearch = !currentSearch ||
        cardTitle.includes(currentSearch) ||
        cardDesc.includes(currentSearch) ||
        cardTags.includes(currentSearch);

      if (matchesCategory && matchesSearch) {
        card.style.display = '';
        visibleCount++;
      } else {
        card.style.display = 'none';
      }
    });

    if (emptyState) {
      emptyState.style.display = visibleCount === 0 ? 'block' : 'none';
    }
  }

  filterBtns.forEach(btn => {
    btn.addEventListener('click', (e) => {
      if (btn.hasAttribute('data-client-filter')) {
        e.preventDefault();
        filterBtns.forEach(b => b.classList.remove('active'));
        btn.classList.add('active');
        currentCategory = btn.getAttribute('data-category');
        filterProjects();
      }
    });
  });

  if (searchInput) {
    searchInput.addEventListener('input', (e) => {
      currentSearch = e.target.value.trim().toLowerCase();
      filterProjects();
    });
  }
}

/**
 * 10. BACK TO TOP BUTTON
 */
function initBackToTop() {
  const btn = document.getElementById('back-to-top-btn');
  if (!btn) return;

  window.addEventListener('scroll', () => {
    if (window.scrollY > 400) {
      btn.classList.add('visible');
    } else {
      btn.classList.remove('visible');
    }
  });

  btn.addEventListener('click', () => {
    window.scrollTo({ top: 0, behavior: 'smooth' });
  });
}

function escapeHtml(text) {
  const div = document.createElement('div');
  div.textContent = text;
  return div.innerHTML;
}

/**
 * 11. ORBITAL SATELLITES SIBLING FALLBACK
 * Complies with modern-web-guidance dynamic-sibling-styling:
 * Sets --sibling-index and --sibling-count if CSS sibling-index() is not natively supported.
 */
function initOrbitalSatellitesFallback() {
  /* MANDATORY: Check for native support before applying fallback */
  if (!CSS.supports('top: calc(sibling-index() * 1px)')) {
    const containers = document.querySelectorAll('.orbit-satellite-container');
    containers.forEach((container) => {
      const items = container.querySelectorAll('.orbit-satellite-item');
      const total = items.length;
      container.style.setProperty('--sibling-count', total);
      items.forEach((item, index) => {
        // sibling-index is 1-based in CSS
        item.style.setProperty('--sibling-index', index + 1);
      });
    });
  }
}

