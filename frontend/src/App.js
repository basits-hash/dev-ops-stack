import React, { useState, useEffect } from 'react';
import axios from 'axios';
import './App.css';

const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000/api';

function App() {
  const [tasks, setTasks] = useState([]);
  const [newTask, setNewTask] = useState('');
  const [filter, setFilter] = useState('all');
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    fetchTasks();
  }, []);

  const fetchTasks = async () => {
    try {
      setLoading(true);
      const response = await axios.get(`${API_URL}/tasks`);
      setTasks(response.data);
      setError('');
    } catch (err) {
      setError('Failed to fetch tasks. Is the backend running?');
    } finally {
      setLoading(false);
    }
  };

  const addTask = async (e) => {
    e.preventDefault();
    if (!newTask.trim()) return;
    try {
      const response = await axios.post(`${API_URL}/tasks`, { title: newTask });
      setTasks([response.data, ...tasks]);
      setNewTask('');
      setError('');
    } catch (err) {
      setError('Failed to add task.');
    }
  };

  const toggleTask = async (id) => {
    try {
      const task = tasks.find((t) => t.id === id);
      const response = await axios.put(`${API_URL}/tasks/${id}`, {
        completed: !task.completed,
      });
      setTasks(tasks.map((t) => (t.id === id ? response.data : t)));
      setError('');
    } catch (err) {
      setError('Failed to update task.');
    }
  };

  const deleteTask = async (id) => {
    try {
      await axios.delete(`${API_URL}/tasks/${id}`);
      setTasks(tasks.filter((t) => t.id !== id));
      setError('');
    } catch (err) {
      setError('Failed to delete task.');
    }
  };

  const filteredTasks = tasks.filter((task) => {
    if (filter === 'active') return !task.completed;
    if (filter === 'completed') return task.completed;
    return true;
  });

  const stats = {
    total: tasks.length,
    active: tasks.filter((t) => !t.completed).length,
    completed: tasks.filter((t) => t.completed).length,
  };

  return (
    <div className="App">
      <div className="container">
        <header className="header">
          <h1>DevOps Task Manager</h1>
          <p className="subtitle">React + FastAPI + MongoDB + Docker</p>
        </header>

        {error && <div className="error-message">{error}</div>}

        <div className="stats">
          <div className="stat-card">
            <div className="stat-value">{stats.total}</div>
            <div className="stat-label">Total</div>
          </div>
          <div className="stat-card">
            <div className="stat-value">{stats.active}</div>
            <div className="stat-label">Active</div>
          </div>
          <div className="stat-card">
            <div className="stat-value">{stats.completed}</div>
            <div className="stat-label">Done</div>
          </div>
        </div>

        <form onSubmit={addTask} className="task-form">
          <input
            type="text"
            placeholder="Add a new task..."
            value={newTask}
            onChange={(e) => setNewTask(e.target.value)}
            className="task-input"
          />
          <button type="submit" className="add-button">Add Task</button>
        </form>

        <div className="filters">
          {['all', 'active', 'completed'].map((f) => (
            <button
              key={f}
              className={`filter-button ${filter === f ? 'active' : ''}`}
              onClick={() => setFilter(f)}
            >
              {f.charAt(0).toUpperCase() + f.slice(1)}
            </button>
          ))}
        </div>

        {loading ? (
          <div className="loading">Loading tasks...</div>
        ) : (
          <div className="task-list">
            {filteredTasks.length === 0 ? (
              <div className="empty-state">
                <p>No tasks found. Add one to get started!</p>
              </div>
            ) : (
              filteredTasks.map((task) => (
                <div key={task.id} className={`task-item ${task.completed ? 'completed' : ''}`}>
                  <div className="task-content">
                    <input
                      type="checkbox"
                      checked={task.completed}
                      onChange={() => toggleTask(task.id)}
                      className="task-checkbox"
                    />
                    <span className="task-title">{task.title}</span>
                  </div>
                  <button onClick={() => deleteTask(task.id)} className="delete-button">
                    Delete
                  </button>
                </div>
              ))
            )}
          </div>
        )}

        <footer className="footer">
          <p>Built by Syed Basit Sherazi</p>
          <p>React · FastAPI · MongoDB · Docker · GitHub Actions</p>
        </footer>
      </div>
    </div>
  );
}

export default App;
