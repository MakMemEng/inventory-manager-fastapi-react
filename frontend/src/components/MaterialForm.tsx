import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';

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

const MaterialForm: React.FC = () => {
  const [material, setMaterial] = useState<Material>({
    id: 0,
    name: '',
    category: '',
    thickness: 0,
    copper_thickness: 0,
    size_x: 0,
    size_y: 0,
    maker: '',
    material_type: '',
    // inventory: '',
  });
  const navigate = useNavigate();

  const handleChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    setMaterial({ ...material, [event.target.name]: event.target.value });
  }

  const handleSubmit = (event: React.FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    // ここで API を呼び出して材料情報を登録します
    navigate('/');
  }

  return (
    <form onSubmit={handleSubmit}>
      <label>
        Material Name:
        <input type="text" name="name" value={material.name} onChange={handleChange} />
      </label>
      {/* 他のフィールドも同様に追加してください */}
      <button type="submit">Submit</button>
    </form>
  );
}

export default MaterialForm;
