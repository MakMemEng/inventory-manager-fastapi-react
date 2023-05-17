import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';

interface Material {
  id: number;
  name: string;
  category: string;
  thickness: number;
  copper_thickness: number;
  size_x: number;
  size_y: number;
  maker: string;
  material_type: string;
  // inventory: string;
}

const MaterialList: React.FC = () => {
  const [materials, setMaterials] = useState<Material[]>([]);
  const [error, setError] = useState<string | null>(null);
  const navigate = useNavigate();

  useEffect(() => {
    const fetchData = async () => {
      try {
        const response = await axios.get('http://localhost:8000/materials');
        setMaterials(response.data);
      } catch (error: any) {
        setError(error.message);
      }
    };

    fetchData();
  }, []);

  const handleEdit = (id: number) => {
    navigate(`/edit/${id}`);
  };

  const handleDelete = async (id: number) => {
    try {
      await axios.delete(`http://localhost:8000/materials/${id}`);
      setMaterials(materials.filter(material => material.id !== id));
    } catch (error: any) {
      setError(error.message);
    }
  };

  if (error) {
    return <div>Error: {error}</div>;
  }

  return (
    <table>
      <thead>
        <tr>
          <th>材料名</th>
          <th>分類名</th>
          <th>板厚</th>
          <th>銅箔厚</th>
          <th>sizeX</th>
          <th>sizeY</th>
          <th>メーカー名</th>
          <th>材質</th>
          <th>Actions</th>
        </tr>
      </thead>
      <tbody>
        {materials.map(material => (
          <tr key={material.id}>
            <td>{material.name}</td>
            <td>{material.category}</td>
            <td>{material.thickness}</td>
            <td>{material.copper_thickness}</td>
            <td>{material.size_x}</td>
            <td>{material.size_y}</td>
            <td>{material.maker}</td>
            <td>{material.material_type}</td>
            <td>
              <button onClick={() => handleEdit(material.id)}>Edit</button>
              <button onClick={() => handleDelete(material.id)}>Delete</button>
            </td>
          </tr>
        ))}
        <tr>
            <td colSpan={9}>
                <button onClick={() => navigate('/add')}>+追加l</button>
            </td>
        </tr>
      </tbody>
    </table>
  );
}

export default MaterialList;
