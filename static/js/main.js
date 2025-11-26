document.addEventListener("DOMContentLoaded", () => {
  // Scroll Animations
  const observerOptions = {
    threshold: 0.1,
  };

  const observer = new IntersectionObserver((entries) => {
    entries.forEach((entry) => {
      if (entry.isIntersecting) {
        entry.target.style.opacity = "1";
        entry.target.style.transform = "translateY(0)";
      }
    });
  }, observerOptions);

  document.querySelectorAll(".feature-card").forEach((el) => {
    el.style.opacity = "0";
    el.style.transform = "translateY(30px)";
    el.style.transition = "all 0.6s ease-out";
    observer.observe(el);
  });

  // Parallax Effect for Hero
  window.addEventListener("scroll", () => {
    const scrolled = window.pageYOffset;
    const heroBg = document.querySelector(".hero-bg");
    if (heroBg) {
      heroBg.style.transform = `translateY(${scrolled * 0.5}px) scale(1.1)`;
    }
  });

  // Translation Dictionary
  const translations = {
    pt: {
      hero_title: "CleanChem Guard",
      hero_subtitle: "Conectando quem faz da limpeza uma arte.",
      hero_desc: "Conheça a CleanChainGuard, uma rede inteligente de cleaners que trocam conhecimento, segurança e resultados.",
      login_title: "Entrar na comunidade",
      create_account_btn: "Criar Conta",
      explore_gallery: "Explorar Galeria",
      section1_title: "Juntos, elevamos o padrão da limpeza.",
      section1_desc: "Conecte-se com profissionais que compartilham os melhores produtos, técnicas e experiências.",
      section2_title: "A CleanChainGuard é a comunidade onde quem limpa com excelência se torna referência",
      section2_desc: "Agora com o suporte de uma inteligência artificial que tira suas dúvidas sobre produtos, métodos e segurança.",
      section3_title: "Use melhor cada produto",
      section3_desc: "Trabalhe com mais confiança e cuide da sua saúde e bem-estar. Produtividade, segurança e sabedoria tudo em um só lugar.",
      feat1_title: "Sabedoria compartilhada",
      feat1_desc: "Aprenda com a experiência de outros profissionais.",
      feat2_title: "Produtividade real",
      feat2_desc: "Otimize tempo e resultados com métodos testados.",
      feat3_title: "Qualidade e segurança",
      feat3_desc: "Produtos recomendados e uso seguro comprovado com ajuda de inteligência artificial.",
      feat4_title: "Conexão e comunidade",
      feat4_desc: "Interaja com quem vive os mesmos desafios e conquistas.",
      newsletter_title: "Fique por dentro das novidades",
      newsletter_desc: "Receba dicas exclusivas e atualizações da comunidade.",
      subscribe_btn: "Inscrever-se",
      closing_title: "Mais do que uma plataforma — uma rede de evolução.",
      closing_desc: "Na CleanChainGuard, cada profissional tem voz. Compartilhe métodos, aprenda novas técnicas, descubra produtos aprovados por quem realmente entende e aumente sua segurança no trabalho.",
      closing_tagline: "Limpeza inteligente começa com colaboração."
    },
    en: {
      hero_title: "CleanChem Guard",
      hero_subtitle: "Connecting those who make cleaning an art.",
      hero_desc: "Meet CleanChainGuard, an intelligent network of cleaners exchanging knowledge, safety, and results.",
      login_title: "Enter the Community",
      login_btn: "Login",
      create_account_btn: "Create Account",
      new_here: "New here?",
      create_account: "Create an account",
      explore_gallery: "Explore Gallery",
      section1_title: "Together, we raise the standard of cleaning.",
      section1_desc: "Connect with professionals who share the best products, techniques, and experiences.",
      section2_title: "CleanChainGuard is the community where excellence becomes the reference",
      section2_desc: "Now with the support of an artificial intelligence that answers your questions about products, methods, and safety.",
      section3_title: "Use every product better",
      section3_desc: "Work with more confidence and take care of your health and well-being. Productivity, safety, and wisdom all in one place.",
      feat1_title: "Shared Wisdom",
      feat1_desc: "Learn from the experience of other professionals.",
      feat2_title: "Real Productivity",
      feat2_desc: "Optimize time and results with tested methods.",
      feat3_title: "Quality and Safety",
      feat3_desc: "Recommended products and proven safe usage with AI assistance.",
      feat4_title: "Connection and Community",
      feat4_desc: "Interact with those who live the same challenges and achievements.",
      newsletter_title: "Stay Updated",
      newsletter_desc: "Get exclusive tips and community updates.",
      subscribe_btn: "Subscribe",
      closing_title: "More than a platform — a network of evolution.",
      closing_desc: "At CleanChainGuard, every professional has a voice. Share methods, learn new techniques, discover products approved by those who truly understand, and increase your work safety.",
      closing_tagline: "Smart cleaning starts with collaboration."
    },
    es: {
      hero_title: "CleanChem Guard",
      hero_subtitle: "Conectando a quienes hacen de la limpieza un arte.",
      hero_desc: "Conozca CleanChainGuard, una red inteligente de cleaners que intercambian conocimiento, seguridad y resultados.",
      login_title: "Entrar en la comunidad",
      login_btn: "Iniciar sesión",
      create_account_btn: "Crear Cuenta",
      new_here: "¿Nuevo aquí?",
      create_account: "Crear una cuenta",
      explore_gallery: "Explorar Galería",
      section1_title: "Juntos, elevamos el estándar de la limpieza.",
      section1_desc: "Conéctese con profesionales que comparten los mejores productos, técnicas y experiencias.",
      section2_title: "CleanChainGuard es la comunidad donde la excelencia se convierte en referencia",
      section2_desc: "Ahora con el soporte de una inteligencia artificial que responde sus dudas sobre productos, métodos y seguridad.",
      section3_title: "Use mejor cada producto",
      section3_desc: "Trabaje con más confianza y cuide su salud y bienestar. Productividad, seguridad y sabiduría todo en un solo lugar.",
      feat1_title: "Sabiduría compartida",
      feat1_desc: "Aprenda de la experiencia de otros profesionales.",
      feat2_title: "Productividad real",
      feat2_desc: "Optimice tiempo y resultados con métodos probados.",
      feat3_title: "Calidad y seguridad",
      feat3_desc: "Productos recomendados y uso seguro comprobado con ayuda de inteligencia artificial.",
      feat4_title: "Conexión y comunidad",
      feat4_desc: "Interactúe con quienes viven los mismos desafíos y logros.",
      newsletter_title: "Manténgase Actualizado",
      newsletter_desc: "Reciba consejos exclusivos y actualizaciones de la comunidad.",
      subscribe_btn: "Suscribirse",
      closing_title: "Más que una plataforma — una red de evolución.",
      closing_desc: "En CleanChainGuard, cada profesional tiene voz. Comparta métodos, aprenda nuevas técnicas, descubra productos aprobados por quienes realmente entienden y aumente su seguridad en el trabajo.",
      closing_tagline: "La limpieza inteligente comienza con colaboración."
    }
  };

  // Language Switching Logic
  const langOptions = document.querySelectorAll(".lang-option");
  const langText = document.getElementById("lang-text");
  
  function setLanguage(lang) {
    // Update display text
    if (langText) {
        langText.textContent = lang.toUpperCase();
    }

    // Update text content
    document.querySelectorAll("[data-i18n]").forEach(el => {
      const key = el.dataset.i18n;
      if (translations[lang] && translations[lang][key]) {
        el.textContent = translations[lang][key];
      }
    });

    // Save preference
    localStorage.setItem("preferred_lang", lang);
  }

  // Initialize language
  const savedLang = localStorage.getItem("preferred_lang") || "pt";
  setLanguage(savedLang);

  langOptions.forEach(btn => {
    btn.addEventListener("click", () => {
      setLanguage(btn.dataset.lang);
    });
  });

  // Navbar Scroll Effect
  const nav = document.querySelector(".glass-nav");
  window.addEventListener("scroll", () => {
    if (window.scrollY > 50) {
      nav.style.background = "rgba(15, 23, 42, 0.95)";
    } else {
      nav.style.background = "rgba(15, 23, 42, 0.7)";
    }
  });
});
