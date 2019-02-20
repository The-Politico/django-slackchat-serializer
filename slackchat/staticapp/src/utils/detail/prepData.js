import assign from 'lodash/assign';
import keys from 'lodash/keys';

export default (data, newPage) => {
  const output = assign({}, data);

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
