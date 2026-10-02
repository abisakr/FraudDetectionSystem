import "tailwindcss";
import { BrowserRouter, Routes, Route } from 'react-router-dom';
import FraudDetection from "./components/FraudDetection";

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<FraudDetection />} />
        
        <Route path="*" element={<FraudDetection />} />
      </Routes>
    </BrowserRouter>
  );
}



export default App;