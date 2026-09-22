// Nikhil Reddy Levaku — Interactive Portfolio Script

document.addEventListener('DOMContentLoaded', () => {
  // Mobile Nav Toggle
  const menuBtn = document.getElementById('mobileMenuBtn');
  const sidebar = document.querySelector('.sidebar');
  if (menuBtn && sidebar) {
    menuBtn.addEventListener('click', () => {
      sidebar.classList.toggle('open');
      menuBtn.textContent = sidebar.classList.contains('open') ? '[close]' : '[menu]';
    });

    // Close when clicking any nav link
    document.querySelectorAll('.nav-link').forEach(link => {
      link.addEventListener('click', () => {
        if (window.innerWidth <= 768) {
          sidebar.classList.remove('open');
          menuBtn.textContent = '[menu]';
        }
      });
    });
  }

  // Active Nav Link Spy on Scroll
  const sections = document.querySelectorAll('section[id]');
  const navLinks = document.querySelectorAll('.nav-link');

  function highlightNavOnScroll() {
    const scrollY = window.pageYOffset;
    sections.forEach(current => {
      const sectionHeight = current.offsetHeight;
      const sectionTop = current.offsetTop - 120;
      const sectionId = current.getAttribute('id');

      if (scrollY > sectionTop && scrollY <= sectionTop + sectionHeight) {
        navLinks.forEach(link => {
          link.classList.remove('active');
          if (link.getAttribute('href') === '#' + sectionId) {
            link.classList.add('active');
          }
        });
      }
    });
  }
  window.addEventListener('scroll', highlightNavOnScroll);

  // Copy to clipboard helper
  window.copyText = function(text, btnElement) {
    navigator.clipboard.writeText(text).then(() => {
      const originalText = btnElement.innerText;
      btnElement.innerText = 'copied!';
      btnElement.style.color = '#38BDF8';
      setTimeout(() => {
        btnElement.innerText = originalText;
        btnElement.style.color = '';
      }, 2000);
    }).catch(err => {
      console.error('Failed to copy: ', err);
    });
  };

  // Interactive Mock API Sandbox
  const mockEndpoints = {
    "GET /api/v1/health": {
      status: 200,
      latency: "12ms",
      response: {
        status: "UP",
        service: "nikhil-backend-core",
        runtime: "Java 21 / Spring Boot 3.2",
        database: "PostgreSQL [Pool: HikariCP 10/10 active]",
        cache: "Redis [HIT_RATE: 94.2%]",
        uptime: "99.98%"
      }
    },
    "POST /api/v1/orders/reserve": {
      status: 201,
      latency: "28ms",
      response: {
        orderId: "ORD_78923019",
        status: "RESERVED",
        idempotencyKey: "idem_4f89d3742b",
        pessimisticLockAcquired: true,
        concurrencyStatus: "TRANSACTION_SERIALIZED",
        redisCacheUpdated: true,
        message: "Seat inventory locked safely without overbooking."
      }
    },
    "GET /api/v1/metrics/db-load": {
      status: 200,
      latency: "18ms",
      response: {
        metric: "DATABASE_LOAD_OPTIMIZATION",
        baselineQueriesPerSec: "14,200 QPS",
        currentQueriesPerSec: "8,520 QPS",
        loadReduction: "~40% via Redis Caching",
        cachingTier: "Redis Cluster + Flyway Normalized Schemas",
        testedWith: "JUnit 5 + Mockito load simulation"
      }
    },
    "GET /api/v1/developer/profile": {
      status: 200,
      latency: "10ms",
      response: {
        candidate: "Nikhil Reddy Levaku",
        primaryRole: "Java Backend Developer",
        stack: ["Core Java", "Spring Boot", "Spring Security", "PostgreSQL", "Redis", "Docker"],
        productionMetrics: {
          restApisShipped: "100+",
          dsaProblemsSolved: "100+ (LeetCode)",
          cgpa: "8.5 / 10",
          hackathon: "RTIH Design Spark Challenge 2026 (48-hr LMS Backend)"
        }
      }
    }
  };

  const endpointSelect = document.getElementById('endpointSelect');
  const runApiBtn = document.getElementById('runApiBtn');
  const apiOutput = document.getElementById('apiOutput');
  const apiStatusCode = document.getElementById('apiStatusCode');
  const apiLatency = document.getElementById('apiLatency');

  function executeMockApi() {
    if (!endpointSelect || !apiOutput) return;
    const selectedKey = endpointSelect.value;
    const data = mockEndpoints[selectedKey];

    apiOutput.textContent = "// Executing REST request...\n// Querying HikariCP pool & Redis cache...";
    if (runApiBtn) runApiBtn.disabled = true;

    setTimeout(() => {
      if (apiStatusCode) {
        apiStatusCode.textContent = "HTTP " + data.status + " OK";
        apiStatusCode.style.color = '#34D399';
      }
      if (apiLatency) {
        apiLatency.textContent = data.latency;
      }
      apiOutput.textContent = JSON.stringify(data.response, null, 2);
      if (runApiBtn) runApiBtn.disabled = false;
    }, 280);
  }

  if (runApiBtn) {
    runApiBtn.addEventListener('click', executeMockApi);
  }
  if (endpointSelect) {
    endpointSelect.addEventListener('change', executeMockApi);
  }
});
