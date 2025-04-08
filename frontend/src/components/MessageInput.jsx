import { useState } from 'react'

export default function MessageInput({ onSend }) {
  const [inputValue, setInputValue] = useState('')

  const handleSubmit = (e) => {
    e.preventDefault()
    if (inputValue.trim()) {
      onSend(inputValue)
      setInputValue('')
    }
  }

  return (
    <form onSubmit={handleSubmit} className="flex gap-3">
      <input
        type="text"
        value={inputValue}
        onChange={(e) => setInputValue(e.target.value)}
        className="flex-1 bg-gray-50/50 border border-gray-200/50 rounded-xl px-5 py-3 focus:outline-none focus:ring-2 focus:ring-blue-500/40 focus:border-blue-500/40 transition-all duration-200 placeholder:text-gray-400"
        placeholder="Type a message..."
      />
      <button
        type="submit"
        className="bg-gradient-to-r from-blue-500 to-blue-600 hover:from-blue-600 hover:to-blue-700 text-white px-6 py-3 rounded-xl font-medium shadow-sm hover:shadow transition-all duration-200 disabled:opacity-50 disabled:cursor-not-allowed"
        disabled={!inputValue.trim()}
      >
        Send
      </button>
    </form>
  )
}
