<script setup>
import { ref, onMounted, onUnmounted } from 'vue';
import { 
  Menu, X, Layers, Grid, Hexagon, Package,
  Factory, Flame, Zap, CheckCircle,
  Leaf, Lightbulb, Truck, Award,
  MapPin, Phone, Mail, Clock,
  Linkedin, Facebook, Instagram, Youtube,
  Calendar, Users, Settings, HardHat,
  ChevronDown
} from 'lucide-vue-next';

// --- State ---
const isScrolled = ref(false);
const mobileMenuOpen = ref(false);
const activeProcessStep = ref(0);
const formData = ref({
  name: '',
  email: '',
  company: '',
  phone: '',
  message: ''
});

// --- Data ---
const products = [
  {
    id: 1,
    title: 'Bobinas & Chapas',
    description: 'Aço plano de alta resistência para indústria automotiva e linha branca. Espessuras de 0,5mm a 12mm.',
    icon: Layers,
    specs: ['Aço carbono', 'Aço inoxidável', 'Galvanizado'],
    image: 'https://images.unsplash.com/photo-1697698532602-ccf880036281?q=80&w=2340&auto=format&fit=crop&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D'
  },
  {
    id: 2,
    title: 'Vergalhões & Construção',
    description: 'CA-50 e CA-60 com a química exata para grandes estruturas. Diâmetros de 6,3mm a 40mm.',
    icon: Package,
    specs: ['CA-50', 'CA-60', 'Certificado ABNT'],
    image: 'https://images.unsplash.com/photo-1763926025680-7966e45e48f5?q=80&w=1338&auto=format&fit=crop&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D'
  },
  {
    id: 3,
    title: 'Tubos & Perfis',
    description: 'Conformação de precisão para aplicações estruturais e industriais. Alta resistência e durabilidade.',
    icon: Hexagon,
    specs: ['Tubos redondos', 'Tubos quadrados', 'Perfis U e I'],
    image: 'https://images.unsplash.com/photo-1763950865873-41f63536825b?q=80&w=3067&auto=format&fit=crop&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D'
  },
  {
    id: 4,
    title: 'Soluções de Varejo',
    description: 'Treliças, Malhas Pop e Telhas para o consumidor final. Produtos prontos para uso.',
    icon: Grid,
    specs: ['Treliças nervuradas', 'Malhas soldadas', 'Telhas metálicas'],
    image: 'https://images.unsplash.com/photo-1610551675799-50d4d0fe0252?q=80&w=1480&auto=format&fit=crop&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D'
  }
];

const stats = [
  { label: 'Anos de Mercado', value: '35+', icon: Calendar },
  { label: 'Clientes Ativos', value: '+2.500', icon: Users },
  { label: 'Toneladas/Mês', value: '50.000', icon: Settings },
  { label: 'Colaboradores', value: '+800', icon: HardHat }
];

const processSteps = [
  {
    id: 1,
    title: 'Alto-Forno',
    description: 'Conversão do minério de ferro em ferro-gusa através de processos de redução a altas temperaturas.',
    temperature: '1500°C',
    icon: Flame,
    image: 'https://images.unsplash.com/photo-1697281679213-fcab27e10ad4?q=80&w=2342&auto=format&fit=crop&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D'
  },
  {
    id: 2,
    title: 'Aciaria',
    description: 'Transformação do ferro-gusa em aço através da adição controlada de elementos químicos.',
    temperature: '1600°C',
    icon: Zap,
    image: 'https://images.unsplash.com/photo-1697281679290-ad7be1b10682?q=80&w=2340&auto=format&fit=crop&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D'
  },
  {
    id: 3,
    title: 'Laminação',
    description: 'Conformação mecânica do aço em bobinas, chapas e perfis com as dimensões desejadas.',
    temperature: '1200°C',
    icon: Settings,
    image: 'https://images.unsplash.com/photo-1748946469841-99e75941b997?q=80&w=2340&auto=format&fit=crop&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D'
  },
  {
    id: 4,
    title: 'Acabamento',
    description: 'Tratamentos finais: corte, galvanização, pintura e controle de qualidade rigoroso.',
    temperature: 'Ambiente',
    icon: CheckCircle,
    image: 'https://images.unsplash.com/photo-1588763806929-eb1eee34e6a6?q=80&w=2340&auto=format&fit=crop&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D'
  }
];

const certifications = [
  { name: 'ISO 9001:2015', desc: 'Gestão de Qualidade', icon: Award },
  { name: 'ISO 14001', desc: 'Gestão Ambiental', icon: Leaf },
  { name: 'ISO 45001', desc: 'Segurança do Trabalho', icon: CheckCircle },
  { name: 'ABNT NBR 16001', desc: 'Responsabilidade Social', icon: Users }
];

const values = [
  { 
    title: 'Qualidade Garantida',
    description: 'Controle rigoroso em todas as etapas da produção com laboratórios próprios.',
    icon: CheckCircle
  },
  { 
    title: 'Sustentabilidade',
    description: 'ETE própria, reciclagem de materiais e redução de emissões de CO₂.',
    icon: Leaf
  },
  { 
    title: 'Inovação Constante',
    description: 'Investimento contínuo em tecnologia e desenvolvimento de novos produtos.',
    icon: Lightbulb
  },
  { 
    title: 'Logística Estratégica',
    description: 'Localização privilegiada no eixo Rio-SP com frota própria.',
    icon: Truck
  }
];

const clients = [
  { sector: 'Construção Civil', percentage: '40%' },
  { sector: 'Indústria Automotiva', percentage: '25%' },
  { sector: 'Linha Branca', percentage: '20%' },
  { sector: 'Outros Setores', percentage: '15%' }
];

// --- Methods ---
const toggleMenu = () => {
  mobileMenuOpen.value = !mobileMenuOpen.value;
};

const handleScroll = () => {
  isScrolled.value = window.scrollY > 50;
};

const smoothScrollTo = (e, target) => {
  e.preventDefault();
  const element = document.querySelector(target);
  if (element) {
    const headerOffset = 80;
    const elementPosition = element.getBoundingClientRect().top;
    const offsetPosition = elementPosition + window.pageYOffset - headerOffset;

    window.scrollTo({
      top: offsetPosition,
      behavior: 'smooth'
    });
  }
  // Fechar menu mobile se estiver aberto
  if (mobileMenuOpen.value) {
    mobileMenuOpen.value = false;
  }
};

const setActiveProcess = (index) => {
  activeProcessStep.value = index;
};

const submitForm = () => {
  // Aqui você implementaria a lógica de envio do formulário
  console.log('Form submitted:', formData.value);
  alert('Mensagem enviada com sucesso! Entraremos em contato em breve.');
  formData.value = {
    name: '',
    email: '',
    company: '',
    phone: '',
    message: ''
  };
};

// --- Lifecycle ---
onMounted(() => {
  window.addEventListener('scroll', handleScroll);
  
  // Auto-rotate process steps
  setInterval(() => {
    activeProcessStep.value = (activeProcessStep.value + 1) % processSteps.length;
  }, 5000);
});

onUnmounted(() => {
  window.removeEventListener('scroll', handleScroll);
});
</script>

<template>
  <div class="vale-foundry">
    <!-- Header -->
    <header class="header" :class="{ 'header--scrolled': isScrolled }">
      <div class="container header__container">
        <div class="logo">
          <span class="logo__text">VALE FOUNDRY</span>
          <span class="logo__sub">TAUBATÉ</span>
        </div>

        <nav class="nav desktop-only">
          <a href="#home" class="nav__link" @click="(e) => smoothScrollTo(e, '#home')">Home</a>
          <a href="#about" class="nav__link" @click="(e) => smoothScrollTo(e, '#about')">Sobre</a>
          <a href="#products" class="nav__link" @click="(e) => smoothScrollTo(e, '#products')">Produtos</a>
          <a href="#process" class="nav__link" @click="(e) => smoothScrollTo(e, '#process')">Processo</a>
          <a href="#values" class="nav__link" @click="(e) => smoothScrollTo(e, '#values')">Valores</a>
          <a href="#contact" class="nav__link" @click="(e) => smoothScrollTo(e, '#contact')">Contato</a>
        </nav>

        <button class="mobile-toggle mobile-only" @click="toggleMenu" aria-label="Menu">
          <Menu v-if="!mobileMenuOpen" :size="26" :stroke-width="2" />
          <X v-else :size="26" :stroke-width="2" />
        </button>
      </div>

      <!-- Mobile Menu -->
      <div class="mobile-menu" :class="{ 'mobile-menu--open': mobileMenuOpen }">
        <a href="#home" class="mobile-menu__link" @click="(e) => smoothScrollTo(e, '#home')">Home</a>
        <a href="#about" class="mobile-menu__link" @click="(e) => smoothScrollTo(e, '#about')">Sobre</a>
        <a href="#products" class="mobile-menu__link" @click="(e) => smoothScrollTo(e, '#products')">Produtos</a>
        <a href="#process" class="mobile-menu__link" @click="(e) => smoothScrollTo(e, '#process')">Processo</a>
        <a href="#values" class="mobile-menu__link" @click="(e) => smoothScrollTo(e, '#values')">Valores</a>
        <a href="#contact" class="mobile-menu__link" @click="(e) => smoothScrollTo(e, '#contact')">Contato</a>
      </div>
    </header>

    <!-- Hero Section -->
    <section id="home" class="hero">
      <div class="hero__overlay"></div>
      <div class="hero__particles">
        <div class="particle" v-for="n in 20" :key="n" :style="{ 
          left: Math.random() * 100 + '%', 
          animationDelay: Math.random() * 5 + 's',
          animationDuration: (Math.random() * 10 + 10) + 's'
        }"></div>
      </div>
      <div class="container hero__content">
        <div class="hero__badge">
          <Factory :size="18" :stroke-width="2" />
          <span>35+ Anos de Excelência</span>
        </div>
        <h1 class="hero__title">
          TRANSFORMANDO MINÉRIO <br>
          <span class="text-highlight">EM OPORTUNIDADES</span>
        </h1>
        <p class="hero__subtitle">Siderurgia integrada de ponta a ponta no coração do Vale do Paraíba</p>
        <div class="hero__cta">
          <a href="#products" class="btn btn--primary" @click="(e) => smoothScrollTo(e, '#products')">Conheça Nossos Produtos</a>
          <a href="#contact" class="btn btn--secondary" @click="(e) => smoothScrollTo(e, '#contact')">Solicitar Orçamento</a>
        </div>
        <div class="hero__scroll" @click="(e) => smoothScrollTo(e, '#about')">
          <span>Role para explorar</span>
          <ChevronDown :size="20" :stroke-width="2" class="bounce-icon" />
        </div>
      </div>
    </section>

    <!-- Stats Bar -->
    <section class="stats-section">
      <div class="container">
        <div class="stats-grid">
          <div class="stat-card" v-for="(stat, index) in stats" :key="index">
            <div class="stat-card__icon">
              <component :is="stat.icon" :size="48" :stroke-width="2" />
            </div>
            <div class="stat-card__value">{{ stat.value }}</div>
            <div class="stat-card__label">{{ stat.label }}</div>
          </div>
        </div>
      </div>
    </section>

    <!-- About Section -->
    <section id="about" class="section about">
      <div class="container">
        <div class="about-content">
          <div class="about-image">
            <img src="https://images.unsplash.com/photo-1720036237467-f902c13bc5a7?q=80&w=1287&auto=format&fit=crop&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D" alt="Siderúrgica Vale Foundry">
          </div>
          <div class="about-text">
        <div class="section-header">
          <h2 class="section-title">A Força do Aço no Coração do Vale</h2>
          <div class="section-line"></div>
        </div>

            <div class="about-timeline">
              <div class="timeline-item">
                <div class="timeline-item__number">01</div>
                <div class="timeline-item__content">
                  <h3>A Origem</h3>
                  <p>A história da Vale Foundry não começa apenas com a construção de um galpão, mas com uma leitura estratégica do mercado. Situada em Taubaté, no coração do Vale do Paraíba, nascemos para suprir a indústria automotiva e a construção civil da região mais rica do país.</p>
          </div>
          </div>

              <div class="timeline-item">
                <div class="timeline-item__number">02</div>
                <div class="timeline-item__content">
                  <h3>Full Cycle</h3>
                  <p>Nosso marco foi o acendimento da Unidade 4 (Alto-Forno). Deixamos de ser processadores para controlar o DNA do aço. Do minério bruto ao ferro-gusa, garantimos a química exata para vergalhões e bobinas de alta performance.</p>
          </div>
        </div>

              <div class="timeline-item">
                <div class="timeline-item__number">03</div>
                <div class="timeline-item__content">
                  <h3>Valor Agregado</h3>
                  <p>Evoluímos para entregar soluções. Inauguramos nosso Centro de Serviços com tecnologia de corte Slitter, galvanização e tubos. Hoje, vamos além da indústria, chegando à casa do cliente com linhas de Treliças e Telhas.</p>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- Products Section -->
    <section id="products" class="section products">
      <div class="container">
        <div class="section-header center">
          <h2 class="section-title">Portfólio de Produtos</h2>
          <p class="section-subtitle">Soluções em aço para todos os segmentos da indústria</p>
          <div class="section-line center"></div>
        </div>

        <div class="products-grid">
          <div class="product-card" v-for="product in products" :key="product.id">
            <div class="product-card__image" :style="{ backgroundImage: `url(${product.image})` }">
              <div class="product-card__overlay"></div>
            </div>
            <div class="product-card__content">
            <div class="product-card__icon">
                <component :is="product.icon" :size="40" :stroke-width="2" />
            </div>
            <h3 class="product-card__title">{{ product.title }}</h3>
            <p class="product-card__desc">{{ product.description }}</p>
              <div class="product-card__specs">
                <span v-for="(spec, idx) in product.specs" :key="idx" class="spec-badge">{{ spec }}</span>
              </div>
              <a href="#contact" class="product-card__link" @click="(e) => smoothScrollTo(e, '#contact')">Solicitar Orçamento &rarr;</a>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- Process Section -->
    <section id="process" class="section process">
      <div class="container">
        <div class="section-header center">
          <h2 class="section-title">Nosso Processo de Produção</h2>
          <p class="section-subtitle">Do minério ao produto final: excelência em cada etapa</p>
          <div class="section-line center"></div>
        </div>

        <div class="process-content">
          <div class="process-steps">
            <div 
              class="process-step" 
              v-for="(step, index) in processSteps" 
              :key="step.id"
              :class="{ 'process-step--active': activeProcessStep === index }"
              @click="setActiveProcess(index)"
            >
              <div class="process-step__icon">
                <component :is="step.icon" :size="40" :stroke-width="2" />
              </div>
              <div class="process-step__info">
                <h3>{{ step.title }}</h3>
                <p>{{ step.description }}</p>
                <span class="process-step__temp">
                  <Flame :size="16" :stroke-width="2" />
                  {{ step.temperature }}
                </span>
              </div>
            </div>
          </div>

          <div class="process-visual">
            <div 
              class="process-image" 
              v-for="(step, index) in processSteps" 
              :key="'img-' + step.id"
              :class="{ 'process-image--active': activeProcessStep === index }"
              :style="{ backgroundImage: `url(${step.image})` }"
            >
              <div class="process-image__overlay"></div>
              <div class="process-image__temp">
                <Flame :size="20" :stroke-width="2" />
                {{ step.temperature }}
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- Values Section -->
    <section id="values" class="section values">
      <div class="container">
        <div class="section-header center">
          <h2 class="section-title">Nossos Valores</h2>
          <p class="section-subtitle">O que nos torna referência no setor siderúrgico</p>
          <div class="section-line center"></div>
        </div>

        <div class="values-grid">
          <div class="value-card" v-for="(value, index) in values" :key="index">
            <div class="value-card__icon">
              <component :is="value.icon" :size="56" :stroke-width="1.5" />
            </div>
            <h3 class="value-card__title">{{ value.title }}</h3>
            <p class="value-card__desc">{{ value.description }}</p>
          </div>
        </div>

        <!-- Certifications -->
        <div class="certifications">
          <h3 class="certifications__title">Certificações & Normas</h3>
          <div class="certifications-grid">
            <div class="cert-badge" v-for="cert in certifications" :key="cert.name">
              <div class="cert-badge__icon">
                <component :is="cert.icon" :size="40" :stroke-width="2" />
              </div>
              <div class="cert-badge__name">{{ cert.name }}</div>
              <div class="cert-badge__desc">{{ cert.desc }}</div>
            </div>
          </div>
        </div>

        <!-- Clients -->
        <div class="clients-section">
          <h3 class="clients__title">Segmentos Atendidos</h3>
          <div class="clients-grid">
            <div class="client-item" v-for="client in clients" :key="client.sector">
              <div class="client-item__bar" :style="{ width: client.percentage }"></div>
              <div class="client-item__info">
                <span class="client-item__sector">{{ client.sector }}</span>
                <span class="client-item__percentage">{{ client.percentage }}</span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- Contact Section -->
    <section id="contact" class="section contact">
      <div class="container">
        <div class="contact-content">
          <div class="contact-info">
            <div class="section-header">
              <h2 class="section-title">Entre em Contato</h2>
              <p class="section-subtitle">Estamos prontos para atender suas necessidades</p>
              <div class="section-line"></div>
            </div>

            <div class="contact-details">
              <div class="contact-item">
                <div class="contact-item__icon">
                  <MapPin :size="32" :stroke-width="2" />
                </div>
                <div class="contact-item__text">
                  <h4>Endereço</h4>
                  <p>Via Dutra, Km 132 - Taubaté, SP<br>CEP 12080-000</p>
                </div>
              </div>

              <div class="contact-item">
                <div class="contact-item__icon">
                  <Phone :size="32" :stroke-width="2" />
                </div>
                <div class="contact-item__text">
                  <h4>Telefone</h4>
                  <p>(12) 3625-8900<br>0800 777 8900</p>
                </div>
              </div>

              <div class="contact-item">
                <div class="contact-item__icon">
                  <Mail :size="32" :stroke-width="2" />
                </div>
                <div class="contact-item__text">
                  <h4>E-mail</h4>
                  <p>vendas@valefoundry.com.br<br>comercial@valefoundry.com.br</p>
                </div>
              </div>

              <div class="contact-item">
                <div class="contact-item__icon">
                  <Clock :size="32" :stroke-width="2" />
                </div>
                <div class="contact-item__text">
                  <h4>Horário de Atendimento</h4>
                  <p>Segunda a Sexta: 8h às 18h<br>Sábado: 8h às 12h</p>
                </div>
              </div>
            </div>
          </div>

          <div class="contact-form">
            <form @submit.prevent="submitForm">
              <div class="form-group">
                <label for="name">Nome Completo *</label>
                <input type="text" id="name" v-model="formData.name" required placeholder="Seu nome">
              </div>

              <div class="form-row">
                <div class="form-group">
                  <label for="email">E-mail *</label>
                  <input type="email" id="email" v-model="formData.email" required placeholder="seu@email.com">
                </div>

                <div class="form-group">
                  <label for="phone">Telefone *</label>
                  <input type="tel" id="phone" v-model="formData.phone" required placeholder="(00) 00000-0000">
                </div>
              </div>

              <div class="form-group">
                <label for="company">Empresa</label>
                <input type="text" id="company" v-model="formData.company" placeholder="Nome da empresa">
              </div>

              <div class="form-group">
                <label for="message">Mensagem *</label>
                <textarea id="message" v-model="formData.message" required rows="5" placeholder="Como podemos ajudar?"></textarea>
              </div>

              <button type="submit" class="btn btn--primary btn--full">Enviar Mensagem</button>
            </form>
          </div>
        </div>
      </div>
    </section>

    <!-- Footer -->
    <footer class="footer">
      <div class="container footer__container">
        <div class="footer__top">
        <div class="footer__brand">
            <div class="logo">
          <span class="logo__text">VALE FOUNDRY</span>
              <span class="logo__sub">TAUBATÉ</span>
        </div>
            <p class="footer__desc">Qualidade que constrói o futuro. Referência em siderurgia integrada no Vale do Paraíba.</p>
            <div class="footer__social">
              <a href="#" aria-label="LinkedIn">
                <Linkedin :size="20" :stroke-width="2" />
              </a>
              <a href="#" aria-label="Facebook">
                <Facebook :size="20" :stroke-width="2" />
              </a>
              <a href="#" aria-label="Instagram">
                <Instagram :size="20" :stroke-width="2" />
              </a>
              <a href="#" aria-label="YouTube">
                <Youtube :size="20" :stroke-width="2" />
              </a>
            </div>
          </div>

          <div class="footer__links-group">
            <h4>Empresa</h4>
            <a href="#about">Sobre Nós</a>
            <a href="#history">História</a>
            <a href="#values">Valores</a>
            <a href="#">Trabalhe Conosco</a>
          </div>

          <div class="footer__links-group">
            <h4>Produtos</h4>
            <a href="#products">Bobinas & Chapas</a>
            <a href="#products">Vergalhões</a>
            <a href="#products">Tubos & Perfis</a>
            <a href="#products">Soluções Varejo</a>
        </div>

          <div class="footer__links-group">
            <h4>Suporte</h4>
            <a href="#contact">Contato</a>
            <a href="#">FAQ</a>
          <a href="#">Política de Privacidade</a>
          <a href="#">Termos de Uso</a>
        </div>
        </div>

        <div class="footer__bottom">
          <p>&copy; {{ new Date().getFullYear() }} Vale Foundry Taubaté. Todos os direitos reservados.</p>
          <p>Desenvolvido com 💙 para a indústria brasileira</p>
        </div>
      </div>
    </footer>
  </div>
</template>

<style scoped>
/* --- Variables & Reset --- */
:root {
  --color-bg: #0a0a0a;
  --color-bg-alt: #111111;
  --color-bg-card: #1a1a1a;
  --color-text: #e0e0e0;
  --color-text-muted: #a0a0a0;
  --color-primary: #2c3e50;
  --color-accent-orange: #ff5722;
  --color-accent-blue: #2980b9;
  --color-accent-gold: #ffa726;
  --color-border: #333333;
  --color-success: #4caf50;
  
  --font-main: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, 'Open Sans', 'Helvetica Neue', sans-serif;
  
  --container-width: 1280px;
  --header-height: 80px;
  --transition-speed: 0.3s;
  --transition-slow: 0.6s;
  --transition-smooth: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
  --transition-bounce: all 0.5s cubic-bezier(0.68, -0.55, 0.265, 1.55);
}

*, *::before, *::after {
  box-sizing: border-box;
  margin: 0;
  padding: 0;
}

html {
  scroll-behavior: smooth;
}

.vale-foundry {
  background-color: var(--color-bg, #0a0a0a);
  color: var(--color-text, #e0e0e0);
  font-family: var(--font-main, sans-serif);
  line-height: 1.6;
  overflow-x: hidden;
}

.container {
  max-width: var(--container-width, 1280px);
  margin: 0 auto;
  padding: 0 20px;
}

a {
  text-decoration: none;
  color: inherit;
  transition: color var(--transition-speed, 0.3s);
}

button {
  font-family: inherit;
}

/* --- Header --- */
.header {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: var(--header-height, 80px);
  z-index: 1000;
  transition: all var(--transition-speed, 0.3s);
  border-bottom: 1px solid transparent;
}

.header--scrolled {
  background-color: rgba(10, 10, 10, 0.95);
  backdrop-filter: blur(20px);
  border-bottom: 1px solid var(--color-border, #333);
  box-shadow: 0 4px 30px rgba(0, 0, 0, 0.3);
}

.header__container {
  display: flex;
  justify-content: space-between;
  align-items: center;
  height: 100%;
}

.logo {
  display: flex;
  flex-direction: column;
  line-height: 1;
  cursor: pointer;
  transition: transform var(--transition-speed);
}

.logo:hover {
  transform: translateY(-2px);
}

.logo__text {
  font-weight: 800;
  font-size: 1.5rem;
  letter-spacing: -0.02em;
  color: #fff;
}

.logo__sub {
  font-size: 0.75rem;
  letter-spacing: 0.2em;
  color: var(--color-accent-orange, #ff5722);
  text-transform: uppercase;
}

.nav {
  display: flex;
  gap: 40px;
}

.nav__link {
  font-size: 0.85rem;
  font-weight: 500;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  color: var(--color-text-muted, #a0a0a0);
  position: relative;
  padding: 5px 0;
}

.nav__link::after {
  content: '';
  position: absolute;
  bottom: 0;
  left: 0;
  width: 0;
  height: 2px;
  background-color: var(--color-accent-orange);
  transition: width var(--transition-speed);
}

.nav__link:hover {
  color: var(--color-accent-orange, #ff5722);
}

.nav__link:hover::after {
  width: 100%;
}

/* --- Mobile Menu --- */
.mobile-toggle {
  background: none;
  border: none;
  cursor: pointer;
  padding: 10px;
  z-index: 1001;
  color: #fff;
  transition: all var(--transition-speed);
  display: flex;
  align-items: center;
  justify-content: center;
}

.mobile-toggle:hover {
  color: var(--color-accent-orange);
  transform: scale(1.1);
}

.mobile-menu {
  position: fixed;
  top: var(--header-height, 80px);
  left: 0;
  width: 100%;
  background-color: rgba(10, 10, 10, 0.98);
  backdrop-filter: blur(20px);
  padding: 30px 20px;
  display: flex;
  flex-direction: column;
  gap: 10px;
  transform: translateY(-150%);
  opacity: 0;
  transition: transform var(--transition-speed), opacity var(--transition-speed);
  z-index: 999;
  border-bottom: 1px solid var(--color-border, #333);
  box-shadow: 0 10px 40px rgba(0, 0, 0, 0.5);
}

.mobile-menu--open {
  transform: translateY(0);
  opacity: 1;
}

.mobile-menu__link {
  font-size: 1.1rem;
  font-weight: 600;
  color: #fff;
  padding: 15px 10px;
  border-bottom: 1px solid #222;
  transition: all var(--transition-speed);
  text-transform: uppercase;
  letter-spacing: 0.05em;
}

.mobile-menu__link:hover {
  color: var(--color-accent-orange);
  padding-left: 20px;
}

/* --- Hero Section --- */
.hero {
  min-height: 100vh;
  position: relative;
  display: flex;
  align-items: center;
  justify-content: center;
  background-image: linear-gradient(135deg, rgba(0,0,0,0.7), rgba(255,87,34,0.2)), url('https://images.unsplash.com/photo-1474674556023-efef886fa147?q=80&w=2340&auto=format&fit=crop&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D');
  background-size: cover;
  background-position: center;
  background-attachment: fixed;
  overflow: hidden;
}

.hero__overlay {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: radial-gradient(circle at 30% 50%, rgba(255,87,34,0.1), transparent 50%);
  pointer-events: none;
}

.hero__particles {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  overflow: hidden;
  pointer-events: none;
}

.particle {
  position: absolute;
  width: 3px;
  height: 3px;
  background-color: rgba(255, 255, 255, 0.3);
  border-radius: 50%;
  animation: float-particle linear infinite;
}

@keyframes float-particle {
  0% {
    transform: translateY(100vh) translateX(0);
    opacity: 0;
  }
  10% {
    opacity: 1;
  }
  90% {
    opacity: 1;
  }
  100% {
    transform: translateY(-100vh) translateX(50px);
    opacity: 0;
  }
}

.hero__content {
  text-align: center;
  z-index: 2;
  max-width: 900px;
  padding: 0 20px;
  animation: fade-in-up 1s ease-out;
}

@keyframes fade-in-up {
  from {
    opacity: 0;
    transform: translateY(30px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.hero__badge {
  display: inline-flex;
  align-items: center;
  gap: 10px;
  padding: 12px 28px;
  background-color: rgba(255, 87, 34, 0.15);
  border: 1px solid rgba(255, 87, 34, 0.3);
  border-radius: 50px;
  color: var(--color-accent-orange);
  font-size: 0.85rem;
  font-weight: 600;
  letter-spacing: 0.05em;
  margin-bottom: 30px;
  text-transform: uppercase;
  animation: pulse-glow 2s ease-in-out infinite;
  backdrop-filter: blur(10px);
  transition: all var(--transition-speed);
}

.hero__badge:hover {
  background-color: rgba(255, 87, 34, 0.25);
  border-color: rgba(255, 87, 34, 0.5);
  transform: scale(1.05);
}

@keyframes pulse-glow {
  0%, 100% {
    box-shadow: 0 0 10px rgba(255, 87, 34, 0.3);
  }
  50% {
    box-shadow: 0 0 20px rgba(255, 87, 34, 0.5);
  }
}

.hero__title {
  font-size: 4.5rem;
  font-weight: 900;
  line-height: 1.05;
  margin-bottom: 65px;
  text-transform: uppercase;
  letter-spacing: -0.02em;
  text-shadow: 2px 4px 20px rgba(0, 0, 0, 0.5);
}

.text-highlight {
  background: linear-gradient(135deg, #fff, var(--color-accent-orange), var(--color-accent-blue));
  -webkit-background-clip: text;
  background-clip: text;
  animation: gradient-shift 5s ease infinite;
  background-size: 200% 200%;
}

@keyframes gradient-shift {
  0%, 100% {
    background-position: 0% 50%;
  }
  50% {
    background-position: 100% 50%;
  }
}

.hero__subtitle {
  font-size: 1.35rem;
  color: #ccc;
  margin-bottom: 45px;
  font-weight: 300;
  line-height: 1.6;
}

.hero__cta {
  display: flex;
  gap: 20px;
  justify-content: center;
  flex-wrap: wrap;
  margin-bottom: 60px;
}

.hero__scroll {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 10px;
  color: var(--color-text-muted);
  font-size: 0.85rem;
  text-transform: uppercase;
  letter-spacing: 0.1em;
  cursor: pointer;
  transition: all var(--transition-speed);
}

.hero__scroll:hover {
  color: var(--color-accent-orange);
  transform: translateY(5px);
}

.bounce-icon {
  animation: bounce 2s ease-in-out infinite;
}

@keyframes bounce {
  0%, 100% {
    transform: translateY(0);
  }
  50% {
    transform: translateY(10px);
  }
}

/* --- Buttons --- */
.btn {
  display: inline-block;
  padding: 16px 45px;
  font-weight: 700;
  font-size: 0.9rem;
  text-transform: uppercase;
  letter-spacing: 0.1em;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  transition: all var(--transition-speed, 0.3s);
  position: relative;
  overflow: hidden;
}

.btn::before {
  content: '';
  position: absolute;
  top: 50%;
  left: 50%;
  width: 0;
  height: 0;
  border-radius: 50%;
  background-color: rgba(255, 255, 255, 0.2);
  transform: translate(-50%, -50%);
  transition: width 0.6s, height 0.6s;
}

.btn:hover::before {
  width: 300px;
  height: 300px;
}

.btn--primary {
  background-color: var(--color-accent-orange, #ff5722);
  color: #fff;
  box-shadow: 0 4px 15px rgba(255, 87, 34, 0.3);
}

.btn--primary:hover {
  background-color: #e64a19;
  transform: translateY(-3px);
  box-shadow: 0 8px 25px rgba(255, 87, 34, 0.4);
}

.btn--secondary {
  background-color: transparent;
  color: #fff;
  border: 2px solid #fff;
}

.btn--secondary:hover {
  background-color: #fff;
  color: #0a0a0a;
  transform: translateY(-3px);
  box-shadow: 0 8px 25px rgba(255, 255, 255, 0.2);
}

.btn--full {
  width: 100%;
}

/* --- Sections General --- */
.section {
  padding: 120px 0;
  position: relative;
}

.section-header {
  margin-bottom: 70px;
}

.section-header.center {
  text-align: center;
}

.section-title {
  font-size: 3rem;
  font-weight: 800;
  margin-bottom: 15px;
  color: #fff;
  letter-spacing: -0.02em;
  line-height: 1.2;
}

.section-subtitle {
  font-size: 1.15rem;
  color: var(--color-text-muted);
  margin-bottom: 25px;
  font-weight: 300;
  line-height: 1.6;
}

.section-line {
  width: 80px;
  height: 4px;
  background: linear-gradient(90deg, var(--color-accent-orange), var(--color-accent-blue));
  border-radius: 2px;
}

.section-line.center {
  margin: 0 auto;
}

/* --- Stats Section --- */
.stats-section {
  padding: 80px 0;
  background-color: var(--color-bg-alt);
  border-top: 1px solid var(--color-border);
  border-bottom: 1px solid var(--color-border);
}

.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 40px;
}

.stat-card {
  text-align: center;
  padding: 40px 20px;
  background: linear-gradient(135deg, rgba(255,255,255,0.03), rgba(255,255,255,0.01));
  border-radius: 10px;
  border: 1px solid rgba(255, 255, 255, 0.05);
  transition: all 0.5s cubic-bezier(0.4, 0, 0.2, 1);
}

.stat-card:hover {
  transform: translateY(-8px);
  border-color: var(--color-accent-orange);
  box-shadow: 0 10px 40px rgba(255, 87, 34, 0.2);
}

.stat-card__icon {
  font-size: 3rem;
  margin-bottom: 15px;
  color: var(--color-accent-orange);
}

.stat-card__value {
  display: block;
  font-size: 3rem;
  font-weight: 900;
  color: var(--color-accent-orange);
  margin-bottom: 10px;
}

.stat-card__label {
  font-size: 0.95rem;
  text-transform: uppercase;
  letter-spacing: 0.1em;
  color: var(--color-text);
  font-weight: 600;
}

/* --- About Section --- */
.about {
  background-color: var(--color-bg);
}

.about-content {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 80px;
  align-items: center;
}

.about-image {
  position: relative;
  border-radius: 15px;
  overflow: hidden;
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.5);
}

.about-image img {
  width: 100%;
  height: 600px;
  object-fit: cover;
  display: block;
}

.about-text {
  padding: 20px 0;
}

.about-timeline {
  display: flex;
  flex-direction: column;
  gap: 40px;
}

.timeline-item {
  display: flex;
  gap: 30px;
  align-items: flex-start;
}

.timeline-item__number {
  font-size: 4rem;
  font-weight: 900;
  color: #fff;
  line-height: 1;
  flex-shrink: 0;
}

.timeline-item__content h3 {
  font-size: 1.5rem;
  margin-bottom: 15px;
  color: #fff;
}

.timeline-item__content p {
  color: var(--color-text-muted);
  line-height: 1.7;
  font-size: 1rem;
}

/* --- Products Section --- */
.products {
  background-color: var(--color-bg-alt);
}

.products-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 35px;
}

.product-card {
  background-color: var(--color-bg-card);
  border-radius: 12px;
  overflow: hidden;
  border: 2px solid rgba(41, 128, 185, 0.3);
  transition: all 0.5s cubic-bezier(0.4, 0, 0.2, 1);
  position: relative;
  display: flex;
  flex-direction: column;
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.3);
}

.product-card:hover {
  transform: translateY(-8px);
  border-color: var(--color-accent-blue);
  box-shadow: 0 20px 60px rgba(41, 128, 185, 0.4);
}

.product-card__image {
  height: 240px;
  background-size: cover;
  background-position: center;
  position: relative;
  overflow: hidden;
}

.product-card__overlay {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: linear-gradient(180deg, transparent 0%, rgba(0,0,0,0.8) 100%);
  transition: background 0.5s ease;
}

.product-card:hover .product-card__overlay {
  background: linear-gradient(180deg, rgba(41,128,185,0.4) 0%, rgba(0,0,0,0.9) 100%);
}

.product-card__content {
  padding: 30px;
  flex: 1;
  display: flex;
  flex-direction: column;
}

.product-card__icon {
  color: var(--color-accent-blue);
  margin-bottom: 20px;
}

.product-card__title {
  font-size: 1.4rem;
  margin-bottom: 15px;
  color: #fff;
  font-weight: 700;
}

.product-card__desc {
  color: var(--color-text-muted);
  font-size: 0.95rem;
  margin-bottom: 20px;
  line-height: 1.6;
  flex: 1;
}

.product-card__specs {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
  margin-bottom: 25px;
}

.spec-badge {
  padding: 6px 12px;
  background-color: rgba(41, 128, 185, 0.15);
  border: 1px solid rgba(41, 128, 185, 0.3);
  border-radius: 20px;
  font-size: 0.75rem;
  color: var(--color-accent-blue);
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.05em;
}

.product-card__link {
  font-size: 0.9rem;
  font-weight: 700;
  color: var(--color-accent-blue);
  display: inline-flex;
  align-items: center;
  gap: 5px;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  transition: all 0.5s cubic-bezier(0.4, 0, 0.2, 1);
}

.product-card__link:hover {
  color: var(--color-accent-orange);
  gap: 12px;
}

/* --- Process Section --- */
.process {
  background-color: var(--color-bg);
}

.process-content {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 60px;
  align-items: start;
}

.process-steps {
  display: flex;
  flex-direction: column;
  gap: 20px;
  position: sticky;
  top: 100px;
}

.process-step {
  padding: 25px;
  background-color: var(--color-bg-card);
  border: 1px solid var(--color-border);
  border-radius: 10px;
  cursor: pointer;
  transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
  display: flex;
  gap: 20px;
  align-items: flex-start;
}

.process-step:hover {
  border-color: var(--color-accent-blue);
  background-color: rgba(41, 128, 185, 0.05);
}

.process-step--active {
  border-color: var(--color-accent-orange);
  background: linear-gradient(135deg, rgba(255,87,34,0.1), rgba(41,128,185,0.05));
  box-shadow: 0 10px 30px rgba(255, 87, 34, 0.2);
}

.process-step__icon {
  color: var(--color-accent-blue);
  line-height: 1;
  flex-shrink: 0;
  transition: color 0.5s ease;
}

.process-step--active .process-step__icon {
  color: var(--color-accent-orange);
}

.process-step__info h3 {
  font-size: 1.3rem;
  margin-bottom: 10px;
  color: #fff;
}

.process-step__info p {
  color: var(--color-text-muted);
  font-size: 0.9rem;
  line-height: 1.6;
  margin-bottom: 10px;
}

.process-step__temp {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  padding: 6px 16px;
  background-color: rgba(255, 87, 34, 0.2);
  border-radius: 20px;
  color: var(--color-accent-orange);
  font-size: 0.85rem;
  font-weight: 700;
  transition: background-color 0.5s ease;
}

.process-step:hover .process-step__temp {
  background-color: rgba(255, 87, 34, 0.3);
}

.process-visual {
  position: relative;
  height: 600px;
  border-radius: 15px;
  overflow: hidden;
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.5);
}

.process-image {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-size: cover;
  background-position: center;
  opacity: 0;
  transition: opacity var(--transition-slow);
}

.process-image--active {
  opacity: 1;
}

.process-image__overlay {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: linear-gradient(135deg, rgba(0,0,0,0.4), rgba(255,87,34,0.2));
}

.process-image__temp {
  position: absolute;
  bottom: 30px;
  right: 30px;
  padding: 15px 25px;
  background-color: rgba(0, 0, 0, 0.8);
  backdrop-filter: blur(10px);
  border-radius: 10px;
  color: #fff;
  font-size: 1.2rem;
  font-weight: 700;
  border: 1px solid rgba(255, 87, 34, 0.5);
  display: flex;
  align-items: center;
  gap: 10px;
  transition: all var(--transition-speed);
  animation: pulse-temp 2s ease-in-out infinite;
}

@keyframes pulse-temp {
  0%, 100% {
    box-shadow: 0 0 20px rgba(255, 87, 34, 0.3);
  }
  50% {
    box-shadow: 0 0 30px rgba(255, 87, 34, 0.6);
  }
}

/* --- Values Section --- */
.values {
  background-color: var(--color-bg-alt);
}

.values-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
  gap: 35px;
  margin-bottom: 80px;
}

.value-card {
  padding: 40px 30px;
  background: linear-gradient(135deg, rgba(255,255,255,0.03), rgba(255,255,255,0.01));
  border: 1px solid var(--color-border);
  border-radius: 12px;
  text-align: center;
  transition: all 0.5s cubic-bezier(0.4, 0, 0.2, 1);
}

.value-card:hover {
  transform: translateY(-8px);
  border-color: var(--color-accent-blue);
  box-shadow: 0 15px 40px rgba(41, 128, 185, 0.2);
}

.value-card__icon {
  font-size: 3.5rem;
  margin-bottom: 25px;
  color: var(--color-accent-blue);
}

.value-card__title {
  font-size: 1.3rem;
  margin-bottom: 15px;
  color: #fff;
  font-weight: 700;
}

.value-card__desc {
  color: var(--color-text-muted);
  line-height: 1.7;
  font-size: 0.95rem;
}

/* --- Certifications --- */
.certifications {
  margin-bottom: 80px;
  padding: 50px;
  background-color: var(--color-bg-card);
  border-radius: 15px;
  border: 1px solid var(--color-border);
}

.certifications__title {
  text-align: center;
  font-size: 2rem;
  margin-bottom: 40px;
  color: #fff;
}

.certifications-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 25px;
}

.cert-badge {
  padding: 25px 20px;
  background-color: rgba(255, 255, 255, 0.03);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 10px;
  text-align: center;
  transition: all 0.5s cubic-bezier(0.4, 0, 0.2, 1);
}

.cert-badge:hover {
  border-color: var(--color-accent-gold);
  background-color: rgba(255, 167, 38, 0.05);
  transform: translateY(-5px);
}

.cert-badge__icon {
  font-size: 2.5rem;
  margin-bottom: 15px;
  color: var(--color-accent-gold);
}

.cert-badge__name {
  display: block;
  font-size: 1.1rem;
  font-weight: 700;
  color: var(--color-accent-gold);
  margin-bottom: 8px;
}

.cert-badge__desc {
  font-size: 0.85rem;
  color: var(--color-text-muted);
}

/* --- Clients --- */
.clients-section {
  padding: 50px;
  background-color: var(--color-bg-card);
  border-radius: 15px;
  border: 1px solid var(--color-border);
}

.clients__title {
  text-align: center;
  font-size: 2rem;
  margin-bottom: 40px;
  color: #fff;
}

.clients-grid {
  display: flex;
  flex-direction: column;
  gap: 25px;
  max-width: 700px;
  margin: 0 auto;
}

.client-item {
  position: relative;
}

.client-item:nth-child(1) .client-item__bar {
  background: linear-gradient(90deg, #ff5722, #ff7043);
  box-shadow: 0 5px 25px rgba(255, 87, 34, 0.5), inset 0 1px 0 rgba(255, 255, 255, 0.2);
}

.client-item:nth-child(2) .client-item__bar {
  background: linear-gradient(90deg, #2980b9, #3498db);
  box-shadow: 0 5px 25px rgba(41, 128, 185, 0.5), inset 0 1px 0 rgba(255, 255, 255, 0.2);
}

.client-item:nth-child(3) .client-item__bar {
  background: linear-gradient(90deg, #ffa726, #ffb74d);
  box-shadow: 0 5px 25px rgba(255, 167, 38, 0.5), inset 0 1px 0 rgba(255, 255, 255, 0.2);
}

.client-item:nth-child(4) .client-item__bar {
  background: linear-gradient(90deg, #e74c3c, #ff6b6b);
  box-shadow: 0 5px 25px rgba(231, 76, 60, 0.5), inset 0 1px 0 rgba(255, 255, 255, 0.2);
}

.client-item__bar {
  height: 55px;
  border-radius: 10px;
  transition: all var(--transition-smooth);
  position: relative;
  overflow: hidden;
}

.client-item__bar::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: linear-gradient(180deg, rgba(255,255,255,0.15) 0%, transparent 100%);
  pointer-events: none;
}

.client-item__info {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 15px 25px;
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  z-index: 1;
}

.client-item__sector {
  font-weight: 700;
  color: #fff;
  font-size: 1.05rem;
  text-shadow: 0 2px 4px rgba(0, 0, 0, 0.3);
}

.client-item__percentage {
  font-weight: 900;
  color: #fff;
  font-size: 1.4rem;
  text-shadow: 0 2px 4px rgba(0, 0, 0, 0.3);
}

/* --- Contact Section --- */
.contact {
  background-color: var(--color-bg);
}

.contact-content {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 80px;
}

.contact-details {
  display: flex;
  flex-direction: column;
  gap: 30px;
  margin-top: 40px;
}

.contact-item {
  display: flex;
  gap: 20px;
  padding: 20px;
  background-color: var(--color-bg-card);
  border: 1px solid var(--color-border);
  border-radius: 10px;
  transition: all 0.5s cubic-bezier(0.4, 0, 0.2, 1);
}

.contact-item:hover {
  border-color: var(--color-accent-orange);
}

.contact-item__icon {
  font-size: 2rem;
  flex-shrink: 0;
  color: var(--color-accent-orange);
}

.contact-item__text h4 {
  color: #fff;
  margin-bottom: 8px;
  font-size: 1.1rem;
}

.contact-item__text p {
  color: var(--color-text-muted);
  line-height: 1.6;
  font-size: 0.95rem;
}

/* --- Contact Form --- */
.contact-form {
  padding: 50px;
  background-color: var(--color-bg-card);
  border: 1px solid var(--color-border);
  border-radius: 15px;
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
}

.form-group {
  margin-bottom: 25px;
}

.form-row {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 20px;
}

.form-group label {
  display: block;
  margin-bottom: 10px;
  color: #fff;
  font-weight: 600;
  font-size: 0.9rem;
  text-transform: uppercase;
  letter-spacing: 0.05em;
}

.form-group input,
.form-group textarea {
  width: 100%;
  padding: 15px;
  background-color: rgba(255, 255, 255, 0.03);
  border: 1px solid var(--color-border);
  border-radius: 8px;
  color: #fff;
  font-family: inherit;
  font-size: 1rem;
  transition: all var(--transition-speed);
}

.form-group input:focus,
.form-group textarea:focus {
  outline: none;
  border-color: var(--color-accent-orange);
  background-color: rgba(255, 255, 255, 0.05);
  box-shadow: 0 0 0 3px rgba(255, 87, 34, 0.1);
}

.form-group textarea {
  resize: vertical;
  min-height: 120px;
}

/* --- Footer --- */
.footer {
  background-color: #050505;
  padding: 80px 0 30px;
  border-top: 1px solid var(--color-border);
}

.footer__top {
  display: grid;
  grid-template-columns: 2fr 1fr 1fr 1fr;
  gap: 60px;
  margin-bottom: 60px;
  padding-bottom: 60px;
  border-bottom: 1px solid var(--color-border);
  }
  
  .footer__brand {
  max-width: 300px;
}

.footer__desc {
  color: var(--color-text-muted);
  margin-top: 20px;
  margin-bottom: 25px;
  line-height: 1.7;
  font-size: 0.95rem;
}

.footer__social {
  display: flex;
  gap: 15px;
}

.footer__social a {
  width: 45px;
  height: 45px;
  display: flex;
  align-items: center;
  justify-content: center;
  background-color: rgba(255, 255, 255, 0.05);
  border: 1px solid var(--color-border);
  border-radius: 8px;
  font-size: 1.3rem;
  transition: all 0.5s cubic-bezier(0.4, 0, 0.2, 1);
}

.footer__social a:hover {
  background-color: var(--color-accent-orange);
  border-color: var(--color-accent-orange);
}

.footer__links-group h4 {
  color: #fff;
  margin-bottom: 25px;
  font-size: 1.1rem;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.05em;
}

.footer__links-group {
  display: flex;
    flex-direction: column;
  gap: 12px;
}

.footer__links-group a {
  color: var(--color-text-muted);
  font-size: 0.95rem;
  transition: color 0.4s ease;
  padding: 5px 0;
}

.footer__links-group a:hover {
  color: var(--color-accent-orange);
}

.footer__bottom {
  text-align: center;
  padding-top: 30px;
}

.footer__bottom p {
  color: #666;
  font-size: 0.9rem;
  margin-bottom: 5px;
}

/* --- Responsive --- */
@media (min-width: 769px) {
  .mobile-only { 
    display: none !important; 
  }
}

@media (max-width: 1024px) {
  .hero {
    background-attachment: scroll !important;
    background-size: cover;
    background-position: center center;
  }
}

@media (max-width: 768px) {
  .desktop-only { 
    display: none !important; 
  }
  
  .hero {
    background-attachment: scroll !important;
    background-size: cover;
    background-position: center center;
  }
  
  .hero__title {
    font-size: 2.5rem;
  }

  .hero__subtitle {
    font-size: 1.1rem;
  }

  .hero__cta {
    flex-direction: column;
    align-items: stretch;
  }

  .hero__badge {
    font-size: 0.75rem;
    padding: 8px 20px;
  }
  
  .section {
    padding: 60px 0;
  }

  .section-title {
    font-size: 2rem;
  }

  .section-subtitle {
    font-size: 1rem;
  }

  .stats-grid {
    grid-template-columns: 1fr;
    gap: 20px;
  }

  .about-content {
    grid-template-columns: 1fr;
    gap: 40px;
  }

  .about-image img {
    height: 400px;
  }

  .timeline-item {
    flex-direction: column;
    gap: 15px;
  }

  .timeline-item__number {
    font-size: 3rem;
  }

  .products-grid {
    grid-template-columns: 1fr;
  }

  .process-content {
    grid-template-columns: 1fr;
    gap: 40px;
  }

  .process-steps {
    position: static;
  }

  .process-visual {
    height: 400px;
  }

  .values-grid {
    grid-template-columns: 1fr;
  }

  .certifications {
    padding: 30px 20px;
  }

  .certifications-grid {
    grid-template-columns: repeat(2, 1fr);
    gap: 15px;
  }

  .clients-section {
    padding: 30px 20px;
  }

  .contact-content {
    grid-template-columns: 1fr;
    gap: 40px;
  }

  .contact-form {
    padding: 30px 20px;
  }

  .form-row {
    grid-template-columns: 1fr;
  }

  .footer__top {
    grid-template-columns: 1fr;
    gap: 40px;
  }

  .footer__brand {
    max-width: 100%;
  }
}

@media (max-width: 480px) {
  .hero__title {
    font-size: 2rem;
  }

  .section-title {
    font-size: 1.75rem;
  }

  .stat-card__value {
    font-size: 2.5rem;
  }

  .product-card__image {
    height: 200px;
  }

  .process-visual {
    height: 300px;
  }

  .certifications-grid {
    grid-template-columns: 1fr;
  }

  .btn {
    padding: 14px 30px;
    font-size: 0.85rem;
  }
}

/* --- Animations for scroll --- */
@keyframes fade-in {
  from {
    opacity: 0;
    transform: translateY(30px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

/* --- Utility classes --- */
.text-center {
  text-align: center;
}

.mt-4 {
  margin-top: 2rem;
}

.mb-4 {
  margin-bottom: 2rem;
}
</style>
