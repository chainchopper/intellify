/* eslint-disable react-hooks/set-state-in-effect */
import './index.css';
import { useState, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { Play, Pause, XCircle, Activity, Server, UploadCloud, Cpu, Database, ShieldCheck } from 'lucide-react';
import OnboardingWizard from './OnboardingWizard';

const API_BASE = "http://127.0.0.1:8080/api";

export default function App() {
  const [tasks, setTasks] = useState<Record<string, Record<string, string>>>({});
  const [recs, setRecs] = useState<Record<string, string>[]>([]);
  const [showWizard, setShowWizard] = useState(true);



  async function fetchTasks() {
    try {
      const res = await fetch(`${API_BASE}/tasks`);
      const data = await res.json();
      setTasks(data.tasks || {});
    } catch { console.error("Could not fetch tasks") }
  };

  const loadMockRecommendations = async () => {
    try {
      const res = await fetch(`${API_BASE}/recommendations`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          category: "financial_reports",
          file_format: ".pdf",
          asset_count: 154
        })
      });
      const data = await res.json();
      setRecs(data.recommendations || []);
    } catch (e) { console.error(e) }
  };

  async function startTask(serviceId: string) {
    try {
      await fetch(`${API_BASE}/tasks/opt-in?service_id=${serviceId}`, { method: "POST" });
      fetchTasks();
    } catch { /* ignore */ }
  };

  async function controlTask(taskId: string, action: string) {
    try {
      await fetch(`${API_BASE}/tasks/control`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ task_id: taskId, action })
      });
      fetchTasks();
    } catch { /* ignore */ }
  };

  const handleWizardComplete = (data: unknown) => {
    console.log("Onboarding Data:", data);
    setShowWizard(false);
    loadMockRecommendations();
  };


  useEffect(() => {
    fetchTasks();
    const interval = setInterval(fetchTasks, 3000);
    return () => clearInterval(interval);
  }, []);

  return (
    <div className="min-h-screen bg-[#0a0f18] text-slate-300 font-sans selection:bg-indigo-500/30">

      {showWizard && <OnboardingWizard onComplete={handleWizardComplete} />}

      {/* Header */}
      <header className="border-b border-white/5 bg-[#0e1420]/80 backdrop-blur-md sticky top-0 z-50">
        <div className="max-w-7xl mx-auto px-6 h-16 flex items-center justify-between">
          <div className="flex items-center gap-3">
            <div className="w-8 h-8 rounded-lg bg-gradient-to-tr from-indigo-500 to-cyan-400 flex items-center justify-center shadow-[0_0_15px_rgba(99,102,241,0.4)]">
              <Activity className="w-5 h-5 text-white" />
            </div>
            <h1 className="text-xl font-bold tracking-wide text-white">Intellify <span className="text-slate-500 font-medium text-sm ml-2">Enterprise Hub</span></h1>
          </div>
          <div className="flex items-center gap-4 text-sm font-medium">
            <div className="flex items-center gap-2 text-emerald-400 bg-emerald-400/10 px-3 py-1.5 rounded-full border border-emerald-400/20">
              <ShieldCheck className="w-4 h-4" /> Securing Local Assets
            </div>
          </div>
        </div>
      </header>

      <main className="max-w-7xl mx-auto px-6 py-8 grid grid-cols-12 gap-8">

        {/* Left Col: Recommendations */}
        <div className="col-span-12 lg:col-span-5 space-y-6">
          <div className="flex items-center justify-between">
            <h2 className="text-lg font-semibold text-white flex items-center gap-2">
              <Database className="w-5 h-5 text-indigo-400" />
              Ingestion Recommendations
            </h2>
            <button
              onClick={loadMockRecommendations}
              className="text-xs bg-indigo-500 hover:bg-indigo-400 text-white px-3 py-1.5 rounded-md transition-colors font-medium">
              Scan Local Drive
            </button>
          </div>

          <AnimatePresence>
            {recs.length === 0 ? (
              <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} className="border border-white/5 bg-white/[0.02] rounded-xl p-8 text-center">
                <UploadCloud className="w-10 h-10 text-slate-600 mx-auto mb-3" />
                <p className="text-slate-400 text-sm">No assets scanned yet.</p>
              </motion.div>
            ) : (
              recs.map((rec, idx) => (
                <motion.div
                  initial={{ opacity: 0, y: 10 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ delay: idx * 0.1 }}
                  key={rec.service_id}
                  className="group border border-white/5 hover:border-indigo-500/30 bg-[#121927] rounded-xl p-5 shadow-lg transition-all"
                >
                  <div className="flex items-start justify-between">
                    <div>
                      <h3 className="text-white font-medium text-base mb-1">{rec.name}</h3>
                      <p className="text-xs text-slate-400 font-mono mb-3">{rec.container}</p>
                    </div>
                    <button
                      onClick={() => startTask(rec.service_id)}
                      className="opacity-0 group-hover:opacity-100 transition-opacity bg-indigo-500/10 hover:bg-indigo-500 text-indigo-400 hover:text-white p-2 rounded-lg"
                    >
                      <Play className="w-4 h-4" fill="currentColor" />
                    </button>
                  </div>
                  <p className="text-sm text-slate-500 leading-relaxed">{rec.description}</p>
                </motion.div>
              ))
            )}
          </AnimatePresence>
        </div>

        {/* Right Col: Active Tasks */}
        <div className="col-span-12 lg:col-span-7 space-y-6">
          <h2 className="text-lg font-semibold text-white flex items-center gap-2">
            <Server className="w-5 h-5 text-cyan-400" />
            Active Workflows (MCP Hub)
          </h2>

          <div className="space-y-4">
            {Object.entries(tasks).length === 0 ? (
              <div className="border border-white/5 bg-white/[0.02] rounded-xl p-8 text-center">
                <Cpu className="w-10 h-10 text-slate-600 mx-auto mb-3" />
                <p className="text-slate-400 text-sm">No active tasks.</p>
              </div>
            ) : (
              Object.entries(tasks).map(([taskId, task]) => (
                <motion.div
                  key={taskId}
                  initial={{ opacity: 0, x: 20 }}
                  animate={{ opacity: 1, x: 0 }}
                  className="border border-white/10 bg-[#121927]/80 backdrop-blur-sm rounded-xl p-5 shadow-xl relative overflow-hidden"
                >
                  {/* Progress Bar BG */}
                  {task.status === "STARTING" && (
                    <div className="absolute top-0 left-0 h-1 bg-indigo-500 w-1/4 animate-pulse" />
                  )}
                  {task.status === "INGESTING" && (
                    <div className="absolute top-0 left-0 h-1 bg-emerald-500 w-3/4" />
                  )}

                  <div className="flex items-center justify-between mb-2">
                    <span className="text-xs font-mono text-slate-400">{taskId}</span>
                    <span className={`text-xs px-2 py-1 rounded-md font-bold ${task.status === "INGESTING" ? "bg-emerald-500/20 text-emerald-400" :
                      task.status === "PAUSED" ? "bg-amber-500/20 text-amber-400" :
                        task.status === "CANCELLED" ? "bg-rose-500/20 text-rose-400" :
                          "bg-indigo-500/20 text-indigo-400"
                      }`}>
                      {task.status}
                    </span>
                  </div>

                  <h3 className="text-white font-medium text-lg mb-4">{task.service_id.toUpperCase()}</h3>

                  <div className="flex items-center gap-2 mt-4">
                    {task.status !== "PAUSED" && task.status !== "CANCELLED" ? (
                      <button
                        onClick={() => controlTask(taskId, "pause")}
                        className="flex items-center gap-1 text-xs bg-amber-500/10 hover:bg-amber-500/20 text-amber-500 px-3 py-1.5 rounded-md transition-colors"
                      >
                        <Pause className="w-3 h-3" /> Pause
                      </button>
                    ) : (
                      <button
                        onClick={() => controlTask(taskId, "resume")}
                        className="flex items-center gap-1 text-xs bg-emerald-500/10 hover:bg-emerald-500/20 text-emerald-500 px-3 py-1.5 rounded-md transition-colors"
                      >
                        <Play className="w-3 h-3" /> Resume
                      </button>
                    )}
                    <button
                      onClick={() => controlTask(taskId, "cancel")}
                      className="flex items-center gap-1 text-xs bg-rose-500/10 hover:bg-rose-500/20 text-rose-500 px-3 py-1.5 rounded-md transition-colors"
                    >
                      <XCircle className="w-3 h-3" /> Cancel
                    </button>
                  </div>
                </motion.div>
              ))
            )}
          </div>
        </div>

      </main>
    </div>
  );
}
