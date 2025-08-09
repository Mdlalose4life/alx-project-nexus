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
    const result = await makeApiCall('/auth/register/', {
      method: 'POST',
      body: JSON.stringify(req.body),
    });

    if (result.error) {
      return res.status(result.status).json({ error: result.error });
    }

    res.status(201).json(result.data);
  } catch (error) {
    res.status(500).json({ error: 'Internal server error' });
  }
}