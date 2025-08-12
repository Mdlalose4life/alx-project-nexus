import { NextApiRequest, NextApiResponse } from 'next';
import { makeApiCall } from '../../../../../utils/api';

export default async function handler(
  req: NextApiRequest,
  res: NextApiResponse
) {
  if (req.method !== 'GET') {
    return res.status(405).json({ error: 'Method not allowed' });
  }

  try {
    const queryParams = new URLSearchParams();
    
    if (req.query.q && typeof req.query.q === 'string') {
      queryParams.append('q', req.query.q);
    }
    if (req.query.category && typeof req.query.category === 'string') {
      queryParams.append('category', req.query.category);
    }
    if (req.query.page && typeof req.query.page === 'string') {
      queryParams.append('page', req.query.page);
    }
    if (req.query.limit && typeof req.query.limit === 'string') {
      queryParams.append('limit', req.query.limit);
    }

    const queryString = queryParams.toString();
    const endpoint = queryString ? `/products/search/?${queryString}` : '/products/search/';

    const result = await makeApiCall(endpoint, {
      method: 'GET',
    });

    if (result.error) {
      return res.status(result.status).json({ error: result.error });
    }

    res.status(200).json(result.data);
  } catch {
    res.status(500).json({ error: 'Internal server error' });
  }
}
