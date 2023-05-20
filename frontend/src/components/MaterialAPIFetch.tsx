import React, { useState, useEffect, ChangeEvent } from "react";
import axios from "axios";

interface Material {
  id: string | number | null;
  name: string;
  category: string;
  thickness: number;
  copper_thickness: number;
  size_x: number;
  size_y: number;
  maker: string;
  material_type: string;
}

// Materialの初期値を設定
const initialMaterial: Material = {
  id: null,
  name: "",
  category: "",
  thickness: 0.0,
  copper_thickness: 0,
  size_x: 0,
  size_y: 0,
  maker: "",
  material_type: ""
};

interface MaterialRowProps {
  material: Material;
  onEdit: (material: Material) => void;
  onDelete: (id: string | number) => void;
}

const MaterialRow: React.FC<MaterialRowProps> = ({ material, onEdit, onDelete }) => {
  const [isEditing, setIsEditing] = useState(false);
  const [tempMaterial, setTempMaterial] = useState(material);

  const handleInputChange = (event: ChangeEvent<HTMLInputElement>) => {
    const { name, value } = event.target;
    setTempMaterial({ ...tempMaterial, [name]: value });
  };

  const handleEdit = () => {
    setIsEditing(true);
  };

  const handleSave = () => {
    setIsEditing(false);
    onEdit(tempMaterial);
  };

  const handleCancel = () => {
    setIsEditing(false);
    setTempMaterial(material);
  };

  if (isEditing) {
    return (
      <tr>
        {Object.keys(tempMaterial).map((key) => (
          key !== "id" && (
            <td key={key}>
              <input
                type="text"
                name={key}
                value={tempMaterial[key as keyof Material] as string}
                onChange={handleInputChange}
              />
            </td>
          )
        ))}
        <td>
          <button onClick={handleSave}>保存</button>
          <button onClick={handleCancel}>キャンセル</button>
        </td>
      </tr>
    );
  } else {
    return (
      <tr>
        {Object.keys(material).map((key) => (
          key !== "id" && (
            <td key={key}>{material[key as keyof Material]}</td>
          )
        ))}
        <td>
          <button onClick={handleEdit}>編集</button>
          <button onClick={() => {
            if(material.id !== null) onDelete(material.id)
          }}>削除
          </button>
        </td>
      </tr>
    );
  }
};

const MaterialAPIFetch: React.FC = () => {
  const [materials, setMaterials] = useState<Material[]>([]);
  const [newMaterialId, setNewMaterialId] = useState(1);

  useEffect(() => {
    axios.get("http://localhost:8000/materials")
      .then(response => {
        setMaterials(response.data);
        console.log("データの取得に成功しました。");
      })
      .catch(error => {
        console.log("データの取得に失敗しました。");
      });
  }, []);

  const handleNewButtonClick = () => {
    setMaterials([...materials, { ...initialMaterial, id: `new-${newMaterialId}` }]);
    setNewMaterialId(newMaterialId + 1);
  };

  const handleInputChange = () => (event: ChangeEvent<HTMLInputElement>) => {
    const { name, value } = event.target;
    setEditedMaterial({ ...editedMaterial, [name]: value });
  };

  const handleDelete = (id: string | number) => {
    if (typeof id === "string" && id.startsWith("new-")) {
      setMaterials(materials.filter(material => material.id !== id));
    } else {
      axios.delete(`http://localhost:8000/materials/${id}`)
        .then(() => {
          setMaterials(materials.filter(material => material.id !== id));
        });
    }
  };

  return (
    <div>
      <button onClick={handleNewButtonClick}>新規作成</button>
      <table>
        <tbody>
        {materials.map((material) => (
          <MaterialRow
            key={material.id}
            material={material}
            onEdit={handleEdit}
            onDelete={handleDelete}
          />
        ))}
        </tbody>
      </table>
    </div>
  );
};

export default MaterialAPIFetch;
