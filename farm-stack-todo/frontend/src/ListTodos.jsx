// frontend/src/ListTodos.jsx
import { useState, useEffect } from "react"
import axios from "axios"

function ListTodos({ onSelectList }) {
  const [lists, setLists] = useState([])
  const [newListName, setNewListName] = useState("")

  const fetchLists = async () => {
    const res = await axios.get("/api/lists")
    setLists(res.data)
  }

  useEffect(() => { fetchLists() }, [])

  const createList = async (e) => {
    e.preventDefault()
    if (!newListName.trim()) return
    await axios.post("/api/lists", { name: newListName })
    setNewListName("")
    fetchLists()
  }

  const deleteList = async (id) => {
    await axios.delete("/api/lists/" + id)
    fetchLists()
  }

  return (
    <div>
      <h2>Your Todo Lists</h2>
      <form onSubmit={createList}>
        <input value={newListName}
          onChange={e => setNewListName(e.target.value)}
          placeholder="New list name..." />
        <button type="submit">+ Create</button>
      </form>
      {lists.length === 0 && <p>No lists yet. Create one!</p>}
      <ul>
        {lists.map(list => (
          <li key={list.id}>
            <span style={{cursor:"pointer",fontWeight:"bold"}}
              onClick={() => onSelectList(list.id)}>
              {list.name}
            </span>
            <span style={{marginLeft:8,color:"#888"}}>
              ({list.item_count} items)
            </span>
            <button onClick={() => deleteList(list.id)}
              style={{marginLeft:12,color:"red"}}>
              Delete
            </button>
          </li>
        ))}
      </ul>
    </div>
  )
}

export default ListTodos
