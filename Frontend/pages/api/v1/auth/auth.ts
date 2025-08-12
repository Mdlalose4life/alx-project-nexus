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
    const result = await makeApiCall('/auth/login/', {
      method: 'POST',
      body: JSON.stringify(req.body),
    });

    if (result.error) {
      return res.status(result.status).json({ error: result.error });
    }

    // If login successful, you might want to set cookies here
    // res.setHeader('Set-Cookie', `token=${result.data.token}; HttpOnly; Path=/`);

    res.status(200).json(result.data);
  } catch {
    res.status(500).json({ error: 'Internal server error' });
  }
}
