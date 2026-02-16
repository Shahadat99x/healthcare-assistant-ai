"use client";

import { useState, useEffect, useCallback } from "react";
import {
  Activity,
  Server,
  Database,
  ScanEye,
  Brain,
  RefreshCw,
  ChevronDown,
  ChevronUp,
  CheckCircle2,
  XCircle,
  AlertTriangle,
  ExternalLink,
} from "lucide-react";
import Link from "next/link";

// ─── Types ────────────────────────────────────────────────────────────────────

interface Check {
  ok: boolean;
  detail: string;
}

interface ReadyResponse {
  status: "ready" | "not_ready";
  checks: {
    ollama: Check;
    rag_index: Check;
    ocr: Check;
  };
}

interface HealthResponse {
  status: string;
  service: string;
  ollama_connected: boolean;
  rag_index_loaded: boolean;
}

type FetchState = "loading" | "ok" | "degraded" | "down";

// ─── Helpers ──────────────────────────────────────────────────────────────────

function stateColor(state: FetchState) {
  switch (state) {
    case "ok":
      return "text-emerald-500";
    case "degraded":
      return "text-amber-500";
    case "down":
      return "text-red-500";
    default:
      return "text-neutral-400";
  }
}

function stateBg(state: FetchState) {
  switch (state) {
    case "ok":
      return "bg-emerald-500/10 border-emerald-500/30";
    case "degraded":
      return "bg-amber-500/10 border-amber-500/30";
    case "down":
      return "bg-red-500/10 border-red-500/30";
    default:
      return "bg-neutral-500/10 border-neutral-500/30";
  }
}

function StateIcon({ state, size = 20 }: { state: FetchState; size?: number }) {
  switch (state) {
    case "ok":
      return <CheckCircle2 size={size} className="text-emerald-500" />;
    case "degraded":
      return <AlertTriangle size={size} className="text-amber-500" />;
    case "down":
      return <XCircle size={size} className="text-red-500" />;
    default:
      return (
        <RefreshCw size={size} className="text-neutral-400 animate-spin" />
      );
  }
}

function stateLabel(state: FetchState) {
  switch (state) {
    case "ok":
      return "Operational";
    case "degraded":
      return "Degraded";
    case "down":
      return "Unreachable";
    default:
      return "Checking…";
  }
}

// ─── Sub-components ───────────────────────────────────────────────────────────

function CheckCard({
  label,
  icon,
  check,
}: {
  label: string;
  icon: React.ReactNode;
  check: Check | null;
}) {
  const state: FetchState =
    check === null ? "loading" : check.ok ? "ok" : "degraded";

  return (
    <div
      className={`rounded-2xl border p-5 transition-all duration-300 ${stateBg(state)}`}
    >
      <div className="flex items-start justify-between gap-3">
        <div className="flex items-center gap-3">
          <div className="p-2 rounded-xl bg-white/60 dark:bg-neutral-800/60 shadow-sm">
            {icon}
          </div>
          <div>
            <p className="font-semibold text-sm text-neutral-900 dark:text-neutral-100">
              {label}
            </p>
            <p className="text-xs text-neutral-500 dark:text-neutral-400 mt-0.5 max-w-[260px] break-words">
              {check?.detail ?? "Checking…"}
            </p>
          </div>
        </div>
        <StateIcon state={state} />
      </div>
    </div>
  );
}

// ─── Main Page ────────────────────────────────────────────────────────────────

export default function StatusPage() {
  const [health, setHealth] = useState<HealthResponse | null>(null);
  const [ready, setReady] = useState<ReadyResponse | null>(null);
  const [apiDown, setApiDown] = useState(false);
  const [refreshing, setRefreshing] = useState(false);
  const [jsonOpen, setJsonOpen] = useState(false);
  const [lastCheck, setLastCheck] = useState<string>("");

  const apiBase =
    process.env.NEXT_PUBLIC_API_BASE_URL || "http://127.0.0.1:8000";

  const fetchStatus = useCallback(async () => {
    setRefreshing(true);
    setApiDown(false);

    try {
      const [hRes, rRes] = await Promise.allSettled([
        fetch(`${apiBase}/health`, { cache: "no-store" }),
        fetch(`${apiBase}/ready`, { cache: "no-store" }),
      ]);

      if (hRes.status === "fulfilled" && hRes.value.ok) {
        setHealth(await hRes.value.json());
      } else {
        setHealth(null);
        setApiDown(true);
      }

      if (rRes.status === "fulfilled") {
        setReady(await rRes.value.json());
      } else {
        setReady(null);
        setApiDown(true);
      }
    } catch {
      setApiDown(true);
      setHealth(null);
      setReady(null);
    } finally {
      setRefreshing(false);
      setLastCheck(new Date().toLocaleTimeString());
    }
  }, [apiBase]);

  useEffect(() => {
    fetchStatus();
    const id = setInterval(fetchStatus, 30_000);
    return () => clearInterval(id);
  }, [fetchStatus]);

  // Determine overall state
  let overall: FetchState = "loading";
  if (apiDown) {
    overall = "down";
  } else if (ready) {
    overall = ready.status === "ready" ? "ok" : "degraded";
  }

  return (
    <div className="min-h-screen bg-neutral-50 dark:bg-neutral-950 text-neutral-900 dark:text-neutral-100 transition-colors">
      {/* Header */}
      <header className="sticky top-0 z-10 flex items-center justify-between border-b border-neutral-200 dark:border-neutral-800 bg-white/80 dark:bg-neutral-950/80 backdrop-blur px-4 sm:px-6 py-3">
        <div className="flex items-center gap-3">
          <Activity size={20} className="text-blue-600" />
          <h1 className="text-lg font-bold tracking-tight">System Status</h1>
        </div>
        <div className="flex items-center gap-3">
          <Link
            href="/chat"
            className="text-xs font-medium text-blue-600 hover:text-blue-700 dark:text-blue-400 dark:hover:text-blue-300 flex items-center gap-1 transition"
          >
            Chat <ExternalLink size={12} />
          </Link>
          <button
            onClick={fetchStatus}
            disabled={refreshing}
            className="inline-flex items-center gap-1.5 text-xs font-semibold rounded-xl border border-neutral-200 dark:border-neutral-700 bg-white dark:bg-neutral-800 hover:bg-neutral-50 dark:hover:bg-neutral-700 px-3 py-1.5 text-neutral-700 dark:text-neutral-200 transition shadow-sm disabled:opacity-50"
          >
            <RefreshCw
              size={13}
              className={refreshing ? "animate-spin" : ""}
            />
            Refresh
          </button>
        </div>
      </header>

      <main className="max-w-2xl mx-auto px-4 sm:px-6 py-8 space-y-6">
        {/* Overall Banner */}
        <div
          className={`rounded-2xl border p-6 text-center transition-all duration-500 ${stateBg(overall)}`}
        >
          <StateIcon state={overall} size={40} />
          <h2 className={`text-2xl font-bold mt-3 ${stateColor(overall)}`}>
            {apiDown
              ? "API Unreachable"
              : stateLabel(overall)}
          </h2>
          <p className="text-sm text-neutral-500 dark:text-neutral-400 mt-1">
            {apiDown
              ? `Cannot connect to ${apiBase}`
              : ready?.status === "ready"
                ? "All subsystems operational"
                : "One or more subsystems need attention"}
          </p>
          {lastCheck && (
            <p className="text-[10px] text-neutral-400 mt-2">
              Last checked: {lastCheck}
            </p>
          )}
        </div>

        {/* API Unreachable state */}
        {apiDown && (
          <div className="rounded-2xl border border-red-200 dark:border-red-800 bg-red-50 dark:bg-red-950/30 p-5 space-y-3">
            <p className="text-sm font-semibold text-red-800 dark:text-red-200">
              Troubleshooting
            </p>
            <ul className="text-xs text-red-700 dark:text-red-300 space-y-1.5 list-disc pl-4">
              <li>
                Is the API running?{" "}
                <code className="bg-red-100 dark:bg-red-900 px-1 rounded text-[11px]">
                  docker compose up --build
                </code>
              </li>
              <li>Check port 8000 is not blocked or in use</li>
              <li>
                Verify NEXT_PUBLIC_API_BASE_URL = <code className="bg-red-100 dark:bg-red-900 px-1 rounded text-[11px]">{apiBase}</code>
              </li>
            </ul>
            <button
              onClick={fetchStatus}
              className="w-full mt-2 rounded-xl bg-red-600 hover:bg-red-700 text-white font-semibold py-2.5 text-sm transition shadow"
            >
              Retry Now
            </button>
          </div>
        )}

        {/* Subsystem Cards */}
        {!apiDown && (
          <div className="grid gap-3">
            <CheckCard
              label="Ollama LLM"
              icon={<Brain size={20} className="text-violet-600" />}
              check={ready?.checks.ollama ?? null}
            />
            <CheckCard
              label="RAG Index"
              icon={<Database size={20} className="text-blue-600" />}
              check={ready?.checks.rag_index ?? null}
            />
            <CheckCard
              label="OCR / Tesseract"
              icon={<ScanEye size={20} className="text-emerald-600" />}
              check={ready?.checks.ocr ?? null}
            />
            <CheckCard
              label="API Process"
              icon={<Server size={20} className="text-neutral-600 dark:text-neutral-400" />}
              check={
                health
                  ? { ok: true, detail: `${health.service} — ${health.status}` }
                  : null
              }
            />
          </div>
        )}

        {/* Raw JSON */}
        {!apiDown && (health || ready) && (
          <div className="rounded-2xl border border-neutral-200 dark:border-neutral-700 overflow-hidden">
            <button
              onClick={() => setJsonOpen(!jsonOpen)}
              className="w-full flex items-center justify-between px-5 py-3 text-xs font-semibold text-neutral-500 dark:text-neutral-400 hover:bg-neutral-100 dark:hover:bg-neutral-800 transition"
            >
              <span>Raw JSON</span>
              {jsonOpen ? (
                <ChevronUp size={14} />
              ) : (
                <ChevronDown size={14} />
              )}
            </button>
            {jsonOpen && (
              <pre className="px-5 pb-4 text-[11px] font-mono text-neutral-600 dark:text-neutral-400 overflow-x-auto max-h-80 whitespace-pre-wrap">
                {JSON.stringify({ health, ready }, null, 2)}
              </pre>
            )}
          </div>
        )}
      </main>
    </div>
  );
}
