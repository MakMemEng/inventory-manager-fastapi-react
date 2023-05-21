import React, { useState, useEffect, ChangeEvent } from "react";
import axios from "axios";

type Material = {
  id: number;
  name: string;
  category: string;
  thickness: number;
  copper_thickness: number;
  size_x: number;
  size_y: number;
  maker: string;
  material_type: string;
};

const MaterialAPIFetch1: React.FC = () => {
  const [materials, setMaterials] = useState<Material[]>([]);
  useEffect(() => {
    axios.get("http://localhost:8000/materials").then((response) => {
      setMaterials(response.data);
    });
  }, []);
  return (
    <div>
      <table>
        <thead>
          <tr>
            <th>name</th>
            <th>category</th>
            <th>thickness</th>
            <th>copper_thickness</th>
            <th>size_x</th>
            <th>size_y</th>
            <th>maker</th>
            <th>material_type</th>
          </tr>
        </thead>
        <tbody>
          <tr>
            {materials.map((material) => (
              <td key={material.id}>{[material.name, material.category]}</td>
            ))}
          </tr>
        </tbody>
      </table>
    </div>
  );
};

export default MaterialAPIFetch1;
