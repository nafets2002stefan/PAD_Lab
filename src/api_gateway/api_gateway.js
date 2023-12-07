const express = require('express');
const axios = require('axios');
const rateLimit = require('express-rate-limit');

const app = express();
const PORT = 3000;

app.use(express.json()); // Middleware to parse JSON requests

const userServiceURL = 'http://127.0.0.1:5002/user';
const itemsServiceURL = 'http://127.0.0.1:5003/items';

const axiosInstance = axios.create({
  timeout: 5000 // Set a timeout of 5 seconds (adjust as needed)
});

// Create a rate limiter for the endpoints
const limiter = rateLimit({
  windowMs: 60 * 1000, // 1 minute
  max: 10, // Limit to 10 requests per minute per IP
});

// User Service Endpoints
app.get('/api/user', limiter, async (req, res) => {
  try {
    const response = await axiosInstance.get(userServiceURL);
    res.json(response.data);
  } catch (error) {
    if (error.response) {
      res.status(error.response.status).json(error.response.data);
    } else if (error.code === 'ECONNABORTED') {
      res.status(408).json({ error: 'Request Timeout' });
    } else {
      res.status(500).json({ error: 'Internal Server Error' });
    }
  }
});

app.post('/api/user', limiter, async (req, res) => {
  try {
    const response = await axiosInstance.post(userServiceURL, req.body, {
      headers: { 'Content-Type': 'application/json' },
    });
    res.json(response.data);
  } catch (error) {
    if (error.response) {
      res.status(error.response.status).json(error.response.data);
    } else if (error.code === 'ECONNABORTED') {
      res.status(408).json({ error: 'Request Timeout' });
    } else {
      res.status(500).json({ error: 'Internal Server Error' });
    }
  }
});

app.get('/api/items', limiter, async (req, res) => {
    try {
      const response = await axiosInstance.get(itemsServiceURL);
      res.json(response.data);
    } catch (error) {
      if (error.response) {
        res.status(error.response.status).json(error.response.data);
      } else if (error.code === 'ECONNABORTED') {
        res.status(408).json({ error: 'Request Timeout' });
      } else {
        res.status(500).json({ error: 'Internal Server Error' });
      }
    }
  });

  app.post('/api/items', limiter, async (req, res) => {
    try {
      const response = await axiosInstance.post(itemsServiceURL, req.body, {
        headers: { 'Content-Type': 'application/json' },
      });
      res.json(response.data);
    } catch (error) {
      if (error.response) {
        res.status(error.response.status).json(error.response.data);
      } else if (error.code === 'ECONNABORTED') {
        res.status(408).json({ error: 'Request Timeout' });
      } else {
        res.status(500).json({ error: 'Internal Server Error' });
      }
    }
  });

  app.get('/api/items/:item_id', limiter, async (req, res) => {
    const item_id = req.params.item_id;
    try {
        const response = await axiosInstance.get(`${itemsServiceURL}/${item_id}`);
      res.json(response.data);
    } catch (error) {
      if (error.response) {
        res.status(error.response.status).json(error.response.data);
      } else if (error.code === 'ECONNABORTED') {
        res.status(408).json({ error: 'Request Timeout' });
      } else {
        res.status(500).json({ error: 'Internal Server Error' });
      }
    }
  });

  app.delete('/api/items/:item_id', limiter, async (req, res) => {
    const item_id = req.params.item_id;
    try {
        const response = await axiosInstance.delete(`${itemsServiceURL}/${item_id}`);
      res.json(response.data);
    } catch (error) {
      if (error.response) {
        res.status(error.response.status).json(error.response.data);
      } else if (error.code === 'ECONNABORTED') {
        res.status(408).json({ error: 'Request Timeout' });
      } else {
        res.status(500).json({ error: 'Internal Server Error' });
      }
    }
  });

  app.get('/api/user/:user_id/cart', limiter, async (req, res) => {
    const user_id = req.params.user_id;
    try {
        const response = await axiosInstance.get(`${userServiceURL}/${user_id}/cart`);
      res.json(response.data);
    } catch (error) {
      if (error.response) {
        res.status(error.response.status).json(error.response.data);
      } else if (error.code === 'ECONNABORTED') {
        res.status(408).json({ error: 'Request Timeout' });
      } else {
        res.status(500).json({ error: 'Internal Server Error' });
      }
    }
  });

  app.post('/api/user/:user_id/cart', limiter, async (req, res) => {
    const user_id = req.params.user_id;
    try {
        const response = await axiosInstance.post(`${userServiceURL}/${user_id}/cart`);
      res.json(response.data);
    } catch (error) {
      if (error.response) {
        res.status(error.response.status).json(error.response.data);
      } else if (error.code === 'ECONNABORTED') {
        res.status(408).json({ error: 'Request Timeout' });
      } else {
        res.status(500).json({ error: 'Internal Server Error' });
      }
    }
  });


app.listen(PORT, () => {
  console.log(`API Gateway running at http://localhost:${PORT}`);
});