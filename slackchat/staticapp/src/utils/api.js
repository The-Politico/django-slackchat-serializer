import assign from 'lodash/assign';
import getContentByName from './getContentByName';

export const CMS_TOKEN = getContentByName('CMS_TOKEN');
export const ROOT = getContentByName('API_ROOT');

const headers = {
  headers: {
    Authorization: `Token ${CMS_TOKEN}`,
    'Content-Type': 'application/json',
  },
};

export const GET = Object.assign({}, headers, { method: 'GET' });
export const POST = Object.assign({}, headers, { method: 'POST' });
export const PUT = Object.assign({}, headers, { method: 'PUT' });
export const PATCH = Object.assign({}, headers, { method: 'PATCH' });
export const DELETE = Object.assign({}, headers, { method: 'DELETE' });

export default (method, data) => {
  const url = `//${window.location.host}${ROOT}`;
  return fetch(url, assign({}, method, { body: JSON.stringify(data) }));
};
