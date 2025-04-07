import Message from './Message'

export default function MessageList({ messages }) {
  return (
    <div className="space-y-4">
      {messages.map((message) => (
        <div key={message.id} className="message-container">
          <Message message={message} />
          <div className="text-xs text-gray-500 mt-1 ml-2">
            {new Date(message.timestamp).toLocaleTimeString()}
          </div>
          {message.sources && (
            <div className="mt-1 ml-2 text-xs text-gray-600">
              <p className="font-semibold">Sources:</p>
              {message.sources.map((source, idx) => (
                <p key={idx} className="text-gray-500">
                  {source.filename}
                </p>
              ))}
            </div>
          )}
        </div>
      ))}
    </div>
  )
}
