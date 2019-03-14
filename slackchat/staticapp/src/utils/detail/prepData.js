import assign from 'lodash/assign';
import keys from 'lodash/keys';
import mapValues from 'lodash/mapValues';

const clean = (data, schema) => {
  return mapValues(data, (val, key) => {
    if (typeof val === 'object') {
      return clean(val, schema.properties[key]);
    } else if (key in schema.properties && schema.properties[key].type === 'string' && val === undefined) {
      return '';
    } else if (val === undefined) {
      return null;
    } else {
      return val;
    }
  });
};

export default (data, schema, newPage) => {
  let output = assign({}, data);

  output = clean(output, schema.json);

  keys(output.meta).forEach(k => {
    output[`meta_${k}`] = output.meta[k];
  });

  delete output.meta;
  delete output.api_id;
  delete output.owner;

  if (output.publish_time === '') {
    output.publish_time = null;
  }

  if (newPage) {
    output.owner = window.LOGGED_IN_USER.pk;
  }

  return output;
};
