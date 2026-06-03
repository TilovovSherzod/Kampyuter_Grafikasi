// Authentication utility functions

function updateAuthNav() {
    const user = JSON.parse(localStorage.getItem('currentUser'));
    const navContainer = document.querySelector('.navbar-nav');
    
    if (!navContainer) return;
    
    // Remove existing auth buttons if any
    const existingAuth = navContainer.querySelector('[data-auth-buttons]');
    if (existingAuth) existingAuth.remove();
    
    // Create auth buttons container
    const authContainer = document.createElement('li');
    authContainer.className = 'nav-item ms-3 d-flex gap-2 align-items-center flex-wrap';
    authContainer.setAttribute('data-auth-buttons', '');
    
    if (user) {
        authContainer.innerHTML = `
            <a href="profile.html" class="nav-link text-warning fw-600" title="Mening profilim">👤 ${user.name}</a>
            <button onclick="logout()" class="btn btn-sm btn-outline-warning" style="font-size: 0.85rem; padding: 6px 12px;">Chiqish</button>
        `;
    } else {
        authContainer.innerHTML = `
            <a href="login.html" class="btn btn-accent btn-sm" style="padding: 8px 16px; font-size: 0.9rem;">Kirish</a>
            <a href="signup.html" class="btn btn-accent-outline btn-sm" style="padding: 8px 16px; font-size: 0.9rem;">Ro'yxat</a>
        `;
    }
    
    navContainer.appendChild(authContainer);
}

function logout() {
    localStorage.removeItem('currentUser');
    alert('Siz chiqib ketdingiz!');
    window.location.href = 'index.html';
}

function checkAuthRequired() {
    const user = JSON.parse(localStorage.getItem('currentUser'));
    if (!user) {
        window.location.href = 'login.html';
        return false;
    }
    return true;
}

// Initialize on page load
document.addEventListener('DOMContentLoaded', function() {
    updateAuthNav();
});
