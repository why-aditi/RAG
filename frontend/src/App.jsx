import Chat from './components/Chat';

export default function App() {
  return (
    <div className="flex flex-col h-screen bg-gradient-to-br from-blue-50 to-indigo-50">
      {/* Fixed Header */}
      <header className="bg-white/80 backdrop-blur-sm shadow-lg fixed top-0 left-0 right-0 z-10 transition-all duration-200">
        <div className="max-w-4xl mx-auto py-6 px-6 flex flex-col sm:flex-row sm:items-center sm:justify-between gap-3">
          <h1 className="text-3xl font-bold text-indigo-900 text-center sm:text-left hover:text-indigo-700 transition-colors duration-200">
            Knowva
          </h1>
          <p className="text-indigo-600/80 text-center sm:text-left text-sm sm:text-base font-medium">
            Ask questions about Angel One services and insurance products
          </p>
        </div>
      </header>

      {/* Chat Scrollable Area */}
      <main className="flex-1 mt-[104px] mb-[72px] px-6 py-6 max-w-4xl mx-auto w-full">
        <Chat />
      </main>

      {/* Fixed Footer */}
      <footer className="bg-white/80 backdrop-blur-sm border-t border-indigo-100 fixed bottom-0 left-0 right-0 z-10 transition-all duration-200">
        <div className="max-w-4xl mx-auto py-5 px-6 text-center text-indigo-600/80 text-sm font-medium">
          <p>Powered by RAG Technology</p>
        </div>
      </footer>
    </div>
  );
}
