import assign from 'lodash/assign';
import getContentByName from 'Utils/getContentByName';

export const CMS_TOKEN = getContentByName('CMS_TOKEN');
export const WEBHOOK_TOKEN = getContentByName('WEBHOOK_TOKEN');
export const ROOT = getContentByName('API_ROOT');
export const WEBHOOKS = window.WEBHOOKS;

const headers = token => {
  const output = {
    headers: {
      'Content-Type': 'application/json',
    },
  };

  if (token) {
    output.headers['Authorization'] = `Token ${CMS_TOKEN}`;
  }

  return output;
};

export const GET = { method: 'GET' };
export const POST = { method: 'POST' };
export const PUT = { method: 'PUT' };
export const PATCH = { method: 'PATCH' };
export const DELETE = { method: 'DELETE' };

export const METHODS = [GET, POST, PUT, PATCH, DELETE];

export default (method, data) => {

};

const fetchCMS = (method, data) => {
  const url = `//${window.location.host}${ROOT}`;
  return fetch(url, assign(
    {},
    method,
    headers(CMS_TOKEN),
    { body: JSON.stringify(data) }
  ));
};

const fetchWebhooks = (method, data) => {
  return Promise.all(WEBHOOKS.map(({ endpoint }) => {
    const url = endpoint;
    return fetch(url, assign(
      {},
      method,
      headers(WEBHOOK_TOKEN),
      { body: JSON.stringify(Object.assign({}, { token: WEBHOOK_TOKEN }, data)) }
    ));
  }));
};

export const cms = {};
export const webhooks = {};

METHODS.forEach(m => {
  cms[m.method] = data => fetchCMS(m, data);
  webhooks[m.method] = data => fetchWebhooks(m, data);
});
