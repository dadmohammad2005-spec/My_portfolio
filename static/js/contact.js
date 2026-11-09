/**
 * Contact Form AJAX Handler
 * Supports asynchronous form submission with CSRF validation,
 * spinner states, and instant error/success feedback.
 */

document.addEventListener('DOMContentLoaded', () => {
  const contactForm = document.getElementById('portfolio-contact-form');
  const alertContainer = document.getElementById('contact-alert-container');
  const submitBtn = document.getElementById('contact-submit-btn');

  if (!contactForm) return;

  contactForm.addEventListener('submit', async (e) => {
    // If browser supports fetch, handle with AJAX for great UX
    e.preventDefault();

    // Disable button & show spinner
    const originalBtnText = submitBtn.innerHTML;
    submitBtn.disabled = true;
    submitBtn.innerHTML = `
      <svg class="animate-spin" style="width:1.25rem; height:1.25rem; animation: spin 1s linear infinite;" viewBox="0 0 24 24" fill="none" stroke="currentColor">
        <circle cx="12" cy="12" r="10" stroke-width="4" stroke="currentColor" stroke-dasharray="32" stroke-linecap="round"></circle>
      </svg>
      Sending message...
    `;

    // Clear previous alerts
    if (alertContainer) {
      alertContainer.innerHTML = '';
    }

    try {
      const formData = new FormData(contactForm);
      const actionUrl = contactForm.getAttribute('action') || window.location.pathname;

      const response = await fetch(actionUrl, {
        method: 'POST',
        headers: {
          'X-Requested-With': 'XMLHttpRequest',
          'Accept': 'application/json',
        },
        body: formData,
      });

      const data = await response.json();

      if (response.ok && data.success) {
        // Show success alert
        if (alertContainer) {
          alertContainer.innerHTML = `
            <div class="alert alert-success">
              <span><strong>Success!</strong> ${data.message}</span>
            </div>
          `;
        }
        contactForm.reset();
      } else {
        // Form errors returned
        let errorMsg = 'Please verify your input.';
        if (data.errors) {
          errorMsg = Object.values(data.errors).flat().join('<br>');
        }
        if (alertContainer) {
          alertContainer.innerHTML = `
            <div class="alert alert-error">
              <span><strong>Error:</strong> ${errorMsg}</span>
            </div>
          `;
        }
      }
    } catch (err) {
      console.error('Contact submission error:', err);
      if (alertContainer) {
        alertContainer.innerHTML = `
          <div class="alert alert-error">
            <span><strong>Submission Error:</strong> Unable to send message. Please try again or email directly.</span>
          </div>
        `;
      }
    } finally {
      submitBtn.disabled = false;
      submitBtn.innerHTML = originalBtnText;
    }
  });
});
