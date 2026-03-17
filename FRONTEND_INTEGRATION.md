# Frontend Integration Guide

This guide explains how to integrate the FindKE backend with your React frontend application using GraphQL (recommended) and REST API.

## Table of Contents
- [Setup](#setup)
- [GraphQL Integration](#graphql-integration)
- [REST API Integration](#rest-api-integration)
- [WebSocket Integration](#websocket-integration)
- [File Uploads](#file-uploads)
- [Authentication](#authentication)
- [Best Practices](#best-practices)

## Setup

### Backend URLs

- **GraphQL Endpoint**: `http://localhost:8000/graphql/`
- **REST API Base**: `http://localhost:8000/api/`
- **WebSocket Base**: `ws://localhost:8000/ws/`
- **Media Files**: `http://localhost:8000/media/`

### Environment Variables

Create a `.env` file in your React project:

```env
REACT_APP_API_URL=http://localhost:8000
REACT_APP_GRAPHQL_URL=http://localhost:8000/graphql/
REACT_APP_WS_URL=ws://localhost:8000/ws/
```

## GraphQL Integration

### 1. Install Apollo Client

```bash
npm install @apollo/client graphql
```

### 2. Configure Apollo Client

Create `src/apollo/client.js`:

```javascript
import { ApolloClient, InMemoryCache, HttpLink, split } from '@apollo/client';
import { setContext } from '@apollo/client/link/context';
import { GraphQLWsLink } from '@apollo/client/link/subscriptions';
import { getMainDefinition } from '@apollo/client/utilities';
import { createClient } from 'graphql-ws';

// HTTP link for queries and mutations
const httpLink = new HttpLink({
  uri: process.env.REACT_APP_GRAPHQL_URL,
});

// WebSocket link for subscriptions
const wsLink = new GraphQLWsLink(
  createClient({
    url: process.env.REACT_APP_WS_URL + 'graphql/',
    connectionParams: () => ({
      authToken: localStorage.getItem('token'),
    }),
  })
);

// Auth link to add token to headers
const authLink = setContext((_, { headers }) => {
  const token = localStorage.getItem('token');
  return {
    headers: {
      ...headers,
      authorization: token ? `Token ${token}` : '',
    },
  };
});

// Split link based on operation type
const splitLink = split(
  ({ query }) => {
    const definition = getMainDefinition(query);
    return (
      definition.kind === 'OperationDefinition' &&
      definition.operation === 'subscription'
    );
  },
  wsLink,
  authLink.concat(httpLink)
);

const client = new ApolloClient({
  link: splitLink,
  cache: new InMemoryCache(),
});

export default client;
```

### 3. Wrap App with Apollo Provider

In `src/index.js`:

```javascript
import React from 'react';
import ReactDOM from 'react-dom/client';
import { ApolloProvider } from '@apollo/client';
import client from './apollo/client';
import App from './App';

const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(
  <React.StrictMode>
    <ApolloProvider client={client}>
      <App />
    </ApolloProvider>
  </React.StrictMode>
);
```

### 4. Example Queries and Mutations

Create `src/graphql/queries.js`:

```javascript
import { gql } from '@apollo/client';

// User Queries
export const GET_ME = gql`
  query GetMe {
    me {
      id
      username
      email
      firstName
      lastName
      bio
      avatar
      followerCount
      followingCount
    }
  }
`;

export const GET_USERS = gql`
  query GetUsers($search: String) {
    users(search: $search) {
      id
      username
      email
      bio
      avatar
      followerCount
      followingCount
    }
  }
`;

// Post Queries
export const GET_FEED = gql`
  query GetFeed($limit: Int, $offset: Int) {
    feed(limit: $limit, offset: $offset) {
      id
      user {
        id
        username
        avatar
      }
      content
      image
      likeCount
      commentCount
      repostCount
      createdAt
    }
  }
`;

// Mutations
export const REGISTER = gql`
  mutation Register($input: RegisterInput!) {
    register(input: $input) {
      token
      user {
        id
        username
        email
      }
    }
  }
`;

export const LOGIN = gql`
  mutation Login($email: String!, $password: String!) {
    login(email: $email, password: $password) {
      token
      user {
        id
        username
        email
      }
    }
  }
`;

export const CREATE_POST = gql`
  mutation CreatePost($input: CreatePostInput!) {
    createPost(input: $input) {
      post {
        id
        content
        image
        createdAt
      }
    }
  }
`;

export const FOLLOW_USER = gql`
  mutation FollowUser($userId: ID!) {
    followUser(userId: $userId) {
      success
      user {
        id
        username
      }
    }
  }
`;

// Subscriptions
export const MESSAGE_SENT = gql`
  subscription MessageSent($conversationId: ID!) {
    messageSent(conversationId: $conversationId) {
      id
      sender {
        id
        username
        avatar
      }
      content
      createdAt
    }
  }
`;
```

### 5. Using Queries and Mutations in Components

```javascript
import React from 'react';
import { useQuery, useMutation } from '@apollo/client';
import { GET_FEED, CREATE_POST } from './graphql/queries';

function Feed() {
  const { loading, error, data, refetch } = useQuery(GET_FEED, {
    variables: { limit: 20, offset: 0 },
  });

  const [createPost] = useMutation(CREATE_POST, {
    onCompleted: () => refetch(),
  });

  const handleCreatePost = async (content) => {
    try {
      await createPost({
        variables: {
          input: { content },
        },
      });
    } catch (err) {
      console.error('Error creating post:', err);
    }
  };

  if (loading) return <p>Loading...</p>;
  if (error) return <p>Error: {error.message}</p>;

  return (
    <div>
      {data.feed.map((post) => (
        <div key={post.id}>
          <p>{post.user.username}</p>
          <p>{post.content}</p>
          <p>Likes: {post.likeCount}</p>
        </div>
      ))}
    </div>
  );
}

export default Feed;
```

## REST API Integration

### 1. Install Axios

```bash
npm install axios
```

### 2. Configure Axios Instance

Create `src/api/axios.js`:

```javascript
import axios from 'axios';

const api = axios.create({
  baseURL: process.env.REACT_APP_API_URL + '/api',
  headers: {
    'Content-Type': 'application/json',
  },
});

// Add token to requests
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('token');
    if (token) {
      config.headers.Authorization = `Token ${token}`;
    }
    return config;
  },
  (error) => Promise.reject(error)
);

// Handle token expiration
api.interceptors.response.use(
  (response) => response,
  async (error) => {
    if (error.response?.status === 401) {
      localStorage.removeItem('token');
      window.location.href = '/login';
    }
    return Promise.reject(error);
  }
);

export default api;
```

### 3. API Service Functions

Create `src/api/services.js`:

```javascript
import api from './axios';

// Auth
export const register = (userData) => api.post('/users/register/', userData);
export const login = (credentials) => api.post('/users/login/', credentials);
export const getMe = () => api.get('/users/me/');

// Posts
export const getPosts = (params) => api.get('/posts/posts/', { params });
export const getFeed = () => api.get('/posts/posts/feed/');
export const createPost = (postData) => api.post('/posts/posts/', postData);
export const likePost = (postId) => api.post(`/posts/posts/${postId}/like/`);
export const unlikePost = (postId) => api.post(`/posts/posts/${postId}/unlike/`);

// Users
export const getUsers = (search) => api.get('/users/profiles/', { params: { search } });
export const getUser = (userId) => api.get(`/users/profiles/${userId}/`);
export const followUser = (userId) => api.post(`/users/profiles/${userId}/follow/`);
export const unfollowUser = (userId) => api.post(`/users/profiles/${userId}/unfollow/`);

// Chat
export const getConversations = () => api.get('/chat/conversations/');
export const getMessages = (conversationId) =>
  api.get('/chat/messages/', { params: { conversation: conversationId } });
export const sendMessage = (messageData) => api.post('/chat/messages/', messageData);

// Notifications
export const getNotifications = () => api.get('/notifications/');
export const markNotificationRead = (notificationId) =>
  api.post(`/notifications/${notificationId}/mark_read/`);
export const getUnreadCount = () => api.get('/notifications/unread_count/');
```

### 4. Using Services in Components

```javascript
import React, { useEffect, useState } from 'react';
import { getFeed, createPost } from './api/services';

function Feed() {
  const [posts, setPosts] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadFeed();
  }, []);

  const loadFeed = async () => {
    try {
      const response = await getFeed();
      setPosts(response.data);
    } catch (error) {
      console.error('Error loading feed:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleCreatePost = async (content) => {
    try {
      await createPost({ content });
      loadFeed();
    } catch (error) {
      console.error('Error creating post:', error);
    }
  };

  if (loading) return <p>Loading...</p>;

  return (
    <div>
      {posts.map((post) => (
        <div key={post.id}>
          <p>{post.user.username}</p>
          <p>{post.content}</p>
        </div>
      ))}
    </div>
  );
}

export default Feed;
```

## WebSocket Integration

### 1. Chat WebSocket

Create `src/hooks/useChat.js`:

```javascript
import { useEffect, useRef, useState } from 'react';

export const useChat = (conversationId, onMessage) => {
  const ws = useRef(null);
  const [connected, setConnected] = useState(false);

  useEffect(() => {
    const token = localStorage.getItem('token');
    const wsUrl = `${process.env.REACT_APP_WS_URL}chat/${conversationId}/`;

    ws.current = new WebSocket(wsUrl);

    ws.current.onopen = () => {
      console.log('WebSocket connected');
      setConnected(true);
    };

    ws.current.onmessage = (event) => {
      const data = JSON.parse(event.data);
      if (data.type === 'message') {
        onMessage(data.data);
      } else if (data.type === 'typing') {
        console.log('User typing:', data.username);
      }
    };

    ws.current.onerror = (error) => {
      console.error('WebSocket error:', error);
    };

    ws.current.onclose = () => {
      console.log('WebSocket disconnected');
      setConnected(false);
    };

    return () => {
      if (ws.current) {
        ws.current.close();
      }
    };
  }, [conversationId, onMessage]);

  const sendMessage = (content) => {
    if (ws.current && connected) {
      ws.current.send(
        JSON.stringify({
          type: 'chat_message',
          message: content,
        })
      );
    }
  };

  const sendTyping = (isTyping) => {
    if (ws.current && connected) {
      ws.current.send(
        JSON.stringify({
          type: 'typing',
          is_typing: isTyping,
        })
      );
    }
  };

  return { sendMessage, sendTyping, connected };
};
```

### 2. Using Chat Hook

```javascript
import React, { useState } from 'react';
import { useChat } from './hooks/useChat';

function ChatRoom({ conversationId }) {
  const [messages, setMessages] = useState([]);
  const [inputValue, setInputValue] = useState('');

  const { sendMessage, sendTyping, connected } = useChat(
    conversationId,
    (message) => {
      setMessages((prev) => [...prev, message]);
    }
  );

  const handleSend = () => {
    if (inputValue.trim()) {
      sendMessage(inputValue);
      setInputValue('');
    }
  };

  const handleTyping = () => {
    sendTyping(true);
    setTimeout(() => sendTyping(false), 3000);
  };

  return (
    <div>
      <div>
        {messages.map((msg) => (
          <div key={msg.id}>
            <strong>{msg.sender.username}:</strong> {msg.content}
          </div>
        ))}
      </div>
      <input
        value={inputValue}
        onChange={(e) => {
          setInputValue(e.target.value);
          handleTyping();
        }}
        onKeyPress={(e) => e.key === 'Enter' && handleSend()}
        disabled={!connected}
      />
      <button onClick={handleSend} disabled={!connected}>
        Send
      </button>
    </div>
  );
}

export default ChatRoom;
```

## File Uploads

### Image Upload with REST API

```javascript
const handleImageUpload = async (file) => {
  const formData = new FormData();
  formData.append('content', 'My new post');
  formData.append('image', file);

  try {
    const response = await api.post('/posts/posts/', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });
    console.log('Post created:', response.data);
  } catch (error) {
    console.error('Upload error:', error);
  }
};

// Usage in component
<input
  type="file"
  accept="image/*"
  onChange={(e) => handleImageUpload(e.target.files[0])}
/>
```

## Authentication

### Auth Context

Create `src/context/AuthContext.js`:

```javascript
import React, { createContext, useState, useEffect } from 'react';
import { getMe } from '../api/services';

export const AuthContext = createContext();

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    checkAuth();
  }, []);

  const checkAuth = async () => {
    const token = localStorage.getItem('token');
    if (token) {
      try {
        const response = await getMe();
        setUser(response.data);
      } catch (error) {
        localStorage.removeItem('token');
      }
    }
    setLoading(false);
  };

  const login = (token, userData) => {
    localStorage.setItem('token', token);
    setUser(userData);
  };

  const logout = () => {
    localStorage.removeItem('token');
    setUser(null);
  };

  return (
    <AuthContext.Provider value={{ user, login, logout, loading }}>
      {children}
    </AuthContext.Provider>
  );
};
```

## Best Practices

### 1. Error Handling

```javascript
try {
  const response = await createPost({ content });
  // Success
} catch (error) {
  if (error.response) {
    // Server responded with error
    console.error('Server error:', error.response.data);
  } else if (error.request) {
    // Request made but no response
    console.error('Network error');
  } else {
    // Something else happened
    console.error('Error:', error.message);
  }
}
```

### 2. Loading States

```javascript
const [loading, setLoading] = useState(false);

const handleAction = async () => {
  setLoading(true);
  try {
    await someApiCall();
  } finally {
    setLoading(false);
  }
};
```

### 3. Pagination

```javascript
const [page, setPage] = useState(1);
const [hasMore, setHasMore] = useState(true);

const loadMore = async () => {
  const response = await getPosts({ page, limit: 20 });
  setHasMore(response.data.next !== null);
  setPage((prev) => prev + 1);
};
```

### 4. Optimistic Updates

```javascript
const handleLike = async (postId) => {
  // Optimistically update UI
  setPosts((prev) =>
    prev.map((post) =>
      post.id === postId
        ? { ...post, likeCount: post.likeCount + 1, isLiked: true }
        : post
    )
  );

  try {
    await likePost(postId);
  } catch (error) {
    // Revert on error
    setPosts((prev) =>
      prev.map((post) =>
        post.id === postId
          ? { ...post, likeCount: post.likeCount - 1, isLiked: false }
          : post
      )
    );
  }
};
```

## Troubleshooting

### CORS Issues

If you encounter CORS errors, ensure the backend `.env` file has:

```env
CORS_ALLOWED_ORIGINS=http://localhost:3000,http://localhost:3001
```

### WebSocket Connection Failures

1. Check WebSocket URL format (ws:// not http://)
2. Verify authentication token is being sent
3. Check browser console for specific error messages

### Authentication Issues

1. Ensure token is stored in localStorage
2. Check token format in Authorization header
3. Verify token hasn't expired (refresh if using JWT)

## Additional Resources

- [Django REST Framework Docs](https://www.django-rest-framework.org/)
- [GraphQL Documentation](https://graphql.org/learn/)
- [Apollo Client Docs](https://www.apollographql.com/docs/react/)
- [Django Channels Docs](https://channels.readthedocs.io/)
