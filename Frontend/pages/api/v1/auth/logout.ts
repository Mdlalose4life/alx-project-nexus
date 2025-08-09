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
    // Get token from cookies or headers
    const token = req.cookies.token || req.headers.authorization?.replace('Bearer ', '');
    
    const result = await makeApiCall('/auth/logout/', {
      method: 'POST',
      headers: {
        Authorization: token ? `Bearer ${token}` : '',
      },
    });

    if (result.error) {
      return res.status(result.status).json({ error: result.error });
    }

    // Clear the token cookie
    res.setHeader('Set-Cookie', 'token=; HttpOnly; Path=/; Max-Age=0');
    
    res.status(200).json(result.data);
  } catch (error) {
    res.status(500).json({ error: 'Internal server error' });
  }
}