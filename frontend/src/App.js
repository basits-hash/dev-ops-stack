import React, { useState, useEffect } from 'react';
import axios from 'axios';
import './App.css';

// Use environment variable for production, fallback to localhost for development
const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000/api';
const IS_DEMO_MODE = !process.env.REACT_APP_API_URL && window.location.hostname.includes('github.io');

function App() {
  const [tasks, setTasks] = useState([]);
  const [newTask, setNewTask] = useState('');
  const [filter, setFilter] = useState('all');
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    if (IS_DEMO_MODE) {
      // Load tasks from localStorage for demo mode
      const savedTasks = localStorage.getItem('demoTasks');
      if (savedTasks) {
        setTasks(JSON.parse(savedTasks));
      } else {
        // Set default demo tasks
        const demoTasks = [
          { _id: '1', title: 'Welcome to DevOps Task Manager!', completed: false, createdAt: new Date().toISOString() },
          { _id: '2', title: 'This is running in Demo Mode (no backend needed)', completed: false, createdAt: new Date().toISOString() },
          { _id: '3', title: 'Try adding your own tasks!', completed: false, createdAt: new Date().toISOString() },
          { _id: '4', title: 'Data is saved in your browser', completed: true, createdAt: new Date().toISOString() },
        ];
        setTasks(demoTasks);
        localStorage.setItem('demoTasks', JSON.stringify(demoTasks));
      }
      setLoading(false);
      setError('');
    } else {
      fetchTasks();
    }
  }, []);

  // Save to localStorage in demo mode
  useEffect(() => {
    if (IS_DEMO_MODE && tasks.length > 0) {
      localStorage.setItem('demoTasks', JSON.stringify(tasks));
    }
  }, [tasks]);

  const fetchTasks = async () => {
    try {
      setLoading(true);
      const response = await axios.get(`${API_URL}/tasks`);
      setTasks(response.data);
      setError('');
    } catch (err) {
      setError('Failed to fetch tasks. Please ensure the backend is running.');
      console.error('Error fetching tasks:', err);
    } finally {
      setLoading(false);
    }
  };

  const addTask = async (e) => {
    e.preventDefault();
    if (!newTask.trim()) return;

    if (IS_DEMO_MODE) {
      // Demo mode - add to local state
      const newTaskObj = {
        _id: Date.now().toString(),
        title: newTask,
        completed: false,
        createdAt: new Date().toISOString(),
      };
      setTasks([newTaskObj, ...tasks]);
      setNewTask('');
      setError('');
    } else {
      try {
        const response = await axios.post(`${API_URL}/tasks`, {
          title: newTask,
        });
        setTasks([...tasks, response.data]);
        setNewTask('');
        setError('');
      } catch (err) {
        setError('Failed to add task');
        console.error('Error adding task:', err);
      }
    }
  };

  const toggleTask = async (id) => {
    if (IS_DEMO_MODE) {
      // Demo mode - toggle in local state
      setTasks(tasks.map((t) => 
        t._id === id ? { ...t, completed: !t.completed } : t
      ));
      setError('');
    } else {
      try {
        const task = tasks.find((t) => t._id === id);
        const response = await axios.put(`${API_URL}/tasks/${id}`, {
          completed: !task.completed,
        });
        setTasks(tasks.map((t) => (t._id === id ? response.data : t)));
        setError('');
      } catch (err) {
        setError('Failed to update task');
        console.error('Error updating task:', err);
      }
    }
  };

  const deleteTask = async (id) => {
    if (IS_DEMO_MODE) {
      // Demo mode - delete from local state
      setTasks(tasks.filter((t) => t._id !== id));
      setError('');
    } else {
      try {
        await axios.delete(`${API_URL}/tasks/${id}`);
        setTasks(tasks.filter((t) => t._id !== id));
        setError('');
      } catch (err) {
        setError('Failed to delete task');
        console.error('Error deleting task:', err);
      }
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
          <h1>🚀 DevOps Task Manager</h1>
          <p className="subtitle">Full-Stack Application with CI/CD Pipeline</p>
        </header>

        {error && <div className="error-message">{error}</div>}

        <div className="stats">
          <div className="stat-card">
            <div className="stat-value">{stats.total}</div>
            <div className="stat-label">Total Tasks</div>
          </div>
          <div className="stat-card">
            <div className="stat-value">{stats.active}</div>
            <div className="stat-label">Active</div>
          </div>
          <div className="stat-card">
            <div className="stat-value">{stats.completed}</div>
            <div className="stat-label">Completed</div>
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
          <button type="submit" className="add-button">
            Add Task
          </button>
        </form>

        <div className="filters">
          <button
            className={`filter-button ${filter === 'all' ? 'active' : ''}`}
            onClick={() => setFilter('all')}
          >
            All
          </button>
          <button
            className={`filter-button ${filter === 'active' ? 'active' : ''}`}
            onClick={() => setFilter('active')}
          >
            Active
          </button>
          <button
            className={`filter-button ${filter === 'completed' ? 'active' : ''}`}
            onClick={() => setFilter('completed')}
          >
            Completed
          </button>
        </div>

        {loading ? (
          <div className="loading">Loading tasks...</div>
        ) : (
          <div className="task-list">
            {filteredTasks.length === 0 ? (
              <div className="empty-state">
                <p>No tasks found. Add one to get started! 🎯</p>
              </div>
            ) : (
              filteredTasks.map((task) => (
                <div
                  key={task._id}
                  className={`task-item ${task.completed ? 'completed' : ''}`}
                >
                  <div className="task-content">
                    <input
                      type="checkbox"
                      checked={task.completed}
                      onChange={() => toggleTask(task._id)}
                      className="task-checkbox"
                    />
                    <span className="task-title">{task.title}</span>
                  </div>
                  <button
                    onClick={() => deleteTask(task._id)}
                    className="delete-button"
                  >
                    🗑️
                  </button>
                </div>
              ))
            )}
          </div>
        )}

        <footer className="footer">
          <p>Built with React, Python FastAPI, MongoDB</p>
          <p>🐳 Containerized | ☸️ AKS Ready | 🔄 Azure DevOps CI/CD</p>
          {IS_DEMO_MODE && (
            <p className="demo-badge">
              🎯 Demo Mode - Data saved locally in browser
            </p>
          )}
        </footer>
      </div>
    </div>
  );
}

export default App;
