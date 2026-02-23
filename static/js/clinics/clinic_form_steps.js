/* ════════════════════════════════════
   CLINIC MULTI-STEP FORM ENGINE
   File: static/js/clinics/clinic_form_steps.js
════════════════════════════════════ */

var TOTAL = 7;
var cur   = 1;
var back  = false;

var META = [
  { label: 'Basic Info' }, { label: 'Location' }, { label: 'Contact' },
  { label: 'Operations' }, { label: 'Banking' },  { label: 'Licensing' },
  { label: 'Review' }
];

/* ── Build progress dots ── */
function buildProgress() {
  var c = document.getElementById('progressSteps');
  c.innerHTML = '';
  META.forEach(function(m, i) {
    var n = i + 1;
    var el = document.createElement('div');
    el.className = 'prog-step' + (n === cur ? ' active' : '') + (n < cur ? ' done' : '');
    el.innerHTML = '<div class="prog-circle">' + (n < cur ? '✓' : n) + '</div>' +
                   '<span class="prog-label">' + m.label + '</span>';
    (function(target){ el.onclick = function(){ jumpTo(target); }; })(n);
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

/* ── Validate one step — returns true if valid ── */
function validateStep(n) {
  var ok    = true;
  var panel = document.getElementById('step' + n);

  /* [data-required] text / select / date / time fields */
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

    /* Live clear-on-fix listeners */
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

  /* [data-group-required] checkbox grids */
  panel.querySelectorAll('[data-group-required]').forEach(function(grid) {
    var id    = grid.id.replace('-grid', '').replace('-', '_');
    var errEl = document.getElementById('err-' + id);
    var nChk  = grid.querySelectorAll('input[type="checkbox"]:checked').length;

    if (nChk === 0) {
      grid.classList.add('invalid');
      if (errEl) errEl.classList.add('show');
      ok = false;
    } else {
      grid.classList.remove('invalid');
      if (errEl) errEl.classList.remove('show');
    }
  });

  return ok;
}

/* ── Navigate forward / backward ── */
function changeStep(dir) {
  if (dir === 1) {
    if (!validateStep(cur)) {
      showToast('⚠️ Please fill in all required fields before continuing.');
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

/* ── Jump to a completed step ── */
function jumpTo(target) {
  if (target >= cur) return;
  back = target < cur;
  cur  = target;
  buildProgress();
  showPanel(cur);
}

/* ── Review helpers ── */
function fv(id) {
  var e = document.getElementById(id);
  return e ? e.value.trim() : '';
}
function ol(id) {
  var e = document.getElementById(id);
  return (e && e.selectedIndex >= 0) ? e.options[e.selectedIndex].text : '—';
}
function ckd(gid) {
  var g = document.getElementById(gid);
  if (!g) return [];
  return Array.prototype.slice.call(g.querySelectorAll('input:checked')).map(function(c) {
    var pill = c.closest('.checkbox-pill');
    return pill ? pill.textContent.trim() : c.value;
  });
}
function isChecked(id) {
  var e = document.getElementById(id);
  return e && e.checked;
}

/* ── Build review summary (Step 7) ── */
function buildReview() {
  var grid = document.getElementById('reviewGrid');
  grid.innerHTML = '';

  var sections = [
    { title: '🏥 Basic Information', rows: [
      { l: 'Name',        v: function(){ return fv('id_name') || '—'; } },
      { l: 'Slogan',      v: function(){ return fv('id_slogan') || '—'; } },
      { l: 'Description', v: function(){ return fv('id_description') || '—'; } },
    ]},
    { title: '📍 Location', rows: [
      { l: 'District',   v: function(){ return ol('id_district'); } },
      { l: 'County',     v: function(){ return ol('id_county'); } },
      { l: 'Sub-county', v: function(){ return ol('id_sub_county'); } },
      { l: 'Parish',     v: function(){ return ol('id_parish'); } },
      { l: 'Village',    v: function(){ return ol('id_village'); } },
    ]},
    { title: '📞 Contact', rows: [
      { l: 'Phone',     v: function(){ return fv('id_phone') || '—'; } },
      { l: 'Email',     v: function(){ return fv('id_email') || '—'; } },
      { l: 'Website',   v: function(){ return fv('id_website') || '—'; } },
      { l: 'Emergency', v: function(){ return fv('id_emergency_contact') || '—'; } },
    ]},
    { title: '⚙️ Operations', rows: [
      { l: 'Hours',       v: function(){ var o = fv('id_opening_time'), c = fv('id_closing_time'); return (o && c) ? o + ' – ' + c : '—'; } },
      { l: 'Status',      v: function(){ return ol('id_operation_status'); } },
      { l: 'Main Clinic', v: function(){ return isChecked('id_is_main_clinic') ? 'Yes' : 'No'; } },
      { l: 'Departments', v: function(){ return ckd('dept-grid'); }, badges: true },
      { l: 'Days',        v: function(){ return ckd('days-grid'); }, badges: true },
    ]},
    { title: '🏦 Banking', rows: [
      { l: 'Bank',    v: function(){ return fv('id_bank_name') || '—'; } },
      { l: 'Account', v: function(){ return fv('id_bank_account_number') || '—'; } },
      { l: 'Branch',  v: function(){ return fv('id_bank_branch') || '—'; } },
    ]},
    { title: '📋 Licensing', rows: [
      { l: 'Body',       v: function(){ return ol('id_licensing_body'); } },
      { l: 'Reg. No.',   v: function(){ return fv('id_registration_number') || '—'; } },
      { l: 'Reg. Date',  v: function(){ return fv('id_registration_date') || '—'; } },
      { l: 'Expiry',     v: function(){ return fv('id_licence_expiry_date') || '—'; } },
      { l: 'Supervisor', v: function(){ return (ol('id_supervisor_title') || '') + ' ' + (fv('id_supervisor') || ''); } },
      { l: 'Active',     v: function(){ return isChecked('id_is_active') ? 'Yes' : 'No'; } },
    ]},
  ];

  sections.forEach(function(sec) {
    var card = document.createElement('div');
    card.className = 'review-card';
    card.innerHTML = '<div class="review-card-title">' + sec.title + '</div>';

    sec.rows.forEach(function(row) {
      var val   = row.v();
      var rowEl = document.createElement('div');
      rowEl.className = 'review-row';

      if (row.badges && Array.isArray(val)) {
        var badges = val.length
          ? val.map(function(v){ return '<span class="rev-badge">' + v + '</span>'; }).join('')
          : '—';
        rowEl.innerHTML =
          '<span class="review-label">' + row.l + '</span>' +
          '<span class="review-value"><div class="rev-badges">' + badges + '</div></span>';
      } else {
        var display = Array.isArray(val) ? (val.join(', ') || '—') : val;
        rowEl.innerHTML =
          '<span class="review-label">' + row.l + '</span>' +
          '<span class="review-value">' + display + '</span>';
      }
      card.appendChild(rowEl);
    });

    grid.appendChild(card);
  });
}

/* ── Logo preview ── */
function previewLogo(input) {
  if (input.files && input.files[0]) {
    var reader = new FileReader();
    reader.onload = function(e) {
      document.getElementById('logoPreview').innerHTML =
        '<img src="' + e.target.result + '" style="height:52px;border-radius:8px;border:1px solid var(--border);object-fit:contain;padding:4px;">' +
        '<span class="field-hint">New logo selected</span>';
    };
    reader.readAsDataURL(input.files[0]);
  }
}

/* ── Toast notification ── */
function showToast(msg) {
  var t = document.getElementById('toastMsg');
  t.textContent = msg;
  t.classList.add('show');
  setTimeout(function(){ t.classList.remove('show'); }, 3400);
}

/* ── Checkbox pill visual sync ── */
function initPills() {
  document.querySelectorAll('.checkbox-pill').forEach(function(pill) {
    var cb = pill.querySelector('input[type="checkbox"]');
    if (!cb) return;
    pill.addEventListener('click', function() {
      setTimeout(function(){ pill.classList.toggle('pill-on', cb.checked); }, 0);
    });
  });
}

/* ── Submit guard: re-validate all steps before allowing POST ── */
function initSubmitGuard() {
  document.getElementById('clinicForm').addEventListener('submit', function(e) {
    var allOk    = true;
    var firstBad = -1;

    for (var s = 1; s < TOTAL; s++) {
      if (!validateStep(s)) {
        allOk = false;
        if (firstBad === -1) firstBad = s;
      }
    }

    if (!allOk) {
      e.preventDefault();
      back = false;
      cur  = firstBad;
      buildProgress();
      showPanel(cur);
      showToast('⚠️ Please complete all required fields before submitting.');
    }
  });
}

/* ════════════════════════════════════
   INIT
   Called from the Django template inline
   <script> block to pass the server-side
   determined start step.

   Usage in template:
     initStepForm(startStep);
════════════════════════════════════ */
function initStepForm(startStep) {
  cur = startStep || 1;
  initPills();
  initSubmitGuard();
  buildProgress();
  showPanel(cur);
}
