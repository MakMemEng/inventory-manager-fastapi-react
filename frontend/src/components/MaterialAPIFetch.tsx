import React, { useState, useEffect, ChangeEvent } from "react";
import axios from "axios";

interface Material {
  id: number | null;
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


const MaterialAPIFetch: React.FC = () => {

  const [materials, setMaterials] = useState<Material[]>([initialMaterial]); // APIから取得したMaterialデータの配列
  const [editedMaterial, setEditedMaterial] = useState<Material>(initialMaterial); // 編集中のMaterial
  const [error, setError] = useState<string | null>(null); // エラーが発生した場合のエラーメッセージ

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

  const newMaterial = (material: Material) => {
    let data = { ...material };
    const { id, ...dataWithoutId } = data;
    axios.post("http://localhost:8000/materials", dataWithoutId)
      .then(response => {
        setMaterials([...materials, response.data]);
        console.log("データの保存に成功しました。");
      })
      .catch(error => {
        console.log("データの保存に失敗しました。");
      });
  };
  ;

  const editMaterial = (material: Material) => {
    axios.put(`http://localhost:8000/materials/${material.id}`, material)
      .then(response => {
        setMaterials(materials.map(material => (
          material.id === response.data.id ? response.data : material
        )));
        console.log("データの更新に成功しました。");
        setEditedMaterial(initialMaterial);
      })
      .catch(error => {
        console.log("データの更新に失敗しました。");
      });
  };

  const deleteMaterial = (id: number) => {
    axios.delete(`http://localhost:8000/materials/${id}`)
      .then(response => {
        setMaterials(materials.filter(material => material.id !== id));
        console.log("データの削除に成功しました。");
      })
      .catch(error => {
        console.log("データの削除に失敗しました。");
      });
  };

  const handleInputChange = () => (event: ChangeEvent<HTMLInputElement>) => {
    const { name, value } = event.target;
    setEditedMaterial({ ...editedMaterial, [name]: value });
  };


  return (
    <table>
      <thead>
      {/* ヘッダーの描画 */}
      <tr>
        <th>材料名</th>
        <th>分類名</th>
        <th>板厚</th>
        <th>銅箔厚</th>
        <th>size_x</th>
        <th>size_y</th>
        <th>メーカー名</th>
        <th>材質</th>
      </tr>
      </thead>
      <tbody>
      { /* 既存Materialの描画 */
        materials.map(material => (
          <tr key={material.id}>
            <td>{material.name}</td>
            <td>{material.category}</td>
            <td>{material.thickness}</td>
            <td>{material.copper_thickness}</td>
            <td>{material.size_x}</td>
            <td>{material.size_y}</td>
            <td>{material.maker}</td>
            <td>{material.material_type}</td>

            <button type="button" onClick={() => setEditedMaterial(material)}>
              <i className="fas fa-pen"></i>
            </button>
            <button type="button" onClick={() => material.id !== null && deleteMaterial(material.id)}>
              <i className="fas fa-trash-alt"></i>
            </button>
          </tr>))
      }
      </tbody>
      <td><input type="text" name="name" value={editedMaterial.name}
                 onChange={handleInputChange()} placeholder="材質名" required /></td>
      <td><input type="text" name="category" value={editedMaterial.category}
                 onChange={handleInputChange()} placeholder="分類名" required /></td>
      <td><input type="number" name="thickness" value={editedMaterial.thickness}
                 onChange={handleInputChange()} placeholder="板厚" required /></td>
      <td><input type="number" name="copper_thickness" value={editedMaterial.copper_thickness}
                 onChange={handleInputChange()} placeholder="銅箔厚"
                 required /></td>
      <td><input type="number" name="size_x" value={editedMaterial.size_x}
                 onChange={handleInputChange()} placeholder="size_X" required /></td>
      <td><input type="number" name="size_y" value={editedMaterial.size_y}
                 onChange={handleInputChange()} placeholder="size_Y" required /></td>
      <td><input type="text" name="maker" value={editedMaterial.maker}
                 onChange={handleInputChange()} placeholder="メーカー名" required /></td>
      <td><input type="text" name="material_type" value={editedMaterial.material_type}
                 onChange={handleInputChange()} placeholder="材質" required /></td>

      {editedMaterial.id !== null ?
        <button type="button" onClick={() => editMaterial(editedMaterial)}>Update</button> :
        <button type="button" onClick={() => newMaterial(editedMaterial)}>Create</button>
      }
      {/*  <i className="fas fa-trash-alt"></i>*/}
      {/*</button>*/}


    </table>
  );
};

export default MaterialAPIFetch;
