import find from 'lodash/find';
import listToObj from 'Utils/listToObj';

const chatTypeLookup = listToObj(window.ALL_CHAT_TYPES.map(({ id }) => id), id => find(window.ALL_CHAT_TYPES, { id }));

export default id => chatTypeLookup[id];
