
import { BrainCircuit } from 'lucide-react';

const Footer = () => {
    return (
        <footer className="border-t border-white/10 py-12 bg-[#0a0a0a]">
            <div className="container mx-auto px-6 md:px-12 grid grid-cols-1 md:grid-cols-4 gap-8">

                <div className="md:col-span-1">
                    <div className="flex items-center gap-2 mb-4">
                        <BrainCircuit className="w-6 h-6 text-blue-500" />
                        <span className="text-xl font-bold tracking-tight text-white">
                            Intellify
                        </span>
                    </div>
                    <p className="text-gray-400 text-sm">
                        Bridging the gap between raw unstructured data and powerful, locally hosted large language models.
                    </p>
                </div>

                <div>
                    <h4 className="text-white font-semibold mb-4">Product</h4>
                    <ul className="space-y-2 text-sm text-gray-400">
                        <li><a href="#" className="hover:text-white transition-colors">Platform</a></li>
                        <li><a href="#" className="hover:text-white transition-colors">NPU-STACK Integration</a></li>
                        <li><a href="#" className="hover:text-white transition-colors">Pricing</a></li>
                        <li><a href="#" className="hover:text-white transition-colors">Documentation</a></li>
                    </ul>
                </div>

                <div>
                    <h4 className="text-white font-semibold mb-4">Company</h4>
                    <ul className="space-y-2 text-sm text-gray-400">
                        <li><a href="#" className="hover:text-white transition-colors">About</a></li>
                        <li><a href="#" className="hover:text-white transition-colors">Blog</a></li>
                        <li><a href="#" className="hover:text-white transition-colors">Careers</a></li>
                        <li><a href="#" className="hover:text-white transition-colors">Contact</a></li>
                    </ul>
                </div>

                <div>
                    <h4 className="text-white font-semibold mb-4">Legal</h4>
                    <ul className="space-y-2 text-sm text-gray-400">
                        <li><a href="#" className="hover:text-white transition-colors">Privacy Policy</a></li>
                        <li><a href="#" className="hover:text-white transition-colors">Terms of Service</a></li>
                        <li><a href="#" className="hover:text-white transition-colors">Cookie Policy</a></li>
                    </ul>
                </div>

            </div>

            <div className="container mx-auto px-6 md:px-12 mt-12 pt-8 border-t border-white/5 flex flex-col md:flex-row justify-between items-center text-sm text-gray-500">
                <p>&copy; {new Date().getFullYear()} Intellify. All rights reserved.</p>
                <div className="flex gap-4 mt-4 md:mt-0">
                    <a href="#" className="hover:text-white transition-colors">Twitter</a>
                    <a href="#" className="hover:text-white transition-colors">GitHub</a>
                    <a href="#" className="hover:text-white transition-colors">Discord</a>
                </div>
            </div>
        </footer>
    );
};

export default Footer;
