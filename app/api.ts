import type { NextApiRequest, NextApiResponse } from 'next';
import axios from 'axios';

export default async function handler(
  req: NextApiRequest,
  res: NextApiResponse
) {
  if (req.method === 'POST') {
    try {
      const response = await axios.post('http://localhost:5000/chat', req.body);
      res.status(200).json(response.data);
    } catch (error) {
      res.status(500).json({ error: 'Error processing chat request' });
    }
  } else {
    res.status(405).json({ error: 'Method not allowed' });
  }
}