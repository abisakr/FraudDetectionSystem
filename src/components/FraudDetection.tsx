import { useState, FormEvent } from 'react';

// Define the exact shape matching the new machine learning model
interface TransactionData {
  amount: number | '';
  oldbalanceOrg: number | '';
  newbalanceOrig: number | '';
  oldbalanceDest: number | '';
  newbalanceDest: number | '';
  type: string;
}

export default function FraudDetection() {
  const [formData, setFormData] = useState<TransactionData>({
    amount: '',
    oldbalanceOrg: '',
    newbalanceOrig: '',
    oldbalanceDest: '',
    newbalanceDest: '',
    type: 'TRANSFER'
  });

  const [isFraud, setIsFraud] = useState<boolean | null>(null);
  const [loading, setLoading] = useState<boolean>(false);
  const [error, setError] = useState<string | null>(null);

  const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement>) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: value
    }));
  };

  const handleSubmit = async (e: FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError(null);
    setIsFraud(null);

    try {
      const response = await fetch('http://localhost:5000/api/predict', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(formData),
      });

      const data = await response.json();

      if (data.status === 'success') {
        setIsFraud(data.is_fraud);
      } else {
        setError(data.message);
      }
    } catch (err) {
      setError('Failed to connect to the server. Is Flask running?');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-slate-900 via-slate-800 to-black py-12 px-4 sm:px-6 lg:px-8 transition-all">
      
      <div className="w-full max-w-2xl mx-auto bg-white/95 backdrop-blur-xl rounded-3xl shadow-[0_0_40px_rgba(0,0,0,0.5)] border border-white/20 overflow-hidden p-8 sm:p-10 transform transition-all duration-500">
        
        <div className="mb-10 text-center">
          <h2 className="text-3xl sm:text-4xl font-extrabold text-transparent bg-clip-text bg-gradient-to-r from-blue-600 to-cyan-600 tracking-tight mb-2">
            AI Fraud Detection
          </h2>
          <p className="text-gray-500 text-sm font-medium">Scan transaction parameters for suspicious activity</p>
        </div>
        
        <form onSubmit={handleSubmit} className="space-y-5">
          <div className="grid grid-cols-1 sm:grid-cols-2 gap-5">
            
            {/* Amount */}
            <div className="group sm:col-span-2">
              <label className="block text-xs font-bold text-gray-500 uppercase tracking-wider mb-1 group-focus-within:text-blue-600 transition-colors">Transaction Amount</label>
              <input 
                type="number" step="0.01" name="amount" required value={formData.amount} onChange={handleChange} 
                placeholder="e.g., 5000.00"
                className="block w-full rounded-xl border-0 bg-gray-50/50 p-3.5 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-200 transition-all duration-200 focus:bg-white focus:ring-2 focus:ring-inset focus:ring-blue-600 focus:outline-none" 
              />
            </div>
            
            {/* Old Balance Origin */}
            <div className="group">
              <label className="block text-xs font-bold text-gray-500 uppercase tracking-wider mb-1 group-focus-within:text-blue-600 transition-colors">Sender Old Balance</label>
              <input 
                type="number" step="0.01" name="oldbalanceOrg" required value={formData.oldbalanceOrg} onChange={handleChange} 
                placeholder="e.g., 10000.00"
                className="block w-full rounded-xl border-0 bg-gray-50/50 p-3.5 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-200 transition-all duration-200 focus:bg-white focus:ring-2 focus:ring-inset focus:ring-blue-600 focus:outline-none" 
              />
            </div>

            {/* New Balance Origin */}
            <div className="group">
              <label className="block text-xs font-bold text-gray-500 uppercase tracking-wider mb-1 group-focus-within:text-blue-600 transition-colors">Sender New Balance</label>
              <input 
                type="number" step="0.01" name="newbalanceOrig" required value={formData.newbalanceOrig} onChange={handleChange} 
                placeholder="e.g., 5000.00"
                className="block w-full rounded-xl border-0 bg-gray-50/50 p-3.5 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-200 transition-all duration-200 focus:bg-white focus:ring-2 focus:ring-inset focus:ring-blue-600 focus:outline-none" 
              />
            </div>

            {/* Old Balance Destination */}
            <div className="group">
              <label className="block text-xs font-bold text-gray-500 uppercase tracking-wider mb-1 group-focus-within:text-blue-600 transition-colors">Receiver Old Balance</label>
              <input 
                type="number" step="0.01" name="oldbalanceDest" required value={formData.oldbalanceDest} onChange={handleChange} 
                placeholder="e.g., 0.00"
                className="block w-full rounded-xl border-0 bg-gray-50/50 p-3.5 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-200 transition-all duration-200 focus:bg-white focus:ring-2 focus:ring-inset focus:ring-blue-600 focus:outline-none" 
              />
            </div>

            {/* New Balance Destination */}
            <div className="group">
              <label className="block text-xs font-bold text-gray-500 uppercase tracking-wider mb-1 group-focus-within:text-blue-600 transition-colors">Receiver New Balance</label>
              <input 
                type="number" step="0.01" name="newbalanceDest" required value={formData.newbalanceDest} onChange={handleChange} 
                placeholder="e.g., 5000.00"
                className="block w-full rounded-xl border-0 bg-gray-50/50 p-3.5 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-200 transition-all duration-200 focus:bg-white focus:ring-2 focus:ring-inset focus:ring-blue-600 focus:outline-none" 
              />
            </div>

            {/* Transaction Type */}
            <div className="group sm:col-span-2 mt-2">
              <label className="block text-xs font-bold text-gray-500 uppercase tracking-wider mb-1 group-focus-within:text-blue-600 transition-colors">Transaction Type</label>
              <select name="type" value={formData.type} onChange={handleChange} className="block w-full rounded-xl border-0 bg-gray-50/50 p-3.5 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-200 transition-all duration-200 focus:bg-white focus:ring-2 focus:ring-inset focus:ring-blue-600 focus:outline-none cursor-pointer">
                <option value="TRANSFER">TRANSFER</option>
                <option value="CASH_OUT">CASH OUT</option>
                <option value="CASH_IN">CASH IN</option>
                <option value="PAYMENT">PAYMENT</option>
                <option value="DEBIT">DEBIT</option>
              </select>
            </div>
          </div>

          <button 
            type="submit" 
            disabled={loading} 
            className="w-full mt-8 bg-gradient-to-r from-blue-600 to-cyan-600 text-white font-bold py-4 px-4 rounded-xl shadow-lg hover:shadow-blue-500/30 transform transition-all duration-200 hover:-translate-y-1 active:translate-y-0 disabled:opacity-70 disabled:cursor-not-allowed flex justify-center items-center group"
          >
            {loading ? (
              <span className="flex items-center gap-2">
                <svg className="animate-spin h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                  <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                  <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                </svg>
                Scanning...
              </span>
            ) : (
              "Run Security Scan"
            )}
          </button>
        </form>

        {/* Error Message */}
        {error && (
          <div className="mt-6 p-4 bg-red-50 text-red-600 rounded-xl border border-red-100 flex items-start gap-3">
            <p className="text-sm font-medium">{error}</p>
          </div>
        )}

        {/* Prediction Results */}
        {isFraud !== null && !loading && (
          <div className={`mt-8 p-6 rounded-2xl border text-center shadow-inner relative overflow-hidden transition-all duration-500 ${isFraud ? 'bg-red-50 border-red-200' : 'bg-emerald-50 border-emerald-200'}`}>
            
            <div className="relative z-10 flex flex-col items-center">
              {isFraud ? (
                <>
                  <svg className="w-12 h-12 text-red-600 mb-2 animate-bounce" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z"></path></svg>
                  <h3 className="text-2xl font-black text-red-700 tracking-tight">FRAUD DETECTED</h3>
                  <p className="text-red-600/80 text-sm mt-1 font-medium">This transaction matches known malicious patterns.</p>
                </>
              ) : (
                <>
                  <svg className="w-12 h-12 text-emerald-500 mb-2" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"></path></svg>
                  <h3 className="text-2xl font-black text-emerald-700 tracking-tight">TRANSACTION SAFE</h3>
                  <p className="text-emerald-600/80 text-sm mt-1 font-medium">No fraudulent anomalies detected.</p>
                </>
              )}
            </div>
          </div>
        )}

      </div>
    </div>
  );
}