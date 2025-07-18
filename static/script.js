function login() {
  const username = document.getElementById('login-username').value;
  const password = document.getElementById('login-password').value;

  fetch('/api/auth/login', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ username, password })
  })
  .then(res => res.json())
  .then(data => {
    if (data.access_token) {
      localStorage.setItem('token', data.access_token);
      window.location.href = '/dashboard';
    } else {
      alert(data.msg || 'Login failed');
    }
  });
}

function register() {
  const username = document.getElementById('reg-username').value;
  const password = document.getElementById('reg-password').value;

  fetch('/api/auth/register', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ username, password })
  })
  .then(res => res.json())
  .then(data => {
    alert(data.msg);
  });
}
