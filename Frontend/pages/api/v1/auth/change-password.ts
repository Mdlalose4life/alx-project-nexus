import { NextApiRequest, NextApiResponse } from 'next';
import { makeApiCall } from '../../../../utils/api';

export default async function handler(
  req: NextApiRequest,
  res: NextApiResponse
) {
  if (req.method !== 'POST') {
    return res.status(405).json({ error: 'Method not allowed' });
  }

  try {
    const token = req.cookies.token || req.headers.authorization?.replace('Bearer ', '');
    
    if (!token) {
      return res.status(401).json({ error: 'Authentication required' });
    }

    const result = await makeApiCall('/auth/change-password/', {
      method: 'POST',
      headers: {
        Authorization: `Bearer ${token}`,
      },
      body: JSON.stringify(req.body),
    });

    if (result.error) {
      return res.status(result.status).json({ error: result.error });
    }

    res.status(200).json(result.data);
  } catch {
    res.status(500).json({ error: 'Internal server error' });
  }
}