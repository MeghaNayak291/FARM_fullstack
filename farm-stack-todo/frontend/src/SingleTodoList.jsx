// frontend/src/SingleTodoList.jsx
import { useState, useEffect } from "react"
import axios from "axios"

function SingleTodoList({ listId, onBack }) {
  const [list, setList] = useState(null)
  const [newItemLabel, setNewItemLabel] = useState("")

  const fetchList = async () => {
    const res = await axios.get("/api/lists/" + listId)
    setList(res.data)
  }

  useEffect(() => { fetchList() }, [listId])

  const addItem = async (e) => {
    e.preventDefault()
    if (!newItemLabel.trim()) return
    const res = await axios.post("/api/lists/" + listId + "/items", { label: newItemLabel })
    setList(res.data)
    setNewItemLabel("")
  }

  const toggleCheck = async (itemId, currentState) => {
    const res = await axios.patch("/api/lists/" + listId + "/checked_state",
      { item_id: itemId, checked_state: !currentState })
    setList(res.data)
  }

  const deleteItem = async (itemId) => {
    const res = await axios.delete("/api/lists/" + listId + "/items/" + itemId)
    setList(res.data)
  }

  if (!list) return <p>Loading...</p>

  return (
    <div>
      <button onClick={onBack}>Back to Lists</button>
      <h2>{list.name}</h2>
      <form onSubmit={addItem}>
        <input value={newItemLabel}
          onChange={e => setNewItemLabel(e.target.value)}
          placeholder="New item..." />
        <button type="submit">+ Add</button>
      </form>
      {list.items.length === 0 && <p>No items yet.</p>}
      <ul>
        {list.items.map(item => (
          <li key={item.id} style={{display:"flex",alignItems:"center",gap:8}}>
            <input type="checkbox" checked={item.checked}
              onChange={() => toggleCheck(item.id, item.checked)} />
            <span style={{
              textDecoration: item.checked ? "line-through" : "none",
              color: item.checked ? "#888" : "inherit"
            }}>
              {item.label}
            </span>
            <button onClick={() => deleteItem(item.id)}
              style={{marginLeft:"auto",color:"red"}}>
              X
            </button>
          </li>
        ))}
      </ul>
    </div>
  )
}
export default SingleTodoList