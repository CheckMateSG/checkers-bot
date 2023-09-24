import React from 'react'

interface Todo {
    userId: number;
    title: string;
}
const achievements = async () => {
    const res = await fetch('https://jsonplaceholder.typicode.com/todos', {cache: 'no-store'})
    const todos: Todo[] = await res.json();
  
    return (
        <>
            <div>achievements</div>
                <p>{new Date().toLocaleTimeString()}</p>
                <ul>
                    {todos.map(Todo => <li key = {Todo.userId}>{Todo.title}</li>)}
                </ul>
        </>
  )
}

export default achievements