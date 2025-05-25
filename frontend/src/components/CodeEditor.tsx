import React from 'react';

interface CodeEditorProps {
  value: string;
  onChange: (value: string) => void;
}

export const CodeEditor: React.FC<CodeEditorProps> = ({ value, onChange }) => {
  return (
    <div className="relative">
      <textarea
        value={value}
        onChange={(e) => onChange(e.target.value)}
        className="w-full h-80 p-4 bg-gray-900 text-green-400 font-mono text-sm border border-gray-700 rounded-lg resize-none focus:outline-none focus:ring-2 focus:ring-purple-500 focus:border-transparent"
        placeholder="# Enter your Python code here..."
        style={{
          fontFamily: 'Monaco, Menlo, "Ubuntu Mono", monospace',
          lineHeight: '1.5',
          tabSize: 4,
        }}
        spellCheck={false}
      />
      <div className="absolute top-2 right-2">
        <div className="bg-gray-800 px-2 py-1 rounded text-xs text-gray-400 border border-gray-700">
          Python
        </div>
      </div>
    </div>
  );
};
