// ========================================
// 中古·回想 - 主要交互脚本
// ========================================

// ---- 移动端菜单切换 ----
function toggleMobileMenu() {
    const menu = document.getElementById('mobileMenu');
    menu.classList.toggle('active');
}

// ---- 搜索功能 ----
function search() {
    const keyword = document.getElementById('searchInput').value.trim();
    if (keyword) {
        window.location.href = '/?search=' + encodeURIComponent(keyword);
    }
}

// 回车搜索
document.addEventListener('DOMContentLoaded', function() {
    const searchInput = document.getElementById('searchInput');
    if (searchInput) {
        searchInput.addEventListener('keypress', function(e) {
            if (e.key === 'Enter') {
                search();
            }
        });
    }
});

// ---- 商品排序 ----
function sortProducts() {
    const sortType = document.getElementById('sortSelect').value;
    const urlParams = new URLSearchParams(window.location.search);
    urlParams.set('sort', sortType);
    window.location.href = '/?' + urlParams.toString();
}

// ---- 自定义下拉选择框 ----
document.addEventListener('DOMContentLoaded', function() {
    const customSelect = document.getElementById('customSortSelect');
    const selectTrigger = customSelect?.querySelector('.custom-select-trigger');
    const options = customSelect?.querySelectorAll('.custom-option');
    const selectText = customSelect?.querySelector('.select-text');
    const hiddenSelect = document.getElementById('sortSelect');

    if (!customSelect) return;

    // 初始化选中的文本
    const selectedOption = customSelect.querySelector('.custom-option.selected');
    if (selectedOption) {
        selectText.textContent = selectedOption.querySelector('span').textContent;
    }

    // 点击触发器打开/关闭下拉菜单
    selectTrigger.addEventListener('click', function(e) {
        e.stopPropagation();
        customSelect.classList.toggle('open');
    });

    // 点击选项
    options.forEach(function(option) {
        option.addEventListener('click', function() {
            const value = this.dataset.value;
            const text = this.querySelector('span').textContent;

            // 更新显示文本
            selectText.textContent = text;

            // 更新选中状态
            options.forEach(opt => opt.classList.remove('selected'));
            this.classList.add('selected');

            // 更新隐藏的select
            hiddenSelect.value = value;

            // 关闭下拉菜单
            customSelect.classList.remove('open');

            // 触发排序
            sortProducts();
        });
    });

    // 点击外部关闭下拉菜单
    document.addEventListener('click', function(e) {
        if (!customSelect.contains(e.target)) {
            customSelect.classList.remove('open');
        }
    });
});

// ---- 自动隐藏 Flash 消息 ----
document.addEventListener('DOMContentLoaded', function() {
    const alerts = document.querySelectorAll('.alert');
    alerts.forEach(function(alert) {
        setTimeout(function() {
            alert.style.transition = 'opacity 0.5s ease';
            alert.style.opacity = '0';
            setTimeout(function() {
                alert.remove();
            }, 500);
        }, 5000);
    });
});

// ---- 图片懒加载 ----
document.addEventListener('DOMContentLoaded', function() {
    const images = document.querySelectorAll('img[data-src]');
    
    const imageObserver = new IntersectionObserver((entries, observer) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const img = entry.target;
                img.src = img.dataset.src;
                img.removeAttribute('data-src');
                observer.unobserve(img);
            }
        });
    });
    
    images.forEach(img => imageObserver.observe(img));
});

// ---- 平滑滚动 ----
document.addEventListener('DOMContentLoaded', function() {
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function(e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });
});

// ---- 导航栏滚动效果 ----
let lastScrollTop = 0;
window.addEventListener('scroll', function() {
    const navbar = document.querySelector('.navbar');
    const scrollTop = window.pageYOffset || document.documentElement.scrollTop;
    
    if (scrollTop > 100) {
        navbar.style.boxShadow = '0 2px 20px rgba(0, 0, 0, 0.3)';
    } else {
        navbar.style.boxShadow = 'none';
    }
    
    lastScrollTop = scrollTop;
});

// ---- 表单输入动画 ----
document.addEventListener('DOMContentLoaded', function() {
    const formControls = document.querySelectorAll('.form-control');
    
    formControls.forEach(input => {
        input.addEventListener('focus', function() {
            this.parentElement.classList.add('focused');
        });
        
        input.addEventListener('blur', function() {
            this.parentElement.classList.remove('focused');
        });
    });
});

// ---- 数字动画（价格显示） ----
function animateNumber(element, target, duration = 1000) {
    const start = 0;
    const increment = target / (duration / 16);
    let current = start;
    
    const timer = setInterval(() => {
        current += increment;
        if (current >= target) {
            current = target;
            clearInterval(timer);
        }
        element.textContent = Math.floor(current).toLocaleString();
    }, 16);
}

// ---- 复制到剪贴板 ----
function copyToClipboard(text) {
    navigator.clipboard.writeText(text).then(() => {
        showToast('已复制到剪贴板');
    }).catch(err => {
        console.error('复制失败:', err);
    });
}

// ---- Toast 提示 ----
function showToast(message, type = 'info') {
    const toast = document.createElement('div');
    toast.className = `toast toast-${type}`;
    toast.textContent = message;
    toast.style.cssText = `
        position: fixed;
        top: 80px;
        left: 50%;
        transform: translateX(-50%);
        background-color: var(--bg-secondary);
        color: var(--text-primary);
        padding: 12px 24px;
        border-radius: 4px;
        border: 1px solid var(--border-color);
        font-family: var(--font-mono);
        font-size: 0.9rem;
        z-index: 10001;
        opacity: 0;
        transition: opacity 0.3s ease;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.4);
    `;
    
    document.body.appendChild(toast);
    
    requestAnimationFrame(() => {
        toast.style.opacity = '1';
    });
    
    setTimeout(() => {
        toast.style.opacity = '0';
        setTimeout(() => toast.remove(), 300);
    }, 3000);
}

// ---- 确认对话框 ----
function confirmAction(message, callback) {
    if (confirm(message)) {
        callback();
    }
}

// ---- 防抖函数 ----
function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}

// ---- 节流函数 ----
function throttle(func, limit) {
    let inThrottle;
    return function(...args) {
        if (!inThrottle) {
            func.apply(this, args);
            inThrottle = true;
            setTimeout(() => inThrottle = false, limit);
        }
    };
}

// ---- 页面加载动画 ----
document.addEventListener('DOMContentLoaded', function() {
    document.body.style.opacity = '0';
    document.body.style.transition = 'opacity 0.5s ease';
    
    requestAnimationFrame(() => {
        document.body.style.opacity = '1';
    });
});

// ---- 图片加载错误处理 ----
document.addEventListener('DOMContentLoaded', function() {
    document.querySelectorAll('img').forEach(img => {
        img.addEventListener('error', function() {
            this.style.display = 'none';
            const placeholder = document.createElement('div');
            placeholder.className = 'placeholder-image';
            placeholder.innerHTML = '<i class="fas fa-image"></i>';
            this.parentElement.appendChild(placeholder);
        });
    });
});

// ---- 外部点击关闭菜单 ----
document.addEventListener('click', function(e) {
    const mobileMenu = document.getElementById('mobileMenu');
    const menuBtn = document.querySelector('.mobile-menu-btn');
    
    if (mobileMenu && menuBtn && 
        !mobileMenu.contains(e.target) && 
        !menuBtn.contains(e.target)) {
        mobileMenu.classList.remove('active');
    }
});

// ---- 键盘快捷键 ----
document.addEventListener('keydown', function(e) {
    // ESC 关闭弹窗
    if (e.key === 'Escape') {
        const modals = document.querySelectorAll('.modal');
        modals.forEach(modal => {
            if (modal.style.display === 'flex') {
                modal.style.display = 'none';
            }
        });
    }
    
    // / 聚焦搜索框
    if (e.key === '/' && document.activeElement.tagName !== 'INPUT') {
        e.preventDefault();
        const searchInput = document.getElementById('searchInput');
        if (searchInput) {
            searchInput.focus();
        }
    }
});

// ---- 首页轮播功能 ----
let currentSlide = 0;
const slides = document.querySelectorAll('.hero-slide');
const dots = document.querySelectorAll('.hero-dots .dot');
const totalSlides = slides.length;
let slideInterval;

function goToSlide(index) {
    if (index < 0) index = totalSlides - 1;
    if (index >= totalSlides) index = 0;
    
    currentSlide = index;
    
    slides.forEach((slide, i) => {
        slide.classList.toggle('active', i === currentSlide);
    });
    
    dots.forEach((dot, i) => {
        dot.classList.toggle('active', i === currentSlide);
    });
    
    // 重置自动播放
    resetSlideInterval();
}

function changeSlide(direction) {
    goToSlide(currentSlide + direction);
}

function resetSlideInterval() {
    clearInterval(slideInterval);
    slideInterval = setInterval(() => {
        changeSlide(1);
    }, 5000);
}

// 初始化轮播
document.addEventListener('DOMContentLoaded', function() {
    if (slides.length > 0) {
        resetSlideInterval();
        
        // 鼠标悬停暂停
        const heroBanner = document.querySelector('.hero-banner');
        if (heroBanner) {
            heroBanner.addEventListener('mouseenter', () => clearInterval(slideInterval));
            heroBanner.addEventListener('mouseleave', resetSlideInterval);
        }
    }
});

// ---- 分类标签滑动指示器 ----
function initCategoryIndicator() {
    const nav = document.getElementById('categoryNav');
    const indicator = document.getElementById('categoryIndicator');
    const activeTab = nav?.querySelector('.category-tab.active');
    
    if (nav && indicator && activeTab) {
        updateCategoryIndicator(activeTab);
    }
}

function updateCategoryIndicator(activeTab) {
    const indicator = document.getElementById('categoryIndicator');
    const nav = document.getElementById('categoryNav');
    
    if (!indicator || !nav || !activeTab) return;
    
    const navRect = nav.getBoundingClientRect();
    const tabRect = activeTab.getBoundingClientRect();
    
    const left = tabRect.left - navRect.left;
    const width = tabRect.width;
    
    indicator.style.left = left + 'px';
    indicator.style.width = width + 'px';
}

// 初始化指示器位置
document.addEventListener('DOMContentLoaded', function() {
    // 延迟初始化，确保布局完成
    setTimeout(initCategoryIndicator, 100);
});

// 窗口大小变化时更新指示器位置
window.addEventListener('resize', debounce(function() {
    const activeTab = document.querySelector('.category-tab.active');
    if (activeTab) {
        updateCategoryIndicator(activeTab);
    }
}, 100));

// ---- 分类筛选（无刷新） ----
function filterCategory(category) {
    // 更新标签选中状态
    const tabs = document.querySelectorAll('.category-tab');
    let activeTab = null;
    tabs.forEach(tab => {
        const isActive = tab.dataset.category === category;
        tab.classList.toggle('active', isActive);
        if (isActive) activeTab = tab;
    });
    
    // 更新滑动指示器位置
    if (activeTab) {
        updateCategoryIndicator(activeTab);
    }
    
    // 获取当前排序方式
    const sortSelect = document.getElementById('sortSelect');
    const sort = sortSelect ? sortSelect.value : 'newest';
    
    // 构建请求URL
    let url = '/api/items';
    const params = [];
    if (category !== 'all') {
        params.push('category=' + category);
    }
    if (sort !== 'newest') {
        params.push('sort=' + sort);
    }
    if (params.length > 0) {
        url += '?' + params.join('&');
    }
    
    // 显示加载状态
    const grid = document.getElementById('productsGrid');
    if (grid) {
        grid.style.opacity = '0.5';
    }
    
    // AJAX请求
    fetch(url)
        .then(response => response.json())
        .then(data => {
            renderProducts(data.items, category);
            updateTitle(category);
            // 更新浏览器URL（不刷新）
            const newUrl = category === 'all' ? '/' : '/?category=' + category;
            history.pushState({category: category}, '', newUrl);
        })
        .catch(error => {
            console.error('加载失败:', error);
            showToast('加载失败，请重试', 'error');
        })
        .finally(() => {
            if (grid) {
                grid.style.opacity = '1';
            }
        });
}

// 渲染商品列表
function renderProducts(items, currentCategory) {
    const grid = document.getElementById('productsGrid');
    if (!grid) return;
    
    if (items.length === 0) {
        grid.innerHTML = `
            <div class="empty-state">
                <i class="fas fa-box-open"></i>
                <p>暂无商品，快来发布第一个吧！</p>
                <a href="/publish" class="btn btn-primary">发布商品</a>
            </div>
        `;
        return;
    }
    
    const categoryNames = {
        'electronics': '数码电子',
        'books': '图书教材',
        'clothes': '服装鞋帽',
        'furniture': '家具家居',
        'sports': '运动户外',
        'others': '其他'
    };
    
    grid.innerHTML = items.map(item => `
        <div class="product-card" data-category="${item.category}">
            <a href="/item/${item.id}">
                <div class="product-image">
                    ${item.image 
                        ? `<img src="/static/images/${item.image}" alt="${item.title}">`
                        : `<div class="placeholder-image"><i class="fas fa-image"></i></div>`
                    }
                </div>
                <div class="product-info">
                    <h3 class="product-title">${item.title}</h3>
                    <p class="product-description">${item.description.substring(0, 50)}...</p>
                    <div class="product-footer">
                        <span class="product-price">¥${item.price}</span>
                        <span class="product-time">${item.created_at}</span>
                    </div>
                    <div class="product-seller">
                        <span>${item.seller_name}</span>
                    </div>
                </div>
            </a>
        </div>
    `).join('');
}

// 更新标题
function updateTitle(category) {
    const titles = {
        'all': '全部商品',
        'electronics': '数码电子',
        'books': '图书教材',
        'clothes': '服装鞋帽',
        'furniture': '家具家居',
        'sports': '运动户外',
        'others': '其他臻品'
    };
    
    const titleEl = document.querySelector('.section-title');
    if (titleEl) {
        titleEl.textContent = titles[category] || '全部商品';
    }
}

// 浏览器前进后退处理
window.addEventListener('popstate', function(e) {
    const category = e.state?.category || 'all';
    
    // 更新标签状态但不触发AJAX（因为已经在历史中）
    const tabs = document.querySelectorAll('.category-tab');
    let activeTab = null;
    tabs.forEach(tab => {
        const isActive = tab.dataset.category === category;
        tab.classList.toggle('active', isActive);
        if (isActive) activeTab = tab;
    });
    
    // 更新滑动指示器位置
    if (activeTab) {
        updateCategoryIndicator(activeTab);
    }
    
    // 重新加载商品
    const sortSelect = document.getElementById('sortSelect');
    const sort = sortSelect ? sortSelect.value : 'newest';
    
    let url = '/api/items';
    const params = [];
    if (category !== 'all') {
        params.push('category=' + category);
    }
    if (sort !== 'newest') {
        params.push('sort=' + sort);
    }
    if (params.length > 0) {
        url += '?' + params.join('&');
    }
    
    fetch(url)
        .then(response => response.json())
        .then(data => {
            renderProducts(data.items, category);
            updateTitle(category);
        })
        .catch(error => {
            console.error('加载失败:', error);
        });
});

// ---- 性能优化：减少重绘 ----
const optimizedScrollHandler = throttle(() => {
    // 滚动相关的处理逻辑
}, 16);

window.addEventListener('scroll', optimizedScrollHandler);

// ---- 导出全局函数 ----
window.SecondHandMarket = {
    search,
    sortProducts,
    toggleMobileMenu,
    showToast,
    copyToClipboard,
    confirmAction,
    debounce,
    throttle,
    animateNumber,
    goToSlide,
    changeSlide,
    filterCategory,
    renderProducts,
    updateCategoryIndicator
};
