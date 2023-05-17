import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import MaterialList from './components/MaterialList';
import MaterialForm from './components/MaterialForm';

const App: React.FC = () => {
  return (
    <Router>
      <Routes>
        <Route path="/materials" element={<MaterialList />} />
        <Route path="/materials/add" element={<MaterialForm />} />
      </Routes>
    </Router>
  );
};

export default App;
