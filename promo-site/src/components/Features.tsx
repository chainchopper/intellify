import React from 'react';
import { motion } from 'framer-motion';
import { Database, Zap, Shield, Cpu, Layers, Workflow } from 'lucide-react';

const Features = () => {
    const features = [
        {
            icon: <Database className="w-6 h-6 text-blue-400" />,
            title: 'Local Ingestion Engine',
            description: 'Connect internal wikis, Google Drive, and Notion securely. Data never leaves your network.',
        },
        {
            icon: <Cpu className="w-6 h-6 text-indigo-400" />,
            title: 'NPU-STACK Integration',
            description: 'Orchestrate LLM fine-tuning natively on your local GPUs or high-performance clusters.',
        },
        {
            icon: <Workflow className="w-6 h-6 text-purple-400" />,
            title: 'Automated Pipelines',
            description: 'From raw PDFs to an interactive AI agent in under 20 minutes with zero coding required.',
        },
        {
            icon: <Shield className="w-6 h-6 text-emerald-400" />,
            title: 'Enterprise Privacy',
            description: '100% data sovereignty. Your customized models belong to you and operate offline if needed.',
        },
        {
            icon: <Layers className="w-6 h-6 text-orange-400" />,
            title: 'Multi-Agent Ecosystems',
            description: 'Deploy specialized agents for HR, Finance, and Legal that collaborate on complex tasks.',
        },
        {
            icon: <Zap className="w-6 h-6 text-yellow-400" />,
            title: 'Real-Time Telemetry',
            description: 'Monitor GPU utilization, model performance, and API latency through our unified dashboard.',
        },
    ];

    return (
        <section id="platform" className="py-24 relative z-10">
            <div className="container mx-auto px-6 md:px-12">
                <div className="text-center mb-16">
                    <h2 className="text-3xl md:text-5xl font-bold tracking-tight text-white mb-4">
                        The Missing Link in <span className="text-blue-500">Enterprise AI</span>
                    </h2>
                    <p className="text-gray-400 max-w-2xl mx-auto text-lg leading-relaxed">
                        Intellify bridges the gap between raw unstructured data and powerful, locally hosted large language models.
                    </p>
                </div>

                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                    {features.map((feature, index) => (
                        <motion.div
                            key={index}
                            initial={{ opacity: 0, y: 20 }}
                            whileInView={{ opacity: 1, y: 0 }}
                            viewport={{ once: true, margin: '-50px' }}
                            transition={{ duration: 0.5, delay: index * 0.1 }}
                            className="p-8 rounded-2xl bg-white/5 border border-white/5 hover:bg-white/10 hover:border-white/10 transition-all group"
                        >
                            <div className="w-12 h-12 rounded-xl bg-white/5 flex items-center justify-center mb-6 group-hover:scale-110 group-hover:bg-white/10 transition-all">
                                {feature.icon}
                            </div>
                            <h3 className="text-xl font-semibold text-white mb-3">
                                {feature.title}
                            </h3>
                            <p className="text-gray-400 leading-relaxed">
                                {feature.description}
                            </p>
                        </motion.div>
                    ))}
                </div>
            </div>
        </section>
    );
};

export default Features;
