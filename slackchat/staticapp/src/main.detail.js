import React from 'react';
import ReactDOM from 'react-dom';
import App from 'Components/Detail';

import getContentByName from 'Utils/getContentByName';

import './theme/base.scss';

const props = {
  data: window.DATA,
  page: getContentByName('PAGE'),

};

ReactDOM.render(
  <App {...props} />,
  document.getElementById('app')
);
