import { useState } from "react";

const URL = "https://DOMAIN";
const LOCALHOST = "http://127.0.0.1:8000";

export function InputField() {
  const [query, setQuery] = useState("");
  const [response, setResponse] = useState<string | null>(null);

  const fetchData = async () => {
    try {
      const res = await fetch(`${LOCALHOST}/items/1?q=${encodeURIComponent(query)}`);
      if (!res.ok) {
        setResponse(`${res.status}`);
        return;
      }
      const data = await res.json();
      setResponse(`200 Ok: ${JSON.stringify(data, null, 2)}`);
    } catch (error) {
      setResponse(`Network Error ${error}`);
    }
  };

  return (
    <div className="flex-grow flex flex-col justify-center items-center space-y-4">
      <div className="flex items-center space-x-2">
        <input
          type="text"
          placeholder="Enter request"
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          className="p-2 border border-gray-300 rounded"
        />
        <button onClick={fetchData} className="p-2 bg-blue-500 text-white rounded">
          Make request
        </button>
      </div>
      {response && (
        <div className="p-2 border border-gray-300 rounded bg-gray-100 w-80 text-center">
          {response}
        </div>
      )}
    </div>
  );
}
