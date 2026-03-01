import React from 'react';
import { motion } from 'framer-motion';

const Showcase = () => {
    return (
        <section id="npu-stack" className="py-24 relative z-10 overflow-hidden">
            <div className="container mx-auto px-6 md:px-12">
                <div className="relative rounded-3xl bg-gradient-to-b from-blue-900/20 to-transparent border border-blue-500/20 p-8 md:p-16 overflow-hidden">

                    <div className="absolute top-0 right-0 w-[800px] h-[800px] bg-blue-500/10 rounded-full blur-[100px] -translate-y-1/2 translate-x-1/3 pointer-events-none"></div>

                    <div className="grid grid-cols-1 lg:grid-cols-2 gap-12 items-center relative z-10">
                        <div>
                            <motion.div
                                initial={{ opacity: 0, x: -30 }}
                                whileInView={{ opacity: 1, x: 0 }}
                                viewport={{ once: true }}
                                transition={{ duration: 0.6 }}
                            >
                                <div className="inline-block px-4 py-1.5 rounded-full bg-indigo-500/10 border border-indigo-500/20 text-indigo-400 text-sm font-semibold mb-6">
                                    Powered by NPU-STACK
                                </div>
                                <h2 className="text-3xl md:text-5xl font-bold tracking-tight text-white mb-6">
                                    Fine-Tuning, Demystified.
                                </h2>
                                <p className="text-xl text-gray-300 mb-8 leading-relaxed">
                                    Intellify natively integrates with the NPU-STACK ecosystem. Forget command line arguments and complex dependency conflicts.
                                    Just point, click, and let our orchestration engine handle the rest.
                                </p>
                                <ul className="space-y-4">
                                    {[
                                        'Automatic Dataset Formatting via Docling',
                                        'Direct Hardware Allocation and Management',
                                        'Zero-Downtime Agent Deployment'
                                    ].map((item, i) => (
                                        <li key={i} className="flex items-center gap-3 text-gray-300">
                                            <div className="w-6 h-6 rounded-full bg-blue-500/20 flex items-center justify-center border border-blue-500/30">
                                                <div className="w-2 h-2 rounded-full bg-blue-400"></div>
                                            </div>
                                            {item}
                                        </li>
                                    ))}
                                </ul>
                            </motion.div>
                        </div>

                        <motion.div
                            initial={{ opacity: 0, scale: 0.9 }}
                            whileInView={{ opacity: 1, scale: 1 }}
                            viewport={{ once: true }}
                            transition={{ duration: 0.6, delay: 0.2 }}
                            className="relative rounded-2xl border border-white/10 bg-[#0f1219]/80 backdrop-blur-xl shadow-2xl p-6 aspect-video flex flex-col overflow-hidden"
                        >
                            {/* Mock Dashboard UI */}
                            <div className="flex items-center gap-2 mb-6 border-b border-white/10 pb-4">
                                <div className="w-3 h-3 rounded-full bg-red-500/80"></div>
                                <div className="w-3 h-3 rounded-full bg-yellow-500/80"></div>
                                <div className="w-3 h-3 rounded-full bg-green-500/80"></div>
                            </div>

                            <div className="flex-1 flex gap-4">
                                <div className="w-1/3 flex flex-col gap-3">
                                    <div className="h-8 bg-white/5 rounded-md w-full animate-pulse"></div>
                                    <div className="h-24 bg-blue-500/10 border border-blue-500/20 rounded-md w-full relative overflow-hidden flex items-center justify-center">
                                        <span className="text-blue-400 text-sm font-medium">Training Active</span>
                                        <div className="absolute top-0 left-0 h-1 bg-blue-500 w-2/3 animate-[pulse_2s_ease-in-out_infinite]"></div>
                                    </div>
                                    <div className="h-8 bg-white/5 rounded-md w-full animate-pulse opacity-50"></div>
                                </div>
                                <div className="flex-1 bg-white/5 rounded-md border border-white/5 p-4 flex flex-col gap-3">
                                    <div className="h-4 bg-white/10 rounded w-1/3"></div>
                                    <div className="flex-1 flex items-end gap-2 pb-2">
                                        {[40, 60, 45, 80, 55, 90, 70, 100].map((h, i) => (
                                            <div key={i} className="flex-1 bg-indigo-500/50 rounded-t-sm" style={{ height: `${h}%` }}></div>
                                        ))}
                                    </div>
                                </div>
                            </div>
                        </motion.div>

                    </div>
                </div>
            </div>
        </section>
    );
};

export default Showcase;
