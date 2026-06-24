import React from 'react';
import { render, screen, waitFor, fireEvent } from '@testing-library/react';
import axios from 'axios';
import App from './App';

jest.mock('axios');

describe('App', () => {
  beforeEach(() => {
    jest.clearAllMocks();
  });

  test('renders the heading and tech subtitle', async () => {
    axios.get.mockResolvedValueOnce({ data: [] });
    render(<App />);
    expect(screen.getByText('DevOps Task Manager')).toBeInTheDocument();
    await waitFor(() =>
      expect(screen.getByText(/No tasks found/i)).toBeInTheDocument()
    );
  });

  test('renders fetched tasks and computes stats', async () => {
    axios.get.mockResolvedValueOnce({
      data: [
        { id: '1', title: 'First task', completed: false, created_at: '' },
        { id: '2', title: 'Done task', completed: true, created_at: '' },
      ],
    });
    render(<App />);
    await waitFor(() =>
      expect(screen.getByText('First task')).toBeInTheDocument()
    );
    expect(screen.getByText('Done task')).toBeInTheDocument();
    // Total stat card should read 2.
    expect(screen.getByText('2')).toBeInTheDocument();
  });

  test('shows an error message when the backend is unreachable', async () => {
    axios.get.mockRejectedValueOnce(new Error('network down'));
    render(<App />);
    await waitFor(() =>
      expect(
        screen.getByText(/Failed to fetch tasks/i)
      ).toBeInTheDocument()
    );
  });

  test('adds a task via the form', async () => {
    axios.get.mockResolvedValueOnce({ data: [] });
    axios.post.mockResolvedValueOnce({
      data: { id: '3', title: 'New task', completed: false, created_at: '' },
    });
    render(<App />);
    await waitFor(() =>
      expect(screen.getByText(/No tasks found/i)).toBeInTheDocument()
    );

    fireEvent.change(screen.getByPlaceholderText(/Add a new task/i), {
      target: { value: 'New task' },
    });
    fireEvent.click(screen.getByText('Add Task'));

    await waitFor(() =>
      expect(screen.getByText('New task')).toBeInTheDocument()
    );
    expect(axios.post).toHaveBeenCalledTimes(1);
  });
});
