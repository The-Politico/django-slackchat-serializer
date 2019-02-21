import assign from 'lodash/assign';
import keys from 'lodash/keys';
import mapValues from 'lodash/mapValues';

const blankifyUndefineds = data => {
  return mapValues(data, k => {
    if (typeof k === 'object') {
      return blankifyUndefineds(k);
    } else if (k === undefined) {
      return '';
    } else {
      return k;
    }
  });
};

export default (data, newPage) => {
  let output = assign({}, data);

  keys(output.meta).forEach(k => {
    output[`meta_${k}`] = output.meta[k];
  });

  delete output.meta;
  delete output.api_id;
  delete output.owner;

  output = blankifyUndefineds(output);

  if (output.publish_time === '') {
    output.publish_time = null;
  }

  if (newPage) {
    output.owner = window.LOGGED_IN_USER.pk;
  }

  return output;
};
