import Chat from './components/Chat';

export default function App() {
  return (
    <div className="flex flex-col h-screen bg-gray-100">
      {/* Fixed Header */}
      <header className="bg-white shadow-sm fixed top-0 left-0 right-0 z-10">
        <div className="max-w-4xl mx-auto py-4 px-4 flex flex-col sm:flex-row sm:items-center sm:justify-between gap-2">
          <h1 className="text-2xl font-semibold text-gray-800 text-center sm:text-left">
            Knowva
          </h1>
          <p className="text-gray-600 text-center sm:text-left text-sm sm:text-base">
            Ask questions about Angel One services and insurance products
          </p>
        </div>
      </header>

      {/* Chat Scrollable Area */}
      <main className="flex-1 mt-[88px] mb-[64px] px-4 py-4 max-w-4xl mx-auto w-full">
        <Chat />
      </main>


      {/* Fixed Footer */}
      <footer className="bg-white border-t fixed bottom-0 left-0 right-0 z-10">
        <div className="max-w-4xl mx-auto py-4 px-4 text-center text-gray-600 text-sm">
          <p>Powered by RAG Technology</p>
        </div>
      </footer>
    </div>
  );
}
