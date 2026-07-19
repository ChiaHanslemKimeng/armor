import re

with open('c:/Users/HANSLEM_KIMENG/Desktop/WEB/Armor/templates/base.html', 'r', encoding='utf-8') as f:
    content = f.read()

# I will replace the <header> block entirely
new_header = """    <header class="header-main-bar sticky-top" style="z-index: 1040 !important;">
        <div class="container py-2">
            <!-- Mobile Layout (Visible only on lg and below) -->
            <div class="d-flex d-lg-none flex-column gap-2 w-100">
                <div class="d-flex justify-content-between align-items-center w-100">
                    <button class="btn btn-dark rounded-2 p-0 d-flex align-items-center justify-content-center shadow-sm border-glass" type="button" data-bs-toggle="offcanvas" data-bs-target="#mobileMenuOffcanvas" aria-controls="mobileMenuOffcanvas" id="stickyMenuToggleMobile" title="Open Menu" style="width: 44px; height: 44px; background: #0f172a; border-color: #ffb800 !important;">
                        <i class="bi bi-list fs-3 text-warning" style="color: #ffb800 !important;"></i>
                    </button>
                    
                    <a class="navbar-brand d-flex align-items-center m-0" href="/">
                        <img src="{% static 'images/glocks_and_armor_logo.png' %}" alt="Glocks And Armor" style="height: 40px; object-fit: contain;">
                    </a>

                    <div class="d-flex align-items-center gap-2">
                        <a href="/orders/cart/" class="btn-tactical-yellow rounded-circle p-0 d-flex align-items-center justify-content-center shadow-sm position-relative" style="width: 44px; height: 44px;" title="Shopping Cart" data-bs-toggle="offcanvas" data-bs-target="#cartOffcanvas" aria-controls="cartOffcanvas">
                            <i class="bi bi-cart3 fs-5"></i>
                            <span class="badge bg-danger rounded-pill font-monospace position-absolute top-0 start-100 translate-middle" style="font-size: 0.65rem; padding: 0.25rem 0.45rem;">{{ cart_count|default:"0" }}</span>
                        </a>
                    </div>
                </div>
                
                <form method="GET" action="/products/" class="d-flex w-100">
                    <div class="input-group shadow-sm w-100">
                        <input type="text" name="q" class="form-control header-search-input px-3 py-2 fs-6 rounded-start" placeholder="Search products..." value="{{ current_query|default:'' }}" style="background: #ffffff !important; color: #0f172a !important;">
                        <button type="submit" class="btn-tactical-yellow px-3 py-2 m-0 rounded-end fs-6" title="Search">
                            <i class="bi bi-search"></i>
                        </button>
                    </div>
                </form>
            </div>

            <!-- Desktop Layout (Visible only on lg and above) -->
            <div class="d-none d-lg-flex justify-content-between align-items-center gap-3 w-100">
                <div class="d-flex align-items-center gap-3">
                    <a class="navbar-brand d-flex align-items-center gap-3 font-outfit fw-black fs-3 text-dark tracking-tight text-decoration-none" href="/">
                        <img src="{% static 'images/glocks_and_armor_logo.png' %}" alt="Glocks And Armor" style="height: 50px; object-fit: contain;">
                    </a>
                    <button class="btn btn-dark rounded-2 p-0 d-flex align-items-center justify-content-center shadow-sm border-glass ms-2" type="button" data-bs-toggle="offcanvas" data-bs-target="#mobileMenuOffcanvas" aria-controls="mobileMenuOffcanvas" id="stickyMenuToggleDesktop" title="Open Menu" style="width: 44px; height: 44px; background: #0f172a; border-color: #ffb800 !important;">
                        <i class="bi bi-list fs-3 text-warning" style="color: #ffb800 !important;"></i>
                    </button>
                </div>

                <form method="GET" action="/products/" class="d-flex flex-grow-1 mx-lg-4" style="max-width: 750px;">
                    <div class="input-group shadow-sm">
                        <input type="text" name="q" class="form-control header-search-input px-4 py-2 fs-6 rounded-start" placeholder="Search 50,000+ tactical firearms, AR-15 parts, ammo, optics, and schematics..." value="{{ current_query|default:'' }}" style="background: #ffffff !important; color: #0f172a !important;">
                        <button type="submit" class="btn-tactical-yellow px-4 py-2 m-0 rounded-end fs-6" title="Search">
                            <i class="bi bi-search"></i>
                        </button>
                    </div>
                </form>

                <div class="d-flex align-items-center gap-3">
                    <a href="/gun-schematics/" class="text-decoration-none text-dark d-none d-xl-flex align-items-center gap-2 font-outfit fw-bold small px-3 py-2 rounded-3" style="border: 1px solid #cbd5e1; background: #f8fafc;" title="Gun Schematics">
                        <i class="bi bi-tools text-warning fs-5" style="color: #d97706 !important;"></i>
                        <span>Schematics</span>
                    </a>

                    <a href="/orders/cart/" class="btn-tactical-yellow rounded-circle p-0 d-flex align-items-center justify-content-center shadow-sm position-relative" style="width: 44px; height: 44px;" title="Shopping Cart" data-bs-toggle="offcanvas" data-bs-target="#cartOffcanvas" aria-controls="cartOffcanvas">
                        <i class="bi bi-cart3 fs-5"></i>
                        <span class="badge bg-danger rounded-pill font-monospace position-absolute top-0 start-100 translate-middle" id="cart-badge" style="font-size: 0.65rem; padding: 0.25rem 0.45rem;">{{ cart_count|default:"0" }}</span>
                    </a>

                    {% if user.is_authenticated %}
                        <div class="dropdown">
                            <button class="btn btn-dark rounded-circle p-0 d-flex align-items-center justify-content-center shadow-sm border-glass dropdown-toggle" style="width: 44px; height: 44px; background: #0f172a; border-color: #ffb800;" type="button" data-bs-toggle="dropdown" title="Account: {{ user.username }}">
                                <i class="bi bi-person-badge-fill fs-5" style="color: #ffb800;"></i>
                            </button>
                            <ul class="dropdown-menu dropdown-menu-end dropdown-menu-dark border-glass shadow-lg mt-2 p-2 rounded-3" style="background: #0f172a;">
                                {% if user.is_staff %}
                                <li><a class="dropdown-item rounded-2 py-2 small text-white" href="/dashboard/"><i class="bi bi-speedometer2 text-danger me-2"></i> Admin Dashboard</a></li>
                                {% endif %}
                                <li><a class="dropdown-item rounded-2 py-2 small text-white" href="/users/dashboard/"><i class="bi bi-person text-info me-2"></i> My Dashboard ({{ user.username }})</a></li>
                                <li><a class="dropdown-item rounded-2 py-2 small text-white" href="/users/dashboard/#order-history"><i class="bi bi-box-seam text-warning me-2"></i> Order History</a></li>
                                <li><a class="dropdown-item rounded-2 py-2 small text-white" href="/users/2fa/"><i class="bi bi-gear text-secondary me-2"></i> Account Security</a></li>
                                <li><hr class="dropdown-divider border-glass"></li>
                                <li><a class="dropdown-item rounded-2 py-2 small text-danger fw-bold" href="/users/logout/"><i class="bi bi-box-arrow-right me-2"></i> Sign Out</a></li>
                            </ul>
                        </div>
                    {% else %}
                        <a href="/users/login/" class="btn btn-dark rounded-circle p-0 d-flex align-items-center justify-content-center shadow-sm border-glass" style="width: 44px; height: 44px; background: #0f172a; border: 1px solid #ffb800;" title="Account Login">
                            <i class="bi bi-person-fill fs-5" style="color: #ffb800;"></i>
                        </a>
                    {% endif %}
                </div>
            </div>
        </div>
    </header>"""

header_start = content.find('<header class="header-main-bar')
header_end = content.find('</header>') + 9

if header_start != -1 and header_end != -1:
    content = content[:header_start] + new_header + content[header_end:]
    with open('c:/Users/HANSLEM_KIMENG/Desktop/WEB/Armor/templates/base.html', 'w', encoding='utf-8') as f:
        f.write(content)
    print("Updated header successfully")
else:
    print("Could not find header")

