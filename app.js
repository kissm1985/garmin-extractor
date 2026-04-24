window.addEventListener('DOMContentLoaded', function () {
  var apiInput = document.getElementById('apiUrl');
  var saveBtn = document.getElementById('saveApiBtn');
  var garminBtn = document.getElementById('testGarminBtn');
  var driveBtn = document.getElementById('testDriveBtn');
  var runBtn = document.getElementById('runBtn');

  var saved = localStorage.getItem('garminExtractorApi') || '';
  apiInput.value = saved;
  setBadge(saved);

  function setBadge(url) {
    var badge = document.getElementById('apiBadge');
    badge.textContent = url ? 'API: beállítva' : 'API: nincs beállítva';
  }

  function show(targetId, data) {
    document.getElementById(targetId).textContent = JSON.stringify(data, null, 2);
  }

  function getApi() {
    return (localStorage.getItem('garminExtractorApi') || '').replace(/\/$/, '');
  }

  async function callApi(path, targetId) {
    var base = getApi();
    if (!base) {
      show(targetId, { status: 'ERROR', message: 'Először add meg és mentsd az API URL-t.' });
      return;
    }

    show(targetId, { status: 'RUNNING', message: 'Kérés folyamatban...' });

    try {
      var response = await fetch(base + path, { method: 'GET' });
      var data = await response.json();
      show(targetId, data);
    } catch (err) {
      show(targetId, { status: 'ERROR', message: String(err) });
    }
  }

  saveBtn.addEventListener('click', function () {
    var url = apiInput.value.trim().replace(/\/$/, '');
    localStorage.setItem('garminExtractorApi', url);
    setBadge(url);
    document.getElementById('logBox').textContent = 'API URL mentve: ' + url;
  });

  garminBtn.addEventListener('click', function () {
    callApi('/test-garmin', 'garminResult');
  });

  driveBtn.addEventListener('click', function () {
    callApi('/test-drive', 'driveResult');
  });

  runBtn.addEventListener('click', function () {
    callApi('/run', 'runResult');
  });
});
