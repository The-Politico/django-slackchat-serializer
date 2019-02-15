import React from 'react';
import ReactDOM from 'react-dom';
import App from 'Components/App';

import getContentByName from 'Utils/getContentByName';
import find from 'lodash/find';
import listToObj from 'Utils/listToObj';

import './theme/base.scss';

const chatTypeLookup = listToObj(window.ALL_CHAT_TYPES.map(({ id }) => id), id => find(window.ALL_CHAT_TYPES, { id }));

const props = {
  chatTypeLookup,
  data: window.CHAT_DATA,
  page: getContentByName('PAGE'),

};

ReactDOM.render(
  <App {...props} />,
  document.getElementById('app')
);
