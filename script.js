// Nikhil Reddy Levaku — Modern Engineering Portfolio Script

document.addEventListener('DOMContentLoaded', () => {

  // 1. Mobile Menu Drawer Toggle
  const mobileToggle = document.getElementById('mobileToggle');
  const mobileDrawer = document.getElementById('mobileDrawer');
  
  if (mobileToggle && mobileDrawer) {
    mobileToggle.addEventListener('click', () => {
      mobileDrawer.classList.toggle('open');
    });

    document.querySelectorAll('.mobile-nav-item').forEach(link => {
      link.addEventListener('click', () => {
        mobileDrawer.classList.remove('open');
      });
    });
  }

  // 2. Active Nav Link Spy on Scroll
  const sections = document.querySelectorAll('section[id]');
  const desktopNavLinks = document.querySelectorAll('.nav-anchor');

  function updateActiveNavLink() {
    const scrollPos = window.pageYOffset + 140;
    sections.forEach(sec => {
      const top = sec.offsetTop;
      const height = sec.offsetHeight;
      const id = sec.getAttribute('id');

      if (scrollPos >= top && scrollPos < top + height) {
        desktopNavLinks.forEach(link => {
          link.classList.remove('active');
          if (link.getAttribute('href') === `#${id}`) {
            link.classList.add('active');
          }
        });
      }
    });
  }
  window.addEventListener('scroll', updateActiveNavLink);

  // 3. Project Category Filter
  const filterBtns = document.querySelectorAll('.filter-btn');
  const projectItems = document.querySelectorAll('.project-item');

  if (filterBtns.length > 0 && projectItems.length > 0) {
    filterBtns.forEach(btn => {
      btn.addEventListener('click', () => {
        const filter = btn.getAttribute('data-filter');
        filterBtns.forEach(b => b.classList.remove('active'));
        btn.classList.add('active');

        projectItems.forEach(item => {
          const categories = item.getAttribute('data-category') || '';
          if (filter === 'all' || categories.split(' ').includes(filter)) {
            item.classList.remove('hidden-filter');
            item.style.opacity = '0';
            item.style.transform = 'translateY(6px)';
            setTimeout(() => {
              item.style.opacity = '1';
              item.style.transform = 'translateY(0)';
            }, 30);
          } else {
            item.classList.add('hidden-filter');
          }
        });
      });
    });
  }

  // 4. Case Study Code Snippet Toggle
  const toggleCodeBtn = document.getElementById('toggleCodeSnippetBtn');
  const codeBody = document.getElementById('codeSnippetBody');
  const codeIndicator = document.getElementById('codeIndicator');

  if (toggleCodeBtn && codeBody) {
    toggleCodeBtn.addEventListener('click', () => {
      const isOpen = codeBody.classList.toggle('open');
      if (codeIndicator) {
        codeIndicator.textContent = isOpen 
          ? 'Hide Implementation Snippet ▴' 
          : 'Show Implementation Snippet ▾';
      }
    });
  }

  // 5. Restrained Interactive Tilt on Hero Portrait Stage
  const portraitStage = document.getElementById('portraitStage');
  const portraitFrame = document.getElementById('portraitFrame');

  if (portraitStage && portraitFrame) {
    portraitStage.addEventListener('mousemove', (e) => {
      const rect = portraitStage.getBoundingClientRect();
      const x = e.clientX - rect.left;
      const y = e.clientY - rect.top;
      const centerX = rect.width / 2;
      const centerY = rect.height / 2;

      const rotateX = ((y - centerY) / centerY) * -5.5;
      const rotateY = ((x - centerX) / centerX) * 6.5;

      portraitFrame.style.transform = `perspective(800px) rotateX(${rotateX.toFixed(2)}deg) rotateY(${rotateY.toFixed(2)}deg)`;
    });

    portraitStage.addEventListener('mouseleave', () => {
      portraitFrame.style.transform = 'perspective(800px) rotateX(0deg) rotateY(0deg)';
    });
  }

  // 6. Universal Document Modal (Resume & Verified Offers)
  const docModal = document.getElementById('docModal');
  const modalBackdrop = document.getElementById('docModalBackdrop');
  const modalDocTitle = document.getElementById('modalDocTitle');
  const modalDocTag = document.getElementById('modalDocTag');
  const modalDownloadBtn = document.getElementById('modalDownloadBtn');
  const modalPdfFrame = document.getElementById('modalPdfFrame');
  const closeDocModalBtn = document.getElementById('closeDocModalBtn');

  function openModalDocument(pdfUrl, title, tag, downloadFilename) {
    if (modalPdfFrame) modalPdfFrame.src = pdfUrl;
    if (modalDocTitle) modalDocTitle.textContent = title;
    if (modalDocTag) modalDocTag.textContent = tag;
    if (modalDownloadBtn) {
      modalDownloadBtn.href = pdfUrl;
      modalDownloadBtn.download = downloadFilename || title;
    }
    if (docModal) {
      docModal.classList.add('active');
      document.body.style.overflow = 'hidden';
    }
  }

  function closeModalDocument() {
    if (docModal) {
      docModal.classList.remove('active');
      document.body.style.overflow = '';
      if (modalPdfFrame) modalPdfFrame.src = '';
    }
  }

  // Resume preview triggers
  const heroPreviewResumeBtn = document.getElementById('heroPreviewResumeBtn');
  if (heroPreviewResumeBtn) {
    heroPreviewResumeBtn.addEventListener('click', () => {
      openModalDocument('resume.pdf', 'Nikhil_Reddy_Levaku_Resume.pdf', '// VERIFIED RESUME', 'Nikhil_Reddy_Levaku_Resume.pdf');
    });
  }

  const contactPreviewResumeBtn = document.getElementById('contactPreviewResumeBtn');
  if (contactPreviewResumeBtn) {
    contactPreviewResumeBtn.addEventListener('click', () => {
      openModalDocument('resume.pdf', 'Nikhil_Reddy_Levaku_Resume.pdf', '// VERIFIED RESUME', 'Nikhil_Reddy_Levaku_Resume.pdf');
    });
  }

  // Offer letter triggers
  const viewAxleroBtn = document.getElementById('viewAxleroOfferBtn');
  if (viewAxleroBtn) {
    viewAxleroBtn.addEventListener('click', () => {
      openModalDocument('axlero_offer.pdf', 'Axlero_Offer_Letter_Nikhil_Reddy.pdf', '// VERIFIED SELECTION: AXLERO', 'Axlero_Offer_Letter_Nikhil_Reddy.pdf');
    });
  }

  const viewInfotactBtn = document.getElementById('viewInfotactOfferBtn');
  if (viewInfotactBtn) {
    viewInfotactBtn.addEventListener('click', () => {
      openModalDocument('infotact_offer.pdf', 'Infotact_Offer_Letter_Nikhil_Reddy.pdf', '// VERIFIED SELECTION: INFOTACT', 'Infotact_Offer_Letter_Nikhil_Reddy.pdf');
    });
  }

  const viewGfcOfferBtn = document.getElementById('viewGfcOfferBtn');
  if (viewGfcOfferBtn) {
    viewGfcOfferBtn.addEventListener('click', () => {
      openModalDocument('gfc_offer.pdf', 'GFC_Offer_Letter_Nikhil_Reddy.pdf', '// VERIFIED OFFER: GLOBAL FUTURE CAREER', 'GFC_Offer_Letter_Nikhil_Reddy.pdf');
    });
  }

  if (closeDocModalBtn) closeDocModalBtn.addEventListener('click', closeModalDocument);
  if (modalBackdrop) modalBackdrop.addEventListener('click', closeModalDocument);
  window.addEventListener('keydown', (e) => {
    if (e.key === 'Escape') closeModalDocument();
  });

  // 7. Animated Metric Numbers on Scroll
  const counterElements = document.querySelectorAll('.metric-number[data-target], .edu-grade[data-target]');
  if ('IntersectionObserver' in window && counterElements.length > 0) {
    const counterObserver = new IntersectionObserver((entries, observer) => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          const el = entry.target;
          observer.unobserve(el);

          const target = parseFloat(el.getAttribute('data-target'));
          const suffix = el.getAttribute('data-suffix') || '';
          const isDecimal = el.getAttribute('data-decimal') === 'true';
          const duration = 1200;
          const startTime = performance.now();

          function updateCounter(currentTime) {
            const elapsed = currentTime - startTime;
            const progress = Math.min(elapsed / duration, 1);
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
    }, { threshold: 0.35 });

    counterElements.forEach(el => counterObserver.observe(el));
  }
});
