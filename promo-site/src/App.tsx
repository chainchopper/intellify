import React from 'react';
import Navbar from './components/Navbar';
import Hero from './components/Hero';
import Features from './components/Features';
import Showcase from './components/Showcase';
import Pricing from './components/Pricing';
import Footer from './components/Footer';

function App() {
  return (
    <div className="min-h-screen bg-[#0a0a0a] text-white selection:bg-blue-500/30 font-sans overflow-x-hidden">
      <div className="fixed inset-0 z-[-1] bg-[radial-gradient(ellipse_at_top,_var(--tw-gradient-stops))] from-blue-900/20 via-[#0a0a0a] to-[#0a0a0a]"></div>
      <Navbar />
      <main>
        <Hero />
        <Features />
        <Showcase />
        <Pricing />
      </main>
      <Footer />
    </div>
  );
}

export default App;
