// SkinRx by Burds Family Practice - progressive enhancements (site remains usable without JS).
(function () {
  // 1. Mobile navigation toggle + outside click / Escape dismissal
  var toggle = document.querySelector('.nav-toggle');
  var nav = document.getElementById('site-nav');
  if (toggle && nav) {
    function closeNav() {
      toggle.setAttribute('aria-expanded', 'false');
      nav.classList.remove('is-open');
    }
    toggle.addEventListener('click', function () {
      var open = toggle.getAttribute('aria-expanded') === 'true';
      toggle.setAttribute('aria-expanded', String(!open));
      nav.classList.toggle('is-open', !open);
    });
    document.addEventListener('keydown', function (e) {
      if (e.key === 'Escape' && nav.classList.contains('is-open')) {
        closeNav();
        toggle.focus();
      }
    });
    document.addEventListener('click', function (e) {
      if (nav.classList.contains('is-open') && !nav.contains(e.target) && !toggle.contains(e.target)) {
        closeNav();
      }
    });
  }

  // 2. Dual-location office hours in Central Time: [openHour, closeHour] per weekday (0 = Sunday)
  var PEOSTA_HOURS = { 0: null, 1: [8, 17], 2: [8, 17], 3: [8, 17], 4: [8, 18], 5: [8, 12], 6: null };
  var DYERSVILLE_HOURS = { 0: null, 1: null, 2: [9, 12], 3: null, 4: [12, 16], 5: null, 6: null };
  var DAY_NAMES = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday'];

  function centralNow() {
    try {
      var parts = new Intl.DateTimeFormat('en-US', {
        timeZone: 'America/Chicago', weekday: 'short', hour: 'numeric', minute: 'numeric', hour12: false
      }).formatToParts(new Date());
      var map = {};
      parts.forEach(function (p) { map[p.type] = p.value; });
      var day = ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat'].indexOf(map.weekday);
      return { day: day, hour: (parseInt(map.hour, 10) % 24) + parseInt(map.minute, 10) / 60 };
    } catch (e) {
      var d = new Date();
      return { day: d.getDay(), hour: d.getHours() + d.getMinutes() / 60 };
    }
  }

  function fmtHour(h) {
    var suffix = h >= 12 ? 'pm' : 'am';
    var hr = h % 12 === 0 ? 12 : h % 12;
    return hr + ' ' + suffix;
  }

  function nextOpening(schedule, day, hour) {
    var todaySlot = schedule[day];
    if (todaySlot && hour < todaySlot[0]) {
      return 'today at ' + fmtHour(todaySlot[0]);
    }
    for (var i = 1; i <= 7; i++) {
      var d = (day + i) % 7;
      if (schedule[d]) {
        return (i === 1 ? 'tomorrow' : DAY_NAMES[d]) + ' at ' + fmtHour(schedule[d][0]);
      }
    }
    return '';
  }

  var now = centralNow();
  var pToday = PEOSTA_HOURS[now.day];
  var dToday = DYERSVILLE_HOURS[now.day];
  var pOpen = !!(pToday && now.hour >= pToday[0] && now.hour < pToday[1]);
  var dOpen = !!(dToday && now.hour >= dToday[0] && now.hour < dToday[1]);
  var anyOpen = pOpen || dOpen;

  var statusText;
  if (pOpen && dOpen) {
    statusText = 'Open now: Peosta (until ' + fmtHour(pToday[1]) + ') & Dyersville (until ' + fmtHour(dToday[1]) + ')';
  } else if (pOpen) {
    statusText = 'Peosta open now · until ' + fmtHour(pToday[1]) + ' today';
  } else if (dOpen) {
    statusText = 'Dyersville open now · until ' + fmtHour(dToday[1]) + ' today';
  } else {
    statusText = 'Closed now · Peosta opens ' + nextOpening(PEOSTA_HOURS, now.day, now.hour);
  }

  document.querySelectorAll('[data-open-status]').forEach(function (el) {
    el.innerHTML = '<span class="dot" aria-hidden="true"></span>' + statusText;
    el.classList.toggle('is-open', anyOpen);
  });

  document.querySelectorAll('.hours tr[data-days]').forEach(function (row) {
    var days = row.getAttribute('data-days').split(',').map(Number);
    if (days.indexOf(now.day) !== -1) row.classList.add('is-today');
  });

  document.querySelectorAll('[data-year]').forEach(function (el) {
    el.textContent = new Date().getFullYear();
  });

  // 3. Interactive Aesthetic Treatment Plan & Cherry Financing Estimator
  document.querySelectorAll('[data-plan-calc]').forEach(function (calc) {
    var presets = Array.prototype.slice.call(calc.querySelectorAll('[data-plan-preset]'));
    var selectEl = calc.querySelector('[data-plan-select]');
    var addons = Array.prototype.slice.call(calc.querySelectorAll('[data-plan-addon]'));
    var customInput = calc.querySelector('[data-plan-custom]');
    var termBtns = Array.prototype.slice.call(calc.querySelectorAll('[data-cherry-term]'));

    var monthlyOut = calc.querySelector('[data-plan-monthly]');
    var totalOut = calc.querySelector('[data-plan-total]');
    var termOut = calc.querySelector('[data-plan-term-label]');
    var breakdownOut = calc.querySelector('[data-plan-breakdown]');
    var noteOut = calc.querySelector('[data-plan-note]');

    var state = {
      basePrice: 1650,
      baseLabel: 'Exion RF Microneedling (Series of 3)',
      note: 'Subject to Cherry approval. 0% APR options available for qualifying applicants; standard APRs start at 5.99%.',
      months: 6,
      apr: 0,
      customMode: false
    };

    var activePreset = presets.find(function (b) { return b.classList.contains('is-active'); }) || presets[0];
    if (activePreset) {
      state.basePrice = parseFloat(activePreset.getAttribute('data-price')) || state.basePrice;
      state.baseLabel = activePreset.getAttribute('data-label') || activePreset.textContent.trim();
      if (activePreset.getAttribute('data-note')) state.note = activePreset.getAttribute('data-note');
    } else if (selectEl && selectEl.options.length) {
      var opt = selectEl.options[selectEl.selectedIndex];
      state.basePrice = parseFloat(opt.value) || state.basePrice;
      state.baseLabel = opt.getAttribute('data-label') || opt.textContent.trim();
    } else if (customInput) {
      state.basePrice = parseFloat(customInput.value) || state.basePrice;
      state.baseLabel = 'Custom Treatment Plan';
      state.customMode = true;
    }

    var activeTerm = termBtns.find(function (b) { return b.classList.contains('is-active'); }) || termBtns[0];
    if (activeTerm) {
      state.months = parseInt(activeTerm.getAttribute('data-months') || activeTerm.getAttribute('data-cherry-term'), 10) || 6;
      state.apr = parseFloat(activeTerm.getAttribute('data-apr')) || 0;
    }

    function money(n) {
      return '$' + Math.round(n).toLocaleString('en-US');
    }

    function calcMonthly(principal, months, apr) {
      if (principal <= 0 || months <= 0) return 0;
      if (!apr || apr <= 0) return principal / months;
      var r = (apr / 100) / 12;
      return principal * (r * Math.pow(1 + r, months)) / (Math.pow(1 + r, months) - 1);
    }

    function render() {
      var addonSum = 0;
      var parts = [state.baseLabel + ' (' + money(state.basePrice) + ')'];
      addons.forEach(function (cb) {
        if (cb.checked) {
          var p = parseFloat(cb.getAttribute('data-price')) || 0;
          var lbl = cb.getAttribute('data-label') || 'Add-on';
          addonSum += p;
          parts.push(lbl + ' (+' + money(p) + ')');
        }
      });

      var total = state.basePrice + addonSum;
      var monthly = calcMonthly(total, state.months, state.apr);

      if (customInput && !state.customMode) {
        customInput.value = String(Math.round(state.basePrice));
      }
      if (monthlyOut) monthlyOut.textContent = money(monthly) + '/mo';
      if (totalOut) totalOut.textContent = money(total) + ' estimated treatment total';
      if (termOut) {
        termOut.textContent = state.apr === 0
          ? state.months + ' monthly payments at 0% APR (qualifying promo estimate)'
          : state.months + ' monthly payments (illustrative ' + state.apr + '% APR estimate)';
      }
      if (breakdownOut) breakdownOut.textContent = 'Plan includes: ' + parts.join(' + ');
      if (noteOut) noteOut.textContent = state.note;
    }

    presets.forEach(function (btn) {
      btn.addEventListener('click', function () {
        state.customMode = false;
        state.basePrice = parseFloat(btn.getAttribute('data-price')) || 0;
        state.baseLabel = btn.getAttribute('data-label') || btn.textContent.trim();
        if (btn.getAttribute('data-note')) state.note = btn.getAttribute('data-note');
        presets.forEach(function (b) {
          var isOn = b === btn;
          b.classList.toggle('is-active', isOn);
          b.setAttribute('aria-pressed', String(isOn));
        });
        if (selectEl) {
          Array.prototype.forEach.call(selectEl.options, function (opt) {
            if (parseFloat(opt.value) === state.basePrice) selectEl.value = opt.value;
          });
        }
        render();
      });
    });

    if (selectEl) {
      selectEl.addEventListener('change', function () {
        state.customMode = false;
        var opt = selectEl.options[selectEl.selectedIndex];
        state.basePrice = parseFloat(opt.value) || 0;
        state.baseLabel = opt.getAttribute('data-label') || opt.textContent.trim();
        if (opt.getAttribute('data-note')) state.note = opt.getAttribute('data-note');
        presets.forEach(function (b) {
          var match = (b.getAttribute('data-label') || b.textContent.trim()) === state.baseLabel;
          b.classList.toggle('is-active', match);
          b.setAttribute('aria-pressed', String(match));
        });
        render();
      });
    }

    addons.forEach(function (cb) {
      cb.addEventListener('change', render);
    });

    if (customInput) {
      customInput.addEventListener('input', function () {
        state.customMode = true;
        state.basePrice = Math.max(100, Math.min(50000, parseFloat(customInput.value) || 0));
        state.baseLabel = 'Custom Treatment Plan';
        presets.forEach(function (b) {
          b.classList.remove('is-active');
          b.setAttribute('aria-pressed', 'false');
        });
        render();
      });
    }

    termBtns.forEach(function (btn) {
      btn.addEventListener('click', function () {
        state.months = parseInt(btn.getAttribute('data-months') || btn.getAttribute('data-cherry-term'), 10) || 6;
        state.apr = parseFloat(btn.getAttribute('data-apr')) || 0;
        termBtns.forEach(function (b) {
          var isOn = b === btn;
          b.classList.toggle('is-active', isOn);
          b.setAttribute('aria-pressed', String(isOn));
        });
        render();
      });
    });

    render();
  });

  // 4. Generic Topic Filter & Live Search (Treatments + Resources)
  document.querySelectorAll('[data-topic-filter], [data-resource-filter]').forEach(function (filterBox) {
    var searchInput = filterBox.querySelector('[data-topic-search], [data-resource-search]');
    var topicBtns = filterBox.querySelectorAll('[data-topic-btn]');
    var countEl = filterBox.querySelector('[data-topic-count], [data-resource-count]');
    var emptyEl = filterBox.querySelector('[data-topic-empty], [data-resource-empty]') || document.querySelector('[data-topic-empty], [data-resource-empty]');
    var resetBtn = filterBox.querySelector('[data-topic-reset], [data-resource-reset]') || document.querySelector('[data-topic-reset], [data-resource-reset]');
    var sections = document.querySelectorAll('[data-topic-section], [data-resource-section]');
    var items = Array.prototype.slice.call(document.querySelectorAll('[data-topic]'));
    var noun = filterBox.getAttribute('data-count-noun') || (countEl && countEl.getAttribute('data-count-noun')) || 'items';
    var activeTopic = 'all';

    function applyFilter() {
      var q = (searchInput ? searchInput.value : '').trim().toLowerCase();
      var visibleTotal = 0;

      if (sections.length) {
        sections.forEach(function (sec) {
          var secItems = sec.querySelectorAll('[data-topic]');
          if (!secItems.length) return;
          var secVisible = 0;
          secItems.forEach(function (item) {
            var topic = item.getAttribute('data-topic') || '';
            var matchTopic = activeTopic === 'all' || topic.split(/\s+/).indexOf(activeTopic) !== -1;
            var matchText = !q || item.textContent.toLowerCase().indexOf(q) !== -1;
            var show = matchTopic && matchText;
            item.hidden = !show;
            if (show) {
              secVisible++;
              visibleTotal++;
            }
          });
          sec.hidden = secVisible === 0;
        });
      } else {
        items.forEach(function (item) {
          var topic = item.getAttribute('data-topic') || '';
          var matchTopic = activeTopic === 'all' || topic.split(/\s+/).indexOf(activeTopic) !== -1;
          var matchText = !q || item.textContent.toLowerCase().indexOf(q) !== -1;
          var show = matchTopic && matchText;
          item.hidden = !show;
          if (show) visibleTotal++;
        });
      }

      if (countEl) {
        countEl.textContent = 'Showing ' + visibleTotal + ' of ' + items.length + ' ' + noun;
      }
      if (emptyEl) {
        emptyEl.hidden = visibleTotal !== 0;
      }
    }

    topicBtns.forEach(function (btn) {
      btn.addEventListener('click', function () {
        activeTopic = btn.getAttribute('data-topic-btn') || 'all';
        topicBtns.forEach(function (b) {
          var active = b === btn;
          b.classList.toggle('is-active', active);
          b.setAttribute('aria-pressed', String(active));
        });
        applyFilter();
      });
    });

    if (searchInput) {
      searchInput.addEventListener('input', applyFilter);
    }

    if (resetBtn) {
      resetBtn.addEventListener('click', function () {
        activeTopic = 'all';
        if (searchInput) searchInput.value = '';
        topicBtns.forEach(function (b) {
          var active = b.getAttribute('data-topic-btn') === 'all';
          b.classList.toggle('is-active', active);
          b.setAttribute('aria-pressed', String(active));
        });
        applyFilter();
      });
    }

    applyFilter();
  });

  // 5. Guided Consultation & Callback Inquiry Builder (static-safe email + copy summary)
  document.querySelectorAll('form[data-inquiry-form]').forEach(function (form) {
    var resultBox = form.parentElement.querySelector('[data-inquiry-result]');
    var previewEl = form.parentElement.querySelector('[data-inquiry-preview]');
    var mailtoEl = form.parentElement.querySelector('[data-inquiry-mailto]');
    var copyBtn = form.parentElement.querySelector('[data-inquiry-copy]');
    var errEl = form.querySelector('[data-inquiry-error]');
    var latestSummary = '';

    form.addEventListener('submit', function (e) {
      e.preventDefault();
      var name = (form.elements.name && form.elements.name.value || '').trim();
      var contact = (form.elements.contact && form.elements.contact.value || '').trim();
      var location = (form.elements.location && form.elements.location.value || '').trim();
      var topic = (form.elements.topic && form.elements.topic.value || 'SkinRx Aesthetic Consultation').trim();
      var timing = (form.elements.timing && form.elements.timing.value || 'Any weekday window').trim();
      var notes = (form.elements.notes && form.elements.notes.value || '').trim();

      if (!name || !contact) {
        if (errEl) {
          errEl.textContent = 'Please enter your name and preferred phone number or email address.';
          errEl.hidden = false;
        }
        return;
      }
      if (errEl) errEl.hidden = true;

      var lines = [
        'Clinic: SkinRx by Burds Family Practice',
        'Consultation / Interest: ' + topic,
        'Name: ' + name,
        'Preferred Contact: ' + contact
      ];
      if (location) lines.push('Preferred Location: ' + location);
      lines.push('Best Time to Reach: ' + timing);
      if (notes) lines.push('Goals / Notes (Non-Urgent): ' + notes);
      latestSummary = lines.join('\n');

      if (previewEl) previewEl.textContent = latestSummary;
      if (mailtoEl) {
        var subject = encodeURIComponent('SkinRx Inquiry: ' + topic + ' (' + name + ')');
        var body = encodeURIComponent(latestSummary + '\n\nSent from burdsskinrx.com');
        mailtoEl.href = 'mailto:bfpstaff@burdsfamilypractice.com?subject=' + subject + '&body=' + body;
      }
      if (resultBox) {
        resultBox.hidden = false;
        resultBox.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
      }
    });

    if (copyBtn) {
      copyBtn.addEventListener('click', function () {
        if (!latestSummary || !navigator.clipboard) return;
        navigator.clipboard.writeText(latestSummary).then(function () {
          var prev = copyBtn.textContent;
          copyBtn.textContent = 'Copied to Clipboard';
          setTimeout(function () { copyBtn.textContent = prev; }, 2000);
        });
      });
    }
  });

  // 6. FAQ Expand / Collapse All toggle
  document.querySelectorAll('[data-faq-toggle]').forEach(function (btn) {
    var targetSel = btn.getAttribute('data-faq-target');
    var container = (targetSel && document.querySelector(targetSel)) || btn.parentElement.nextElementSibling || btn.closest('.section');
    if (!container) return;
    btn.addEventListener('click', function () {
      var details = container.querySelectorAll('details');
      if (!details.length) return;
      var anyClosed = false;
      details.forEach(function (d) { if (!d.open) anyClosed = true; });
      details.forEach(function (d) { d.open = anyClosed; });
      btn.textContent = anyClosed ? 'Collapse all questions' : 'Expand all questions';
    });
  });

  // 7. Back to top visibility & smooth click
  var topBtn = document.querySelector('.back-to-top');
  if (topBtn) {
    topBtn.hidden = false;
    function syncTop() {
      topBtn.classList.toggle('is-visible', window.scrollY > 520);
    }
    window.addEventListener('scroll', syncTop, { passive: true });
    syncTop();
    topBtn.addEventListener('click', function () {
      window.scrollTo({ top: 0, behavior: 'smooth' });
    });
  }
})();
