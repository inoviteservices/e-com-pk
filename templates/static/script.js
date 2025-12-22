const placeholder = 'https://dummyimage.com/640x640/f2f4ff/3764ff&text=imfresh';

const combos = [
  {
    name: 'imfresh Men Cream (Dopenight + Original) Combo',
    price: 799,
    strike: 1198,
    rating: 276,
    tag: 'Combo',
    image: 'https://imfreshmen.com/_next/image?url=https%3A%2F%2Fstorage.googleapis.com%2Fgoodfeel_images%2Fproduct_image%2Fdopenight_original_imfresh_new_first_image_for_website_27_11_2025.webp&w=1920&q=75',
  },
  {
    name: 'imfresh Men Cream (Dopenight + Sweet Killer) Combo',
    price: 799,
    strike: 1198,
    rating: 476,
    tag: 'Combo',
    image: 'https://imfreshmen.com/_next/image?url=https%3A%2F%2Fstorage.googleapis.com%2Fgoodfeel_images%2Fproduct_image%2Fdopenight_sweet_killer_imfresh_new_first_image_for_website_27_11_2025.webp&w=1920&q=75',
  },
  {
    name: 'imfresh Men Cream (Original + Sweet Killer) Combo',
    price: 799,
    strike: 1198,
    rating: 5769,
    tag: 'Combo',
    image: 'https://imfreshmen.com/_next/image?url=https%3A%2F%2Fstorage.googleapis.com%2Fgoodfeel_images%2Fproduct_image%2Fsweet_killer_original_imfresh_new_first_image_for_website_27_11_2025.webp&w=1920&q=75',
  },
  {
    name: 'imfresh Men Cream (Original + Dopenight + Sweet Killer)',
    price: 999,
    strike: 1797,
    rating: 376,
    tag: 'Combo',
    image: 'https://imfreshmen.com/_next/image?url=https%3A%2F%2Fstorage.googleapis.com%2Fgoodfeel_images%2Fproduct_image%2Fdopenight_pk_of_2_imfresh_new_first_image_for_website_27_11_2025.webp&w=1920&q=75',
  },
];

const singles = [
  {
    name: 'imfresh Men Cream (Original) | Whole body deodorant',
    price: 549,
    strike: 599,
    rating: 5769,
    tag: 'Bestseller',
    image: 'https://imfreshmen.com/_next/image?url=https%3A%2F%2Fstorage.googleapis.com%2Fgoodfeel_images%2Fproduct_image%2Foriginal_imfresh_new_first_image_for_website_27_11_2025.webp&w=1920&q=75',
  },
  {
    name: 'imfresh Men Cream (Dopenight) | Whole body deodorant',
    price: 549,
    strike: 599,
    rating: 345,
    tag: 'New',
    image: 'https://imfreshmen.com/_next/image?url=https%3A%2F%2Fstorage.googleapis.com%2Fgoodfeel_images%2Fproduct_image%2Fdopenight_imfresh_new_first_image_for_website_27_11_2025.webp&w=1920&q=75',
  },
  {
    name: 'imfresh Men Cream (Sweet Killer) | Whole body deodorant',
    price: 549,
    strike: 599,
    rating: 5769,
    tag: 'Popular',
    image: 'https://imfreshmen.com/_next/image?url=https%3A%2F%2Fstorage.googleapis.com%2Fgoodfeel_images%2Fproduct_image%2Fsweetkiller_imfresh_new_first_image_for_website_27_11_2025.webp&w=1920&q=75',
  },
  {
    name: 'imfresh Exfoliating Body Wash',
    price: 399,
    strike: 599,
    rating: 500,
    tag: 'Fresh drop',
    image: 'https://imfreshmen.com/_next/image?url=https%3A%2F%2Fstorage.googleapis.com%2Fgoodfeel_images%2Fproduct_image%2Favocado_body_wash_new_first_image_for_website_25_11_2025.webp&w=1920&q=75',
  },
];

const testimonialPlaceholder = 'https://dummyimage.com/240x240/f2f4ff/111827&text=imfresh+review';

const testimonials = [
  {
    name: 'Alice Smith',
    text: 'One of the best smelling deodorants I’ve purchased.',
    role: 'Buyer',
    image: 'https://images.unsplash.com/photo-1524504388940-b1c1722653e1?auto=format&fit=crop&w=400&q=80',
  },
  {
    name: 'Sanket Ingle',
    text: 'Great natural deodorant. Helps with odour and smells amazing.',
    role: 'Buyer',
    image: './assets/sanket.png',
  },
  {
    name: 'Emma Wilson',
    text: 'Wasn’t sure about cream deodorant, but this works better than sprays.',
    role: 'Buyer',
    image: 'https://images.unsplash.com/photo-1524502397800-2eeaad7c3fe5?auto=format&fit=crop&w=400&q=80',
  },
  {
    name: 'Michael Sanders',
    text: 'Nice fragrance without harmful chemicals. Go-to product.',
    role: 'Buyer',
    image: 'https://images.unsplash.com/photo-1463453091185-61582044d556?auto=format&fit=crop&w=400&q=80',
  },
  {
    name: 'Olivia Davis',
    text: 'Amazing fragrance and great at killing sweat smell.',
    role: 'Buyer',
    image: 'https://images.unsplash.com/photo-1494790108377-be9c29b29330?auto=format&fit=crop&w=400&q=80',
  },
];

const heroSlides = [
  {
    title: 'The unforgettable scent she can’t resist!',
    bullets: ['Blend of 11 premium notes', 'Long lasting', 'Scientifically formulated'],
    ctaText: 'Shop New Launch',
    image: './assets/hero-1.jpg',
    
  },
  {
    title: 'Smell Dope. Look Unbothered. Get Noticed.',
    bullets: ['Luxurious fragrance notes', 'Long lasting confidence', 'Magnetic night fragrance'],
    ctaText: 'Shop Dopenight',
    image: './assets/hero-2.jpg',
    
  },
];

function money(value) {
  return `₹ ${value}`;
}

function renderProducts(list, targetId) {
  const grid = document.getElementById(targetId);
  if (!grid) return;
  grid.innerHTML = list
    .map(
      (item) => `
      <article class="card product-card">
        <div class="badge">${item.tag}</div>
        <img src="${item.image || placeholder}" alt="${item.name}" loading="lazy" onerror="this.src='${placeholder}'">
        <h3>${item.name}</h3>
        <div class="stars">⭐️⭐️⭐️⭐️⭐️ <span class="product-meta">(${item.rating})</span></div>
        <div class="price">
          <span class="price__current">${money(item.price)}</span>
          <span class="price__strike">${money(item.strike)}</span>
        </div>
        <button class="btn primary full">Buy Now</button>
      </article>
    `,
    )
    .join('');
}

function initTestimonialCarousel() {
  const track = document.getElementById('testimonial-track');
  const prevBtn = document.querySelector('.testimonial__control.prev');
  const nextBtn = document.querySelector('.testimonial__control.next');
  if (!track || !prevBtn || !nextBtn) return;

  let perView = 1;
  let current = 0;
  let slides = [];
  let isAnimating = false;
  let resizeTimer = null;

  const getPerView = () => {
    if (window.innerWidth >= 1200) return 3;
    if (window.innerWidth >= 768) return 2;
    return 1;
  };

  // render slides including clones for infinite loop
  const renderSlides = () => {
    const clonesHead = testimonials.slice(0, perView);
    const clonesTail = testimonials.slice(-perView);
    const loopSlides = [...clonesTail, ...testimonials, ...clonesHead];

    track.innerHTML = loopSlides
      .map(
        (item) => `
      <article class="testimonial-card testimonial__slide">
        <div class="testimonial__avatar">
          <img src="${item.image || testimonialPlaceholder}" alt="${item.name}" loading="lazy" onerror="this.src='${testimonialPlaceholder}'" />
        </div>
        <div class="badge">Real review</div>
        <p>${item.text}</p>
        <h4>${item.name}</h4>
        <p class="muted">${item.role}</p>
        <div class="stars">★ ★ ★ ★ ★</div>
      </article>
    `,
      )
      .join('');

    slides = Array.from(track.children);
    slides.forEach((slide) => {
      // ensure consistent base style independent of CSS quirks
      slide.style.flex = `0 0 ${100 / perView}%`;
      slide.style.boxSizing = 'border-box';
    });

    // start at the first real slide (after clones)
    current = perView;
    // jump to initial position without transition (force layout)
    setTransform(false);
  };

  // core transform helper (uses translate3d for GPU)
  const setTransform = (withTransition = true) => {
    if (!track) return;
    track.style.willChange = 'transform';
    track.style.transition = withTransition ? 'transform 0.38s cubic-bezier(.22,.9,.36,1)' : 'none';
    // use translate3d to push to GPU and avoid subpixel rounding issues
    const percent = (100 / perView) * current;
    // use requestAnimationFrame to ensure the browser applies transition smoothly
    requestAnimationFrame(() => {
      track.style.transform = `translate3d(-${percent}%, 0, 0)`;
    });
  };

  const applyLayout = () => {
    const newPerView = getPerView();
    // avoid re-rendering when perView hasn't changed
    if (newPerView === perView && slides.length) return;
    perView = newPerView;
    renderSlides();
  };

  // next/prev handlers with basic click-throttle while animating
  const next = () => {
    if (isAnimating) return;
    isAnimating = true;
    current += 1;
    setTransform(true);
    toggleControls(true);
  };

  const prev = () => {
    if (isAnimating) return;
    isAnimating = true;
    current -= 1;
    setTransform(true);
    toggleControls(true);
  };

  // enable/disable controls visually and functionally
  const toggleControls = (disabled) => {
    prevBtn.disabled = disabled;
    nextBtn.disabled = disabled;
  };

  // when transition finishes, handle loop snapping without visual jump
  track.addEventListener('transitionend', () => {
    // compute boundaries
    const lastIndex = slides.length - perView;
    // if moved past the cloned head (end), snap back to real first slide
    if (current >= lastIndex) {
      // jump (no transition) to the real first slide index
      current = perView;
      // disable transition, set transform, force reflow, then re-enable
      track.style.transition = 'none';
      const percent = (100 / perView) * current;
      track.style.transform = `translate3d(-${percent}%, 0, 0)`;
      // force reflow to ensure the change is applied immediately
      void track.offsetHeight;
    } else if (current < perView) {
      // moved before the cloned tail (start), snap to the real last group
      current = slides.length - perView * 2;
      track.style.transition = 'none';
      const percent = (100 / perView) * current;
      track.style.transform = `translate3d(-${percent}%, 0, 0)`;
      void track.offsetHeight;
    }
    // allow a tiny tick before re-enabling transitions/controls so browser stabilizes
    setTimeout(() => {
      isAnimating = false;
      toggleControls(false);
      // restore default transition style (keeps future transitions smooth)
      track.style.transition = '';
    }, 20);
  });

  // attach UI handlers
  nextBtn.addEventListener('click', next);
  prevBtn.addEventListener('click', prev);

  // handle resize — debounce to avoid noisy reflows
  window.addEventListener('resize', () => {
    clearTimeout(resizeTimer);
    resizeTimer = setTimeout(() => {
      // preserve the currently-visible logical slide index as best as we can
      // compute index in the real testimonials array based on current position
      const visibleIndex = Math.round(current - perView);
      applyLayout();
      // clamp and restore current to keep the same visible slide after layout change
      current = Math.min(Math.max(perView + visibleIndex, perView), Math.max(slides.length - perView * 2, perView));
      setTransform(false);
    }, 140);
  });

  // initial layout
  applyLayout();

  // small UX: allow keyboard navigation (optional)
  document.addEventListener('keydown', (e) => {
    if (e.key === 'ArrowRight') next();
    if (e.key === 'ArrowLeft') prev();
  });
}


document.addEventListener('DOMContentLoaded', () => {
  renderProducts(combos, 'combo-grid');
  renderProducts(singles, 'singles-grid');
  initTestimonialCarousel();
  buildHero();

  const form = document.querySelector('.newsletter__form');
  if (form) {
    form.addEventListener('submit', (e) => {
      e.preventDefault();
      alert('Thanks for subscribing! (placeholder)');
      form.reset();
    });
  }
});

function buildHero() {
  const slidesWrap = document.getElementById('hero-slides');
  const dotsWrap = document.getElementById('hero-dots');
  if (!slidesWrap || !dotsWrap) return;

  slidesWrap.innerHTML = heroSlides
    .map(
      (slide) => `
        <div class="carousel__slide" style="background-image:url('${slide.image}'), url('${slide.fallback || slide.image}')">
        </div>
      `,
    )
    .join('');

  dotsWrap.innerHTML = heroSlides
    .map((_, idx) => `<span class="carousel__dot" data-index="${idx}"></span>`)
    .join('');

  const baseSlides = Array.from(document.querySelectorAll('.carousel__slide'));
  const dotEls = Array.from(document.querySelectorAll('.carousel__dot'));

  // If only one slide, no need for controls or cloning
  if (baseSlides.length <= 1) {
    dotEls.forEach((d, i) => d.classList.toggle('active', i === 0));
    return;
  }

  const total = baseSlides.length;
  let current = 0;

  const setTransform = (withTransition = true) => {
    slidesWrap.style.transition = withTransition ? 'transform 0.5s ease' : 'none';
    slidesWrap.style.transform = `translateX(-${current * 100}%)`;
  };

  const updateDots = () => {
    dotEls.forEach((d, i) => d.classList.toggle('active', i === current));
  };

  const next = () => {
    current = (current + 1) % total;
    setTransform(true);
    updateDots();
  };

  const prev = () => {
    current = (current - 1 + total) % total;
    setTransform(true);
    updateDots();
  };

  document.querySelector('.carousel__control.next')?.addEventListener('click', next);
  document.querySelector('.carousel__control.prev')?.addEventListener('click', prev);

  dotEls.forEach((dot, idx) =>
    dot.addEventListener('click', () => {
      current = idx;
      setTransform(true);
      updateDots();
    }),
  );

  // Initial state
  setTransform(false);
  updateDots();

  setInterval(next, 5000);
}

