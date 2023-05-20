import React, { useState, ChangeEvent, useEffect } from "react";
import axios from "axios";

// Materialの型定義
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

// 初期値として空のMaterialオブジェクトを作成します
const initialMaterial: Material = {
  id: -Date.now(),
  name: "",
  category: "",
  thickness: 0.0,
  copper_thickness: 0,
  size_x: 0,
  size_y: 0,
  maker: "",
  material_type: ""
};

const MaterialsTable = () => {
  const [materials, setMaterials] = useState<Material[]>([]); // APIから取得したMaterialデータの配列
  const [newMaterials, setNewMaterials] = useState<Material[]>([]); // 新規に追加するMaterialの配列
  const [editingId, setEditingId] = useState<number | null>(null); // 編集中のMaterialのID
  const [error, setError] = useState<string | null>(null); // エラーが発生した場合のエラーメッセージ

  // フィールド名の配列
  const fields = Object.keys(initialMaterial) as Array<keyof Material>;
  const displayFields = fields.filter(field => field !== "id");
  // const fields: (keyof Material)[] = Object.keys(initialMaterial) as (keyof Material)[];

  useEffect(() => {
    // const fetchData = () => {
    //   axios.get("http://localhost:8000/materials")
    //     .then(response => {
    //       setMaterials(response.data);
    //       console.log("データの取得に成功しました。");
    //     })
    //     .catch(error => {
    //       setError(error.message);
    //       console.log("データの取得に失敗しました。");
    //     });
    // };
    //
    // fetchData();
    fetch("http://localhost:8000/materials", {method: "GET"})
      .then(response => response.json())
      .then(data => {
        setMaterials(data);
        console.log("データの取得に成功しました。");
      })
      .catch(error => {
        setError(error.message);
        console.log("データの取得に失敗しました。");
      });
  }, []);
  // return { materials, setMaterials, error };

  // Materialのフィールドを編集する関数
  const handleInputChange = (event: ChangeEvent<HTMLInputElement>,
                             id: number,
                             field: keyof Material,
                             isNew: boolean) => {
    const value = event.target.value;
    // isNewがtrueの場合は新規Materialの変更、falseの場合は既存Materialの変更
    if (isNew) {
      // 新規Materialの場合
      setNewMaterials(prevMaterials => prevMaterials.map(material =>
        material.id === id ? { ...material, [field]: value } : material
      ));
    } else {
      // 既存Materialの場合
      setMaterials(materials.map(material =>
        material.id === id ? { ...material, [field]: value } : material
      ));
    }
  };

  const handleCreate = async () => {
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

  const handleAdd = () => {
    // 既存のnewMaterials配列の末尾に新たなMaterialを追加します。
    setNewMaterials(prevMaterials => [...prevMaterials, initialMaterial]);
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

  const handleEdit = (id: number) => {
    setEditingId(id); // 編集モードを開始
  };

  const handleCancel = (id: number) => {
    if (id < 0) {
      // 新規Materialの場合
      setNewMaterials(prevMaterials => prevMaterials.filter(material => material.id !== id));
    } else {
      // 既存Materialの場合
      setEditingId(null);
    }
  }

  // 描画部分
  return (
    <table>
      <thead>
      {/* ヘッダーの描画 */}
      <tr>
        {displayFields.map(field => <th key={field}>{field}</th>)}
        <th>Actions</th>
      </tr>
      </thead>
      <tbody>
      {/* 既存Materialの描画 */}
      {materials.map(material => {
        return (
          <tr key={material.id}>
            {displayFields.map(field => (
              <td key={field}>
                {editingId === material.id ? ( // 編集モードの場合
                  <input
                    type="text"
                    value={material[field]}
                    onChange={event => handleInputChange(event, material.id, field, false)}
                  />
                ) : (
                  material[field]
                )}
              </td>
            ))}
            <td>
              {editingId === material.id ? ( // 編集モードの場合
                <>
                  <button onClick={() => handleUpdate(material.id)}>更新</button>
                  <button onClick={() => handleCancel(material.id)}>Cancel</button>
                </>
              ) : (
                <>
                  <button onClick={() => handleEdit(material.id)}>編集</button>
                </>
              )}
              <button onClick={() => handleDelete(material.id)}>削除</button>
            </td>
          </tr>
        );
      })}
      {/* 新規Materialの描画 */}
      {newMaterials.map((material, index) => {
          return (
            <tr key={material.id}>
              {displayFields.map(field => (
                <td key={field}>
                  <input
                    type="text"
                    value={material[field]}
                    onChange={event => handleInputChange(event, material.id, field, true)}
                  />
                </td>
              ))}
              <td>
                <button onClick={() => handleCreate}>作成</button>
                <button onClick={() => handleCancel(material.id)}>Cancel</button>
              </td>
            </tr>
          );
        }
      )}
      </tbody>
      <tfoot>
      <tr>
        <td colSpan={9}>
        {/*<td colSpan={displayFields.length + 1}>*/}
          <button onClick={handleAdd}>+新規作成</button>
        </td>
      </tr>
      </tfoot>
    </table>
  );
};

export default MaterialsTable;
