import keys from 'lodash/keys';
import uniq from 'lodash/uniq';

const isEqual = (a, b) => {
  if (a === b) {
    return true;
  }

  if (
    (a === '' && b === undefined) ||
    (b === '' && a === undefined) ||
    (a === '' && b === null) ||
    (b === '' && a === null)
  ) {
    return true;
  }

  return false;
};

const hasChanged = (original, change) => {
  if (original === undefined && change !== undefined) {
    return true;
  }

  const allKeys = uniq([...keys(original), ...keys(change)]);

  console.log(allKeys);

  let changed = allKeys.some(k => {
    console.log(k);
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
