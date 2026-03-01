import React, { useState, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { BrainCircuit, Menu, X, ArrowRight } from 'lucide-react';

const Navbar = () => {
    const [scrolled, setScrolled] = useState(false);
    const [mobileMenuOpen, setMobileMenuOpen] = useState(false);

    useEffect(() => {
        const handleScroll = () => {
            setScrolled(window.scrollY > 50);
        };
        window.addEventListener('scroll', handleScroll);
        return () => window.removeEventListener('scroll', handleScroll);
    }, []);

    return (
        <header
            className={`fixed top-0 w-full z-50 transition-all duration-300 ${scrolled
                    ? 'bg-[#0a0a0a]/80 backdrop-blur-md border-b border-white/5 py-4'
                    : 'bg-transparent py-6'
                }`}
        >
            <div className="container mx-auto px-6 md:px-12 flex justify-between items-center">
                <div className="flex items-center gap-2">
                    <div className="bg-blue-600 p-2 rounded-lg">
                        <BrainCircuit className="w-6 h-6 text-white" />
                    </div>
                    <span className="text-xl font-bold tracking-tight text-white">
                        Intellify
                    </span>
                </div>

                <nav className="hidden md:flex items-center gap-8">
                    {['Platform', 'Solutions', 'NPU-STACK', 'Pricing'].map((item) => (
                        <a
                            key={item}
                            href={`#${item.toLowerCase()}`}
                            className="text-sm font-medium text-gray-300 hover:text-white transition-colors"
                        >
                            {item}
                        </a>
                    ))}
                    <a
                        href="http://localhost:5175"
                        className="group flex items-center gap-2 px-5 py-2.5 bg-white/5 hover:bg-white/10 border border-white/10 rounded-full text-sm font-medium transition-all"
                    >
                        Launch Dashboard
                        <ArrowRight className="w-4 h-4 group-hover:translate-x-1 transition-transform" />
                    </a>
                </nav>

                <button
                    className="md:hidden text-white"
                    onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
                >
                    {mobileMenuOpen ? <X /> : <Menu />}
                </button>
            </div>

            {/* Mobile Menu */}
            <AnimatePresence>
                {mobileMenuOpen && (
                    <motion.div
                        initial={{ opacity: 0, y: -20 }}
                        animate={{ opacity: 1, y: 0 }}
                        exit={{ opacity: 0, y: -20 }}
                        className="absolute top-16 left-0 w-full bg-[#0f1219] border-b border-white/10 p-6 flex flex-col gap-4 shadow-xl"
                    >
                        {['Platform', 'Solutions', 'NPU-STACK', 'Pricing'].map((item) => (
                            <a
                                key={item}
                                href={`#${item.toLowerCase()}`}
                                className="text-base font-medium text-gray-300 hover:text-white transition-colors"
                            >
                                {item}
                            </a>
                        ))}
                    </motion.div>
                )}
            </AnimatePresence>
        </header>
    );
};

export default Navbar;
