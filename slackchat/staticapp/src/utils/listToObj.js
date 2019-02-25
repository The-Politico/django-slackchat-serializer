import mapKeys from 'lodash/mapKeys';
import mapValues from 'lodash/mapValues';
import assign from 'lodash/assign';

/**
* Converts a list into an object
* @param {Array} list – The list whose items will be converted into the object's keys.
* @param {Fuction} [fillFunc] – A function called to fill the object's value. Fills with null if function is not provided.
* @return {Object} – An object with the keys of list's values and filled with data created from fillFunc.
*/
export default (list, fillFunc = () => null) => mapValues(
  mapKeys(
    assign({}, list), val => val
  ), fillFunc
);
