import Link from "next/link";

export default function Home() {
  return (
    <div className="flex min-h-screen flex-col items-center justify-center p-24 bg-gray-50 text-gray-900">
      <main className="text-center space-y-6">
        <h1 className="text-4xl font-bold tracking-tight text-blue-900 sm:text-6xl">
          Healthcare Assistant AI
        </h1>
        <p className="text-xl leading-8 text-gray-600">
          Local-first triage assistant (RAG + safety + evaluation)
        </p>
        <div className="mt-10 flex items-center justify-center gap-x-6">
          <Link
            href="/chat"
            className="rounded-md bg-blue-600 px-3.5 py-2.5 text-sm font-semibold text-white shadow-sm hover:bg-blue-500 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-blue-600"
          >
            Open Chat
          </Link>
        </div>
      </main>
    </div>
  );
}
