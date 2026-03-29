// frontend/src/App.jsx
import { useState } from "react"
import ListTodos from "./ListTodos"
import SingleTodoList from "./SingleTodoList"

function App() {
  const [selectedListId, setSelectedListId] = useState(null)
  return (
    <div className="app">
      <h1>FARM Todo App</h1>
      {selectedListId ? (
        <SingleTodoList
          listId={selectedListId}
          onBack={() => setSelectedListId(null)}
        />
      ) : (
        <ListTodos onSelectList={setSelectedListId} />
      )}
    </div>
  )
}
export default App