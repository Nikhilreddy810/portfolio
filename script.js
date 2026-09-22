// Nikhil Reddy Levaku — Interactive Portfolio Script

document.addEventListener('DOMContentLoaded', () => {
  // 1. Interactive Cursor Glow Spotlight
  const cursorGlow = document.getElementById('cursorGlow');
  if (cursorGlow) {
    let mouseX = window.innerWidth / 2;
    let mouseY = window.innerHeight / 2;
    let currentX = mouseX;
    let currentY = mouseY;

    window.addEventListener('mousemove', (e) => {
      mouseX = e.clientX;
      mouseY = e.clientY;
    });

    function animateSpotlight() {
      currentX += (mouseX - currentX) * 0.12;
      currentY += (mouseY - currentY) * 0.12;
      cursorGlow.style.left = currentX + 'px';
      cursorGlow.style.top = currentY + 'px';
      requestAnimationFrame(animateSpotlight);
    }
    animateSpotlight();
  }

  // 2. Interactive 3D Card Tilt & Movement on Cursor
  const tiltCards = document.querySelectorAll('.interactive-tilt');
  tiltCards.forEach(card => {
    card.addEventListener('mousemove', (e) => {
      const rect = card.getBoundingClientRect();
      const x = e.clientX - rect.left;
      const y = e.clientY - rect.top;
      
      const centerX = rect.width / 2;
      const centerY = rect.height / 2;

      const rotateX = ((y - centerY) / centerY) * -4.5;
      const rotateY = ((x - centerX) / centerX) * 4.5;

      card.style.transform = `perspective(1000px) rotateX(${rotateX.toFixed(2)}deg) rotateY(${rotateY.toFixed(2)}deg) translateY(-3px)`;
    });

    card.addEventListener('mouseleave', () => {
      card.style.transform = 'perspective(1000px) rotateX(0deg) rotateY(0deg) translateY(0px)';
    });
  });

  // 2b. Interactive 3D Cutout Silhouette Parallax Tilt (Matching Sketch)
  const hero3dStage = document.getElementById('hero3dStage');
  const silhouetteFigure = document.getElementById('silhouetteFigure');
  if (hero3dStage && silhouetteFigure) {
    hero3dStage.addEventListener('mousemove', (e) => {
      const rect = hero3dStage.getBoundingClientRect();
      const x = e.clientX - rect.left;
      const y = e.clientY - rect.top;
      
      const centerX = rect.width / 2;
      const centerY = rect.height / 2;

      // Realistic 3D rotational tilt & slight dynamic translation
      const rotateX = ((y - centerY) / centerY) * -9; // -9deg to +9deg
      const rotateY = ((x - centerX) / centerX) * 11; // -11deg to +11deg
      const moveX = ((x - centerX) / centerX) * 8;

      silhouetteFigure.style.transform = `perspective(1000px) rotateX(${rotateX.toFixed(2)}deg) rotateY(${rotateY.toFixed(2)}deg) translateX(${moveX.toFixed(1)}px)`;
    });

    hero3dStage.addEventListener('mouseleave', () => {
      silhouetteFigure.style.transform = 'perspective(1000px) rotateX(0deg) rotateY(0deg) translateX(0px)';
    });
  }

  // 3. Mobile Nav Toggle
  const menuBtn = document.getElementById('mobileMenuBtn');
  const sidebar = document.querySelector('.sidebar');
  if (menuBtn && sidebar) {
    menuBtn.addEventListener('click', () => {
      sidebar.classList.toggle('open');
      menuBtn.textContent = sidebar.classList.contains('open') ? '[close]' : '[menu]';
    });

    document.querySelectorAll('.nav-link').forEach(link => {
      link.addEventListener('click', () => {
        if (window.innerWidth <= 768) {
          sidebar.classList.remove('open');
          menuBtn.textContent = '[menu]';
        }
      });
    });
  }

  // 4. Active Nav Spy on Scroll
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

  // 5. Copy to Clipboard
  window.copyText = function(text, btnElement) {
    navigator.clipboard.writeText(text).then(() => {
      const origText = btnElement.innerText;
      btnElement.innerText = 'copied!';
      btnElement.style.color = '#38BDF8';
      setTimeout(() => {
        btnElement.innerText = origText;
        btnElement.style.color = '';
      }, 2000);
    }).catch(err => {
      console.error('Failed to copy: ', err);
    });
  };

  // 6. Interactive Architecture Pipeline Sequencer
  function triggerPipelineAnimation() {
    const nodes = [
      { node: 'node-client', link: 'flow-link-1', badge: 'badge-client' },
      { node: 'node-gateway', link: 'flow-link-2', badge: 'badge-gateway' },
      { node: 'node-service', link: 'flow-link-3', badge: 'badge-service' },
      { node: 'node-redis', link: 'flow-link-4', badge: 'badge-redis' },
      { node: 'node-postgres', link: null, badge: 'badge-postgres' }
    ];

    // Reset previous pulses
    nodes.forEach(item => {
      const el = document.getElementById(item.node);
      const b = document.getElementById(item.badge);
      if (el) el.classList.remove('active-pulse');
      if (b) b.classList.remove('active-badge');
      if (item.link) {
        const l = document.getElementById(item.link);
        if (l) l.classList.remove('active-pulse');
      }
    });

    // Step through each layer sequentially
    nodes.forEach((item, index) => {
      setTimeout(() => {
        const el = document.getElementById(item.node);
        const b = document.getElementById(item.badge);
        if (el) el.classList.add('active-pulse');
        if (b) b.classList.add('active-badge');
        if (item.link) {
          const l = document.getElementById(item.link);
          if (l) l.classList.add('active-pulse');
        }
      }, index * 200);
    });
  }

  // 7. Interactive Mock API Sandbox
  const mockEndpoints = {
    "GET /api/v1/health": {
      status: 200,
      latency: "12ms",
      response: {
        status: "UP",
        service: "nikhil-backend-core",
        runtime: "Java 21 / Spring Boot 3.2",
        database: "PostgreSQL [HikariCP pool 10/10 active]",
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
    "GET /api/v1/offers/received": {
      status: 200,
      latency: "15ms",
      response: {
        candidate: "Nikhil Reddy Levaku",
        verifiedOffers: [
          {
            company: "Axlero Innovative Solutions",
            role: "Java Developer Intern",
            tenure: "25 Sep 2026 - 25 Dec 2026",
            empId: "AXL-JV-KSUL6U",
            mode: "Remote",
            scope: "Spring REST APIs & Database performance"
          },
          {
            company: "Infotact Solutions",
            role: "Associate L1 (Java Development)",
            tenure: "05 Sep 2026 - 05 Dec 2026",
            empId: "8c62241c4127",
            mode: "Remote",
            scope: "Core Java, JDBC, Spring Boot, MySQL/PostgreSQL"
          }
        ]
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

    triggerPipelineAnimation();

    apiOutput.textContent = "// Executing REST request...\n// [Layer 1] Spring Security Gateway -> JWT Authenticated\n// [Layer 2] Querying Redis cache -> HIT\n// [Layer 3] HikariCP PostgreSQL Transaction -> Committed";
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
    }, 450);
  }

  if (runApiBtn) {
    runApiBtn.addEventListener('click', executeMockApi);
  }
  if (endpointSelect) {
    endpointSelect.addEventListener('change', executeMockApi);
  }

  // 8. In-Browser Universal Document Modal (Resume, Axlero Offer, Infotact Offer)
  const resumeModal = document.getElementById('resumeModal');
  const modalDocTitle = document.getElementById('modalDocTitle');
  const modalDocTag = document.getElementById('modalDocTag');
  const modalPdfFrame = document.getElementById('modalPdfFrame');
  const modalDownloadBtn = document.getElementById('modalDownloadBtn');
  const closeModalBtn = document.getElementById('closeResumeModalBtn');
  const modalBackdrop = document.getElementById('resumeModalBackdrop');

  const openModalBtn = document.getElementById('openResumeModalBtn');
  const heroModalBtn = document.getElementById('heroPreviewResumeBtn');
  const heroPreviewResumePill = document.getElementById('heroPreviewResumePill');
  const heroPreviewAxleroPill = document.getElementById('heroPreviewAxleroPill');
  const heroPreviewInfotactPill = document.getElementById('heroPreviewInfotactPill');
  const viewAxleroOfferBtn = document.getElementById('viewAxleroOfferBtn');
  const viewInfotactOfferBtn = document.getElementById('viewInfotactOfferBtn');

  function openDocument(pdfUrl, title, tag, downloadFilename) {
    if (modalPdfFrame) modalPdfFrame.src = pdfUrl;
    if (modalDocTitle) modalDocTitle.textContent = title;
    if (modalDocTag) modalDocTag.textContent = tag;
    if (modalDownloadBtn) {
      modalDownloadBtn.href = pdfUrl;
      modalDownloadBtn.download = downloadFilename || title;
    }
    if (resumeModal) {
      resumeModal.classList.add('active');
      document.body.style.overflow = 'hidden';
    }
  }

  function closeDocument() {
    if (resumeModal) {
      resumeModal.classList.remove('active');
      document.body.style.overflow = '';
      if (modalPdfFrame) modalPdfFrame.src = '';
    }
  }

  // Resume Triggers
  if (openModalBtn) openModalBtn.addEventListener('click', () => {
    openDocument('resume.pdf', 'Nikhil_Reddy_Levaku_Resume.pdf', '// RESUME PREVIEW', 'Nikhil_Reddy_Levaku_Resume.pdf');
  });
  if (heroModalBtn) heroModalBtn.addEventListener('click', () => {
    openDocument('resume.pdf', 'Nikhil_Reddy_Levaku_Resume.pdf', '// RESUME PREVIEW', 'Nikhil_Reddy_Levaku_Resume.pdf');
  });
  if (heroPreviewResumePill) heroPreviewResumePill.addEventListener('click', () => {
    openDocument('resume.pdf', 'Nikhil_Reddy_Levaku_Resume.pdf', '// RESUME PREVIEW', 'Nikhil_Reddy_Levaku_Resume.pdf');
  });

  // Axlero Offer Letter Triggers
  if (heroPreviewAxleroPill) heroPreviewAxleroPill.addEventListener('click', () => {
    openDocument('axlero_offer.pdf', 'Axlero_Offer_Letter_Nikhil_Reddy.pdf', '// VERIFIED SELECTION: AXLERO', 'Axlero_Offer_Letter_Nikhil_Reddy.pdf');
  });
  if (viewAxleroOfferBtn) viewAxleroOfferBtn.addEventListener('click', () => {
    openDocument('axlero_offer.pdf', 'Axlero_Offer_Letter_Nikhil_Reddy.pdf', '// VERIFIED SELECTION: AXLERO', 'Axlero_Offer_Letter_Nikhil_Reddy.pdf');
  });

  // Infotact Offer Letter Triggers
  if (heroPreviewInfotactPill) heroPreviewInfotactPill.addEventListener('click', () => {
    openDocument('infotact_offer.pdf', 'Infotact_Offer_Letter_Nikhil_Reddy.pdf', '// VERIFIED SELECTION: INFOTACT', 'Infotact_Offer_Letter_Nikhil_Reddy.pdf');
  });
  if (viewInfotactOfferBtn) viewInfotactOfferBtn.addEventListener('click', () => {
    openDocument('infotact_offer.pdf', 'Infotact_Offer_Letter_Nikhil_Reddy.pdf', '// VERIFIED SELECTION: INFOTACT', 'Infotact_Offer_Letter_Nikhil_Reddy.pdf');
  });

  if (closeModalBtn) closeModalBtn.addEventListener('click', closeDocument);
  if (modalBackdrop) modalBackdrop.addEventListener('click', closeDocument);
  window.addEventListener('keydown', (e) => {
    if (e.key === 'Escape') closeDocument();
  });

  // 10. Project Category Filter
  const filterPills = document.querySelectorAll('.filter-pill');
  const projectPanels = document.querySelectorAll('.project-panel');

  if (filterPills.length > 0 && projectPanels.length > 0) {
    filterPills.forEach(pill => {
      pill.addEventListener('click', () => {
        const filter = pill.getAttribute('data-filter');
        filterPills.forEach(p => p.classList.remove('active'));
        pill.classList.add('active');

        projectPanels.forEach(panel => {
          const categories = panel.getAttribute('data-category') || '';
          if (filter === 'all' || categories.split(' ').includes(filter)) {
            panel.classList.remove('hidden-filter');
            panel.style.opacity = '0';
            panel.style.transform = 'translateY(8px)';
            setTimeout(() => {
              panel.style.opacity = '1';
              panel.style.transform = 'translateY(0)';
            }, 30);
          } else {
            panel.classList.add('hidden-filter');
          }
        });
      });
    });
  }

  // 11. Visual Architecture Topology Drawer Toggle
  const toggleArchBtn = document.getElementById('toggleArchTopologyBtn');
  const flightArchDrawer = document.getElementById('flightArchDrawer');
  const topologyBtnText = document.getElementById('topologyBtnText');

  if (toggleArchBtn && flightArchDrawer) {
    toggleArchBtn.addEventListener('click', () => {
      const isOpen = flightArchDrawer.classList.toggle('open');
      if (topologyBtnText) {
        topologyBtnText.textContent = isOpen 
          ? 'Hide Architecture Topology Flow ▴' 
          : 'Explore Visual Architecture Topology Flow ▾';
      }
    });
  }

  // 12. Animated Numbers Counter on Scroll
  const counterElements = document.querySelectorAll('.metric-val[data-target], .edu-cgpa[data-target]');
  if ('IntersectionObserver' in window && counterElements.length > 0) {
    const counterObserver = new IntersectionObserver((entries, observer) => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          const el = entry.target;
          observer.unobserve(el);

          const target = parseFloat(el.getAttribute('data-target'));
          const suffix = el.getAttribute('data-suffix') || '';
          const isDecimal = el.getAttribute('data-decimal') === 'true';
          const duration = 1400; // ms
          const startTime = performance.now();

          function updateCounter(currentTime) {
            const elapsed = currentTime - startTime;
            const progress = Math.min(elapsed / duration, 1);
            // Ease out cubic
            const easeProgress = 1 - Math.pow(1 - progress, 3);
            const currentVal = target * easeProgress;

            if (isDecimal) {
              el.textContent = currentVal.toFixed(1) + suffix;
            } else {
              el.textContent = Math.floor(currentVal) + suffix;
            }

            if (progress < 1) {
              requestAnimationFrame(updateCounter);
            } else {
              el.textContent = (isDecimal ? target.toFixed(1) : target) + suffix;
            }
          }

          requestAnimationFrame(updateCounter);
        }
      });
    }, { threshold: 0.3 });

    counterElements.forEach(el => counterObserver.observe(el));
  }
});
