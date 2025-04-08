export default function Message({ message }) {
  return (
    <div className={`flex ${message.sender === 'user' ? 'justify-end' : 'justify-start'} animate-fade-in`}>
      <div 
        className={`
          max-w-xs lg:max-w-md px-5 py-3 rounded-2xl 
          transform transition-all duration-200 hover:shadow-md
          ${message.sender === 'user' 
            ? 'bg-gradient-to-br from-blue-500 to-blue-600 text-white rounded-br-md ml-12' 
            : 'bg-gradient-to-br from-gray-50 to-gray-100 text-gray-800 rounded-bl-md mr-12 border border-gray-100/50'}
        `}
      >
        <p className="leading-relaxed whitespace-pre-wrap break-words">
          {message.text}
        </p>
      </div>
    </div>
  )
}
