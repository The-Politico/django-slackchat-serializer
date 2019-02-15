import keys from 'lodash/keys';
import uniq from 'lodash/uniq';

const isEqual = (a, b) => {
  if (a === b) {
    return true;
  }

  if ((a === '' && b === undefined) || (b === '' && a === undefined)) {
    return true;
  }

  return false;
};

const hasChanged = (original, change) => {
  const allKeys = uniq([...keys(original), ...keys(change)]);

  let changed = allKeys.some(k => {
    if ((k in original && typeof original[k] === 'object') || (k in change && typeof change[k] === 'object')) {
      const innerChanged = hasChanged(original[k], change[k]);
      if (innerChanged) {
        return true;
      }
    } else if (!isEqual(original[k], change[k])) {
      return true;
    }
  });

  return changed;
};

export default hasChanged;
