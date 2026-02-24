/* ════════════════════════════════════
   STAFF REGISTRATION — STEP ENGINE
   File: static/medi_clinics/js/staff_form.js
════════════════════════════════════ */

/* ── Role definitions ── */
var TECHNICAL_ROLES = [
  ['physician',            'Physician / Doctor'],
  ['specialist',           'Specialist'],
  ['nurse',                'Nurse'],
  ['nurse_practitioner',   'Nurse Practitioner'],
  ['physician_assistant',  'Physician Assistant'],
  ['medical_assistant',    'Medical Assistant'],
  ['pharmacist',           'Pharmacist'],
  ['lab_technician',       'Lab Technician'],
  ['radiology_technician', 'Radiology Technician'],
  ['dietitian',            'Dietitian / Nutritionist'],
  ['social_worker',        'Social Worker / Counselor'],
];

var SUPPORT_ROLES = [
  ['clinic_manager',     'Clinic Manager / Administrator'],
  ['receptionist',       'Receptionist / Front Desk'],
  ['billing_specialist', 'Billing & Insurance Specialist'],
  ['records_clerk',      'Medical Records Clerk'],
  ['it_support',         'IT Support Staff'],
  ['maintenance',        'Cleaning & Maintenance Staff'],
];

/* ════════════════════════════════════
   STEP ENGINE
════════════════════════════════════ */
var TOTAL = 6;
var cur   = 1;
var back  = false;

var META = [
  { label: 'Account'    },
  { label: 'Personal'   },
  { label: 'Employment' },
  { label: 'Next of Kin'},
  { label: 'Pay & Status'},
  { label: 'Review'     },
];

/* ── Build progress dots ── */
function buildProgress() {
  var c = document.getElementById('progressSteps');
  c.innerHTML = '';
  META.forEach(function(m, i) {
    var n  = i + 1;
    var el = document.createElement('div');
    el.className = 'prog-step' + (n === cur ? ' active' : '') + (n < cur ? ' done' : '');
    el.innerHTML = '<div class="prog-circle">' + (n < cur ? '&#10003;' : n) + '</div>' +
                   '<span class="prog-label">' + m.label + '</span>';
    (function(t){ el.onclick = function(){ jumpTo(t); }; })(n);
    c.appendChild(el);
    if (i < META.length - 1) {
      var conn = document.createElement('div');
      conn.className = 'prog-connector' + (n < cur ? ' done' : '');
      c.appendChild(conn);
    }
  });
  var pct = ((cur - 1) / (TOTAL - 1)) * 100;
  document.getElementById('progressBar').style.width = Math.max(pct, 2) + '%';
  document.getElementById('stepCounter').textContent = 'Step ' + cur + ' of ' + TOTAL;
}

/* ── Show panel ── */
function showPanel(n) {
  document.querySelectorAll('.step-panel').forEach(function(p) {
    p.classList.remove('active', 'go-back');
  });
  var p = document.getElementById('step' + n);
  if (p) {
    p.classList.add('active');
    if (back) p.classList.add('go-back');
  }
  document.getElementById('btnPrev').disabled         = (n === 1);
  document.getElementById('btnNext').style.display   = (n === TOTAL) ? 'none'        : 'inline-flex';
  document.getElementById('btnSubmit').style.display = (n === TOTAL) ? 'inline-flex' : 'none';
  if (n === TOTAL) buildReview();
  window.scrollTo({ top: 0, behavior: 'smooth' });
}

/* ── Validate one step ── */
function validateStep(n) {
  var ok    = true;
  var panel = document.getElementById('step' + n);

  panel.querySelectorAll('[data-required]').forEach(function(el) {
    var name  = el.getAttribute('name') || '';
    var errEl = document.getElementById('err-' + name);
    var empty = !el.value || el.value.trim() === '';

    if (empty) {
      el.classList.add('invalid');
      if (errEl) errEl.classList.add('show');
      ok = false;
    } else {
      el.classList.remove('invalid');
      if (errEl) errEl.classList.remove('show');
    }

    ['input', 'change'].forEach(function(ev) {
      el.addEventListener(ev, function fix() {
        if (el.value.trim()) {
          el.classList.remove('invalid');
          if (errEl) errEl.classList.remove('show');
          el.removeEventListener(ev, fix);
        }
      });
    });
  });

  return ok;
}

/* ── Navigate ── */
function changeStep(dir) {
  if (dir === 1) {
    if (!validateStep(cur)) {
      showToast('Please fill in all required fields before continuing.');
      return;
    }
    back = false;
    cur  = Math.min(cur + 1, TOTAL);
  } else {
    back = true;
    cur  = Math.max(cur - 1, 1);
  }
  buildProgress();
  showPanel(cur);
}

/* ── Jump to completed step ── */
function jumpTo(target) {
  if (target >= cur) return;
  back = target < cur;
  cur  = target;
  buildProgress();
  showPanel(cur);
}

/* ════════════════════════════════════
   REVIEW BUILDER
════════════════════════════════════ */
function fv(id) { var e = document.getElementById(id); return e ? e.value.trim() : ''; }
function ol(id) { var e = document.getElementById(id); return (e && e.selectedIndex >= 0) ? e.options[e.selectedIndex].text : '-'; }

function buildReview() {
  var grid = document.getElementById('reviewGrid');
  grid.innerHTML = '';

  var sections = [
    { title: 'Account', rows: [
      { l: 'Username', v: function(){ return fv('id_username') || '-'; } },
      { l: 'Email',    v: function(){ return fv('id_email') || '-'; } },
    ]},
    { title: 'Personal Information', rows: [
      { l: 'First Name',   v: function(){ return fv('id_first_name') || '-'; } },
      { l: 'Last Name',    v: function(){ return fv('id_last_name') || '-'; } },
      { l: 'Date of Birth',v: function(){ return fv('id_date_of_birth') || '-'; } },
      { l: 'National ID',  v: function(){ return fv('id_national_id') || '-'; } },
      { l: 'Phone',        v: function(){ return fv('id_phone') || '-'; } },
    ]},
    { title: 'Employment', rows: [
      { l: 'Type',          v: function(){ return ol('id_employment_type'); } },
      { l: 'Role',          v: function(){ return ol('id_role'); } },
      { l: 'Reg. Number',   v: function(){ return fv('id_registration_number') || '-'; } },
      { l: 'Licence Expiry',v: function(){ return fv('id_license_expiry_date') || '-'; } },
    ]},
    { title: 'Next of Kin', rows: [
      { l: 'Name',         v: function(){ return fv('id_next_of_kin') || '-'; } },
      { l: 'Relationship', v: function(){ return fv('id_nok_relationship') || '-'; } },
      { l: 'Phone',        v: function(){ return fv('id_nok_phone') || '-'; } },
    ]},
    { title: 'Compensation & Status', rows: [
      { l: 'Gross Salary',    v: function(){ return fv('id_gross_salary') ? 'UGX ' + fv('id_gross_salary') : '-'; } },
      { l: 'Allowance',       v: function(){ return fv('id_monthly_allowance') ? 'UGX ' + fv('id_monthly_allowance') : '-'; } },
      { l: 'Account Status',  v: function(){ return ol('id_account_status'); } },
      { l: 'Duty Status',     v: function(){ return ol('id_duty_status'); } },
    ]},
  ];

  sections.forEach(function(sec) {
    var card = document.createElement('div');
    card.className = 'review-card';
    card.innerHTML = '<div class="review-card-title">' + sec.title + '</div>';

    sec.rows.forEach(function(row) {
      var rowEl = document.createElement('div');
      rowEl.className = 'review-row';
      rowEl.innerHTML =
        '<span class="review-label">' + row.l + '</span>' +
        '<span class="review-value">' + row.v() + '</span>';
      card.appendChild(rowEl);
    });
    grid.appendChild(card);
  });
}

/* ════════════════════════════════════
   ROLE CASCADE
════════════════════════════════════ */
function updateRoles(type) {
  var roleSelect = document.getElementById('id_role');
  if (!roleSelect) return;
  roleSelect.innerHTML = '<option value="">Select role...</option>';
  if (!type) return;

  var roles = (type === 'technical') ? TECHNICAL_ROLES : SUPPORT_ROLES;
  roles.forEach(function(pair) {
    var opt = document.createElement('option');
    opt.value       = pair[0];
    opt.textContent = pair[1];
    if (pair[0] === (typeof PREVIOUS_ROLE !== 'undefined' ? PREVIOUS_ROLE : '')) {
      opt.selected = true;
    }
    roleSelect.appendChild(opt);
  });
}

function updateTechnicalFields(type) {
  var isTechnical = (type === 'technical');
  var regStar = document.getElementById('reg_required_star');
  var licStar = document.getElementById('lic_required_star');
  var regField = document.getElementById('registration_number_field');
  var licField = document.getElementById('license_expiry_field');

  if (regStar) regStar.style.display = isTechnical ? 'inline' : 'none';
  if (licStar) licStar.style.display = isTechnical ? 'inline' : 'none';
  if (regField) regField.style.opacity = isTechnical ? '1' : '.5';
  if (licField) licField.style.opacity = isTechnical ? '1' : '.5';

  /* Also update data-required so validation only fires for technical staff */
  var regInput = document.getElementById('id_registration_number');
  var licInput = document.getElementById('id_license_expiry_date');
  if (regInput) { if (isTechnical) regInput.setAttribute('data-required','true'); else regInput.removeAttribute('data-required'); }
  if (licInput) { if (isTechnical) licInput.setAttribute('data-required','true'); else licInput.removeAttribute('data-required'); }
}

/* ════════════════════════════════════
   TOAST
════════════════════════════════════ */
function showToast(msg) {
  var t = document.getElementById('toastMsg');
  t.textContent = '⚠️  ' + msg;
  t.classList.add('show');
  setTimeout(function(){ t.classList.remove('show'); }, 3400);
}

/* ════════════════════════════════════
   SUBMIT GUARD
════════════════════════════════════ */
function initSubmitGuard() {
  document.getElementById('staffForm').addEventListener('submit', function(e) {
    var allOk = true; var firstBad = -1;
    for (var s = 1; s < TOTAL; s++) {
      if (!validateStep(s)) { allOk = false; if (firstBad === -1) firstBad = s; }
    }
    if (!allOk) {
      e.preventDefault();
      back = false; cur = firstBad;
      buildProgress(); showPanel(cur);
      showToast('Please complete all required fields before submitting.');
    }
  });
}

/* ════════════════════════════════════
   INIT  — called from inline <script>
   initStaffForm(startStep)
════════════════════════════════════ */
function initStaffForm(startStep) {
  cur = startStep || 1;

  /* Employment type cascade */
  var typeSelect = document.getElementById('id_employment_type');
  if (typeSelect) {
    typeSelect.addEventListener('change', function() {
      updateRoles(this.value);
      updateTechnicalFields(this.value);
    });
    updateRoles(typeSelect.value);
    updateTechnicalFields(typeSelect.value);
  }

  initSubmitGuard();
  buildProgress();
  showPanel(cur);
}
