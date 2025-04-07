import MessageList from './MessageList'
import MessageInput from './MessageInput'

export default function ChatContainer({ messages, onSend }) {
  return (
    <div className="flex flex-col h-[calc(100vh-12rem)] max-w-3xl mx-auto bg-gray-50 rounded-lg shadow-sm p-4">
      <div className="flex-1 overflow-y-auto">
        <MessageList messages={messages} />
      </div>
      <div className="mt-4">
        <MessageInput onSend={onSend} />
      </div>
    </div>
  )
}
