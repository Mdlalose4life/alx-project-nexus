import { NextApiRequest, NextApiResponse } from 'next';
import { makeApiCall } from '../../../../utils/api';

export default async function handler(
  req: NextApiRequest,
  res: NextApiResponse
) {
  if (req.method !== 'GET') {
    return res.status(405).json({ error: 'Method not allowed' });
  }

  const { slug } = req.query;

  if (!slug || typeof slug !== 'string') {
    return res.status(400).json({ error: 'Invalid slug parameter' });
  }

  try {
    const result = await makeApiCall(`/business-categories/${slug}/`, {
      method: 'GET',
    });

    if (result.error) {
      return res.status(result.status).json({ error: result.error });
    }

    res.status(200).json(result.data);
  } catch (error) {
    res.status(500).json({ error: 'Internal server error' });
  }
}