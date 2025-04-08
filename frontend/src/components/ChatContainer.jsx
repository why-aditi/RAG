import MessageList from './MessageList'
import MessageInput from './MessageInput'

export default function ChatContainer({ messages, onSend }) {
  return (
    <div className="flex flex-col h-[calc(100vh-12rem)] max-w-3xl mx-auto bg-white/80 backdrop-blur-sm rounded-xl shadow-lg p-6 border border-gray-100/50 overflow-hidden">
      <div className="flex-1 overflow-y-auto pr-4 -mr-4 scroll-smooth scrollbar-thin scrollbar-thumb-gray-300 scrollbar-track-transparent hover:scrollbar-thumb-gray-400 transition-colors">
        <MessageList messages={messages} />
      </div>
      <div className="mt-6 pt-4 border-t border-gray-100/50">
        <MessageInput onSend={onSend} />
      </div>
    </div>
  )
}
