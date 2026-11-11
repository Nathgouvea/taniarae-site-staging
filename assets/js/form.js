/* =========================================================================
   Tania Rae · form.js
   Contact form logic ONLY. Sends the form to Formspree with fetch and shows
   a thank-you message in place. Without JavaScript the form still works as
   a normal POST to Formspree (browser checks the required fields).
   ========================================================================= */
(function () {
  'use strict';

  var form = document.getElementById('contact-form');
  if (!form || !window.fetch || !window.FormData) return;

  var success = document.getElementById('form-success');
  var signature = document.getElementById('signature');
  var status = document.getElementById('form-status');
  var button = form.querySelector('button[type="submit"]');
  var buttonLabel = button.textContent;
  var sending = false;

  // Messages shown under each field when something is missing or wrong.
  var MESSAGES = {
    'f-name':    { missing: 'Please tell me your name.' },
    'f-email':   { missing: 'Please add your email, so I can reply.',
                   invalid: 'This email doesn’t look quite right. Please check it.' },
    'f-consent': { missing: 'Please tick this box, so I may use your details to reply.' }
  };
  var SEND_ERROR = 'Sorry, your message didn’t go through. Please try again in a moment.';

  // We show our own friendly errors instead of the browser bubbles.
  form.setAttribute('novalidate', '');

  function errorFor(input) {
    return document.getElementById(input.id + '-error');
  }

  function setError(input, text) {
    var el = errorFor(input);
    if (!el) return;
    if (text) {
      el.textContent = text;
      el.hidden = false;
      input.setAttribute('aria-invalid', 'true');
      input.setAttribute('aria-describedby', el.id);
    } else {
      el.textContent = '';
      el.hidden = true;
      input.removeAttribute('aria-invalid');
      input.removeAttribute('aria-describedby');
    }
  }

  function check(input) {
    var msg = MESSAGES[input.id];
    if (!msg) return true;
    var empty = input.type === 'checkbox' ? !input.checked : input.value.trim() === '';
    if (empty) { setError(input, msg.missing); return false; }
    if (msg.invalid && !input.checkValidity()) { setError(input, msg.invalid); return false; }
    setError(input, '');
    return true;
  }

  // Clear an error as soon as the person fixes it.
  Object.keys(MESSAGES).forEach(function (id) {
    var input = document.getElementById(id);
    if (!input) return;
    input.addEventListener(input.type === 'checkbox' ? 'change' : 'input', function () {
      if (input.getAttribute('aria-invalid') === 'true') check(input);
    });
  });

  function setSending(on) {
    sending = on;
    button.textContent = on ? 'Sending…' : buttonLabel;
    if (on) button.setAttribute('aria-disabled', 'true');
    else button.removeAttribute('aria-disabled');
  }

  form.addEventListener('submit', function (event) {
    event.preventDefault();
    if (sending) return; // no double submits

    status.hidden = true;
    status.textContent = '';

    // Validate every field, then move focus to the first problem.
    var firstInvalid = null;
    Object.keys(MESSAGES).forEach(function (id) {
      var input = document.getElementById(id);
      if (input && !check(input) && !firstInvalid) firstInvalid = input;
    });
    if (firstInvalid) { firstInvalid.focus(); return; }

    setSending(true);
    fetch(form.action, {
      method: 'POST',
      body: new FormData(form),
      headers: { Accept: 'application/json' }
    })
      .then(function (response) {
        if (!response.ok) throw new Error('Formspree responded ' + response.status);
        form.hidden = true;
        signature.hidden = true;
        success.hidden = false;
        success.focus();
      })
      .catch(function (error) {
        console.error(error);
        status.textContent = SEND_ERROR;
        status.hidden = false;
        setSending(false);
        button.focus();
      });
  });
})();
