import React from 'react';
import { motion } from 'framer-motion';
import { Check } from 'lucide-react';

const Pricing = () => {
    const tiers = [
        {
            name: 'Starter',
            price: 'Free',
            description: 'Perfect for exploring local AI capabilities.',
            features: [
                'Single Node NPU-STACK',
                'Up to 5 Data Sources',
                'Basic Telemetry',
                'Community Support',
            ],
            buttonText: 'Get Started',
            popular: false,
        },
        {
            name: 'Professional',
            price: '$299',
            period: '/mo',
            description: 'For teams building production AI workflows.',
            features: [
                'Multi-Node NPU-STACK Support',
                'Unlimited Data Sources',
                'Automated Fine-Tuning Pipelines',
                'Advanced Analytics Dashboard',
                'RBAC & Security Policies',
                'Priority Email Support',
            ],
            buttonText: 'Start Free Trial',
            popular: true,
        },
        {
            name: 'Enterprise',
            price: 'Custom',
            description: 'Uncompromising scale and dedicated support.',
            features: [
                'Unlimited Everything',
                'Air-Gapped Deployments',
                'Custom Agent Integration',
                'Dedicated Success Manager',
                '24/7 Phone Support',
                'SLA Guarantees',
            ],
            buttonText: 'Contact Sales',
            popular: false,
        },
    ];

    return (
        <section id="pricing" className="py-24 relative z-10 bg-gradient-to-b from-transparent to-[#0a0a0a]/50">
            <div className="container mx-auto px-6 md:px-12">
                <div className="text-center mb-16">
                    <h2 className="text-3xl md:text-5xl font-bold tracking-tight text-white mb-4">
                        Simple, Transparent Pricing
                    </h2>
                    <p className="text-gray-400 max-w-2xl mx-auto text-lg leading-relaxed">
                        Scale your AI infrastructure confidently with plans designed for extreme flexibility.
                    </p>
                </div>

                <div className="grid grid-cols-1 md:grid-cols-3 gap-8 max-w-6xl mx-auto">
                    {tiers.map((tier, index) => (
                        <motion.div
                            key={index}
                            initial={{ opacity: 0, scale: 0.95 }}
                            whileInView={{ opacity: 1, scale: 1 }}
                            viewport={{ once: true }}
                            transition={{ duration: 0.5, delay: index * 0.1 }}
                            className={`relative p-8 rounded-3xl bg-white/5 border ${tier.popular ? 'border-blue-500 shadow-2xl shadow-blue-500/10' : 'border-white/5'
                                } flex flex-col`}
                        >
                            {tier.popular && (
                                <div className="absolute top-0 left-1/2 -translate-x-1/2 -translate-y-1/2 px-4 py-1 bg-gradient-to-r from-blue-600 to-indigo-600 rounded-full text-xs font-bold text-white uppercase tracking-wider">
                                    Most Popular
                                </div>
                            )}

                            <div className="mb-8">
                                <h3 className="text-2xl font-semibold text-white mb-2">{tier.name}</h3>
                                <p className="text-gray-400 h-10">{tier.description}</p>
                            </div>

                            <div className="mb-8">
                                <span className="text-5xl font-bold text-white">{tier.price}</span>
                                {tier.period && <span className="text-gray-400"> {tier.period}</span>}
                            </div>

                            <ul className="space-y-4 mb-8 flex-grow">
                                {tier.features.map((feature, fIndex) => (
                                    <li key={fIndex} className="flex items-start gap-3 text-gray-300">
                                        <Check className="w-5 h-5 text-blue-500 shrink-0" />
                                        <span>{feature}</span>
                                    </li>
                                ))}
                            </ul>

                            <button
                                className={`w-full py-4 rounded-xl font-medium transition-all ${tier.popular
                                        ? 'bg-blue-600 hover:bg-blue-500 text-white'
                                        : 'bg-white/5 hover:bg-white/10 text-white border border-white/10'
                                    }`}
                            >
                                {tier.buttonText}
                            </button>
                        </motion.div>
                    ))}
                </div>
            </div>
        </section>
    );
};

export default Pricing;
