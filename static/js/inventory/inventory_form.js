/**
 * inventory_form.js
 * Save to: static/js/inventory/inventory_form.js
 *
 * Handles:
 *  - Multi-step navigation (4 steps)
 *  - Per-step field validation
 *  - Progress bar + step indicator
 *  - Pill checkbox toggle behaviour
 *  - Review/summary generation on step 4
 *  - Toast notifications
 */

/* ═══════════════════════════════════════════
   CONFIGURATION
═══════════════════════════════════════════ */
const INV_STEPS = [
  {
    id:    'invStep1',
    label: 'Drug ID',
    icon:  '💊',
    requiredFields: ['brand_name', 'generic_name', 'formulation'],
    groupRequired:  ['drug_categories'],
  },
  {
    id:    'invStep2',
    label: 'Stock',
    icon:  '📊',
    requiredFields: ['sale_price', 'sale_unit'],
    groupRequired:  [],
  },
  {
    id:    'invStep3',
    label: 'Status',
    icon:  '🔧',
    requiredFields: [],
    groupRequired:  [],
  },
  {
    id:    'invStep4',
    label: 'Review',
    icon:  '✅',
    requiredFields: [],
    groupRequired:  [],
  },
];

const TOTAL_STEPS = INV_STEPS.length;
let currentStep   = 1;

/* ═══════════════════════════════════════════
   INIT
═══════════════════════════════════════════ */
function initInvForm(startStep) {
  startStep = startStep || 1;
  buildProgressBar();
  bindPillCheckboxes();
  bindNavButtons();
  goToStep(startStep, 'forward');
}

/* ═══════════════════════════════════════════
   PROGRESS BAR
═══════════════════════════════════════════ */
function buildProgressBar() {
  const container = document.getElementById('invProgressSteps');
  if (!container) return;

  container.innerHTML = '';

  INV_STEPS.forEach(function (step, idx) {
    const num = idx + 1;

    // Step node
    const node = document.createElement('div');
    node.className   = 'inv-prog-step';
    node.id          = 'invProgStep' + num;
    node.innerHTML   = `
      <div class="inv-prog-circle">${num}</div>
      <div class="inv-prog-label">${step.label}</div>
    `;
    node.addEventListener('click', function () {
      // Allow clicking already-completed steps to go back
      if (num < currentStep) goToStep(num, 'backward');
    });
    container.appendChild(node);

    // Connector (between steps)
    if (idx < INV_STEPS.length - 1) {
      const conn = document.createElement('div');
      conn.className = 'inv-prog-connector';
      conn.id        = 'invConn' + num;
      container.appendChild(conn);
    }
  });
}

function updateProgressBar(step) {
  INV_STEPS.forEach(function (_, idx) {
    const num  = idx + 1;
    const node = document.getElementById('invProgStep' + num);
    if (!node) return;

    node.classList.remove('active', 'done');
    if (num === step)  node.classList.add('active');
    if (num < step)    node.classList.add('done');

    // Update connector
    const conn = document.getElementById('invConn' + num);
    if (conn) {
      conn.classList.toggle('done', num < step);
    }
  });

  // Fill bar
  const fill = document.getElementById('invProgressFill');
  if (fill) {
    const pct = step === 1 ? 2 : Math.round(((step - 1) / (TOTAL_STEPS - 1)) * 100);
    fill.style.width = pct + '%';
  }

  // Counter
  const counter = document.getElementById('invStepCounter');
  if (counter) counter.textContent = 'Step ' + step + ' of ' + TOTAL_STEPS;
}

/* ═══════════════════════════════════════════
   NAVIGATION
═══════════════════════════════════════════ */
function bindNavButtons() {
  const btnPrev = document.getElementById('invBtnPrev');
  const btnNext = document.getElementById('invBtnNext');

  if (btnPrev) btnPrev.addEventListener('click', function () { changeInvStep(-1); });
  if (btnNext) btnNext.addEventListener('click', function () { changeInvStep(1); });
}

function changeInvStep(direction) {
  if (direction === 1 && !validateStep(currentStep)) return;
  const next = currentStep + direction;
  if (next < 1 || next > TOTAL_STEPS) return;
  goToStep(next, direction === 1 ? 'forward' : 'backward');
}

function goToStep(step, direction) {
  // Hide current panel
  const currentPanel = document.getElementById(INV_STEPS[currentStep - 1].id);
  if (currentPanel) currentPanel.classList.remove('active', 'go-back');

  currentStep = step;

  // Show new panel
  const newPanel = document.getElementById(INV_STEPS[step - 1].id);
  if (newPanel) {
    newPanel.classList.remove('go-back');
    if (direction === 'backward') newPanel.classList.add('go-back');
    newPanel.classList.add('active');
  }

  // If review step, build summary
  if (step === TOTAL_STEPS) buildReview();

  // Buttons
  const btnPrev   = document.getElementById('invBtnPrev');
  const btnNext   = document.getElementById('invBtnNext');
  const btnSubmit = document.getElementById('invBtnSubmit');

  if (btnPrev)   btnPrev.disabled          = step === 1;
  if (btnNext)   btnNext.style.display     = step === TOTAL_STEPS ? 'none'   : '';
  if (btnSubmit) btnSubmit.style.display   = step === TOTAL_STEPS ? ''       : 'none';

  updateProgressBar(step);
  window.scrollTo({ top: 0, behavior: 'smooth' });
}

/* ═══════════════════════════════════════════
   VALIDATION
═══════════════════════════════════════════ */
function validateStep(step) {
  const cfg     = INV_STEPS[step - 1];
  let   isValid = true;

  // Single required fields
  cfg.requiredFields.forEach(function (name) {
    const el  = document.querySelector('[name="' + name + '"]');
    const err = document.getElementById('err-' + name);
    if (!el) return;

    const empty = !el.value || el.value.trim() === '';
    el.classList.toggle('invalid', empty);
    if (err) err.classList.toggle('show', empty);
    if (empty) isValid = false;
  });

  // Group-required (checkboxes)
  cfg.groupRequired.forEach(function (name) {
    const checked = document.querySelectorAll('[name="' + name + '"]:checked').length;
    const err     = document.getElementById('err-' + name);
    const grid    = document.querySelector('[data-name="' + name + '"]');

    if (grid)  grid.classList.toggle('invalid', checked === 0);
    if (err)   err.classList.toggle('show', checked === 0);
    if (checked === 0) isValid = false;
  });

  if (!isValid) showToast('⚠ Please fill in all required fields', 'error');
  return isValid;
}

/* ═══════════════════════════════════════════
   PILL CHECKBOXES
═══════════════════════════════════════════ */
function bindPillCheckboxes() {
  document.querySelectorAll('.inv-pill').forEach(function (pill) {
    const cb = pill.querySelector('input[type="checkbox"]');
    if (!cb) return;

    // Sync initial state
    pill.classList.toggle('pill-on', cb.checked);

    pill.addEventListener('click', function () {
      cb.checked = !cb.checked;
      pill.classList.toggle('pill-on', cb.checked);

      // Clear group error if now at least one is checked
      const groupName = cb.name;
      const anyChecked = document.querySelectorAll('[name="' + groupName + '"]:checked').length > 0;
      const err = document.getElementById('err-' + groupName);
      if (err && anyChecked) err.classList.remove('show');
    });
  });
}

/* ═══════════════════════════════════════════
   REVIEW BUILDER
═══════════════════════════════════════════ */
function buildReview() {
  const grid = document.getElementById('invReviewGrid');
  if (!grid) return;

  const val = function (name) {
    const el = document.querySelector('[name="' + name + '"]');
    if (!el) return '—';
    return el.value.trim() || '—';
  };

  const selectLabel = function (name) {
    const el = document.querySelector('[name="' + name + '"]');
    if (!el || !el.options) return '—';
    return el.options[el.selectedIndex]
      ? el.options[el.selectedIndex].text
      : '—';
  };

  const checkboxLabels = function (name) {
    const labels = [];
    document.querySelectorAll('[name="' + name + '"]:checked').forEach(function (cb) {
      const pill = cb.closest('.inv-pill');
      if (pill) labels.push(pill.textContent.trim());
    });
    return labels;
  };

  const toggleVal = function (name) {
    const el = document.querySelector('[name="' + name + '"]');
    return el && el.checked ? 'Yes' : 'No';
  };

  const sections = [
    {
      title: '💊 Drug Identification',
      rows: [
        { label: 'Brand Name',    value: val('brand_name') },
        { label: 'Generic Name',  value: val('generic_name') },
        { label: 'Categories',    value: checkboxLabels('drug_categories'), isBadges: true },
        { label: 'Formulation',   value: selectLabel('formulation') },
        { label: 'Storage',       value: selectLabel('storage_condition') },
      ],
    },
    {
      title: '📊 Stock & Pricing',
      rows: [
        { label: 'Reorder Level', value: val('reorder_level') || '—' },
        { label: 'Stock Target',  value: val('stock_target') || '—' },
        { label: 'Sale Price',    value: val('sale_price') ? 'UGX ' + val('sale_price') : '—' },
        { label: 'Sale Unit',     value: selectLabel('sale_unit') },
      ],
    },
    {
      title: '🔧 Status Flags',
      rows: [
        { label: 'Active',            value: toggleVal('is_active') },
        { label: 'Pause Stocking',    value: toggleVal('pause_stocking') },
        { label: 'Discontinued',      value: toggleVal('discontinued') },
      ],
    },
  ];

  grid.innerHTML = sections.map(function (sec) {
    const rows = sec.rows.map(function (row) {
      let valueHtml;
      if (row.isBadges && Array.isArray(row.value)) {
        if (row.value.length === 0) {
          valueHtml = '<span class="inv-review-value">—</span>';
        } else {
          valueHtml = '<div class="inv-rev-badges">' +
            row.value.map(function (v) {
              return '<span class="inv-rev-badge">' + v + '</span>';
            }).join('') +
            '</div>';
        }
      } else {
        valueHtml = '<span class="inv-review-value">' + (row.value || '—') + '</span>';
      }
      return '<div class="inv-review-row">' +
        '<span class="inv-review-label">' + row.label + '</span>' +
        valueHtml +
        '</div>';
    }).join('');

    return '<div class="inv-review-card">' +
      '<div class="inv-review-card-title">' + sec.title + '</div>' +
      rows +
      '</div>';
  }).join('');
}

/* ═══════════════════════════════════════════
   BOOT  — reads Django-rendered JSON, never
   mixes template tags with JS syntax
═══════════════════════════════════════════ */
document.addEventListener('DOMContentLoaded', function () {
  var startStep = 1;

  var dataEl = document.getElementById('invBootData');
  if (dataEl) {
    try {
      var boot = JSON.parse(dataEl.textContent);
      if (boot.hasErrors && boot.errorFields.length) {
        var stepMap = {
          1: ['brand_name', 'generic_name', 'drug_categories', 'formulation', 'storage_condition'],
          2: ['reorder_level', 'stock_target', 'sale_price', 'sale_unit'],
          3: ['discontinued', 'pause_stocking', 'is_active'],
        };
        outer:
        for (var s = 1; s <= 3; s++) {
          for (var i = 0; i < stepMap[s].length; i++) {
            if (boot.errorFields.indexOf(stepMap[s][i]) !== -1) {
              startStep = s;
              break outer;
            }
          }
        }
      }
    } catch (e) {
      console.warn('invBootData parse error', e);
    }
  }

  initInvForm(startStep);
});

/* ═══════════════════════════════════════════
   TOAST
═══════════════════════════════════════════ */
function showToast(msg, type) {
  const toast = document.getElementById('invToast');
  if (!toast) return;

  toast.textContent = msg;
  toast.style.background = type === 'error' ? '#7f1d1d' : '#1e293b';
  toast.classList.add('show');

  setTimeout(function () {
    toast.classList.remove('show');
  }, 2800);
}