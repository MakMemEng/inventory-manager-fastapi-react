import React, { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import axios from "axios";

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

interface Props {
  material: Material;
  editing: boolean;
  onChange: (event: React.ChangeEvent<HTMLInputElement>,
             id: number,
             key: keyof Material) => void;
  onUpdate: (id: number) => void;
  onCancel: () => void;
  onEdit: (id: number) => void;
  onDelete: (id: number) => void;
}

const MaterialRow: React.FC<Props> = ({
                                        material,
                                        editing,
                                        onChange,
                                        onUpdate,
                                        onCancel,
                                        onEdit,
                                        onDelete
                                      }) => (
  <tr>
    {Object.keys(material).map((key) => (
      <td key={key}>
        {editing ? (
          <input type="text" value={material[key as keyof Material]} onChange={e => onChange(e, material.id, key as keyof Material)} />
        ) : (
          material[key as keyof Material]
        )}
      </td>
    ))}
    <td>
      {editing ? (
        <>
          <button onClick={() => onUpdate(material.id)}>Update</button>
          <button onClick={onCancel}>Cancel</button>
        </>
      ) : (
        <>
          <button onClick={() => onEdit(material.id)}>Edit</button>
          <button onClick={() => onDelete(material.id)}>Delete</button>
        </>
      )}
    </td>
  </tr>
);

const MaterialList = ({ ...rest }) => {
  const [materials, setMaterials] = useState<Material[]>([]);
  const [newMaterials, setNewMaterials] = useState<Material[]>([]);
  const [editingId, setEditingId] = useState<number | null>(null);
  const [error, setError] = useState<string | null>(null);
  const navigate = useNavigate();

  useEffect(() => {
    const fetchData = async () => {
      try {
        const response = await axios.get("http://localhost:8000/materials");
        setMaterials(response.data);
      } catch (error: any) {
        setError(error.message);
      }
    };

    fetchData();
  }, []);

  const addNewMaterial = () => {
    // 初期状態のMaterialオブジェクトを作成します。
    const newMaterial: Material = {
      id: Date.now(),  // 一時的なIDとして現在のタイムスタンプを使用
      name: "",
      category: "",
      thickness: 0,
      copper_thickness: 0,
      size_x: 0,
      size_y: 0,
      maker: "",
      material_type: ""
    };

    // 既存のnewMaterials配列の末尾に新たなMaterialを追加します。
    setNewMaterials(prevMaterials => [...prevMaterials, newMaterial]);
  };


  const saveNewMaterials = async () => {
    const newMaterials = materials.filter(material => material.id < 0); // 未保存のMaterialを取得
    for (const material of newMaterials) {
      try {
        const response = await axios.post("http://localhost:8000/materials", material); // MaterialをサーバーにPOST
        const savedMaterial = response.data; // レスポンスから保存されたMaterialを取得
        setMaterials(prevMaterials => {
          const index = prevMaterials.findIndex(m => m.id === material.id); // 保存前のMaterialのインデックスを取得
          const newMaterials = [...prevMaterials]; // 現在のMaterials配列をコピー
          newMaterials[index] = savedMaterial; // 保存されたMaterialで置き換え
          return newMaterials; // 新しいMaterials配列で状態を更新
        });
      } catch (error: any) {
        console.error(error); // エラーログを出力
      }
    }
  };

  const handleNewMaterialChange = (index: number, field: keyof Material, value: string | number) => {
    setNewMaterials(prevMaterials => prevMaterials.map((material, i) =>
      i === index ? { ...material, [field]: value } : material
    ));
  };

  const handleDeleteNewMaterial = (index: number) => {
    setNewMaterials(prevMaterials => prevMaterials.filter((_, i) => i !== index));
  };

  const handleEdit = (id: number) => {
    setEditingId(id); // 編集モードに入るためにIDをセット
  };

  const handleInputChange = (event: React.ChangeEvent<HTMLInputElement>, id: number, field: keyof Material) => {
    setMaterials(materials.map(material => {
      if (material.id === id) {
        return { ...material, [field]: event.target.value };
      } else {
        return material;
      }
    }));
  };

  const handleUpdate = async (id: number) => {
    const materialToUpdate = materials.find(material => material.id === id);
    if (!materialToUpdate) {
      return;
    }

    try {
      const response = await axios.put(`http://localhost:8000/materials/${id}`, materialToUpdate);
      setMaterials(materials.map(material => material.id === id ? response.data : material));
      setEditingId(null);  // 編集モードを終了
    } catch (error: any) {
      setError(error.message);
    }
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
        <MaterialRow
          key={material.id}
          material={material}
          editing={editingId === material.id}
          onChange={handleInputChange}
          onUpdate={() => handleUpdate(material.id)}
          onCancel={() => setEditingId(null)}
          onEdit={() => handleEdit(material.id)}
          onDelete={() => handleDelete(material.id)}
        />
      ))}
      {newMaterials.map((material, index) => (
        <MaterialRow
          key={index}
          material={material}
          editing={true}
          onChange={(e, _, key) => handleNewMaterialChange(index, key, e.target.value)}
          onDelete={() => handleDeleteNewMaterial(index)}
          onUpdate={() => {}}
          onCancel={() => {}}
          onEdit={() => {}}
        />
      ))}
      <tr>
        <td colSpan={9}>
          <button onClick={addNewMaterial}>+追加</button>
          <button onClick={saveNewMaterials}>登録</button>
        </td>
      </tr>
      </tbody>
    </table>
  );
};

export default MaterialList;
