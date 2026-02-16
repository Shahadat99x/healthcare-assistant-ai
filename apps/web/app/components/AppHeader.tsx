"use client";

import Link from "next/link";
import { useTheme } from "next-themes";
import { useSyncExternalStore, type ReactNode } from "react";
import { Moon, Sun, Upload } from "lucide-react";

function ThemeToggle() {
  const { theme, setTheme, resolvedTheme } = useTheme();
  const mounted = useSyncExternalStore(
    () => () => {},
    () => true,
    () => false
  );
  const current = resolvedTheme ?? theme;

  if (!mounted) return null;

  const toggleTheme = () => {
    setTheme(current === "dark" ? "light" : "dark");
  };

  return (
    <button
      onClick={toggleTheme}
      className="p-2 rounded-full hover:bg-neutral-100 dark:hover:bg-neutral-800 text-neutral-500 dark:text-neutral-400 transition"
      aria-label="Toggle theme"
    >
      {current === "dark" ? <Sun size={18} /> : <Moon size={18} />}
    </button>
  );
}

export default function AppHeader({ children }: { children?: ReactNode }) {
  return (
    <header className="sticky top-0 z-10 flex items-center justify-between border-b border-neutral-200 dark:border-neutral-800 bg-white/80 dark:bg-neutral-950/80 backdrop-blur px-3 sm:px-5 py-2.5 transition-colors duration-300">
      <div className="flex items-center gap-2 sm:gap-3 min-w-0">
        <h1 className="text-base sm:text-lg font-bold text-neutral-900 dark:text-white tracking-tight truncate flex items-center gap-2">
          🏥 <span className="hidden sm:inline">Healthcare Assistant</span>
          <span className="sm:hidden">Assistant</span>
        </h1>
        <a
          href="/intake"
          className="inline-flex items-center gap-1.5 text-xs font-semibold bg-emerald-600 hover:bg-emerald-700 text-white px-3 py-1.5 rounded-xl transition shadow-sm"
        >
          <Upload size={13} />
          <span className="hidden sm:inline">Upload</span>
        </a>
      </div>
      <div className="flex items-center gap-2">
        {children}
        {children && (
          <div className="w-px h-6 bg-neutral-200 dark:bg-neutral-800 mx-1" />
        )}
        <ThemeToggle />
      </div>
    </header>
  );
}
