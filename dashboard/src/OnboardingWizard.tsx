import { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { ShieldCheck, HardDrive, Network, FileSearch, ArrowRight, CheckCircle2 } from 'lucide-react';

interface Props {
    onComplete: (data: unknown) => void;
}

export default function OnboardingWizard({ onComplete }: Props) {
    const [step, setStep] = useState(0);
    const [paths, setPaths] = useState("");
    const [lanScan, setLanScan] = useState(true);

    const steps = [
        {
            title: "Welcome to Intellify",
            desc: "Your Enterprise AI Onboarding Journey starts here. We will configure your local environment, scan your assets, and recommend custom AI models tailored to your business data.",
            icon: <ShieldCheck className="w-12 h-12 text-indigo-400 mx-auto" />,
        },
        {
            title: "Local Asset Discovery",
            desc: "Provide the absolute paths to the local drives or network shares you want Intellify to index. We only scan metadata; raw files never leave your premise.",
            icon: <HardDrive className="w-12 h-12 text-emerald-400 mx-auto" />,
            content: (
                <div className="mt-4">
                    <label className="block text-sm font-medium text-slate-300 mb-2">Watch Folders (one per line)</label>
                    <textarea
                        value={paths}
                        onChange={e => setPaths(e.target.value)}
                        placeholder="C:\Finance\n\\Server\HR_Archive"
                        className="w-full bg-[#0a0f18] border border-white/10 rounded-lg p-3 text-sm text-slate-300 focus:border-indigo-500 outline-none resize-none h-24"
                    />
                </div>
            )
        },
        {
            title: "Hardware & LAN Mapping",
            desc: "Intellify can scan your local subnet to discover available compute endpoints, GPUs, and network hardware to optimize your deployment architecture.",
            icon: <Network className="w-12 h-12 text-cyan-400 mx-auto" />,
            content: (
                <div className="mt-6 flex items-center justify-between bg-white/[0.02] border border-white/5 p-4 rounded-lg cursor-pointer hover:border-white/10" onClick={() => setLanScan(!lanScan)}>
                    <div>
                        <p className="text-sm font-medium text-white">Perform Subnet Scan</p>
                        <p className="text-xs text-slate-400 mt-1">Discover available compute nodes on 192.168.x.x</p>
                    </div>
                    <div className={`w-10 h-6 rounded-full transition-colors flex items-center px-1 ${lanScan ? 'bg-indigo-500' : 'bg-slate-700'}`}>
                        <div className={`w-4 h-4 rounded-full bg-white transition-transform ${lanScan ? 'translate-x-4' : 'translate-x-0'}`} />
                    </div>
                </div>
            )
        },
        {
            title: "Initialize Scanning",
            desc: "Intellify Local Agent is ready to deploy. It will generate `asset_metadata.json` for all discovered assets, enabling the Recommendation Engine to formulate your AI pipeline.",
            icon: <FileSearch className="w-12 h-12 text-purple-400 mx-auto" />
        }
    ];

    const handleNext = () => {
        if (step < steps.length - 1) {
            setStep(step + 1);
        } else {
            onComplete({ paths: paths.split('\n').filter(p => p.trim()), lanScan });
        }
    };

    return (
        <div className="fixed inset-0 z-50 bg-[#0a0f18]/90 backdrop-blur-xl flex items-center justify-center p-6">
            <motion.div
                initial={{ opacity: 0, scale: 0.95, y: 20 }}
                animate={{ opacity: 1, scale: 1, y: 0 }}
                className="max-w-xl w-full bg-[#121927] border border-white/10 rounded-2xl shadow-2xl overflow-hidden shadow-indigo-500/10"
            >
                {/* Progress Bar */}
                <div className="h-1.5 w-full bg-white/5">
                    <motion.div
                        className="h-full bg-gradient-to-r from-indigo-500 to-cyan-400"
                        initial={{ width: 0 }}
                        animate={{ width: `${((step + 1) / steps.length) * 100}%` }}
                        transition={{ ease: "easeInOut" }}
                    />
                </div>

                <div className="p-10 text-center">
                    <AnimatePresence mode="wait">
                        <motion.div
                            key={step}
                            initial={{ opacity: 0, x: 20 }}
                            animate={{ opacity: 1, x: 0 }}
                            exit={{ opacity: 0, x: -20 }}
                            transition={{ duration: 0.2 }}
                        >
                            <div className="mb-6">{steps[step].icon}</div>
                            <h2 className="text-2xl font-bold text-white mb-3">{steps[step].title}</h2>
                            <p className="text-slate-400 text-sm leading-relaxed max-w-sm mx-auto">
                                {steps[step].desc}
                            </p>
                            {steps[step].content && (
                                <div className="mt-8 text-left max-w-sm mx-auto">
                                    {steps[step].content}
                                </div>
                            )}
                        </motion.div>
                    </AnimatePresence>

                    <div className="mt-12 flex items-center justify-center gap-4">
                        {step > 0 && (
                            <button
                                onClick={() => setStep(step - 1)}
                                className="px-6 py-2.5 rounded-lg text-sm font-medium text-slate-400 hover:text-white hover:bg-white/5 transition-colors"
                            >
                                Back
                            </button>
                        )}
                        <button
                            onClick={handleNext}
                            className="flex items-center gap-2 px-6 py-2.5 rounded-lg text-sm font-medium bg-indigo-500 hover:bg-indigo-400 text-white shadow-lg shadow-indigo-500/20 transition-all"
                        >
                            {step === steps.length - 1 ? (
                                <>Deploy Agent <CheckCircle2 className="w-4 h-4" /></>
                            ) : (
                                <>Continue <ArrowRight className="w-4 h-4" /></>
                            )}
                        </button>
                    </div>
                </div>
            </motion.div>
        </div>
    );
}
