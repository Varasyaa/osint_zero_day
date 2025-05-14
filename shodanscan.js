import React, { useState } from 'react';
import axios from 'axios';

function ShodanScan() {
  const [target, setTarget] = useState('');
  const [result, setResult] = useState(null);

  const scan = async () => {
    try {
      const res = await axios.post('/api/shodan', { target });
      setResult(res.data);
    } catch (err) {
      alert("Scan failed");
    }
  };

  return (
    <div className="p-4">
      <h2 className="text-xl font-bold mb-2">Shodan Scan</h2>
      <input
        type="text"
        placeholder="Enter IP or domain"
        value={target}
        onChange={(e) => setTarget(e.target.value)}
        className="border p-2 mr-2"
      />
      <button onClick={scan} className="bg-blue-600 text-white px-4 py-2 rounded">Scan</button>

      {result && (
        <div className="mt-4">
          <h3 className="text-lg font-bold">Results</h3>
          <pre className="bg-gray-100 p-2 rounded">{JSON.stringify(result, null, 2)}</pre>
        </div>
      )}
    </div>
  );
}

export default ShodanScan;
